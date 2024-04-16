import streamlit as st
import firebase_admin
import io
import json
from firebase_admin import credentials, db
from PIL import Image

if not firebase_admin._apps:
    cred = credentials.Certificate("path_firebase/firebase_credentials.json")
    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://trueguide-846cb-default-rtdb.firebaseio.com/"}
    )


def app():
    def display_data(data):
        num_items = len(data)
        num_columns = min(num_items, 5)  # Atur jumlah kolom maksimum di sini

        # Hitung jumlah baris per kolom
        rows_per_column = num_items // num_columns + (num_items % num_columns > 0)

        for i in range(rows_per_column):
            cols = st.columns(num_columns)
            for j in range(num_columns):
                idx = i + j * rows_per_column
                if idx < num_items:
                    key, value = list(data.items())[idx]
                    cols[j].write(f"Kategori: {value['category']}")
                    cols[j].write(f"Judul Aktivitas: {value['judul_aktivitas']}")
                    cols[j].write(
                        f"Deskripsi Aktivitas: {value['deskripsi_aktivitas']}"
                    )
                    cols[j].write(f"Hari Aktivitas: {value['hari_aktivitas']}")
                    cols[j].image(
                        value["gambar_aktivitas"],
                        caption="Gambar Aktivitas",
                        use_column_width=True,
                    )
                    cols[j].write(f"Body Aktivitas: {value['body_aktivitas']}")
                    cols[j].markdown("---")

    def get_data(path):
        ref = db.reference(path)
        data = ref.get()
        return data

    def add_data(path, new_data):
        ref = db.reference(path)
        ref.push(new_data)

    def update_data(path, data_key, updated_data):
        ref = db.reference(path)
        ref.child(data_key).update(updated_data)

    def delete_data(path, data_key):
        ref = db.reference(path)
        ref.child(data_key).delete()

    st.title("Data Kegiatan Mingguan")

    path = [
        "/SM7",
        "/SALES_SKILL",
        "/PRODUCT_&_KNOWLEDGE",
        "/PRU_SALES_ACADEMY",
        "/PERSONAL_EXCELLENT_MENTALITY_ATTITUDE",
    ]

    st.title("List Data:")
    selected_path = st.selectbox("Select path:", path)
    data = get_data(selected_path)

    if data:
        display_data(data)
    else:
        st.write("Data tidak ditemukan.")

    st.title("Tambah Data")
    body_aktivitas = st.text_input("Hari Aktivitas", help="Misalnya: Senin")
    category_list = [
        "SM7",
        "SALES_SKILL",
        "PRODUCT_&_KNOWLEDGE",
        "PRU_SALES_ACADEMY",
        "PERSONAL_EXCELLENT_MENTALITY_ATTITUDE",
    ]
    category = st.selectbox("Category:", category_list)
    deskripsi_aktivitas = st.text_input(
        "Deskripsi Aktivitas",
        help="Misalnya: Kegiatan kumpul-kumpul bersama partner bisnis",
    )
    gambar_aktivitas = st.text_input("Gambar Aktivitas")
    hari_aktivitas = st.text_input("Tanggal Aktivitas", help="Misalnya: 21 April 2024")
    judul_aktivitas = st.text_input("Judul Aktivitas", help="Misalnya: True Workshop")

    if st.button("Tambah Data"):
        new_data = {
            "body_aktivitas": body_aktivitas,
            "category": category,
            "deskripsi_aktivitas": deskripsi_aktivitas,
            "gambar_aktivitas": gambar_aktivitas,
            "hari_aktivitas": hari_aktivitas,
            "judul_aktivitas": judul_aktivitas,
        }
        add_data(selected_path, new_data)

    # Ambil data dari Firebase
    data = get_data(selected_path)

    # Periksa kembali apakah data kosong setelah menambahkan
    if not data:
        st.write("Data tidak ditemukan.")
        return

    # Form untuk mengubah data yang ada
    st.title("Update Existing Data")
    selected_judul_aktivitas = st.selectbox(
        "Select judul aktivitas to update:",
        [value["judul_aktivitas"] for value in data.values()],
    )

    # Temukan data yang sesuai dengan judul_aktivitas yang dipilih
    selected_data = None
    for key, value in data.items():
        if value["judul_aktivitas"] == selected_judul_aktivitas:
            selected_data = value
            break

    if selected_data:
        updated_body_aktivitas = st.text_input(
            "Updated Body Aktivitas",
            selected_data["body_aktivitas"],
            help="Misalnya: Senin",
        )
        updated_category = st.text_input("Updated Category", selected_data["category"])
        updated_deskripsi_aktivitas = st.text_input(
            "Updated Deskripsi Aktivitas",
            selected_data["deskripsi_aktivitas"],
            help="Misalnya: Kegiatan kumpul-kumpul bersama partner bisnis",
        )
        updated_gambar_aktivitas = st.text_input(
            "Updated Gambar Aktivitas", selected_data["gambar_aktivitas"]
        )
        updated_hari_aktivitas = st.text_input(
            "Updated Hari Aktivitas",
            selected_data["hari_aktivitas"],
            help="Misalnya: 21 April 2024",
        )
        updated_judul_aktivitas = st.text_input(
            "Updated Judul Aktivitas",
            selected_data["judul_aktivitas"],
            help="Misalnya: True Workshop",
        )

        if st.button("Update"):
            updated_data = {
                "body_aktivitas": updated_body_aktivitas,
                "category": updated_category,
                "deskripsi_aktivitas": updated_deskripsi_aktivitas,
                "gambar_aktivitas": updated_gambar_aktivitas,
                "hari_aktivitas": updated_hari_aktivitas,
                "judul_aktivitas": updated_judul_aktivitas,
            }
            update_data(selected_path, selected_judul_aktivitas, updated_data)
    else:
        st.write("Judul aktivitas tidak ditemukan dalam data.")

    st.title("Hapus Data")
    data_to_delete = st.selectbox(
        "Pilih judul aktivitas untuk dihapus:",
        [value["judul_aktivitas"] for value in data.values()],
    )

    if st.button("Hapus"):
        key_to_delete = None
        for key, value in data.items():
            if value["judul_aktivitas"] == data_to_delete:
                key_to_delete = key
                break
        if key_to_delete:
            delete_data(selected_path, key_to_delete)
        else:
            st.error("Judul aktivitas tidak ditemukan.")

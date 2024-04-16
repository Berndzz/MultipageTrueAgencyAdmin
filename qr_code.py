import streamlit as st
import qrcode
import json
from PIL import Image
import io


def app():
    def create_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((250, 250))
        return img

    st.title("QR Code Generator for Events TRUE AGENCY SM7")

    programs = [
        "Training SM7",
        "Training PRU SALES ACADEMY",
        "Training Product & Knowledge",
        "Personal Excellent Mentallity & Attitude",
        "Sales Skill",
    ]

    events = [
        "True Talk",
        "True Story",
        "True Gathering",
        "True Skill",
        "True WorkShop",
        "Pengenalan Sejarah Asuransi (Syariah), Tokoh dan Istilah didalam Asuransi Jiwa",
        "Peta Produk As. Tradisional & Kegunaan di Masyarakat",
        "Pru Cinta & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "Pru Anugerah & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PCB 88 & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PKKS & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "PSS Plus Pro & Role Play Presentasi & Membuat + Menerangkan ilustrasi",
        "Perbandingan antar Produk Asuransi, Kapan Menjual itu semua >> Role Play",
        "Mengisi SPAJ, CEKATAN & Pru PayLink >> Role Play",
        "Mengoperasikan Pru Force (Lisensi, Training, Income, %, Lapse) + PULSE",
        "Peraturan - peraturan KLAIM, Kode Etik (TTD, KTP, Edit Document, PEC)",
        "Hukum Dasar Penjualan As., Pola Ring 123, & Tehnik Canvassing",
        "Dream Book, Janji Temu, Daily Activity",
        "Membangun Hubungan, Perkenalan",
        "Fact Finding (Market Survey) & Tehnik Up Selling",
        "Tehnik Bertanya & Memberikan Solusi + Ide (Identifikasi Need)",
        "Presentasi Keranjang Batu (+ Role Play)",
        "Presentasi 28000 (+ Role Play)",
        "Presentasi Pak Hikmad (+ Role Play)",
        "Urutan Acara Prospek Lengkap (+ Role Play)",
        "Membaca Kebutuhan, Kemampuan & Kemauan Beli & Solusi",
        "Tehnik Handling Objection & Role Play",
        "SALES CLINIC & Perlengkapan Perang & Sales Tools",
        "Presentasi Bisnis (NBO), HO NBO, Hitung Komisi - OR",
        "Mentalitas Sales Asuransi Jiwa (Misi & Visi Asuransi, Aktifitas Rutin)",
        "Kemampuan Inisiasi (Menggerakkan Agen & Team)",
        "Pemantauan Target Mingguan - Tahunan, Pemantauan Aktifitas, Strategy",
        "Penampilan (Grooming), Buah Tangan / Hadiah, Pru Flyer (Referensi)",
        "Mengantar Polis, Etika dalam mengurus KLAIM, Servicing Klien Lama (Hadiah ultah, HWA)",
        "Kedisplinan, Komitmen, Mindset, Etika, Attitude",
        "Management Keuangan Agen & Leader, Investasi Seminar / Skill Upgrade dll",
        "3 Misi Mulia, 7 Penghambat, Visi dan Misi Agen Asuransi, 7 Pilar Kepercayaan",
    ]

    tab_items = [
        "Q1",
        "Q2",
        "Q3",
        "Mentality & Attitude",
        "PRU Sales Academy",
        "Product & Knowledge Academy",
        "Sales Skill",
    ]

    with st.form("event_form", clear_on_submit=True):
        selected_event = st.selectbox("Pilih Acara", events)
        selected_program = st.selectbox("Pilih Program", programs)
        selected_tab_item = st.selectbox("Pilih Tab Item", tab_items)
        tanggal_acara = st.date_input("Tanggal Acara")
        jam_mulai = st.time_input("Jam Mulai")
        jam_selesai = st.time_input("Jam Selesai")
        lokasi = st.text_input("Lokasi")
        submit_button = st.form_submit_button("Generate QR Code")

    if submit_button:
        event_data = {
            "namaAcara": selected_event,
            "program": selected_program,
            "tabName": selected_tab_item,
            "tanggalAcara": str(tanggal_acara),
            "jamMulai": str(jam_mulai),
            "jamSelesai": str(jam_selesai),
            "lokasi": lokasi,
            "kehadiran": "",
        }
        json_data = json.dumps(event_data)
        qr_code_img = create_qr_code(json_data)

        # Konversi PIL Image ke BytesIO
        buf = io.BytesIO()
        qr_code_img.save(buf, format="PNG")
        buf.seek(0)

        # Menampilkan QR code di UI
        st.image(buf, caption="QR Code for Event", use_column_width=True)

        # Opsi untuk mengunduh QR code sebagai gambar
        buf.seek(0)  # Reset buffer position
        st.download_button(
            label="Download QR Code",
            data=buf,
            file_name="event_qr_code.png",
            mime="image/png",
        )

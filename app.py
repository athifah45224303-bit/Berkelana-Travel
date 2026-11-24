"""Aplikasi utama Sistem Administrasi Travel Berkelana.

Jalankan dari folder proyek:
    streamlit run app.py
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

LOGO_FAVICON = Path(__file__).resolve().parent / "assets" / "favicon.png"

st.set_page_config(
    page_title="Berkelana Travel — Sistem Administrasi",
    page_icon=str(LOGO_FAVICON),
    layout="wide",
    initial_sidebar_state="expanded",
)

import auth
import components as ui
import database as db
from tampilan import (
    dashboard,
    kreator,
    kursi,
    log,
    login,
    pelanggan,
    pemesanan,
    pengguna,
    riwayat,
    rute,
)
from utils import rupiah, tanggal_indo


@st.cache_resource(show_spinner="Menyiapkan database Berkelana Travel...")
def _siapkan_aplikasi() -> bool:
    db.init_db()
    return True


_siapkan_aplikasi()

ui.terapkan_css()

HALAMAN = {
    "Dashboard": dashboard.render,
    "Pelanggan": pelanggan.render,
    "Rute & Tarif": rute.render,
    "Data Kursi": kursi.render,
    "Pemesanan Tiket": pemesanan.render,
    "Riwayat Pemesanan": riwayat.render,
    "Log Aktivitas": log.render,
    "Kelola Pengguna": pengguna.render,
    "Kreator": kreator.render,
}

with st.sidebar:
    ui.sidebar_brand()

if not auth.sudah_login():
    login.render()
    st.stop()

with st.sidebar:
    halaman = st.radio(
        "Navigasi",
        options=list(HALAMAN),
        label_visibility="collapsed",
        key="navigasi_utama",
    )

    try:
        ringkas = db.ringkasan_dashboard()
        ringkasan_sidebar = (
            f"<b>{ringkas['total_pemesanan']} pemesanan aktif</b><br>"
            f"{ringkas['total_tiket']} tiket · {ringkas['rute_aktif']} rute aktif<br>"
            f"Pendapatan {rupiah(ringkas['total_pendapatan'])}"
        )
    except Exception:
        ringkasan_sidebar = "Database sedang disiapkan."

    st.divider()
    ui.sidebar_note(
        f"<b>{tanggal_indo(date.today())}</b><br><br>{ringkasan_sidebar}"
    )
    st.caption("Database lokal: berkelana.db")
    st.caption(f"Masuk sebagai **{auth.pengguna_sekarang()}**")
    if st.button("Keluar", width="stretch", key="tombol_keluar"):
        db.catat_logout_pengguna(int(st.session_state[auth.KUNCI_ID]))
        auth.logout()
        st.rerun()

ui.tampilkan_flash()
HALAMAN[halaman]()

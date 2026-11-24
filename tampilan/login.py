"""Halaman gerbang login.

Dua tab: Masuk (sign in) untuk akun yang sudah terdaftar dan Daftar (sign up)
untuk membuat akun baru. Saat tabel pengguna masih kosong, tab Daftar
dibuka lebih dulu karena belum ada akun yang bisa masuk.
"""

from __future__ import annotations

import streamlit as st

import auth
import components as ui
import database as db

FITUR = (
    ("Kelola pelanggan, rute, tarif, dan kursi", "data master perjalanan"),
    ("Pemesanan tiket dengan denah kursi real-time", "tanpa kursi bentrok"),
    ("Nota, riwayat transaksi, dan log aktivitas", "jejak audit otomatis"),
)


def _panel_brand() -> None:
    logo = ui.logo_data_uri()
    gambar = (
        f'<img src="{logo}" alt="Logo Berkelana Travel">'
        if logo
        else '<div class="bk-auth-monogram">BT</div>'
    )
    butir = "".join(
        f'<li><span class="tick"></span><span><b>{judul}</b> — {ketika}</span></li>'
        for judul, ketika in FITUR
    )
    st.markdown(
        f"""
        <div class="bk-auth-brand">
            {gambar}
            <div class="name">Berkelana Travel</div>
            <div class="tag">Sistem Administrasi Perjalanan</div>
            <ul class="list">{butir}</ul>
            <div class="foot">Python · Streamlit · SQLite — data tersimpan lokal</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _kartu_daftar() -> None:
    st.markdown(
        '<h3 class="bk-auth-title">Daftar akun baru</h3>'
        '<p class="bk-auth-sub">Buat akun petugas, hanya butuh satu menit.</p>',
        unsafe_allow_html=True,
    )
    with st.form("form_daftar", clear_on_submit=True):
        username = st.text_input(
            "Username",
            placeholder="Contoh: athifah",
            key="daftar_username",
            help="3-30 karakter: huruf, angka, titik, garis bawah, atau tanda hubung.",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimal 8 karakter",
            key="daftar_password",
        )
        konfirmasi = st.text_input(
            "Ulangi password",
            type="password",
            key="daftar_konfirmasi",
        )
        daftar = st.form_submit_button("Daftar sekarang", type="primary", width="stretch")

    if not daftar:
        return

    if password != konfirmasi:
        st.error("Konfirmasi password tidak sama dengan password.")
        return
    try:
        pengguna = auth.buat_akun(username, password)
    except db.KesalahanBisnis as exc:
        st.error(str(exc))
        return
    except auth.KesalahanAutentikasi as exc:
        st.error(str(exc))
        return

    auth.buka_sesi(pengguna)
    ui.set_flash("success", f"Akun {pengguna['username']} berhasil dibuat. Selamat datang!")
    st.rerun()


def _kartu_masuk() -> None:
    st.markdown(
        '<h3 class="bk-auth-title">Masuk</h3>'
        '<p class="bk-auth-sub">Gunakan akun yang sudah terdaftar.</p>',
        unsafe_allow_html=True,
    )
    with st.form("form_login"):
        username = st.text_input(
            "Username",
            placeholder="Masukkan username",
            key="login_username",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Masukkan password",
            key="login_password",
        )
        masuk = st.form_submit_button("Masuk", type="primary", width="stretch")

    if not masuk:
        return

    try:
        pengguna = auth.login(username, password)
    except auth.KesalahanAutentikasi as exc:
        st.error(str(exc))
        return

    ui.set_flash("success", f"Login berhasil. Halo, {pengguna['username']}!")
    st.rerun()


def render() -> None:
    st.markdown('<div style="height:.6rem"></div>', unsafe_allow_html=True)
    with st.container(key="bk_auth_card"):
        brand, formulir = st.columns([1.02, 1], gap="small")
        with brand:
            _panel_brand()
        with formulir:
            belum_ada_akun = not db.daftar_pengguna()
            if belum_ada_akun:
                st.markdown(
                    '<div class="bk-auth-hint">'
                    '<span class="bk-auth-hint-icon">i</span>'
                    "<span><b>Belum ada akun.</b> Daftarkan akun petugas pertama "
                    "untuk mulai memakai sistem.</span></div>",
                    unsafe_allow_html=True,
                )
                tab_daftar, tab_masuk = st.tabs(["Daftar", "Masuk"])
                with tab_daftar:
                    _kartu_daftar()
                with tab_masuk:
                    _kartu_masuk()
            else:
                tab_masuk, tab_daftar = st.tabs(["Masuk", "Daftar"])
                with tab_masuk:
                    _kartu_masuk()
                with tab_daftar:
                    _kartu_daftar()
            st.markdown(
                '<div class="bk-auth-foot">'
                "Password disimpan sebagai hash bcrypt, tidak pernah dalam bentuk teks biasa."
                "</div>",
                unsafe_allow_html=True,
            )

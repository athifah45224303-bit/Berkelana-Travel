"""Halaman pengelolaan akun pengguna (kelola user)."""

from __future__ import annotations

import pandas as pd
import streamlit as st

import auth
import components as ui
import database as db
from utils import waktu_lengkap


def _tabel_pengguna(data: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(data)
    return pd.DataFrame(
        {
            "Username": df["username"],
            "Status": df["aktif"].map(lambda x: "Aktif" if x else "Nonaktif"),
            "Dibuat": df["dibuat_pada"].map(lambda x: waktu_lengkap(x)),
            "Login terakhir": df["login_terakhir"].map(
                lambda x: waktu_lengkap(x) if pd.notna(x) and x else "Belum pernah"
            ),
        }
    )


def _form_tambah() -> None:
    with st.form("form_tambah_pengguna", clear_on_submit=True):
        username = st.text_input(
            "Username *",
            placeholder="Contoh: diza",
            help="3-30 karakter: huruf, angka, titik, garis bawah, atau tanda hubung.",
        )
        password = st.text_input(
            "Password *",
            type="password",
            placeholder="Minimal 8 karakter",
        )
        konfirmasi = st.text_input("Ulangi password *", type="password")
        st.caption("* Wajib diisi. Password di-hash dengan bcrypt (cost factor 12).")
        disimpan = st.form_submit_button("Tambah pengguna", type="primary")

    if not disimpan:
        return
    if password != konfirmasi:
        st.error("Konfirmasi password tidak sama dengan password.")
        return
    try:
        baru = auth.buat_akun(username, password)
    except db.KesalahanBisnis as exc:
        st.error(str(exc))
        return
    except auth.KesalahanAutentikasi as exc:
        st.error(str(exc))
        return
    ui.set_flash("success", f"Pengguna {baru['username']} berhasil ditambahkan.")
    st.rerun()


def _form_ganti_password(pengguna: dict) -> None:
    with st.form(f"form_ganti_password_{pengguna['id_user']}"):
        lama = st.text_input("Password lama *", type="password")
        baru = st.text_input("Password baru *", type="password")
        konfirmasi = st.text_input("Ulangi password baru *", type="password")
        simpan = st.form_submit_button("Simpan password baru", type="primary")

    if not simpan:
        return
    if baru != konfirmasi:
        st.error("Konfirmasi password baru tidak sama.")
        return
    try:
        auth.ganti_password(pengguna["id_user"], lama, baru)
    except auth.KesalahanAutentikasi as exc:
        st.error(str(exc))
        return
    ui.set_flash("success", f"Password {pengguna['username']} berhasil diganti.")
    st.rerun()


def render() -> None:
    ui.page_header(
        "Kelola Pengguna",
        "Tambah akun petugas, nonaktifkan akses, dan ganti password.",
    )

    semua = db.daftar_pengguna()
    aktif = sum(1 for p in semua if p["aktif"])

    kolom = st.columns(4)
    with kolom[0]:
        ui.metrik("Total pengguna", f"{len(semua)}", "Seluruh akun terdaftar")
    with kolom[1]:
        ui.metrik("Aktif", f"{aktif}", "Akun yang bisa login")
    with kolom[2]:
        ui.metrik("Nonaktif", f"{len(semua) - aktif}", "Akun dinonaktifkan")
    with kolom[3]:
        ui.metrik("Sedang login", auth.pengguna_sekarang(), "Akun sesi ini")

    tab_daftar, tab_tambah = st.tabs(["Daftar Pengguna", "Tambah Pengguna"])

    with tab_tambah:
        st.markdown(
            """
            <div class="bk-note">
                <b>Keamanan akun:</b> password tidak pernah disimpan sebagai teks biasa.
                Setiap password di-hash dengan bcrypt cost factor 12 dan salt acak,
                sehingga password asli tidak bisa dibaca kembali dari database.
            </div>
            """,
            unsafe_allow_html=True,
        )
        _form_tambah()

    with tab_daftar:
        if not semua:
            ui.empty_state(
                "Belum ada pengguna",
                "Tambahkan akun pertama untuk dapat masuk ke sistem.",
            )
            return

        st.dataframe(
            _tabel_pengguna(semua),
            hide_index=True,
            width="stretch",
            height=min(360, 42 + len(semua) * 35),
        )

        pilihan = st.selectbox(
            "Pilih pengguna",
            options=[p["id_user"] for p in semua],
            format_func=lambda pid: next(
                f"{p['username']} · {'Aktif' if p['aktif'] else 'Nonaktif'}"
                for p in semua
                if p["id_user"] == pid
            ),
            key="pilih_pengguna",
        )
        pilih = next(p for p in semua if p["id_user"] == pilihan)
        adalah_saya = pilih["id_user"] == st.session_state.get(auth.KUNCI_ID)

        kiri, kanan = st.columns([1, 1.05])
        with kiri:
            inisial = (pilih["username"][:1] or "?").upper()
            st.markdown(
                f'<div class="bk-user-cell"><div class="bk-avatar">{ui.esc(inisial)}</div>'
                f"<div><b>{ui.esc(pilih['username'])}</b><br>"
                f"<span>Dibuat {ui.esc(waktu_lengkap(pilih['dibuat_pada']))}</span></div></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div style='margin-top:.6rem'>"
                f"{ui.badge_status_aktif(pilih['aktif'])}</div>",
                unsafe_allow_html=True,
            )
            st.caption(
                "Login terakhir: "
                + (
                    waktu_lengkap(pilih["login_terakhir"])
                    if pilih["login_terakhir"]
                    else "belum pernah login"
                )
            )

            with st.expander("Hapus pengguna"):
                if len(semua) <= 1:
                    st.info("Akun pengguna terakhir tidak dapat dihapus.")
                elif adalah_saya:
                    st.info("Akun yang sedang digunakan tidak dapat dihapus.")
                else:
                    st.warning("Penghapusan bersifat permanen.")
                    yakin = st.checkbox(
                        f"Saya yakin menghapus {pilih['username']}",
                        key=f"yakin_hapus_pengguna_{pilih['id_user']}",
                    )
                    if st.button(
                        "Hapus pengguna",
                        disabled=not yakin,
                        key=f"hapus_pengguna_{pilih['id_user']}",
                    ):
                        try:
                            db.hapus_pengguna(pilih["id_user"])
                        except db.KesalahanBisnis as exc:
                            st.error(str(exc))
                        else:
                            ui.set_flash(
                                "success",
                                f"Pengguna {pilih['username']} berhasil dihapus.",
                            )
                            st.rerun()

        with kanan:
            st.markdown("##### Ganti password")
            _form_ganti_password(pilih)

            st.markdown("##### Status akun")
            if adalah_saya:
                st.info("Akun ini sedang digunakan, statusnya tidak dapat diubah.")
            else:
                aktifkan = not pilih["aktif"]
                label = "Aktifkan akun" if aktifkan else "Nonaktifkan akun"
                if st.button(label, key=f"status_pengguna_{pilih['id_user']}"):
                    try:
                        db.atur_status_pengguna(pilih["id_user"], aktifkan)
                    except db.KesalahanBisnis as exc:
                        st.error(str(exc))
                    else:
                        ui.set_flash(
                            "success",
                            f"Akun {pilih['username']} berhasil {'diaktifkan' if aktifkan else 'dinonaktifkan'}.",
                        )
                        st.rerun()

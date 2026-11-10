"""Halaman identitas tim kreator aplikasi."""

from __future__ import annotations

import streamlit as st

import components as ui
from utils import esc

ANGGOTA = (
    ("Athifah Luthfia Hikmah", "4.52.24.3.03"),
    ("Diaz Purnama Shifa", "4.52.24.3.07"),
    ("Hana Noor Istiqomah", "4.52.24.3.12"),
    ("Shintya Bela Yuliyanti", "4.52.24.3.26"),
)

WARNA = (
    ("#1e68af", "#5c9fd6"),
    ("#b45309", "#f59e0b"),
    ("#1d4ed8", "#38bdf8"),
    ("#be185d", "#f472b6"),
)

MATA_KULIAH = "Pemrograman Bisnis & Perancangan Sistem Administrasi"
DOSEN = "Dwi Budi Santoso, S.Kom., M.Kom."

CSS_KREATOR = """
<style>
.bk-campus {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 1.9rem 2rem 1.7rem;
    color: #eaf2fb;
    background:
        radial-gradient(circle at 92% -20%, rgba(92, 159, 214, 0.40), transparent 26rem),
        radial-gradient(circle at -6% 110%, rgba(30, 104, 175, 0.45), transparent 24rem),
        linear-gradient(135deg, #052747 0%, #07366c 48%, #1e68af 100%);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 18px 44px rgba(7, 54, 108, 0.28);
}
.bk-campus::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
    background-size: 34px 34px;
    mask-image: radial-gradient(circle at 80% 0%, #000 0%, transparent 62%);
    pointer-events: none;
}
.bk-campus-eyebrow {
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #a8cbe8;
}
.bk-campus h2 {
    margin: 0.5rem 0 0.25rem;
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
}
.bk-campus p {
    margin: 0;
    color: #dceafa;
    font-size: 1rem;
}
.bk-campus-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 1.1rem;
}
.bk-campus-chips span {
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 999px;
    padding: 0.34rem 0.85rem;
    font-size: 0.8rem;
    font-weight: 700;
    color: #f0f7ff;
    backdrop-filter: blur(4px);
}
.bk-creator-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 0.25rem;
}
.bk-creator-card {
    background: linear-gradient(160deg, #ffffff 0%, #f3f8fd 100%);
    border: 1px solid var(--bk-line);
    border-radius: 18px;
    padding: 1.2rem 1.25rem 1.1rem;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
    transition: transform 150ms ease, box-shadow 150ms ease, border-color 150ms ease;
}
.bk-creator-card:hover {
    transform: translateY(-3px);
    border-color: var(--c1);
    box-shadow: 0 16px 34px rgba(15, 23, 42, 0.10);
}
.bk-creator-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.bk-creator-avatar {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 800;
    font-size: 1.02rem;
    letter-spacing: 0.02em;
    color: #ffffff;
    background: linear-gradient(140deg, var(--c1), var(--c2));
    box-shadow: 0 8px 18px color-mix(in srgb, var(--c1) 35%, transparent);
}
.bk-creator-no {
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    color: var(--bk-muted);
    background: rgba(30, 104, 175, 0.07);
    border: 1px solid var(--bk-line);
    border-radius: 999px;
    padding: 0.22rem 0.6rem;
}
.bk-creator-name {
    margin-top: 0.85rem;
    font-size: 1.12rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--bk-ink);
}
.bk-creator-nim {
    margin-top: 0.3rem;
    display: inline-block;
    font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--c1);
    background: color-mix(in srgb, var(--c1) 9%, #ffffff);
    border: 1px solid color-mix(in srgb, var(--c1) 26%, #ffffff);
    border-radius: 9px;
    padding: 0.24rem 0.55rem;
}
.bk-creator-tag {
    margin-top: 0.7rem;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--bk-muted);
}
@media (max-width: 720px) {
    .bk-campus { padding: 1.4rem 1.3rem; }
    .bk-campus h2 { font-size: 1.35rem; }
    .bk-creator-grid { grid-template-columns: 1fr; }
}
</style>
"""


def _inisial(nama: str) -> str:
    return "".join(bagian[0] for bagian in nama.split())[:3].upper()


def _teks_identitas() -> str:
    baris = [
        "IDENTITAS TIM KREATOR",
        "Sistem Administrasi Travel Berkelana",
        "",
        "Mahasiswa Politeknik Negeri Semarang",
        "Jurusan Administrasi Bisnis",
        "Program Studi Administrasi Bisnis Terapan",
        "Kelas BT-3D - Kelompok 2",
        "",
    ]
    baris += [f"{i}. {nama} ({nim})" for i, (nama, nim) in enumerate(ANGGOTA, start=1)]
    baris += ["", f"Mata Kuliah: {MATA_KULIAH}", f"Dosen Pengampu: {DOSEN}"]
    return "\n".join(baris) + "\n"


def render() -> None:
    st.markdown(CSS_KREATOR, unsafe_allow_html=True)
    ui.page_header(
        "🎓",
        "Kreator",
        "Tim penyusun Sistem Administrasi Travel Berkelana — Kelompok 2.",
    )

    st.markdown(
        """
        <div class="bk-campus">
            <div class="bk-campus-eyebrow">Mahasiswa Politeknik Negeri Semarang</div>
            <h2>Jurusan Administrasi Bisnis</h2>
            <p>Program Studi Administrasi Bisnis Terapan</p>
            <div class="bk-campus-chips">
                <span>Kelas BT-3D</span>
                <span>Kelompok 2</span>
                <span>4 Anggota</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ui.judul_bagian("Tim Kreator", "Empat anggota kelompok penyusun sistem")

    kartu = []
    for idx, (nama, nim) in enumerate(ANGGOTA):
        warna = WARNA[idx]
        kartu.append(
            f"""
            <div class="bk-creator-card" style="--c1:{warna[0]};--c2:{warna[1]};">
                <div class="bk-creator-top">
                    <div class="bk-creator-avatar">{esc(_inisial(nama))}</div>
                    <span class="bk-creator-no">{idx + 1:02d}</span>
                </div>
                <div class="bk-creator-name">{esc(nama)}</div>
                <div class="bk-creator-nim">{esc(nim)}</div>
                <div class="bk-creator-tag">Anggota Kelompok 2</div>
            </div>
            """
        )
    grid_html = '<div class="bk-creator-grid">' + "".join(kartu) + "</div>"
    grid_html = "\n".join(
        baris.strip() for baris in grid_html.splitlines() if baris.strip()
    )
    st.markdown(grid_html, unsafe_allow_html=True)

    st.download_button(
        "⬇️ Unduh identitas tim (.txt)",
        data=_teks_identitas().encode("utf-8-sig"),
        file_name="identitas-kreator-berkelana.txt",
        mime="text/plain",
        key="unduh_identitas_kreator",
    )
    st.caption(f"Mata kuliah: {MATA_KULIAH} · Dosen pengampu: {DOSEN}")
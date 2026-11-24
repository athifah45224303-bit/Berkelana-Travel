"""Komponen visual bersama untuk aplikasi Streamlit Berkelana Travel."""

from __future__ import annotations

import base64
import html
from datetime import date, time
from pathlib import Path
from typing import Any, Iterable, Mapping

import streamlit as st

from utils import (
    buat_teks_nota,
    esc,
    jam_indo,
    nama_file_nota,
    rupiah,
    tanggal_indo,
    tanggal_singkat,
    waktu_lengkap,
)


CSS = """
<style>
:root {
    --bk-brand: #1e68af;
    --bk-brand-dark: #07366c;
    --bk-brand-soft: #dceafa;
    --bk-accent: #5c9fd6;
    --bk-ink: #0f172a;
    --bk-muted: #64748b;
    --bk-line: #d7e3f0;
    --bk-surface: #ffffff;
}
.stApp {
    background:
        radial-gradient(circle at 88% -8%, rgba(30, 104, 175, 0.10), transparent 32rem),
        linear-gradient(180deg, #f7fafc 0%, #f1f5f9 100%);
}
.block-container {
    padding-top: 2.1rem;
    padding-bottom: 3rem;
    max-width: 1220px;
}
h1, h2, h3, h4 {
    color: var(--bk-ink);
    letter-spacing: -0.02em;
}
p, label, .stMarkdown {
    color: #334155;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #052747 0%, #07366c 52%, #0a4a8f 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.1rem;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] {
    color: #eaf2fb !important;
}
[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 0.18rem;
}
[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: 11px;
    padding: 0.58rem 0.7rem;
    transition: background 120ms ease, transform 120ms ease;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255, 255, 255, 0.09);
}
[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: rgba(255, 255, 255, 0.16);
    border-color: rgba(255, 255, 255, 0.18);
}
[data-testid="stSidebar"] div[role="radiogroup"] label p {
    font-size: 0.94rem;
    font-weight: 600;
}
[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    display: none;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15);
}
.bk-brand {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 0.55rem;
    margin: 0 0 1.1rem 0;
    padding: 0.35rem 0.25rem 0.95rem 0.25rem;
    border-bottom: 1px solid rgba(255,255,255,0.16);
}
.bk-brand-logo-wrap {
    background: #ffffff;
    border-radius: 14px;
    padding: 0.5rem 0.6rem;
    box-shadow: 0 10px 22px rgba(0,0,0,0.18);
}
.bk-brand-logo {
    display: block;
    width: 100%;
    height: auto;
}
.bk-brand-icon {
    width: 46px;
    height: 46px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: linear-gradient(145deg, #5c9fd6, #1e68af);
    color: #ffffff;
    font-size: 1.45rem;
    box-shadow: 0 10px 22px rgba(0,0,0,0.18);
    flex: 0 0 auto;
}
.bk-brand-name {
    font-size: 1.15rem;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -0.02em;
}
.bk-brand-sub {
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    opacity: 0.76;
    margin-top: 0.18rem;
}
.bk-sidebar-note {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 13px;
    padding: 0.8rem 0.85rem;
    margin-top: 0.7rem;
    font-size: 0.76rem;
    line-height: 1.55;
}
.bk-sidebar-note b { color: #cfe3f7; }
/* Tombol Keluar: warna cerah agar mudah ditemukan di sidebar */
.st-key-tombol_keluar button {
    background-image: linear-gradient(135deg, #ff8659 0%, #ef2f56 100%) !important;
    background-color: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.30) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 11px !important;
    box-shadow: 0 8px 20px rgba(239, 47, 86, 0.40) !important;
    transition: transform 0.14s ease, box-shadow 0.14s ease;
}
.st-key-tombol_keluar button:hover {
    background-image: linear-gradient(135deg, #ff9a70 0%, #ff3f68 100%) !important;
    box-shadow: 0 11px 26px rgba(239, 47, 86, 0.52) !important;
    transform: translateY(-1px);
}
.st-key-tombol_keluar button:active {
    transform: translateY(0);
    box-shadow: 0 5px 12px rgba(239, 47, 86, 0.34) !important;
}
.st-key-tombol_keluar button:focus-visible {
    outline: 2px solid #ffd9de !important;
    outline-offset: 2px;
}
/* Navigasi sidebar: daftar teks polos dengan penanda aktif */
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child {
    display: none !important;
}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] {
    padding: 0.34rem 0.55rem !important;
    border-radius: 9px !important;
    background: transparent !important;
    transition: background 0.15s ease;
}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:hover {
    background: rgba(255, 255, 255, 0.07) !important;
}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"]:has(input:checked) {
    background: rgba(255, 255, 255, 0.13) !important;
    box-shadow: inset 3px 0 0 #8fc1ec !important;
}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] p {
    font-weight: 600 !important;
}
.bk-page-head {
    border-left: 4px solid var(--bk-brand);
    padding-left: 1.05rem;
    margin: 0 0 1.15rem 0;
}
.bk-page-head h1 {
    font-size: 1.85rem;
    line-height: 1.14;
    margin: 0;
    padding: 0;
}
.bk-page-head p {
    margin: 0.28rem 0 0 0;
    color: var(--bk-muted);
    font-size: 0.92rem;
}
.bk-hero {
    position: relative;
    overflow: hidden;
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    background:
        radial-gradient(circle at 92% 20%, rgba(92, 159, 214, 0.35), transparent 14rem),
        linear-gradient(120deg, #07366c 0%, #1e68af 58%, #3d84c6 100%);
    border-radius: 20px;
    padding: 1.6rem 1.8rem;
    color: #f0f7ff;
    margin-bottom: 1.25rem;
    box-shadow: 0 18px 44px rgba(7, 54, 108, 0.20);
}
.bk-hero .bk-eyebrow {
    display: inline-block;
    font-size: 0.68rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #bcd7f0;
    font-weight: 800;
    margin-bottom: 0.45rem;
}
.bk-hero h1 {
    color: #ffffff;
    font-size: 2.05rem;
    margin: 0 0 0.4rem 0;
    line-height: 1.13;
}
.bk-hero p {
    color: #dceafa;
    margin: 0;
    max-width: 640px;
    font-size: 0.94rem;
    line-height: 1.6;
}
.bk-hero-date {
    align-self: flex-start;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 999px;
    padding: 0.45rem 0.85rem;
    font-size: 0.76rem;
    font-weight: 700;
    color: #eaf2fb;
    white-space: nowrap;
}
.bk-metric {
    background: #ffffff;
    border: 1px solid var(--bk-line);
    border-radius: 16px;
    padding: 1rem 1.05rem 0.95rem 1.05rem;
    min-height: 118px;
    box-shadow: 0 7px 22px rgba(15, 23, 42, 0.045);
    position: relative;
    overflow: hidden;
    container-type: inline-size;
}
.bk-metric::after {
    content: "";
    position: absolute;
    right: -26px;
    bottom: -38px;
    width: 92px;
    height: 92px;
    border-radius: 50%;
    background: rgba(30, 104, 175, 0.055);
}
.bk-metric-top {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    margin-bottom: 0.55rem;
}
.bk-metric-label {
    font-size: 0.71rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--bk-muted);
}
.bk-metric-label::before {
    content: "";
    display: inline-block;
    width: 15px;
    height: 3px;
    border-radius: 2px;
    background: var(--bk-accent);
    margin-right: 0.5rem;
    vertical-align: 0.22em;
}
.bk-metric-value {
    line-height: 1.1;
    font-weight: 800;
    color: var(--bk-ink);
    letter-spacing: -0.035em;
    font-size: clamp(0.85rem, 9cqw, 1.55rem);
}
.bk-metric-sub {
    margin-top: 0.42rem;
    font-size: 0.75rem;
    color: var(--bk-muted);
    line-height: 1.35;
}
@container (max-width: 145px) {
    .bk-metric {
        padding: 0.8rem 0.8rem 0.75rem 0.8rem;
        min-height: 108px;
    }
    .bk-metric-label {
        font-size: 0.61rem;
        letter-spacing: 0.04em;
    }
    .bk-metric-sub {
        font-size: 0.66rem;
    }
}
.bk-metric.accent {
    background: linear-gradient(145deg, #1e68af, #3d84c6);
    border-color: transparent;
}
.bk-metric.accent .bk-metric-label,
.bk-metric.accent .bk-metric-sub {
    color: #dceafa;
}
.bk-metric.accent .bk-metric-value { color: #ffffff; }
.bk-metric.accent .bk-metric-label::before { background: rgba(255, 255, 255, 0.82); }
.bk-metric.accent::after { background: rgba(255,255,255,0.09); }
.bk-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin: 1.35rem 0 0.7rem 0;
}
.bk-section-title h3 {
    margin: 0;
    font-size: 1.08rem;
    font-weight: 800;
}
.bk-section-title span {
    color: var(--bk-muted);
    font-size: 0.76rem;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 16px;
    border-color: var(--bk-line);
    background: rgba(255,255,255,0.78);
}
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--bk-line);
    border-radius: 16px;
    padding: 0.9rem 1rem;
    box-shadow: 0 7px 22px rgba(15, 23, 42, 0.04);
}
div[data-testid="stMetricValue"] {
    font-weight: 800;
    letter-spacing: -0.03em;
}
.stButton > button,
.stDownloadButton > button,
button[kind="secondary"],
button[kind="primary"] {
    border-radius: 10px;
    font-weight: 700;
    transition: transform 100ms ease, box-shadow 100ms ease;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 18px rgba(30, 104, 175, 0.14);
}
.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1e68af, #3d84c6);
    border-color: #1e68af;
}
.stButton > button:disabled {
    opacity: 0.55;
}
div[data-testid="stForm"] {
    background: rgba(255,255,255,0.64);
    border: 1px solid var(--bk-line);
    border-radius: 16px;
    padding: 1.05rem 1.05rem 0.35rem 1.05rem;
}
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-baseweb="textarea"] > div {
    border-radius: 9px;
}
button[data-baseweb="tab"] {
    font-weight: 700;
}
div[data-testid="stExpander"] details {
    border-radius: 13px;
    border-color: var(--bk-line);
    background: rgba(255,255,255,0.62);
}
.bk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.32rem;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 0.71rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    white-space: nowrap;
}
.bk-badge.green { background: #dcfce7; color: #166534; }
.bk-badge.grey { background: #e8edf1; color: #475569; }
.bk-badge.amber { background: #fef3c7; color: #92400e; }
.bk-badge.red { background: #fee2e2; color: #991b1b; }
.bk-badge.teal { background: #dceafa; color: #07366c; }
.bk-trip {
    background: #ffffff;
    border: 1px solid var(--bk-line);
    border-radius: 17px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
}
.bk-trip-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 0.55rem;
}
.bk-trip-code {
    font-weight: 800;
    letter-spacing: 0.02em;
    color: #1e68af;
    font-size: 0.82rem;
}
.bk-trip-route {
    font-size: 1.32rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    color: var(--bk-ink);
    margin: 0.18rem 0 0.5rem 0;
}
.bk-trip-route .arrow {
    color: var(--bk-accent);
    padding: 0 0.3rem;
}
.bk-trip-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem 1.1rem;
    color: var(--bk-muted);
    font-size: 0.82rem;
}
.bk-trip-meta b { color: #1e293b; }
.bk-trip-meta em {
    font-style: normal;
    font-weight: 700;
    color: var(--bk-muted);
    margin-right: 0.12rem;
}
.bk-seat-shell {
    background: linear-gradient(180deg, #ffffff, #f8fafc);
    border: 1px solid var(--bk-line);
    border-radius: 18px;
    padding: 1rem 1.1rem 1.15rem 1.1rem;
    margin: 0.2rem 0 0.85rem 0;
}
.bk-bus-front {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #94a3b8;
    border-bottom: 1px dashed #cbd5e1;
    padding-bottom: 0.6rem;
    margin-bottom: 0.75rem;
}
.bk-bus-mark {
    width: 34px;
    height: 9px;
    border-radius: 4px 4px 2px 2px;
    background: #cbd5e1;
    position: relative;
    flex: none;
}
.bk-bus-mark::after {
    content: "";
    position: absolute;
    left: 5px;
    right: 5px;
    top: 2px;
    height: 3px;
    border-radius: 2px;
    background: #e2e8f0;
}
.bk-seat-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(88px, 1fr));
    gap: 0.6rem 1rem;
    max-width: 250px;
    margin: 0 auto;
}
.bk-seat {
    border-radius: 11px;
    padding: 0.48rem 0.2rem 0.45rem 0.2rem;
    text-align: center;
    border: 1.5px solid #bbf7d0;
    background: #f0fdf4;
    color: #166534;
    min-height: 57px;
}
.bk-seat .num { font-weight: 800; font-size: 0.92rem; line-height: 1.1; }
.bk-seat .st { font-size: 0.56rem; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 0.18rem; opacity: 0.8; }
.bk-seat.booked {
    background: #e5e7eb;
    border-color: #cbd5e1;
    color: #6b7280;
}
.bk-seat.inactive {
    background: #f8fafc;
    border: 1.5px dashed #cbd5e1;
    color: #94a3b8;
}
.bk-seat.selected {
    background: #fef3c7;
    border-color: #f59e0b;
    color: #92400e;
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.14);
}
.bk-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem 1rem;
    font-size: 0.72rem;
    color: var(--bk-muted);
    margin-top: 0.7rem;
    justify-content: center;
}
.bk-legend i {
    display: inline-block;
    width: 11px;
    height: 11px;
    border-radius: 3px;
    margin-right: 0.28rem;
    vertical-align: -1px;
}
.bk-profile {
    background: linear-gradient(155deg, #ffffff 0%, #f3f8fd 100%);
    border: 1px solid var(--bk-line);
    border-radius: 18px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.045);
}
.bk-profile-name {
    font-size: 1.22rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0.15rem 0 0.2rem 0;
}
.bk-profile-sub { color: var(--bk-muted); font-size: 0.83rem; }
.bk-profile-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.55rem;
    margin-top: 0.9rem;
}
.bk-profile-stat {
    background: rgba(255,255,255,0.8);
    border: 1px solid var(--bk-line);
    border-radius: 11px;
    padding: 0.5rem 0.55rem;
}
.bk-profile-stat span {
    display: block;
    color: var(--bk-muted);
    font-size: 0.64rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.bk-profile-stat b {
    display: block;
    color: var(--bk-ink);
    font-size: 0.92rem;
    margin-top: 0.15rem;
}
.bk-price-box {
    background: linear-gradient(150deg, #f0f7ff, #eaf2fb);
    border: 1px solid #bcd7f0;
    border-radius: 16px;
    padding: 1rem 1.15rem;
}
.bk-price-box .row {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    font-size: 0.83rem;
    color: #475569;
    padding: 0.22rem 0;
}
.bk-price-box .row.total {
    border-top: 1px dashed #a8cbe8;
    margin-top: 0.45rem;
    padding-top: 0.6rem;
    color: #0f172a;
    font-weight: 800;
    font-size: 1rem;
}
.bk-price-box .row.total b { color: #1e68af; font-size: 1.25rem; }
.bk-empty {
    text-align: center;
    padding: 2.2rem 1rem;
    border: 1px dashed #cbd5e1;
    border-radius: 16px;
    background: rgba(255,255,255,0.55);
    color: var(--bk-muted);
}
.bk-empty .mark {
    width: 44px;
    height: 44px;
    margin: 0 auto 0.75rem auto;
    border-radius: 13px;
    border: 2px dashed #cbd5e1;
    background: rgba(248, 250, 252, 0.9);
}
.bk-seat-usage {
    display: inline-flex;
    gap: 0.22rem;
}
.bk-seat-usage i {
    width: 9px;
    height: 9px;
    border-radius: 2px;
    background: #e2e8f0;
    display: inline-block;
}
.bk-seat-usage i.on { background: #1e68af; }
.bk-note {
    border-left: 4px solid #f59e0b;
    background: #fffbeb;
    padding: 0.75rem 0.9rem;
    border-radius: 0 10px 10px 0;
    font-size: 0.82rem;
    color: #78350f;
    margin: 0.4rem 0 0.8rem 0;
}
.bk-receipt-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 800;
    color: #1e68af;
    margin-bottom: 0.4rem;
}
div[data-testid="stCode"] pre {
    background: #fbfdfd !important;
    border: 1px solid var(--bk-line) !important;
    border-radius: 12px !important;
}
/* Halaman masuk & daftar: kartu split brand + formulir */
.st-key-bk_auth_card {
    background: #ffffff;
    border: 1px solid var(--bk-line);
    border-radius: 22px;
    overflow: hidden;
    box-shadow: 0 26px 60px rgba(7, 54, 108, 0.16);
    max-width: 980px;
    width: 100%;
    margin: 0 auto;
}
.st-key-bk_auth_card [data-testid="stHorizontalBlock"] {
    gap: 0;
    align-items: stretch;
}
.st-key-bk_auth_card [data-testid="stColumn"] {
    padding: 2.1rem 1.75rem;
}
.st-key-bk_auth_card [data-testid="stColumn"]:first-child {
    background:
        radial-gradient(circle at 16% 10%, rgba(92, 159, 214, 0.42), transparent 11rem),
        linear-gradient(158deg, #052747 0%, #07366c 46%, #1e68af 100%);
}
.st-key-bk_auth_card [data-testid="stColumn"]:last-child {
    background: #ffffff;
}
.bk-auth-brand {
    color: #eaf2fb;
    display: flex;
    flex-direction: column;
    height: 100%;
}
.st-key-bk_auth_card [data-testid="stColumn"]:first-child [data-testid="stVerticalBlock"],
.st-key-bk_auth_card [data-testid="stColumn"]:first-child [data-testid="stElementContainer"],
.st-key-bk_auth_card [data-testid="stColumn"]:first-child [data-testid="stMarkdown"],
.st-key-bk_auth_card [data-testid="stColumn"]:first-child [data-testid="stMarkdown"] > div {
    height: 100%;
}
.bk-auth-brand img {
    width: 78px;
    height: auto;
    border-radius: 14px;
    background: #ffffff;
    padding: 0.35rem;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.24);
}
.bk-auth-monogram {
    width: 78px;
    height: 78px;
    border-radius: 16px;
    display: grid;
    place-items: center;
    background: #ffffff;
    color: var(--bk-brand-dark);
    font-weight: 800;
    font-size: 1.55rem;
    letter-spacing: 0.05em;
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.24);
}
.bk-auth-brand .name {
    font-size: 1.32rem;
    font-weight: 800;
    color: #ffffff;
    margin-top: 1rem;
    letter-spacing: -0.01em;
}
.bk-auth-brand .tag {
    font-size: 0.82rem;
    color: #a9c9e8;
    margin-top: 0.15rem;
}
.bk-auth-brand .list {
    list-style: none;
    padding: 0;
    margin: 1.35rem 0 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.7rem;
}
.bk-auth-brand .list li {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    font-size: 0.85rem;
    color: #d7e7f7;
    line-height: 1.45;
}
.bk-auth-brand .list b {
    color: #ffffff;
}
.bk-auth-brand .tick {
    flex: none;
    position: relative;
    width: 1.05rem;
    height: 1.05rem;
    margin-top: 0.12rem;
    border-radius: 50%;
    background: rgba(127, 212, 168, 0.18);
}
.bk-auth-brand .tick::after {
    content: "";
    position: absolute;
    left: 0.33rem;
    top: 0.19rem;
    width: 0.24rem;
    height: 0.48rem;
    border: solid #7fd4a8;
    border-width: 0 2px 2px 0;
    transform: rotate(43deg);
}
.bk-auth-brand .foot {
    margin-top: auto;
    padding-top: 1.4rem;
    font-size: 0.73rem;
    color: #9dbcdb;
}
.st-key-bk_auth_card h3.bk-auth-title {
    margin: 0 0 0.15rem 0;
    font-size: 1.28rem;
    color: var(--bk-brand-dark);
}
.st-key-bk_auth_card p.bk-auth-sub {
    margin: 0 0 1rem 0;
    font-size: 0.85rem;
    color: var(--bk-muted);
}
.st-key-bk_auth_card [role="tablist"] {
    gap: 0.35rem;
    border-bottom: none;
    margin-bottom: 1.1rem;
}
.st-key-bk_auth_card [data-testid="stTab"] {
    border-radius: 999px;
    padding: 0.4rem 1rem;
    background: #eef4fb;
}
.st-key-bk_auth_card [data-testid="stTab"]:hover {
    background: #dde9f6;
}
.st-key-bk_auth_card [data-testid="stTab"] p {
    color: #475569;
    font-weight: 600;
    font-size: 0.87rem;
}
.st-key-bk_auth_card [data-testid="stTab"][aria-selected="true"] {
    background: linear-gradient(135deg, #1e68af, #3d84c6);
}
.st-key-bk_auth_card [data-testid="stTab"][aria-selected="true"] p {
    color: #ffffff;
}
.st-key-bk_auth_card .react-aria-SelectionIndicator {
    display: none;
}
.st-key-bk_auth_card [role="tablist"]::after {
    display: none;
}
.st-key-bk_auth_card [data-testid="stForm"] {
    background: transparent;
    border: none;
    padding: 0;
}
.st-key-bk_auth_card input[type="text"],
.st-key-bk_auth_card input[type="password"] {
    border-radius: 11px;
    border: 1px solid #d7e3f0;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
}
.st-key-bk_auth_card input[type="text"]:focus,
.st-key-bk_auth_card input[type="password"]:focus {
    border-color: var(--bk-brand);
    box-shadow: 0 0 0 3px rgba(30, 104, 175, 0.14);
}
.st-key-bk_auth_card label {
    font-size: 0.82rem;
    font-weight: 600;
    color: #334155;
}
.st-key-bk_auth_card .stButton > button {
    border-radius: 11px;
    font-weight: 600;
    padding-top: 0.45rem;
    padding-bottom: 0.45rem;
}
.st-key-bk_auth_card [data-testid="stCaptionContainer"] {
    font-size: 0.74rem;
}
.bk-auth-hint {
    display: flex;
    gap: 0.5rem;
    align-items: flex-start;
    background: #f1f7fd;
    border: 1px solid #d7e3f0;
    border-radius: 12px;
    padding: 0.62rem 0.8rem;
    font-size: 0.78rem;
    color: #33506f;
    margin-bottom: 1rem;
}
.bk-auth-hint b {
    color: var(--bk-brand-dark);
}
.bk-auth-hint-icon {
    flex: none;
    width: 1.15rem;
    height: 1.15rem;
    margin-top: 0.04rem;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: var(--bk-brand);
    color: #ffffff;
    font-size: 0.74rem;
    font-weight: 800;
    font-style: italic;
}
.bk-auth-foot {
    margin-top: 1.1rem;
    padding-top: 0.9rem;
    border-top: 1px solid #eef2f6;
    font-size: 0.76rem;
    color: var(--bk-muted);
    text-align: center;
}
@media (max-width: 900px) {
    .st-key-bk_auth_card [data-testid="stColumn"] {
        padding: 1.5rem 1.3rem;
    }
}
.bk-user-cell {
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.bk-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    background: linear-gradient(145deg, #5c9fd6, #1e68af);
    color: #ffffff;
    font-weight: 800;
    font-size: 0.85rem;
    flex: none;
}
.bk-user-cell b { color: var(--bk-ink); font-size: 0.9rem; }
.bk-user-cell span { color: var(--bk-muted); font-size: 0.75rem; }
.bk-log-chip {
    display: inline-block;
    padding: 0.15rem 0.48rem;
    border-radius: 6px;
    background: #eef2f6;
    color: #475569;
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}
@media (max-width: 740px) {
    .bk-hero { flex-direction: column; padding: 1.25rem; }
    .bk-hero h1 { font-size: 1.55rem; }
    .bk-page-head h1 { font-size: 1.5rem; }
    .bk-seat-grid { max-width: 100%; }
}
</style>
"""


def terapkan_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


FOLDER_ASET = Path(__file__).resolve().parent / "assets"


@st.cache_data(show_spinner=False)
def _logo_data_uri() -> str:
    berkas = FOLDER_ASET / "logo-sidebar.png"
    if not berkas.exists():
        return ""
    data = base64.b64encode(berkas.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


def logo_data_uri() -> str:
    """Logo sebagai data URI (dipakai di halaman login)."""
    return _logo_data_uri()


def sidebar_brand() -> None:
    logo = _logo_data_uri()
    if logo:
        isi = (
            '<div class="bk-brand-logo-wrap">'
            f'<img class="bk-brand-logo" src="{logo}" alt="Logo Berkelana Travel">'
            "</div>"
            '<div class="bk-brand-sub">Sistem Administrasi</div>'
        )
    else:
        isi = (
            '<div class="bk-brand-icon">BT</div>'
            "<div>"
            '<div class="bk-brand-name">Berkelana Travel</div>'
            '<div class="bk-brand-sub">Sistem Administrasi</div>'
            "</div>"
        )
    st.markdown(f'<div class="bk-brand">{isi}</div>', unsafe_allow_html=True)


def sidebar_note(teks_html: str) -> None:
    st.markdown(f'<div class="bk-sidebar-note">{teks_html}</div>', unsafe_allow_html=True)


def page_header(judul: str, deskripsi: str) -> None:
    st.markdown(
        f"""
        <div class="bk-page-head">
            <h1>{esc(judul)}</h1>
            <p>{esc(deskripsi)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(judul: str, deskripsi: str, tanggal: str) -> None:
    st.markdown(
        f"""
        <div class="bk-hero">
            <div class="bk-hero-copy">
                <span class="bk-eyebrow">Sistem Administrasi Travel</span>
                <h1>{esc(judul)}</h1>
                <p>{esc(deskripsi)}</p>
            </div>
            <div class="bk-hero-date">{esc(tanggal)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrik(
    label: str,
    nilai: str,
    sub: str = "",
    aksen: bool = False,
) -> None:
    kelas = "bk-metric accent" if aksen else "bk-metric"
    st.markdown(
        f"""
        <div class="{kelas}">
            <div class="bk-metric-top">
                <span class="bk-metric-label">{esc(label)}</span>
            </div>
            <div class="bk-metric-value">{esc(nilai)}</div>
            <div class="bk-metric-sub">{esc(sub)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def judul_bagian(judul: str, keterangan: str = "") -> None:
    st.markdown(
        f"""
        <div class="bk-section-title">
            <h3>{esc(judul)}</h3>
            <span>{esc(keterangan)}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(teks: str, warna: str = "teal") -> str:
    return f'<span class="bk-badge {esc(warna)}">{esc(teks)}</span>'


def badge_status_aktif(aktif: bool | int, label_aktif: str = "Aktif", label_nonaktif: str = "Nonaktif") -> str:
    return badge(label_aktif, "green") if aktif else badge(label_nonaktif, "grey")


def set_flash(jenis: str, pesan: str) -> None:
    """jenis: success, error, warning, info."""
    st.session_state.setdefault("_flash", []).append((jenis, pesan))


def tampilkan_flash() -> None:
    pesan = st.session_state.pop("_flash", [])
    for jenis, teks in pesan:
        getattr(st, jenis)(teks)


def denah_kursi(
    daftar_kursi: Iterable[Mapping[str, Any]],
    terpakai: Mapping[int, str] | None = None,
    dipilih: Iterable[int] = (),
    label_depan: str = "Depan kendaraan",
) -> None:
    terpakai = terpakai or {}
    dipilih_set = {int(x) for x in dipilih}
    kartu: list[str] = []
    for k in daftar_kursi:
        kid = int(k["id_kursi"])
        nomor = str(k["nomor_kursi"])
        aktif = bool(k.get("status_aktif", 1))
        if not aktif:
            kelas, status = "inactive", "Nonaktif"
            judul = f"{nomor} — nonaktif"
        elif kid in terpakai:
            kelas, status = "booked", "Dipesan"
            judul = f"{nomor} — dipesan"
        elif kid in dipilih_set:
            kelas, status = "selected", "Dipilih"
            judul = f"{nomor} — dipilih"
        else:
            kelas, status = "", "Tersedia"
            judul = f"{nomor} — tersedia"
        kartu.append(
            f'<div class="bk-seat {kelas}" title="{esc(judul)}">'
            f'<div class="num">{esc(nomor)}</div><div class="st">{esc(status)}</div></div>'
        )
    st.markdown(
        f"""
        <div class="bk-seat-shell">
            <div class="bk-bus-front"><span class="bk-bus-mark"></span>{esc(label_depan)}</div>
            <div class="bk-seat-grid">{''.join(kartu)}</div>
            <div class="bk-legend">
                <span><i style="background:#bbf7d0"></i>Tersedia</span>
                <span><i style="background:#f59e0b"></i>Dipilih</span>
                <span><i style="background:#cbd5e1"></i>Sudah dipesan</span>
                <span><i style="background:#f8fafc;border:1px dashed #cbd5e1"></i>Nonaktif</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kartu_perjalanan(data: Mapping[str, Any], boleh_batal: bool = False) -> None:
    """Kartu ringkas satu pemesanan."""
    st.markdown(
        f"""
        <div class="bk-trip">
            <div class="bk-trip-top">
                <span class="bk-trip-code">{esc(data.get('kode_pemesanan', '-'))}</span>
                {badge('AKTIF', 'green')}
            </div>
            <div class="bk-trip-route">
                {esc(data.get('kota_asal', '-'))}<span class="arrow">→</span>{esc(data.get('kota_tujuan', '-'))}
            </div>
            <div class="bk-trip-meta">
                <span><em>Jadwal:</em> <b>{esc(data.get('kode_jadwal') or data.get('kode_rute', '-'))}</b></span>
                <span><em>Tanggal:</em> <b>{esc(tanggal_indo(data.get('tanggal_keberangkatan', date.today())))}</b></span>
                <span><em>Jam:</em> <b>{esc(jam_indo(data.get('jam_keberangkatan', '00:00')))}</b></span>
                <span><em>Kursi:</em> <b>{esc(data.get('nomor_kursi', '-'))}</b></span>
                <span><em>Tiket:</em> <b>{esc(data.get('jumlah_pesan_tiket', 0))}</b></span>
                <span><em>Total:</em> <b>{esc(rupiah(data.get('total_harga')))}</b></span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kartu_jadwal(data: Mapping[str, Any], kapasitas: int) -> None:
    """Kartu jadwal keberangkatan dengan indikator keterisian."""
    tiket = int(data.get("tiket_terjual", data.get("jumlah_pesan_tiket", 0)) or 0)
    persen = min(100, round(tiket / kapasitas * 100)) if kapasitas else 0
    sisa = max(kapasitas - tiket, 0)
    tanggal = data.get("tanggal_keberangkatan", date.today())
    jam = data.get("jam_keberangkatan", "00:00")
    st.markdown(
        f"""
        <div class="bk-trip" style="padding:.9rem 1rem;margin-bottom:.55rem">
            <div class="bk-trip-top" style="margin-bottom:.25rem">
                <span class="bk-trip-code">{esc(data.get('kode_jadwal') or data.get('kode_rute', '-'))} · {esc(tanggal_singkat(tanggal))}</span>
                {badge(f'{sisa} kursi tersisa', 'green' if sisa > 2 else 'amber')}
            </div>
            <div class="bk-trip-route" style="font-size:1.08rem;margin-bottom:.3rem">
                {esc(data.get('kota_asal', '-'))}<span class="arrow">→</span>{esc(data.get('kota_tujuan', '-'))}
            </div>
            <div class="bk-trip-meta" style="font-size:.77rem">
                <span><em>Jam:</em> {esc(jam_indo(jam))}</span>
                <span><em>Kursi:</em> {esc(tiket)}/{esc(kapasitas)}</span>
                <span><em>Pemesanan:</em> {esc(data.get('jumlah_pemesanan', 0))}</span>
            </div>
            <div style="height:6px;background:#e8eef0;border-radius:99px;margin-top:.55rem;overflow:hidden">
                <div style="height:100%;width:{persen}%;background:{'#f59e0b' if persen >= 75 else '#1e68af'};border-radius:99px"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kartu_pelanggan(data: Mapping[str, Any]) -> None:
    st.markdown(
        f"""
        <div class="bk-profile">
            <div>{badge(str(data.get('kode_pelanggan', '-')), 'teal')}</div>
            <div class="bk-profile-name">{esc(data.get('nama_pelanggan', '-'))}</div>
            <div class="bk-profile-sub">{esc(data.get('nomor_telepon', '-'))} &nbsp;·&nbsp; Terdaftar {esc(waktu_lengkap(data.get('dibuat_pada')))}</div>
            <div class="bk-profile-stats">
                <div class="bk-profile-stat"><span>Pemesanan</span><b>{esc(data.get('jumlah_pemesanan', 0))}</b></div>
                <div class="bk-profile-stat"><span>Tiket</span><b>{esc(data.get('total_tiket', 0))}</b></div>
                <div class="bk-profile-stat"><span>Total belanja</span><b>{esc(rupiah(data.get('total_belanja', 0)))}</b></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kotak_harga(
    harga_satuan: int,
    jumlah: int,
    total: int,
    label_kursi: str = "",
) -> None:
    st.markdown(
        f"""
        <div class="bk-price-box">
            <div class="row"><span>Harga per tiket</span><span>{esc(rupiah(harga_satuan))}</span></div>
            <div class="row"><span>Jumlah tiket</span><span>{esc(jumlah)} tiket</span></div>
            <div class="row"><span>Kursi dipilih</span><span>{esc(label_kursi or '-')}</span></div>
            <div class="row total"><span>Total bayar</span><b>{esc(rupiah(total))}</b></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(judul: str, pesan: str) -> None:
    st.markdown(
        f"""
        <div class="bk-empty">
            <div class="mark"></div>
            <div style="font-weight:800;color:#334155;margin-bottom:.25rem">{esc(judul)}</div>
            <div style="font-size:.84rem">{esc(pesan)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def nota(data: Mapping[str, Any], key_prefix: str = "nota") -> None:
    """Menampilkan nota teks dan tombol unduh."""
    teks = buat_teks_nota(dict(data))
    with st.container(border=True):
        st.markdown(
            '<div class="bk-receipt-head">Nota Pemesanan</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Tunjukkan atau cetak nota ini sebagai bukti pemesanan. "
            "Pembayaran dan pengembalian dana dilakukan di luar sistem."
        )
        st.code(teks, language=None)
        st.download_button(
            "Unduh nota (.txt)",
            data=teks.encode("utf-8"),
            file_name=nama_file_nota(dict(data)),
            mime="text/plain",
            key=f"{key_prefix}_unduh_nota",
        )


def ringkasan_jadwal_teks(tanggal: date, jam: time) -> str:
    return f"{tanggal_singkat(tanggal)} · {jam_indo(jam)}"

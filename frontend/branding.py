"""Canonical HealthBrief logo and wordmark, shared by the two real pages."""
import base64
from html import escape
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).parent
LOGO_SVG = (_ROOT / "assets/healthbrief_logo.svg").read_text(encoding="utf-8")
LOGO_URL = "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("ascii")
_CSS = (_ROOT / "styles/branding.css").read_text(encoding="utf-8")


def render_brand(subtitle: str, *, heading: bool = False) -> None:
    tag = "h1" if heading else "p"
    st.html(
        f'<style>{_CSS}</style><div class="hb-brand">'
        f'<img src="{LOGO_URL}" alt="HealthBrief report monogram">'
        '<div class="hb-brand-copy">'
        f'<{tag} class="hb-brand-wordmark">Health<span>Brief</span></{tag}>'
        f'<p class="hb-brand-subtitle">{escape(subtitle)}</p>'
        '</div></div>'
    )

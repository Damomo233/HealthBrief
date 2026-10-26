from pathlib import Path

import streamlit as st
from branding import LOGO_SVG, render_brand
from showcase import render_showcase
from features import render_features


FRONTEND_DIR = Path(__file__).parent
homepage_css = (FRONTEND_DIR / "styles" / "homepage.css").read_text(encoding="utf-8")

st.set_page_config(page_title="HealthBrief", page_icon=LOGO_SVG)
st.html(f"<style>{homepage_css}</style>")

with st.container(key="hb_home"):
    with st.container(key="hb_home_nav"):
        brand_column, features_column, start_column = st.columns(
            [6, 1.1, 1.3], gap="small", vertical_alignment="center"
        )
        with brand_column:
            render_brand("Your trusted automated health companion")
        with features_column:
            st.html('<a class="hb-home-nav-link" href="#hb-core-functions">Features</a>')
        with start_column:
            st.html('<a class="hb-home-start" href="#hb-core-functions">Get Started</a>')

    with st.container(key="hb_home_hero"):
        st.html(
            '<div class="hb-home-intro">'
            '<p class="hb-home-product">HealthBrief</p>'
            '<p class="hb-home-tagline">Your trusted automated health companion</p>'
            '</div>'
            '<h1 class="hb-home-headline">'
            '<span class="hb-home-headline-first">Understand Your Medical Data</span><br>'
            '<span class="hb-home-emphasis">easier, clearer, smarter</span>'
            '</h1>'
            '<p class="hb-home-description">'
            'HealthBrief helps you read lab reports, compare trends, and prepare better '
            'questions for your next doctor visit. Try a guided preview with a sample report today.'
            '</p>'
        )
        with st.container(key="hb_home_cta"):
            st.html('<a class="hb-home-start" href="#hb-core-functions">Get Started</a>')

    render_showcase()
    # A real light-DOM target works with native anchors without JavaScript.
    st.html('<div id="hb-core-functions" class="hb-scroll-target" tabindex="-1" aria-label="HealthBrief core functions"></div>')
    render_features()

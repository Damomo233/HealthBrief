"""Local-asset showcase; its controls never rerun the report workflow."""
import base64
from pathlib import Path

import streamlit as st
from streamlit.components.v2 import component

FRONTEND_DIR = Path(__file__).parent
# Replace only this asset to refresh the product preview without changing layout.
PRODUCT_PREVIEW = FRONTEND_DIR / 'assets/dashboard_preview.png'

_HTML = '''
<section class="showcase" aria-label="HealthBrief visual showcase" aria-roledescription="carousel">
  <div class="stage" data-focus="0" role="group" aria-roledescription="slide">
    <figure class="visual product"><div class="product-image"><img alt="Actual HealthBrief Dashboard showing a sample lab report" draggable="false"></div><span class="preview-note">Dashboard · sample data</span></figure>
    <figure class="visual doctor"><img alt="Professional female doctor in a white coat" draggable="false"></figure>
    <figure class="visual man"><img alt="Older man reading his smartphone" draggable="false"></figure>
    <figure class="visual woman"><img alt="Older woman reading her smartphone" draggable="false"></figure>
  </div>
  <div class="controls" aria-label="Showcase controls">
    <button class="arrow previous" type="button" aria-label="Previous showcase view"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m14 5-7 7 7 7"/></svg></button>
    <div class="dots" role="group" aria-label="Choose showcase view">
      <button class="dot" type="button" aria-label="Show product preview" aria-current="true"></button>
      <button class="dot" type="button" aria-label="Show professional doctor" aria-current="false"></button>
      <button class="dot" type="button" aria-label="Show older man" aria-current="false"></button>
      <button class="dot" type="button" aria-label="Show older woman" aria-current="false"></button>
    </div>
    <button class="arrow next" type="button" aria-label="Next showcase view"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="m10 5 7 7-7 7"/></svg></button>
  </div>
  <p class="caption" aria-live="polite" aria-atomic="true">Understand your report</p>
</section>
'''

_showcase = component(
    'healthbrief_showcase',
    html=_HTML,
    css=(FRONTEND_DIR / 'styles/showcase.css').read_text(encoding='utf-8'),
    js=(FRONTEND_DIR / 'showcase.js').read_text(encoding='utf-8'),
    isolate_styles=True,
)


@st.cache_data(show_spinner=False, max_entries=8)
def _image_url(path: str, modified_ns: int) -> str:
    """Cache encoding; the file timestamp invalidates a replaced preview."""
    return 'data:image/png;base64,' + base64.b64encode(Path(path).read_bytes()).decode('ascii')


def render_showcase() -> None:
    paths = [PRODUCT_PREVIEW] + [FRONTEND_DIR / 'assets' / f'portrait_{i}.png' for i in (1, 2, 3)]
    images = [_image_url(str(path), path.stat().st_mtime_ns) for path in paths]
    _showcase(data={'images': images}, key='hb_showcase', height='content', width='stretch')

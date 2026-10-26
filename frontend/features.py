"""Homepage capability strip and real Dashboard navigation."""
import base64
from pathlib import Path

import streamlit as st
from streamlit.components.v2 import component
from branding import LOGO_URL

FRONTEND_DIR = Path(__file__).parent

_HTML = '''
<section class="hb-features" aria-labelledby="hb-features-title">
  <header class="feature-intro">
    <h2 id="hb-features-title">From Complex Report to Clear Insights</h2>
    <p class="section-copy">Read your report, compare two check-ups, and prepare clearer questions for your doctor.</p>
  </header>

  <div class="feature-grid">
    <article class="feature-panel" aria-labelledby="analysis-title">
      <div class="feature-visual analysis-visual" role="img" aria-label="Illustration of a text-based PDF becoming structured biomarker information">
        <div class="paper" aria-hidden="true">
          <span class="paper-fold"></span><span class="paper-label">LAB REPORT</span>
          <i class="paper-line wide"></i><i class="paper-line"></i><i class="paper-line short"></i>
          <div class="paper-rule"></div>
          <i class="paper-line"></i><i class="paper-line wide"></i><i class="paper-line short"></i>
          <span class="pdf-label">PDF</span>
        </div>
        <svg class="extract-connector" aria-hidden="true" viewBox="0 0 48 24"><path d="M2 12h38m-8-7 8 7-8 7"/></svg>
        <div class="extracted" aria-hidden="true">
          <span class="mini-label">Extracted results</span>
          <div class="field-row"><span>Biomarker</span><strong>LDL</strong></div>
          <div class="field-row"><span>Value</span><strong>3.7 mmol/L</strong></div>
          <div class="field-row"><span>Reference</span><strong>≤ 3.4</strong></div>
          <span class="example-label extraction-note">Sample extraction</span>
        </div>
      </div>
      <div class="feature-content">
        <h3 id="analysis-title">Current Report Analysis</h3>
        <p>Upload a text-based PDF to review key biomarkers, values, units, and reference ranges in one structured view.</p>
        <a class="learn-more" href="dashboard" data-feature="0" aria-label="Learn more about Current Report Analysis in Dashboard">Learn more <span aria-hidden="true">→</span></a>
      </div>
    </article>

    <article class="feature-panel" aria-labelledby="biomarker-title">
      <div class="feature-visual biomarker-visual" role="img" aria-label="Sample biomarker values showing high LDL, normal HDL, and low hemoglobin">
        <div class="biomarker-sheet" aria-hidden="true">
          <div class="mini-heading"><span>Key biomarkers</span><span class="example-label">Sample data</span></div>
          <div class="biomarker-row"><div><strong>LDL</strong><small>Reference ≤ 3.4 mmol/L</small></div><span class="marker-value">3.7 <small>mmol/L</small></span><span class="status high">HIGH</span></div>
          <div class="biomarker-row"><div><strong>HDL</strong><small>Reference ≥ 1.0 mmol/L</small></div><span class="marker-value">1.4 <small>mmol/L</small></span><span class="status normal">NORMAL</span></div>
          <div class="biomarker-row"><div><strong>Hemoglobin</strong><small>Reference 120–170 g/L</small></div><span class="marker-value">110 <small>g/L</small></span><span class="status low">LOW</span></div>
        </div>
      </div>
      <div class="feature-content">
        <h3 id="biomarker-title">Biomarker Visualization</h3>
        <p>Review values, units, and reference ranges together, with clear normal, high, and low result status.</p>
        <a class="learn-more" href="dashboard" data-feature="1" aria-label="Learn more about Biomarker Visualization in Dashboard">Learn more <span aria-hidden="true">→</span></a>
      </div>
    </article>

    <article class="feature-panel" aria-labelledby="comparison-title">
      <div class="feature-visual comparison-visual" role="img" aria-label="Illustrative comparison of LDL in one previous report and the current report, 4.2 and 3.7 mmol per liter">
        <div class="comparison-sheet" aria-hidden="true">
          <div class="mini-heading"><span>LDL <small>mmol/L</small></span><span class="example-label">Sample data</span></div>
          <div class="comparison-values"><div><span>Previous report</span><strong>4.2</strong></div><div><span>Current report</span><strong>3.7</strong></div></div>
          <svg class="comparison-chart" viewBox="0 0 300 110" aria-hidden="true">
            <rect class="reference-band" x="20" y="69" width="260" height="27" rx="3"/>
            <path class="chart-grid" d="M20 35h260M20 69h260M20 96h260"/>
            <text class="reference-label" x="273" y="87" text-anchor="end">Reference ≤ 3.4</text>
            <path class="chart-line" d="M38 25 260 55"/>
            <circle cx="38" cy="25" r="4"/><circle class="current-point" cx="260" cy="55" r="5"/>
          </svg>
          <span class="comparison-note">Two reports. A clearer comparison.</span>
        </div>
      </div>
      <div class="feature-content">
        <h3 id="comparison-title">Trend Comparison</h3>
        <p>Compare your current report with one previous report to review biomarker changes between check-ups.</p>
        <a class="learn-more" href="dashboard" data-feature="2" aria-label="Learn more about Trend Comparison in Dashboard">Learn more <span aria-hidden="true">→</span></a>
      </div>
    </article>

    <article class="feature-panel" aria-labelledby="ask-title">
      <div class="feature-visual ask-visual" role="img" aria-label="Illustrative report questions: Why is my LDL high? Has my LDL improved? What should I ask my doctor? These are non-interactive examples.">
        <div class="assistant-preview" aria-hidden="true">
          <div class="assistant-heading"><span class="assistant-icon"><img alt=""></span><span>Ask HealthBrief</span><span class="example-label">Examples</span></div>
          <div class="prompt-bubble">Understand your report results.</div>
          <div class="question-examples"><span>Why is my LDL high?</span><span>Has my LDL improved?</span><span>What should I ask my doctor?</span></div>
        </div>
      </div>
      <div class="feature-content">
        <h3 id="ask-title">Ask HealthBrief</h3>
        <p>Ask about your report results and abnormal markers, and prepare clearer questions for your next doctor visit.</p>
        <a class="learn-more" href="dashboard" data-feature="3" aria-label="Learn more about Ask HealthBrief in Dashboard">Learn more <span aria-hidden="true">→</span></a>
      </div>
    </article>
  </div>
  <aside class="closing-band" aria-label="HealthBrief's approach to clearer health conversations">
    <div class="closing-copy">
      <svg class="quote-icon" aria-hidden="true" viewBox="0 0 40 32"><path d="M3 27V16C3 8 7 4 15 3v6c-4 1-6 3-6 7h7v11Zm21 0V16c0-8 4-12 12-13v6c-4 1-6 3-6 7h7v11Z"/></svg>
      <blockquote>HealthBrief bridges the gap between complex medical data and everyday understanding.</blockquote>
      <p>Designed for clearer, more confident health conversations.</p>
    </div>
    <figure class="closing-image"><img alt="Older couple resting together on a bench beside a lake" draggable="false"></figure>
  </aside>
</section>
'''

_JS = '''
export default function({parentElement, data, setTriggerValue}) {
  const section = parentElement.querySelector('.hb-features');
  section.querySelector('.closing-image img').src = data.closing_image;
  section.querySelector('.assistant-icon img').src = data.logo;
  const links = [...section.querySelectorAll('.learn-more')];
  links.forEach(link => {
    link.onclick = event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      setTriggerValue('open_dashboard', Number(link.dataset.feature));
    };
  });
  const panels = [...section.querySelectorAll('.feature-panel')];
  const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let observer;
  function revealAll() {
    observer?.disconnect();
    panels.forEach(panel => panel.classList.remove('reveal-pending'));
  }
  // Content is visible by default if scripting or observation is unavailable.
  const cleanup = () => {
    observer?.disconnect();
    links.forEach(link => { link.onclick = null; });
    motion.removeEventListener('change', onMotionChange);
  };
  const onMotionChange = event => { if (event.matches) revealAll(); };
  if (typeof window.IntersectionObserver !== 'function' || motion.matches) return cleanup;
  try {
    observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.remove('reveal-pending');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.12, rootMargin: '0px 0px -24px 0px'});
    panels.forEach((panel, index) => {
      // Preserve content already above the viewport after a restored scroll.
      if (panel.getBoundingClientRect().bottom <= 0) return;
      panel.style.setProperty('--reveal-delay', `${index * 65}ms`);
      panel.classList.add('reveal-pending');
      observer.observe(panel);
    });
  } catch {
    revealAll();
    return cleanup;
  }
  motion.addEventListener('change', onMotionChange);
  return cleanup;
}
'''

_features = component(
    'healthbrief_features',
    html=_HTML,
    css=(FRONTEND_DIR / 'styles/features.css').read_text(encoding='utf-8'),
    js=_JS,
    isolate_styles=True,
)


@st.cache_data(show_spinner=False, max_entries=2)
def _closing_image_url(path: str, modified_ns: int) -> str:
    return 'data:image/png;base64,' + base64.b64encode(Path(path).read_bytes()).decode('ascii')


def render_features() -> None:
    image = FRONTEND_DIR / 'assets/calmtime.png'
    result = _features(
        data={'closing_image': _closing_image_url(str(image), image.stat().st_mtime_ns), 'logo': LOGO_URL},
        key='hb_features', height='content', width='stretch',
        on_open_dashboard_change=lambda: None,
    )
    if result.open_dashboard is not None:
        st.switch_page('dashboard.py')

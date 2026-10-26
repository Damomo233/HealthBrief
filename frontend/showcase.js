export default function(component) {
  const { parentElement, data } = component;
  const root = parentElement.querySelector('.showcase');
  const stage = root.querySelector('.stage');
  const captions = ['Understand your report', 'Review key biomarkers', 'Compare check-ups', 'Ask better questions'];
  const names = ['Product preview', 'Professional doctor', 'Older man using a smartphone', 'Older woman using a smartphone'];
  const images = [...root.querySelectorAll('.visual img')];
  images.forEach((img, i) => { img.src = data.images[i]; });
  const dots = [...root.querySelectorAll('.dot')];
  let current = Number(stage.dataset.focus || 0);
  function show(index) {
    current = (index + 4) % 4;
    stage.dataset.focus = String(current);
    dots.forEach((dot, i) => dot.setAttribute('aria-current', String(i === current)));
    root.querySelector('.caption').textContent = captions[current];
    stage.setAttribute('aria-label', `${current + 1} of 4: ${names[current]}`);
  }
  root.querySelector('.previous').onclick = () => show(current - 1);
  root.querySelector('.next').onclick = () => show(current + 1);
  dots.forEach((dot, i) => { dot.onclick = () => show(i); });
  root.onkeydown = event => {
    if (!['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) return;
    event.preventDefault();
    show(event.key === 'Home' ? 0 : event.key === 'End' ? 3 : current + (event.key === 'ArrowRight' ? 1 : -1));
  };
  show(current);
  // No timers, document listeners or Python callbacks: navigation stays independent.
  return () => {
    root.onkeydown = null;
    root.querySelectorAll('button').forEach(button => { button.onclick = null; });
  };
}

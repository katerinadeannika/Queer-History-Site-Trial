(() => {
  const button = document.querySelector('[data-nav-toggle]');
  const layout = document.querySelector('.reference-layout');
  if (!button || !layout) return;
  const set = (open) => {
    layout.classList.toggle('nav-open', open);
    button.setAttribute('aria-expanded', String(open));
    button.setAttribute('aria-label', open ? 'Close chapter navigation' : 'Open chapter navigation');
  };
  button.addEventListener('click', () => set(!layout.classList.contains('nav-open')));
  document.addEventListener('keydown', (event) => { if (event.key === 'Escape') set(false); });
})();
(() => {
  const header = document.querySelector('.site-header');
  const hero = document.querySelector('.home-hero'); // MUST be the hero section element
  if (!header || !hero) return;

  const clamp01 = (n) => Math.max(0, Math.min(1, n));

  function onScroll() {
    const rect = hero.getBoundingClientRect();
    const h = rect.height || 1;

    // 0 when hero top is at top of viewport
    // 0.5 when hero is half off (top = -0.5h)
    // 1 when hero is fully off (top = -h)
    const t = clamp01((-rect.top) / h);

    header.style.setProperty('--hdr', t.toFixed(3));

    // Keep class-based styles in sync with the scroll progress.
    header.classList.toggle('is-transparent', t < 0.05);
    header.classList.toggle('is-scrolled', t > 0.95);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();
})();

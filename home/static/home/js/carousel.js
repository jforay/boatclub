document.querySelectorAll('.rotater-container').forEach(container => {
  const carousel = container.querySelector('.rotater');
  const prevBtn = container.querySelector('.rotater-btn.prev');
  const nextBtn = container.querySelector('.rotater-btn.next');
  const items = Array.from(container.querySelectorAll('.rotater-item'));
  const totalItems = items.length;
  const intervalMs = Number(container.dataset.interval) || 4000;

  if (!carousel || totalItems === 0) return;

  let currentIndex = 0;
  let autoTimer = null;

  function setTransition(enabled) {
    carousel.style.transition = enabled ? 'transform .8s ease-in-out' : 'none';
  }

  function updateCarousel() {
    carousel.style.transform = `translateX(${-100 * currentIndex}%)`;
  }

  function goTo(index, { animate = true } = {}) {
    if (index < 0) index = totalItems - 1;
    if (index >= totalItems) index = 0;

    setTransition(animate);
    currentIndex = index;
    updateCarousel();
  }

  function scheduleNext() {
    clearTimeout(autoTimer);
    autoTimer = setTimeout(() => {
      // If we're at the last slide, snap back to first (no animation).
      if (currentIndex === totalItems - 1) {
        goTo(0, { animate: false });
        // Re-enable transition for next moves
        requestAnimationFrame(() => setTransition(true));
      } else {
        goTo(currentIndex + 1, { animate: true });
      }
      scheduleNext();
    }, intervalMs);
  }

  nextBtn?.addEventListener('click', () => {
    clearTimeout(autoTimer);
    goTo(currentIndex + 1);
    scheduleNext();
  });

  prevBtn?.addEventListener('click', () => {
    clearTimeout(autoTimer);
    goTo(currentIndex - 1);
    scheduleNext();
  });

  // Init
  setTransition(false);
  goTo(0, { animate: false });
  requestAnimationFrame(() => setTransition(true));
  scheduleNext();
});

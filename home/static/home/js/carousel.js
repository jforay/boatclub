document.querySelectorAll('.rotater-container').forEach(container => {
    const carousel = container.querySelector('.rotater');
    const prevBtn = container.querySelector('.rotater-btn.prev');
    const nextBtn = container.querySelector('.rotater-btn.next');
    const items = Array.from(container.querySelectorAll('.rotater-item'));
    const totalItems = items.length;
    const intervalMs = Number(container.dataset.interval) || 4000;

    if (totalItems === 0) return;

    // Clone ends for seamless loop
    const firstClone = items[0].cloneNode(true);
    const lastClone = items[totalItems - 1].cloneNode(true);
    carousel.appendChild(firstClone);
    carousel.insertBefore(lastClone, items[0]);

    let currentIndex = 1;      // start on first real slide
    let isJumping = false;     // prevents visible snap logic
    let autoTimer = null;

    function setTransition(enabled) {
        carousel.style.transition = enabled ? 'transform .8s ease-in-out' : 'none';
    }

    function updateCarousel() {
        const offset = currentIndex * -100;
        carousel.style.transform = `translateX(${offset}%)`;
    }

    function scheduleNext() {
        clearTimeout(autoTimer);
        autoTimer = setTimeout(() => {
            goTo(currentIndex + 1);
        }, intervalMs);
    }

    function goTo(index, { animate = true } = {}) {
        setTransition(animate);
        currentIndex = index;
        updateCarousel();

        // If we are NOT animating (initial load / instant jump),
        // schedule immediately because there won't be a transitionend.
        if (!animate) {
            requestAnimationFrame(() => setTransition(true));
            scheduleNext();
        }
        // If we ARE animating, we schedule in transitionend
        // so the timer starts when the new slide is fully visible.
    }

    function jumpTo(index) {
        isJumping = true;
        setTransition(false);
        currentIndex = index;
        updateCarousel();

        // Re-enable transition on the next frame
        requestAnimationFrame(() => {
            setTransition(true);
            isJumping = false;

            // After a clone->real jump, the "real" slide is now visible
            // (still no animation), so restart the timer here.
            scheduleNext();
        });
    }

    nextBtn?.addEventListener('click', () => {
        clearTimeout(autoTimer);
        goTo(currentIndex + 1);
    });

    prevBtn?.addEventListener('click', () => {
        clearTimeout(autoTimer);
        goTo(currentIndex - 1);
    });

    carousel.addEventListener('transitionend', event => {
        if (event.target !== carousel || isJumping) return;

        // Handle wraparound
        if (currentIndex === totalItems + 1) {
            jumpTo(1); // cloned first -> real first
            return;
        }
        if (currentIndex === 0) {
            jumpTo(totalItems); // cloned last -> real last
            return;
        }

        // Normal slide finished animating -> start full interval now
        scheduleNext();
    });

    // Init at first real slide (no animation) AND start autoplay
    goTo(1, { animate: false });
});

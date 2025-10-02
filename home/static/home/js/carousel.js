document.querySelectorAll('.carousel-container').forEach(container => {
    const carousel = container.querySelector('.carousel'); // Scope carousel
    const prevBtn = container.querySelector('.carousel-btn.prev'); // Scope prev button
    const nextBtn = container.querySelector('.carousel-btn.next'); // Scope next button
    const items = container.querySelectorAll('.carousel-item'); // Scope items
    const totalItems = items.length; // Calculate total items in the current carousel
    let currentIndex = 0;

    function updateCarousel() {
        const offset = currentIndex * -100; // Move by index
        carousel.style.transform = `translateX(${offset}%)`;
    }

    // Event listener for next button
    nextBtn.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    });

    // Event listener for previous button
    prevBtn.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    });

    // Auto-slide every 7 seconds
    setInterval(() => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    }, 7000);

    // Initialize carousel (if not empty)
    if (totalItems > 0) {
        updateCarousel();
    }
});

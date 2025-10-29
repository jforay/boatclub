let currentIndex = 0;
console.log("✅ boat_detail.js loaded");

function setImage(index) {
    currentIndex = index;
    document.getElementById('mainImage').src = images[index];
    updateActiveThumbnail();
}

function changeImage(direction) {
    currentIndex += direction;
    if (currentIndex < 0) currentIndex = images.length - 1;
    if (currentIndex >= images.length) currentIndex = 0;
    document.getElementById('mainImage').src = images[currentIndex];
    updateActiveThumbnail();
}

function updateActiveThumbnail() {
    let thumbs = document.querySelectorAll('.thumbnail');
    thumbs.forEach((t, i) => {
        t.classList.toggle('active', i === currentIndex);
    });
}

document.addEventListener('DOMContentLoaded', updateActiveThumbnail);

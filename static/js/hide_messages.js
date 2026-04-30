setTimeout(() => {
const msg = document.querySelector('.message-container');
if (msg) {
    msg.style.opacity = '0';
    msg.style.transition = 'opacity 0.5s ease';
    setTimeout(() => msg.remove(), 500);
}
}, 3000);

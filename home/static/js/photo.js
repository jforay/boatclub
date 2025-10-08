document.addEventListener("DOMContentLoaded", function () {
  const photos = document.querySelectorAll('.scroll-photo');

  const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        console.log("Photo in view!"); // <-- test log

        entry.target.classList.add('in-view');
      }
      else{
        entry.target.classList.remove('in-view');
      }
    });
  }, { threshold: 0.2 }); // trigger when 20% visible

  photos.forEach(photo => {
    observer.observe(photo);
  });
});

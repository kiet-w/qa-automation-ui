/**
 * reporting/assets/js/lightbox.js - Evidence screenshot modal viewer.
 */

window.openLightbox = function (imgSrc, title) {
    const modal = document.getElementById("lightboxModal");
    const modalImg = document.getElementById("lightboxImg");
    if (modal && modalImg) {
        modalImg.src = imgSrc;
        modal.classList.add("active");
    }
};

window.closeLightbox = function () {
    const modal = document.getElementById("lightboxModal");
    if (modal) {
        modal.classList.remove("active");
    }
};

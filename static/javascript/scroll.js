function duplicateSlides(sliderId) {
    const sliderTrack = document.querySelector(`#${sliderId} .slider-track`);
    const slides = Array.from(sliderTrack.children);
    slides.forEach((slide) => {
        const clone = slide.cloneNode(true);
        sliderTrack.appendChild(clone);
    });
}

duplicateSlides("slider1");
duplicateSlides("slider2");
duplicateSlides("slider3");
duplicateSlides("slider4");
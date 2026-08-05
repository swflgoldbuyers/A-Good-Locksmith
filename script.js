// ======================================
// MOBILE MENU
// ======================================

const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

if (menuToggle && navLinks) {

    menuToggle.addEventListener("click", () => {

        navLinks.classList.toggle("active");

    });

    document.querySelectorAll(".nav-links a").forEach(link => {

        link.addEventListener("click", () => {

            navLinks.classList.remove("active");

        });

    });

}

// ======================================
// HEADER SCROLL EFFECT
// ======================================

const header = document.querySelector("header");

window.addEventListener("scroll", () => {

    if (!header) return;

    if (window.scrollY > 40) {

        header.classList.add("scrolled");

    } else {

        header.classList.remove("scrolled");

    }

});

// ======================================
// SCROLL REVEAL ANIMATIONS
// ======================================

const revealElements = document.querySelectorAll(`
.service-row,
.about-layout,
.feature-card,
.stat-card,
.location-pill,
.article-card,
.hero-content,
.section-heading,
.faq-item
`);

const revealObserver = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

            revealObserver.unobserve(entry.target);

        }

    });

}, {

    threshold: 0.12,
    rootMargin: "0px 0px -40px 0px"

});

revealElements.forEach(el => {

    el.classList.add("hidden");

    revealObserver.observe(el);

});

// ======================================
// ACTIVE NAV LINKS
// ======================================

const sections = document.querySelectorAll("section[id]");
const navItems = document.querySelectorAll(".nav-links a");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const top = section.offsetTop - 140;
        const height = section.offsetHeight;

        if (window.scrollY >= top && window.scrollY < top + height) {

            current = section.id;

        }

    });

    navItems.forEach(link => {

        link.classList.remove("active-link");

        if (link.getAttribute("href") === "#" + current) {

            link.classList.add("active-link");

        }

    });

});

// ======================================
// SMOOTH SCROLL
// ======================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {

            e.preventDefault();

            target.scrollIntoView({

                behavior: "smooth"

            });

        }

    });

});

// ======================================
// CURRENT YEAR
// ======================================

const year = document.querySelector("#year");

if (year) {

    year.textContent = new Date().getFullYear();

}

// ======================================
// FAQ ACCORDION
// ======================================

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach(item => {

    const button = item.querySelector(".faq-question");
    const icon = item.querySelector(".faq-icon");

    button.addEventListener("click", () => {

        const isActive = item.classList.contains("active");

        faqItems.forEach(faq => {

            faq.classList.remove("active");

            const i = faq.querySelector(".faq-icon");

            if (i) i.textContent = "+";

        });

        if (!isActive) {

            item.classList.add("active");

            if (icon) icon.textContent = "−";

        }

    });

});

// ======================================
// GOOGLE REVIEWS CAROUSEL
// ======================================

const reviewTrack = document.querySelector(".review-track");
const googleCards = document.querySelectorAll(".google-review-card");
const carouselDots = document.querySelectorAll(".carousel-dot");
const carouselPrev = document.querySelector(".carousel-prev");
const carouselNext = document.querySelector(".carousel-next");

if (reviewTrack && googleCards.length) {

    let currentIndex = 0;
    let autoTimer = null;
    const AUTO_MS = 5000;

    const getSlidesPerView = () => {

        if (window.innerWidth <= 640) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;

    };

    const getMaxIndex = () => {

        return Math.max(0, googleCards.length - getSlidesPerView());

    };

    const updateDots = () => {

        carouselDots.forEach((dot, i) => {

            const isActive = i === currentIndex;

            dot.classList.toggle("active", isActive);
            dot.setAttribute("aria-selected", isActive ? "true" : "false");

        });

    };

    const updateCarousel = () => {

        const slidesPerView = getSlidesPerView();

        if (currentIndex > getMaxIndex()) {

            currentIndex = getMaxIndex();

        }

        const card = googleCards[0];

        if (!card) return;

        const gap = 20;
        const cardWidth = card.getBoundingClientRect().width;
        const offset = currentIndex * (cardWidth + gap);

        reviewTrack.style.transform = `translateX(-${offset}px)`;

        updateDots();

    };

    const goTo = (index) => {

        currentIndex = Math.min(Math.max(0, index), getMaxIndex());

        updateCarousel();

    };

    const nextReview = () => {

        goTo(currentIndex >= getMaxIndex() ? 0 : currentIndex + 1);

    };

    const prevReview = () => {

        goTo(currentIndex <= 0 ? getMaxIndex() : currentIndex - 1);

    };

    const resetAuto = () => {

        if (autoTimer) clearInterval(autoTimer);

        autoTimer = setInterval(nextReview, AUTO_MS);

    };

    if (carouselNext) carouselNext.addEventListener("click", () => { nextReview(); resetAuto(); });
    if (carouselPrev) carouselPrev.addEventListener("click", () => { prevReview(); resetAuto(); });

    carouselDots.forEach((dot, index) => {

        dot.addEventListener("click", () => {

            goTo(Math.min(index, getMaxIndex()));

            resetAuto();

        });

    });

    window.addEventListener("resize", updateCarousel);

    const reviewCarousel = document.querySelector(".review-carousel");

    if (reviewCarousel) {

        reviewCarousel.addEventListener("mouseenter", () => {

            if (autoTimer) clearInterval(autoTimer);

        });

        reviewCarousel.addEventListener("mouseleave", resetAuto);

    }

    updateCarousel();

    resetAuto();

}

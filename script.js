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
.service-card,
.service-row,
.about-grid,
.review-card,
.stat-card,
.area-card,
.location-pill,
.trust-badge,
.article-card,
.review-carousel,
.hero-content,
.section-title,
.section-heading,
.faq-item
`);

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.classList.add("show");

            observer.unobserve(entry.target);

        }

    });

}, {

    threshold: 0.15

});

revealElements.forEach(el => {

    el.classList.add("hidden");

    observer.observe(el);

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
// REVIEW CAROUSEL
// ======================================

const reviewSlides = document.querySelectorAll(".review-slide");
const carouselDots = document.querySelectorAll(".carousel-dot");
const carouselPrev = document.querySelector(".carousel-prev");
const carouselNext = document.querySelector(".carousel-next");

if (reviewSlides.length) {

    let currentReview = 0;

    const showReview = (index) => {

        reviewSlides.forEach((slide, i) => {

            slide.classList.toggle("active", i === index);

        });

        carouselDots.forEach((dot, i) => {

            dot.classList.toggle("active", i === index);
            dot.setAttribute("aria-selected", i === index ? "true" : "false");

        });

        currentReview = index;

    };

    const nextReview = () => {

        showReview((currentReview + 1) % reviewSlides.length);

    };

    const prevReview = () => {

        showReview((currentReview - 1 + reviewSlides.length) % reviewSlides.length);

    };

    if (carouselNext) carouselNext.addEventListener("click", nextReview);
    if (carouselPrev) carouselPrev.addEventListener("click", prevReview);

    carouselDots.forEach((dot, index) => {

        dot.addEventListener("click", () => showReview(index));

    });

}

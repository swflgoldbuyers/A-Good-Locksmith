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
// GOOGLE REVIEWS DATA
// ======================================

const googleReviews = [
    {
        name: "Jill Brufsky",
        localGuide: false,
        reviewCount: 1,
        rating: 5,
        text: "Matt from A Good Locksmith was great! It was easy to set up the appointment. He was prompt and quickly changed the locks on our new home. Highly recommend!"
    },
    {
        name: "Nancy Grimmenga",
        localGuide: false,
        reviewCount: 4,
        rating: 5,
        text: "Provided good service and was very helpful and respectful. Highly recommend Matt for any future projects."
    },
    {
        name: "Jeff Smith",
        localGuide: false,
        reviewCount: 10,
        rating: 5,
        text: "5 stars is not enough. Timely, courteous, communicative, clean, efficient and totally professional. The work was completed in an exemplary manner."
    },
    {
        name: "Andrea Kovach",
        localGuide: false,
        reviewCount: 5,
        rating: 5,
        text: "Matt was great! Prompt, polite and fixed my issues ASAP!! Highly recommend!!"
    },
    {
        name: "Len Eckert",
        localGuide: false,
        reviewCount: 4,
        rating: 5,
        text: "Mike is a great guy! He was our son's baseball coach. Known him for 20 years. He does great work, honest, and timely. He relocked our whole house when we moved in. He's the best!"
    },
    {
        name: "Logan McDonald",
        localGuide: false,
        reviewCount: 6,
        rating: 5,
        text: "Very reliable, got to me in time, made a deal and was very friendly and understanding!!!"
    },
    {
        name: "Nate Winters",
        localGuide: false,
        reviewCount: 4,
        rating: 5,
        text: "Logan is absolutely amazing and treated us really well while we were visiting."
    },
    {
        name: "TNT Donuts Gaming",
        localGuide: false,
        reviewCount: 1,
        rating: 5,
        text: "Matt. Thank you. So much after hard day of work."
    },
    {
        name: "SALON SOL",
        localGuide: false,
        reviewCount: 1,
        rating: 5,
        text: "Kind, courteous, professional!"
    },
    {
        name: "Art Capri",
        localGuide: true,
        reviewCount: 45,
        rating: 5,
        text: "Great service and prices."
    },
    {
        name: "Pam Gustafson",
        localGuide: true,
        reviewCount: 22,
        rating: 5,
        text: "Mike is awesome! He called me back within 5 minutes of leaving a message and was out to fix our lock within 2 hours. Fair price, great service!!"
    },
    {
        name: "Karen K.",
        localGuide: true,
        reviewCount: 17,
        rating: 5,
        text: "Efficient. Kind. Polite, and my locks work better than they ever did! Reasonably priced as well. Highly recommend!"
    },
    {
        name: "Kimberly Kavanagh",
        localGuide: true,
        reviewCount: 24,
        rating: 5,
        text: "Within 20 minutes of my call, Mike was at my door to rekey two locks and install a mailbox lock."
    },
    {
        name: "Phil Guida",
        localGuide: true,
        reviewCount: 26,
        rating: 5,
        text: "Excellent, reliable service."
    },
    {
        name: "Gary Pottruff",
        localGuide: false,
        reviewCount: 5,
        rating: 5,
        text: "Just had the front and garage doors rekeyed by Mike. Very quick, professional and reasonably priced. Definitely recommend this company."
    },
    {
        name: "Micah Owenby",
        localGuide: true,
        reviewCount: 52,
        rating: 5,
        text: "I had my locks changed out at a business of mine. They were quick and reasonable. I would definitely recommend A Good Locksmith to anyone looking for a fair and quick locksmith."
    },
    {
        name: "Howard Feingold",
        localGuide: false,
        reviewCount: 4,
        rating: 5,
        text: "Being a second generation locksmith, Mike is very adept at his trade!"
    },
    {
        name: "Chris Reyes",
        localGuide: false,
        reviewCount: 3,
        rating: 5,
        text: "Mike is great. Showed up on time, did a great job and is just generally a terrific guy. I have already referred him to several friends. If you need a locksmith, Mike and A Good Locksmith is your guy!"
    },
    {
        name: "Patricia Forman",
        localGuide: false,
        reviewCount: 2,
        rating: 5,
        text: "I have used A Good Locksmith numerous times and they are always PROMPT, PROFESSIONAL and reasonable. Helped me a great deal when I needed special locks because a dementia family member lived in the house."
    },
    {
        name: "Pat Stark",
        localGuide: false,
        reviewCount: 2,
        rating: 5,
        text: "Several years ago I had a new door installed and called Mike to see if it could be keyed to the same key as all other locks."
    },
    {
        name: "Craig Carlson",
        localGuide: false,
        reviewCount: 8,
        rating: 5,
        text: "Mike is a professional that does great work!"
    },
    {
        name: "J Lan (Pyro Land)",
        localGuide: false,
        reviewCount: 8,
        rating: 5,
        text: "Mike did a great job!"
    },
    {
        name: "Steve Possino",
        localGuide: false,
        reviewCount: 8,
        rating: 5,
        text: "Mike is the ultimate professional and great guy. We had a challenging situation and he solved it quickly."
    },
    {
        name: "Clyde Beverung",
        localGuide: false,
        reviewCount: 6,
        rating: 5,
        text: "Mike did a great job. Enjoyed his company and getting to know him. Highly recommend his services."
    },
    {
        name: "Rachel Adams",
        localGuide: false,
        reviewCount: 6,
        rating: 5,
        text: "Mike has taken care of my property management business for years for rekeys, lockouts and even keys to my camper. Thanks again Mike."
    }
];

const GOOGLE_BADGE_SVG = `<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>`;

const getReviewInitial = (name) => {

    const trimmed = name.trim();

    if (!trimmed) return "?";

    const firstChar = trimmed.charAt(0);

    return /[A-Za-z0-9]/.test(firstChar) ? firstChar.toUpperCase() : "?";

};

const formatReviewMeta = (review) => {

    const countLabel = review.reviewCount === 1
        ? "1 Google Review"
        : `${review.reviewCount} Google Reviews`;

    if (review.localGuide) {

        return `Local Guide · ${countLabel}`;

    }

    return countLabel;

};

const escapeHtml = (value) => {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");

};

const buildReviewCardHtml = (review) => {

    const meta = formatReviewMeta(review);
    const stars = "★".repeat(review.rating || 5);

    return `
        <article class="google-review-card">
            <div class="grc-top">
                <div class="grc-profile">
                    <span class="grc-avatar" aria-hidden="true">${escapeHtml(getReviewInitial(review.name))}</span>
                    <div class="grc-author">
                        <cite class="grc-name">${escapeHtml(review.name)}</cite>
                        ${meta ? `<span class="grc-meta">${escapeHtml(meta)}</span>` : ""}
                    </div>
                </div>
                <span class="grc-google-badge" aria-label="Google Review">${GOOGLE_BADGE_SVG}</span>
            </div>
            <div class="grc-stars" aria-label="${review.rating || 5} out of 5 stars">${stars}</div>
            <div class="grc-body">
                <div class="grc-text-wrap">
                    <p class="grc-text">${escapeHtml(review.text)}</p>
                </div>
                <button type="button" class="grc-read-more" hidden>Read More</button>
            </div>
        </article>
    `;

};

const renderGoogleReviews = () => {

    const reviewTrack = document.querySelector(".review-track");
    const dotsContainer = document.querySelector(".review-carousel-dots");

    if (!reviewTrack || !dotsContainer) return [];

    const activeReviews = googleReviews.filter((review) => review.text && review.text.trim());

    reviewTrack.innerHTML = activeReviews.map(buildReviewCardHtml).join("");

    dotsContainer.innerHTML = "";

    return activeReviews;

};

const REVIEW_TEXT_LINES = 4;

const refreshReviewReadMoreCard = (card) => {

    const wrap = card.querySelector(".grc-text-wrap");
    const text = card.querySelector(".grc-text");
    const btn = card.querySelector(".grc-read-more");

    if (!wrap || !text || !btn) return;

    const getCollapsedHeight = () => {

        const lineHeight = parseFloat(window.getComputedStyle(text).lineHeight);

        return Math.ceil(lineHeight * REVIEW_TEXT_LINES);

    };

    if (!card.classList.contains("grc-expanded")) {

        wrap.style.maxHeight = `${getCollapsedHeight()}px`;

    }

    if (card.classList.contains("grc-expanded")) {

        wrap.style.maxHeight = `${text.scrollHeight}px`;

        return;

    }

    btn.hidden = text.scrollHeight <= wrap.clientHeight + 1;

};

const setupReviewReadMoreCard = (card) => {

    const wrap = card.querySelector(".grc-text-wrap");
    const text = card.querySelector(".grc-text");
    const btn = card.querySelector(".grc-read-more");

    if (!wrap || !text || !btn) return;

    const getCollapsedHeight = () => {

        const lineHeight = parseFloat(window.getComputedStyle(text).lineHeight);

        return Math.ceil(lineHeight * REVIEW_TEXT_LINES);

    };

    const setCollapsed = () => {

        card.classList.remove("grc-expanded");
        wrap.style.maxHeight = `${getCollapsedHeight()}px`;
        btn.textContent = "Read More";

    };

    setCollapsed();

    requestAnimationFrame(() => {

        refreshReviewReadMoreCard(card);

    });

    btn.addEventListener("click", () => {

        const isExpanded = card.classList.contains("grc-expanded");

        if (isExpanded) {

            setCollapsed();

        } else {

            card.classList.add("grc-expanded");
            wrap.style.maxHeight = `${text.scrollHeight}px`;
            btn.textContent = "Show Less";

        }

    });

};

const initReviewReadMore = () => {

    document.querySelectorAll(".google-review-card").forEach((card) => {

        if (card.dataset.readMoreInit === "true") {

            refreshReviewReadMoreCard(card);

            return;

        }

        card.dataset.readMoreInit = "true";
        setupReviewReadMoreCard(card);

    });

};

// ======================================
// GOOGLE REVIEWS CAROUSEL
// ======================================

const initReviewCarousel = () => {

    renderGoogleReviews();
    initReviewReadMore();

    const reviewTrack = document.querySelector(".review-track");
    const googleCards = document.querySelectorAll(".google-review-card");
    const dotsContainer = document.querySelector(".review-carousel-dots");
    const carouselPrev = document.querySelector(".carousel-prev");
    const carouselNext = document.querySelector(".carousel-next");

    if (!reviewTrack || !googleCards.length || !dotsContainer) return;

    let currentIndex = 0;
    let autoTimer = null;
    let carouselDots = [];
    const AUTO_MS = 5000;

    const getSlidesPerView = () => {

        if (window.innerWidth <= 640) return 1;
        if (window.innerWidth <= 992) return 2;
        return 3;

    };

    const getMaxIndex = () => {

        return Math.max(0, googleCards.length - getSlidesPerView());

    };

    const buildDots = () => {

        dotsContainer.innerHTML = "";

        const dotCount = getMaxIndex() + 1;

        carouselDots = [];

        for (let i = 0; i < dotCount; i += 1) {

            const dot = document.createElement("button");

            dot.type = "button";
            dot.className = "carousel-dot";
            dot.setAttribute("aria-label", `Reviews slide ${i + 1}`);
            dot.setAttribute("aria-selected", "false");

            dot.addEventListener("click", () => {

                goTo(i);
                resetAuto();

            });

            dotsContainer.appendChild(dot);
            carouselDots.push(dot);

        }

    };

    const updateDots = () => {

        carouselDots.forEach((dot, i) => {

            const isActive = i === currentIndex;

            dot.classList.toggle("active", isActive);
            dot.setAttribute("aria-selected", isActive ? "true" : "false");

        });

    };

    const updateCarousel = () => {

        if (currentIndex > getMaxIndex()) {

            currentIndex = getMaxIndex();

        }

        const card = reviewTrack.querySelector(".google-review-card");

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

    const handleResize = () => {

        initReviewReadMore();
        buildDots();
        updateCarousel();

    };

    if (carouselNext) carouselNext.addEventListener("click", () => { nextReview(); resetAuto(); });
    if (carouselPrev) carouselPrev.addEventListener("click", () => { prevReview(); resetAuto(); });

    buildDots();

    window.addEventListener("resize", handleResize);

    const reviewCarousel = document.querySelector(".review-carousel");

    if (reviewCarousel) {

        reviewCarousel.addEventListener("mouseenter", () => {

            if (autoTimer) clearInterval(autoTimer);

        });

        reviewCarousel.addEventListener("mouseleave", resetAuto);

    }

    updateCarousel();

    resetAuto();

};

initReviewCarousel();

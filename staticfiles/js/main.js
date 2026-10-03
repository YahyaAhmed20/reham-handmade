/* =========================================================
   DAKKAN — MAIN JS
   Clean version for the الذكان project
========================================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       AOS INIT
    ========================= */
    if (typeof AOS !== "undefined") {
        AOS.init({
            duration: 680,
            once: true,
            offset: 55,
        });
    }


    /* =========================
       NAVBAR SCROLL & ACTIVE LINK
    ========================= */
    const nav = document.getElementById("nav");
    const btt = document.getElementById("btt");

    window.addEventListener("scroll", function () {

        // Navbar scrolled
        if (nav) {
            nav.classList.toggle("scrolled", window.scrollY > 60);
        }

        // Back to top
        if (btt) {
            btt.classList.toggle("show", window.scrollY > 300);
        }

        // Active link based on section
        document.querySelectorAll("section[id]").forEach(function (sec) {
            var top = sec.offsetTop - 110,
                bot = top + sec.offsetHeight;

            if (window.scrollY >= top && window.scrollY < bot) {

                document.querySelectorAll(".nav-link").forEach(function (l) {
                    l.classList.remove("active");
                });

                var lnk = document.querySelector('.nav-link[href="#' + sec.id + '"]');
                if (lnk) lnk.classList.add("active");
            }
        });

    });


    /* =========================
       SMOOTH SCROLL + MOBILE NAV CLOSE
    ========================= */
    document.querySelectorAll('a[href^="#"]').forEach(function (a) {

        a.addEventListener("click", function (e) {

            var href = this.getAttribute("href");
            if (!href || href === "#") return;

            var t = document.querySelector(href);
            if (!t) return;

            e.preventDefault();

            // Close Bootstrap mobile navbar if open
            var navCollapse = document.getElementById("navmenu");

            if (navCollapse && navCollapse.classList.contains("show")) {

                if (typeof bootstrap !== "undefined") {
                    var bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
                    if (bsCollapse) {
                        bsCollapse.hide();
                    } else {
                        navCollapse.classList.remove("show");
                    }
                } else {
                    navCollapse.classList.remove("show");
                }
            }

            // Scroll after slight delay to let navbar close
            setTimeout(function () {
                window.scrollTo({
                    top: t.offsetTop - 78,
                    behavior: "smooth",
                });
            }, 50);

        });

    });


    /* =========================
       MAGNIFIC POPUP (safe)
    ========================= */
    if (typeof jQuery !== "undefined" && jQuery.fn.magnificPopup) {

        jQuery(".magnific_popup").magnificPopup({
            type: "iframe",
            mainClass: "mfp-fade",
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false,
        });

    }


    /* =========================
       SWIPER (safe)
    ========================= */
    if (typeof Swiper !== "undefined") {

        // Testimonials Swiper
        if (document.querySelector(".tesSwiper")) {

            new Swiper(".tesSwiper", {
                slidesPerView: 1,
                spaceBetween: 22,
                loop: true,
                autoplay: {
                    delay: 4000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
                breakpoints: {
                    640:  { slidesPerView: 2 },
                    1024: { slidesPerView: 3 },
                },
            });

        }

        // Generic Swiper (لو عايز تعمل سلايدر تاني)
        if (document.querySelector(".mySwiper")) {

            new Swiper(".mySwiper", {
                slidesPerView: 1,
                spaceBetween: 20,
                loop: true,
                pagination: {
                    el: ".swiper-pagination",
                    clickable: true,
                },
                breakpoints: {
                    768:  { slidesPerView: 2 },
                    1024: { slidesPerView: 3 },
                },
            });

        }

    }


    /* =========================
       ESC KEY — closes modals (safe)
    ========================= */
    document.addEventListener("keydown", function (e) {

        if (e.key === "Escape") {

            // Any modal with class .open
            document.querySelectorAll(".open").forEach(function (el) {
                el.classList.remove("open");
            });

            document.body.style.overflow = "";

        }

    });


    /* =========================
       BACK TO TOP BUTTON
    ========================= */
    if (btt) {

        btt.addEventListener("click", function (e) {

            e.preventDefault();

            window.scrollTo({
                top: 0,
                behavior: "smooth",
            });

        });

    }

});
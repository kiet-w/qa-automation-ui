/**
 * reporting/assets/js/views.js - Smooth scroll navigation, active spy, theme toggling, toasts, and shortcuts.
 */

// Smooth Scroll to Section on Single Page
window.scrollToSection = function (sectionId) {
    const el = document.getElementById(sectionId);
    if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    // Update active nav button
    document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
    const map = {
        "section-kpi": "nav-btn-kpi",
        "section-analytics": "nav-btn-analytics",
        "section-pipeline": "nav-btn-pipeline",
        "section-video": "nav-btn-video",
        "section-steps": "nav-btn-steps",
        "section-system": "nav-btn-system",
    };
    const targetBtnId = map[sectionId];
    if (targetBtnId) {
        const btn = document.getElementById(targetBtnId);
        if (btn) btn.classList.add("active");
    }
};

// Backward-compatible switchView
window.switchView = function (viewName) {
    if (viewName === "dashboard") {
        window.scrollToSection("section-kpi");
    } else if (viewName === "tests") {
        window.scrollToSection("section-video");
    }
};

// Accordion Controls (Multi-Test View)
window.toggleTestCard = function (idx) {
    const card = document.getElementById(`test-card-${idx}`);
    if (!card) return;
    const isCollapsed = card.classList.contains("collapsed");
    if (isCollapsed) {
        card.classList.remove("collapsed");
        const header = card.querySelector(".test-accordion-header");
        if (header) header.setAttribute("aria-expanded", "true");
    } else {
        card.classList.add("collapsed");
        const header = card.querySelector(".test-accordion-header");
        if (header) header.setAttribute("aria-expanded", "false");
    }
};
window.toggleAccordion = window.toggleTestCard;

window.expandAllTests = function () {
    document.querySelectorAll(".test-item-card").forEach(card => {
        card.classList.remove("collapsed");
        const header = card.querySelector(".test-accordion-header");
        if (header) header.setAttribute("aria-expanded", "true");
    });
};

window.collapseAllTests = function () {
    document.querySelectorAll(".test-item-card").forEach(card => {
        card.classList.add("collapsed");
        const header = card.querySelector(".test-accordion-header");
        if (header) header.setAttribute("aria-expanded", "false");
    });
};

// Status Filter (All / Passed / Failed)
window.filterTests = function (status) {
    document.querySelectorAll(".filter-btn").forEach(btn => {
        if (btn.getAttribute("data-filter") === status) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });

    document.querySelectorAll(".test-item-card").forEach(card => {
        const cardStatus = card.getAttribute("data-status") || "";
        if (status === "all" || cardStatus === status) {
            card.classList.remove("is-hidden");
        } else {
            card.classList.add("is-hidden");
        }
    });
};

// Theme Toggle (Light / Dark)
window.toggleTheme = function () {
    const isDark = document.body.getAttribute("data-theme") === "dark";
    const newTheme = isDark ? "light" : "dark";
    if (newTheme === "dark") {
        document.body.setAttribute("data-theme", "dark");
    } else {
        document.body.removeAttribute("data-theme");
    }
    localStorage.setItem("extent-theme", newTheme);
    updateThemeIcon(newTheme);
};

function updateThemeIcon(theme) {
    const iconContainer = document.getElementById("theme-icon-container");
    if (!iconContainer) return;
    if (theme === "dark") {
        // Sun icon for switching to light
        iconContainer.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
    } else {
        // Moon icon for switching to dark
        iconContainer.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
    }
}

// Toast notification
function showSeekToast(msg) {
    let toast = document.getElementById("seekToast");
    if (!toast) return;
    const textSpan = document.getElementById("seekToastText");
    if (textSpan) textSpan.textContent = msg;
    toast.classList.add("active");
    clearTimeout(window._toastTimeout);
    window._toastTimeout = setTimeout(() => {
        toast.classList.remove("active");
    }, 2200);
}

// Scroll Spy to highlight active navigation link
window.addEventListener("scroll", function () {
    const sections = ["section-kpi", "section-analytics", "section-pipeline", "section-video", "section-steps", "section-system"];
    const scrollPos = window.scrollY + 120;
    for (let i = sections.length - 1; i >= 0; i--) {
        const sec = document.getElementById(sections[i]);
        if (sec && sec.offsetTop <= scrollPos) {
            const map = {
                "section-kpi": "nav-btn-kpi",
                "section-analytics": "nav-btn-analytics",
                "section-pipeline": "nav-btn-pipeline",
                "section-video": "nav-btn-video",
                "section-steps": "nav-btn-steps",
                "section-system": "nav-btn-system",
            };
            document.querySelectorAll(".nav-btn").forEach(btn => btn.classList.remove("active"));
            const btn = document.getElementById(map[sections[i]]);
            if (btn) btn.classList.add("active");
            break;
        }
    }
}, { passive: true });

// Keyboard Shortcuts (ExtentReports standard)
document.addEventListener("keydown", function (e) {
    if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

    if (e.key === "d" || e.key === "D") {
        window.scrollToSection("section-kpi");
    } else if (e.key === "t" || e.key === "T") {
        window.scrollToSection("section-steps");
    } else if (e.key === "v" || e.key === "V") {
        window.scrollToSection("section-video");
    } else if (e.key === "l" || e.key === "L") {
        window.toggleTheme();
    } else if (e.key === "Escape") {
        if (typeof window.closeLightbox === "function") {
            window.closeLightbox();
        }
    }
});

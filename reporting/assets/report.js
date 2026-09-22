(function () {
"use strict";

/**
 * reporting/assets/js/i18n.js - Bilingual Translations (EN / VI).
 */
const translations = {
    en: {
        report_title: "ExtentReports",
        report_subtitle: "UI Automation Test Report",
        kpi_tests: "TESTS",
        kpi_steps: "STEPS",
        kpi_start_time: "START TIME",
        kpi_duration: "DURATION",
        lbl_passed: "passed",
        lbl_failed: "failed",
        lbl_skipped: "skipped",
        chart_status_title: "Tests & Steps Status",
        chart_duration_title: "Timeline & Step Durations",
        pipeline_title: "Step Execution Pipeline",
        pipeline_hint: "Click any step node to seek video to that step",
        sysinfo_title: "Environment & System Information",
        th_param: "Parameter",
        th_value: "Value",
        steps_table_title: "Step Execution Log & Evidence",
        th_status: "Status",
        th_timestamp: "Timestamp",
        th_details: "Step Details",
        th_evidence: "Evidence",
        video_title: "Execution Video Recording",
        tag_expected: "Expected:",
        tag_actual: "Actual:",
        tag_error: "Error:",
        btn_zoom: "Enlarge Fullscreen",
        click_to_zoom: "Click image to view in full resolution",
        lbl_screenshot_evidence: "Screenshot Evidence Deliverable",
        lbl_legend_pass: "Passed",
        lbl_legend_fail: "Failed",
        lbl_legend_skip: "Skipped",
        pass_rate: "PASS RATE",
        toast_seek: "Jumped to Step",
        test_suite_title: "Test Cases & Scenarios",
        filter_all: "All",
        filter_passed: "Passed",
        filter_failed: "Failed",
        btn_expand_all: "Expand All",
        btn_collapse_all: "Collapse All",
        no_video_rec: "No video recording available for this test case"
    },
    vi: {
        report_title: "ExtentReports",
        report_subtitle: "Báo Cáo Tự Động Hóa Giao Diện",
        kpi_tests: "BÀI TEST",
        kpi_steps: "CÁC BƯỚC",
        kpi_start_time: "THỜI GIAN BẮT ĐẦU",
        kpi_duration: "THỜI LƯỢNG",
        lbl_passed: "thành công",
        lbl_failed: "thất bại",
        lbl_skipped: "bỏ qua",
        chart_status_title: "Tỷ Lệ Trạng Thái Kiểm Thử",
        chart_duration_title: "Thời Lượng Từng Bước Thực Thi",
        pipeline_title: "Sơ Đồ Luồng Thực Thi Các Bước",
        pipeline_hint: "Nhấn vào từng node để tua video đến bước đó",
        sysinfo_title: "Thông Tin Môi Trường & Hệ Thống",
        th_param: "Tham Số",
        th_value: "Giá Trị",
        steps_table_title: "Nhật Ký Thực Thi Từng Bước & Bằng Chứng",
        th_status: "Trạng Thái",
        th_timestamp: "Thời Điểm",
        th_details: "Chi Tiết Bước",
        th_evidence: "Bằng Chứng",
        video_title: "Video Ghi Hình Quá Trình Chạy",
        tag_expected: "Kỳ vọng:",
        tag_actual: "Thực tế:",
        tag_error: "Lỗi:",
        btn_zoom: "Phóng to toàn màn hình",
        click_to_zoom: "Nhấn vào ảnh để xem kích thước đầy đủ",
        lbl_screenshot_evidence: "Ảnh Chụp Bằng Chứng Kết Quả",
        lbl_legend_pass: "Thành công",
        lbl_legend_fail: "Thất bại",
        lbl_legend_skip: "Bỏ qua",
        pass_rate: "TỶ LỆ ĐẠT",
        toast_seek: "Đã tua tới Bước",
        test_suite_title: "Danh Sách Kịch Bản Kiểm Thử",
        filter_all: "Tất Cả",
        filter_passed: "Thành Công",
        filter_failed: "Thất Bại",
        btn_expand_all: "Bung Tất Cả",
        btn_collapse_all: "Thu Gọn",
        no_video_rec: "Không có video ghi hình cho bài test này"
    }
};

let currentLang = localStorage.getItem("extent-lang") || "en";

window.toggleLanguage = function () {
    currentLang = currentLang === "en" ? "vi" : "en";
    localStorage.setItem("extent-lang", currentLang);
    applyLanguage(currentLang);
};

function applyLanguage(lang) {
    const dict = translations[lang] || translations.en;
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    const langBtn = document.getElementById("lang-btn");
    if (langBtn) {
        langBtn.textContent = lang.toUpperCase();
    }
}


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


/**
 * reporting/assets/js/video.js - Video seeking and 2-way playback synchronization.
 */

// Seek Video & Scroll
window.seekVideoAndScroll = function (startTime, targetId, testIdx, stepIdx) {
    // Automatically switch to tests view if currently on dashboard
    window.switchView("tests");

    // 1. Ensure target test card is expanded if currently collapsed
    const testCard = document.getElementById(`test-card-${testIdx}`);
    if (testCard && testCard.classList.contains("collapsed")) {
        testCard.classList.remove("collapsed");
        const header = testCard.querySelector(".test-accordion-header");
        if (header) header.setAttribute("aria-expanded", "true");
    }

    const videoPlayer = document.getElementById(`video-player-${testIdx}`);
    const videoSection = document.getElementById(`video-section-${testIdx}`);

    if (videoPlayer) {
        const targetOffset = Math.max(0, parseFloat(startTime) || 0);

        // Highlight table row
        document.querySelectorAll(".step-log-row").forEach(r => r.classList.remove("active-sync-row"));
        const targetRow = document.getElementById(`step-row-${testIdx}-${stepIdx}`);
        if (targetRow) {
            targetRow.classList.add("active-sync-row");
        }

        // Scroll to video first
        if (videoSection) {
            videoSection.scrollIntoView({ behavior: "smooth", block: "center" });
        } else if (testCard) {
            testCard.scrollIntoView({ behavior: "smooth", block: "start" });
        }

        // Seek after scroll begins
        setTimeout(() => {
            videoPlayer.currentTime = targetOffset;
            const playPromise = videoPlayer.play();
            if (playPromise !== undefined) {
                playPromise.catch(() => {});
            }
            const dict = (typeof translations !== "undefined" && translations[currentLang]) ? translations[currentLang] : {};
            const prefix = dict.toast_seek || "Jumped to Step";
            if (typeof showSeekToast === "function") {
                showSeekToast(`${prefix} ${stepIdx + 1}: ${targetOffset.toFixed(1)}s`);
            }
        }, 300);
    } else if (testCard) {
        // Fallback when no video is attached: scroll to step row or test card
        const targetRow = document.getElementById(`step-row-${testIdx}-${stepIdx}`);
        if (targetRow) {
            document.querySelectorAll(".step-log-row").forEach(r => r.classList.remove("active-sync-row"));
            targetRow.classList.add("active-sync-row");
            targetRow.scrollIntoView({ behavior: "smooth", block: "center" });
        } else {
            testCard.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }
};

// Synchronize while video is playing
window.syncVideoWithDiagram = function (testIdx, currentTime) {
    // 1. Sync pipeline nodes
    const nodes = document.querySelectorAll(`.pipeline-node[data-test-idx="${testIdx}"]`);
    nodes.forEach(node => {
        const start = parseFloat(node.getAttribute("data-start") || "0");
        const end = parseFloat(node.getAttribute("data-end") || "0");
        if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
            node.classList.add("active-sync-step");
        } else {
            node.classList.remove("active-sync-step");
        }
    });

    // 2. Sync bar chart
    const bars = document.querySelectorAll(`.bar-group[data-test-idx="${testIdx}"]`);
    bars.forEach(bar => {
        const start = parseFloat(bar.getAttribute("data-start") || "0");
        const end = parseFloat(bar.getAttribute("data-end") || "0");
        if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
            bar.classList.add("active-sync-bar");
        } else {
            bar.classList.remove("active-sync-bar");
        }
    });

    // 3. Sync Step Log table rows
    const rows = document.querySelectorAll(`.step-log-row[data-test-idx="${testIdx}"]`);
    rows.forEach(row => {
        const start = parseFloat(row.getAttribute("data-start") || "0");
        const end = parseFloat(row.getAttribute("data-end") || "0");
        if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
            row.classList.add("active-sync-row");
        } else {
            row.classList.remove("active-sync-row");
        }
    });
};


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


/**
 * reporting/assets/js/main.js - DOM initialization on page load.
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. Initialize Theme
    const savedTheme = localStorage.getItem("extent-theme") || "dark";
    if (savedTheme === "dark") {
        document.body.setAttribute("data-theme", "dark");
    } else {
        document.body.removeAttribute("data-theme");
    }
    if (typeof updateThemeIcon === "function") {
        updateThemeIcon(savedTheme);
    }

    // 2. Initialize Language
    if (typeof applyLanguage === "function" && typeof currentLang !== "undefined") {
        applyLanguage(currentLang);
    }
});

})();
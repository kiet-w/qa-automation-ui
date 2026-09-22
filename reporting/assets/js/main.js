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

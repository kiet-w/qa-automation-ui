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

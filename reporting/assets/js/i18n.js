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

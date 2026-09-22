        // Inline Dictionary for Instant Bilingual Switching (EN / VI)
        const translations = {
            en: {
                page_title: "UI Automation Execution Report",
                header_title: "UI Automation Execution Report",
                header_subtitle: "Playwright + Pytest Offline Test Intelligence",
                kpi_total: "Total Tests",
                kpi_passed: "Passed",
                kpi_failed: "Failed",
                kpi_duration: "Total Duration",
                kpi_rate: "Pass Rate",
                lbl_collected: "Collected tests",
                lbl_success_runs: "Successful runs",
                lbl_error_runs: "Requires attention",
                lbl_wall_time: "Execution wall time",
                lbl_reliability: "Quality rating",
                chart_donut_title: "Result Distribution",
                chart_bar_title: "Execution Duration Breakdown (Seconds)",
                pass_rate: "PASS RATE",
                lbl_legend_pass: "Passed",
                lbl_legend_fail: "Failed",
                lbl_legend_skip: "Skipped",
                badge_offline_svg: "Pure SVG",
                pipeline_title: "Interactive Step Execution Pipeline",
                pipeline_hint: "Click any node or bar to seek video to that step",
                video_title: "Execution Video Recording",
                video_badge: "WebM Playback (Offline)",
                steps_title: "Execution Steps & Evidence",
                lbl_steps_recorded: "steps recorded",
                screenshot_evidence: "Screenshot Evidence:",
                click_to_zoom: "Click image to view full resolution",
                expand_image: "Enlarge",
                step_error_label: "Step Failure:",
                traceback_title: "Failure Traceback",
                lbl_duration: "Duration:",
                env_browser: "Browser:",
                env_python: "Python:",
                env_platform: "Platform:",
                env_executed: "Executed At:",
                footer_signature: "Self-contained Playwright Test Report Generator",
                no_duration_data: "No duration data available.",
                no_steps: "No detailed steps recorded.",
                video_missing_file: "Video recording file exists on disk but could not be embedded."
            },
            vi: {
                page_title: "Báo Cáo Thực Thi Kiểm Thử Tự Động",
                header_title: "Báo Cáo Thực Thi Kiểm Thử Tự Động",
                header_subtitle: "Bảng Điều Khiển Kiểm Thử Playwright + Pytest Offline",
                kpi_total: "Tổng Số Test",
                kpi_passed: "Thành Công",
                kpi_failed: "Thất Bại",
                kpi_duration: "Tổng Thời Gian",
                kpi_rate: "Tỷ Lệ Đạt",
                lbl_collected: "Tổng số test case",
                lbl_success_runs: "Lượt chạy thành công",
                lbl_error_runs: "Cần kiểm tra lại",
                lbl_wall_time: "Thời gian thực thi",
                lbl_reliability: "Đánh giá chất lượng",
                chart_donut_title: "Phân Bố Kết Quả Kiểm Thử",
                chart_bar_title: "Biểu Đồ Thời Gian Thực Thi (Giây)",
                pass_rate: "TỶ LỆ ĐẠT",
                lbl_legend_pass: "Thành công",
                lbl_legend_fail: "Thất bại",
                lbl_legend_skip: "Bỏ qua",
                badge_offline_svg: "SVG Thuần",
                pipeline_title: "Sơ Đồ Luồng Thực Thi Các Bước",
                pipeline_hint: "Nhấn vào từng node hoặc cột để tua video đến bước đó",
                video_title: "Video Ghi Hình Quá Trình Chạy",
                video_badge: "WebM Playback (Nội Tuyến)",
                steps_title: "Chi Tiết Từng Bước & Bằng Chứng",
                lbl_steps_recorded: "bước đã ghi nhận",
                screenshot_evidence: "Ảnh Chụp Bằng Chứng:",
                click_to_zoom: "Nhấn vào ảnh để xem kích thước đầy đủ",
                expand_image: "Phóng to",
                step_error_label: "Lỗi Tại Bước Này:",
                traceback_title: "Nhật Ký Truy Vết Lỗi (Traceback)",
                lbl_duration: "Thời gian:",
                env_browser: "Trình duyệt:",
                env_python: "Python:",
                env_platform: "Hệ điều hành:",
                env_executed: "Thời điểm chạy:",
                footer_signature: "Hệ thống Báo Cáo Tự Động Playwright - 100% Tự Chứa",
                no_duration_data: "Không có dữ liệu thời gian.",
                no_steps: "Chưa ghi nhận bước kiểm thử nào.",
                video_missing_file: "Tìm thấy file video trên đĩa nhưng chưa nhúng được."
            }
        };

        let currentLang = 'en';

        function setLanguage(lang) {
            if (!translations[lang]) return;
            currentLang = lang;

            // Update all elements with data-i18n attribute
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (translations[lang][key]) {
                    el.textContent = translations[lang][key];
                }
            });

            // Toggle active state on buttons
            const btnEn = document.getElementById('btn-lang-en');
            const btnVi = document.getElementById('btn-lang-vi');
            if (btnEn && btnVi) {
                btnEn.classList.toggle('active', lang === 'en');
                btnVi.classList.toggle('active', lang === 'vi');
            }

            document.documentElement.lang = lang;
            try {
                localStorage.setItem('execution_report_lang', lang);
            } catch(e) {}
        }

        // Format seconds into mm:ss.s format
        function formatTime(seconds) {
            if (isNaN(seconds) || seconds < 0) return "00:00.0";
            const mins = Math.floor(seconds / 60);
            const secs = Math.floor(seconds % 60);
            const tenths = Math.floor((seconds % 1) * 10);
            return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}.${tenths}`;
        }

        let seekToastTimer = null;
        function showSeekToast(timeSec, stepIdx) {
            const toast = document.getElementById('seekToast');
            const textEl = document.getElementById('seekToastText');
            if (!toast || !textEl) return;

            const timeStr = formatTime(timeSec);
            const stepPrefix = currentLang === 'vi' ? 'Bước' : 'Step';
            const actionText = currentLang === 'vi' ? 'Đã tua video đến' : 'Video seeked to';
            textEl.textContent = `${actionText} ${timeStr} (${stepPrefix} ${stepIdx + 1})`;

            toast.classList.add('visible');
            if (seekToastTimer) clearTimeout(seekToastTimer);
            seekToastTimer = setTimeout(() => {
                toast.classList.remove('visible');
            }, 2400);
        }

        // Main Seek Video & Synchronize Diagram function
        function seekVideoAndScroll(timeSec, cardId, testIdx, stepIdx) {
            const video = document.getElementById(`video-player-${testIdx}`) || document.querySelector('.video-player');
            const container = document.getElementById(`video-container-${testIdx}`) || (video ? video.closest('.video-container') : null);

            if (!video || !container) return;

            // 1. Pause video immediately and seek to target time so user does not miss frames while moving
            video.pause();
            video.currentTime = Math.max(0, timeSec);

            // 2. Immediately synchronize active state with SVG diagram and step cards
            syncVideoWithDiagram(testIdx, timeSec);

            // 3. Highlight the corresponding step card below
            if (cardId) {
                const card = document.getElementById(cardId);
                if (card) {
                    card.classList.add('step-highlight');
                    setTimeout(() => {
                        card.classList.remove('step-highlight');
                    }, 3000);
                }
            }

            // 4. Show floating toast notification
            showSeekToast(timeSec, stepIdx);

            // 5. Add pulse highlight effect on video container
            container.classList.remove('video-seek-pulse');
            void container.offsetWidth; // force DOM reflow to restart animation
            container.classList.add('video-seek-pulse');

            // 6. Smooth scroll viewport to center the video
            const rect = container.getBoundingClientRect();
            const isAlreadyCentered = (
                rect.top >= 40 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) - 40
            );

            container.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // 7. ONLY play video after arriving at the video location
            let playbackStarted = false;
            const startPlayback = () => {
                if (playbackStarted) return;
                playbackStarted = true;
                video.play().catch(() => {});
            };

            if (isAlreadyCentered) {
                // Video is already in direct view, start after short 150ms visual pause
                setTimeout(startPlayback, 150);
            } else {
                // Wait for smooth scroll to finish before playing video
                let scrollTimer = null;
                const onScrollFinished = () => {
                    clearTimeout(scrollTimer);
                    scrollTimer = setTimeout(() => {
                        window.removeEventListener('scroll', onScrollFinished);
                        startPlayback();
                    }, 120);
                };

                window.addEventListener('scroll', onScrollFinished, { passive: true });

                // Fallback guarantee in case scroll completes quickly or native scrollend is missing
                setTimeout(() => {
                    window.removeEventListener('scroll', onScrollFinished);
                    startPlayback();
                }, 650);
            }
        }

        // Real-time synchronization while video is playing
        function syncVideoWithDiagram(testIdx, currentTime) {
            // Update timestamp readout
            const timeDisplay = document.getElementById(`video-time-display-${testIdx}`);
            if (timeDisplay) {
                timeDisplay.textContent = formatTime(currentTime);
            }

            // Sync pipeline SVG nodes
            const nodes = document.querySelectorAll(`.pipeline-node[data-test-idx="${testIdx}"]`);
            nodes.forEach(node => {
                const start = parseFloat(node.getAttribute('data-start') || '0');
                const end = parseFloat(node.getAttribute('data-end') || '0');
                if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
                    node.classList.add('active-sync-step');
                } else {
                    node.classList.remove('active-sync-step');
                }
            });

            // Sync Duration Bar Chart bars
            const bars = document.querySelectorAll(`.bar-group[data-test-idx="${testIdx}"]`);
            bars.forEach(bar => {
                const start = parseFloat(bar.getAttribute('data-start') || '0');
                const end = parseFloat(bar.getAttribute('data-end') || '0');
                if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
                    bar.classList.add('active-sync-bar');
                } else {
                    bar.classList.remove('active-sync-bar');
                }
            });

            // Sync step cards
            const cards = document.querySelectorAll(`.step-card[data-test-idx="${testIdx}"]`);
            cards.forEach(card => {
                const start = parseFloat(card.getAttribute('data-start') || '0');
                const end = parseFloat(card.getAttribute('data-end') || '0');
                if (currentTime >= start && (currentTime < end || (start === end && currentTime >= start))) {
                    card.classList.add('active-playing-card');
                } else {
                    card.classList.remove('active-playing-card');
                }
            });
        }

        // Smooth scroll to step card when pipeline node clicked
        function scrollToStep(targetId) {
            const card = document.getElementById(targetId);
            if (card) {
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                card.classList.add('step-highlight');
                setTimeout(() => {
                    card.classList.remove('step-highlight');
                }, 2200);
            }
        }

        // Lightbox Modal Controls
        function openLightbox(imgSrc, title) {
            const modal = document.getElementById('lightboxModal');
            const img = document.getElementById('lightboxImg');
            const titleEl = document.getElementById('lightboxTitle');

            if (modal && img) {
                img.src = imgSrc;
                if (titleEl) titleEl.textContent = title || 'Execution Evidence';
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        }

        function closeLightbox() {
            const modal = document.getElementById('lightboxModal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        }

        function handleLightboxClick(event) {
            if (event.target.id === 'lightboxModal') {
                closeLightbox();
            }
        }

        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeLightbox();
            }
        });

        // Initialize language from localStorage if available
        document.addEventListener('DOMContentLoaded', () => {
            try {
                const saved = localStorage.getItem('execution_report_lang');
                if (saved === 'vi' || saved === 'en') {
                    setLanguage(saved);
                }
            } catch(e) {}
        });

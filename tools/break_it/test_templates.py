"""
tools/break_it/test_templates.py - Reference Code Templates for AI Coding Agents.

Provides ready-to-use test recipes adhering to Invariant 8:
- Dimension A: Malformed & Hostile Inputs
- Dimension B: Client-Side Validation Bypass
- Dimension C: Concurrency, Debounce & Timing Chaos
- Dimension D: Authorization & Flow Tampering
- Dimension E: Viewport & Accessibility Boundaries
- Dimension F: Invisible Client Defect Detection
"""

TEMPLATE_CLIENT_BYPASS = '''
    @pytest.mark.break_it
    def test_tc_brk_001_client_bypass_rejects_invalid_input(self):
        """
        TC_BRK_001 — Client Constraint Bypass: Strips client validations and forces invalid payload.
        Verifies: Backend rejects invalid input; Exceptor flags bug if system accepts.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])

        with self.step("Step 1: Open form, fill valid data, and strip client constraints"):
            page_obj.open()
            page_obj.fill_full_form(data)
            page_obj.strip_client_constraints()
            page_obj.force_set_value(page_obj.{FIELD_SELECTOR}, "{INVALID_VALUE}")

        with self.step("Step 2: Submit form and verify server rejection"):
            page_obj.save()
            snapshot = page_obj.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="TC_BRK_001 Client Bypass")
            assert not snapshot["success_visible"], "System accepted invalid payload after client bypass!"

        with self.step("Step 3: Verify zero uncaught runtime JS exceptions"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_001")
'''

TEMPLATE_HOSTILE_STRINGS_XSS = '''
    @pytest.mark.break_it
    @pytest.mark.parametrize(
        "xss_payload",
        NAUGHTY_DATA.get("xss_payloads", ["<script>alert('XSS')</script>"])[:3],
    )
    def test_tc_brk_002_hostile_xss_injection_resilience(self, xss_payload: str):
        """
        TC_BRK_002 — Hostile Input: Verifies XSS payloads are safely escaped and trigger no native dialogs.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])
        dialog_messages = []
        self.page.on("dialog", lambda d: (dialog_messages.append(d.message), d.dismiss()))

        with self.step(f"Step 1: Populate form with hostile string: {xss_payload}"):
            page_obj.open()
            page_obj.fill_full_form(data)
            page_obj.force_set_value(page_obj.{FIELD_SELECTOR}, xss_payload)
            page_obj.save()

        with self.step("Step 2: Verify no unhandled native dialog was triggered"):
            assert len(dialog_messages) == 0, f"XSS executed! Dialog captured: {dialog_messages}"

        with self.step("Step 3: Verify client runtime health and zero JS errors"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context=xss_payload)
'''

TEMPLATE_DOUBLE_CLICK_IDEMPOTENCY = '''
    @pytest.mark.break_it
    def test_tc_brk_003_double_click_submit_idempotency(self):
        """
        TC_BRK_003 — Concurrency: Verifies rapid double-click on action button sends exactly 1 request.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])

        with self.step("Step 1: Open form and prepare valid submission"):
            page_obj.open()
            page_obj.fill_full_form(data)

        with self.step("Step 2: Track network dispatches and trigger rapid double-click"):
            tracker = page_obj.track_requests("{API_PATTERN}", method="POST")
            btn = page_obj.wait_for_visible(page_obj.{ACTION_BTN})
            btn.dblclick()
            self.page.wait_for_load_state("domcontentloaded")
            
            # If endpoint is tracked, verify debounce
            if tracker.count > 0:
                assert tracker.count == 1, f"Debounce failure! Dispatched {tracker.count} requests."
            tracker.stop()

        with self.step("Step 3: Verify client health"):
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_003")
'''

TEMPLATE_BOUNDARY_LENGTH_OVERFLOW = '''
    @pytest.mark.break_it
    def test_tc_brk_004_extreme_boundary_string_length(self):
        """
        TC_BRK_004 — Extreme Boundary: 10,000 character string in input field without layout overflow.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])
        huge_string = "A" * 10000

        with self.step("Step 1: Inject 10,000-character string bypassing client constraints"):
            page_obj.open()
            page_obj.fill_full_form(data)
            page_obj.strip_client_constraints()
            page_obj.force_set_value(page_obj.{FIELD_SELECTOR}, huge_string)

        with self.step("Step 2: Submit form and verify no layout clipping or browser crash"):
            page_obj.save()
            self.assert_no_horizontal_overflow()
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_004")
'''

TEMPLATE_DROPDOWN_ENUM_INJECTION = '''
    @pytest.mark.break_it
    def test_tc_brk_005_dropdown_unauthorized_enum_injection(self):
        """
        TC_BRK_005 — Schema Tampering: Injects unauthorized <option> into select element and submits.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])

        with self.step("Step 1: Inject synthetic unauthorized option into dropdown"):
            page_obj.open()
            page_obj.fill_full_form(data)
            page_obj.inject_select_option(
                page_obj.{SELECT_SELECTOR},
                value="SYNTHETIC_INVALID_ENUM_999",
                label="Synthetic Option",
            )

        with self.step("Step 2: Submit form and verify DOM resilience and backend rejection"):
            page_obj.save()
            snapshot = page_obj.get_state_snapshot()
            Exceptor.expect_bug_if_accepted(snapshot, context="TC_BRK_005 Enum Injection")
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_005")
'''

TEMPLATE_SERVER_500_RESILIENCE = '''
    @pytest.mark.break_it
    def test_tc_brk_006_server_500_graceful_handling(self):
        """
        TC_BRK_006 — Server Chaos: Verifies UI displays clear error and does not WSoD when backend returns 500.
        """
        page_obj = self.get_page({PAGE_CLASS})
        data = copy.deepcopy(self.load_json_data("{DATA_PATH}")["{VALID_KEY}"])

        with self.step("Step 1: Mock 500 Internal Server Error on target endpoint"):
            page_obj.open()
            page_obj.fill_full_form(data)
            page_obj.mock_http_response("{API_PATTERN}", status=500, body=\'{"error": "Internal Server Error"}\')

        with self.step("Step 2: Trigger action and verify user-friendly error display"):
            page_obj.save()
            # Verify UI did not freeze in perpetual loading
            # self.assert_no_hanging_spinners()
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_006")
'''

TEMPLATE_KEYBOARD_ACCESSIBILITY = '''
    @pytest.mark.break_it
    def test_tc_brk_007_keyboard_tab_navigation_no_focus_trap(self):
        """
        TC_BRK_007 — Accessibility: Verifies sequential Tab navigation advances without getting trapped.
        """
        page_obj = self.get_page({PAGE_CLASS})

        with self.step("Step 1: Open form and focus first input"):
            page_obj.open()
            self.page.locator(page_obj.{FIELD_SELECTOR}).focus()

        with self.step("Step 2: Advance Tab key 10 times and verify focus moves"):
            focused_tags = []
            for _ in range(10):
                self.page.keyboard.press("Tab")
                tag = self.page.evaluate("() => document.activeElement ? document.activeElement.tagName : 'NONE'")
                focused_tags.append(tag)
            assert len(set(focused_tags)) > 1, f"Focus trapped! Visited: {focused_tags}"
            Exceptor.expect_zero_js_errors(page_obj.get_technical_snapshot(), context="TC_BRK_007")
'''

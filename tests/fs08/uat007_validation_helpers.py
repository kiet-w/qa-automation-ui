"""Data-driven, observable UAT-007 field checks against the live profile form."""
import copy
import json
from pathlib import Path
import re

from playwright.sync_api import expect

from pages.fs08.parent_profile_page import ParentProfilePage
from pages.fs08.singpass_login_page import SingpassLoginPage

CASE_FILE = Path(__file__).resolve().parents[2] / "data/fs08/uat007_coverage_cases.json"
CASES = json.loads(CASE_FILE.read_text(encoding="utf-8"))
FIELD_SELECTORS = {
    "phoneNumber": ParentProfilePage.INPUT_PHONE,
    "email": ParentProfilePage.INPUT_EMAIL,
    "mailingBlock": ParentProfilePage.INPUT_BLOCK,
    "mailingStreet": ParentProfilePage.INPUT_STREET,
    "mailingUnit": ParentProfilePage.INPUT_UNIT,
    "mailingPostalCode": ParentProfilePage.INPUT_POSTAL,
    "mailingCountry": ParentProfilePage.INPUT_COUNTRY,
}


def cases_for(*fields):
    return [copy.deepcopy(case) for case in CASES if case["field"] in fields]


def input_value(case):
    value = case["input"]
    if isinstance(value, dict):
        return value["prefix"] * value["count"] + value["suffix"]
    return value


def check_case(test, fs08_data, case):
    profile = test.get_page(ParentProfilePage)
    login = test.get_page(SingpassLoginPage)
    login.login_with_persona(fs08_data["uat_007"]["persona"]["name"], base_url=fs08_data["base_url"])
    profile.open(base_url=fs08_data["base_url"])
    profile.click_update_details()
    selector = FIELD_SELECTORS[case["field"]]
    field = test.page.locator(selector)
    entered = input_value(case)

    with test.step(f'{case["id"]}: {case["title"]}', expected=case["source"]):
        assert field.count() == 1, f'{case["field"]} must exist exactly once in live edit form'
        baseline = field.input_value()
        field.fill(entered)
        field.blur()
        actual = field.input_value()
        kind = case["kind"]

        clipped = kind in {"invalid_or_clipped", "overflow"} and actual != entered
        if clipped:
            assert actual == entered[:case["limit"]], "Input was transformed beyond documented clipping"
            if kind == "invalid_or_clipped" and case["field"] == "phoneNumber":
                clipped = bool(re.fullmatch(r"[689][0-9]{7}", actual))

        if kind == "invalid" or (kind == "invalid_or_clipped" and not clipped) or (kind == "overflow" and not clipped):
            if not profile.is_save_disabled():
                profile.click_save_changes()
            assert not profile.is_confirm_dialog_open(timeout=500), "Invalid data opened confirmation"
            expect(field).to_have_attribute("aria-invalid", "true")
            if case.get("message"):
                expect(test.page.get_by_text(case["message"], exact=True).first).to_be_visible()
            assert not profile.is_raw_i18n_key(profile.get_field_error_text(case["field"])), "Raw i18n key leaked"
        else:
            expected = case.get("normalized", entered) if kind == "trim" else entered
            if kind == "trim":
                assert actual.strip() == expected, "Whitespace altered the meaningful field value"
            elif not clipped:
                assert actual == expected, f'Expected field value {expected!r}, got {actual!r}'
            if "length" in case:
                assert len(actual) == case["length"], "Fixture does not hit documented boundary"
            assert field.get_attribute("aria-invalid") != "true", "Valid data marked invalid"
            if kind != "optional" and actual != baseline:
                assert not profile.is_save_disabled(), "Valid change did not enable Save"
        test.highlight_actual_result(locator=selector, text=f'{case["id"]}: {kind}')
        test.step.set_actual(f'{case["field"]}: {actual!r}; aria-invalid={field.get_attribute("aria-invalid")}')

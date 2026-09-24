"""
pages/curricula_trainer_page.py - Page Object Model for Curricula Trainer Account Creation.
Encapsulates all locators, form inputs, dynamic state toggles, and user actions.
Inherits from BasePage.
"""
from pathlib import Path
from typing import Any, Dict, Optional, Union
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage

WORKSPACE_DIR = Path(__file__).resolve().parent.parent


class CurriculaTrainerPage(BasePage):
    """Page Object for Curricula Create Trainer Account form."""

    # Selectors - Personal Information
    PREFERRED_NAME = "#preferredName"
    GENDER_MALE = "input[name='gender'][value='Male']"
    GENDER_FEMALE = "input[name='gender'][value='Female']"
    ID_TYPE = "#idType"
    ID_NUMBER = "#idNumber"
    ID_DOCUMENT = "#idDocument"
    NATIONALITY = "#nationality"
    DOB = "#dob"
    RACE = "#race"
    BIRTH_COUNTRY = "#birthCountry"
    TAX_RESIDENT_YES = "input[name='taxResident'][value='Yes']"
    TAX_RESIDENT_NO = "input[name='taxResident'][value='No']"

    # Selectors - Contact Information
    PRIMARY_EMAIL = "#primaryEmail"
    PRIMARY_CODE = "#primaryCode"
    PRIMARY_PHONE = "#primaryPhone"
    SECONDARY_CODE = "#secondaryCode"
    SECONDARY_PHONE = "#secondaryPhone"

    # Selectors - Emergency Contact Information
    EMERGENCY_NAME = "#emergencyName"
    EMERGENCY_RELATIONSHIP = "#emergencyRelationship"
    EMERGENCY_CODE = "#emergencyCode"
    EMERGENCY_PHONE = "#emergencyPhone"

    # Selectors - Residential Address
    RESIDENTIAL_TYPE_SG = "input[name='residentialType'][value='Singapore']"
    RESIDENTIAL_TYPE_NON_SG = "input[name='residentialType'][value='Non-Singapore']"
    COUNTRY_REGION = "#countryRegion"
    POSTAL_CODE = "#postalCode"
    POSTAL_REQ = "#postalReq"

    SG_BLOCK_FIELD = "#sgBlockField"
    BLOCK_NUMBER = "#blockNumber"
    SG_BUILDING_FIELD = "#sgBuildingField"
    BUILDING_NAME = "#buildingName"
    SG_STREET_FIELD = "#sgStreetField"
    STREET_NAME = "#streetName"
    SG_FLOOR_UNIT_FIELD = "#sgFloorUnitField"
    FLOOR_NUMBER = "#floorNumber"
    UNIT_NUMBER = "#unitNumber"
    FLOOR_NOT_APPLICABLE = "#floorNotApplicable"

    NON_SG_ADDRESS1 = "#nonSgAddress1"
    ADDRESS_1 = "#address1"
    NON_SG_ADDRESS2 = "#nonSgAddress2"
    ADDRESS_2 = "#address2"
    NON_SG_CITY = "#nonSgCity"
    CITY = "#city"
    NON_SG_STATE = "#nonSgState"
    STATE_PROVINCE = "#stateProvince"

    # Selectors - Actions & Notifications
    SAVE_BTN = "#saveBtn"
    CANCEL_BTN = "#cancelBtn"
    SUCCESS_BOX = "#successBox"

    def __init__(self, page: Page):
        super().__init__(page)
        self.file_url = (WORKSPACE_DIR / "curricula_trainer_account.html").as_uri()

    def open(self):
        """Navigate to the local Curricula Create Trainer Account HTML file."""
        return self.navigate(self.file_url)

    def type_field(self, selector_or_locator: Union[str, Locator], text: str, delay: int = 20):
        """Scroll element smoothly into view, focus, and type text sequentially like a real human user."""
        loc = self.wait_for_visible(selector_or_locator)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(40)
        loc.click()
        loc.fill("")
        loc.press_sequentially(str(text), delay=delay)
        self.page.wait_for_timeout(60)

    # --- Personal Information Actions ---
    def set_preferred_name(self, name: str):
        self.type_field(self.PREFERRED_NAME, name)

    def select_gender(self, gender: str):
        radio_sel = self.GENDER_MALE if gender.lower() == "male" else self.GENDER_FEMALE
        loc = self.wait_for_visible(radio_sel)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.click()
        self.page.wait_for_timeout(100)

    def select_id_type(self, id_type: str):
        loc = self.wait_for_visible(self.ID_TYPE)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.select_option(id_type)
        self.page.wait_for_timeout(100)

    def set_id_number(self, id_number: str):
        self.type_field(self.ID_NUMBER, id_number)

    def upload_document(self, file_path: Union[str, Path]):
        resolved_path = Path(file_path)
        if not resolved_path.is_absolute():
            resolved_path = WORKSPACE_DIR / resolved_path
        loc = self.wait_for_visible(self.ID_DOCUMENT)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.set_input_files(str(resolved_path))
        self.page.wait_for_timeout(150)

    def select_nationality(self, nationality: str):
        loc = self.wait_for_visible(self.NATIONALITY)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.select_option(nationality)
        self.page.wait_for_timeout(100)

    def set_dob(self, dob_str: str):
        loc = self.wait_for_visible(self.DOB)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.fill(dob_str)
        self.page.wait_for_timeout(100)

    def select_race(self, race: str):
        loc = self.wait_for_visible(self.RACE)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.select_option(race)
        self.page.wait_for_timeout(100)

    def select_birth_country(self, country: str):
        loc = self.wait_for_visible(self.BIRTH_COUNTRY)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.select_option(country)
        self.page.wait_for_timeout(100)

    def select_tax_resident(self, is_resident: bool):
        radio_sel = self.TAX_RESIDENT_YES if (is_resident or str(is_resident).lower() in ("yes", "true", "1")) else self.TAX_RESIDENT_NO
        loc = self.wait_for_visible(radio_sel)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.click()
        self.page.wait_for_timeout(100)

    # --- Contact Information Actions ---
    def set_primary_email(self, email: str):
        self.type_field(self.PRIMARY_EMAIL, email)

    def set_primary_phone(self, code: str, phone: str):
        code_sel = self.wait_for_visible(self.PRIMARY_CODE)
        code_sel.scroll_into_view_if_needed()
        code_sel.select_option(code)
        self.type_field(self.PRIMARY_PHONE, phone)

    def set_secondary_phone(self, code: str, phone: str):
        code_sel = self.wait_for_visible(self.SECONDARY_CODE)
        code_sel.scroll_into_view_if_needed()
        code_sel.select_option(code)
        self.type_field(self.SECONDARY_PHONE, phone)

    # --- Emergency Contact Information Actions ---
    def set_emergency_contact(self, name: str, relationship: str, code: str, phone: str):
        self.type_field(self.EMERGENCY_NAME, name)
        rel_sel = self.wait_for_visible(self.EMERGENCY_RELATIONSHIP)
        rel_sel.scroll_into_view_if_needed()
        rel_sel.select_option(relationship)
        code_sel = self.wait_for_visible(self.EMERGENCY_CODE)
        code_sel.scroll_into_view_if_needed()
        code_sel.select_option(code)
        self.type_field(self.EMERGENCY_PHONE, phone)

    # --- Residential Address Actions ---
    def set_residential_type(self, res_type: str):
        """Toggle between Singapore and Non-Singapore residential types."""
        radio_sel = self.RESIDENTIAL_TYPE_SG if res_type.lower() in ("singapore", "sg") else self.RESIDENTIAL_TYPE_NON_SG
        loc = self.wait_for_visible(radio_sel)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.click()
        self.page.wait_for_timeout(150)

    def select_country_region(self, country: str):
        loc = self.wait_for_visible(self.COUNTRY_REGION)
        loc.scroll_into_view_if_needed()
        self.page.wait_for_timeout(50)
        loc.select_option(country)
        self.page.wait_for_timeout(100)

    def set_postal_code(self, postal_code: str, trigger_blur: bool = True):
        self.type_field(self.POSTAL_CODE, postal_code)
        if trigger_blur:
            self.page.locator(self.POSTAL_CODE).dispatch_event("blur")
            self.page.wait_for_timeout(200)

    def set_singapore_address(
        self,
        postal_code: str,
        block: str,
        street: str,
        floor: Optional[str] = None,
        unit: Optional[str] = None,
        building: Optional[str] = None,
        floor_na: bool = False,
    ):
        self.set_postal_code(postal_code)
        current_block = self.get_field_value(self.BLOCK_NUMBER)
        if not current_block or current_block != block:
            self.type_field(self.BLOCK_NUMBER, block)
        current_street = self.get_field_value(self.STREET_NAME)
        if not current_street or current_street != street:
            self.type_field(self.STREET_NAME, street)
        if building:
            self.type_field(self.BUILDING_NAME, building)
        if floor_na:
            self.set_floor_not_applicable(True)
        else:
            if floor:
                self.type_field(self.FLOOR_NUMBER, floor)
            if unit:
                self.type_field(self.UNIT_NUMBER, unit)

    def set_floor_not_applicable(self, checked: bool = True):
        box = self.wait_for_visible(self.FLOOR_NOT_APPLICABLE)
        box.scroll_into_view_if_needed()
        is_checked = box.is_checked()
        if is_checked != checked:
            self.page.wait_for_timeout(50)
            box.click()
            self.page.wait_for_timeout(100)

    def set_non_singapore_address(
        self,
        country: str,
        address1: str,
        city: str,
        address2: Optional[str] = None,
        state_province: Optional[str] = None,
        postal_code: Optional[str] = None,
    ):
        self.set_residential_type("Non-Singapore")
        self.select_country_region(country)
        self.type_field(self.ADDRESS_1, address1)
        self.type_field(self.CITY, city)
        if address2:
            self.type_field(self.ADDRESS_2, address2)
        if state_province:
            self.type_field(self.STATE_PROVINCE, state_province)
        if postal_code:
            self.type_field(self.POSTAL_CODE, postal_code)

    def fill_full_form(self, data: Dict[str, Any]):
        """Fill all fields based on a test data dictionary with realistic user pacing."""
        # Personal
        if "preferred_name" in data:
            self.set_preferred_name(data["preferred_name"])
        if "gender" in data:
            self.select_gender(data["gender"])
        if "id_type" in data:
            self.select_id_type(data["id_type"])
        if "id_number" in data:
            self.set_id_number(data["id_number"])
        if "id_document" in data and data["id_document"]:
            self.upload_document(data["id_document"])
        if "nationality" in data:
            self.select_nationality(data["nationality"])
        if "dob" in data:
            self.set_dob(data["dob"])
        if "race" in data:
            self.select_race(data["race"])
        if "birth_country" in data:
            self.select_birth_country(data["birth_country"])
        if "tax_resident" in data:
            self.select_tax_resident(data["tax_resident"])

        # Contact
        if "primary_email" in data:
            self.set_primary_email(data["primary_email"])
        if "primary_phone" in data:
            self.set_primary_phone(data.get("primary_code", "+65"), data["primary_phone"])
        if "secondary_phone" in data and data["secondary_phone"]:
            self.set_secondary_phone(data.get("secondary_code", "+65"), data["secondary_phone"])

        # Emergency
        if "emergency_name" in data:
            self.set_emergency_contact(
                data["emergency_name"],
                data.get("emergency_relationship", "Father"),
                data.get("emergency_code", "+65"),
                data.get("emergency_phone", "98765432"),
            )

        # Residential
        res_type = data.get("residential_type", "Singapore")
        self.set_residential_type(res_type)
        if res_type.lower() in ("singapore", "sg"):
            if "postal_code" in data:
                self.set_postal_code(data["postal_code"])
            if "block_number" in data:
                self.type_field(self.BLOCK_NUMBER, data["block_number"])
            if "street_name" in data:
                self.type_field(self.STREET_NAME, data["street_name"])
            if "building_name" in data and data["building_name"]:
                self.type_field(self.BUILDING_NAME, data["building_name"])
            if data.get("floor_not_applicable"):
                self.set_floor_not_applicable(True)
            else:
                if "floor_number" in data:
                    self.type_field(self.FLOOR_NUMBER, data["floor_number"])
                if "unit_number" in data:
                    self.type_field(self.UNIT_NUMBER, data["unit_number"])
        else:
            if "country_region" in data:
                self.select_country_region(data["country_region"])
            if "address1" in data:
                self.type_field(self.ADDRESS_1, data["address1"])
            if "city" in data:
                self.type_field(self.CITY, data["city"])
            if "address2" in data and data["address2"]:
                self.type_field(self.ADDRESS_2, data["address2"])
            if "state_province" in data and data["state_province"]:
                self.type_field(self.STATE_PROVINCE, data["state_province"])

    # --- Actions & Submissions ---
    def save(self):
        """Scroll smoothly to Save button, highlight/focus, click, and wait for form reaction."""
        save_btn = self.wait_for_visible(self.SAVE_BTN)
        save_btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(350)
        save_btn.click()
        # Wait for form reaction (success notification or validation error highlights)
        self.page.wait_for_timeout(800)

    def cancel(self):
        """Click the Cancel button."""
        cancel_btn = self.wait_for_visible(self.CANCEL_BTN)
        cancel_btn.scroll_into_view_if_needed()
        self.page.wait_for_timeout(250)
        cancel_btn.click()
        self.page.wait_for_timeout(400)

    # --- Inspection & Assertions Helpers ---
    def is_error_visible(self, key: str) -> bool:
        """Check if an error element with data-for='key' is visible."""
        loc = self.page.locator(f".error[data-for='{key}']")
        if loc.count() == 0:
            return False
        return loc.is_visible()

    def get_error_text(self, key: str) -> str:
        """Get the error message text for a field key."""
        loc = self.page.locator(f".error[data-for='{key}']")
        return loc.inner_text().strip() if loc.is_visible() else ""

    def is_input_invalid_styled(self, input_id: str) -> bool:
        """Check if input element has .invalid CSS class."""
        loc = self.page.locator(f"#{input_id}")
        classes = loc.get_attribute("class") or ""
        return "invalid" in classes.split()

    def is_success_visible(self) -> bool:
        """Check if the success message box is visible."""
        return self.page.locator(self.SUCCESS_BOX).is_visible()

    def get_success_text(self) -> str:
        """Get the success message text."""
        return self.page.locator(self.SUCCESS_BOX).inner_text().strip()

    def get_field_value(self, selector: str) -> str:
        """Retrieve current value of an input or select element."""
        return self.page.locator(selector).input_value()

    def is_element_enabled(self, selector: str) -> bool:
        """Check if an element is enabled."""
        return self.page.locator(selector).is_enabled()

    def scroll_to_error(self, key: str, highlight: bool = True, pause_ms: int = 1500) -> Locator:
        """
        Scroll smoothly to the specific field / error message, highlight it with a glowing red halo,
        and pause so that the viewer can clearly observe the error in real-time and in video recording.
        """
        err_loc = self.page.locator(f".error[data-for='{key}']")
        input_loc = self.page.locator(f"#{key}")

        scroll_target = err_loc if err_loc.count() > 0 and err_loc.is_visible() else input_loc
        if scroll_target.count() == 0:
            scroll_target = input_loc

        if scroll_target.count() > 0:
            scroll_target.scroll_into_view_if_needed()
            self.page.wait_for_timeout(200)

        # Apply glowing red highlight animation to both the input and the error message
        if highlight:
            self.page.evaluate(
                """([k]) => {
                    const input = document.getElementById(k);
                    const error = document.querySelector(`.error[data-for="${k}"]`);
                    if (input) {
                        input.style.outline = '3px solid #e53935';
                        input.style.boxShadow = '0 0 16px rgba(229, 57, 53, 0.7)';
                        input.style.transition = 'all 0.3s ease';
                    }
                    if (error) {
                        error.style.fontWeight = 'bold';
                        error.style.fontSize = '14px';
                        error.style.background = '#ffebee';
                        error.style.padding = '4px 8px';
                        error.style.borderRadius = '4px';
                        error.style.display = 'inline-block';
                        error.style.marginTop = '4px';
                    }
                }""",
                [key]
            )

        if pause_ms > 0:
            self.page.wait_for_timeout(pause_ms)

        return err_loc

    def scroll_to_first_error(self, highlight: bool = True, pause_ms: int = 1500) -> Optional[str]:
        """
        Find the first visible error on the form, scroll to it, highlight it, and pause.
        Returns the data-for key of the error.
        """
        visible_errors = self.page.locator(".error:visible")
        if visible_errors.count() > 0:
            first_err = visible_errors.first
            first_err.scroll_into_view_if_needed()
            key = first_err.get_attribute("data-for")
            if key:
                self.scroll_to_error(key, highlight=highlight, pause_ms=pause_ms)
                return key
            else:
                self.page.wait_for_timeout(pause_ms)
        return None

    def take_screenshot(self, filepath: Union[str, Path], full_page: bool = True) -> str:
        """Capture screenshot with settling pause to ensure all visual elements are rendered."""
        self.page.wait_for_timeout(500)
        return super().take_screenshot(filepath, full_page=full_page)

    def get_state_snapshot(self) -> Dict[str, Any]:
        """
        Collect current UI state snapshot for Exceptor evaluation:
        {
            "success_visible": bool,
            "visible_errors": {"field_id": "error message text", ...}
        }
        """
        visible_errors: Dict[str, str] = {}
        error_locators = self.page.locator(".error:visible")
        count = error_locators.count()
        for i in range(count):
            loc = error_locators.nth(i)
            key = loc.get_attribute("data-for") or f"unknown_{i}"
            text = loc.inner_text().strip()
            visible_errors[key] = text

        return {
            "success_visible": self.is_success_visible(),
            "visible_errors": visible_errors,
        }

"""
tests/fs03/fs03-school-directory/school_seed.py - UI seed factory for isolated schools.
Creates a school through the verified create form so lifecycle tests never mutate shared seed rows
(Rule 03 anti-noise: every test owns its data). Actions only; assertions stay in test functions.
"""
import re
from typing import Dict

from playwright.sync_api import expect

from pages.fs03.school_create_page import SchoolCreatePage
from directory_helpers import unique_code, unique_name


def create_school_via_ui(
    create_page: SchoolCreatePage,
    data: Dict,
    label: str = "seed",
    with_user: bool = False,
) -> Dict[str, str]:
    """Fill and submit the create form, wait for redirect, and return the created school identity."""
    code = unique_code(data)
    name = unique_name(data, label)

    create_page.open(base_url=data["base_url"])
    expect(create_page.page).to_have_url(re.compile(r".*/school-management/new$"))

    create_page.fill_moe_school_code(code)
    create_page.fill_school_name(name)
    create_page.select_school_type(data["school_type_label"])
    create_page.select_first_academic_level()
    if with_user:
        create_page.select_first_school_user()

    create_page.submit_form()
    expect(create_page.page).to_have_url(re.compile(r".*/school-management$"), timeout=15000)
    return {"code": code, "name": name}

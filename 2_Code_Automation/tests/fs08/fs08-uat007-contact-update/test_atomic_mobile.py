"""UAT-007 mobile matrix: TC-UAT007-10..29, R8-AC12 and MSG-0001/0805."""
import pytest

from tests.base_test import BaseTest


@pytest.mark.p0
@pytest.mark.atomic
class TestAtomicMobile(BaseTest):
    """One automation function per sourced mobile testcase."""

    def test_tc_uat007_10_mobile_required_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-10")

    def test_tc_uat007_11_mobile_whitespace_only(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-11")

    def test_tc_uat007_12_mobile_bva_seven_digits(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-12")

    def test_tc_uat007_13_mobile_prefix_nine(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-13")

    def test_tc_uat007_14_mobile_prefix_eight(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-14")

    def test_tc_uat007_15_mobile_prefix_six(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-15")

    def test_tc_uat007_16_mobile_bva_nine_digits(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-16")

    def test_tc_uat007_17_mobile_prefix_one(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-17")

    def test_tc_uat007_18_mobile_prefix_two(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-18")

    def test_tc_uat007_19_mobile_prefix_three(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-19")

    def test_tc_uat007_20_mobile_prefix_four(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-20")

    def test_tc_uat007_21_mobile_prefix_five(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-21")

    def test_tc_uat007_22_mobile_prefix_seven(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-22")

    def test_tc_uat007_23_mobile_alphabetic(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-23")

    def test_tc_uat007_24_mobile_hyphen(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-24")

    def test_tc_uat007_25_mobile_country_code(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-25")

    def test_tc_uat007_26_mobile_negative_sign(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-26")

    def test_tc_uat007_27_mobile_trim(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-27")

    def test_tc_uat007_28_mobile_xss_inert(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-28")

    def test_tc_uat007_29_mobile_sqli_rejected(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-29")

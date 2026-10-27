"""UAT-007 email matrix: TC-UAT007-30..46, R8-AC13 and MSG-0001/0806."""
import pytest

from tests.base_test import BaseTest


@pytest.mark.p0
@pytest.mark.atomic
class TestAtomicEmail(BaseTest):
    """One automation function per sourced email testcase."""

    def test_tc_uat007_30_email_required_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-30")

    def test_tc_uat007_31_email_whitespace_only(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-31")

    def test_tc_uat007_32_email_trim(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-32")

    def test_tc_uat007_33_email_basic_valid(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-33")

    def test_tc_uat007_34_email_plus_subdomain(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-34")

    def test_tc_uat007_35_email_bva_149(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-35")

    def test_tc_uat007_36_email_bva_150(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-36")

    def test_tc_uat007_37_email_bva_151(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-37")

    def test_tc_uat007_38_email_missing_at(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-38")

    def test_tc_uat007_39_email_missing_domain(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-39")

    def test_tc_uat007_40_email_missing_username(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-40")

    def test_tc_uat007_41_email_missing_tld(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-41")

    def test_tc_uat007_42_email_double_at(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-42")

    def test_tc_uat007_43_email_double_dot(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-43")

    def test_tc_uat007_44_email_internal_space(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-44")

    def test_tc_uat007_45_email_xss_inert(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-45")

    def test_tc_uat007_46_email_sqli_rejected(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-46")

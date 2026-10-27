"""UAT-007 mailing matrix: TC-UAT007-47..73 and R8-AC15."""
import pytest

from tests.base_test import BaseTest


@pytest.mark.p0
@pytest.mark.atomic
class TestAtomicMailing(BaseTest):
    """One automation function per sourced mailing-address testcase."""

    def test_tc_uat007_47_street_required_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-47")

    def test_tc_uat007_48_street_whitespace(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-48")

    def test_tc_uat007_49_street_trim(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-49")

    def test_tc_uat007_50_street_bva_99(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-50")

    def test_tc_uat007_51_street_bva_100(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-51")

    def test_tc_uat007_52_street_bva_101(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-52")

    def test_tc_uat007_53_street_punctuation(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-53")

    def test_tc_uat007_54_street_xss_inert(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-54")

    def test_tc_uat007_55_postal_required_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-55")

    def test_tc_uat007_56_postal_whitespace(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-56")

    def test_tc_uat007_57_postal_bva_five(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-57")

    def test_tc_uat007_58_postal_bva_six(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-58")

    def test_tc_uat007_59_postal_leading_zero(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-59")

    def test_tc_uat007_60_postal_bva_seven(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-60")

    def test_tc_uat007_61_postal_alpha(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-61")

    def test_tc_uat007_62_country_required_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-62")

    def test_tc_uat007_63_country_whitespace(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-63")

    def test_tc_uat007_64_country_trim(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-64")

    def test_tc_uat007_65_country_bva_100(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-65")

    def test_tc_uat007_66_country_bva_101(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-66")

    def test_tc_uat007_67_block_optional_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-67")

    def test_tc_uat007_68_block_bva_20(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-68")

    def test_tc_uat007_69_block_bva_21(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-69")

    def test_tc_uat007_70_unit_optional_empty(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-70")

    def test_tc_uat007_71_unit_singapore_format(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-71")

    def test_tc_uat007_72_unit_bva_20(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-72")

    def test_tc_uat007_73_unit_bva_21(self, fs08_data, uat007_case_runner):
        uat007_case_runner(self, fs08_data, "TC-UAT007-73")

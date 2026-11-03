#!/usr/bin/env python3
"""
=============================================================================
Batch Convert All 28 Individual Modules to Option A (14 Columns)
=============================================================================
"""

import os
import sys
from pathlib import Path
from option_a_converter import convert_single_sheet_to_option_a

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SUBMISSION_DIR = REPO_ROOT / "automation-uat/submission_for_instructor"
TESTING_DIR = SUBMISSION_DIR / "automation-testing"
INDIVIDUAL_DIR = TESTING_DIR / "02_Individual_Modules"

CORE_DIR = INDIVIDUAL_DIR / "00_Core_and_Executive"
ADMIN_DIR = INDIVIDUAL_DIR / "01_Admin_Portal_5173"
PARENT_DIR = INDIVIDUAL_DIR / "02_Parent_Citizen_Portal_5174"
ADVANCED_DIR = INDIVIDUAL_DIR / "03_Advanced_Quality_Suite"

TARGET_FILES = [
    # 00_Core_and_Executive (Skip 00_Core_01 summary which is a dashboard table)
    (CORE_DIR / "00_Core_02_E2E_Happy_Path_Automation_Flow.xlsx", "E2E Happy Path Flow"),
    (CORE_DIR / "00_Core_03_GovTech_EduSave_UAT_Test_Plan.xlsx", "GovTech UAT Test Plan"),
    (CORE_DIR / "00_Core_04_Automation_Unit_and_Architecture_Invariants.xlsx", "Automation Unit & Architecture Invariants"),

    # 01_Admin_Portal_5173
    (ADMIN_DIR / "01_Admin_01_Login_and_SSO.xlsx", "Admin Login & Microsoft SSO"),
    (ADMIN_DIR / "01_Admin_02_Dashboard_Shell.xlsx", "Admin Dashboard Shell & Navigation"),
    (ADMIN_DIR / "01_Admin_03_School_Management.xlsx", "School Management Directory"),
    (ADMIN_DIR / "01_Admin_03_School_Create_Spec_Matrix.xlsx", "School Create Spec Matrix"),
    (ADMIN_DIR / "01_Admin_04_School_User_Management.xlsx", "School User Management"),
    (ADMIN_DIR / "01_Admin_04_School_User_Spec_Matrix.xlsx", "School User Spec Matrix"),
    (ADMIN_DIR / "01_Admin_05_Academic_Years_and_Levels.xlsx", "Academic Years & Levels"),
    (ADMIN_DIR / "01_Admin_06_Class_Management.xlsx", "Class Management"),
    (ADMIN_DIR / "01_Admin_07_Student_Management.xlsx", "Student Management & Enrollment"),
    (ADMIN_DIR / "01_Admin_08_School_Configuration.xlsx", "School Configuration"),
    (ADMIN_DIR / "01_Admin_09_Fee_Batches_and_Fee_Management.xlsx", "Fee Batches & Fee Management"),
    (ADMIN_DIR / "01_Admin_10_Support_Console_and_Audit.xlsx", "Support Console & Impersonation Audit"),

    # 02_Parent_Citizen_Portal_5174
    (PARENT_DIR / "02_Parent_01_Login_and_Mockpass.xlsx", "Parent Singpass & Mockpass Login"),
    (PARENT_DIR / "02_Parent_02_Citizen_Dashboard.xlsx", "Citizen Dashboard & Wallets"),
    (PARENT_DIR / "02_Parent_03_Profile_and_Contact.xlsx", "Parent Profile & Contact Update"),
    (PARENT_DIR / "02_Parent_04_FAS_Application_Wizard.xlsx", "FAS Application Wizard"),
    (PARENT_DIR / "02_Parent_05_AI_Assistant_and_Guided_Tour.xlsx", "AI Assistant & Guided Tour"),
    (PARENT_DIR / "02_Parent_06_Payment_Checkout_Simulator.xlsx", "Payment Checkout Simulator"),
    (PARENT_DIR / "02_Parent_07_Child_Authentication_and_IDOR.xlsx", "Child Authentication & IDOR"),
    (PARENT_DIR / "02_Parent_08_FSD_104_Specs_Compliance_Audit.xlsx", "FSD 104 Specs Compliance Audit"),

    # 03_Advanced_Quality_Suite
    (ADVANCED_DIR / "03_Advanced_01_8_Forms_Destructive_Testing_Suite.xlsx", "8 Forms Destructive Testing Suite"),
    (ADVANCED_DIR / "03_Advanced_02_Security_and_Performance_Benchmark.xlsx", "Security & Performance Benchmark"),
    (ADVANCED_DIR / "03_Advanced_03_Date_Testing_and_Temporal_Audit.xlsx", "Date Testing & Temporal Audit"),
    (ADVANCED_DIR / "03_Advanced_04_Comprehensive_Defect_UI_Dossier.xlsx", "Comprehensive Defect UI Dossier"),
]

def batch_convert():
    print(f"[*] Starting batch conversion of {len(TARGET_FILES)} modules to Option A...")
    success_count = 0
    for file_path, title in TARGET_FILES:
        try:
            ok = convert_single_sheet_to_option_a(file_path, file_path, title)
            if ok:
                success_count += 1
        except Exception as e:
            print(f"[!] Error converting {file_path.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n[✓] Batch conversion finished: {success_count}/{len(TARGET_FILES)} files converted successfully!")

if __name__ == "__main__":
    batch_convert()

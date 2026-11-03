#!/usr/bin/env python3
"""
Comprehensive Duplicate Audit Script
Generates statistics and cross-reference table for automation-uat/DUPLICATE_AUDIT_REPORT.md
"""

import os
import openpyxl
from pathlib import Path

MASTER_PATH = Path("/home/baudui/Projects/automation-ui/automation-uat/MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx")

CANDIDATES = [
    {
        "num": 1,
        "path": "reports/testcase5173/01_admin_login_and_sso/TEST_EXECUTION_EVIDENCE_01_Admin_Login_And_Sso.xlsx",
        "domain": "Admin Portal (localhost:5173) - Auth & SSO",
    },
    {
        "num": 2,
        "path": "reports/testcase5173/02_admin_dashboard_shell/TEST_EXECUTION_EVIDENCE_02_Admin_Dashboard_Shell.xlsx",
        "domain": "Admin Portal (localhost:5173) - Dashboard Shell",
    },
    {
        "num": 3,
        "path": "reports/testcase5173/03_school_management/TEST_EXECUTION_EVIDENCE_03_School_Management.xlsx",
        "domain": "Admin Portal (localhost:5173) - School Management",
    },
    {
        "num": 4,
        "path": "reports/testcase5173/04_school_user_management/TEST_EXECUTION_EVIDENCE_04_School_User_Management.xlsx",
        "domain": "Admin Portal (localhost:5173) - School User Management",
    },
    {
        "num": 5,
        "path": "reports/testcase5173/06_class_management/TEST_EXECUTION_EVIDENCE_06_Class_Management.xlsx",
        "domain": "Admin Portal (localhost:5173) - Class Management",
    },
    {
        "num": 6,
        "path": "reports/testcase5173/07_student_management_and_enrollment/TEST_EXECUTION_EVIDENCE_07_Student_Management_And_Enrollment.xlsx",
        "domain": "Admin Portal (localhost:5173) - Student Management & Enrollment",
    },
    {
        "num": 7,
        "path": "reports/testcase5173/08_school_config/TEST_EXECUTION_EVIDENCE_08_School_Config.xlsx",
        "domain": "Admin Portal (localhost:5173) - School Configuration",
    },
    {
        "num": 8,
        "path": "reports/testcase5173/TEST_EXECUTION_EVIDENCE_Testcase5173.xlsx",
        "domain": "Admin Portal (localhost:5173) - Full Multi-Module Aggregated Suite",
    },
    {
        "num": 9,
        "path": "reports/testcase5174/coreservice/01_parent_login_and_mockpass/TEST_EXECUTION_EVIDENCE_01_Parent_Login_And_Mockpass.xlsx",
        "domain": "Parent Portal (localhost:5174) - Parent Login & MockPass",
    },
    {
        "num": 10,
        "path": "reports/testcase5174/coreservice/02_eservice_dashboard_home/TEST_EXECUTION_EVIDENCE_02_Eservice_Dashboard_Home.xlsx",
        "domain": "Parent Portal (localhost:5174) - E-Service Dashboard Home",
    },
    {
        "num": 11,
        "path": "reports/testcase5174/coreservice/03_parent_profile_and_contact/TEST_EXECUTION_EVIDENCE_03_Parent_Profile_And_Contact.xlsx",
        "domain": "Parent Portal (localhost:5174) - Parent Profile & Contact",
    },
    {
        "num": 12,
        "path": "reports/testcase5174/coreservice/06_payment_checkout_simulator/TEST_EXECUTION_EVIDENCE_06_Payment_Checkout_Simulator.xlsx",
        "domain": "Parent Portal (localhost:5174) - Payment Checkout Simulator",
    },
    {
        "num": 13,
        "path": "reports/testcase5174/coreservice/TEST_EXECUTION_EVIDENCE_Coreservice.xlsx",
        "domain": "Parent Portal (localhost:5174) - CoreService Smoke/Curated Suite",
    },
    {
        "num": 14,
        "path": "reports/fs03/fs03-dashboard-shell/TEST_EXECUTION_EVIDENCE_FS03_Dashboard_Shell.xlsx",
        "domain": "Admin Portal (localhost:5173) - FS03 Dashboard Shell",
    },
    {
        "num": 15,
        "path": "reports/fs03/fs03-school-create/TEST_EXECUTION_EVIDENCE_FS03_School_Create.xlsx",
        "domain": "Admin Portal (localhost:5173) - FS03 School Create",
    },
    {
        "num": 16,
        "path": "reports/fs08/fs08-parent-profile/TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx",
        "domain": "Parent Portal (localhost:5174) - FS08 Parent Profile Spec (English)",
    },
    {
        "num": 17,
        "path": "reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx",
        "domain": "Cross-System - Sprint 3 UAT Test Plan",
    },
    {
        "num": 18,
        "path": "reports/unit/TEST_EXECUTION_EVIDENCE_Unit.xlsx",
        "domain": "Internal Test Framework - Runner & Hygiene Unit Tests",
    },
]

def analyze_all():
    m_wb = openpyxl.load_workbook(MASTER_PATH, data_only=True)
    master_sheets = {}
    for sname in m_wb.sheetnames:
        ws = m_wb[sname]
        imgs = len(ws._images) if hasattr(ws, "_images") else 0
        rows = list(ws.iter_rows(values_only=True))
        tc_ids = []
        for r in rows:
            for c in r[:3]:
                if c and isinstance(c, str) and any(c.strip().startswith(p) for p in ["TC-", "STAGE-", "DEST-", "SEC-", "DEF-", "UAT-", "TEST-"]):
                    tc_ids.append(c.strip().split("\n")[0])
                    break
        master_sheets[sname] = {
            "row_count": len(rows),
            "imgs": imgs,
            "tc_ids": set(tc_ids),
            "tc_list": tc_ids
        }

    report_lines = []
    for c in CANDIDATES:
        p = Path(c["path"])
        if not p.exists():
            c["status"] = "MISSING"
            continue
        wb = openpyxl.load_workbook(p, data_only=True)
        ws = wb.active
        imgs = len(ws._images) if hasattr(ws, "_images") else 0
        rows = list(ws.iter_rows(values_only=True))
        tc_ids = []
        for r in rows:
            for cell in r[:3]:
                if cell and isinstance(cell, str) and any(cell.strip().startswith(p) for p in ["TC-", "STAGE-", "DEST-", "SEC-", "DEF-", "UAT-", "TEST-", "Ac", "Cod", "Nam"]):
                    tc_ids.append(cell.strip().split("\n")[0])
                    break
        
        # Check overlaps
        c_set = set(tc_ids)
        overlap_info = []
        for ms_name, ms_data in master_sheets.items():
            common = c_set.intersection(ms_data["tc_ids"])
            if common:
                pct = len(common) / len(c_set) * 100 if c_set else 0
                overlap_info.append((ms_name, len(common), pct, list(common)[:3]))
                
        c["rows"] = len(rows)
        c["tcs"] = len(tc_ids)
        c["imgs"] = imgs
        c["tc_ids"] = tc_ids
        c["overlap_info"] = overlap_info
        print(f"Cand {c['num']}: {c['path']} -> TCs: {c['tcs']}, Imgs: {c['imgs']}, Overlaps: {[(o[0], o[1], f'{o[2]:.1f}%') for o in overlap_info]}")

if __name__ == "__main__":
    analyze_all()

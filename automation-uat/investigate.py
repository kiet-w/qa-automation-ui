#!/usr/bin/env python3
"""
Detailed investigation of candidate workbooks and cross-module comparisons.
"""

import json
from pathlib import Path
import openpyxl

MASTER_FILE = Path("/home/baudui/Projects/automation-ui/automation-uat/MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx")

CANDIDATES = [
    "reports/testcase5173/01_admin_login_and_sso/TEST_EXECUTION_EVIDENCE_01_Admin_Login_And_Sso.xlsx",
    "reports/testcase5173/02_admin_dashboard_shell/TEST_EXECUTION_EVIDENCE_02_Admin_Dashboard_Shell.xlsx",
    "reports/testcase5173/03_school_management/TEST_EXECUTION_EVIDENCE_03_School_Management.xlsx",
    "reports/testcase5173/04_school_user_management/TEST_EXECUTION_EVIDENCE_04_School_User_Management.xlsx",
    "reports/testcase5173/06_class_management/TEST_EXECUTION_EVIDENCE_06_Class_Management.xlsx",
    "reports/testcase5173/07_student_management_and_enrollment/TEST_EXECUTION_EVIDENCE_07_Student_Management_And_Enrollment.xlsx",
    "reports/testcase5173/08_school_config/TEST_EXECUTION_EVIDENCE_08_School_Config.xlsx",
    "reports/testcase5173/TEST_EXECUTION_EVIDENCE_Testcase5173.xlsx",
    "reports/testcase5174/coreservice/01_parent_login_and_mockpass/TEST_EXECUTION_EVIDENCE_01_Parent_Login_And_Mockpass.xlsx",
    "reports/testcase5174/coreservice/02_eservice_dashboard_home/TEST_EXECUTION_EVIDENCE_02_Eservice_Dashboard_Home.xlsx",
    "reports/testcase5174/coreservice/03_parent_profile_and_contact/TEST_EXECUTION_EVIDENCE_03_Parent_Profile_And_Contact.xlsx",
    "reports/testcase5174/coreservice/06_payment_checkout_simulator/TEST_EXECUTION_EVIDENCE_06_Payment_Checkout_Simulator.xlsx",
    "reports/testcase5174/coreservice/TEST_EXECUTION_EVIDENCE_Coreservice.xlsx",
    "reports/fs03/fs03-dashboard-shell/TEST_EXECUTION_EVIDENCE_FS03_Dashboard_Shell.xlsx",
    "reports/fs03/fs03-school-create/TEST_EXECUTION_EVIDENCE_FS03_School_Create.xlsx",
    "reports/fs08/fs08-parent-profile/TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx",
    "reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx",
    "reports/unit/TEST_EXECUTION_EVIDENCE_Unit.xlsx",
]

def get_sheet_details(ws):
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return {"headers": [], "rows": [], "imgs": 0}
    
    header_idx = -1
    for idx, r in enumerate(rows[:15]):
        str_cells = [str(c).strip().lower() for c in r if c is not None]
        if any("tc" in c or "test case" in c or "scenario" in c or "test id" in c or "no" in c or "step" in c for c in str_cells):
            header_idx = idx
            break
    if header_idx == -1:
        header_idx = 0
    headers = [str(c).strip() if c is not None else "" for c in rows[header_idx]]
    
    col_map = {"id": -1, "title": -1, "url": -1, "status": -1}
    for c_idx, h in enumerate(headers):
        hl = h.lower()
        if col_map["id"] == -1 and any(k in hl for k in ["test case id", "tc id", "tc_id", "case id", "test id", "tc code"]):
            col_map["id"] = c_idx
        elif col_map["title"] == -1 and any(k in hl for k in ["title", "scenario", "test scenario", "name", "description", "test case description"]):
            col_map["title"] = c_idx
        elif col_map["url"] == -1 and any(k in hl for k in ["url", "endpoint", "page", "route", "target"]):
            col_map["url"] = c_idx
        elif col_map["status"] == -1 and any(k in hl for k in ["status", "result"]):
            col_map["status"] = c_idx

    data = []
    for r_idx in range(header_idx + 1, len(rows)):
        r = rows[r_idx]
        if not any(r):
            continue
        tc_id = ""
        if col_map["id"] != -1 and r[col_map["id"]] is not None:
            tc_id = str(r[col_map["id"]]).strip()
        else:
            for c in r[:3]:
                if c is not None:
                    cs = str(c).strip()
                    if any(cs.startswith(p) for p in ["TC-", "TC_", "UAT", "STAGE-", "DEST-", "SEC-", "DEF-", "TEST-"]):
                        tc_id = cs
                        break
        title = str(r[col_map["title"]]).strip() if col_map["title"] != -1 and r[col_map["title"]] is not None else ""
        url = str(r[col_map["url"]]).strip() if col_map["url"] != -1 and r[col_map["url"]] is not None else ""
        status = str(r[col_map["status"]]).strip() if col_map["status"] != -1 and r[col_map["status"]] is not None else ""
        
        # also check for endpoints if not in url col
        if not url:
            for c in r:
                if c and ("localhost" in str(c) or "http" in str(c) or "/" in str(c)):
                    if any(sub in str(c) for sub in ["5173", "5174", "portal", "admin", "school", "login"]):
                        url = str(c).strip()
                        break
        data.append({
            "id": tc_id,
            "title": title,
            "url": url,
            "status": status
        })
    img_count = len(ws._images) if hasattr(ws, "_images") else 0
    return {"headers": headers, "data": data, "imgs": img_count}

def main():
    m_wb = openpyxl.load_workbook(MASTER_FILE, data_only=True)
    master_info = {}
    for s in m_wb.sheetnames:
        master_info[s] = get_sheet_details(m_wb[s])
        
    cand_info = {}
    for c in CANDIDATES:
        p = Path(c)
        if not p.exists():
            continue
        c_wb = openpyxl.load_workbook(p, data_only=True)
        sheets_detail = {}
        for s in c_wb.sheetnames:
            sheets_detail[s] = get_sheet_details(c_wb[s])
        cand_info[c] = sheets_detail

    # Now let's analyze specific questions:
    print("=== ANALYSIS OF SPECIFIC CANDIDATES ===")
    
    # 1. Candidate 5: 06_class_management (18 TCs in cand vs 17 in Drive 06 Class Mgmt)
    c5_ids = [r["id"] for r in cand_info["reports/testcase5173/06_class_management/TEST_EXECUTION_EVIDENCE_06_Class_Management.xlsx"]["Test Cases"]["data"]]
    m_c6_ids = [r["id"] for r in master_info["Drive 06 Class Mgmt"]["data"]]
    print(f"Cand 5 IDs count: {len(c5_ids)}, Master Drive 06 IDs count: {len(m_c6_ids)}")
    print(f"Diff Cand5 - Master: {set(c5_ids) - set(m_c6_ids)}")
    print(f"Diff Master - Cand5: {set(m_c6_ids) - set(c5_ids)}")

    # 2. Candidate 8: TEST_EXECUTION_EVIDENCE_Testcase5173.xlsx vs 01, 02, 03, 04, 06, 07, 08
    c8_ids = [r["id"] for r in cand_info["reports/testcase5173/TEST_EXECUTION_EVIDENCE_Testcase5173.xlsx"]["Execution Evidence"]["data"]]
    c8_id_set = set(c8_ids)
    print(f"\nCandidate 8 Total TCs: {len(c8_ids)}, Unique IDs: {len(c8_id_set)}")
    
    # Breakdown of C8 IDs by prefix
    from collections import Counter
    prefixes = Counter([i.split("-")[1] if "-" in i else i[:6] for i in c8_ids])
    print(f"Candidate 8 ID prefixes: {prefixes}")
    
    # 3. Candidate 6 & 7 (07 Student Mgmt and 08 School Config)
    c6_ids = [r["id"] for r in cand_info["reports/testcase5173/07_student_management_and_enrollment/TEST_EXECUTION_EVIDENCE_07_Student_Management_And_Enrollment.xlsx"]["Test Cases"]["data"]]
    c7_ids = [r["id"] for r in cand_info["reports/testcase5173/08_school_config/TEST_EXECUTION_EVIDENCE_08_School_Config.xlsx"]["Test Cases"]["data"]]
    print(f"\nCandidate 6 (07 Student Mgmt): {len(c6_ids)} TCs, IDs: {c6_ids[:5]} ... {c6_ids[-3:]}")
    print(f"In Master?: {any(i in set(m_id for s in master_info.values() for m_id in [r['id'] for r in s['data']]) for i in c6_ids)}")
    print(f"In Cand 8?: {len(set(c6_ids).intersection(c8_id_set))} / {len(c6_ids)}")
    
    print(f"\nCandidate 7 (08 School Config): {len(c7_ids)} TCs, IDs: {c7_ids[:5]} ... {c7_ids[-3:]}")
    print(f"In Master?: {any(i in set(m_id for s in master_info.values() for m_id in [r['id'] for r in s['data']]) for i in c7_ids)}")
    print(f"In Cand 8?: {len(set(c7_ids).intersection(c8_id_set))} / {len(c7_ids)}")

    # 4. Candidate 14: fs03-dashboard-shell
    c14_ids = [r["id"] for r in cand_info["reports/fs03/fs03-dashboard-shell/TEST_EXECUTION_EVIDENCE_FS03_Dashboard_Shell.xlsx"]["Test Cases"]["data"]]
    print(f"\nCandidate 14 (fs03-dashboard-shell): {len(c14_ids)} TCs, vs Drive 02 Admin Dashboard: {c14_ids == [r['id'] for r in master_info['Drive 02 Admin Dashboard']['data']]}")

    # 5. Candidate 15: fs03-school-create
    c15_ids = [r["id"] for r in cand_info["reports/fs03/fs03-school-create/TEST_EXECUTION_EVIDENCE_FS03_School_Create.xlsx"]["Test Cases"]["data"]]
    m_sch_create = [r["id"] for r in master_info["FS03 School Create Evidence"]["data"]]
    m_drive_sch = [r["id"] for r in master_info["Drive 03 School Mgmt"]["data"]]
    print(f"\nCandidate 15 (fs03-school-create): {len(c15_ids)} TCs. IDs: {c15_ids}")
    print(f"Overlap with Master 'FS03 School Create Evidence': {set(c15_ids).intersection(set(m_sch_create))}")
    print(f"Overlap with Master 'Drive 03 School Mgmt': {set(c15_ids).intersection(set(m_drive_sch))}")

    # 6. Candidate 16: fs08-parent-profile
    c16_ids = [r["id"] for r in cand_info["reports/fs08/fs08-parent-profile/TEST_EXECUTION_EVIDENCE_FS08_Parent_Profile.xlsx"]["Execution Evidence (104 TCs)"]["data"]]
    print(f"\nCandidate 16 (fs08-parent-profile): {len(c16_ids)} TCs. Sample IDs: {c16_ids[:10]}")
    c11_ids = [r["id"] for r in cand_info["reports/testcase5174/coreservice/03_parent_profile_and_contact/TEST_EXECUTION_EVIDENCE_03_Parent_Profile_And_Contact.xlsx"]["Test Cases"]["data"]]
    print(f"Cand 11 (5174-03 parent profile) TCs: {len(c11_ids)}. Sample IDs: {c11_ids[:10]}")
    print(f"Overlap c16 and c11: {set(c16_ids).intersection(set(c11_ids))}")

    # 7. Coreservice candidates (9, 10, 11, 12, 13)
    c9_ids = [r["id"] for r in cand_info["reports/testcase5174/coreservice/01_parent_login_and_mockpass/TEST_EXECUTION_EVIDENCE_01_Parent_Login_And_Mockpass.xlsx"]["Test Cases"]["data"]]
    c10_ids = [r["id"] for r in cand_info["reports/testcase5174/coreservice/02_eservice_dashboard_home/TEST_EXECUTION_EVIDENCE_02_Eservice_Dashboard_Home.xlsx"]["Test Cases"]["data"]]
    c12_ids = [r["id"] for r in cand_info["reports/testcase5174/coreservice/06_payment_checkout_simulator/TEST_EXECUTION_EVIDENCE_06_Payment_Checkout_Simulator.xlsx"]["Test Cases"]["data"]]
    c13_ids = [r["id"] for r in cand_info["reports/testcase5174/coreservice/TEST_EXECUTION_EVIDENCE_Coreservice.xlsx"]["Execution Evidence"]["data"]]
    print(f"\nCoreservice 01 TCs ({len(c9_ids)}): {c9_ids}")
    print(f"Coreservice 02 TCs ({len(c10_ids)}): {c10_ids}")
    print(f"Coreservice 06 TCs ({len(c12_ids)}): {c12_ids}")
    print(f"Coreservice Aggregate C13 TCs ({len(c13_ids)}): {c13_ids}")
    all_core_sub = set(c9_ids) | set(c10_ids) | set(c11_ids) | set(c12_ids)
    print(f"Total union of Coreservice submodules (01, 02, 03, 06): {len(all_core_sub)} TCs")
    print(f"C13 overlap with Coreservice submodules: {len(set(c13_ids).intersection(all_core_sub))} / {len(c13_ids)}")

    # 8. Candidate 17 (uat) and 18 (unit)
    c17_ids = [r["id"] for r in cand_info["reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx"]["Tests"]["data"]]
    print(f"\nCandidate 17 (uat): {len(c17_ids)} TCs. Sample IDs: {c17_ids[:10]}")
    c17_titles = [r["title"] for r in cand_info["reports/uat/TEST_EXECUTION_EVIDENCE_Uat.xlsx"]["Tests"]["data"]][:5]
    print(f"Sample Titles c17: {c17_titles}")
    
    c18_ids = [r["id"] for r in cand_info["reports/unit/TEST_EXECUTION_EVIDENCE_Unit.xlsx"]["Execution Evidence"]["data"]]
    print(f"\nCandidate 18 (unit): {len(c18_ids)} TCs. Sample IDs: {c18_ids[:10]}")

if __name__ == "__main__":
    main()

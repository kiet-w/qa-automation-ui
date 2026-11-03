#!/usr/bin/env python3
"""
Rigorous Evidence-Based Duplicate Audit Script
Cross-references candidate test reports in reports/ against MASTER_TEST_EXECUTION_EVIDENCE_ALL_MODULES.xlsx
"""

import os
import sys
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

def analyze_sheet(ws):
    """Extract rows, test cases, images, and key text fields from an openpyxl worksheet."""
    img_count = len(ws._images) if hasattr(ws, "_images") else 0
    rows = list(ws.iter_rows(values_only=True))
    
    # Find headers
    header_idx = -1
    headers = []
    for idx, r in enumerate(rows[:10]):
        str_cells = [str(c).strip().lower() for c in r if c is not None]
        if any("tc" in c or "test case" in c or "scenario" in c or "test id" in c or "no" in c for c in str_cells):
            header_idx = idx
            headers = [str(c).strip() if c is not None else "" for c in r]
            break
            
    test_cases = []
    if header_idx != -1:
        # Map columns
        tc_id_col = -1
        tc_title_col = -1
        url_col = -1
        status_col = -1
        
        for c_idx, h in enumerate(headers):
            hl = h.lower()
            if any(k in hl for k in ["test case id", "tc id", "tc_id", "case id", "test id"]):
                tc_id_col = c_idx
            elif any(k in hl for k in ["title", "scenario", "test description", "description", "test case description"]):
                tc_title_col = c_idx
            elif any(k in hl for k in ["url", "endpoint", "page", "target"]):
                url_col = c_idx
            elif any(k in hl for k in ["status", "result"]):
                status_col = c_idx
                
        # If no explicit tc_id_col, fallback to col 0 or 1
        for r_idx in range(header_idx + 1, len(rows)):
            row = rows[r_idx]
            if not any(row):
                continue
            tc_id = str(row[tc_id_col]).strip() if tc_id_col != -1 and row[tc_id_col] is not None else ""
            title = str(row[tc_title_col]).strip() if tc_title_col != -1 and row[tc_title_col] is not None else ""
            url = str(row[url_col]).strip() if url_col != -1 and row[url_col] is not None else ""
            status = str(row[status_col]).strip() if status_col != -1 and row[status_col] is not None else ""
            
            # If tc_id is empty, try first few cols
            if not tc_id:
                for c in row[:3]:
                    if c and any(prefix in str(c) for prefix in ["TC", "UAT", "SEC", "DATE", "BUG", "FORM"]):
                        tc_id = str(c).strip()
                        break
            
            # Combine non-empty cells for signature
            row_signature = " | ".join(str(c).strip() for c in row if c is not None)
            test_cases.append({
                "row_idx": r_idx + 1,
                "tc_id": tc_id,
                "title": title,
                "url": url,
                "status": status,
                "raw": row_signature
            })
            
    return {
        "title": ws.title,
        "max_row": ws.max_row,
        "max_column": ws.max_column,
        "image_count": img_count,
        "header_idx": header_idx,
        "headers": headers,
        "test_cases": test_cases
    }

def main():
    print(f"Loading Master Workbook: {MASTER_FILE}")
    master_wb = openpyxl.load_workbook(MASTER_FILE, data_only=True)
    master_sheets = {}
    print(f"Master Sheet Names ({len(master_wb.sheetnames)}):")
    for name in master_wb.sheetnames:
        ws = master_wb[name]
        info = analyze_sheet(ws)
        master_sheets[name] = info
        tc_ids = [t['tc_id'] for t in info['test_cases'] if t['tc_id']]
        print(f"  - [{name}]: max_row={info['max_row']}, images={info['image_count']}, TCs={len(info['test_cases'])}, sample_ids={tc_ids[:3]}")

    print("\n" + "="*80)
    print("ANALYZING CANDIDATE FILES")
    print("="*80)
    
    candidates_info = {}
    for cand in CANDIDATES:
        p = Path(cand)
        if not p.exists():
            print(f"[MISSING FILE] {cand}")
            continue
        try:
            wb = openpyxl.load_workbook(p, data_only=True)
            sheet_infos = []
            total_images = 0
            total_tcs = 0
            for sname in wb.sheetnames:
                ws = wb[sname]
                sinfo = analyze_sheet(ws)
                sheet_infos.append(sinfo)
                total_images += sinfo["image_count"]
                total_tcs += len(sinfo["test_cases"])
            candidates_info[cand] = {
                "sheets": sheet_infos,
                "total_images": total_images,
                "total_tcs": total_tcs
            }
            snames = [s["title"] for s in sheet_infos]
            sample_ids = []
            for s in sheet_infos:
                sample_ids.extend([t['tc_id'] for t in s['test_cases'] if t['tc_id']])
            print(f"\nCandidate: {cand}")
            print(f"  Sheets ({len(snames)}): {snames} | Total TCs: {total_tcs} | Images: {total_images}")
            print(f"  Sample TC IDs: {sample_ids[:5]}")
        except Exception as e:
            print(f"[ERROR READING] {cand}: {e}")

if __name__ == "__main__":
    main()

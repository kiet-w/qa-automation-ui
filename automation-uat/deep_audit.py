#!/usr/bin/env python3
"""
Deep cross-reference script:
Compares candidate workbooks against the 14 Master sheets in detail.
"""

import os
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

def extract_rows(ws):
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    
    header_idx = -1
    for idx, r in enumerate(rows[:15]):
        str_cells = [str(c).strip().lower() for c in r if c is not None]
        if any("tc" in c or "test case" in c or "scenario" in c or "test id" in c or "no" in c or "step" in c for c in str_cells):
            header_idx = idx
            break
            
    if header_idx == -1:
        header_idx = 0
        
    headers = [str(c).strip() if c is not None else "" for c in rows[header_idx]]
    
    # Identify key columns
    col_map = {"id": -1, "title": -1, "url": -1, "status": -1, "desc": -1, "image": -1}
    for c_idx, h in enumerate(headers):
        hl = h.lower()
        if col_map["id"] == -1 and any(k in hl for k in ["test case id", "tc id", "tc_id", "case id", "test id", "tc code"]):
            col_map["id"] = c_idx
        elif col_map["title"] == -1 and any(k in hl for k in ["title", "scenario", "test scenario", "name"]):
            col_map["title"] = c_idx
        elif col_map["desc"] == -1 and any(k in hl for k in ["description", "test case description", "objective"]):
            col_map["desc"] = c_idx
        elif col_map["url"] == -1 and any(k in hl for k in ["url", "endpoint", "page", "route", "target"]):
            col_map["url"] = c_idx
        elif col_map["status"] == -1 and any(k in hl for k in ["status", "result"]):
            col_map["status"] = c_idx
        elif col_map["image"] == -1 and any(k in hl for k in ["evidence", "screenshot", "image"]):
            col_map["image"] = c_idx

    data_rows = []
    for r_idx in range(header_idx + 1, len(rows)):
        r = rows[r_idx]
        if not any(r):
            continue
        
        tc_id = ""
        if col_map["id"] != -1 and r[col_map["id"]] is not None:
            tc_id = str(r[col_map["id"]]).strip()
        else:
            # Fallback scan in first 3 columns
            for c in r[:3]:
                if c is not None:
                    cs = str(c).strip()
                    if any(cs.startswith(p) for p in ["TC-", "TC_", "UAT", "STAGE-", "DEST-", "SEC-", "DEF-", "TEST-"]):
                        tc_id = cs
                        break
        
        title = str(r[col_map["title"]]).strip() if col_map["title"] != -1 and r[col_map["title"]] is not None else ""
        desc = str(r[col_map["desc"]]).strip() if col_map["desc"] != -1 and r[col_map["desc"]] is not None else ""
        url = str(r[col_map["url"]]).strip() if col_map["url"] != -1 and r[col_map["url"]] is not None else ""
        status = str(r[col_map["status"]]).strip() if col_map["status"] != -1 and r[col_map["status"]] is not None else ""
        
        data_rows.append({
            "row_num": r_idx + 1,
            "id": tc_id,
            "title": title or desc,
            "url": url,
            "status": status,
            "full_row": [str(c) if c is not None else "" for c in r]
        })
    return headers, data_rows

def main():
    m_wb = openpyxl.load_workbook(MASTER_FILE, data_only=True)
    master_data = {}
    master_all_tc_ids = set()
    master_id_to_sheet = {}
    
    for sname in m_wb.sheetnames:
        ws = m_wb[sname]
        headers, rows = extract_rows(ws)
        img_count = len(ws._images) if hasattr(ws, "_images") else 0
        tc_ids = [r["id"] for r in rows if r["id"]]
        for tid in tc_ids:
            # Clean newline or extra formatting
            clean_id = tid.replace("\n", " ").strip()
            master_all_tc_ids.add(clean_id)
            master_id_to_sheet[clean_id] = sname
            
        master_data[sname] = {
            "headers": headers,
            "rows": rows,
            "img_count": img_count,
            "tc_ids": set(tc_ids)
        }
        
    print(f"Master workbook loaded. Total sheets: {len(master_data)}, Total unique TC IDs: {len(master_all_tc_ids)}")

    results = []

    for cand_path in CANDIDATES:
        p = Path(cand_path)
        if not p.exists():
            results.append({"candidate": cand_path, "status": "MISSING"})
            continue
            
        c_wb = openpyxl.load_workbook(p, data_only=True)
        cand_sheets = {}
        cand_all_tc_ids = []
        cand_total_imgs = 0
        cand_rows_count = 0
        
        for sname in c_wb.sheetnames:
            ws = c_wb[sname]
            headers, rows = extract_rows(ws)
            img_count = len(ws._images) if hasattr(ws, "_images") else 0
            cand_total_imgs += img_count
            cand_rows_count += len(rows)
            for r in rows:
                if r["id"]:
                    cand_all_tc_ids.append(r["id"])
            cand_sheets[sname] = {
                "headers": headers,
                "rows": rows,
                "img_count": img_count
            }
            
        # Analyze overlap with master sheets
        overlap_by_sheet = {}
        for sname, m_info in master_data.items():
            common = set(cand_all_tc_ids).intersection(m_info["tc_ids"])
            if common:
                overlap_by_sheet[sname] = {
                    "count": len(common),
                    "percentage": len(common) / len(cand_all_tc_ids) if cand_all_tc_ids else 0,
                    "samples": list(common)[:5]
                }
                
        # Also check title similarities or row text
        results.append({
            "candidate": cand_path,
            "sheet_count": len(c_wb.sheetnames),
            "sheet_names": c_wb.sheetnames,
            "total_tcs": len(cand_all_tc_ids),
            "total_rows": cand_rows_count,
            "total_images": cand_total_imgs,
            "tc_ids_sample": cand_all_tc_ids[:5],
            "overlap_by_sheet": overlap_by_sheet
        })

    output_file = Path("/tmp/audit_summary.json")
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSummary written to {output_file}")
    for res in results:
        print(f"\nCandidate: {res.get('candidate')}")
        print(f"  Sheets: {res.get('sheet_names')}, TCs: {res.get('total_tcs')}, Imgs: {res.get('total_images')}")
        print(f"  Overlap with master: {res.get('overlap_by_sheet')}")

if __name__ == "__main__":
    main()

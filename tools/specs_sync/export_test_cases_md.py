#!/usr/bin/env python3
"""
Exports and structures Sprint 1 Test Cases and Defects from:
  [agile] fs/raw/Test Cases + Defect sprint 1.xlsx
Into high-fidelity Markdown files in:
  [agile] fs/md/Test Cases/
  [agile] fs/md/Test Cases + Defect sprint 1.md
"""

import os
from pathlib import Path
import openpyxl

REPO_ROOT = Path(__file__).resolve().parents[2]
XLSX_PATH = str(REPO_ROOT / "specs/raw/Test Cases + Defect sprint 1.xlsx")
MD_DIR = str(REPO_ROOT / "specs/md/Test Cases")
MASTER_MD_PATH = str(REPO_ROOT / "specs/md/Test Cases + Defect sprint 1.md")

MODULE_TITLES = {
    "R1 TC": {
        "filename": "TC_R1_Education_Account_Lifecycle.md",
        "title": "R1: Education Account Lifecycle & Closure — Sprint 1 Test Cases",
        "module": "R1 - Education Account Lifecycle",
        "spec_ref": "[agile] fs/md/FS document/FS-01_Education_Account_Lifecycle.md"
    },
    "R3 TC": {
        "filename": "TC_R3_School_Student_Fee_Management.md",
        "title": "R3: School, Student & Fee Master Data Management — Sprint 1 Test Cases",
        "module": "R3 - School, Student & Fee Master Data",
        "spec_ref": "[agile] fs/md/FS document/FS-03_School_Student_Fee_Management.md"
    },
    "R8 TC": {
        "filename": "TC_R8_Parent_Portal_SingPass_Profile.md",
        "title": "R8: Parent Portal (SingPass, Profile & Account Info) — Sprint 1 Test Cases",
        "module": "R8 - Parent Portal & SingPass Profile",
        "spec_ref": "[agile] fs/md/FS document/FS-08_Parent_Portal_SingPass_Profile.md"
    },
    "R9 TC": {
        "filename": "TC_R9_Outstanding_Fees_and_Payment.md",
        "title": "R9: Outstanding Fees and Payment Engine — Sprint 1 Test Cases",
        "module": "R9 - Outstanding Fees and Payment",
        "spec_ref": "[agile] fs/md/FS document/FS-09_Outstanding_Fees_and_Payment.md"
    }
}

def clean_cell(val):
    if val is None:
        return ""
    text = str(val).strip()
    return text

def clean_cell_table(val):
    if val is None:
        return ""
    text = str(val).strip().replace("\n", "<br>").replace("|", "\\|")
    return text

def generate_clean_master_md(wb, output_path):
    lines = ["# Test Cases + Defect sprint 1.xlsx\n"]
    lines.append("> Source: `[agile] fs/raw/Test Cases + Defect sprint 1.xlsx`\n")
    lines.append("> Single Source of Truth for Sprint 1 QA Test Cases (R1, R3, R8, R9) and Defect Log.\n\n")

    for sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        lines.append(f"\n## Sheet: {sheet_name}\n")
        
        # Determine actual header length
        header_vals = []
        for col in range(1, sheet.max_column + 1):
            val = sheet.cell(1, col).value
            if val is not None and str(val).strip():
                header_vals.append(str(val).strip().replace("\n", " "))
            else:
                break
        
        num_cols = len(header_vals)
        if num_cols == 0:
            lines.append("*(Sheet is empty)*\n")
            continue
        
        lines.append("| " + " | ".join(header_vals) + " |")
        lines.append("| " + " | ".join([":---"] * num_cols) + " |")

        for r in range(2, sheet.max_row + 1):
            row_data = [sheet.cell(r, c).value for c in range(1, num_cols + 1)]
            if not any(v is not None and str(v).strip() for v in row_data):
                continue
            cleaned = [clean_cell_table(v) for v in row_data]
            lines.append("| " + " | ".join(cleaned) + " |")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated clean master MD: {output_path}")

def generate_tc_module_md(sheet, meta, output_path):
    tc_rows = []
    num_cols = 19
    for r in range(2, sheet.max_row + 1):
        tc_id = sheet.cell(r, 1).value
        if tc_id and str(tc_id).strip():
            row_dict = {
                "id": clean_cell(sheet.cell(r, 1).value),
                "scenario_id": clean_cell(sheet.cell(r, 2).value),
                "title": clean_cell(sheet.cell(r, 3).value),
                "test_suite": clean_cell(sheet.cell(r, 4).value),
                "page": clean_cell(sheet.cell(r, 5).value),
                "severity": clean_cell(sheet.cell(r, 6).value),
                "priority": clean_cell(sheet.cell(r, 7).value),
                "status": clean_cell(sheet.cell(r, 8).value),
                "test_type": clean_cell(sheet.cell(r, 9).value),
                "environment": clean_cell(sheet.cell(r, 10).value),
                "preconditions": clean_cell(sheet.cell(r, 11).value),
                "test_data": clean_cell(sheet.cell(r, 12).value),
                "test_steps": clean_cell(sheet.cell(r, 13).value),
                "expected_result": clean_cell(sheet.cell(r, 14).value),
                "actual_result": clean_cell(sheet.cell(r, 15).value),
                "assumption_ref": clean_cell(sheet.cell(r, 16).value),
                "defect_id": clean_cell(sheet.cell(r, 17).value),
                "traceability": clean_cell(sheet.cell(r, 18).value),
                "note": clean_cell(sheet.cell(r, 19).value),
            }
            tc_rows.append(row_dict)

    lines = []
    lines.append(f"# {meta['title']}\n")
    lines.append(f"> **Module**: {meta['module']}")
    lines.append(f"> **Specification Reference**: [{os.path.basename(meta['spec_ref'])}](file:///{os.path.abspath(meta['spec_ref'])})")
    lines.append(f"> **Source Spreadsheet**: `Test Cases + Defect sprint 1.xlsx` (Sheet `{sheet.title}`)")
    lines.append(f"> **Total Test Cases**: {len(tc_rows)}\n")

    # Group by suite
    suites = {}
    for tc in tc_rows:
        suite = tc["test_suite"] or "Unclassified"
        suites.setdefault(suite, []).append(tc)

    lines.append("## Executive Test Suite Summary\n")
    lines.append("| Test Suite | Scenario Count | Test Cases | Priorities | Severities |")
    lines.append("| :--- | :--- | :--- | :--- | :--- |")
    for s_name, items in suites.items():
        scenarios = set(it["scenario_id"] for it in items if it["scenario_id"])
        priorities = set(it["priority"] for it in items if it["priority"])
        severities = set(it["severity"] for it in items if it["severity"])
        lines.append(f"| {s_name} | {len(scenarios)} ({', '.join(sorted(scenarios))}) | {len(items)} | {', '.join(sorted(priorities))} | {', '.join(sorted(severities))} |")
    lines.append("\n---\n")

    lines.append("## Quick Reference Index Table\n")
    lines.append("| Test Case ID | Scenario ID | Title | Page / Area | Priority | Severity | Type | Defect ID | Traceability |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for tc in tc_rows:
        t_id = tc["id"]
        sc_id = tc["scenario_id"]
        title = tc["title"].replace("|", "\\|")
        page = tc["page"].replace("|", "\\|")
        pri = tc["priority"]
        sev = tc["severity"]
        ttype = tc["test_type"]
        def_id = tc["defect_id"]
        trace = tc["traceability"].replace("\n", " ").replace("|", "\\|")
        lines.append(f"| [`{t_id}`](#{t_id.lower().replace(' ', '-')}) | `{sc_id}` | {title} | {page} | {pri} | {sev} | {ttype} | {def_id} | {trace} |")
    lines.append("\n---\n")

    lines.append("## Detailed Test Case Specifications\n")
    for s_name, items in suites.items():
        lines.append(f"\n### Test Suite: {s_name}\n")
        for tc in items:
            t_id = tc["id"]
            lines.append(f"#### `{t_id}`: {tc['title']}\n")
            lines.append(f"- **Scenario ID**: `{tc['scenario_id']}`")
            lines.append(f"- **Test Suite**: {tc['test_suite']}")
            lines.append(f"- **Page / Target**: `{tc['page']}`")
            lines.append(f"- **Severity / Priority**: `{tc['severity']}` / `{tc['priority']}`")
            lines.append(f"- **Execution Status**: `{tc['status']}` | **Test Type**: `{tc['test_type']}`")
            if tc['defect_id']:
                lines.append(f"- **Linked Defect ID**: `{tc['defect_id']}`")
            if tc['traceability']:
                lines.append(f"- **Traceability**: {tc['traceability']}")
            if tc['environment']:
                lines.append(f"- **Environment**: {tc['environment']}")
            if tc['assumption_ref']:
                lines.append(f"- **Assumption Reference**: {tc['assumption_ref']}")
            if tc['note']:
                lines.append(f"- **Note**: {tc['note']}")
            
            lines.append("\n**Preconditions:**")
            lines.append(f"```text\n{tc['preconditions'] if tc['preconditions'] else '(None)'}\n```")

            lines.append("\n**Test Data:**")
            lines.append(f"```text\n{tc['test_data'] if tc['test_data'] else '(None)'}\n```")

            lines.append("\n**Test Steps:**")
            steps = tc['test_steps'].split("\n")
            for step in steps:
                s = step.strip()
                if s:
                    lines.append(f"- {s}" if not s[0].isdigit() else s)

            lines.append("\n**Expected Result:**")
            lines.append(f"> {tc['expected_result'].replace(chr(10), chr(10) + '> ')}")
            
            if tc['actual_result']:
                lines.append(f"\n**Actual Result:**\n> {tc['actual_result']}")

            lines.append("\n---\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated module MD: {output_path} ({len(tc_rows)} TCs)")

def generate_defects_md(wb, output_path):
    defect_sheets = [("R1 Defect", "R1"), ("R3 Defect", "R3"), ("R8 Defect", "R8"), ("R9 Defect", "R9")]
    all_defects = []

    for s_name, mod in defect_sheets:
        sheet = wb[s_name]
        for r in range(2, sheet.max_row + 1):
            d_id = sheet.cell(r, 1).value
            if d_id and str(d_id).strip():
                d_dict = {
                    "module": mod,
                    "sheet": s_name,
                    "id": clean_cell(sheet.cell(r, 1).value),
                    "summary": clean_cell(sheet.cell(r, 2).value),
                    "severity": clean_cell(sheet.cell(r, 3).value),
                    "priority": clean_cell(sheet.cell(r, 4).value),
                    "status": clean_cell(sheet.cell(r, 5).value),
                    "type": clean_cell(sheet.cell(r, 6).value),
                    "environment": clean_cell(sheet.cell(r, 7).value),
                    "preconditions": clean_cell(sheet.cell(r, 8).value),
                    "steps": clean_cell(sheet.cell(r, 9).value),
                    "expected": clean_cell(sheet.cell(r, 10).value),
                    "actual": clean_cell(sheet.cell(r, 11).value),
                    "linked_tcs": clean_cell(sheet.cell(r, 12).value),
                    "evidence": clean_cell(sheet.cell(r, 13).value),
                    "notes": clean_cell(sheet.cell(r, 14).value),
                }
                all_defects.append(d_dict)

    lines = []
    lines.append("# Sprint 1 Defect Log & Known Issues Master\n")
    lines.append("> Source: `[agile] fs/raw/Test Cases + Defect sprint 1.xlsx`")
    lines.append("> Covers known defects identified during Sprint 1 test execution across R1, R3, R8, and R9.")
    lines.append("> Use with `@pytest.mark.xfail(strict=True, reason=\"<BUG-ID>: <summary>\")` per Invariant 5 in `AGENTS.md`.\n\n")

    lines.append("## Defect Inventory Matrix\n")
    lines.append("| Defect ID | Module | Status | Severity | Priority | Type | Summary | Linked TCs |")
    lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    for d in all_defects:
        sum_clean = d["summary"].replace("\n", " ").replace("|", "\\|")
        linked_clean = d["linked_tcs"].replace("\n", " ").replace("|", "\\|")
        lines.append(f"| [`{d['id']}`](#{d['id'].lower()}) | `{d['module']}` | **{d['status']}** | {d['severity']} | {d['priority']} | {d['type']} | {sum_clean} | `{linked_clean}` |")

    lines.append("\n---\n")
    lines.append("## Detailed Defect Reports\n")

    for d in all_defects:
        d_id = d["id"]
        lines.append(f"### `{d_id}`: {d['summary'].split(chr(10))[0]}\n")
        lines.append(f"- **Module**: `{d['module']}` ({d['sheet']})")
        lines.append(f"- **Status**: **{d['status']}**")
        lines.append(f"- **Severity / Priority**: `{d['severity']}` / `{d['priority']}`")
        lines.append(f"- **Defect Type**: `{d['type']}`")
        if d['linked_tcs']:
            lines.append(f"- **Linked Test Case(s)**: `{d['linked_tcs']}`")
        if d['environment']:
            lines.append(f"- **Environment**: {d['environment'].replace(chr(10), ' | ')}")
        if d['evidence']:
            lines.append(f"- **Evidence**: {d['evidence']}")
        if d['notes']:
            lines.append(f"- **Notes**: {d['notes']}")

        lines.append("\n**Preconditions:**")
        lines.append(f"```text\n{d['preconditions'] if d['preconditions'] else '(None)'}\n```")

        lines.append("\n**Steps to Reproduce:**")
        steps = d['steps'].split("\n")
        for step in steps:
            s = step.strip()
            if s:
                lines.append(f"- {s}" if not s[0].isdigit() else s)

        lines.append("\n**Expected Result:**")
        lines.append(f"> {d['expected'].replace(chr(10), chr(10) + '> ')}")

        lines.append("\n**Actual Result:**")
        lines.append(f"> {d['actual'].replace(chr(10), chr(10) + '> ')}")

        lines.append("\n**Pytest Strict XFAIL Directive:**")
        lines.append(f"```python\n@pytest.mark.xfail(strict=True, reason=\"{d_id}: {d['summary'].split(chr(10))[0]}\")\n```")

        lines.append("\n---\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated defects MD: {output_path} ({len(all_defects)} defects)")

def generate_index_readme(output_path):
    content = """# Sprint 1 Test Cases & Defect Catalog

Single source of truth for all automated and manual Test Cases and Defect logs executed during Sprint 1 for the MOE Education Account & Fee Management System (EAFAMS).

## 📚 Module Test Suites

| Module | Document | Scope | Total TCs | Defect Count |
| :--- | :--- | :--- | :--- | :--- |
| **R1: Education Account Lifecycle** | [`TC_R1_Education_Account_Lifecycle.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R1_Education_Account_Lifecycle.md) | Age 7 auto-creation, age 16 closure, sync audit, duplicate prevention, wallet & ledger rules | 73 | 1 (Template) |
| **R3: School, Student & Fee Master** | [`TC_R3_School_Student_Fee_Management.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R3_School_Student_Fee_Management.md) | School setup, academic levels, classes, fee catalog, fee pricing, publication & charges | 105 | 5 (Open) |
| **R8: Parent Portal & Profile** | [`TC_R8_Parent_Portal_SingPass_Profile.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R8_Parent_Portal_SingPass_Profile.md) | SingPass authentication, home dashboard, parent details update, child link, audit log | 125 | 5 (Open) |
| **R9: Outstanding Fees & Payment** | [`TC_R9_Outstanding_Fees_and_Payment.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/TC_R9_Outstanding_Fees_and_Payment.md) | Invoice access, EA payment, online payment, split payment, idempotency, retry, receipts | 162 | 3 (Open) |
| **Defects Master Log** | [`DEFECTS_Sprint_1_Master.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases/DEFECTS_Sprint_1_Master.md) | All known defects across R1, R3, R8, R9 with steps to reproduce, expected results & xfail syntax | - | 14 total |
| **Master Workbook Raw Table** | [`Test Cases + Defect sprint 1.md`](file:///home/baudui/Projects/automation-ui/%5Bagile%5D%20fs/md/Test%20Cases%20%2B%20Defect%20sprint%201.md) | Complete unedited multi-sheet tabular view exported directly from Google Sheets | 465 | 14 |

---

## 🎯 Traceability & Invariant Guidelines
Per **`AGENTS.md`**:
- **Invariant 3 (Test Case Identification & Traceability)**: Every test function must be named `test_tc_<scenario_id>_...` matching the corresponding TC or Scenario ID from these documents.
- **Invariant 5 (Verification-First Bug Handling)**: Open bugs listed in `DEFECTS_Sprint_1_Master.md` must be decorated with `@pytest.mark.xfail(strict=True, reason="BUG-xxx: <description>")`.
- **Invariant 6 (Zero Assumptions)**: Assertions and data parameters MUST cite the exact Test Case ID and Expected Result from these markdown files.
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated index README: {output_path}")

def main():
    os.makedirs(MD_DIR, exist_ok=True)
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)

    # 1. Clean Master MD
    generate_clean_master_md(wb, MASTER_MD_PATH)

    # 2. Module MDs
    for sheet_name, meta in MODULE_TITLES.items():
        sheet = wb[sheet_name]
        out_path = os.path.join(MD_DIR, meta["filename"])
        generate_tc_module_md(sheet, meta, out_path)

    # 3. Defects Master MD
    defects_out_path = os.path.join(MD_DIR, "DEFECTS_Sprint_1_Master.md")
    generate_defects_md(wb, defects_out_path)

    # 4. Readme Index
    readme_out_path = os.path.join(MD_DIR, "README.md")
    generate_index_readme(readme_out_path)

    print("ALL TEST CASES AND DEFECTS EXPORTED AND STRUCTURED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

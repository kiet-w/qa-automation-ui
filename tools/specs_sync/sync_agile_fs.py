#!/usr/bin/env python3
"""
tools/sync_agile_fs.py - Đồng bộ toàn diện & chuyển đổi tài liệu Google Drive vào [agile] fs/
Architecture:
- [agile] fs/raw/: Lưu trữ tài liệu gốc (gdoc -> docx, gsheet -> xlsx, binary docx/xlsx/xlsm).
- [agile] fs/md/: Chuyển đổi Markdown độ trung thực cao cho AI coding agents.
- Tự động bóc tách 'Tổng hợp FS' thành các module độc lập FS-01 đến FS-10.
- Tự động xuất 465+ Test Cases và Defects từ 'Test Cases + Defect sprint 1.xlsx'.
"""

import os
import sys
import subprocess
import shutil
import re
from pathlib import Path
import openpyxl
import docx

WORKSPACE = Path(__file__).resolve().parents[2]
RAW_DIR = WORKSPACE / "specs" / "raw"
MD_DIR = WORKSPACE / "specs" / "md"
GDRIVE_CLI = "/home/baudui/.gemini/config/plugins/gdrive/skills/gdrive/scripts/gdrive"

def run_cmd(cmd):
    cmd_str = " ".join(cmd)
    print(f"Executing: {cmd_str}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR {res.returncode}] {res.stderr.strip()}", file=sys.stderr)
    else:
        print(f"  [SUCCESS] {res.stdout.strip()[:120]}")
    return res

def excel_to_markdown(xlsx_path, md_path):
    try:
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        lines = [f"# {os.path.basename(xlsx_path)}\n"]
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            lines.append(f"\n## Sheet: {sheet_name}\n")
            rows = []
            max_col = 0
            for row in sheet.iter_rows(values_only=True):
                cleaned_row = [str(c).strip().replace("\n", "<br>") if c is not None else "" for c in row]
                if any(cleaned_row):
                    rows.append(cleaned_row)
                    if len(cleaned_row) > max_col:
                        max_col = len(cleaned_row)
            if not rows:
                lines.append("*(Sheet is empty)*\n")
                continue
            for r in rows:
                while len(r) < max_col:
                    r.append("")
            header = rows[0]
            header_labels = [h if h else f"Col_{i+1}" for i, h in enumerate(header)]
            lines.append("| " + " | ".join(header_labels) + " |")
            lines.append("| " + " | ".join([":---"] * max_col) + " |")
            for r in rows[1:]:
                lines.append("| " + " | ".join(r) + " |")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  ✓ Excel -> MD: {xlsx_path.name} -> {md_path.name}")
    except Exception as e:
        print(f"  [!] Failed converting {xlsx_path} to MD: {e}", file=sys.stderr)

def docx_to_markdown(docx_path, md_path):
    try:
        doc = docx.Document(docx_path)
        lines = [f"# {os.path.basename(docx_path).replace('.docx', '')}\n"]
        for element in doc.element.body:
            tag = element.tag.split('}')[-1]
            if tag == 'p':
                p = docx.text.paragraph.Paragraph(element, doc)
                text = p.text.strip()
                if not text:
                    continue
                style_name = p.style.name if p.style else ""
                if "Heading 1" in style_name:
                    lines.append(f"\n# {text}\n")
                elif "Heading 2" in style_name:
                    lines.append(f"\n## {text}\n")
                elif "Heading 3" in style_name:
                    lines.append(f"\n### {text}\n")
                elif "Heading 4" in style_name:
                    lines.append(f"\n#### {text}\n")
                elif "List" in style_name:
                    lines.append(f"- {text}")
                else:
                    lines.append(f"\n{text}")
            elif tag == 'tbl':
                tbl = docx.table.Table(element, doc)
                table_rows = []
                for row in tbl.rows:
                    row_cells = [cell.text.strip().replace("\n", "<br>") for cell in row.cells]
                    table_rows.append(row_cells)
                if table_rows:
                    lines.append("\n| " + " | ".join(table_rows[0]) + " |")
                    lines.append("| " + " | ".join([":---"] * len(table_rows[0])) + " |")
                    for r in table_rows[1:]:
                        lines.append("| " + " | ".join(r) + " |")
                    lines.append("")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  ✓ Docx -> MD: {docx_path.name} -> {md_path.name}")
    except Exception as e:
        print(f"  [!] Failed converting {docx_path} to MD: {e}", file=sys.stderr)

ITEMS = [
    # Root Folder
    {"id": "1pEDzZFchCHvW1TW-D1USJvNnJWwHwqp8_DwjLlkKgHk", "name": "[Agile] High-level Solution", "type": "gdoc", "subpath": ""},
    {"id": "1pBGhdjuLnCzpJMs41NTfmnSTZ2r15-JBg4bOMZBOArI", "name": "Feature list", "type": "gdoc", "subpath": ""},
    {"id": "1i_tgxB7jRS2GYGo3QNlT1r7OyqJzZeJlfm63B3so47k", "name": "First meeting questions", "type": "gdoc", "subpath": ""},
    {"id": "1CJl6aP92qwMMzroW0-Na0YZqsMcVK1Dev4RxcjSm4JA", "name": "Nội dung Overview Sprint 1", "type": "gdoc", "subpath": ""},
    {"id": "1k7paZmnUG_2dl62q_9dYdMpcUgv9Lc2m", "name": "Product Backlog V2.xlsm", "type": "binary", "subpath": ""},
    {"id": "1t-bbhmbKYh20_77fKZRmr7g-PyxXTyv9", "name": "Test Cases + Defect sprint 1.xlsx", "type": "binary", "subpath": ""},

    # defeact Folder
    {"id": "1MqvjAzudgwKR_98K3Zv1FGelZaURvdk8aVbrqWMvLxA", "name": "DEFECT MY Profile(edusave)", "type": "gdoc", "subpath": "defeact"},

    # Dev Folder
    {"id": "1t8cyWpOe9L8ECS-lmzXmtWSm_kXkF8SQSx2BQ7Z3p88", "name": "Sprint Backlog", "type": "gsheet", "subpath": "Dev"},

    # Documentation Folder
    {"id": "1V6f8hoe6rC8WZ_haJ5lvhM0LcguWrXX7n-In9TkXD6o", "name": "[AGILE] MoM 23-10-2026", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1TYnZ44hcBkcycc6gcdY4W4RiFkIrSsMf", "name": "Meeting Transcript - 23 Oct 2026.docx", "type": "binary", "subpath": "Documentation"},
    {"id": "1hg9DZ0TLMNOqNnq6aYPisEG76lh_VCNE78MSBffU9bE", "name": "Agile Glossary", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1PtJandfYWUeulz3XP8XeJNKkJX4K7zkIILDZkHFTS24", "name": "Agile requirements", "type": "gsheet", "subpath": "Documentation"},
    {"id": "1F_BRbQKK_YRrj0phpMIZ5IeY8tiH2hwq5fnV6AesLPQ", "name": "Kickoff Transcript refined", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1-0dL2-DsYh_aRo1vTmjLfS3iJHvrZCu8", "name": "Meeting Transcript - 19 Oct 2026.docx", "type": "binary", "subpath": "Documentation"},
    {"id": "11Vj7sqPQo10I2S44suvTrJjCE68iEKV4iRLhQAlvhOw", "name": "MoM - Kickoff meeting - 12/10", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1p5w-oVDXgjMizjOF8LgJDpq43oalACjCmki4cq9c24U", "name": "MoM - Sprint 1 - 16/10", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1wb-i82JJbipSala8NUfd9K42SPVfGZX4EGhNZpNYdgo", "name": "Questionaire", "type": "gsheet", "subpath": "Documentation"},
    {"id": "1RwS1SpU2ijyZeWdEQtNsEGvtceFMAAM6", "name": "Sprint 1 Review Transcript.docx", "type": "binary", "subpath": "Documentation"},

    # FS document Folder
    {"id": "1k0xJrdGwCzFzfqVhofzwgRPcdvoV8O9DFtzWpq-_kjQ", "name": "Tổng hợp FS", "type": "gdoc", "subpath": "FS document"},
    {"id": "136FreXwU5XDCJLkTV5lXqLsbvGAn659YfWc85mTKLqk", "name": "R6 — analysis", "type": "gdoc", "subpath": "FS document"},
    {"id": "1ZtldHtOf786wmVkKDZUxRpDF9kwTjmE1", "name": "FS-08 Parent Portal – SingPass, Education Account, Profile.docx", "type": "binary", "subpath": "FS document"},
    {"id": "1lTsdeia41yMKhH5w7X8t1S5BvGIyifzB", "name": "FS Function 9 - Outstanding Fees and Payment (Final).docx", "type": "binary", "subpath": "FS document"},
    {"id": "1_x7FDJyGzf6zkw54RkdeZ0b_9b67jdU8", "name": "FS R2 – Top-Up Management.docx", "type": "binary", "subpath": "FS document"},

    # Requirement analysis Folder
    {"id": "1yhv1VlMDopiOmBo6F9qS08kwi6Kj7lcai0H4bEaQNyw", "name": "Function Requirements", "type": "gdoc", "subpath": "Requirement analysis"},
    {"id": "1YpRJKk_LpoCpdYv7V4uhSrQXhD5rm2OCvUW1uWfK_ds", "name": "Functional Reqirement 3", "type": "gdoc", "subpath": "Requirement analysis"},
]

def split_tong_hop_fs(md_path: Path):
    """
    Split master 'Tổng hợp FS.md' into modular specifications FS-01 to FS-10
    based on authoritative section markers.
    """
    print("\n[+] Bóc tách 'Tổng hợp FS.md' thành các module độc lập FS-01 đến FS-10...")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    def find_idx(pattern):
        for i, l in enumerate(lines):
            if l.strip().startswith(pattern):
                return i
        return -1

    r1_final = find_idx("# **R1 (Final)**")
    r2_v3 = find_idx("# **R2 (v3)**")
    r3_v3 = find_idx("# **R3 v3**")
    r4 = find_idx("# **R4**")
    r5 = find_idx("# **R5**")
    r6 = find_idx("# **R6**")
    r7 = find_idx("# **R7**")
    r8_final = find_idx("# **R8 (Final)**")
    r9_v2 = find_idx("# **R9 (v2)**")
    r10 = find_idx("# **R10**")

    fs_dir = md_path.parent
    modules = {}

    if r1_final != -1 and r2_v3 != -1:
        modules["FS-01_Education_Account_Lifecycle.md"] = lines[r1_final:r2_v3]

    if r2_v3 != -1 and r3_v3 != -1:
        modules["FS-02_Education_Account_TopUp.md"] = lines[r2_v3:r3_v3]

    if r3_v3 != -1 and r4 != -1:
        modules["FS-03_School_Student_Fee_Management.md"] = lines[r3_v3:r4]

    if r4 != -1 and r5 != -1:
        modules["FS-04_Financial_Assistance_Scheme_FAS.md"] = lines[r4:r5]

    if r5 != -1 and r6 != -1:
        modules["FS-05_Hardcopy_Applications_Offline.md"] = lines[r5:r6]

    if r6 != -1 and r7 != -1:
        modules["FS-06_FAS_Budget_and_Statistics.md"] = lines[r6:r7]

    if r7 != -1 and r8_final != -1:
        modules["FS-07_User_Simulation_ViewAs.md"] = lines[r7:r8_final]

    if r8_final != -1 and r9_v2 != -1:
        modules["FS-08_Parent_Portal_SingPass_Profile.md"] = lines[r8_final:r9_v2]

    if r9_v2 != -1 and r10 != -1:
        modules["FS-09_Outstanding_Fees_and_Payment.md"] = lines[r9_v2:r10]

    if r10 != -1:
        modules["FS-10_FAS_Family_Application_Portal.md"] = lines[r10:]

    for fname, content in modules.items():
        out_file = fs_dir / fname
        with open(out_file, "w", encoding="utf-8") as out:
            out.writelines(content)
        print(f"  ✓ Sinh module {fname} ({len(content)} dòng)")

def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU ĐỒNG BỘ TÀI LIỆU GOOGLE DRIVE VÀO [AGILE] FS")
    print("=" * 70)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    updated_count = 0

    for item in ITEMS:
        sub_raw = RAW_DIR / item["subpath"]
        sub_md = MD_DIR / item["subpath"]
        sub_raw.mkdir(parents=True, exist_ok=True)
        sub_md.mkdir(parents=True, exist_ok=True)

        name = item["name"]
        safe_name = name.replace("/", "-")
        fid = item["id"]
        itype = item["type"]

        print(f"\n[•] Đang xử lý: {item['subpath']}/{name} ({itype}) [ID: {fid}]...")

        if itype == "gdoc":
            raw_path = sub_raw / f"{safe_name}.docx"
            md_path = sub_md / f"{safe_name}.md"
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(raw_path), "--format", "docx"])
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(md_path), "--format", "md"])
            updated_count += 1

            if name == "Tổng hợp FS":
                split_tong_hop_fs(md_path)

        elif itype == "gsheet":
            raw_path = sub_raw / f"{safe_name}.xlsx"
            md_path = sub_md / f"{safe_name}.md"
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(raw_path), "--format", "xlsx"])
            excel_to_markdown(raw_path, md_path)
            updated_count += 1

        elif itype == "binary":
            raw_path = sub_raw / safe_name
            run_cmd([GDRIVE_CLI, "readonly", "download", fid, "--out", str(raw_path)])
            clean_name = Path(safe_name).stem
            md_path = sub_md / f"{clean_name}.md"

            if name.endswith(".docx"):
                docx_to_markdown(raw_path, md_path)
            elif name.endswith((".xlsx", ".xlsm")):
                excel_to_markdown(raw_path, md_path)
            updated_count += 1

    # Tự động xuất Test Cases & Defects từ 'Test Cases + Defect sprint 1.xlsx'
    test_cases_script = Path(__file__).resolve().parent / "export_test_cases_md.py"
    if test_cases_script.exists():
        print("\n" + "=" * 70)
        print("📊 TỰ ĐỘNG XUẤT 465+ TEST CASES & DEFECTS SPRINT 1")
        print("=" * 70)
        subprocess.run(["python3", str(test_cases_script)], cwd=str(WORKSPACE))

    print("\n" + "=" * 70)
    print(f"✅ ĐỒNG BỘ TOÀN BỘ {updated_count} TÀI LIỆU GOOGLE DRIVE THÀNH CÔNG!")
    print(f"  • Thư mục Raw  : {RAW_DIR}")
    print(f"  • Thư mục MD   : {MD_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
tools/sync_specs.py
Đồng bộ toàn diện tài liệu từ Google Drive (ID: 1wry8P-LjWUMaXIg70qa4spuGU4VJc42a)
vào thư mục specs/raw/ và specs/md/, đồng thời bóc tách module và cập nhật UAT.
"""

import os
import sys
import json
import subprocess
import shutil
import re
from pathlib import Path
import openpyxl
import docx

WORKSPACE = Path(__file__).resolve().parent.parent
RAW_DIR = WORKSPACE / "specs" / "raw"
MD_DIR = WORKSPACE / "specs" / "md"
GDRIVE_CLI = shutil.which("gdrive") or "/home/baudui/.gemini/antigravity/bin/gdrive"
ROOT_FOLDER_ID = "1wry8P-LjWUMaXIg70qa4spuGU4VJc42a"

def run_cmd(cmd, desc=""):
    if desc:
        print(f"[CMD] {desc}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [ERROR] {res.stderr.strip()}", file=sys.stderr)
    else:
        out = res.stdout.strip()
        if out:
            print(f"  [OK] {out[:100]}...")
    return res

def sanitize_name(name):
    # Thay thế ký tự không an toàn cho tên file/folder trên hệ thống tệp
    return name.replace("/", "-").replace("\\", "-").replace(":", "-").strip()

def excel_to_markdown(xlsx_path, md_path):
    try:
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        lines = [f"# {Path(xlsx_path).name}\n"]
        for sheet_name in wb.sheetnames:
            sheet = wb[sheet_name]
            lines.append(f"\n## Sheet: {sheet_name}\n")
            rows = []
            max_col = 0
            for row in sheet.iter_rows(values_only=True):
                cleaned_row = [str(c).strip().replace("\n", "<br>").replace("|", "\\|") if c is not None else "" for c in row]
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
        md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  ✓ Excel -> MD: {xlsx_path.name} -> {md_path.name}")
    except Exception as e:
        print(f"  [!] Failed converting {xlsx_path} to MD: {e}", file=sys.stderr)

def docx_to_markdown(docx_path, md_path):
    try:
        doc = docx.Document(docx_path)
        lines = [f"# {Path(docx_path).stem}\n"]
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
                    row_cells = [cell.text.strip().replace("\n", "<br>").replace("|", "\\|") for cell in row.cells]
                    table_rows.append(row_cells)
                if table_rows:
                    lines.append("\n| " + " | ".join(table_rows[0]) + " |")
                    lines.append("| " + " | ".join([":---"] * len(table_rows[0])) + " |")
                    for r in table_rows[1:]:
                        lines.append("| " + " | ".join(r) + " |")
                    lines.append("")
        md_path.parent.mkdir(parents=True, exist_ok=True)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  ✓ Docx -> MD: {docx_path.name} -> {md_path.name}")
    except Exception as e:
        print(f"  [!] Failed converting {docx_path} to MD: {e}", file=sys.stderr)

def split_tong_hop_fs(md_path: Path):
    """
    Split master 'Tổng hợp FS.md' into modular specifications FS-01 to FS-10
    """
    print("\n[+] Bóc tách 'Tổng hợp FS.md' thành các module độc lập FS-01 đến FS-10...")
    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    def find_idx(patterns):
        if isinstance(patterns, str):
            patterns = [patterns]
        for i, l in enumerate(lines):
            for pat in patterns:
                if pat.lower() in l.lower() and l.strip().startswith("#"):
                    return i
        return -1

    r1_idx = find_idx(["#  **r1", "# **r1", "r1 – education account lifecycle"])
    r2_idx = find_idx(["# **function 2 (r2)", "# **fs function 2"])
    r3_idx = find_idx(["# **functional specification – r3", "# **functional specification - r3"])
    r4_idx = find_idx(["# **fs f4", "# **r4"])
    r5_idx = find_idx(["# **fs f5", "# **r5"])
    r6_idx = find_idx(["r6 – fas budget & statistics", "r6 - fas budget", "# **r6"])
    # If r6_idx found in subhead, find preceding # heading
    if r6_idx != -1 and not lines[r6_idx].strip().startswith("# **FUNCTIONAL"):
        for back in range(r6_idx, max(0, r6_idx - 10), -1):
            if lines[back].strip().startswith("# **FUNCTIONAL"):
                r6_idx = back
                break

    r8_idx = find_idx(["# **fs-08", "# **fs 08", "# **r8"])
    r9_idx = find_idx(["# **fs function 9", "# **r9"])
    r10_idx = find_idx(["# **fs f10", "# **r10"])

    print(f"  Indices: R1={r1_idx}, R2={r2_idx}, R3={r3_idx}, R4={r4_idx}, R5={r5_idx}, R6={r6_idx}, R8={r8_idx}, R9={r9_idx}, R10={r10_idx}")

    fs_dir = md_path.parent
    modules = {}

    if r1_idx != -1 and r2_idx != -1:
        modules["FS-01_Education_Account_Lifecycle.md"] = lines[r1_idx:r2_idx]
    if r2_idx != -1 and r3_idx != -1:
        modules["FS-02_Education_Account_TopUp.md"] = lines[r2_idx:r3_idx]
    if r3_idx != -1 and r4_idx != -1:
        modules["FS-03_School_Student_Fee_Management.md"] = lines[r3_idx:r4_idx]
    if r4_idx != -1 and r5_idx != -1:
        modules["FS-04_Financial_Assistance_Scheme_FAS.md"] = lines[r4_idx:r5_idx]
    if r5_idx != -1 and r6_idx != -1:
        modules["FS-05_Hardcopy_Applications_Offline.md"] = lines[r5_idx:r6_idx]
    if r6_idx != -1 and r8_idx != -1:
        modules["FS-06_FAS_Budget_and_Statistics.md"] = lines[r6_idx:r8_idx]
    if r8_idx != -1 and r9_idx != -1:
        modules["FS-08_Parent_Portal_SingPass_Profile.md"] = lines[r8_idx:r9_idx]
    if r9_idx != -1 and r10_idx != -1:
        modules["FS-09_Outstanding_Fees_and_Payment.md"] = lines[r9_idx:r10_idx]
    if r10_idx != -1:
        modules["FS-10_FAS_Family_Application_Portal.md"] = lines[r10_idx:]

    for fname, content in modules.items():
        out_file = fs_dir / fname
        with open(out_file, "w", encoding="utf-8") as out:
            out.writelines(content)
        print(f"  ✓ Sinh module {fname} ({len(content)} dòng)")

def scan_folder(folder_id, current_rel=""):
    cmd = [GDRIVE_CLI, "readonly", "ls", folder_id, "--json"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error listing folder {folder_id}: {res.stderr}", file=sys.stderr)
        return []
    items = json.loads(res.stdout)
    all_files = []
    for it in items:
        name = it.get("name", "")
        safe_item_name = sanitize_name(name)
        rel_path = f"{current_rel}/{safe_item_name}" if current_rel else safe_item_name
        it["rel_path"] = rel_path
        mime = it.get("mimeType", "")
        if mime == "application/vnd.google-apps.folder":
            all_files.extend(scan_folder(it["id"], rel_path))
        else:
            all_files.append(it)
    return all_files

def main():
    print("=" * 70)
    print("🚀 BẮT ĐẦU ĐỒNG BỘ TOÀN BỘ TÀI LIỆU GOOGLE DRIVE VÀO SPECS/")
    print(f"Drive Folder ID: {ROOT_FOLDER_ID}")
    print("=" * 70)

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    MD_DIR.mkdir(parents=True, exist_ok=True)

    items = scan_folder(ROOT_FOLDER_ID)
    print(f"Tìm thấy tổng cộng {len(items)} files trong Google Drive.")

    updated_count = 0

    for it in items:
        fid = it["id"]
        rel_path = it["rel_path"]
        mime = it.get("mimeType", "")
        name = it.get("name", "")
        mod_time = it.get("modifiedTime", "")

        rel_dir = Path(rel_path).parent
        file_stem = Path(rel_path).stem
        file_suffix = Path(rel_path).suffix

        raw_folder = RAW_DIR / rel_dir
        md_folder = MD_DIR / rel_dir
        raw_folder.mkdir(parents=True, exist_ok=True)
        md_folder.mkdir(parents=True, exist_ok=True)

        print(f"\n[•] Xử lý: {rel_path} ({mime}) [MTime: {mod_time}]")

        if mime == "application/vnd.google-apps.document":
            raw_path = raw_folder / f"{file_stem}.docx"
            md_path = md_folder / f"{file_stem}.md"
            print(f"  -> Exporting Google Doc to {raw_path.name} & {md_path.name}")
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(raw_path), "--format", "docx"])
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(md_path), "--format", "md"])
            updated_count += 1

            if name == "Tổng hợp FS":
                split_tong_hop_fs(md_path)

        elif mime == "application/vnd.google-apps.spreadsheet":
            raw_path = raw_folder / f"{file_stem}.xlsx"
            md_path = md_folder / f"{file_stem}.md"
            print(f"  -> Exporting Google Sheet to {raw_path.name}")
            run_cmd([GDRIVE_CLI, "readonly", "export", fid, str(raw_path), "--format", "xlsx"])
            excel_to_markdown(raw_path, md_path)
            updated_count += 1

        else:
            # Binary file: docx, xlsx, xlsm, pdf, etc.
            filename = Path(rel_path).name
            raw_path = raw_folder / filename
            print(f"  -> Downloading binary to {raw_path}")
            run_cmd([GDRIVE_CLI, "readonly", "download", fid, "--out", str(raw_path)])
            updated_count += 1

            clean_stem = Path(filename).stem
            md_path = md_folder / f"{clean_stem}.md"

            if filename.lower().endswith(".docx"):
                docx_to_markdown(raw_path, md_path)
            elif filename.lower().endswith((".xlsx", ".xlsm")):
                excel_to_markdown(raw_path, md_path)

    # Nếu có QA/uat-master.xlsx, cập nhật vào uat/
    qa_uat = RAW_DIR / "QA" / "uat-master.xlsx"
    if qa_uat.exists():
        target_uat_master = WORKSPACE / "uat" / "MASTER_UAT_SPRINT_3.xlsx"
        target_uat = WORKSPACE / "uat" / "uat.xlsx"
        shutil.copy2(qa_uat, target_uat_master)
        shutil.copy2(qa_uat, target_uat)
        print(f"\n[+] Đã cập nhật {qa_uat} -> {target_uat_master} và {target_uat}")

    print("\n" + "=" * 70)
    print(f"✅ HOÀN TẤT ĐỒNG BỘ {updated_count} TÀI LIỆU VÀO SPECS!")
    print(f"  • Thư mục Raw  : {RAW_DIR}")
    print(f"  • Thư mục MD   : {MD_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()

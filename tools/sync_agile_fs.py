#!/usr/bin/env python3
"""
Orchestrates downloading and conversion of all Google Drive Agile Project files into:
- [agile] fs/raw/ (original binary docx/xlsx/xlsm)
- [agile] fs/md/ (high-fidelity Markdown for AI coding agents)
"""

import os
import subprocess
import shutil
import openpyxl
import docx

WORKSPACE = "/home/baudui/Projects/automation-ui"
RAW_DIR = os.path.join(WORKSPACE, "[agile] fs", "raw")
MD_DIR = os.path.join(WORKSPACE, "[agile] fs", "md")
GDRIVE_CLI = "/home/baudui/.gemini/config/plugins/gdrive/skills/gdrive/scripts/gdrive"

def run_cmd(cmd):
    print(f"Executing: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error ({res.returncode}): {res.stderr}")
    else:
        print(f"Done: {res.stdout.strip()}")
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
        print(f"Excel -> MD: {xlsx_path} -> {md_path}")
    except Exception as e:
        print(f"Failed converting {xlsx_path} to MD: {e}")

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
        print(f"Docx -> MD: {docx_path} -> {md_path}")
    except Exception as e:
        print(f"Failed converting {docx_path} to MD: {e}")

ITEMS = [
    # Root
    {"id": "1pEDzZFchCHvW1TW-D1USJvNnJWwHwqp8_DwjLlkKgHk", "name": "[Agile] High-level Solution", "type": "gdoc", "subpath": ""},
    {"id": "1pBGhdjuLnCzpJMs41NTfmnSTZ2r15-JBg4bOMZBOArI", "name": "Feature list", "type": "gdoc", "subpath": ""},
    {"id": "1i_tgxB7jRS2GYGo3QNlT1r7OyqJzZeJlfm63B3so47k", "name": "First meeting questions", "type": "gdoc", "subpath": ""},
    {"id": "1CJl6aP92qwMMzroW0-Na0YZqsMcVK1Dev4RxcjSm4JA", "name": "Nội dung Overview Sprint 1", "type": "gdoc", "subpath": ""},
    {"id": "1k7paZmnUG_2dl62q_9dYdMpcUgv9Lc2m", "name": "Product Backlog V2.xlsm", "type": "binary", "subpath": ""},
    {"id": "1t-bbhmbKYh20_77fKZRmr7g-PyxXTyv9", "name": "Test Cases + Defect sprint 1.xlsx", "type": "binary", "subpath": ""},

    # Documentation
    {"id": "1hg9DZ0TLMNOqNnq6aYPisEG76lh_VCNE78MSBffU9bE", "name": "Agile Glossary", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1PtJandfYWUeulz3XP8XeJNKkJX4K7zkIILDZkHFTS24", "name": "Agile requirements", "type": "gsheet", "subpath": "Documentation"},
    {"id": "1F_BRbQKK_YRrj0phpMIZ5IeY8tiH2hwq5fnV6AesLPQ", "name": "Kickoff Transcript refined", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1-0dL2-DsYh_aRo1vTmjLfS3iJHvrZCu8", "name": "Meeting Transcript - 19 Oct 2026.docx", "type": "binary", "subpath": "Documentation"},
    {"id": "11Vj7sqPQo10I2S44suvTrJjCE68iEKV4iRLhQAlvhOw", "name": "MoM - Kickoff meeting - 12_10", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1p5w-oVDXgjMizjOF8LgJDpq43oalACjCmki4cq9c24U", "name": "MoM - Sprint 1 - 16_10", "type": "gdoc", "subpath": "Documentation"},
    {"id": "1wb-i82JJbipSala8NUfd9K42SPVfGZX4EGhNZpNYdgo", "name": "Questionaire", "type": "gsheet", "subpath": "Documentation"},
    {"id": "1RwS1SpU2ijyZeWdEQtNsEGvtceFMAAM6", "name": "Sprint 1 Review Transcript.docx", "type": "binary", "subpath": "Documentation"},

    # FS document
    {"id": "1lTsdeia41yMKhH5w7X8t1S5BvGIyifzB", "name": "FS Function 9 - Outstanding Fees and Payment (Final).docx", "type": "binary", "subpath": "FS document"},
    {"id": "1_x7FDJyGzf6zkw54RkdeZ0b_9b67jdU8", "name": "FS R2 – Top-Up Management.docx", "type": "binary", "subpath": "FS document"},
    {"id": "1ZtldHtOf786wmVkKDZUxRpDF9kwTjmE1", "name": "FS-08 Parent Portal – SingPass, Education Account, Profile.docx", "type": "binary", "subpath": "FS document"},
    {"id": "136FreXwU5XDCJLkTV5lXqLsbvGAn659YfWc85mTKLqk", "name": "R6 — analysis", "type": "gdoc", "subpath": "FS document"},
    {"id": "1k0xJrdGwCzFzfqVhofzwgRPcdvoV8O9DFtzWpq-_kjQ", "name": "Tổng hợp FS", "type": "gdoc", "subpath": "FS document"},

    # Requirement analysis
    {"id": "1yhv1VlMDopiOmBo6F9qS08kwi6Kj7lcai0H4bEaQNyw", "name": "Function Requirements", "type": "gdoc", "subpath": "Requirement analysis"},
    {"id": "1YpRJKk_LpoCpdYv7V4uhSrQXhD5rm2OCvUW1uWfK_ds", "name": "Functional Reqirement 3", "type": "gdoc", "subpath": "Requirement analysis"},
]

def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(MD_DIR, exist_ok=True)

    for item in ITEMS:
        sub_raw = os.path.join(RAW_DIR, item["subpath"])
        sub_md = os.path.join(MD_DIR, item["subpath"])
        os.makedirs(sub_raw, exist_ok=True)
        os.makedirs(sub_md, exist_ok=True)

        name = item["name"]
        fid = item["id"]
        itype = item["type"]

        if itype == "gdoc":
            raw_path = os.path.join(sub_raw, f"{name}.docx")
            md_path = os.path.join(sub_md, f"{name}.md")
            if not os.path.exists(raw_path):
                run_cmd([GDRIVE_CLI, "readonly", "export", fid, raw_path, "--format", "docx"])
            if not os.path.exists(md_path):
                run_cmd([GDRIVE_CLI, "readonly", "export", fid, md_path, "--format", "md"])

        elif itype == "gsheet":
            raw_path = os.path.join(sub_raw, f"{name}.xlsx")
            md_path = os.path.join(sub_md, f"{name}.md")
            if not os.path.exists(raw_path):
                run_cmd([GDRIVE_CLI, "readonly", "export", fid, raw_path, "--format", "xlsx"])
            excel_to_markdown(raw_path, md_path)

        elif itype == "binary":
            raw_path = os.path.join(sub_raw, name)
            if not os.path.exists(raw_path):
                run_cmd([GDRIVE_CLI, "readonly", "download", fid, "--out", raw_path])
            
            clean_name = os.path.splitext(name)[0]
            md_path = os.path.join(sub_md, f"{clean_name}.md")
            if name.endswith(".docx"):
                docx_to_markdown(raw_path, md_path)
            elif name.endswith((".xlsx", ".xlsm")):
                if name == "Test Cases + Defect sprint 1.xlsx":
                    subprocess.run(["python3", os.path.join(WORKSPACE, "tools", "export_test_cases_md.py")])
                else:
                    excel_to_markdown(raw_path, md_path)

    print("ALL DRIVE FILES DOWNLOADED AND CONVERTED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

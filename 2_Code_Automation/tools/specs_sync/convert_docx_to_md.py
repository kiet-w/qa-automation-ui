#!/usr/bin/env python3
import sys
import os
from pathlib import Path
import docx

def docx_to_markdown(docx_path: str, md_path: str):
    docx_file = Path(docx_path)
    md_file = Path(md_path)
    if not docx_file.exists():
        print(f"File not found: {docx_path}", file=sys.stderr)
        sys.exit(1)

    doc = docx.Document(docx_file)
    lines = [f"# {docx_file.stem}\n"]

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

    md_file.parent.mkdir(parents=True, exist_ok=True)
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Successfully converted {docx_file} -> {md_file} ({len(lines)} lines)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: convert_docx_to_md.py <input.docx> <output.md>")
        sys.exit(1)
    docx_to_markdown(sys.argv[1], sys.argv[2])

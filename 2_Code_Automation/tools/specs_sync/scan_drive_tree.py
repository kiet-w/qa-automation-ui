#!/usr/bin/env python3
import subprocess
import json
import sys

def list_folder(folder_id, path=""):
    res = subprocess.run(["gdrive", "readonly", "ls", folder_id, "--json"], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error listing {folder_id}: {res.stderr}", file=sys.stderr)
        return []
    items = json.loads(res.stdout)
    results = []
    for item in items:
        name = item.get("name", "")
        cur_path = f"{path}/{name}" if path else name
        item["full_path"] = cur_path
        mime = item.get("mimeType", "")
        if mime == "application/vnd.google-apps.folder":
            results.append(item)
            results.extend(list_folder(item["id"], cur_path))
        else:
            results.append(item)
    return results

root_id = "1wry8P-LjWUMaXIg70qa4spuGU4VJc42a"
all_items = list_folder(root_id)
print(f"Total items found: {len(all_items)}")
for it in all_items:
    mime = it.get("mimeType", "")
    fid = it.get("id", "")
    mtime = it.get("modifiedTime", "")
    fpath = it.get("full_path", "")
    size = it.get("size", "")
    print(f"{mime:45} | {mtime:24} | {fid:44} | {fpath}")

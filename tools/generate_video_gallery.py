#!/usr/bin/env python3
import json
from pathlib import Path
import sys

ROOT = Path("/home/baudui/automation-ui")
sys.path.append(str(ROOT / "tools"))
from generate_execution_evidence_xlsx import EXECUTED_CASES

OUTPUT_HTML = ROOT / "reports" / "fs03" / "fs03-school-create" / "video_gallery.html"

items = []
for tc in EXECUTED_CASES:
    rel_path = tc["video_subpath"].replace("reports/fs03/fs03-school-create/", "")
    items.append({
        "id": tc["id"],
        "pillar": tc["pillar"],
        "title": tc["title"],
        "status": tc["status"],
        "severity": tc["severity"],
        "video_src": rel_path,
        "video_name": tc["video_name"],
        "actual": tc["actual"]
    })

items_json = json.dumps(items, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduFAMS FS03 — 1080p Video Evidence Player</title>
  <style>
    :root {
      --bg: #0F172A;
      --card-bg: #1E293B;
      --border: #334155;
      --text: #F8FAFC;
      --text-muted: #94A3B8;
      --accent: #3B82F6;
      --success: #22C55E;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }
    .sidebar {
      width: 440px;
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      background: #111827;
    }
    .sidebar-header {
      padding: 16px;
      border-bottom: 1px solid var(--border);
    }
    .sidebar-header h1 {
      font-size: 15px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 4px;
    }
    .sidebar-header p {
      font-size: 12px;
      color: var(--text-muted);
    }
    .search-box {
      margin-top: 10px;
      width: 100%;
      padding: 8px 12px;
      background: #1F2937;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 13px;
    }
    .tc-list {
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }
    .tc-item {
      padding: 10px 12px;
      border-radius: 6px;
      margin-bottom: 6px;
      cursor: pointer;
      background: #1F2937;
      border: 1px solid transparent;
      transition: all 0.15s;
    }
    .tc-item:hover {
      background: #374151;
    }
    .tc-item.active {
      background: #1E3A8A;
      border-color: #3B82F6;
    }
    .tc-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 4px;
    }
    .tc-id {
      font-family: monospace;
      font-size: 11px;
      font-weight: bold;
      color: #60A5FA;
    }
    .badge {
      font-size: 10px;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(34, 197, 94, 0.2);
      color: #4ADE80;
    }
    .tc-title {
      font-size: 12px;
      color: #E2E8F0;
      line-height: 1.4;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
    .main-view {
      flex: 1;
      display: flex;
      flex-direction: column;
      padding: 24px;
      overflow-y: auto;
    }
    .video-wrapper {
      background: #000;
      border-radius: 10px;
      overflow: hidden;
      box-shadow: 0 10px 25px rgba(0,0,0,0.5);
      border: 1px solid var(--border);
      max-height: 65vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    video {
      width: 100%;
      height: 100%;
      max-height: 65vh;
      outline: none;
    }
    .info-panel {
      margin-top: 16px;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px;
    }
    .info-title {
      font-size: 16px;
      font-weight: bold;
      color: #F8FAFC;
      margin-bottom: 8px;
    }
    .info-desc {
      font-size: 13px;
      color: #94A3B8;
      line-height: 1.5;
    }
    .info-actual {
      margin-top: 10px;
      padding: 8px 12px;
      background: rgba(34, 197, 94, 0.1);
      border-left: 3px solid #22C55E;
      color: #86EFAC;
      font-size: 12px;
    }
  </style>
</head>
<body>
  <div class="sidebar">
    <div class="sidebar-header">
      <h1>🎬 FS03: Test Video Evidence</h1>
      <p>22 Full HD 1080p Recordings (100% Passed)</p>
      <input type="text" id="search" class="search-box" placeholder="🔍 Tìm kiếm test case (ID, tên)..." oninput="filterList()">
    </div>
    <div class="tc-list" id="tc-list"></div>
  </div>
  <div class="main-view">
    <div class="video-wrapper">
      <video id="player" controls autoplay>
        <source id="video-source" src="" type="video/webm">
        Trình duyệt không hỗ trợ thẻ video HTML5.
      </video>
    </div>
    <div class="info-panel">
      <div class="info-title" id="cur-title">Chọn một test case bên trái để xem video</div>
      <div class="info-desc" id="cur-id"></div>
      <div class="info-actual" id="cur-actual"></div>
    </div>
  </div>

  <script>
    const cases = __CASES_JSON__;
    let activeIdx = 0;

    function renderList(filtered = cases) {
      const container = document.getElementById('tc-list');
      container.innerHTML = '';
      filtered.forEach((tc) => {
        const div = document.createElement('div');
        div.className = 'tc-item ' + (tc.id === cases[activeIdx].id ? 'active' : '');
        div.onclick = () => selectCase(cases.indexOf(tc));
        div.innerHTML = `
          <div class="tc-top">
            <span class="tc-id">${tc.id}</span>
            <span class="badge">${tc.status}</span>
          </div>
          <div class="tc-title">${tc.title}</div>
        `;
        container.appendChild(div);
      });
    }

    function selectCase(idx) {
      activeIdx = idx;
      const tc = cases[idx];
      const player = document.getElementById('player');
      const source = document.getElementById('video-source');
      source.src = tc.video_src;
      player.load();
      player.play();

      document.getElementById('cur-title').innerText = tc.title;
      document.getElementById('cur-id').innerText = `${tc.id} • Pillar: ${tc.pillar} • Severity: ${tc.severity} • File: ${tc.video_name}`;
      document.getElementById('cur-actual').innerText = tc.actual;

      renderList();
    }

    function filterList() {
      const q = document.getElementById('search').value.toLowerCase();
      const filtered = cases.filter(c => c.id.toLowerCase().includes(q) || c.title.toLowerCase().includes(q));
      renderList(filtered);
    }

    if (cases.length > 0) {
      selectCase(0);
    }
  </script>
</body>
</html>"""

final_html = html_template.replace("__CASES_JSON__", items_json)
OUTPUT_HTML.write_text(final_html, encoding="utf-8")
print(f"[+] Successfully wrote: {OUTPUT_HTML}")

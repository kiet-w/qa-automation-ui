"""
reporting/clean_report.py - Minimalist, Human-Friendly HTML Test Report Generator.

Transforms report.json into an intuitive 4-tier hierarchical report:
- LEVEL 1: TEST SUITE (Module or Feature Group)
- LEVEL 2: TEST SCENARIO (Business Scenario / Flow)
- LEVEL 3: TEST CASE (Atomic Scenario Verification)
- LEVEL 4: TEST STEPS (Detailed actions, Expected vs Actual, Screenshots)

Features:
- 5 Large KPI metrics (Tổng, Pass, Fail, Flaky, Skip).
- "Cần xử lý" action cards with 1-click jump to failure.
- Explicit visual badges for TEST SUITE and SCENARIO.
- Offline 100%, zero CDN dependencies, auto dark/light theme.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from reporting.core.sanitizer import clean_error_message


def _resolve_suite_and_scenario(t: Dict[str, Any], meta: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    Extracts (suite_name, scenario_name, tc_id, tc_title) with full 4-tier hierarchy.
    Handles both Pytest suites and Markdown-driven specs.
    """
    nodeid = t.get("nodeid", "Unknown")
    parts = nodeid.split("::")
    file_path = Path(parts[0])

    # 1. Resolve Suite Name
    suite_cand = meta.get("suite") or meta.get("user_story")
    if suite_cand and suite_cand != "Hệ thống":
        suite_name = suite_cand
    else:
        # Detect from file path
        path_str = str(file_path).lower()
        if "fs09" in path_str:
            suite_name = "Module FS09: Outstanding Fees & Payment"
        elif "fs08" in path_str:
            suite_name = "Module FS08: Parent Portal & Profile"
        elif "fs03" in path_str:
            suite_name = "Module FS03: School Student Fee Management"
        elif "us04" in path_str or "curricula" in path_str:
            suite_name = "Curricula Trainer Account Management"
        elif "us01" in path_str or "bing" in path_str:
            suite_name = "Module US01: Web Search Functionality"
        elif "break_it" in path_str:
            suite_name = "Resilience & Adversarial Quality Gate"
        elif "unit" in path_str:
            suite_name = "Architecture Invariants & Unit Tests"
        else:
            folder = file_path.parent.name
            suite_name = f"Test Suite: {folder.replace('_', ' ').title()}" if folder and folder != "." else "Test Suite: Main"

    # 2. Resolve Scenario Name
    scenario_cand = meta.get("scenario")
    if scenario_cand:
        scenario_name = scenario_cand
    elif file_path.suffix.lower() == ".md":
        # In markdown specs: parts[-1] is the scenario title
        scenario_name = parts[-1] if len(parts) > 1 else "Kịch bản chính"
    else:
        # In Pytest: file_path.stem is typically test_ts01_invoice_inquiry
        stem = file_path.stem
        m_ts = re.match(r"^test_ts(\d+)_(.*)$", stem, re.I)
        if m_ts:
            ts_num = int(m_ts.group(1))
            ts_desc = m_ts.group(2).replace("_", " ").title()
            scenario_name = f"TS-{ts_num:02d}: {ts_desc}"
        else:
            clean_stem = re.sub(r"^test_", "", stem).replace("_", " ").title()
            scenario_name = f"Scenario: {clean_stem}"

    # 3. Resolve Test Case ID & Title
    raw_func = parts[-1] if len(parts) > 1 else parts[0]
    clean_func = re.sub(r"\[.*?\]$", "", raw_func)

    id_patterns = [
        r"^test_((?:tc|ts|brk)_[a-z0-9]+_(?:auto|dt|bva|nav)_\d+[a-z]?)_(.*)$",
        r"^test_((?:tc|ts|brk)_[a-z0-9]+_api_ep)_(.*)$",
        r"^test_((?:tc|ts|brk)_[a-z0-9]+_\d+[a-z]?)_(.*)$",
        r"^test_((?:tc|ts|brk)_[a-z0-9_]+?)_(.*)$",
    ]
    tc_id = None
    clean_title = clean_func
    for pat in id_patterns:
        m_id = re.match(pat, clean_func, re.I)
        if m_id:
            tc_id = m_id.group(1).upper().replace("_", "-")
            clean_title = m_id.group(2).replace("_", " ").title()
            break

    if not tc_id:
        m_id = re.search(r"(?:test_)?((?:tc|hp|us|brk)[_-]?[a-z0-9]+(?:_[a-z0-9]+)?)", clean_func, re.I)
        if m_id:
            raw_id = m_id.group(1).upper().replace("_", "-")
            m_code = re.match(r"^([A-Z]+)(\d+.*)$", raw_id)
            tc_id = f"{m_code.group(1)}-{m_code.group(2)}" if m_code else raw_id
        else:
            tc_id = meta.get("jira_id") or "TC"
        clean_title = re.sub(r"^test_(?:tc|hp|us|brk)[_-]?[a-z0-9]+_", "", clean_func, flags=re.I)
        clean_title = re.sub(r"^test_", "", clean_title)
        clean_title = clean_title.replace("_", " ").title()

    if not clean_title or clean_title == tc_id:
        clean_title = scenario_name

    tc_title = f"{tc_id}: {clean_title}" if not clean_title.startswith(tc_id) else clean_title

    return suite_name, scenario_name, tc_id, tc_title


def build_clean_html(report_data: Dict[str, Any], title: str = "Kết quả chạy kiểm thử tự động") -> str:
    created = report_data.get("created", 0)
    import datetime
    run_time_str = datetime.datetime.fromtimestamp(created).strftime("%d/%m/%Y %H:%M:%S") if created else datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    duration_total = float(report_data.get("duration", 0.0))
    run_id = report_data.get("run_id", "RUN-LOCAL")

    raw_tests = report_data.get("tests", [])
    
    # 4-Tier Hierarchy: Suite -> Scenario -> Case -> Steps
    suite_map: Dict[str, Dict[str, List[Dict[str, Any]]]] = {}

    for t in raw_tests:
        nodeid = t.get("nodeid", "Unknown")
        outcome = t.get("outcome", "unknown").lower()
        if outcome == "passed":
            st = "pass"
        elif outcome in ("failed", "error"):
            st = "fail"
        elif outcome == "skipped":
            st = "skip"
        elif outcome in ("xfailed", "xfail"):
            st = "xfail"
        else:
            st = "flaky"

        meta = t.get("metadata", {})
        suite_name, scenario_name, tc_id, tc_title = _resolve_suite_and_scenario(t, meta)

        steps_raw = meta.get("steps", [])
        steps = []
        fail_at = None
        for idx, s in enumerate(steps_raw):
            s_title = s.get("title", f"Bước {idx + 1}")
            s_exp = s.get("expected", "")
            s_act = clean_error_message(s.get("actual", ""))
            steps.append({
                "title": s_title,
                "expected": s_exp,
                "actual": s_act,
                "status": s.get("status", "passed"),
            })
            if s.get("status") in ("failed", "xfailed") and fail_at is None:
                fail_at = idx

        if not steps:
            steps = [{
                "title": f"Thực thi kiểm thử cho {tc_title}",
                "expected": "Kiểm tra đúng theo yêu cầu FSD / AC",
                "actual": "Hoàn tất thành công",
                "status": "passed" if st == "pass" else ("xfailed" if st == "xfail" else "failed"),
            }]

        call = t.get("call", {})
        crash = call.get("crash", {})
        raw_err = crash.get("message") or call.get("longrepr") or ""
        err_msg = clean_error_message(raw_err)
        xfail_reason = meta.get("xfail_reason") or t.get("xfail_reason") or ""

        tags = meta.get("tags", [])
        if not tags and "keywords" in t:
            tags = [f"@{k}" for k in t["keywords"] if k.lower() in ("smoke", "p0", "p1", "p2", "regression", "uat", "ui", "functional", "break_it", "adversarial")]

        is_uat = meta.get("is_uat", False) or "@uat" in tags or "uat" in scenario_name.lower() or "uat" in tc_title.lower()
        is_break_it = meta.get("is_break_it", False) or "@break_it" in tags or "@break" in tags or "@adversarial" in tags or "break" in scenario_name.lower() or "brk" in tc_id.lower()
        is_integration = meta.get("is_integration", False) or "@integration" in tags or "@api" in tags or "integration" in scenario_name.lower() or "api" in scenario_name.lower()

        case_obj = {
            "id": tc_id,
            "title": tc_title,
            "st": st,
            "dur": round(float(t.get("duration", 0.0)), 2),
            "trace": meta.get("jira_id") or tc_id,
            "tags": tags,
            "is_uat": is_uat,
            "is_break_it": is_break_it,
            "is_integration": is_integration,
            "steps": steps,
            "xfail_reason": xfail_reason,
            "exp": "Tất cả các bước thực thi thành công và thỏa mãn điều kiện kiểm tra.",
        }

        if st == "xfail":
            case_obj["cat"] = "Lỗi sản phẩm đã ghi nhận (Strict XFAIL)"
            case_obj["defect"] = xfail_reason or "Known Product Defect"
            case_obj["note"] = f"Lỗi sản phẩm: {xfail_reason}" if xfail_reason else "Known Product Defect (Strict XFAIL)"
            if fail_at is not None:
                case_obj["failAt"] = fail_at
                case_obj["act"] = clean_error_message(steps[fail_at].get("actual")) or f"Xác nhận lỗi tại bước {fail_at + 1}: {steps[fail_at]['title']}"
                case_obj["err"] = err_msg or xfail_reason
        elif fail_at is not None:
            case_obj["failAt"] = fail_at
            case_obj["exp"] = steps[fail_at].get("expected") or "Hành vi giao diện và kết quả đúng như kỳ vọng theo tài liệu."
            case_obj["act"] = clean_error_message(steps[fail_at].get("actual")) or f"Phát hiện lỗi tại bước {fail_at + 1}: {steps[fail_at]['title']}"
            case_obj["err"] = err_msg or "Lỗi không xác định trong quá trình thực thi."
            case_obj["cat"] = "Lỗi giao diện / Kịch bản"
            case_obj["defect"] = "Cần kiểm tra"

        if suite_name not in suite_map:
            suite_map[suite_name] = {}
        if scenario_name not in suite_map[suite_name]:
            suite_map[suite_name][scenario_name] = []

        suite_map[suite_name][scenario_name].append(case_obj)

    suites_json_list = []
    for s_name, sc_dict in suite_map.items():
        scenarios_list = []
        for sc_name, cases in sc_dict.items():
            sc_is_uat = any(c.get("is_uat") for c in cases)
            sc_is_break_it = any(c.get("is_break_it") for c in cases)
            sc_is_integration = any(c.get("is_integration") for c in cases)
            scenarios_list.append({
                "name": sc_name,
                "cases": cases,
                "is_uat": sc_is_uat,
                "is_break_it": sc_is_break_it,
                "is_integration": sc_is_integration,
            })
        suites_json_list.append({"name": s_name, "scenarios": scenarios_list})

    suites_js_str = json.dumps(suites_json_list, ensure_ascii=False)
    run_meta_str = f"Môi trường Localhost · Run ID: {run_id} · Thời gian: {run_time_str} · Thời lượng: {duration_total:.1f}s · Chromium"

    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - {run_id}</title>
<style>
:root{{
  --bg:#f5f6f8; --card:#ffffff; --text:#172033; --muted:#5f6b80; --line:#e3e7ee;
  --pass:#0f7a3a; --pass-bg:#e4f4ea; --fail:#c1262d; --fail-bg:#fdeaea;
  --xfail:#b45309; --xfail-bg:#fffbeb; --flaky:#955c00; --flaky-bg:#fff2d6; --skip:#566074; --skip-bg:#eceff4;
  --accent:#1f56d8; --code:#f1f3f7;
}}
@media (prefers-color-scheme:dark){{
  :root{{
    --bg:#11141b; --card:#1a1f2a; --text:#eef1f7; --muted:#a0a9bb; --line:#2b3242;
    --pass:#5fd990; --pass-bg:#15301f; --fail:#ff8086; --fail-bg:#3b1c1f;
    --xfail:#f6bd4f; --xfail-bg:#3a2d12; --flaky:#f6bd4f; --flaky-bg:#3a2d12; --skip:#b0b8c8; --skip-bg:#262c39;
    --accent:#86a8ff; --code:#10131a;
  }}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
.wrap{{max-width:960px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-size:26px;line-height:1.2;margin:0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px}}
.sub{{color:var(--muted);margin:8px 0 0;font-size:15px}}
.tag{{display:inline-block;padding:2px 10px;border-radius:6px;background:var(--pass-bg);color:var(--pass);font-size:13px;font-weight:700}}
h2{{font-size:19px;margin:36px 0 14px;display:flex;align-items:center;gap:8px}}

/* số liệu */
.nums{{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-top:22px}}
@media (max-width:600px){{.nums{{grid-template-columns:repeat(3,1fr)}}}}
.num{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}}
.num b{{display:block;font-size:36px;line-height:1.1}}
.num span{{font-size:14px;color:var(--muted);font-weight:600}}
.num.pass b{{color:var(--pass)}} .num.fail b{{color:var(--fail)}} .num.xfail b{{color:var(--xfail)}} .num.flaky b{{color:var(--flaky)}} .num.skip b{{color:var(--skip)}}
.bar{{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--skip-bg);margin-top:16px}}
.bar i{{display:block;height:100%}}
.bar .pass{{background:var(--pass)}} .bar .fail{{background:var(--fail)}} .bar .xfail{{background:var(--xfail)}} .bar .flaky{{background:var(--flaky)}} .bar .skip{{background:var(--skip)}}
.verdict{{margin:16px 0 0;font-size:17px;font-weight:600}}

/* nhãn trạng thái */
.st{{display:inline-block;min-width:76px;text-align:center;padding:3px 10px;border-radius:6px;font-size:13px;font-weight:700}}
.st.pass{{background:var(--pass-bg);color:var(--pass)}} .st.fail{{background:var(--fail-bg);color:var(--fail)}}
.st.xfail{{background:var(--xfail-bg);color:var(--xfail)}} .st.flaky{{background:var(--flaky-bg);color:var(--flaky)}} .st.skip{{background:var(--skip-bg);color:var(--skip)}}
.id{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px;color:var(--muted);font-weight:600}}

/* badge cấp bậc */
.badge-suite{{display:inline-block;padding:2px 8px;border-radius:6px;background:var(--accent);color:#fff;font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;margin-right:8px;vertical-align:middle}}
.badge-scn{{display:inline-block;padding:2px 7px;border-radius:5px;background:var(--code);border:1px solid var(--line);color:var(--muted);font-size:11px;font-weight:700;letter-spacing:0.03em;text-transform:uppercase;margin-right:6px}}
.badge-atomic{{display:inline-block;padding:2px 8px;border-radius:6px;background:#0284c7;color:#fff;font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;margin-right:6px;vertical-align:middle}}
.badge-integration{{display:inline-block;padding:2px 8px;border-radius:6px;background:#f59e0b;color:#fff;font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;margin-right:6px;vertical-align:middle}}
.badge-uat{{display:inline-block;padding:2px 8px;border-radius:6px;background:#8b5cf6;color:#fff;font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;margin-right:6px;vertical-align:middle}}
.badge-break-it{{display:inline-block;padding:2px 8px;border-radius:6px;background:#f43f5e;color:#fff;font-size:11px;font-weight:800;letter-spacing:0.06em;text-transform:uppercase;margin-right:6px;vertical-align:middle}}
.tag-pill{{display:inline-block;padding:1px 6px;border-radius:4px;background:var(--code);border:1px solid var(--line);color:var(--accent);font-size:11px;font-family:ui-monospace,Menlo,Consolas,monospace;font-weight:600;margin-left:6px}}

/* cần xử lý */
.todo{{display:grid;gap:10px}}
.todo-item{{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--fail);border-radius:10px;padding:12px 16px;display:flex;gap:12px;align-items:center;justify-content:space-between;flex-wrap:wrap}}
.todo-item.xfail{{border-left-color:var(--xfail)}}
.todo-item.flaky{{border-left-color:var(--flaky)}}
.todo-item .t{{font-weight:600}}
.todo-item .why{{color:var(--muted);font-size:14px;margin-top:2px}}
.go{{background:var(--accent);color:#fff;border:0;border-radius:8px;padding:8px 16px;font:inherit;font-size:14px;font-weight:600;cursor:pointer}}

/* bộ lọc */
.tools{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px}}
.pill{{background:var(--card);border:1px solid var(--line);color:var(--text);border-radius:999px;padding:6px 16px;font:inherit;font-size:14px;cursor:pointer;font-weight:500}}
.pill[aria-pressed="true"]{{background:var(--text);color:var(--bg);border-color:var(--text);font-weight:700}}
.search{{flex:1;min-width:200px;background:var(--card);color:var(--text);border:1px solid var(--line);border-radius:999px;padding:7px 16px;font:inherit;font-size:14px}}

/* danh sách suite & scenario */
.suite{{margin-top:30px;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}}
.suite h3{{font-size:18px;margin:0 0 14px;display:flex;justify-content:space-between;gap:10px;align-items:center;padding-bottom:12px;border-bottom:2px solid var(--line)}}
.suite h3 small{{font-size:13px;color:var(--muted);font-weight:700;background:var(--bg);padding:3px 10px;border-radius:999px}}
.scn{{margin-top:18px}}
.scn h4{{font-size:15px;color:var(--text);margin:0 0 8px;font-weight:600;display:flex;align-items:center}}
.list{{background:var(--bg);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
details.case+details.case{{border-top:1px solid var(--line)}}
details.case>summary{{list-style:none;cursor:pointer;display:flex;align-items:center;gap:14px;padding:12px 14px;flex-wrap:wrap}}
details.case>summary::-webkit-details-marker{{display:none}}
details.case>summary:hover{{background:var(--code)}}
details.case>summary .id{{width:120px;flex:none}}
details.case>summary .ti{{flex:1;min-width:220px;font-weight:500}}
details.case>summary .du{{color:var(--muted);font-size:13px;font-weight:600}}
details.case>summary::after{{content:"›";color:var(--muted);font-size:20px;line-height:1;transition:transform .15s}}
details.case[open]>summary::after{{transform:rotate(90deg)}}

/* chi tiết */
.detail{{padding:12px 16px 20px;display:grid;gap:16px;background:var(--card);border-top:1px dashed var(--line)}}
.detail h5{{margin:0 0 6px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}}
ol.steps{{margin:0;padding:0;list-style:none;display:grid;gap:8px}}
ol.steps li{{display:flex;gap:10px;align-items:baseline}}
ol.steps .m{{flex:none;width:20px;font-weight:700;text-align:center}}
ol.steps .ok .m{{color:var(--pass)}} ol.steps .bad .m{{color:var(--fail)}} ol.steps .no .m{{color:var(--skip)}}
ol.steps .bad{{font-weight:700;color:var(--fail)}} ol.steps .no{{color:var(--muted)}}
.two{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
@media (max-width:640px){{.two{{grid-template-columns:1fr}}}}
.box{{border-radius:10px;padding:12px 14px}}
.box.exp{{background:var(--pass-bg);color:var(--pass)}} .box.act{{background:var(--fail-bg);color:var(--fail)}}
.box h5{{color:inherit;opacity:.9}}
pre{{margin:0;background:var(--code);border:1px solid var(--line);border-radius:8px;padding:12px 14px;font:13px/1.55 ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;word-break:break-word;color:var(--text)}}
.foot{{color:var(--muted);font-size:14px;border-top:1px solid var(--line);padding-top:10px}}
.foot b{{color:var(--text)}}
.hide{{display:none !important}}
.empty{{color:var(--muted);text-align:center;padding:24px;background:var(--card);border-radius:10px;border:1px dashed var(--line)}}
</style>
</head>
<body>
<div class="wrap">

  <h1>{title} <span class="tag">Báo Cáo Tinh Gọn</span></h1>
  <p class="sub" id="sub"></p>

  <div class="nums" id="nums"></div>
  <div class="bar" id="bar"></div>
  <p class="verdict" id="verdict"></p>

  <h2>⚠️ Cần Xử Lý</h2>
  <div class="todo" id="todo"></div>

  <h2>📋 Danh Sách Test Suites & Scenarios</h2>
  <div class="tools" id="tools">
    <button class="pill" data-f="all" aria-pressed="true">Tất cả</button>
    <button class="pill" data-f="fail" aria-pressed="false">Fail</button>
    <button class="pill" data-f="xfail" aria-pressed="false">XFailed (Bugs)</button>
    <button class="pill" data-f="flaky" aria-pressed="false">Flaky</button>
    <button class="pill" data-f="skip" aria-pressed="false">Skip</button>
    <button class="pill" data-f="pass" aria-pressed="false">Pass</button>
    <input class="search" id="q" type="search" placeholder="Tìm theo ID, tên test hoặc suite…" aria-label="Tìm test case">
  </div>
  <div id="tree"></div>
  <div class="empty hide" id="none">Không có test case nào khớp.</div>

</div>

<script>
(function(){{
  var run = "{run_meta_str}";
  var suites = {suites_js_str};
  var NAME = {{pass:"✔ PASS", fail:"✘ FAIL", xfail:"⚠ XFAIL (LỖI ĐÃ BIẾT)", flaky:"⚠ FLAKY", skip:"– SKIP"}};

  function esc(s){{
    return String(s||"").replace(/[&<>"']/g, function(c){{
      return {{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}}[c];
    }});
  }}
  function st(s){{ return '<span class="st '+s+'">'+NAME[s]+'</span>'; }}
  function dur(d){{ return d ? d.toFixed(1)+"s" : ""; }}

  var all = [];
  suites.forEach(function(s){{ s.scenarios.forEach(function(x){{ x.cases.forEach(function(c){{ all.push(c); }}); }}); }});
  var n = {{pass:0, fail:0, xfail:0, flaky:0, skip:0}};
  all.forEach(function(c){{ n[c.st] = (n[c.st]||0) + 1; }});
  var total = all.length, executed = total - (n.skip||0);
  var rate = executed ? Math.round(n.pass/executed*1000)/10 : 0;

  document.getElementById("sub").textContent = run;

  // số liệu lớn
  var cards = [["", total, "Tổng"],["pass", n.pass||0, "Pass"],["fail", n.fail||0, "Fail"]];
  if (n.xfail) cards.push(["xfail", n.xfail||0, "XFailed (Bugs)"]);
  if (n.flaky) cards.push(["flaky", n.flaky||0, "Flaky"]);
  cards.push(["skip", n.skip||0, "Skip"]);
  document.getElementById("nums").innerHTML = cards.map(function(c){{
    return '<div class="num '+c[0]+'"><b>'+c[1]+'</b><span>'+c[2]+'</span></div>';
  }}).join("");
  document.getElementById("bar").innerHTML = ["pass","fail","xfail","flaky","skip"].map(function(k){{
    return n[k] ? '<i class="'+k+'" style="width:'+((n[k]/total)*100)+'%"></i>' : "";
  }}).join("");
  document.getElementById("verdict").textContent =
    (n.fail ? n.fail+" test lỗi chưa đạt (Failed). " : "") +
    (n.xfail ? n.xfail+" lỗi sản phẩm đã xác nhận (XFailed). " : "") +
    (n.fail === 0 && n.xfail === 0 ? "Tất cả test cases đều đạt chuẩn (100% Passed). " : "") +
    "Tỷ lệ pass "+rate+"% (tính trên "+executed+" test đã chạy).";

  // cần xử lý
  var todoList = all.filter(function(c){{return c.st==="fail";}}).concat(all.filter(function(c){{return c.st==="xfail";}})).concat(all.filter(function(c){{return c.st==="flaky";}}));
  document.getElementById("todo").innerHTML = todoList.length ? todoList.map(function(c){{
    var why = c.xfail_reason ? ("Lỗi sản phẩm đã ghi nhận (Strict XFAIL): " + c.xfail_reason) : ((c.failAt!=null) ? ("Lỗi ở bước "+(c.failAt+1)+": "+(c.steps[c.failAt].title||c.steps[c.failAt])) : (c.note||"Kiểm tra log thực thi"));
    return '<div class="todo-item '+c.st+'">'+
      '<div><div class="t">'+st(c.st)+' &nbsp;'+esc(c.title)+' <span class="id">'+esc(c.id)+'</span></div>'+
      '<div class="why">'+esc(why)+'</div></div>'+
      '<button class="go" data-jump="'+esc(c.id)+'">Xem chi tiết</button></div>';
  }}).join("") : '<div class="empty">Không có lỗi nào cần xử lý. Toàn bộ kịch bản đều vượt qua!</div>';

  // chi tiết
  function detail(c){{
    var h = '<div class="detail">';
    h += '<div><h5>Các bước thực thi (Test Steps)</h5><ol class="steps">'+c.steps.map(function(s,i){{
      var stepTitle = typeof s === "object" ? s.title : s;
      var cls="ok", m="✔";
      if(c.st==="skip"){{cls="no"; m="–";}}
      else if(c.failAt!=null){{
        if(i===c.failAt){{cls="bad"; m="✘";}}
        else if(i>c.failAt){{cls="no"; m="–";}}
      }}
      return '<li class="'+cls+'"><span class="m">'+m+'</span><span>'+esc(stepTitle)+'</span></li>';
    }}).join("")+'</ol></div>';
    if(c.st==="fail" || c.st==="xfail"){{
      var errTitle = c.st==="xfail" ? "Chi tiết lỗi sản phẩm (Known Bug / Strict XFAIL)" : "Thông báo lỗi chi tiết";
      h += '<div class="two"><div class="box exp"><h5>Kỳ vọng (Expected)</h5>'+esc(c.exp)+'</div><div class="box act"><h5>Thực tế (Actual)</h5>'+esc(c.act)+'</div></div>';
      h += '<div><h5>'+errTitle+'</h5><pre>'+esc(c.err)+'</pre></div>';
    }} else {{
      h += '<div><h5>Kết quả kỳ vọng</h5><div class="box exp">'+esc(c.exp)+'</div></div>';
      if(c.note) h += '<div><h5>Ghi chú</h5>'+esc(c.note)+'</div>';
    }}
    var f = [];
    if(c.trace) f.push('Mã kịch bản: <b>'+esc(c.trace)+'</b>');
    if(c.cat)   f.push('Phân loại: <b>'+esc(c.cat)+'</b>');
    if(f.length) h += '<div class="foot">'+f.join(" &nbsp;·&nbsp; ")+'</div>';
    return h+'</div>';
  }}
  function cnt(cases){{
    var p = cases.filter(function(c){{return c.st==="pass";}}).length;
    return p+"/"+cases.length+" pass";
  }}
  document.getElementById("tree").innerHTML = suites.map(function(s){{
    var cs = []; s.scenarios.forEach(function(x){{ cs = cs.concat(x.cases); }});
    return '<section class="suite">'+
      '<h3><div><span class="badge-suite">TEST SUITE</span> '+esc(s.name)+'</div><small>'+cnt(cs)+'</small></h3>'+
      s.scenarios.map(function(x){{
        var scnBadge = x.is_break_it ? '<span class="badge-break-it">💥 BREAK_IT</span>' : (x.is_integration ? '<span class="badge-integration">🔗 INTEGRATION</span>' : (x.is_uat ? '<span class="badge-uat">🚀 UAT JOURNEY</span>' : '<span class="badge-atomic">⚡ ATOMIC</span>'));
        return '<div class="scn">'+
          '<h4>' + scnBadge + esc(x.name) + '</h4>'+
          '<div class="list">'+
          x.cases.map(function(c){{
            var tagsHtml = (c.tags||[]).map(function(t){{ return '<span class="tag-pill">'+esc(t)+'</span>'; }}).join("");
            return '<details class="case" id="case-'+esc(c.id)+'" data-st="'+c.st+'" data-t="'+esc((s.name+" "+x.name+" "+c.id+" "+c.title+" "+(c.tags||[]).join(" ")).toLowerCase())+'">'+
              '<summary>'+st(c.st)+'<span class="id">'+esc(c.id)+'</span><span class="ti">'+esc(c.title)+tagsHtml+'</span><span class="du">'+dur(c.dur)+'</span></summary>'+
              detail(c)+'</details>';
          }}).join("")+'</div></div>';
      }}).join("")+'</section>';
  }}).join("");

  // lọc và tìm
  var treeEl = document.getElementById("tree");
  var state = {{f:"all", q:""}};
  function apply(){{
    var any = false;
    Array.prototype.forEach.call(treeEl.querySelectorAll("details.case"), function(el){{
      var ok = (state.f==="all" || el.getAttribute("data-st")===state.f) &&
               (!state.q || el.getAttribute("data-t").indexOf(state.q)!==-1);
      el.classList.toggle("hide", !ok);
      if(ok) any = true;
    }});
    Array.prototype.forEach.call(treeEl.querySelectorAll(".scn"), function(el){{
      el.classList.toggle("hide", !el.querySelector("details.case:not(.hide)"));
    }});
    Array.prototype.forEach.call(treeEl.querySelectorAll(".suite"), function(el){{
      el.classList.toggle("hide", !el.querySelector("details.case:not(.hide)"));
    }});
    document.getElementById("none").classList.toggle("hide", any);
  }}
  function setPills(f){{
    Array.prototype.forEach.call(document.querySelectorAll(".pill"), function(b){{
      b.setAttribute("aria-pressed", b.getAttribute("data-f")===f ? "true" : "false");
    }});
  }}
  document.getElementById("tools").addEventListener("click", function(e){{
    var b = e.target.closest("button[data-f]");
    if(!b) return;
    state.f = b.getAttribute("data-f");
    setPills(state.f);
    apply();
  }});
  document.getElementById("q").addEventListener("input", function(e){{
    state.q = e.target.value.trim().toLowerCase();
    apply();
  }});

  // nhảy tới test case
  document.getElementById("todo").addEventListener("click", function(e){{
    var b = e.target.closest("button[data-jump]");
    if(!b) return;
    state.f = "all"; state.q = "";
    document.getElementById("q").value = "";
    setPills("all");
    apply();
    var el = document.getElementById("case-"+b.getAttribute("data-jump"));
    if(!el) return;
    el.open = true;
    el.scrollIntoView({{behavior:"smooth", block:"center"}});
  }});
}})();
</script>
</body>
</html>"""


def generate_clean_report(json_path: Path, output_html_path: Optional[Path] = None) -> Path:
    """Reads report.json and outputs the minimalist HTML report."""
    if not json_path.exists():
        raise FileNotFoundError(f"Report JSON not found: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    out_path = output_html_path or json_path.parent / "bao_cao_tinh_gon.html"
    html_content = build_clean_html(data)
    out_path.write_text(html_content, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import sys
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("reports/report.json")
    dst = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    res = generate_clean_report(src, dst)
    print(f"✓ Minimalist Clean Report generated: {res}")

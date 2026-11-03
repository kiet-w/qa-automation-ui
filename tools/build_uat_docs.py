import json
import os
import shutil
from collections import Counter

UAT_DIR = 'uat'

with open(f'{UAT_DIR}/json/tests.json', 'r', encoding='utf-8') as f:
    tests_data = json.load(f)

with open(f'{UAT_DIR}/json/timeline.json', 'r', encoding='utf-8') as f:
    timeline_data = json.load(f)

with open(f'{UAT_DIR}/json/gates.json', 'r', encoding='utf-8') as f:
    gates_data = json.load(f)

with open(f'{UAT_DIR}/json/test_data.json', 'r', encoding='utf-8') as f:
    test_data = json.load(f)

with open(f'{UAT_DIR}/json/readiness.json', 'r', encoding='utf-8') as f:
    readiness_data = json.load(f)

with open(f'{UAT_DIR}/json/team.json', 'r', encoding='utf-8') as f:
    team_data = json.load(f)

cases = tests_data['cases']

def status_badge(status):
    s = status.strip()
    if s == 'Pass':
        return '🟢 **Pass**'
    elif s == 'Fail':
        return '🔴 **Fail**'
    elif s == 'Blocked':
        return '🚫 **Blocked**'
    elif s == 'In Progress':
        return '🟡 **In Progress**'
    elif s == 'Not Run':
        return '⚪ **Not Run**'
    return f'**{s}**'

def md_escape(text):
    if not text:
        return ''
    return text.replace('|', '\\|').replace('\n', '<br>')

# 1. Generate uat/TESTS.md
with open(f'{UAT_DIR}/TESTS.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Danh Sách Chi Tiết 61 Test Cases\n\n')
    f.write(f'> {tests_data["description"]}\n\n')
    f.write('| STT | Mã UAT | Tên Kịch Bản | Phân Hệ (Area) | Người Phụ Trách | Vai Trò (Role) | Trạng Thái | Setup & Gate | Kết Quả Thực Tế | Bằng Chứng / Defect |\n')
    f.write('| :---: | :--- | :--- | :--- | :---: | :--- | :---: | :--- | :--- | :--- |\n')
    for i, c in enumerate(cases, 1):
        st = status_badge(c['Status'])
        f.write(f"| {i} | **{c['ID']}** | {md_escape(c['Test'])} | `{c['Area']}` | {c['Owner']} | {md_escape(c['Role'])} | {st} | {md_escape(c['Setup, data and gate'])} | {md_escape(c['Actual result'])} | {md_escape(c['Evidence or defect'])} |\n")

# 2. Generate uat/TIMELINE.md
with open(f'{UAT_DIR}/TIMELINE.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Kế Hoạch Tiến Độ (Timeline)\n\n')
    f.write(f'> {timeline_data["description"]}\n\n')
    f.write('| Thời Gian (When) | Cột Mốc (Milestone) | Phụ Trách (Owner) | Điều Kiện Hoàn Thành (Done When) | Trạng Thái |\n')
    f.write('| :--- | :--- | :--- | :--- | :---: |\n')
    for item in timeline_data['items']:
        f.write(f"| **{item['When']}** | {item['Milestone']} | {item['Owner']} | {item['Done when']} | `{item['Status']}` |\n")

# 3. Generate uat/GATES.md
with open(f'{UAT_DIR}/GATES.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Cổng Kiểm Soát & Giả Định (Gates & Working Assumptions)\n\n')
    f.write(f'> {gates_data["description"]}\n\n')
    f.write('## 1. Bốn Cổng Kiểm Soát (4 Gates)\n\n')
    f.write('| Cổng (Gate) | Nội Dung Cần Quyết Định | Nguồn (From) | Phụ Trách | Các Ca Bị Ảnh Hưởng | Trạng Thái | Nghị Quyết (Resolution) |\n')
    f.write('| :---: | :--- | :---: | :--- | :--- | :---: | :--- |\n')
    for g in gates_data['gates']:
        f.write(f"| **{g['ID']}** | {md_escape(g['What must be settled'])} | {g['From']} | {g['Owner']} | `{md_escape(g['Affected tests'])}` | `{g['Status']}` | {g['Resolution']} |\n")
    f.write('\n## 2. Giả Định Đang Áp Dụng (Working Assumptions - Chưa Phê Duyệt Chính Thức)\n\n')
    for note in gates_data['working_assumptions']:
        f.write(f'- {note}\n')

# 4. Generate uat/TEST_DATA.md
with open(f'{UAT_DIR}/TEST_DATA.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — 12 Bộ Dữ Liệu Kiểm Thử (Test Data Requirements)\n\n')
    f.write(f'> {test_data["description"]}\n\n')
    f.write('| Mã Dataset | Dữ Liệu Cần Thiết | Người Chuẩn Bị | Thiết Lập (Setup) | Khôi Phục (Reset) |\n')
    f.write('| :--- | :--- | :---: | :--- | :--- |\n')
    for ds in test_data['datasets']:
        f.write(f"| **`{ds['ID']}`** | {md_escape(ds['Data needed'])} | {ds['Owner']} | {md_escape(ds['Setup'])} | {md_escape(ds['Reset'])} |\n")

# 5. Generate uat/READINESS.md
with open(f'{UAT_DIR}/READINESS.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Tiêu Chuẩn Sẵn Sàng & Nghiệm Thu (Readiness & Exit Criteria)\n\n')
    f.write(f'> {readiness_data["description"]}\n\n')
    f.write('| Mã Check | Nội Dung Kiểm Tra | Người Phụ Trách | Bằng Chứng Cần Có | Trạng Thái | Kết Quả / Ghi Chú |\n')
    f.write('| :--- | :--- | :---: | :--- | :---: | :--- |\n')
    for item in readiness_data['checks']:
        f.write(f"| **`{item['ID']}`** | {md_escape(item['Check'])} | {item['Owner']} | {md_escape(item['Evidence needed'])} | `{item['Status']}` | {md_escape(item['Result or notes'])} |\n")

# 6. Generate uat/TEAM.md
with open(f'{UAT_DIR}/TEAM.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Phân Công Đội Ngũ & Kiểm Thử Chéo (Team & Peer Review)\n\n')
    f.write(f'> {team_data["description"]}\n\n')
    f.write('| Thành Viên | Phạm Vi Phụ Trách (Test Area) | Người Phản Biện (Reviewer) |\n')
    f.write('| :--- | :--- | :--- |\n')
    for mem in team_data['team']:
        f.write(f"| **{mem['Person']}** | {mem['Test area']} | **{mem['Reviewer']}** |\n")

# 7. Generate Area submodules in uat/modules/
area_map = {
    'EA lifecycle': ('01_ea_lifecycle', 'Vòng Đời Tài Khoản Giáo Dục (Education Account)'),
    'Parent access and results': ('02_parent_access_and_results', 'Cổng Phụ Huynh & Tra Cứu Kết Quả'),
    'School setup': ('03_school_setup', 'Thiết Lập Dữ Liệu Trường & Học Sinh'),
    'Fees and payments': ('04_fees_and_payments', 'Học Phí, Biểu Phí & Thanh Toán'),
    'Top-up': ('05_top_up', 'Nạp Tiền Vào Tài Khoản Giáo Dục (Top-Up)'),
    'FAS submission': ('06_fas_submission', 'Nộp Hồ Sơ Trợ Cấp Tài Chính (FAS Submission)'),
    'FAS assessment': ('07_fas_assessment', 'Đánh Giá & Phê Duyệt Hồ Sơ Trợ Cấp (FAS Assessment)'),
    'Budget and statistics': ('08_budget_and_statistics', 'Ngân Sách & Thống Kê MOE / Trường'),
    'Access and help': ('09_access_and_help', 'Quyền Truy Cập, View As & Trợ Giúp FAQ'),
    'End-to-end': ('10_end_to_end', 'Hành Trình Nghiệp Vụ Xuyên Suốt (End-to-End Journeys)')
}

for area_name, (folder, vi_title) in area_map.items():
    area_cases = [c for c in cases if c['Area'] == area_name]
    dir_path = os.path.join(UAT_DIR, 'modules', folder)
    os.makedirs(dir_path, exist_ok=True)
    with open(os.path.join(dir_path, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(f'# Phân Hệ: {vi_title} ({area_name})\n\n')
        f.write(f'Tổng số: **{len(area_cases)}** test cases.\n\n')
        f.write('| STT | Mã UAT | Tên Kịch Bản | Vai Trò | Người Phụ Trách | Trạng Thái | Kết Quả Thực Tế |\n')
        f.write('| :---: | :--- | :--- | :--- | :---: | :---: | :--- |\n')
        for i, c in enumerate(area_cases, 1):
            short_res = c['Actual result'][:120] + ('...' if len(c['Actual result']) > 120 else '')
            f.write(f"| {i} | **{c['ID']}** | {md_escape(c['Test'])} | {md_escape(c['Role'])} | {c['Owner']} | {status_badge(c['Status'])} | {md_escape(short_res)} |\n")
        f.write('\n## Chi Tiết Từng Kịch Bản\n\n')
        for c in area_cases:
            f.write(f"### {c['ID']} — {c['Test']}\n\n")
            f.write(f"- **Phân hệ:** `{c['Area']}`\n")
            f.write(f"- **Phụ trách:** {c['Owner']}\n")
            f.write(f"- **Vai trò:** {c['Role']}\n")
            f.write(f"- **Trạng thái:** {status_badge(c['Status'])}\n\n")
            f.write(f"#### 1. Setup, Data & Gate\n```\n{c['Setup, data and gate']}\n```\n\n")
            f.write(f"#### 2. Các Bước Thực Hiện & Kết Quả Kỳ Vọng (Steps & Expected Results)\n```\n{c['Steps and expected results']}\n```\n\n")
            f.write(f"#### 3. Kết Quả Thực Tế (Actual Result)\n```\n{c['Actual result']}\n```\n\n")
            f.write(f"#### 4. Bằng Chứng / Defect (Evidence / Defect)\n```\n{c['Evidence or defect']}\n```\n\n---\n\n")

# 8. Generate Master uat/README.md
status_counts = Counter(c['Status'] for c in cases)
owner_counts = Counter(c['Owner'] for c in cases)

with open(f'{UAT_DIR}/README.md', 'w', encoding='utf-8') as f:
    f.write('# Sprint 3 UAT — Kế Hoạch & Ma Trận Kiểm Thử Nghiệm Thu Người Dùng (UAT Master)\n\n')
    f.write('> **Nguồn dữ liệu:** Đồng bộ trực tiếp từ Google Spreadsheet chính thức Sprint 3 UAT: essential test plan.\n')
    f.write('> **Tổng số kịch bản:** 61 kịch bản kiểm thử bao phủ toàn bộ 10 phân hệ nghiệp vụ Sprint 1, Sprint 2 và các tính năng mở rộng.\n\n')
    f.write('## 1. Bảng Chỉ Số Tổng Quan (Executive Summary)\n\n')
    f.write(f'- 🟢 **Đạt (Pass):** {status_counts.get("Pass", 0)} ca\n')
    f.write(f'- 🔴 **Không Đạt (Fail):** {status_counts.get("Fail", 0)} ca\n')
    f.write(f'- 🟡 **Đang Thực Hiện (In Progress):** {status_counts.get("In Progress", 0)} ca\n')
    f.write(f'- 🚫 **Bị Chặn (Blocked):** {status_counts.get("Blocked", 0)} ca\n')
    f.write(f'- ⚪ **Chưa Chạy (Not Run):** {status_counts.get("Not Run", 0)} ca\n')
    f.write(f'- 📊 **Tổng Cộng:** **{len(cases)}** test cases\n\n')
    f.write('## 2. Phân Bổ Theo 10 Phân Hệ Nghiệp Vụ (10 UAT Areas)\n\n')
    f.write('| STT | Phân Hệ Nghiệp Vụ (Area) | Tên Tiếng Việt | Số Ca | Thư Mục Chi Tiết |\n')
    f.write('| :---: | :--- | :--- | :---: | :--- |\n')
    for i, (area_name, (folder, vi_title)) in enumerate(area_map.items(), 1):
        count = sum(1 for c in cases if c['Area'] == area_name)
        f.write(f"| {i} | `{area_name}` | {vi_title} | **{count}** | [`modules/{folder}`](modules/{folder}/README.md) |\n")
    f.write('\n## 3. Phân Công Trách Nhiệm Nhân Sự (Team Allocation)\n\n')
    f.write('| Thành Viên | Số Ca Phụ Trách | Phân Hệ Chính | Reviewer |\n')
    f.write('| :--- | :---: | :--- | :--- |\n')
    for mem in team_data['team']:
        p = mem['Person']
        c_cnt = sum(1 for c in cases if c['Owner'].lower() == p.lower())
        f.write(f"| **{p}** | **{c_cnt}** ca | {mem['Test area']} | **{mem['Reviewer']}** |\n")
    f.write('\n## 4. Mục Lục Tài Liệu Cấu Thành Bộ UAT\n\n')
    f.write('- 📑 **[MASTER_UAT_SPRINT_3.xlsx](MASTER_UAT_SPRINT_3.xlsx)**: File Excel gốc nguyên bản tải từ Google Spreadsheet\n')
    f.write('- 📋 **[TESTS.md](TESTS.md)**: Danh sách đầy đủ 61 test cases 10 cột\n')
    f.write('- ⏱️ **[TIMELINE.md](TIMELINE.md)**: Kế hoạch mốc thời gian thực thi nội bộ & bàn giao khách hàng\n')
    f.write('- 🚪 **[GATES.md](GATES.md)**: 4 Cổng kiểm soát (G1-G4) & các giả định kỹ thuật D05-D09\n')
    f.write('- 💾 **[TEST_DATA.md](TEST_DATA.md)**: 12 bộ dữ liệu test (DATA-ROLES, DATA-LIFE, DATA-CSV, v.v.)\n')
    f.write('- ✅ **[READINESS.md](READINESS.md)**: 10 điều kiện sẵn sàng vào UAT (READY-01..10) và 3 điều kiện nghiệm thu (EXIT-01..03)\n')
    f.write('- 👥 **[TEAM.md](TEAM.md)**: Bảng phân công vai trò và người review chéo\n')
    f.write('- 📦 **[json/](json/)**: Dữ liệu JSON chuẩn hóa cho hệ thống script và máy đọc\n\n')

print('All markdown and modules generated successfully!')

import json
from pathlib import Path

data = {
    "xss_payloads": [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>",
        "\"><svg onload=alert(document.cookie)>",
        "<details open ontoggle=alert(1)>",
        "<iframe src=\"javascript:alert(1)\"></iframe>"
    ],
    "injection_payloads": [
        "' OR 1=1--",
        "'; DROP TABLE users; --",
        "\" OR \"\"=\"",
        "{{7*7}}",
        "${7*7}",
        "=1+1",
        "@SUM(1+1)*cmd|' /C calc'!A0",
        "-1+1"
    ],
    "special_characters_and_whitespace": [
        "",
        "   ",
        "\t\t\n\r\n",
        "   leading space",
        "trailing space   ",
        "null\u0000byte",
        "' \" < > & % \\ / ; : [ ] { } | ` ~ ! @ # $ ^ * ( ) _ + =",
        "𝕿𝖍𝖊 𝖖𝖚𝖎𝖈𝖐 𝖇𝖗𝖔𝖜𝖓 𝖋𝖔𝖝",
        "🚀🔥🎉✨🤖💡🚨🏆",
        "﷽",
        "اللغة العربية (RTL test string)",
        "עִבְרִית (Hebrew RTL test string)",
        "日本語・한국어・中文 (CJK Unified Ideographs)"
    ],
    "vietnamese_diacritics": [
        "Nguyễn Thị Ánh Tuyết",
        "Nguye\u0303n Thi\u0323 A\u0301nh Tuye\u0301t",
        "Đặng Vũ Cảnh Toàn",
        "Đa\u0323ng Vu\u0303 Ca\u0309nh Toa\u0300n"
    ],
    "boundary_numbers": [
        -999999999,
        -1,
        0,
        0.0001,
        0.1,
        0.2,
        0.30000000000000004,
        100000.0,
        0.00001,
        999999999999999,
        "0,5",
        "1.000.000,50"
    ],
    "boundary_dates": [
        "2026-02-29",
        "2024-02-29",
        "2026-04-31",
        "1970-01-01",
        "1800-12-31",
        "2099-12-31",
        "9999-12-31"
    ],
    "malformed_emails": [
        "plainaddress",
        "#@%^%#$@#$@#.com",
        "@example.com",
        "Joe Smith <email@example.com>",
        "email.example.com",
        "email@example@example.com",
        ".email@example.com",
        "email.@example.com",
        "email..email@example.com",
        "email@example",
        "email@-example.com"
    ],
    "malformed_phones": [
        "0000000",
        "1234",
        "+65abc123",
        "99999999999999999999",
        "--++--",
        "       "
    ],
    "boundary_lengths": {
        "zero_length": "",
        "max_length_plus_one_256": "A" * 256,
        "extreme_overflow_10k": "B" * 10000
    }
}

Path("data/naughty_strings.json").write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
print("Successfully generated data/naughty_strings.json")

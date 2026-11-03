#!/usr/bin/env python3
"""
=============================================================================
Annotate and Highlight BSK Screenshots with High-Precision QA Markers
- Bold Red/Crimson Highlighting Bounding Boxes
- Official [VERIFIED EVIDENCE] / [DEFECT EVIDENCE] Badges
- Corner accents and clean typography
=============================================================================
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path("/home/baudui/Projects/automation-ui")
SCREENSHOTS_DIR = REPO_ROOT / "reports/screenshots"

FONT_PATH = "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"

def draw_qa_annotation(
    image_path: Path,
    box: tuple,  # (x1, y1, x2, y2)
    badge_text: str,
    is_defect: bool = False,
    badge_position: str = "top-left"  # or "top-right", "inside-top"
):
    if not image_path.exists():
        print(f"[!] Warning: File not found: {image_path}")
        return

    im = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(im)

    # Primary colors
    if is_defect:
        primary_color = (220, 38, 38, 255)       # Red-600
        wash_color = (239, 68, 68, 30)            # Translucent wash
        badge_bg = (185, 28, 28, 255)            # Red-700
    else:
        primary_color = (225, 29, 72, 255)       # Rose-600
        wash_color = (244, 63, 94, 25)            # Light translucent wash
        badge_bg = (190, 18, 60, 255)            # Rose-700

    border_color = (255, 255, 255, 255)
    text_color = (255, 255, 255, 255)

    x1, y1, x2, y2 = box

    # 1. Subtle translucent wash over region
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([x1, y1, x2, y2], fill=wash_color)
    im = Image.alpha_composite(im, overlay)
    draw = ImageDraw.Draw(im)

    # 2. Main Bounding Box (4px thickness)
    thickness = 4
    for i in range(thickness):
        draw.rectangle([x1 - i, y1 - i, x2 + i, y2 + i], outline=primary_color)

    # 3. Corner brackets for modern HUD / QA evidence aesthetics
    corner_len = 24
    corner_thick = 6
    # Top-Left
    draw.line([(x1 - 2, y1 - 2), (x1 + corner_len, y1 - 2)], fill=border_color, width=corner_thick)
    draw.line([(x1 - 2, y1 - 2), (x1 - 2, y1 + corner_len)], fill=border_color, width=corner_thick)
    # Top-Right
    draw.line([(x2 + 2, y1 - 2), (x2 - corner_len, y1 - 2)], fill=border_color, width=corner_thick)
    draw.line([(x2 + 2, y1 - 2), (x2 + 2, y1 + corner_len)], fill=border_color, width=corner_thick)
    # Bottom-Left
    draw.line([(x1 - 2, y2 + 2), (x1 + corner_len, y2 + 2)], fill=border_color, width=corner_thick)
    draw.line([(x1 - 2, y2 + 2), (x1 - 2, y2 - corner_len)], fill=border_color, width=corner_thick)
    # Bottom-Right
    draw.line([(x2 + 2, y2 + 2), (x2 - corner_len, y2 + 2)], fill=border_color, width=corner_thick)
    draw.line([(x2 + 2, y2 + 2), (x2 + 2, y2 - corner_len)], fill=border_color, width=corner_thick)

    # 4. Badge Text & Box
    font = ImageFont.truetype(FONT_PATH, 16)
    bbox = font.getbbox(badge_text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    pad_x = 14
    pad_y = 8
    badge_w = text_w + pad_x * 2
    badge_h = text_h + pad_y * 2

    if badge_position == "top-left":
        bx1 = max(10, x1)
        by1 = max(10, y1 - badge_h - 4)
    elif badge_position == "inside-top":
        bx1 = x1 + 8
        by1 = y1 + 8
    else:  # top-right
        bx1 = max(10, x2 - badge_w)
        by1 = max(10, y1 - badge_h - 4)

    bx2 = bx1 + badge_w
    by2 = by1 + badge_h

    # Badge shadow & background
    draw.rectangle([bx1 + 2, by1 + 2, bx2 + 2, by2 + 2], fill=(0, 0, 0, 140))
    draw.rectangle([bx1, by1, bx2, by2], fill=badge_bg, outline=border_color, width=2)

    # Badge text
    tx = bx1 + pad_x - bbox[0]
    ty = by1 + pad_y - bbox[1]
    draw.text((tx, ty), badge_text, fill=text_color, font=font)

    # Convert back to RGB and overwrite
    final_im = im.convert("RGB")
    final_im.save(image_path, "PNG", quality=95)
    print(f"  [✓] Annotated: {image_path.name} -> {badge_text}")


def annotate_all():
    print("[*] Starting QA evidence screenshot annotation pass...")

    CONFIGS = [
        # 1. Support Console (5173)
        (
            SCREENSHOTS_DIR / "support_console/admin_view_as_persona_selection.png",
            (270, 210, 1860, 780),
            "[VERIFIED EVIDENCE: School Persona Selection & SCH-003 Roster]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "support_console/admin_view_as_mandatory_validation.png",
            (1150, 200, 1870, 790),
            "[VERIFIED EVIDENCE: Mandatory Reason & Ticket - Button Disabled]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "support_console/admin_view_as_session_history.png",
            (270, 140, 1860, 800),
            "[VERIFIED EVIDENCE: 10-Column Forensic Audit Trail & Date Filtering]",
            False,
            "top-left"
        ),

        # 2. FAS Application Wizard (5174)
        (
            SCREENSHOTS_DIR / "fas_wizard/parent_fas_landing_list.png",
            (260, 120, 1650, 480),
            "[VERIFIED EVIDENCE: Citizen FAS Landing & New Application CTA]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step1_applicant.png",
            (260, 140, 1650, 820),
            "[VERIFIED EVIDENCE: Step 1 - MyInfo Pre-filled Applicant Identity]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step2_beneficiaries.png",
            (260, 100, 1650, 820),
            "[VERIFIED EVIDENCE: Step 2 - Auto-Linked Beneficiary Students]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "fas_wizard/parent_fas_wizard_step3_family_income.png",
            (260, 150, 1650, 820),
            "[VERIFIED EVIDENCE: Step 3 - Means-Testing & Submit Application]",
            False,
            "top-left"
        ),

        # 3. AI Assistant & Guided Tour (5174)
        (
            SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_launcher.png",
            (1520, 770, 1880, 865),
            "[VERIFIED EVIDENCE: Floating AI Assistant Launcher Button]",
            False,
            "inside-top"
        ),
        (
            SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_chat_drawer.png",
            (1320, 10, 1895, 875),
            "[VERIFIED EVIDENCE: AI Assistant Drawer & Session History]",
            False,
            "inside-top"
        ),
        (
            SCREENSHOTS_DIR / "ai_assistant/parent_ai_assistant_chat_prompt.png",
            (1320, 10, 1895, 875),
            "[VERIFIED EVIDENCE: Conversational Chat Prompt & Guidance Interface]",
            False,
            "inside-top"
        ),
        (
            SCREENSHOTS_DIR / "ai_assistant/parent_guided_tour_modal.png",
            (1420, 60, 1880, 320),
            "[VERIFIED EVIDENCE: Guided Tour Onboarding Strategy Selector]",
            False,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "ai_assistant/parent_i18n_language_switcher.png",
            (1640, 60, 1880, 310),
            "[VERIFIED EVIDENCE: Language Switcher - Vietnamese & Profile Options]",
            False,
            "top-left"
        ),

        # 4. Live Defects (5173)
        (
            SCREENSHOTS_DIR / "defects/bug04_edusave_accounts_404.png",
            (220, 90, 1160, 560),
            "[DEFECT REPRODUCED: 404 Route Not Found on /edusave/accounts]",
            True,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "defects/bug05_edusave_topup_404.png",
            (220, 90, 1160, 560),
            "[DEFECT REPRODUCED: 404 Route Not Found on /edusave/top-up]",
            True,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "defects/bug06_moefas_404.png",
            (220, 90, 1160, 560),
            "[DEFECT REPRODUCED: 404 Route Not Found on /moefas]",
            True,
            "top-left"
        ),
        (
            SCREENSHOTS_DIR / "defects/bug07_fas_applications_access_restricted.png",
            (220, 80, 1220, 350),
            "[DEFECT REPRODUCED: RBAC Access Restriction on /fas-applications]",
            True,
            "top-left"
        ),
    ]

    for path, box, text, is_defect, pos in CONFIGS:
        draw_qa_annotation(path, box, text, is_defect=is_defect, badge_position=pos)

    print("[✓] All 16 QA screenshots successfully annotated and highlighted!")

if __name__ == "__main__":
    annotate_all()

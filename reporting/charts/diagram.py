"""
reporting/charts/diagram.py - Pure Python Editorial Diagram Generator.

Applies the opinionated editorial design system of diagram-design:
- Pure mathematical SVG generation without external libraries, Graphviz, or CDNs.
- High-contrast editorial palette (Ink, Paper, Subtle Slate, and focused Accents).
- Strict typographic hierarchy: Sans for headings/labels, Monospace for commands/paths.
- Masked connector text (never bleeds through lines) and clean arrowheads.
- 4/10 target density: technically rigorous without visual clutter.
"""

import html
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class EditorialDiagramTheme:
    """Editorial design tokens compliant with GitHub color system & diagram-design guidelines."""

    BG_CANVAS = "var(--bg-canvas, #0d1117)"
    BG_CARD = "var(--bg-card, #161b22)"
    BG_CARD_HOVER = "var(--bg-card-hover, #1f242c)"
    BG_PILL = "var(--bg-pill, #21262d)"
    BORDER_DEFAULT = "var(--border-color, #30363d)"
    BORDER_MUTED = "var(--border-color, #30363d)"
    BORDER_FOCAL = "var(--accent-blue, #1f6feb)"
    BORDER_SUCCESS = "var(--status-pass, #3fb950)"
    BORDER_FAIL = "var(--status-fail, #f85149)"
    BORDER_WARN = "var(--status-skip, #d29922)"
    TEXT_PRIMARY = "var(--text-primary, #e6edf3)"
    TEXT_SECONDARY = "var(--text-secondary, #8b949e)"
    TEXT_MUTED = "var(--text-secondary, #8b949e)"

    # Unified GitHub signal colors
    STATUS_PASS = "var(--status-pass, #3fb950)"
    STATUS_FAIL = "var(--status-fail, #f85149)"
    STATUS_SKIP = "var(--status-skip, #d29922)"
    ACCENT_BLUE = "var(--accent-blue, #58a6ff)"
    ACCENT_BLUE_SOLID = "var(--accent-blue-solid, #1f6feb)"

    # Backward compatibility aliases
    ACCENT_CYAN = "var(--accent-blue, #58a6ff)"
    ACCENT_EMERALD = "var(--status-pass, #3fb950)"
    ACCENT_CORAL = "var(--status-fail, #f85149)"
    ACCENT_INDIGO = "var(--status-skip, #d29922)"

    FONT_SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
    FONT_MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', monospace"


def render_connector(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: Optional[str] = None,
    theme: EditorialDiagramTheme = EditorialDiagramTheme,
    dashed: bool = False,
) -> List[str]:
    """
    Renders an orthogonal or straight connector line with an arrowhead.
    Includes a background masking rect for the label to prevent line bleed-through.
    """
    elements = []
    dash_attr = ' stroke-dasharray="4,4"' if dashed else ""
    line_svg = f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2-6:.1f}" y2="{y2:.1f}" stroke="{theme.BORDER_DEFAULT}" stroke-width="1.5"{dash_attr} marker-end="url(#diag-arrow)"/>'
    elements.append(line_svg)

    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        label_len = len(label)
        mask_w = label_len * 6.5 + 14
        mask_h = 18
        elements.append(
            f'<rect x="{mid_x - mask_w/2:.1f}" y="{mid_y - mask_h/2:.1f}" width="{mask_w:.1f}" height="{mask_h}" rx="3" fill="{theme.BG_CANVAS}" stroke="{theme.BORDER_MUTED}" stroke-width="1"/>'
        )
        elements.append(
            f'<text x="{mid_x:.1f}" y="{mid_y + 3.8:.1f}" text-anchor="middle" font-family="{theme.FONT_MONO}" font-size="9.5" font-weight="600" fill="{theme.ACCENT_BLUE}">{html.escape(label)}</text>'
        )

    return elements


def generate_system_architecture_diagram_svg(
    width: int = 1060,
    height: int = 370,
    theme: EditorialDiagramTheme = EditorialDiagramTheme,
) -> str:
    """
    Generates a pure SVG End-to-End System Architecture diagram for the UI Automation framework.
    Visual Type: Architecture (Component Topology & Pipeline Flow).
    """
    svg_parts = [
        f'<svg viewBox="0 0 {width} {height}" class="editorial-diagram-svg" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background:{theme.BG_CANVAS}; border:1px solid {theme.BORDER_MUTED}; border-radius:12px; display:block;">',
        '  <defs>',
        '    <marker id="diag-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
        f'      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="{theme.TEXT_SECONDARY}"/>',
        '    </marker>',
        '    <filter id="focal-glow" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#1f6feb" flood-opacity="0.25"/>',
        '    </filter>',
        '  </defs>',
        '  <!-- Header Metadata Strip -->',
        f'  <text x="32" y="38" font-family="{theme.FONT_SANS}" font-size="15" font-weight="800" letter-spacing="0.05em" fill="{theme.TEXT_PRIMARY}">UI AUTOMATION SYSTEM ARCHITECTURE</text>',
        f'  <text x="32" y="56" font-family="{theme.FONT_MONO}" font-size="11" fill="{theme.TEXT_SECONDARY}">Playwright Engine • Brave 1080p Headed • 4-Layer Modular Report Intelligence</text>',
    ]

    # Node definitions
    nodes = [
        {
            "num": "01",
            "title": "Orchestrator",
            "subtitle": "run_tests.py / pytest",
            "details": ["pytest-xdist parallel", "CLI flag passthrough", "Live ANSI summary"],
            "badge": "CONTROLLER",
            "focal": False,
        },
        {
            "num": "02",
            "title": "Fixtures & Stealth",
            "subtitle": "conftest.py",
            "details": ["Playwright Stealth", "Brave /usr/bin/brave", "Viewport 1920x1080"],
            "badge": "BROWSER ENV",
            "focal": False,
        },
        {
            "num": "03",
            "title": "Page Objects",
            "subtitle": "pages/ & components/",
            "details": ["Page Object Model (POM)", "Modular UI Components", "Zero Assertions in POM"],
            "badge": "AUTOMATION",
            "focal": False,
        },
        {
            "num": "04",
            "title": "Evidence Store",
            "subtitle": "reports/ & artifacts",
            "details": ["1080p WebM Recordings", "Step Evidence PNGs", "Structured report.json"],
            "badge": "DELIVERABLES",
            "focal": False,
        },
        {
            "num": "05",
            "title": "Enterprise Report",
            "subtitle": "reporting/ engine",
            "details": ["Layer 1: Audit & Jira", "Layer 2: Release Gate", "Layer 4: SVG Trend Line"],
            "badge": "CORE DELIVERABLE",
            "focal": True,
        },
    ]

    num_nodes = len(nodes)
    margin_x = 32
    start_y = 88
    card_w = 168
    card_h = 220
    gap = (width - 2 * margin_x - num_nodes * card_w) / (num_nodes - 1)

    node_coords = []
    for i, n in enumerate(nodes):
        x = margin_x + i * (card_w + gap)
        y = start_y
        node_coords.append((x, y))

    # Connectors between nodes
    connector_labels = ["launches", "drives", "records", "parses & embeds"]
    for i in range(num_nodes - 1):
        x1 = node_coords[i][0] + card_w
        y1 = node_coords[i][1] + card_h / 2
        x2 = node_coords[i + 1][0]
        y2 = y1
        label = connector_labels[i] if i < len(connector_labels) else None
        conn_lines = render_connector(x1, y1, x2, y2, label=label, theme=theme)
        svg_parts.extend([f"  {c}" for c in conn_lines])

    # Render Node Cards
    for i, n in enumerate(nodes):
        x, y = node_coords[i]
        is_focal = n["focal"]
        border_col = theme.BORDER_FOCAL if is_focal else theme.BORDER_DEFAULT
        glow_filter = ' filter="url(#focal-glow)"' if is_focal else ""
        badge_bg = "rgba(31, 111, 235, 0.16)" if is_focal else theme.BG_PILL
        badge_fg = theme.ACCENT_BLUE if is_focal else theme.TEXT_MUTED
        card_bg = "#1b222d" if is_focal else theme.BG_CARD

        svg_parts.append(f'  <!-- Node {n["num"]}: {n["title"]} -->')
        svg_parts.append(f'  <g id="arch-node-{i}">')
        svg_parts.append(
            f'    <rect x="{x:.1f}" y="{y:.1f}" width="{card_w}" height="{card_h}" rx="10" fill="{card_bg}" stroke="{border_col}" stroke-width="{1.8 if is_focal else 1}"{glow_filter}/>'
        )

        # Node Header Pill Badge
        svg_parts.append(
            f'    <rect x="{x + 12:.1f}" y="{y + 12:.1f}" width="{card_w - 24}" height="20" rx="4" fill="{badge_bg}"/>'
        )
        svg_parts.append(
            f'    <text x="{x + card_w/2:.1f}" y="{y + 25.5:.1f}" text-anchor="middle" font-family="{theme.FONT_MONO}" font-size="9.5" font-weight="700" fill="{badge_fg}">{n["num"]} • {n["badge"]}</text>'
        )

        # Title & Subtitle
        svg_parts.append(
            f'    <text x="{x + 14:.1f}" y="{y + 56:.1f}" font-family="{theme.FONT_SANS}" font-size="13.5" font-weight="700" fill="{theme.TEXT_PRIMARY}">{html.escape(n["title"])}</text>'
        )
        svg_parts.append(
            f'    <text x="{x + 14:.1f}" y="{y + 74:.1f}" font-family="{theme.FONT_MONO}" font-size="10" fill="{theme.ACCENT_BLUE}">{html.escape(n["subtitle"])}</text>'
        )

        # Divider
        svg_parts.append(
            f'    <line x1="{x + 14:.1f}" y1="{y + 86:.1f}" x2="{x + card_w - 14:.1f}" y2="{y + 86:.1f}" stroke="{theme.BORDER_MUTED}" stroke-width="1"/>'
        )

        # Bullet list
        for d_idx, bullet in enumerate(n["details"]):
            b_y = y + 108 + d_idx * 24
            svg_parts.append(
                f'    <circle cx="{x + 18:.1f}" cy="{b_y - 3.5:.1f}" r="2" fill="{theme.ACCENT_BLUE if is_focal else theme.TEXT_MUTED}"/>'
            )
            svg_parts.append(
                f'    <text x="{x + 26:.1f}" y="{b_y:.1f}" font-family="{theme.FONT_SANS}" font-size="10.5" fill="{theme.TEXT_SECONDARY}">{html.escape(bullet)}</text>'
            )

        svg_parts.append("  </g>")

    # Footer note
    svg_parts.append(
        f'  <text x="{width - 32}" y="{height - 18}" text-anchor="end" font-family="{theme.FONT_MONO}" font-size="9.5" fill="{theme.TEXT_SECONDARY}">Zero CDN • Pure SVG • 100% Offline</text>'
    )
    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def generate_enterprise_layer_diagram_svg(
    width: int = 860,
    height: int = 340,
    theme: EditorialDiagramTheme = EditorialDiagramTheme,
) -> str:
    """
    Generates a pure SVG 4-Layer Enterprise Architecture stack diagram.
    Visual Type: Layer Stack (Hierarchical Audit & Decision Model).
    """
    svg_parts = [
        f'<svg viewBox="0 0 {width} {height}" class="editorial-diagram-svg" width="100%" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background:{theme.BG_CANVAS}; border:1px solid {theme.BORDER_MUTED}; border-radius:12px; display:block;">',
        '  <defs>',
        '    <marker id="diag-arrow-down" viewBox="0 0 10 10" refX="5" refY="8" markerWidth="6" markerHeight="6" orient="auto">',
        f'      <path d="M 1.5 0 L 5 8 L 8.5 0 z" fill="{theme.TEXT_SECONDARY}"/>',
        '    </marker>',
        '  </defs>',
        f'  <text x="32" y="36" font-family="{theme.FONT_SANS}" font-size="15" font-weight="800" fill="{theme.TEXT_PRIMARY}">4-LAYER ENTERPRISE QA REPORT ARCHITECTURE</text>',
        f'  <text x="32" y="54" font-family="{theme.FONT_MONO}" font-size="11" fill="{theme.TEXT_SECONDARY}">Audit Traceability • Release Gates • Root Cause Debugging • Historical Trends</text>',
    ]

    layers = [
        {
            "layer": "LAYER 1",
            "title": "Metadata & Traceability (Audit)",
            "meta": "Run ID, CI Trigger, Git Ref, Brave 1080p, Jira / Test IDs",
            "role": "AUDIT & COMPLIANCE",
            "color": theme.ACCENT_BLUE,
        },
        {
            "layer": "LAYER 2",
            "title": "Executive Summary & Release Gate",
            "meta": "Gate Verdict (READY / BLOCKED), Risk Matrix, Pass Rate Delta ▲/▼",
            "role": "C-LEVEL / QA LEAD",
            "color": theme.STATUS_PASS,
        },
        {
            "layer": "LAYER 3",
            "title": "Detailed Test Cases & Root Cause",
            "meta": "Expected vs Actual, Root Cause (Bug/Flaky/Env), Video Seek, Lightbox",
            "role": "ENGINEERING & QA",
            "color": theme.STATUS_FAIL,
        },
        {
            "layer": "LAYER 4",
            "title": "Historical Trends & Release Velocity",
            "meta": "Multi-Run SVG Progression, Run Comparison Table, history.json",
            "role": "RELEASE GOVERNANCE",
            "color": theme.STATUS_SKIP,
        },
    ]

    start_y = 74
    layer_h = 52
    gap_y = 12
    card_x = 32
    card_w = width - 64

    for i, l in enumerate(layers):
        y = start_y + i * (layer_h + gap_y)
        col = l["color"]

        svg_parts.append(f'  <!-- Layer {i+1} -->')
        svg_parts.append(f'  <g id="layer-box-{i+1}">')
        svg_parts.append(
            f'    <rect x="{card_x}" y="{y}" width="{card_w}" height="{layer_h}" rx="8" fill="{theme.BG_CARD}" stroke="{col}" stroke-width="1.2"/>'
        )
        # Left Accent indicator bar
        svg_parts.append(
            f'    <rect x="{card_x}" y="{y}" width="6" height="{layer_h}" rx="3" fill="{col}"/>'
        )
        # Layer Badge
        svg_parts.append(
            f'    <rect x="{card_x + 18}" y="{y + 12}" width="78" height="26" rx="4" fill="{theme.BG_PILL}"/>'
        )
        svg_parts.append(
            f'    <text x="{card_x + 57}" y="{y + 29}" text-anchor="middle" font-family="{theme.FONT_MONO}" font-size="10.5" font-weight="700" fill="{col}">{l["layer"]}</text>'
        )

        # Title & Meta
        svg_parts.append(
            f'    <text x="{card_x + 112}" y="{y + 24}" font-family="{theme.FONT_SANS}" font-size="13" font-weight="700" fill="{theme.TEXT_PRIMARY}">{l["title"]}</text>'
        )
        svg_parts.append(
            f'    <text x="{card_x + 112}" y="{y + 41}" font-family="{theme.FONT_MONO}" font-size="10" fill="{theme.TEXT_SECONDARY}">{l["meta"]}</text>'
        )

        # Role badge on the right
        role_w = len(l["role"]) * 7.5 + 16
        role_x = card_x + card_w - role_w - 18
        svg_parts.append(
            f'    <rect x="{role_x}" y="{y + 15}" width="{role_w}" height="22" rx="4" fill="{theme.BG_PILL}" stroke="{theme.BORDER_MUTED}" stroke-width="1"/>'
        )
        svg_parts.append(
            f'    <text x="{role_x + role_w/2}" y="{y + 29.5}" text-anchor="middle" font-family="{theme.FONT_MONO}" font-size="9" font-weight="600" fill="{theme.TEXT_SECONDARY}">{l["role"]}</text>'
        )
        svg_parts.append("  </g>")

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def generate_standalone_html(svg_content: str, title: str = "UI Automation Diagram") -> str:
    """Wraps an SVG diagram into a clean, standalone HTML page for presentation."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{
            background-color: #0d1117;
            color: #e6edf3;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 32px 16px;
        }}
        .diagram-container {{
            max-width: 1100px;
            width: 100%;
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }}
        .header {{
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        .header h1 {{ font-size: 18px; font-weight: 700; color: #e6edf3; }}
        .header span {{ font-family: monospace; font-size: 11px; color: #8b949e; }}
    </style>
</head>
<body>
    <div class="diagram-container">
        <div class="header">
            <h1>{html.escape(title)}</h1>
            <span>Pure SVG • Editorial Design System</span>
        </div>
        {svg_content}
    </div>
</body>
</html>
"""


def main():
    """CLI generator: writes standalone SVG and HTML diagrams."""
    output_dir = Path(__file__).resolve().parent.parent.parent / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)

    arch_svg = generate_system_architecture_diagram_svg()
    arch_html = generate_standalone_html(arch_svg, "UI Automation System Architecture")

    svg_file = output_dir / "system_architecture.svg"
    html_file = output_dir / "system_architecture.html"

    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(arch_svg)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(arch_html)

    layer_svg = generate_enterprise_layer_diagram_svg()
    layer_html = generate_standalone_html(layer_svg, "4-Layer Enterprise QA Architecture")
    layer_html_file = output_dir / "enterprise_layers_architecture.html"
    with open(layer_html_file, "w", encoding="utf-8") as f:
        f.write(layer_html)

    print("=" * 65)
    print("🎨 [Pure Python Editorial Diagram Generator]")
    print(f"   Architecture SVG : {svg_file}")
    print(f"   Architecture HTML: {html_file}")
    print(f"   Enterprise Layer : {layer_html_file}")
    print("✅ All diagrams generated successfully (100% offline & self-contained)!")
    print("=" * 65)


if __name__ == "__main__":
    main()

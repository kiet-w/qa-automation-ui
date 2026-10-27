"""
reporting/charts/trend.py - Pure SVG Historical Trend Chart across execution runs.
"""

import html
from typing import Any, Dict, List


def generate_trend_chart_svg(history_runs: List[Dict[str, Any]]) -> str:
    """
    Generates a pure SVG multi-run trend chart showing Pass Rate % (line + area)
    and Duration (secondary bar) across the last 5-10 test runs.
    100% offline, zero external dependencies or JavaScript libraries.
    """
    if not history_runs:
        return '<div class="no-data-hint" style="color: var(--text-secondary, #8b949e);" data-i18n="no_trend_data">No historical run data available.</div>'

    width = 620
    height = 210
    margin_left = 55
    margin_right = 55
    margin_top = 30
    margin_bottom = 45

    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    n = len(history_runs)
    if n == 1:
        history_runs = [
            {**history_runs[0], "run_id": "PREV-" + str(history_runs[0].get("run_id", "1"))[-4:]},
            history_runs[0],
        ]
        n = 2

    x_coords = []
    slot_width = plot_width / (n - 1) if n > 1 else plot_width
    for i in range(n):
        x_coords.append(margin_left + i * slot_width)

    max_duration = max((float(r.get("duration", 10.0)) for r in history_runs), default=30.0)
    if max_duration <= 0:
        max_duration = 30.0
    ceil_duration = max(round(max_duration * 1.2, 0), 10.0)

    line_points = []
    for i, r in enumerate(history_runs):
        pass_rate = float(r.get("pass_rate", 100.0))
        y = margin_top + plot_height * (1.0 - (pass_rate / 100.0))
        line_points.append((x_coords[i], y, pass_rate, r))

    pts_str = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _ in line_points)
    first_x, first_y = line_points[0][0], line_points[0][1]
    last_x, last_y = line_points[-1][0], line_points[-1][1]
    baseline_y = margin_top + plot_height

    area_path = (
        f"M {first_x:.1f},{baseline_y:.1f} "
        f"L {pts_str} "
        f"L {last_x:.1f},{baseline_y:.1f} Z"
    )
    line_path = f"M {pts_str}"

    svg_parts = [
        f'<svg viewBox="0 0 {width} {height}" class="trend-chart-svg" width="100%" height="200" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <linearGradient id="trend-area-grad" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0%" stop-color="#3fb950" stop-opacity="0.25"/>',
        '      <stop offset="100%" stop-color="#3fb950" stop-opacity="0.02"/>',
        '    </linearGradient>',
        '    <linearGradient id="trend-bar-grad" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0%" stop-color="#1f6feb" stop-opacity="0.35"/>',
        '      <stop offset="100%" stop-color="#0969da" stop-opacity="0.12"/>',
        '    </linearGradient>',
        '    <filter id="glow-dot" x="-30%" y="-30%" width="160%" height="160%">',
        '      <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000000" flood-opacity="0.35"/>',
        '    </filter>',
        '  </defs>',
    ]

    for pct in [0, 25, 50, 75, 100]:
        y = margin_top + plot_height * (1.0 - (pct / 100.0))
        svg_parts.append(
            f'  <line x1="{margin_left}" y1="{y:.1f}" x2="{width - margin_right}" y2="{y:.1f}" stroke="var(--border-color, #30363d)" stroke-dasharray="2,3" stroke-width="1"/>'
        )
        svg_parts.append(
            f'  <text x="{margin_left - 8}" y="{y + 3:.1f}" text-anchor="end" font-size="9.5" fill="var(--text-secondary, #8b949e)" font-family="monospace">{pct}%</text>'
        )
        dur_label = f"{(ceil_duration * (pct / 100.0)):.0f}s"
        svg_parts.append(
            f'  <text x="{width - margin_right + 8}" y="{y + 3:.1f}" text-anchor="start" font-size="9.5" fill="var(--text-secondary, #8b949e)" font-family="monospace">{dur_label}</text>'
        )

    svg_parts.append(
        f'  <line x1="{margin_left}" y1="{baseline_y:.1f}" x2="{width - margin_right}" y2="{baseline_y:.1f}" stroke="var(--border-color, #30363d)" stroke-width="1.5"/>'
    )

    bar_width = min(22.0, (slot_width * 0.4) if n > 1 else 30.0)
    for i, r in enumerate(history_runs):
        dur = float(r.get("duration", 0.0))
        bar_h = (dur / ceil_duration) * plot_height
        bar_x = x_coords[i] - (bar_width / 2)
        bar_y = baseline_y - bar_h
        svg_parts.append(
            f'  <rect x="{bar_x:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" height="{bar_h:.1f}" rx="3" fill="url(#trend-bar-grad)">'
            f'    <title>Run {html.escape(str(r.get("run_id", "")))}: Duration {dur:.1f}s</title>'
            f'  </rect>'
        )

    svg_parts.append(f'  <path d="{area_path}" fill="url(#trend-area-grad)"/>')
    svg_parts.append(
        f'  <path d="{line_path}" fill="none" stroke="var(--status-pass, #3fb950)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>'
    )

    for i, (x, y, pass_rate, r) in enumerate(line_points):
        run_label = str(r.get("run_id", f"#{i + 1}"))
        if len(run_label) > 10:
            run_label = run_label[:9] + "…"

        is_current = (i == n - 1)
        dot_color = "var(--status-pass, #3fb950)" if pass_rate >= 90 else ("var(--status-skip, #d29922)" if pass_rate >= 70 else "var(--status-fail, #f85149)")
        dot_r = 5.0 if is_current else 3.8

        svg_parts.append(
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{dot_r}" fill="{dot_color}" stroke="#0d1117" stroke-width="1.8" filter="url(#glow-dot)">'
            f'    <title>{html.escape(run_label)}: {pass_rate:.1f}% Pass Rate</title>'
            f'  </circle>'
        )

        label_y = y - 8 if y > margin_top + 16 else y + 14
        svg_parts.append(
            f'  <text x="{x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{dot_color}" font-family="system-ui, sans-serif">{pass_rate:.0f}%</text>'
        )

        run_name_styled = f'<tspan fill="{ "var(--accent-blue, #58a6ff)" if is_current else "var(--text-secondary, #8b949e)" }" font-weight="{ "700" if is_current else "500" }">{html.escape(run_label)}</tspan>'
        svg_parts.append(
            f'  <text x="{x:.1f}" y="{baseline_y + 16:.1f}" text-anchor="middle" font-size="9.5" font-family="system-ui, sans-serif">{run_name_styled}</text>'
        )
        if is_current:
            svg_parts.append(
                f'  <text x="{x:.1f}" y="{baseline_y + 28:.1f}" text-anchor="middle" font-size="8.5" fill="var(--accent-blue, #58a6ff)" font-weight="700" font-family="system-ui, sans-serif">(Current)</text>'
            )

    svg_parts.append('  <!-- Legend -->')
    svg_parts.append(
        '  <g transform="translate(60, 14)">'
        '    <circle cx="5" cy="0" r="3.5" fill="var(--status-pass, #3fb950)"/>'
        '    <text x="13" y="3" font-size="9.5" fill="var(--text-secondary, #8b949e)" font-family="system-ui, sans-serif">Pass Rate (%)</text>'
        '    <rect x="110" y="-4" width="8" height="8" rx="2" fill="var(--accent-blue, #1f6feb)" fill-opacity="0.6"/>'
        '    <text x="123" y="3" font-size="9.5" fill="var(--text-secondary, #8b949e)" font-family="system-ui, sans-serif">Duration (s)</text>'
        '  </g>'
    )

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)

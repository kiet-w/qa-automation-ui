"""
reporting/charts/bar.py - Pure SVG Duration Bar Chart with video seek support.
"""

import html
from typing import Any, List


def generate_duration_bar_chart_svg(items: List[Any]) -> str:
    """
    Generates a pure SVG Bar Chart comparing execution duration of steps or tests.
    Includes baseline, grid indicators, rounded bars, timing labels, and click-to-seek video support.
    """
    if not items:
        return '<div class="no-data-hint" style="color: var(--text-secondary, #8b949e);" data-i18n="no_duration_data">No duration data available.</div>'

    num_items = len(items)
    # Dynamic slot calculation to guarantee ample breathing room and prevent any text overlap
    if num_items <= 6:
        desired_slot = 62.0
    elif num_items <= 12:
        desired_slot = 50.0
    else:
        desired_slot = 44.0

    margin_left = 65
    margin_right = 30
    margin_top = 28
    margin_bottom = 45
    height = 205

    # Calculate dynamic width so that bars never crunch together
    min_width = 540
    calculated_width = int(margin_left + margin_right + num_items * desired_slot)
    width = max(min_width, calculated_width)

    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    max_val = max((item[1] for item in items), default=1.0)
    if max_val <= 0:
        max_val = 1.0
    ceiling = max(round(max_val * 1.15, 1), 1.0)

    bar_slot = plot_width / num_items
    bar_width = min(32.0, max(14.0, bar_slot * 0.52))

    svg_parts = [
        '<div class="bar-chart-scroll-wrapper">',
        f'<svg viewBox="0 0 {width} {height}" class="bar-chart-svg" width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <linearGradient id="bar-grad" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0%" stop-color="#1f6feb" stop-opacity="0.85"/>',
        '      <stop offset="100%" stop-color="#0969da" stop-opacity="0.95"/>',
        '    </linearGradient>',
        '    <linearGradient id="bar-grad-accent" x1="0" y1="0" x2="0" y2="1">',
        '      <stop offset="0%" stop-color="#3fb950" stop-opacity="0.9"/>',
        '      <stop offset="100%" stop-color="#238636" stop-opacity="0.95"/>',
        '    </linearGradient>',
        '  </defs>',
    ]

    # Grid lines (0%, 50%, 100%)
    for ratio in [0.0, 0.5, 1.0]:
        y = margin_top + plot_height * (1.0 - ratio)
        val_label = f"{ceiling * ratio:.1f}s"
        svg_parts.append(
            f'  <line x1="{margin_left}" y1="{y:.1f}" x2="{width - margin_right}" y2="{y:.1f}" stroke="var(--border-color, #30363d)" stroke-dasharray="3,3" stroke-width="1"/>'
        )
        svg_parts.append(
            f'  <text x="{margin_left - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="10" fill="var(--text-secondary, #8b949e)" font-family="monospace">{val_label}</text>'
        )

    # Baseline axis
    baseline_y = margin_top + plot_height
    svg_parts.append(
        f'  <line x1="{margin_left}" y1="{baseline_y}" x2="{width - margin_right}" y2="{baseline_y}" stroke="var(--border-color, #30363d)" stroke-width="1.5"/>'
    )

    # Bars
    for i, item in enumerate(items):
        label = item[0]
        val = item[1]
        rest = item[2:] if len(item) > 2 else None

        bar_h = (val / ceiling) * plot_height
        bar_x = margin_left + i * bar_slot + (bar_slot - bar_width) / 2
        bar_y = baseline_y - bar_h

        is_highlight = (val == max_val and len(items) > 1)
        grad_id = "bar-grad-accent" if is_highlight else "bar-grad"

        # Format bottom label cleanly to avoid overlapping
        if num_items > 10 and "Test #" in label:
            short_label = f"#{label.split('#')[-1].strip()}"
        elif len(label) > 10:
            short_label = label[:9] + "…"
        else:
            short_label = label

        extra_attrs = ""
        tooltip_text = f"{html.escape(label)}: {val:.2f}s"
        if rest and len(rest) >= 5:
            start_time, end_time, t_idx, s_idx, card_target_id = rest
            extra_attrs = (
                f' id="bar-group-{t_idx}-{s_idx}"'
                f' class="bar-group clickable-bar"'
                f' data-test-idx="{t_idx}" data-step-idx="{s_idx}"'
                f' data-start="{start_time:.2f}" data-end="{end_time:.2f}"'
                f' onclick="seekVideoAndScroll({start_time:.2f}, \'{card_target_id}\', {t_idx}, {s_idx})"'
                f' role="button"'
            )
            tooltip_text = f"{html.escape(label)}: {val:.2f}s ({start_time:.1f}s - {end_time:.1f}s) • Click to seek video"
        else:
            extra_attrs = ' class="bar-group"'

        font_size_val = 10 if bar_slot >= 38 else 9

        svg_parts.extend([
            f'  <g{extra_attrs} tabindex="0">',
            f'    <rect x="{bar_x:.1f}" y="{bar_y:.1f}" width="{bar_width:.1f}" height="{max(bar_h, 2):.1f}" rx="4" fill="url(#{grad_id})">',
            f'      <title>{tooltip_text}</title>',
            '    </rect>',
            f'    <text x="{bar_x + bar_width/2:.1f}" y="{bar_y - 6:.1f}" text-anchor="middle" font-size="{font_size_val}" font-weight="700" fill="var(--text-primary, #e6edf3)" class="chart-text-main" font-family="monospace">{val:.1f}s</text>',
            f'    <text x="{bar_x + bar_width/2:.1f}" y="{baseline_y + 16:.1f}" text-anchor="middle" font-size="10" font-weight="600" fill="var(--text-secondary, #8b949e)" class="chart-text-sub" font-family="system-ui, sans-serif">{html.escape(short_label)}</text>',
            '  </g>',
        ])

    svg_parts.append('</svg>')
    svg_parts.append('</div>')
    return "\n".join(svg_parts)

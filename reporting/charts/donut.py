"""
reporting/charts/donut.py - Pure SVG Donut Chart showing Pass/Fail/Skip outcomes.
"""


def generate_donut_chart_svg(passed: int, failed: int, skipped: int) -> str:
    """
    Generates a pure SVG Donut Chart showing the distribution of test outcomes.
    Uses stroke-dasharray and stroke-dashoffset on SVG <circle>.
    100% offline, zero external dependencies.
    """
    total = passed + failed + skipped
    r = 65
    cx, cy = 100, 100
    circumference = 2 * 3.141592653589793 * r

    if total == 0:
        pass_pct = 0
        pass_dash = 0.0
        fail_dash = 0.0
        skip_dash = 0.0
    else:
        pass_pct = round((passed / total) * 100)
        pass_dash = (passed / total) * circumference
        fail_dash = (failed / total) * circumference
        skip_dash = (skipped / total) * circumference

    offset_pass = 0.0
    offset_fail = -pass_dash
    offset_skip = -(pass_dash + fail_dash)

    svg_parts = [
        '<svg viewBox="0 0 200 200" class="donut-svg" width="100%" height="180" xmlns="http://www.w3.org/2000/svg">',
        '  <defs>',
        '    <filter id="glow-pass" x="-20%" y="-20%" width="140%" height="140%">',
        '      <feDropShadow dx="0" dy="0" stdDeviation="3" flood-color="#10b981" flood-opacity="0.3"/>',
        '    </filter>',
        '  </defs>',
        '  <!-- Background track -->',
        f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e293b" stroke-width="20"/>',
    ]

    if total == 0:
        svg_parts.append(
            f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#334155" stroke-width="20"/>'
        )
    else:
        svg_parts.append(f'  <g transform="rotate(-90 {cx} {cy})">')
        if passed > 0:
            svg_parts.append(
                f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#10b981" stroke-width="20" '
                f'stroke-dasharray="{pass_dash:.2f} {circumference - pass_dash:.2f}" stroke-dashoffset="{offset_pass:.2f}" '
                f'stroke-linecap="round" filter="url(#glow-pass)"/>'
            )
        if failed > 0:
            svg_parts.append(
                f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ef4444" stroke-width="20" '
                f'stroke-dasharray="{fail_dash:.2f} {circumference - fail_dash:.2f}" stroke-dashoffset="{offset_fail:.2f}" '
                f'stroke-linecap="round"/>'
            )
        if skipped > 0:
            svg_parts.append(
                f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#94a3b8" stroke-width="20" '
                f'stroke-dasharray="{skip_dash:.2f} {circumference - skip_dash:.2f}" stroke-dashoffset="{offset_skip:.2f}"/>'
            )
        svg_parts.append('  </g>')

    svg_parts.extend([
        f'  <text x="{cx}" y="{cy - 4}" text-anchor="middle" font-size="28" font-weight="800" fill="#f8fafc" font-family="system-ui, sans-serif">{pass_pct}%</text>',
        f'  <text x="{cx}" y="{cy + 18}" text-anchor="middle" font-size="11" font-weight="600" fill="#94a3b8" font-family="system-ui, sans-serif" data-i18n="pass_rate">PASS RATE</text>',
        '</svg>',
    ])
    return "\n".join(svg_parts)

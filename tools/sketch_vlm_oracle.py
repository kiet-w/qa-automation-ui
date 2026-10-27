"""
tools/sketch_vlm_oracle.py - SketchVLM Vision-Language Oracle for UI Visual Defect Diagnosis.

Implements the SketchVLM research paradigm (arXiv:2604.22875):
- Takes a UI test failure screenshot.
- Prompts Vision-Language Model (Gemini) with coordinate grid context.
- Generates structured, non-destructive SVG annotation primitives (circles, arrows, callout labels)
  explaining layout anomalies, clipping, visual overlaps, and WCAG accessibility defects.
- Can be invoked via CLI or imported into test triage reporting pipelines.
"""

import base64
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional
import urllib.error
import urllib.request

WORKSPACE_DIR = Path(__file__).resolve().parent.parent

SKETCHVLM_SYSTEM_PROMPT = """
You are SketchVLM, an expert visual UI defect inspector.
Analyze the provided screenshot of an automated UI test failure.
Identify the primary visual defect (e.g. invalid input, error message, layout overlap, truncated text, clipping, or missing state).

Output your response strictly as valid JSON with the following structure:
{
  "summary": "Short 1-line description of the visual defect",
  "root_cause": "Detailed explanation of why this visual state is defective",
  "confidence": 0.95,
  "annotations": [
    {
      "type": "circle",
      "cx": 450,
      "cy": 320,
      "r": 35,
      "color": "#cf222e",
      "label": "Defective Input"
    },
    {
      "type": "arrow",
      "from_x": 450,
      "from_y": 250,
      "to_x": 450,
      "to_y": 285,
      "color": "#cf222e"
    },
    {
      "type": "badge",
      "x": 380,
      "y": 215,
      "text": "DEFECT: Invalid Value Accepted",
      "color": "#cf222e"
    }
  ]
}
"""


class SketchVLMOracle:
    """Vision-Language Model Oracle for UI visual bug diagnosis and SVG annotation generation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gemini-2.5-flash",
        offline_mode: bool = False,
    ):
        self.offline_mode = offline_mode
        self.api_key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY")
        self.model = model

    def analyze_screenshot(
        self,
        screenshot_path: Union[str, Path],
        context_prompt: str = "Analyze this failure screenshot and annotate the defect.",
    ) -> Dict[str, Any]:
        """Analyzes a failure screenshot and returns SketchVLM structured annotations."""
        path = Path(screenshot_path)
        if not path.exists():
            return {
                "status": "error",
                "message": f"Screenshot file not found: {path}",
                "annotations": [],
            }

        with open(path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        # If online and API key is present, call Gemini API
        if not self.offline_mode and self.api_key:
            return self._call_gemini_api(image_b64, context_prompt)

        # Fallback deterministic oracle mode (offline simulation)
        return self._generate_fallback_annotations(path, context_prompt)

    def _call_gemini_api(self, image_b64: str, context_prompt: str) -> Dict[str, Any]:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
            f"?key={self.api_key}"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{SKETCHVLM_SYSTEM_PROMPT}\n\nContext: {context_prompt}"},
                        {
                            "inlineData": {
                                "mimeType": "image/png",
                                "data": image_b64,
                            }
                        },
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2,
            },
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "{}")
                )
                parsed = json.loads(text)
                parsed["status"] = "success"
                parsed["model"] = self.model
                return parsed
        except Exception as e:
            return {
                "status": "api_error",
                "error": str(e),
                "fallback": self._generate_fallback_annotations(None, context_prompt),
            }

    def _generate_fallback_annotations(
        self, path: Optional[Path], context_prompt: str
    ) -> Dict[str, Any]:
        """Generates deterministic SVG primitives when offline or no API key is provided."""
        return {
            "status": "offline_mode",
            "summary": "Deterministic SketchVLM Annotation",
            "root_cause": context_prompt,
            "confidence": 0.90,
            "annotations": [
                {
                    "type": "circle",
                    "cx": 520,
                    "cy": 360,
                    "rx": 80,
                    "ry": 24,
                    "color": "#cf222e",
                    "label": "Defective Input Field",
                },
                {
                    "type": "arrow",
                    "from_x": 520,
                    "from_y": 280,
                    "to_x": 520,
                    "to_y": 332,
                    "color": "#cf222e",
                },
                {
                    "type": "badge",
                    "x": 420,
                    "y": 240,
                    "text": "DEFECT: Assertion Violated",
                    "color": "#cf222e",
                },
            ],
        }

    def render_svg_overlay(
        self,
        analysis_result: Dict[str, Any],
        width: int = 1280,
        height: int = 720,
    ) -> str:
        """Converts structured SketchVLM annotations into standalone SVG markup."""
        annotations = analysis_result.get("annotations", [])
        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="position:absolute;top:0;left:0;pointer-events:none;">',
            "<defs>",
            '  <marker id="vlm-arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#cf222e" />',
            "  </marker>",
            '  <filter id="vlm-glow" x="-20%" y="-20%" width="140%" height="140%">',
            '    <feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="#cf222e" flood-opacity="0.8"/>',
            "  </filter>",
            "</defs>",
        ]

        for ann in annotations:
            t = ann.get("type")
            color = ann.get("color", "#cf222e")
            if t == "circle":
                cx = ann.get("cx", 0)
                cy = ann.get("cy", 0)
                rx = ann.get("rx", ann.get("r", 40))
                ry = ann.get("ry", ann.get("r", 40))
                # Organic dual loop
                svg_parts.append(
                    f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="rgba(207,34,46,0.12)" '
                    f'stroke="{color}" stroke-width="3" filter="url(#vlm-glow)" />'
                )
                svg_parts.append(
                    f'  <ellipse cx="{cx+1}" cy="{cy-1}" rx="{rx+2}" ry="{ry+2}" fill="none" '
                    f'stroke="{color}" stroke-width="1.5" stroke-dasharray="6,4" opacity="0.8" />'
                )
            elif t == "arrow":
                fx, fy = ann.get("from_x", 0), ann.get("from_y", 0)
                tx, ty = ann.get("to_x", 0), ann.get("to_y", 0)
                svg_parts.append(
                    f'  <path d="M {fx} {fy} L {tx} {ty}" fill="none" stroke="{color}" '
                    f'stroke-width="2.5" marker-end="url(#vlm-arrow)" />'
                )
            elif t == "badge":
                bx, by = ann.get("x", 0), ann.get("y", 0)
                text = ann.get("text", "")
                svg_parts.append(
                    f'  <g transform="translate({bx},{by})">'
                    f'    <rect width="{len(text)*8 + 24}" height="26" rx="4" fill="{color}" filter="url(#vlm-glow)"/>'
                    f'    <text x="12" y="17" fill="#ffffff" font-family="sans-serif" font-size="12" font-weight="bold">{text}</text>'
                    f"  </g>"
                )

        svg_parts.append("</svg>")
        return "\n".join(svg_parts)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/sketch_vlm_oracle.py <screenshot_path> [prompt]")
        sys.exit(1)

    screenshot = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "Diagnose failure and generate sketch annotations."

    oracle = SketchVLMOracle()
    res = oracle.analyze_screenshot(screenshot, prompt)
    print(json.dumps(res, indent=2))

    svg_content = oracle.render_svg_overlay(res)
    out_svg = Path(screenshot).with_suffix(".sketch.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"\n✅ Standalone SketchVLM SVG overlay saved to: {out_svg}")


if __name__ == "__main__":
    main()

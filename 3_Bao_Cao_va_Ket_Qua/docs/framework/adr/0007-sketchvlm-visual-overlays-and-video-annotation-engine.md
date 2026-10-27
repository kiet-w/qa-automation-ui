# ADR-0007: SketchVLM-Inspired Visual Overlays & Real-Time Video Annotation Engine

## Status
Accepted

## Context
Automated UI test recordings (WebM videos captured via Playwright) are critical evidence for engineering teams, QA leads, and product owners. However, raw browser automation videos frequently suffer from comprehension bottlenecks:
1. Viewers cannot determine which test step is currently running without cross-referencing external logs.
2. Fast automated mouse actions (clicks, rapid keystrokes, form resets) happen instantaneously without visual cues, making it hard to see what triggered a state change.
3. When assertions fail, standard error reporting often only highlights errors post-mortem in static reports. Videos end abruptly without visually circling the root cause element or pointing an arrow to the defect.
4. While research frameworks like **SketchVLM** (*arXiv:2604.22875*) demonstrate that Vision-Language Models (VLMs) can generate SVG circles, arrows, and callouts to explain reasoning, attempting to process 30fps video frames through external VLM inference is prohibitively slow (>1s/frame), astronomically expensive in API tokens, and susceptible to spatial coordinate hallucinations.

## Decision
We implement a **Dual-Layer Visual Architecture** combining browser-native DOM/SVG real-time overlays for live video recordings with an on-demand VLM oracle for complex visual screenshot triage:

### Layer 1: Real-Time Browser-Native Visual Engine (`core/sketch_annotator.py`)
- **Zero Token Overhead & Zero Latency**: Uses lightweight, non-blocking DOM and SVG manipulation executed directly in the browser instance.
- **Live Step HUD Bar**: When `StepTracker` enters `with self.step(...)`, a sleek glassmorphism banner (`[STEP X] <step_title>`) is rendered at the top of the browser viewport. This is natively recorded into Playwright's WebM video, ensuring viewers always know the active step.
- **Action Radar & Spotlight**: Whenever Page Objects perform user interactions (`click_element`, `fill_text`, `save`, `cancel`), an animated radar pulse and action pill (e.g. `👆 CLICK: "Save"`, `✏️ TYPE: "..."`) appear over the target element for 500ms.
- **SketchVLM Defect Callout**: On assertion failure, the engine automatically:
  1. Identifies the defective DOM element using tested tokens, semantic selectors, and validation states.
  2. Injects a full-page SVG canvas with a hand-drawn sketch ellipse (dual-stroke organic loop) around the defective element.
  3. Renders an SVG curved arrow with an arrowhead pointing from a floating defect card to the element's center.
  4. Displays a top `DEFECT CAPTURE` evidence banner.
  5. Holds the browser frame for 1.4s so the video camera and failure screenshot capture complete visual defect evidence.
- **Non-Destructive Execution**: All injected visual layers enforce `pointer-events: none` and `user-select: none`, guaranteeing zero interference with native Playwright clicks, typing, or synthetic events.

### Layer 2: On-Demand SketchVLM AI Oracle (`tools/sketch_vlm_oracle.py`)
- For Tier 3 (Visual & Layout Integrity) and Tier 6 (Accessibility) defects where the DOM does not immediately reveal root cause (e.g., text clipping, Z-index stacking collisions, modal overlaps, subtle alignment shifts):
  - Engineers or CI/CD pipelines can invoke `SketchVLMOracle` with the failure screenshot.
  - Prompts Google Gemini with the SketchVLM prompt schema, returning structured XML/JSON primitives (circles, arrows, badges) and producing a standalone `.sketch.svg` overlay.

## Consequences

### Positive
- **High-Clarity Video Recordings**: Test videos serve as self-explanatory visual walk-throughs with step tickers and interaction highlights.
- **Instant Defect Pinpointing**: Failed test videos and screenshots explicitly circle the bug and draw a pointer arrow to the problematic field before closing.
- **Zero Performance & Token Cost**: Layer 1 adds zero API token costs and negligible execution overhead (~50ms per action).
- **Architectural Traceability**: Integrates seamlessly with `BasePage`, `StepTracker`, and `pytest_runtest_makereport`.

### Negative / Trade-offs
- Defect highlight adds a brief 1.4s pause before test teardown only when a failure occurs. This is intentional to guarantee video capture of the defect frame.

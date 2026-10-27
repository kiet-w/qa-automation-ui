# ADR-0004: Video Asset Optimization & Scalable Offline Reporting

## Status
Accepted

## Context
The reporting engine (`reporting/`) generates 100% self-contained offline ExtentReports HTML documents with zero CDN dependencies.
Prior to this ADR, every test execution video (Full HD 1080p WebM) was unconditionally read, Base64-encoded, and embedded directly into the HTML document as `data:video/webm;base64,...`.
In test suites with large test counts (such as User Story 4 with 68 test cases), embedding 68 Full HD videos led to:
1. Catastrophic HTML bloat (exceeding 200MB - 400MB per report).
2. Out-of-memory crashes and browser tab freezes during DOM parsing and rendering.
3. Wasteful 1080p video recording overhead for embedded player cards rendered at ~700px width.

## Decision
We adopt a **Hybrid Dual-Mode Video Delivery Architecture** combined with optimized capture resolution:

1. **Resolution Optimization (720p)**:
   - Configure `record_video_size` to `1280x720` (720p 16:9).
   - This provides razor-sharp UI clarity for form fields and status badges while cutting raw video storage and processing overhead by 50-60%.

2. **Default Mode: Lightweight Linked Media (`embed_media=False`)**:
   - WebM video recordings remain in their respective run artifact directory (`test-results/<run_id>/<test_slug>/video.webm`).
   - The report HTML uses multi-candidate relative `<source>` elements to resolve video paths dynamically whether viewed from:
     - `reports/<ticket>/execution_report.html` (`src="test-results/..."`)
     - `reports/<ticket>/history/<run_id>.html` (`src="../test-results/..."`)
     - `reports/execution_report.html` (`src="<ticket>/test-results/..."`)
   - Keeps single-file HTML reports ultra-lightweight (~1MB - 2MB), preserving smooth 60fps scrolling and fast initial page load.

3. **Standalone Portable Mode (`--embed-media`)**:
   - When users need to share a strictly standalone single file via email or chat without accompanying folder structures, passing `--embed-media` activates Base64 embedding.

## Consequences

### Positive
- **Drastic Size Reduction**: HTML reports drop from >200MB to ~1MB (99% reduction) in default mode.
- **Fast Rendering & Zero Tab Freezing**: Browser handles the HTML report instantaneously without memory strain.
- **Native Browser Video Streaming**: The browser natively streams WebM from disk instead of buffering massive Base64 strings in V8 memory.
- **Portability Maintained**: Users can still produce 100% self-contained monolithic files when explicitly requested via `--embed-media`.

### Negative / Trade-offs
- In default linked mode, moving the `.html` file away from its parent `reports/<ticket>/` directory without copying `test-results/` will cause video playback to fail (though full test logs, duration charts, and step timelines remain fully readable).

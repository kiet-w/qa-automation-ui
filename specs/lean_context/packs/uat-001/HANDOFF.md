# UAT-001 — source handoff

Status: **draft source selection**, not approved testcase/coverage. No automation executed.

- `manifest.json`: selected sources and reasons with file hashes; editable selection source.
- `source.pack.json`: exact excerpts, 12 deduplicated entries; use pack.py list/read by entry, not cat.
- `manifest.draft.json`: initial keyword candidates only; no claim of completeness.
- Existing testcase: `1_Nghiep_Vu_va_Specs/testcases/f01/f01-education-accounts/TC_F01_UAT001_EA_Provisioning.md` (preserved, not migrated).
- Sources: final F01 portion + shared data/boundaries of FS-01, F01 atomic specs/flow/component map, recorded education-accounts BSK, existing testcase. Historical FSD duplicate and illustrative POM code were not copied into the pack.

Next design task: check pack freshness; inspect the entries needed; reconcile exact BR/AC/control coverage, F02/shared dependencies and existing TC oracles; check recorded DOM against the target build. Existing testcase labels/coverage are source claims, not verified by this handoff.

Before coding: obtain real testcase review evidence, locate/complete referenced fixtures and BSK for the target version, then build a coding manifest with Testcase/Fixtures/UI roles. Do not make up approval or fixture contents. Reuse the reviewed artifact and rule 04; do not redo broad spec discovery.

# MCP Session Log

No MCP, CAD, rendering, Illustrator, Photoshop, Blender, Fusion, or SolidWorks
session was run for the Round 4 V5 migration patch below. The 2026-07-01 V5
refresh pass (rows below) did run a local OpenSCAD CLI render-check on a new
codeCAD master; it did not run wolframscript (Wolfram stays source-only per
V5 honesty rules) and did not create measured tuning, reed/mouthpiece, or
prototype validation data.

The repo already contains generated or starter artifacts under `build/`,
including OpenSCAD/SolidWorks sources, SVG drawing previews, presentation
exports, and measurement templates. The Round 4 patch only added V5 authority
and provenance records; it did not create new CAD geometry, DXF coordinates,
measured tuning data, reed/mouthpiece data, or prototype validation.

| session_id | timestamp_utc | tool | input_authority | outputs | role | authority_result | review_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r4-v5-migration-2026-05-30 | 2026-05-30 | none | README.md; design.md; build/packet/design.md; build/packet/drawing-brief.md; build/packet/visual-bom-brief.md | visual-output-register.csv; cad/mcp-session-log.md; README.md | provenance_stub | pending_measurement | self_checked | V5 register/status/provenance only; no fabricated CAD, DXF, acoustic, or measurement data. |
| fable-v5-refresh-2026-07-01 | 2026-07-01 | claude-code (Fable 5) | build/packet/family-spec.csv; build/data/tone-hole-schedule.csv; build/cad/solidworks-design-table.csv | bom.csv; sourcing.csv; cut-list.csv; drawing-brief.md; validation.csv | packet_refresh | fabrication | self_checked | V5 refresh pass; tabular packet data reviewed against design table (family-spec.csv, tone-hole-schedule.csv); root sourcing.csv/cut-list.csv/drawing-brief.md scaffolded honestly (TBD-marked) to satisfy required-baseline check, condensed from existing build/packet/ equivalents, no new dimensions invented. |
| fable-v5-refresh-2026-07-01 | 2026-07-01 | claude-code (Fable 5) + OpenSCAD CLI | build/packet/family-spec.csv; build/data/tone-hole-schedule.csv | cad/chalumeau.scad | cad_authoring | pending_measurement | self_checked | New parametric bore-envelope + tone-hole-schedule OpenSCAD master for all four family variants (soprano/alto/tenor/bass), values traced to family-spec.csv and tone-hole-schedule.csv. Mouthpiece, reed, reed-seat/tenor socket, tone-hole undercutting, and keywork are explicitly out of scope (see file header) — tuning-sensitive regions requiring hand refinement against a measured prototype. OpenSCAD render check: pass (openscad -o STL, exit 0, both default soprano render and SHOW_FAMILY=true four-variant layout). |
| fable-v5-refresh-2026-07-01 | 2026-07-01 | claude-code (Fable 5) | build/packet/chalumeau-packet-starter.wl | visual-output-register.csv (WL-001 row) | analysis_source | derived_preview | unreviewed | Existing Wolfram stopped-pipe first-pass acoustic model source; left as-is (not rewritten, not renamed). Not executed in this pass — source-only, L2 evidence per honesty rules. |

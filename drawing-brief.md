# Chalumeau Drawing Brief (Root Starter)

Instrument: Chalumeau family
Revision/date: REV-A (root V5 refresh, 2026-07-01)
Units: inches unless noted
Source workbook/CAD/catalog ID: CLM-001 / SolidWorks design table

This root file is a condensed entry point. The detailed drawing brief lives at
[`build/packet/drawing-brief.md`](build/packet/drawing-brief.md); do not
duplicate dimensions here that would drift out of sync with that source.

## Required Views (summary)

- Family comparison side view with bore axis and body lengths (soprano, alto,
  tenor, bass).
- Soprano C dimensioned side view with all H/K hole coordinates.
- Cross-section through bore, tone-hole chimney, and raised collar.
- Keywork detail for K01/K02 (optional, two-key handmade lever system).
- Exploded view: mouthpiece/reed, body, bell, K01, K02, pads, posts.

## Authority Notes

- Bore ID, body length, and tone-hole positions/diameters are sourced from
  `build/packet/family-spec.csv` and `build/data/tone-hole-schedule.csv`
  (mirrored into `build/cad/solidworks-design-table.csv`). All values are
  `pending_measurement` / formula-derived starting points, not measured build
  authority.
- Mouthpiece, reed, and reed-table geometry are explicitly out of scope for
  this packet's CAD/drawing authority until reed/mouthpiece setup is selected
  and measured (see `risks.md` R-BB-001 and `validation.csv` VAL-BB-010).
- Hole X-from-bell tolerance target: +/- 0.020 in for the first prototype;
  holes are drilled undersize and opened during tuning.

## Drawing Outputs In This Packet

- `build/drawings/chalumeau-family-sheet.svg`
- `build/drawings/chalumeau-soprano-c4-dimensioned.svg`
- `build/drawings/keywork-lever-detail.svg`
- `cad/chalumeau.scad` — bore envelope + hole-schedule OpenSCAD master (added
  in this V5 refresh pass; mouthpiece/reed geometry out of scope, see header).

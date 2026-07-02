# Design Intent — chalumeau rev A

- Master CAD: `cad/chalumeau.scad` (sha256: 13451f99a86a681640b9e17f356b9698ee71d95884940ccebe95520e1bb521b9), driven by `build/packet/family-spec.csv` (sha256: 9ce0445943e6ebc0a44ed7502ac97fb6d3492f08f3095edcdd2c2f542a6a8b5a) and `build/data/tone-hole-schedule.csv` (sha256: 0f35e805d9f5326e0fc78a537e0cde939696324145dede14f72cae74ca83d0da)
- Function: cylindrical, single-reed, effectively stopped-pipe woodwind family in soprano C, alto G, tenor C, and bass F. Body length, bore ID, and tone-hole positions/diameters are formula/table-driven rather than one-off dimensions. First-pass acoustic law: `f = c / (4 * L_eff)` (design.md "Acoustic Boundary"). The recommended build order is soprano first, keyless, with a commercial reed/mouthpiece; optional two-key handmade lever hardware (K01/K02) may follow once the keyless body speaks reliably.
- Environment: indoor practice/prototype instrument; single-reed excitation, hand-held, no sustained structural load beyond finger/lever pressure on tone-hole covers.
- Target qty: 1 (soprano prototype). Deadline: TBD. Budget/unit ceiling: TBD.

## Critical dimensions (carry tolerances)

| Feature | Nominal (soprano CLM-SOP-C4) | Tolerance | Why critical | Source |
| --- | --- | --- | --- | --- |
| Bore ID | 0.500 in | +/- 0.003 in after ream/lap | sets stopped-pipe effective length and reed-seat fit | `build/packet/family-spec.csv` (measurement_required) |
| Body length (final) | 12.672 in | trim allowance; final by tuning | root pitch (C4, 261.63 Hz target) | `build/packet/family-spec.csv` (measurement_required) |
| Bell OD | 1.65 in | drawing/CAD review target | end-correction and foot flare geometry | `build/packet/family-spec.csv` (measurement_required) |
| Tone-hole X from bell (H01-H07, K01-K02) | 0.622-6.370 in (9 holes) | +/- 0.020 in first prototype | pitch of each scale degree/chromatic note | `build/data/tone-hole-schedule.csv` (measurement_required) |
| Tone-hole diameter (H01-H07, K01-K02) | 0.150-0.200 in | drilled undersize, opened during tuning | pitch and response of each note | `build/data/tone-hole-schedule.csv`, drill-undersize build_note |
| Wall thickness | 0.188 in | shop review | structural margin around tone holes/key posts | `build/packet/family-spec.csv` (measurement_required) |

## Incidental (free for DFM)

- Bell flare curve profile, exterior surface finish/turning texture, cosmetic collar/ring details, blank-to-final-length turning allowance (currently 1.5 in per `build/packet/cut-list.csv`).

## Must-nots (DFM may never violate)

- Do not treat `build/cad/`, `build/drawings/`, or `cad/chalumeau.scad` as reviewed fabrication authority — they are `pending_measurement` starter/source evidence until the soprano prototype's measured pitch/response data is folded back (risks.md R-BB-005; validation.csv VAL-BB-050).
- Do not drill tone holes to final diameter directly — start undersize (15-25%) and enlarge only against logged measured cents error (risks.md R-BB-002; tone-hole-schedule.csv build_note).
- Do not apply Native American flute (K2) or open-open flute end corrections — chalumeau is a cylindrical single-reed stopped pipe; keep `acoustic_law=stopped_pipe`, `end_condition=one_end_closed_reed` (design.md "Acoustic Boundary"; risks.md R-BB-003).
- Do not treat optional K01/K02 keywork as validated until leak-light/suction test passes with pads installed (risks.md R-BB-004; validation.csv VAL-BB-040).
- Do not model or fabricate mouthpiece/reed/reed-seat geometry from this CAD master — that geometry is explicitly out of scope and tuning-sensitive (cad/chalumeau.scad header; risks.md R-BB-001).

## Material intent

- Preferred: domestic hardwood prototype blanks (cherry, hard maple, or walnut) for the first soprano build (`bom.csv` CLM-BB-001; `build/packet/sourcing.csv`).
- Acceptable subs: dense keeper-build woods (ipe, cocobolo, boxwood, rosewood, grenadilla substitute) or Delrin/acetal for dimensional-stability testing, per `sourcing.csv`/`build/packet/sourcing.csv`.
- Forbidden: none recorded; oily/allergenic dense woods require dust control and finish tests before use (risks.md R-BB-006).

## Stage status

Stage 0 intake complete 2026-07-01. Gate A (Alpha shop compile) NOT yet run — no concessions logged, nothing presented as shippable or build-ready.

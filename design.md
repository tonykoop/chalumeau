# Chalumeau Bare-Bones Starter Design

Current status: **bare-bones readiness packet / prototype-validation scaffold**.

Fabrication authority: **not build-ready**. The repo contains useful generated
packet artifacts under `build/`, including design tables, SVG drawing exports,
and OpenSCAD/SolidWorks starter files, but no measured prototype data or
reviewed CAD/DXF fabrication authority is present in this root packet.

## Intent

Create a reviewable repo-root entry point for the chalumeau family: a
cylindrical single-reed woodwind with keyless first-build emphasis and optional
two-key handmade metalwork after the soprano body speaks reliably.

The existing detailed packet lives in `build/packet/design.md`. This root
starter file does not replace that packet; it summarizes the current evidence
and the gates required before promoting the repo beyond scaffold status.

## Current Evidence

| Evidence | Location | Readiness note |
| --- | --- | --- |
| Family design narrative | `build/packet/design.md` | First-pass stopped-pipe model; requires measured correction. |
| Family dimensions and tables | `build/packet/family-spec.csv`, `build/design-tables/chalumeau-family-design-table.xlsx` | Formula-derived starting points, not measured build authority. |
| Tone-hole schedule | `build/data/tone-hole-schedule.csv` | Drill undersized; tune and log measured response before accepting. |
| CAD/OpenSCAD starters | `build/cad/` | Source/starter evidence only; no reviewed DXF or fabrication release. |
| Drawing previews | `build/drawings/` | Useful shop-review drawings; verify against measured prototype before build release. |
| Presentation packet | `build/presentation/` | Review/export surface; older manifest paths require root-level caution. |

## Acoustic Boundary

The chalumeau should be treated as a cylindrical single-reed stopped pipe in
the low register. The working first-pass model is:

```text
f = c / (4 * L_eff)
L_eff = c / (4 * f)
```

This packet does **not** apply Native American flute K2 corrections or
open-open flute assumptions. Reed/mouthpiece compliance, bore finish, tone-hole
chimney height, and player pressure require prototype measurement before any
tuning claim becomes validated.

`build/packet/family-spec.csv` now records `acoustic_law=stopped_pipe`,
`end_condition=one_end_closed_reed`, and
`dimension_provenance=measurement_required` for each family member. That keeps
the quarter-wave reed-pipe assumption explicit without pretending the current
lengths are empirically corrected build dimensions.

## Assumptions To Verify

| Assumption | Current value | Evidence needed |
| --- | --- | --- |
| Soprano C is the first prototype | assumption | Build-log decision and measured response. |
| Commercial reed/mouthpiece should be used first | assumption | Selected reed/mouthpiece model, strength, facing, and setup notes. |
| Tone-hole positions are starting points | derived estimate | Measured pitch sweep after drilling undersized holes. |
| Optional K01/K02 keywork can seal reliably | requires measurement | Leak-light/suction test and tuning data with pads installed. |
| Scaled alto/tenor/bass variants are viable | TBD | Soprano correction data before scaling. |

## Measurement Capture Files

The current measurement files are capture templates only. They become evidence
after shop measurements fill in the empty `measured_hz`, `cents_error`,
`onset_pressure_in_h2o`, `response_rating_1_5`, bore, gap, leak, and action
fields.

| Gate | Template | Blocks |
| --- | --- | --- |
| P0 reed/mouthpiece setup | `build/data/reed-mouthpiece-capture-template.csv` | root pitch claims |
| P1 bore/root tuning | `build/data/bore-trim-capture-template.csv` | final tone-hole drilling |
| P2 pitch/response sweep | `build/data/prototype-measurement-template.csv` and `build/data/tuning-capture-template.csv` | tone-hole acceptance and family scaling |
| P3 keywork seal | `validation.csv` plus shop leak evidence | keyed-note claims |

## Promotion Gates

The repo should stay at scaffold status until:

- the first soprano prototype has measured pitch/response data;
- reed and mouthpiece setup are recorded with each measurement pass;
- tone-hole changes are logged from undersized drilling through final tuning;
- keywork leak tests are documented if levers are installed;
- the chosen CAD/DXF/design-table artifact is declared as fabrication authority;
- sourcing rows are checked at purchase time, not treated as current quotes.

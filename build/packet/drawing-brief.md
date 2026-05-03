# Chalumeau Drawing Brief

Instrument: Chalumeau family
Revision/date: REV-A
Units: inches unless noted
Source workbook/CAD/catalog ID: CLM-001 / SolidWorks design table

## Required Views

- Family comparison side view with bore axis and body lengths.
- Soprano C dimensioned side view with all H/K hole coordinates.
- Cross-section through bore, tone-hole chimney, and raised collar.
- Keywork detail for K01/K02: closed/open positions, pad, cup, pivot,
  posts, spring, touchpiece.
- Exploded view: mouthpiece/reed, body, bell, K01, K02, pads, posts.
- Ergonomic view: hand reach for keyless soprano and keyed bass notes.

## Critical Dimensions

| Feature | Dimension source | Tolerance |
| --- | --- | --- |
| Bore ID | `family-spec.csv` | +/- 0.003 in after ream/lap |
| Body length | `family-spec.csv` | leave trim allowance; final by tuning |
| Hole X from bell | `../data/tone-hole-schedule.csv` | +/- 0.020 in first prototype |
| Hole diameter | `../data/tone-hole-schedule.csv` | start undersize; final by tuning |
| Pad seat flatness | `../hardware/keywork-parts.csv` | no visible leak |
| Pivot alignment | keywork drawing | lever moves freely without side shake |

## Drawing Outputs In This Packet

- `../drawings/chalumeau-family-sheet.svg`
- `../drawings/chalumeau-soprano-c4-dimensioned.svg`
- `../drawings/keywork-lever-detail.svg`

## Notes For SolidWorks

Drive dimensions from global variables. Do not dimension hole centers
manually in separate sketches unless the dimension names match the CSV.

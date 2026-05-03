# CLM-001 - Chalumeau Family

Generated: 2026-05-03

## Intent

Design a family of chalumeaux that can be built in Tony's shop using
lathe/CNC workflows, commercial reeds for early isolation tests, and
optional handmade metal keywork. The family should cover a useful range
without pretending the first-pass physics is final: all tone-hole
coordinates are starting points that must be validated with a real reed,
mouthpiece, bore, and player pressure.

## Source Artifacts

- Repo: `https://github.com/tonykoop/chalumeau`
- Local inspiration photos: `images/chalumeau1.jpg`, `images/chalumeau5.jpg`,
  and `images/7173-372-1_1920x1080.avif`
- Workbook inspected: `C:/Users/Tony/Documents/Claude/Projects/Career/flutes-staging/Musical Instruments.xlsx`
- Relevant workbook source sheet: `Great Highland Bagpipe`, especially the
  contrast between conical double-reed chanter rows and cylindrical
  single-reed drone rows.
- Done-bar reference style: `tongue-drum` repo packet and skill v3
  packet requirements.

## Governing Model

The chalumeau is modeled as a cylindrical single-reed pipe that behaves
like a stopped pipe in its low register.

```text
f = c / (4 * L_eff)
L_eff = c / (4 * f)
c = 13552 in/s at about 68 F
body_length = L_eff - bell_end_correction - reed_end_correction
bell_end_correction = 0.61 * bore_radius
reed_end_correction = 0.25 * bore_id   # first-pass assumption
tone_hole_x_from_bell = body_length - (c/(4*f_note) - reed_corr - 0.30*hole_dia)
cents_error = 1200 * log2(measured_hz / target_hz)
```

The model deliberately does not use Tony's NAF K2 corrections. Those
corrections are for open-open Native American style flutes in a specific
bore range. The chalumeau reed, stopped-pipe boundary condition,
mouthpiece volume, bore diameter, and tone-hole chimneys need their own
empirical correction after prototype measurement.

## Family Spec

| ID | Variant | Root | Bore ID | Final body L | Blank L | Sections |
| --- | --- | --- | --- | --- | --- | --- |
| CLM-SOP-C4 | Soprano C | C4 | 0.5 | 12.672 | 14.172 | 1 body + mouthpiece + bell |
| CLM-ALT-G3 | Alto G | G3 | 0.625 | 16.939 | 18.439 | 1 body + mouthpiece + bell |
| CLM-TEN-C3 | Tenor C | C3 | 0.75 | 25.483 | 26.983 | 2 body joints + mouthpiece + bell |
| CLM-BAS-F2 | Bass F | F2 | 0.875 | 38.32 | 39.82 | 3 body joints + mouthpiece + bell |

## Tone-Hole Strategy

- The keyless core uses seven front holes for a diatonic octave:
  offsets +2, +4, +5, +7, +9, +11, +12 semitones from the all-closed
  root.
- `K01` is an optional normally closed semitone key near the bell. It
  gives the first chromatic note above the root without forcing an
  awkward low finger stretch.
- `K02` is an optional upper chromatic side key. It gives a practical
  chromatic note between scale degrees 6 and 7 and doubles as a keywork
  fabrication exercise.
- A clarinet-style register vent is listed only as an experimental
  future feature. The first chalumeau should be judged by the low
  register before chasing overblown twelfths.

## Hardware Alignment

The hardware is intentionally small-shop manufacturable:

| Hardware | Role | First-build method | Upgrade path |
| --- | --- | --- | --- |
| K01 lever | opens low semitone tone hole | brass strip lever, pivot post pair, leather/cork pad | nickel-silver lever with soldered pad cup |
| K02 lever | opens upper chromatic tone hole | side lever with flat spring return | clarinet-style post/rod key with regulation cork |
| Optional register vent | tests clarinet evolution | leave undrilled until the body speaks well | small lined vent tube near mouthpiece |
| Raised tone-hole collars | ergonomic/aesthetic reference to photos | turn integral collars or add rings | separate stabilized-wood collars |

## SolidWorks Parameter Convention

Use `CLM_` as the project prefix, keep units in the variable name, and
use stable hole IDs that match the CSV and drawings:

- `CLM_Bore_ID_in`, `CLM_Body_L_Final_in`, `CLM_Bell_OD_in`
- `CLM_H01_X_Bell_in`, `CLM_H01_Dia_in`
- `CLM_K01_X_Bell_in`, `CLM_K01_Dia_in`
- `CLM_Key_Pivot_Rod_Dia_in`, `CLM_Pad_Overhang_in`

The SolidWorks design table is `cad/solidworks-design-table.csv`. The
equation snippets are in `cad/solidworks-equations.txt`.

## Assumptions And Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Reed/mouthpiece compliance shifts pitch | the reed is not a hard closed end | test with one commercial reed/mouthpiece before final hole tuning |
| Tone holes are first-pass estimates | small holes do not act as perfect open ends | drill undersized, tune larger, log every change |
| Bass holes exceed finger comfort | low instruments become large quickly | use key pads for lower/bigger holes |
| Handmade key pads leak | leaks ruin tuning and response | leak-light/suction test before pitch tuning |
| Dense oily woods complicate machining | cocobolo/ipe dust and finish issues | prototype in cherry/maple first |

## Validation Plan

1. Calibrate tuner/microphone at A4 = 440 Hz.
2. Build `CLM-SOP-C4` with no levers and a commercial reed/mouthpiece.
3. Tune the all-closed root by trimming the bell/foot only after reed
   response is stable.
4. Open holes from the bell upward, enlarging in small increments and
   logging measured frequency and cents error.
5. Add K01/K02 to either the same body or a second soprano body. Validate
   sealing before measuring pitch.
6. Update the empirical correction column in the design workbook before
   scaling to alto, tenor, or bass.

## Next Actions

- Confirm the actual reed and mouthpiece family for the soprano prototype.
- Decide whether the first body gets raised collars like the inspiration
  image or plain chamfered holes for faster tuning.
- Model `CLM-SOP-C4` in SolidWorks using the provided global variables.
- After first measurements, add a `prototype_correction_pct` column to
  `data/tone-hole-schedule.csv`.

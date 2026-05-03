# Chalumeau Family Capstone Print Packet

Generated: 2026-05-03
Packet folder: `/mnt/c/Users/Tony/Documents/GitHub/chalumeau`

## File Map

| File | Purpose |
| --- | --- |
| `design.md` | Project intent, catalog metadata, assumptions, and validation plan. |
| `bom.csv` | Starter bill of materials with part categories, quantities, drawing refs, and notes. |
| `sourcing.csv` | Supplier/search tracker with specs, price/date fields, lead time, substitutes, and risks. |
| `cut-list.csv` | Rough/final stock sizes, material, grain/orientation, operations, yield, and offcuts. |
| `drawing-brief.md` | Manufacturing drawing and technical product sketch brief. |
| `assembly-manual.md` | Shop-facing sequence, tools, fixtures, safety, tuning, finishing, and maintenance notes. |
| `validation.csv` | Target/measured values, tolerance, environment, result, and tuning/build action log. |
| `supplier-rfq.md` | Supplier email/request-for-quote starter. |
| `visual-bom-brief.md` | Art direction for an image-forward visual BOM. |
| `wolfram-starter.wl` | Wolfram starter for physics, optimization, visualization, and validation. |
| `README.md` | Project artifact. |
| `SKILLS.md` | Project artifact. |
| `family-spec.csv` | Project artifact. |
| `image-attributions.md` | Project artifact. |

<div class="page-break"></div>

## design.md

Project intent, catalog metadata, assumptions, and validation plan.

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
- Attributed inspiration/reference photos: `images/chalumeau1.jpg` and
  `images/chalumeau5.jpg`, from Petr Skalicky / Dudy.eu:
  `https://www.dudy.eu/chalumeau.php`
- Additional local inspiration image: `images/7173-372-1_1920x1080.avif`
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

<div class="page-break"></div>

## bom.csv

Starter bill of materials with part categories, quantities, drawing refs, and notes.

| item_no | subsystem | part_name | qty | material_spec | dimensions_spec | make_buy | estimated_cost | drawing_ref | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Body | Turned chalumeau body blanks | 4 | Cherry or hard maple for first pass; ipe/cocobolo/boxwood for keeper builds | see family-spec.csv blank_length_in and turning_blank_in | make | 80 | drawings/chalumeau-family-sheet.svg | Use lower-cost domestic hardwood for bore and keywork tests before dense/oily woods. |
| 2 | Bore | Long drill and reamer set | 1 | Aircraft-length brad point/twist drills plus adjustable/shell reamers | 0.500, 0.625, 0.750, 0.875 in bore targets | buy | 120 | cnc/cnc-lathe-plan.md | Exact tooling depends on whether bores are drilled solid or routed as split blanks. |
| 3 | Mouthpiece | Single-reed mouthpieces | 4 | Purchased clarinet/sax mouthpiece adapted by size, or shop-made Delrin mouthpiece | socket IDs in family-spec.csv; reed table in design.md | buy first, make later | 160 | drawing-brief.md | Use bought mouthpieces/reeds to isolate body acoustics before making reeds. |
| 4 | Tone holes | Raised tone-hole collars or drilled holes | 36 | Integral turned collars for visual style; chamfered holes for first prototype | see data/tone-hole-schedule.csv | make | 20 | drawings/chalumeau-soprano-c4-dimensioned.svg | Collars are visual and ergonomic; pitch comes from hole center, diameter, and chimney. |
| 5 | Keywork | Two-key chalumeau lever set | 4 | 0.040-0.062 in brass/nickel silver sheet, 1/16 in pivot rod, phosphor bronze spring | K01 and K02 per variant; see hardware/keywork-parts.csv | make | 60 | drawings/keywork-lever-detail.svg | The first soprano can be built keyless, then retrofitted with keys. |
| 6 | Pads | Leather/cork/felt pad stack | 12 | Clarinet-style skin pads or cork backed with thin leather | pad OD = tone hole OD + 0.080 to 0.125 in | buy or make | 35 | hardware/lever-fabrication-guide.md | Use leak light or suction test before tuning. |
| 7 | Finish | Oil/shellac finish and bore oil | 1 | Dewaxed shellac outside; bore oil compatible with chosen wood | finish schedule in assembly-manual.md | buy | 30 | assembly-manual.md | Avoid thick finish buildup inside tone holes or under pads. |

<div class="page-break"></div>

## sourcing.csv

Supplier/search tracker with specs, price/date fields, lead time, substitutes, and risks.

| component | required_spec | search_terms | supplier_candidates | date_checked | unit_price | lead_time | substitute_rule | risk_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Domestic hardwood prototype blanks | Straight-grain cherry, hard maple, or walnut; 1.5-2.25 in square; length per family-spec.csv | turning blank cherry hard maple 2x2x18 2x2x30 | local hardwood dealer, Bell Forest, Cook Woods, Woodcraft | not live-checked | research before purchase | research before purchase | Any stable fine-grained hardwood is acceptable for first acoustic prototypes. | Soft woods dent around tone holes and key posts; use for process tests only. |
| Dense keeper-build blanks | Ipe, cocobolo, boxwood, rosewood, grenadilla substitute; dry and crack-free | ipe turning blank cocobolo clarinet blank boxwood woodwind blank | Gilmer Wood, Cook Woods, Bell Forest, specialty woodwind blank suppliers | not live-checked | research before purchase | research before purchase | Delrin/acetal is acceptable for dimensional-stability testing. | Allergenic/oily woods need dust control, wiping before glue, and finish tests. |
| Single reeds and mouthpieces | Soprano/alto use clarinet-like reeds; tenor/bass may use sax/low clarinet reeds or custom mouthpiece | clarinet mouthpiece blank baroque clarinet reed tenor chalumeau mouthpiece | woodwind suppliers, early-music makers, 3D print/Delrin shop-made option | not live-checked | research before purchase | research before purchase | Use commercial reed first to decouple reed-making from bore tuning. | Reed strength and mouthpiece volume can shift pitch and response significantly. |
| Brass/nickel-silver key stock | 0.040-0.062 in sheet, 1/16 in rod, 0-80 or M1.6 screws, post stock | nickel silver sheet woodwind key rod phosphor bronze spring wire | McMaster-Carr, K&S metals, MusicMedic, instrument repair suppliers | not live-checked | research before purchase | research before purchase | Brass is easier to prototype; nickel silver wears better and solders cleanly. | Tiny screws strip easily; buy extras and make drill guides. |
| Pads, cork, felt, leather | Clarinet/sax pads or leather-over-cork pads sized to K01/K02 tone holes | clarinet pads sheet cork felt key bumper leather pad cup | MusicMedic, Ferree's Tools, instrument repair suppliers | not live-checked | research before purchase | research before purchase | Cork plus thin leather is acceptable for first handmade keys. | Pad seating matters more than pad material for early prototypes. |

<div class="page-break"></div>

## cut-list.csv

Rough/final stock sizes, material, grain/orientation, operations, yield, and offcuts.

| part_id | variant | material | qty | rough_dimensions_in | final_dimensions_in | operation | grain_orientation | yield_notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-SOP-C4-BODY | Soprano C | prototype hardwood | 1 | 1.25 x 1.25 x 14.172 | OD 0.875; bore 0.5; body length 12.672 | lathe turn, drill/ream bore, drill tone holes, final tune | long grain parallel to bore | leave 1.5 in length allowance and 0.1875 in OD cleanup allowance |
| CLM-SOP-C4-BELL | Soprano C | contrasting hardwood or same blank offcut | 1 | 2.025 x 2.025 x 3.000 | bell OD 1.65; socket fits bore/body OD by CAD | lathe turn bell flare and socket | long grain parallel to bore | use a separate bell to simplify tuning and repair |
| CLM-ALT-G3-BODY | Alto G | prototype hardwood | 1 | 1.438 x 1.438 x 18.439 | OD 1.063; bore 0.625; body length 16.939 | lathe turn, drill/ream bore, drill tone holes, final tune | long grain parallel to bore | leave 1.5 in length allowance and 0.1875 in OD cleanup allowance |
| CLM-ALT-G3-BELL | Alto G | contrasting hardwood or same blank offcut | 1 | 2.325 x 2.325 x 3.000 | bell OD 1.95; socket fits bore/body OD by CAD | lathe turn bell flare and socket | long grain parallel to bore | use a separate bell to simplify tuning and repair |
| CLM-TEN-C3-BODY | Tenor C | prototype hardwood | 1 | 1.625 x 1.625 x 26.983 | OD 1.25; bore 0.75; body length 25.483 | lathe turn, drill/ream bore, drill tone holes, final tune | long grain parallel to bore | leave 1.5 in length allowance and 0.1875 in OD cleanup allowance |
| CLM-TEN-C3-BELL | Tenor C | contrasting hardwood or same blank offcut | 1 | 2.725 x 2.725 x 3.000 | bell OD 2.35; socket fits bore/body OD by CAD | lathe turn bell flare and socket | long grain parallel to bore | use a separate bell to simplify tuning and repair |
| CLM-BAS-F2-BODY | Bass F | prototype hardwood | 1 | 1.875 x 1.875 x 39.82 | OD 1.5; bore 0.875; body length 38.32 | lathe turn, drill/ream bore, drill tone holes, final tune | long grain parallel to bore | leave 1.5 in length allowance and 0.1875 in OD cleanup allowance |
| CLM-BAS-F2-BELL | Bass F | contrasting hardwood or same blank offcut | 1 | 3.275 x 3.275 x 3.000 | bell OD 2.9; socket fits bore/body OD by CAD | lathe turn bell flare and socket | long grain parallel to bore | use a separate bell to simplify tuning and repair |

<div class="page-break"></div>

## drawing-brief.md

Manufacturing drawing and technical product sketch brief.

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
| Hole X from bell | `data/tone-hole-schedule.csv` | +/- 0.020 in first prototype |
| Hole diameter | `data/tone-hole-schedule.csv` | start undersize; final by tuning |
| Pad seat flatness | `hardware/keywork-parts.csv` | no visible leak |
| Pivot alignment | keywork drawing | lever moves freely without side shake |

## Drawing Outputs In This Packet

- `drawings/chalumeau-family-sheet.svg`
- `drawings/chalumeau-soprano-c4-dimensioned.svg`
- `drawings/keywork-lever-detail.svg`

## Notes For SolidWorks

Drive dimensions from global variables. Do not dimension hole centers
manually in separate sketches unless the dimension names match the CSV.

<div class="page-break"></div>

## assembly-manual.md

Shop-facing sequence, tools, fixtures, safety, tuning, finishing, and maintenance notes.

# Chalumeau Assembly Manual

## Build Order

Build the soprano C keyless version first. Do not add keywork until the
bore, reed, and seven front holes speak reliably.

## Phase 0 - Design Freeze

1. Pick the exact reed and mouthpiece.
2. Print `data/tone-hole-schedule.csv` and mark which holes will be
   drilled in the first pass.
3. Decide whether the prototype uses raised collars or plain chamfered
   holes. Plain holes tune faster; collars match the inspiration photo.
4. Confirm the blank dimensions from `cut-list.csv`.

## Phase 1 - Body Blank And Bore

1. Mill/turn the blank oversize and mark the bore centerline.
2. Drill the bore from the reed-seat end with the longest stable drill
   setup available.
3. Ream or lap to final bore diameter. Measure at both ends.
4. Turn the exterior body profile, leaving extra length at the bell end.
5. Cut the mouthpiece socket/tenon but keep the reed setup removable.

## Phase 2 - Root Tuning

1. Assemble reed, mouthpiece, and body with all holes undrilled.
2. Measure the all-closed pitch.
3. Trim the bell/foot in small steps only after the reed is stable.
4. Record every trim amount in `validation.csv`.

## Phase 3 - Tone Holes

1. Lay out hole centers from `data/tone-hole-schedule.csv`, measuring
   from `DATUM_BELL_FACE`.
2. Center punch lightly. A wandering bit will change tuning.
3. Drill each hole 15-25 percent undersize.
4. Open holes from low to high. After each enlargement, play the target
   note and log measured frequency.
5. Chamfer only after pitch is close; chamfering can sharpen the note.

## Phase 4 - Optional K01/K02 Keywork

1. Drill keyed tone holes undersize.
2. Fabricate levers using `hardware/lever-fabrication-guide.md`.
3. Install posts and pivot rods.
4. Seat pads and leak-test before tuning.
5. Tune keyed notes after the pad seal is stable.

## Phase 5 - Finish

1. Sand exterior through 320 or finer.
2. Seal the bore lightly; avoid thick buildup.
3. Apply shellac/oil finish outside.
4. Keep finish out of tone holes and under pads.
5. Re-test all notes after finish cures.

## Maintenance Notes

- Swab the bore after playing.
- Check pad seating after humidity swings.
- Keep a build log for each reed/mouthpiece combination; reed strength
  can make the same body read sharp or flat.

<div class="page-break"></div>

## validation.csv

Target/measured values, tolerance, environment, result, and tuning/build action log.

| test_id | variant | target | target_value | measured_value | tolerance | environment | result | action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-001 | all | A4 reference | 440.00 Hz |  | tuner reads 440 within calibration | record temp F, humidity percent |  | Calibrate tuner/mic before instrument data. |
| VAL-010 | Soprano C | all holes closed | C4, 261.63 Hz |  | +/- 15 cents before final tuning; +/- 8 cents after | 68-72 F preferred |  | Trim bell end shorter to sharpen; add temporary tape/extension if sharp. |
| VAL-020 | all | tone-hole sweep | each row in data/tone-hole-schedule.csv |  | +/- 12 cents after tuning | same reed, same mouthpiece, same blowing pressure |  | Open hole diameter to sharpen; use wax/tape collar to flatten during tests. |
| VAL-030 | keyed builds | pad leak test | no visible leak under leak light; suction holds 10 s |  | zero audible hiss at normal blowing pressure | before final tone-hole tuning |  | Reseat pad, regulate cork, or lap tone-hole rim. |
| VAL-040 | experimental register key | overblown twelfth check | note + 19 semitones if vent is clarinet-like |  | document response only; not a first-build pass/fail | same reed and embouchure as low-register test |  | Move/resize vent only after the core chalumeau speaks well. |

<div class="page-break"></div>

## supplier-rfq.md

Supplier email/request-for-quote starter.

# Supplier RFQ - Chalumeau Materials And Keywork

Hello,

I am sourcing materials for a small family of handmade single-reed
chalumeaux. Please quote the items below, including unit price, volume
price if applicable, lead time, shipping estimate, and any recommended
substitutes.

## Wood Or Plastic Blanks

- Straight-grain turning blanks suitable for woodwind bodies.
- Prototype species: cherry, hard maple, walnut, or Delrin/acetal.
- Keeper species: ipe, boxwood, cocobolo, rosewood, or grenadilla
  substitute.
- Sizes range from about 1.25 x 1.25 x 15 in to 2.25 x 2.25 x 41 in.
  Exact dimensions are in `cut-list.csv`.

## Keywork Materials

- Brass or nickel-silver sheet, 0.040-0.062 in thick.
- 1/16 in rod or equivalent pivot stock.
- Small screws, post stock, and phosphor bronze spring wire.
- Clarinet/sax pads or pad leather/cork materials.

## Requirements

- Material must be stable, dry, and suitable for fine drilling/turning.
- Please identify any allergy/dust or finish compatibility concerns.
- Substitutions are acceptable if dimensional stability and machinability
  are comparable.

Thank you.

<div class="page-break"></div>

## visual-bom-brief.md

Art direction for an image-forward visual BOM.

# Visual BOM Brief

## Layout

Use the Ashiko visual BOM pattern: hero image at the top, spreadsheet
rows below, and one part image/render per row. Use the actual local
chalumeau photos for the hero/inspiration image until Tony has shop
photos of the prototypes.

## Real Images Available

- `images/chalumeau1.jpg`: full instrument inspiration, attributed to
  Petr Skalicky / Dudy.eu, `https://www.dudy.eu/chalumeau.php`.
- `images/chalumeau5.jpg`: close-up of raised collars and wood finish,
  attributed to Petr Skalicky / Dudy.eu, `https://www.dudy.eu/chalumeau.php`.
- `images/7173-372-1_1920x1080.avif`: additional inspiration image,
  not universally supported by all renderers.

## Part Rows To Show

1. Turned body blank.
2. Mouthpiece/reed assembly.
3. Bell.
4. H01-H07 tone-hole row with raised collars.
5. K01 low semitone lever.
6. K02 side chromatic lever.
7. Pad/cork/felt stack.
8. Pivot posts, rods, springs, screws.
9. Finish and bore oil.

## Placeholder Policy

Generated or schematic part images are acceptable for planning, but mark
them as placeholders until replaced with supplier images or shop photos.
Build-critical dimensions must come from the CSV/workbook/SolidWorks,
not from pixels in the visual BOM.

<div class="page-break"></div>

## wolfram-starter.wl

Wolfram starter for physics, optimization, visualization, and validation.

```wolfram
(* Chalumeau family acoustic starter - generated 2026-05-03 *)

ClearAll["Global`*"];

speedOfSoundInPerSec = 13552.0;
midiFrequency[m_] := 440*2^((m - 69)/12);
centsError[measured_, target_] := 1200*Log2[measured/target];

bodyLength[rootMidi_, boreID_] := Module[
  {f = midiFrequency[rootMidi], acoustic, bellCorr, reedCorr},
  acoustic = speedOfSoundInPerSec/(4*f);
  bellCorr = 0.61*(boreID/2);
  reedCorr = 0.25*boreID;
  acoustic - bellCorr - reedCorr
];

holeXFromBell[rootMidi_, offset_, boreID_, holeRatio_] := Module[
  {f = midiFrequency[rootMidi + offset], holeDia, holeCorr, reedCorr, eff, body},
  holeDia = boreID*holeRatio;
  holeCorr = 0.30*holeDia;
  reedCorr = 0.25*boreID;
  eff = speedOfSoundInPerSec/(4*f);
  body = bodyLength[rootMidi, boreID];
  body - (eff - reedCorr - holeCorr)
];

variants = {
  <|"ID" -> "CLM-SOP-C4", "RootMIDI" -> 60, "BoreID" -> 0.500|>,
  <|"ID" -> "CLM-ALT-G3", "RootMIDI" -> 55, "BoreID" -> 0.625|>,
  <|"ID" -> "CLM-TEN-C3", "RootMIDI" -> 48, "BoreID" -> 0.750|>,
  <|"ID" -> "CLM-BAS-F2", "RootMIDI" -> 41, "BoreID" -> 0.875|>
};

holeOffsets = {1, 2, 4, 5, 7, 9, 10, 11, 12};
holeRatios = {0.32, 0.36, 0.38, 0.34, 0.38, 0.40, 0.30, 0.34, 0.32};

familyTable = Table[
  With[{v = variants[[i]]},
    <|
      "ID" -> v["ID"],
      "RootHz" -> midiFrequency[v["RootMIDI"]],
      "BodyLengthIn" -> bodyLength[v["RootMIDI"], v["BoreID"]],
      "HolePositionsFromBellIn" -> MapThread[
holeXFromBell[v["RootMIDI"], #1, v["BoreID"], #2]&,
{holeOffsets, holeRatios}
      ]
    |>
  ],
  {i, Length[variants]}
];

Dataset[familyTable]

Manipulate[
  Plot[
    speedOfSoundInPerSec/(4*(x + 0.61*(bore/2) + 0.25*bore)),
    {x, 4, 42},
    PlotRange -> {80, 700},
    AxesLabel -> {"Body length (in)", "Frequency (Hz)"},
    PlotLabel -> "Stopped cylindrical reed bore first-pass model"
  ],
  {{bore, 0.5, "Bore ID (in)"}, 0.35, 1.0}
]
```

<div class="page-break"></div>

## README.md

Project artifact.

# Chalumeau Family

> A build-ready design packet for a family of single-reed chalumeaux:
> keyless folk-pipe simplicity first, optional handmade two-key metalwork
> second, and a documented path toward clarinet-style register experiments.

![Inspiration chalumeau with turned wood body, raised tone-hole collars, black mouthpiece, and flared bell](images/chalumeau1.jpg)
*Photo/reference instrument by Petr Skalicky / Dudy.eu, from
[dudy.eu/chalumeau.php](https://www.dudy.eu/chalumeau.php). Used here
as an attributed design reference, not as Tony's own build photo.*

## GitHub Repo Metadata

**Description:** Parametric build packet for a handmade chalumeau family,
including stopped-reed acoustics, tone-hole schedules, SolidWorks design
tables, and DIY keywork.

**Suggested topics:** `chalumeau`, `woodwind`, `single-reed`,
`clarinet-history`, `instrument-making`, `parametric-design`,
`solidworks`, `acoustic-modeling`, `cnc-lathe`, `woodworking`,
`music-technology`, `build-packet`

## What this is

This repository now contains a complete first-pass engineering packet for
designing and building a family of chalumeaux in soprano C, alto G, tenor
C, and bass F. The design is parametric: body length, bore, tone-hole
positions, and optional levers are driven from formulas rather than
hidden one-off dimensions.

The packet starts from attributed Dudy.eu chalumeau reference photos in
`images/`, Tony's `Musical Instruments.xlsx` workbook, and especially
the reed/bore lessons in the `Great Highland Bagpipe` sheet. The
acoustic model is not copied from Native American style flute K2
corrections. A chalumeau is a cylindrical, single-reed, effectively
stopped pipe, so it gets its own validation loop.

## Family plan

| ID | Variant | Root | Bore ID | Final body L | Blank L | Sections |
| --- | --- | --- | --- | --- | --- | --- |
| CLM-SOP-C4 | Soprano C | C4 | 0.5 | 12.672 | 14.172 | 1 body + mouthpiece + bell |
| CLM-ALT-G3 | Alto G | G3 | 0.625 | 16.939 | 18.439 | 1 body + mouthpiece + bell |
| CLM-TEN-C3 | Tenor C | C3 | 0.75 | 25.483 | 26.983 | 2 body joints + mouthpiece + bell |
| CLM-BAS-F2 | Bass F | F2 | 0.875 | 38.32 | 39.82 | 3 body joints + mouthpiece + bell |

The recommended build order is `CLM-SOP-C4` first, with no levers, using
a commercial reed/mouthpiece. Once that speaks cleanly, add the two
optional levers to the same body or a second soprano body. Then scale up
to alto, tenor, and bass.

## Why some have levers

Keyless chalumeaux are mechanically close to folk reed pipes: finger
holes cover the notes that are reachable by hand. A few levers appear
when a useful tone hole is too low, too high, too large, or too awkward
to cover directly. The historical two-key chalumeau/early clarinet
moment is exactly that transition: keys first helped extend and smooth
the low register, then the clarinet moved one key into a better register
vent position and gradually accumulated more keys for chromatic notes,
trills, low extensions, and better intonation.

## Packet map

- `chalumeau-family-design-table.xlsx`: Excel design workbook with blue
  inputs and formulas.
- `family-spec.csv`: one row per family member.
- `data/tone-hole-schedule.csv`: calculated tone-hole and keyed-hole
  positions.
- `design.md`: governing model, assumptions, keywork strategy, and risk
  register.
- `hardware/lever-fabrication-guide.md`: how to make the metal levers,
  pads, pivots, and springs yourself.
- `cad/solidworks-design-table.csv`: SolidWorks configuration table.
- `cad/solidworks-global-variables.md`: variable naming conventions and
  equation pattern.
- `drawings/`: SVG drawing sheets for the family, soprano C, and keywork.
- `assembly-manual.md`, `bom.csv`, `sourcing.csv`, `cut-list.csv`,
  `validation.csv`, `supplier-rfq.md`: shop-facing build packet files.
- `wolfram-starter.wl`: Wolfram starter for acoustic sweeps and tuning
  validation.
- `capstone-deck.pptx` and `print-packet.pdf`: presentation and printable
  versions of the packet.

## Status

| Area | Status |
| --- | --- |
| Acoustic model | first-order stopped cylindrical reed model complete |
| Parametric family table | complete, with formulas and SolidWorks export |
| Keywork concept | two-key handmade lever system specified |
| Manufacturing drawings | SVG first-pass sheets complete |
| Shop build method | complete for prototype workflow |
| Tuning validation | template ready; needs measured prototype data |
| SolidWorks | variable conventions and design table ready |

## License

Released under [CC-BY 4.0](LICENSE) for original written/design content
in this repository. The Dudy.eu reference photos are attributed source
images, not Tony-owned build photos; replace them with shop photos as
prototypes are built.

<div class="page-break"></div>

## SKILLS.md

Project artifact.

# Skills Demonstrated

## stopped-cylindrical-reed-bore

Models a single-reed cylindrical bore as a stopped pipe in the low
register, with explicit reed and bell end-correction assumptions.

## handmade-woodwind-keywork

Designs and fabricates simple early-woodwind levers using brass or
nickel silver, pivot rods, pads, posts, and springs.

## solidworks-parametric-family-table

Uses one design table to drive multiple instrument-family
configurations, with stable named dimensions that match CSV, drawings,
and validation logs.

## empirical-tone-hole-validation

Starts with physics-derived hole positions, then tunes the real
prototype by measured frequency and cents error rather than trusting the
first-pass model blindly.

<div class="page-break"></div>

## family-spec.csv

Project artifact.

| instrument_id | variant | root_note | root_midi | root_frequency_hz | bore_id_in | wall_thickness_in | body_od_in | bell_od_in | acoustic_length_in | body_length_final_in | blank_length_in | turning_blank_in | sections | build_priority | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-SOP-C4 | Soprano C | C4 | 60 | 261.63 | 0.5 | 0.188 | 0.875 | 1.65 | 12.95 | 12.672 | 14.172 | 1.25 x 1.25 x 14.172 | 1 body + mouthpiece + bell | Prototype 1 | first-order design; validate after reed and bore prototype |
| CLM-ALT-G3 | Alto G | G3 | 55 | 196.0 | 0.625 | 0.219 | 1.063 | 1.95 | 17.286 | 16.939 | 18.439 | 1.438 x 1.438 x 18.439 | 1 body + mouthpiece + bell | Prototype 2 | first-order design; validate after reed and bore prototype |
| CLM-TEN-C3 | Tenor C | C3 | 48 | 130.81 | 0.75 | 0.25 | 1.25 | 2.35 | 25.9 | 25.483 | 26.983 | 1.625 x 1.625 x 26.983 | 2 body joints + mouthpiece + bell | Prototype 3 | first-order design; validate after reed and bore prototype |
| CLM-BAS-F2 | Bass F | F2 | 41 | 87.31 | 0.875 | 0.313 | 1.5 | 2.9 | 38.806 | 38.32 | 39.82 | 1.875 x 1.875 x 39.82 | 3 body joints + mouthpiece + bell | Stretch prototype | first-order design; validate after reed and bore prototype |

<div class="page-break"></div>

## image-attributions.md

Project artifact.

# Image Attributions

## Dudy.eu Chalumeau Reference Photos

- `images/chalumeau1.jpg`
- `images/chalumeau5.jpg`

Attribution: Petr Skalicky / Dudy.eu, chalumeau reference page:
https://www.dudy.eu/chalumeau.php

Use in this repo: attributed visual reference for form, finish, raised
tone-hole collars, mouthpiece layout, and bell styling. These are not Tony's
own build photos.

## Additional Local Inspiration Image

- `images/7173-372-1_1920x1080.avif`

Attribution/source: TBD. Keep as local inspiration only until provenance is
confirmed or replace with shop-generated imagery.

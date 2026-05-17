# Chalumeau Prototype Validation Loop

This loop keeps the current chalumeau packet at prototype readiness until
real measurements prove the reed, mouthpiece, bore, tone holes, and player
response. CAD tables, drawings, and generated visuals are planning aids until
their dimensions are reconciled with measured shop data.

## Gate Summary

| Gate | Evidence file | Pass condition | Blocks |
| --- | --- | --- | --- |
| P0 reed/mouthpiece setup | `../data/reed-mouthpiece-capture-template.csv` | one stable `reed_id` and `mouthpiece_id` chosen, with onset and response notes recorded | root pitch claims |
| P1 bore/root tuning | `../data/bore-trim-capture-template.csv` | bore stations measured, datum confirmed, all-closed C4 within +/- 15 cents before final tuning | final tone-hole drilling |
| P2 tone-hole tuning | `../data/tuning-capture-template.csv` | H01-H07 measured with same `reed_id`, `mouthpiece_id`, and `bore_profile_id`; final rows within +/- 12 cents | family scaling |
| P3 keywork seal | `validation.csv` plus build photos or leak notes | K01/K02 pads pass leak-light or suction check before pitch rows are trusted | keyed-note claims |
| P4 scale-up decision | revised design table or correction notes | empirical correction is documented from P1/P2 before alto, tenor, or bass dimensions are promoted | larger-family builds |

## P0 - Reed And Mouthpiece Setup

1. Choose a commercial reed and mouthpiece for the first soprano C test.
2. Assign stable IDs such as `REED-001` and `MP-001`.
3. Record reed strength, soak state, mouthpiece facing if known, ligature,
   onset pressure, response rating, and any chirp/squeak behavior in
   `../data/reed-mouthpiece-capture-template.csv`.
4. Use the same IDs in the bore and tuning logs. If either changes, start a
   new `session_id` instead of mixing measurements.

## P1 - Bore And Root Tuning

1. Measure the bore at the reed seat, mid-bore, and bell face before tone-hole
   layout.
2. Record body length before every trim, body length after every trim, and the
   all-closed measured frequency in `../data/bore-trim-capture-template.csv`.
3. Treat the all-closed root as provisional until the reed response is stable.
4. Do not drill final tone-hole diameters until the datum, bore, and root row
   are internally consistent.

## P2 - Tone-Hole Tuning

1. Drill holes 15-25 percent undersize.
2. Tune from the bell upward, logging each diameter change and measured
   frequency in `../data/tuning-capture-template.csv`.
3. Keep `dynamic_level` consistent, starting with `mp`, so pitch rows compare
   like with like.
4. If response drops below `3` on the 1-5 scale, fix leak, reed, or hole
   behavior before treating cents error as a geometry problem.

## P3 - Keywork And Register Experiments

K01 and K02 are allowed only after the keyless low register speaks reliably.
Record leak-light or suction results in `validation.csv` before trusting keyed
pitch rows. The register vent remains experimental and should be documented as
response research, not a first-build pass/fail requirement.

## Claim Boundary

Until P0-P2 contain measured data, this repo should describe the chalumeau as a
first-pass prototype packet with validation templates. Do not call it
build-ready, L3, L4, empirically tuned, or production-ready until the measured
logs and revised authority tables support those claims.

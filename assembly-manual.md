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

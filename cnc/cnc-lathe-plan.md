# CNC And Lathe Plan

## Preferred First Prototype Method

Use the lathe/drill-ream workflow for the soprano C prototype. The bore
is short enough that a solid blank is practical and easier to validate
than a split-blank glue-up.

## Operations

1. Square and center the blank.
2. Drill pilot bore from reed-seat end.
3. Step drill/ream to target bore ID.
4. Turn exterior cylinder and ornamental beads/collars.
5. Cut mouthpiece socket and bell tenon/socket.
6. Mark hole centers from bell datum using a V-block or rotary index.
7. Drill holes undersize on drill press or CNC with a cradle fixture.
8. Tune holes by hand reaming.
9. Add keywork post holes only after key lever geometry is confirmed.

## CNC Fixture Concept

- V-block cradle with two dowel pin datums.
- Bore axis parallel to X.
- Bell face against a fixed stop for `DATUM_BELL_FACE`.
- Rotary/indexing marks for front-hole plane and side-key plane.
- Use a peck cycle for clean hole walls; back up the bore with a
  removable mandrel if tearout appears.

## Tooling Notes

- Long drill bits must be checked for runout.
- Ream/lap the bore after drilling; do not rely on twist drill diameter.
- Keep tone-hole drills small for first pass and open by hand.
- For bass, consider split-blank routing if long drilling wanders.

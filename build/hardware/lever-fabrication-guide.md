# Handmade Chalumeau Lever Fabrication Guide

## Goal

Make small metal levers that behave like early woodwind keys: a spring
keeps a pad closed over a tone hole, and the player's finger presses a
touchpiece to open it.

## Recommended Prototype Materials

| Part | Prototype spec | Keeper-build upgrade |
| --- | --- | --- |
| Lever arm | 0.040-0.062 in brass strip | nickel silver strip |
| Pivot | 1/16 in brass rod or shoulder screw | hardened rod between turned posts |
| Posts | brass tube/rod, screwed or epoxied into body | silver-soldered post feet and screws |
| Spring | 0.012-0.018 in phosphor bronze wire | blued needle spring or flat spring |
| Pad cup | brass washer/cup soldered to arm | spun/soldered cup |
| Pad | cork with thin leather facing | clarinet-style skin pad |
| Regulation | cork/felt bumper | cork/felt plus adjustment screw |

## Simple K01/K02 Construction

1. Drill the keyed tone hole undersize and leave the rim proud enough to
   sand flat.
2. Turn or file a flat pad seat around the hole. A pad cannot seal on a
   lumpy collar.
3. Make a paper lever pattern. The touchpiece should sit under a natural
   finger motion, while the pad cup centers over the tone hole.
4. Cut the lever from brass strip. Round every player-facing edge.
5. Solder or rivet a small pad cup/washer to the pad end.
6. Drill the pivot hole. Ream until the lever rotates freely on the rod
   without side shake.
7. Mount two posts on the body. Use a drill guide so both post holes are
   square to the bore centerline.
8. Install the lever and spring. The default state for K01/K02 is pad
   closed; pressing the lever opens the tone hole.
9. Add cork or felt stops so the lever opens only 0.060-0.100 in beyond
   acoustic clearance.
10. Seat the pad with shellac or contact cement. Check with a leak light
    or suction test before tuning.

## Pad Geometry Rule

Pad OD should be the tone-hole diameter plus 0.080-0.125 in. The pad cup
should not hit the body before the pad compresses. Keep the pad travel
low; huge key lift feels sloppy and slows the action.

## Spring Options

- Flat spring: easiest for a first prototype. Screw or rivet one end to
  the lever/body and let the free end bias the lever closed.
- Needle spring: better action, but requires a spring cradle or post.
- Elastic/thread return: useful for a temporary test, not a final build.

## SolidWorks Modeling Notes

Model each key as a subassembly:

- `Key_K01_Lever`
- `Key_K01_Post_A`
- `Key_K01_Post_B`
- `Key_K01_Pad`
- `Key_K01_Spring`

Mate the lever concentric to `CLM_Key_Pivot_Rod_Dia_in`. Add an angular
limit mate for closed/open positions. Keep pad compression as an
explicit variable, not an accidental interference.

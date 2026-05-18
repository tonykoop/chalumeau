# Chalumeau Family

> Bare-bones readiness packet for a family of single-reed chalumeaux:
> keyless folk-pipe simplicity first, optional handmade two-key metalwork
> second, and a documented path toward clarinet-style register experiments.
> The current repo is an L2 scaffold, not a build-ready or measured packet.

![Inspiration chalumeau with turned wood body, raised tone-hole collars, black mouthpiece, and flared bell](assets/images/chalumeau1.jpg)
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

This repository now contains a first-pass engineering packet for
designing and prototyping a family of chalumeaux in soprano C, alto G,
tenor C, and bass F. The design is parametric: body length, bore,
tone-hole positions, and optional levers are driven from formulas rather
than hidden one-off dimensions. It is not yet a build-ready or
empirically validated packet; the first soprano prototype still needs
measured reed, mouthpiece, bore, tuning, and response data.

The packet starts from attributed Dudy.eu chalumeau reference photos in
`assets/images/`, Tony's `Musical Instruments.xlsx` workbook, and especially
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

## Root starter packet

These root-level files are the review entry point for the current bare-bones
packet. They keep missing measurements and authority gaps visible before anyone
uses the deeper `build/` artifacts for shop work.

- [`design.md`](design.md) - current assumptions, acoustic boundary, evidence map, and promotion gates.
- [`bom.csv`](bom.csv) - starter material/components list with source and authority status.
- [`validation.csv`](validation.csv) - gates that must pass before L3/build-ready claims.
- [`risks.md`](risks.md) - acoustic, fabrication, sourcing, keywork, and documentation risks.
- [`photo-shotlist.md`](photo-shotlist.md) - future public-safe prototype documentation shots.
- [`capstone-manifest.json`](capstone-manifest.json) - root packet metadata and release gates.

## Existing build packet map

- [`build/packet/`](build/packet/) - design narrative, BOM, sourcing, cut list, validation loop, validation gates, assembly, RFQ, drawing/visual briefs, and Wolfram starter.
- [`build/presentation/`](build/presentation/) - capstone deck, printable packet, HTML/PDF exports, and manifest.
- [`build/design-tables/`](build/design-tables/) - Excel and SolidWorks-ready design tables.
- [`build/drawings/`](build/drawings/) - dimensioned drawing sheets and drawing exports.
- [`build/cad/`](build/cad/) - CAD/OpenSCAD/SolidWorks source and exports.
- [`build/cnc/`](build/cnc/) - CNC/CAM plans, setup sheets, fixtures, and toolpaths.
- [`build/hardware/`](build/hardware/) - handmade lever/keywork parts, guides, and hardware tables.
- [`assets/images/`](assets/images/) - photos, attributed references, concept art, and generated visuals.
- [`docs/`](docs/) - attribution, provenance, research, handoff notes, and reorganization manifest.

## Status

| Area | Status |
| --- | --- |
| Acoustic model | first-order stopped cylindrical reed model drafted; needs measured correction |
| Parametric family table | formula-derived scaffold, with SolidWorks export |
| Keywork concept | two-key handmade lever system specified |
| Manufacturing drawings | SVG first-pass sheets present; not reviewed fabrication authority |
| Shop build method | starter workflow for prototype review |
| Reed/tuning validation | capture templates and validation loop ready; needs measured prototype data |
| SolidWorks | variable conventions and design table ready |

## License

Released under [CC-BY 4.0](LICENSE) for original written/design content
in this repository. The Dudy.eu reference photos are attributed source
images, not Tony-owned build photos; replace them with shop photos as
prototypes are built.

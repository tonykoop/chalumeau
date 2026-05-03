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

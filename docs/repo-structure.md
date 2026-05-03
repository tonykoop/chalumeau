# Repository Structure

This repo uses the lean instrument-folder layout documented in [instrument-maker/docs/instrument-repo-folder-template.md](../../instrument-maker/docs/instrument-repo-folder-template.md). The goal is to keep the GitHub root short enough that the README preview is visible immediately.

```text
chalumeau/
├── README.md                   # first-reader overview
├── LICENSE
├── assets/                     # images, thumbnails, recordings
├── build/                      # packet, presentation, CAD/CNC, drawings, data
├── docs/                       # attribution, provenance, research, manifests
├── tools/                      # repo-specific generators or analysis scripts
└── .gitignore
```

The full move history for this layout is tracked in [`reorg-manifest.json`](reorg-manifest.json).

## Build Packet Locations

- [`../build/packet/`](../build/packet/) - design narrative, BOM, sourcing, cut list, validation, assembly, RFQ, drawing/visual briefs, and Wolfram starter.
- [`../build/presentation/`](../build/presentation/) - capstone deck, printable packet, HTML/PDF exports, and manifest.
- [`../build/design-tables/`](../build/design-tables/) - Excel and SolidWorks-ready design tables.
- [`../build/drawings/`](../build/drawings/) - dimensioned drawing sheets and drawing exports.
- [`../build/cad/`](../build/cad/) - CAD/OpenSCAD/SolidWorks source and exports.
- [`../build/cnc/`](../build/cnc/) - CNC/CAM plans, setup sheets, fixtures, and toolpaths.
- [`../build/hardware/`](../build/hardware/) - handmade lever/keywork parts, guides, and hardware tables.
- [`../assets/images/`](../assets/images/) - photos, attributed references, concept art, and generated visuals.
- [`./`](./) - attribution, provenance, research, handoff notes, and reorganization manifest.

## Migration Note

No source files were intentionally deleted in this reorganization. Moved paths are recorded in `reorg-manifest.json`.

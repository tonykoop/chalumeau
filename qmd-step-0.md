# QMD Step 0 Record

Date: 2026-05-30.

Commands run after syncing `main` and before edits:

```sh
qmd search "chalumeau" -c instrument-builds
timeout 25 qmd query "chalumeau V5 packet"
```

Usable keyword hits:

- `instrument-builds/docs/plans/2026-05-17-r27-merge-and-winds/elsa.md`,
  noting `tonykoop/chalumeau` PR #3, "Add chalumeau bare-bones starter packet".
- `instrument-builds/.../headstock-driven-deep-bore-drilling.md`, which names
  prototype chalumeau or reed-pipe bores as a use case for straight cylindrical
  bore drilling.

Semantic query result:

- `qmd query "chalumeau V5 packet"` crashed inside Bun/node-llama after the
  timeout, ending with `timeout: the monitored command dumped core`.

Existing repo evidence used for this migration:

- `README.md`
- `design.md`
- `build/packet/design.md`
- `build/packet/drawing-brief.md`
- `build/packet/visual-bom-brief.md`
- `docs/image-attributions.md`

No QMD result supplied measured reed data, measured bore/tuning corrections,
reviewed CAD/DXF authority, or prototype validation evidence.

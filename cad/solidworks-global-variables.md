# SolidWorks Global Variable Naming

## Naming Rules

- Prefix every chalumeau global variable with `CLM_`.
- Use stable hole IDs: `H01` through `H07` for finger holes, `K01` and
  `K02` for keyed holes.
- Include units in the name when the variable is dimensional:
  `_in`, `_deg`, `_Hz`, `_pct`.
- Use `X_Bell` for coordinates measured from the bell/foot datum and
  `X_Reed` for coordinates measured from the reed-seat datum.
- Use `Dia` for diameters and `OD`/`ID` only when the outside/inside
  distinction matters.

## Datums

| Datum | SolidWorks name | Meaning |
| --- | --- | --- |
| Bore axis | `DATUM_BORE_AXIS` | centerline of bore and turned body |
| Bell plane | `DATUM_BELL_FACE` | zero for `CLM_H##_X_Bell_in` |
| Reed seat plane | `DATUM_REED_SEAT` | zero for mouthpiece socket and reed reference |
| Front-hole plane | `DATUM_FRONT_HOLES` | angular plane for H01-H07 |
| Key side plane | `DATUM_KEY_SIDE` | angular plane for K02 and optional side levers |

## Core Variables

```text
CLM_SOS_in_per_s
CLM_Root_MIDI
CLM_Root_Hz
CLM_Bore_ID_in
CLM_Wall_T_in
CLM_Body_OD_in
CLM_Body_L_Final_in
CLM_Blank_L_in
CLM_Bell_OD_in
CLM_Mouthpiece_Socket_ID_in
CLM_Reed_Corr_in
CLM_Bell_End_Corr_in
```

## Repeated Hole Variables

```text
CLM_H01_X_Bell_in
CLM_H01_Dia_in
CLM_H01_Chimney_H_in
CLM_K01_X_Bell_in
CLM_K01_Dia_in
CLM_K01_Pad_OD_in
CLM_K01_Lever_L_in
```

## Configuration Table

Use `cad/solidworks-design-table.csv` as the seed table. In SolidWorks,
map the values either to global variables or to dimension names such as:

```text
CLM_Bore_ID_in@Sketch_Bore
CLM_Body_L_Final_in@Boss_Body
CLM_H01_X_Bell_in@Sketch_Holes
CLM_H01_Dia_in@Sketch_Holes
```

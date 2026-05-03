# Workbook Inspection Summary

Inspected workbook:

`C:/Users/Tony/Documents/Claude/Projects/Career/flutes-staging/Musical Instruments.xlsx`

Relevant source sheet:

`Great Highland Bagpipe`

Useful starting points found:

- Chanter rows document conical double-reed behavior and show why
  conical reed instruments should not be treated exactly like flutes.
- Drone rows use a cylindrical single-reed stopped-pipe model
  `f = c/(4L)`, which is closer to the chalumeau boundary condition.
- Reed rows emphasize buying/commercial reeds first, because reed-making
  skill can mask bore-design errors.
- Wood rows suggest a sensible prototype sequence: cherry/walnut/maple
  first, ipe/cocobolo/boxwood/dense woods later.

Applied decision:

The chalumeau packet uses a stopped cylindrical single-reed model and a
validation-first tone-hole schedule. It does not import Native American
flute K2 corrections or bagpipe chanter conical-bore dimensions.

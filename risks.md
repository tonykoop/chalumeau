# Chalumeau Bare-Bones Risk Register

Current status: **bare-bones readiness packet / L2 scaffold**.

This root risk register is intentionally conservative. It records what can go
wrong before the first measured soprano prototype, and it does not treat
generated tables, SVG previews, or source CAD as fabrication authority.

| Risk ID | Area | Risk | Why it matters | Mitigation / next test |
| --- | --- | --- | --- | --- |
| R-BB-001 | Acoustics | Reed and mouthpiece compliance shift the effective pipe length. | A first-pass stopped-pipe model can be wrong if the reed setup is unstable. | Select one commercial reed/mouthpiece setup and record it with every measurement. |
| R-BB-002 | Tuning | Tone-hole positions and diameters are derived estimates. | Oversized holes cannot be made smaller without repair. | Drill undersized, tune gradually, and log measured cents error in a prototype pass. |
| R-BB-003 | Boundary conditions | NAF or open-flute corrections could be misapplied. | Wrong acoustic law would make the schedule misleading. | Keep chalumeau labeled as cylindrical single-reed stopped pipe until measurement proves corrections. |
| R-BB-004 | Keywork | Handmade K01/K02 pads may leak or bind. | Leaks can make tuning data useless and response unreliable. | Validate keyless body first; then leak-light/suction-test each key before pitch logging. |
| R-BB-005 | Fabrication | CAD/OpenSCAD/SVG artifacts may be mistaken for reviewed fabrication authority. | Starter geometry can propagate unvalidated dimensions to the shop. | Declare the authority artifact only after CAD/DXF/design-table review and measured prototype feedback. |
| R-BB-006 | Materials | Dense or oily woods may crack, move, or complicate machining. | Keeper-build wood can hide process errors and introduce health hazards. | Prototype in domestic hardwood first; treat dense woods as later substitutions requiring dust/finish checks. |
| R-BB-007 | Sourcing | Supplier prices, availability, and reed compatibility are not live-checked. | Stale sourcing can derail the first build or force geometry changes. | Recheck sourcing at purchase time and record substitutions. |
| R-BB-008 | Documentation | Attributed reference photos could be mistaken for Tony build photos. | Public readers need provenance clarity. | Keep captions explicit and replace with Tony-built prototype photos when available. |

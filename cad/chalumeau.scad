// Chalumeau family — bore envelope + tone-hole schedule master.
//
// AUTHORITY: pending_measurement. NOT fabrication authority until reviewed
// against a measured soprano prototype (see README "V5 Authority Boundary"
// and validation.csv VAL-BB-050). This is a codeCAD envelope master, not a
// reviewed/released CAD/DXF artifact.
//
// SOURCE OF TRUTH (do not hand-edit numbers below without updating these):
//   - build/packet/family-spec.csv        (root, bore_id_in, wall_thickness_in,
//                                           body_od_in, bell_od_in,
//                                           body_length_final_in)
//   - build/data/tone-hole-schedule.csv   (x_from_bell_in, hole_dia_in per
//                                           variant, holes K01,H01-H05,K02,H06,H07)
//   - build/cad/solidworks-design-table.csv mirrors the same two tables in a
//     flat CLM_* column layout for SolidWorks; values here match it.
// All dimensions are inches, matching the design table's native units.
//
// SCOPE: this master models the cylindrical BORE ENVELOPE and the TONE-HOLE
// POSITION SCHEDULE only. Per the V5 woodwind addendum, the following are
// explicitly OUT OF SCOPE and are NOT modeled here — they are tuning-sensitive
// regions that must be hand-refined against a measured prototype, not faked
// with placeholder geometry:
//   - mouthpiece geometry (facing, table, rails, tip opening)
//   - reed geometry / reed-and-mouthpiece assembly
//   - reed seat / mouthpiece tenon socket cut into the body
//   - tone-hole undercutting or chimney/collar tuning profile
//   - keywork (K01/K02 lever, pad, cup, pivot, post, spring — see
//     build/hardware/keywork-parts.csv, out of scope for this envelope)
// Tone holes are modeled as simple through-bores at the schedule's
// x_from_bell / diameter values, on a single row along -Y (the schedule has
// no per-hole rotation/angle column, so no angular placement is invented).
//
// Family plan (README): build order is soprano first (no levers, commercial
// reed/mouthpiece), then alto/tenor/bass after soprano correction data.

$fn = 96;

// ---- Per-variant body dimensions (build/packet/family-spec.csv) ----
// [id, bore_id_in, wall_thickness_in, body_od_in, bell_od_in, body_length_final_in, blank_length_in]
variant_body = [
  ["CLM-SOP-C4", 0.500, 0.188, 0.875, 1.65, 12.672, 14.172],
  ["CLM-ALT-G3", 0.625, 0.219, 1.063, 1.95, 16.939, 18.439],
  ["CLM-TEN-C3", 0.750, 0.250, 1.25,  2.35, 25.483, 26.983],
  ["CLM-BAS-F2", 0.875, 0.313, 1.5,   2.9,  38.320, 39.820],
];

// ---- Tone-hole schedule (build/data/tone-hole-schedule.csv) ----
// [x_from_bell_in, hole_dia_in, label] per variant, in K01..H07 schedule order.
tone_holes_sop = [
  [0.622, 0.160, "K01"], [1.314, 0.180, "H01"], [2.576, 0.190, "H02"],
  [3.147, 0.170, "H03"], [4.211, 0.190, "H04"], [5.157, 0.200, "H05"],
  [5.574, 0.150, "K02"], [5.988, 0.170, "H06"], [6.370, 0.160, "H07"],
];
tone_holes_alt = [
  [0.840, 0.200, "K01"], [1.763, 0.225, "H01"], [3.447, 0.238, "H02"],
  [4.209, 0.213, "H03"], [5.630, 0.238, "H04"], [6.892, 0.250, "H05"],
  [7.450, 0.188, "K02"], [8.002, 0.213, "H06"], [8.512, 0.200, "H07"],
];
tone_holes_ten = [
  [1.297, 0.240, "K01"], [2.678, 0.270, "H01"], [5.200, 0.285, "H02"],
  [6.345, 0.255, "H03"], [8.470, 0.285, "H04"], [10.361, 0.300, "H05"],
  [11.203, 0.225, "K02"], [12.028, 0.255, "H06"], [12.793, 0.240, "H07"],
];
tone_holes_bas = [
  [1.995, 0.280, "K01"], [4.061, 0.315, "H01"], [7.838, 0.333, "H02"],
  [9.557, 0.298, "H03"], [12.739, 0.333, "H04"], [15.570, 0.350, "H05"],
  [16.839, 0.263, "K02"], [18.071, 0.298, "H06"], [19.220, 0.280, "H07"],
];

function variant_index(id) =
  id == "CLM-SOP-C4" ? 0 :
  id == "CLM-ALT-G3" ? 1 :
  id == "CLM-TEN-C3" ? 2 :
  id == "CLM-BAS-F2" ? 3 : -1;

function tone_holes_for(id) =
  id == "CLM-SOP-C4" ? tone_holes_sop :
  id == "CLM-ALT-G3" ? tone_holes_alt :
  id == "CLM-TEN-C3" ? tone_holes_ten :
  id == "CLM-BAS-F2" ? tone_holes_bas : [];

// Cylindrical bore envelope: straight body with a bell flare at the foot end.
// The head (mouthpiece) end is left as a bare flat face — no tenon socket or
// mouthpiece geometry is modeled (out of scope, see header).
module chalumeau_bore_envelope(body_len, bore_id, body_od, bell_od, bell_flare_len = 1.6) {
  difference() {
    union() {
      cylinder(h = body_len, d = body_od);
      // bell flare at the foot (x=0 end, matches x_from_bell datum)
      translate([0, 0, -bell_flare_len])
        cylinder(h = bell_flare_len, d1 = bell_od, d2 = body_od);
    }
    translate([0, 0, -bell_flare_len - 1])
      cylinder(h = body_len + bell_flare_len + 2, d = bore_id);
  }
}

// Single tone hole, positioned by x_from_bell along the bore axis, drilled
// radially through the wall on the -Y face (schedule has no angle column).
module tone_hole(x_from_bell, dia, body_od) {
  translate([0, -body_od / 2, x_from_bell])
    rotate([90, 0, 0])
      cylinder(h = body_od, d = dia, center = true);
}

// Full variant: bore envelope with its tone-hole schedule subtracted.
module chalumeau_variant(id) {
  vi = variant_index(id);
  assert(vi >= 0, str("unknown variant id: ", id));
  b = variant_body[vi];
  bore_id  = b[1];
  body_od  = b[3];
  bell_od  = b[4];
  body_len = b[5];
  holes    = tone_holes_for(id);

  difference() {
    chalumeau_bore_envelope(body_len, bore_id, body_od, bell_od);
    for (h = holes) {
      tone_hole(h[0], h[1], body_od);
    }
  }
}

// ---- Top-level assembly ----
// Render one variant by default (soprano, the README's first-build target).
// Set SHOW_FAMILY = true to lay out all four variants side by side for
// review; each is still pending_measurement, not a fabrication release.
SELECTED_VARIANT = "CLM-SOP-C4";
SHOW_FAMILY = false;

if (SHOW_FAMILY) {
  gap = 3;
  for (i = [0 : len(variant_body) - 1]) {
    id = variant_body[i][0];
    x_offset = i * (variant_body[3][4] + gap); // space by largest bell OD (bass) + gap
    translate([x_offset, 0, 0])
      chalumeau_variant(id);
  }
} else {
  chalumeau_variant(SELECTED_VARIANT);
}

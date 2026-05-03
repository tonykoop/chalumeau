// Chalumeau family OpenSCAD starter.
// Build-critical dimensions should be driven from SolidWorks/CSV before machining.

$fn = 96;

module chalumeau_body(body_len=12.672, bore_id=0.5, body_od=0.875, bell_od=1.65) {
  difference() {
    union() {
      cylinder(h=body_len, d=body_od);
      translate([0,0,-1.6]) cylinder(h=1.6, d1=bell_od, d2=body_od);
      translate([0,0,body_len]) cylinder(h=1.2, d=body_od*1.12);
    }
    translate([0,0,-2]) cylinder(h=body_len+4, d=bore_id);
  }
}

module tone_hole(x_from_bell, dia, body_od=0.875) {
  translate([0, -body_od/2, x_from_bell])
    rotate([90,0,0])
      cylinder(h=body_od, d=dia, center=true);
}

module soprano_c4_preview() {
  difference() {
    chalumeau_body();
    tone_hole(0.625, 0.160);
    tone_hole(1.335, 0.180);
    tone_hole(2.474, 0.190);
    tone_hole(3.004, 0.170);
    tone_hole(3.942, 0.190);
    tone_hole(4.787, 0.200);
    tone_hole(5.171, 0.150);
    tone_hole(5.544, 0.170);
    tone_hole(6.201, 0.160);
  }
}

soprano_c4_preview();

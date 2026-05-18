#!/usr/bin/env python3
"""Generate the chalumeau build packet.

This script is intentionally self-contained and uses only the Python standard
library so it can run in the lightweight Codex/WSL environment.
"""

from __future__ import annotations

import csv
import datetime as dt
import html
import json
import math
from pathlib import Path
from textwrap import dedent
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
TODAY = dt.date.today().isoformat()
SOS_IN_PER_SEC = 13552.0


NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]


VARIANTS = [
    {
        "id": "CLM-SOP-C4",
        "variant": "Soprano C",
        "root_note": "C4",
        "root_midi": 60,
        "bore_id_in": 0.500,
        "wall_in": 0.1875,
        "body_od_in": 0.875,
        "bell_od_in": 1.650,
        "mouthpiece_socket_id_in": 0.535,
        "sections": "1 body + mouthpiece + bell",
        "build_priority": "Prototype 1",
    },
    {
        "id": "CLM-ALT-G3",
        "variant": "Alto G",
        "root_note": "G3",
        "root_midi": 55,
        "bore_id_in": 0.625,
        "wall_in": 0.21875,
        "body_od_in": 1.063,
        "bell_od_in": 1.950,
        "mouthpiece_socket_id_in": 0.660,
        "sections": "1 body + mouthpiece + bell",
        "build_priority": "Prototype 2",
    },
    {
        "id": "CLM-TEN-C3",
        "variant": "Tenor C",
        "root_note": "C3",
        "root_midi": 48,
        "bore_id_in": 0.750,
        "wall_in": 0.250,
        "body_od_in": 1.250,
        "bell_od_in": 2.350,
        "mouthpiece_socket_id_in": 0.790,
        "sections": "2 body joints + mouthpiece + bell",
        "build_priority": "Prototype 3",
    },
    {
        "id": "CLM-BAS-F2",
        "variant": "Bass F",
        "root_note": "F2",
        "root_midi": 41,
        "bore_id_in": 0.875,
        "wall_in": 0.3125,
        "body_od_in": 1.500,
        "bell_od_in": 2.900,
        "mouthpiece_socket_id_in": 0.920,
        "sections": "3 body joints + mouthpiece + bell",
        "build_priority": "Stretch prototype",
    },
]


HOLES = [
    {
        "id": "K01",
        "offset": 1,
        "label": "root sharp semitone",
        "control": "normally closed lever",
        "ratio": 0.32,
        "tier": "two-key historical option",
    },
    {
        "id": "H01",
        "offset": 2,
        "label": "scale degree 2",
        "control": "RH little finger",
        "ratio": 0.36,
        "tier": "keyless core",
    },
    {
        "id": "H02",
        "offset": 4,
        "label": "scale degree 3",
        "control": "RH ring finger",
        "ratio": 0.38,
        "tier": "keyless core",
    },
    {
        "id": "H03",
        "offset": 5,
        "label": "scale degree 4",
        "control": "RH middle finger",
        "ratio": 0.34,
        "tier": "keyless core",
    },
    {
        "id": "H04",
        "offset": 7,
        "label": "scale degree 5",
        "control": "RH index finger",
        "ratio": 0.38,
        "tier": "keyless core",
    },
    {
        "id": "H05",
        "offset": 9,
        "label": "scale degree 6",
        "control": "LH ring finger",
        "ratio": 0.40,
        "tier": "keyless core",
    },
    {
        "id": "K02",
        "offset": 10,
        "label": "upper chromatic",
        "control": "normally closed side lever",
        "ratio": 0.30,
        "tier": "two-key historical option",
    },
    {
        "id": "H06",
        "offset": 11,
        "label": "scale degree 7",
        "control": "LH middle finger",
        "ratio": 0.34,
        "tier": "keyless core",
    },
    {
        "id": "H07",
        "offset": 12,
        "label": "octave/root repeat",
        "control": "LH index finger",
        "ratio": 0.32,
        "tier": "keyless core",
    },
]


def ensure_dirs() -> None:
    for name in [
        "cad",
        "cnc",
        "data",
        "drawings",
        "hardware",
        "research",
        "tools",
    ]:
        (ROOT / name).mkdir(exist_ok=True)


def freq_from_midi(midi: float) -> float:
    return 440.0 * (2.0 ** ((midi - 69.0) / 12.0))


def note_name(midi: int) -> str:
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"


def round3(value: float) -> float:
    return round(value + 1e-12, 3)


def variant_model(v: dict[str, object]) -> dict[str, object]:
    midi = int(v["root_midi"])
    bore = float(v["bore_id_in"])
    root_hz = freq_from_midi(midi)
    acoustic_len = SOS_IN_PER_SEC / (4.0 * root_hz)
    bell_end_corr = 0.61 * (bore / 2.0)
    reed_corr = 0.25 * bore
    body_len = acoustic_len - bell_end_corr - reed_corr
    blank_len = body_len + 1.50
    out = dict(v)
    out.update(
        {
            "root_hz": root_hz,
            "acoustic_len_in": acoustic_len,
            "bell_end_corr_in": bell_end_corr,
            "reed_corr_in": reed_corr,
            "body_len_final_in": body_len,
            "blank_len_in": blank_len,
            "turning_blank_in": f"{round3(float(v['body_od_in']) + 0.375)} x {round3(float(v['body_od_in']) + 0.375)} x {round3(blank_len)}",
            "trim_allowance_in": 1.50,
        }
    )
    return out


def hole_schedule() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for variant in [variant_model(v) for v in VARIANTS]:
        body_len = float(variant["body_len_final_in"])
        bore = float(variant["bore_id_in"])
        reed_corr = float(variant["reed_corr_in"])
        for h in HOLES:
            note_midi = int(variant["root_midi"]) + int(h["offset"])
            freq = freq_from_midi(note_midi)
            hole_dia = bore * float(h["ratio"])
            hole_corr = 0.30 * hole_dia
            eff_len = SOS_IN_PER_SEC / (4.0 * freq)
            x_from_reed = eff_len - reed_corr - hole_corr
            x_from_bell = body_len - x_from_reed
            rows.append(
                {
                    "variant_id": variant["id"],
                    "variant": variant["variant"],
                    "root_note": variant["root_note"],
                    "hole_id": h["id"],
                    "label": h["label"],
                    "note": note_name(note_midi),
                    "semitone_offset": h["offset"],
                    "target_freq_hz": round(freq, 2),
                    "hole_dia_in": round3(hole_dia),
                    "hole_dia_mm": round3(hole_dia * 25.4),
                    "x_from_bell_in": round3(x_from_bell),
                    "x_from_reed_seat_in": round3(x_from_reed),
                    "control": h["control"],
                    "tier": h["tier"],
                    "source_model": "stopped cylindrical reed first pass",
                    "build_note": "drill 15-25 percent undersize, then open during tuning",
                }
            )
    return rows


def write_text(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned = dedent(text).strip()
    cleaned = "\n".join(
        line[8:] if line.startswith("        ") else line
        for line in cleaned.splitlines()
    )
    path.write_text(cleaned + "\n", encoding="utf-8")


def write_csv(rel: str, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if not fieldnames:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join(out)


def family_rows() -> list[dict[str, object]]:
    rows = []
    for v in [variant_model(x) for x in VARIANTS]:
        rows.append(
            {
                "instrument_id": v["id"],
                "variant": v["variant"],
                "root_note": v["root_note"],
                "root_midi": v["root_midi"],
                "root_frequency_hz": round(float(v["root_hz"]), 2),
                "bore_id_in": round3(float(v["bore_id_in"])),
                "wall_thickness_in": round3(float(v["wall_in"])),
                "body_od_in": round3(float(v["body_od_in"])),
                "bell_od_in": round3(float(v["bell_od_in"])),
                "acoustic_length_in": round3(float(v["acoustic_len_in"])),
                "body_length_final_in": round3(float(v["body_len_final_in"])),
                "blank_length_in": round3(float(v["blank_len_in"])),
                "turning_blank_in": v["turning_blank_in"],
                "sections": v["sections"],
                "build_priority": v["build_priority"],
                "status": "first-order design; validate after reed and bore prototype",
            }
        )
    return rows


def write_core_csvs() -> None:
    family = family_rows()
    write_csv("family-spec.csv", family)
    schedule = hole_schedule()
    write_csv("data/tone-hole-schedule.csv", schedule)

    bom = [
        {
            "item_no": "1",
            "subsystem": "Body",
            "part_name": "Turned chalumeau body blanks",
            "qty": "4",
            "material_spec": "Cherry or hard maple for first pass; ipe/cocobolo/boxwood for keeper builds",
            "dimensions_spec": "see family-spec.csv blank_length_in and turning_blank_in",
            "make_buy": "make",
            "estimated_cost": "80",
            "drawing_ref": "drawings/chalumeau-family-sheet.svg",
            "notes": "Use lower-cost domestic hardwood for bore and keywork tests before dense/oily woods.",
        },
        {
            "item_no": "2",
            "subsystem": "Bore",
            "part_name": "Long drill and reamer set",
            "qty": "1",
            "material_spec": "Aircraft-length brad point/twist drills plus adjustable/shell reamers",
            "dimensions_spec": "0.500, 0.625, 0.750, 0.875 in bore targets",
            "make_buy": "buy",
            "estimated_cost": "120",
            "drawing_ref": "cnc/cnc-lathe-plan.md",
            "notes": "Exact tooling depends on whether bores are drilled solid or routed as split blanks.",
        },
        {
            "item_no": "3",
            "subsystem": "Mouthpiece",
            "part_name": "Single-reed mouthpieces",
            "qty": "4",
            "material_spec": "Purchased clarinet/sax mouthpiece adapted by size, or shop-made Delrin mouthpiece",
            "dimensions_spec": "socket IDs in family-spec.csv; reed table in design.md",
            "make_buy": "buy first, make later",
            "estimated_cost": "160",
            "drawing_ref": "drawing-brief.md",
            "notes": "Use bought mouthpieces/reeds to isolate body acoustics before making reeds.",
        },
        {
            "item_no": "4",
            "subsystem": "Tone holes",
            "part_name": "Raised tone-hole collars or drilled holes",
            "qty": "36",
            "material_spec": "Integral turned collars for visual style; chamfered holes for first prototype",
            "dimensions_spec": "see data/tone-hole-schedule.csv",
            "make_buy": "make",
            "estimated_cost": "20",
            "drawing_ref": "drawings/chalumeau-soprano-c4-dimensioned.svg",
            "notes": "Collars are visual and ergonomic; pitch comes from hole center, diameter, and chimney.",
        },
        {
            "item_no": "5",
            "subsystem": "Keywork",
            "part_name": "Two-key chalumeau lever set",
            "qty": "4",
            "material_spec": "0.040-0.062 in brass/nickel silver sheet, 1/16 in pivot rod, phosphor bronze spring",
            "dimensions_spec": "K01 and K02 per variant; see hardware/keywork-parts.csv",
            "make_buy": "make",
            "estimated_cost": "60",
            "drawing_ref": "drawings/keywork-lever-detail.svg",
            "notes": "The first soprano can be built keyless, then retrofitted with keys.",
        },
        {
            "item_no": "6",
            "subsystem": "Pads",
            "part_name": "Leather/cork/felt pad stack",
            "qty": "12",
            "material_spec": "Clarinet-style skin pads or cork backed with thin leather",
            "dimensions_spec": "pad OD = tone hole OD + 0.080 to 0.125 in",
            "make_buy": "buy or make",
            "estimated_cost": "35",
            "drawing_ref": "hardware/lever-fabrication-guide.md",
            "notes": "Use leak light or suction test before tuning.",
        },
        {
            "item_no": "7",
            "subsystem": "Finish",
            "part_name": "Oil/shellac finish and bore oil",
            "qty": "1",
            "material_spec": "Dewaxed shellac outside; bore oil compatible with chosen wood",
            "dimensions_spec": "finish schedule in assembly-manual.md",
            "make_buy": "buy",
            "estimated_cost": "30",
            "drawing_ref": "assembly-manual.md",
            "notes": "Avoid thick finish buildup inside tone holes or under pads.",
        },
    ]
    write_csv("bom.csv", bom)

    sourcing = [
        {
            "component": "Domestic hardwood prototype blanks",
            "required_spec": "Straight-grain cherry, hard maple, or walnut; 1.5-2.25 in square; length per family-spec.csv",
            "search_terms": "turning blank cherry hard maple 2x2x18 2x2x30",
            "supplier_candidates": "local hardwood dealer, Bell Forest, Cook Woods, Woodcraft",
            "date_checked": "not live-checked",
            "unit_price": "research before purchase",
            "lead_time": "research before purchase",
            "substitute_rule": "Any stable fine-grained hardwood is acceptable for first acoustic prototypes.",
            "risk_notes": "Soft woods dent around tone holes and key posts; use for process tests only.",
        },
        {
            "component": "Dense keeper-build blanks",
            "required_spec": "Ipe, cocobolo, boxwood, rosewood, grenadilla substitute; dry and crack-free",
            "search_terms": "ipe turning blank cocobolo clarinet blank boxwood woodwind blank",
            "supplier_candidates": "Gilmer Wood, Cook Woods, Bell Forest, specialty woodwind blank suppliers",
            "date_checked": "not live-checked",
            "unit_price": "research before purchase",
            "lead_time": "research before purchase",
            "substitute_rule": "Delrin/acetal is acceptable for dimensional-stability testing.",
            "risk_notes": "Allergenic/oily woods need dust control, wiping before glue, and finish tests.",
        },
        {
            "component": "Single reeds and mouthpieces",
            "required_spec": "Soprano/alto use clarinet-like reeds; tenor/bass may use sax/low clarinet reeds or custom mouthpiece",
            "search_terms": "clarinet mouthpiece blank baroque clarinet reed tenor chalumeau mouthpiece",
            "supplier_candidates": "woodwind suppliers, early-music makers, 3D print/Delrin shop-made option",
            "date_checked": "not live-checked",
            "unit_price": "research before purchase",
            "lead_time": "research before purchase",
            "substitute_rule": "Use commercial reed first to decouple reed-making from bore tuning.",
            "risk_notes": "Reed strength and mouthpiece volume can shift pitch and response significantly.",
        },
        {
            "component": "Brass/nickel-silver key stock",
            "required_spec": "0.040-0.062 in sheet, 1/16 in rod, 0-80 or M1.6 screws, post stock",
            "search_terms": "nickel silver sheet woodwind key rod phosphor bronze spring wire",
            "supplier_candidates": "McMaster-Carr, K&S metals, MusicMedic, instrument repair suppliers",
            "date_checked": "not live-checked",
            "unit_price": "research before purchase",
            "lead_time": "research before purchase",
            "substitute_rule": "Brass is easier to prototype; nickel silver wears better and solders cleanly.",
            "risk_notes": "Tiny screws strip easily; buy extras and make drill guides.",
        },
        {
            "component": "Pads, cork, felt, leather",
            "required_spec": "Clarinet/sax pads or leather-over-cork pads sized to K01/K02 tone holes",
            "search_terms": "clarinet pads sheet cork felt key bumper leather pad cup",
            "supplier_candidates": "MusicMedic, Ferree's Tools, instrument repair suppliers",
            "date_checked": "not live-checked",
            "unit_price": "research before purchase",
            "lead_time": "research before purchase",
            "substitute_rule": "Cork plus thin leather is acceptable for first handmade keys.",
            "risk_notes": "Pad seating matters more than pad material for early prototypes.",
        },
    ]
    write_csv("sourcing.csv", sourcing)

    cut_rows = []
    for row in family:
        cut_rows.append(
            {
                "part_id": f"{row['instrument_id']}-BODY",
                "variant": row["variant"],
                "material": "prototype hardwood",
                "qty": "1",
                "rough_dimensions_in": row["turning_blank_in"],
                "final_dimensions_in": f"OD {row['body_od_in']}; bore {row['bore_id_in']}; body length {row['body_length_final_in']}",
                "operation": "lathe turn, drill/ream bore, drill tone holes, final tune",
                "grain_orientation": "long grain parallel to bore",
                "yield_notes": "leave 1.5 in length allowance and 0.1875 in OD cleanup allowance",
            }
        )
        cut_rows.append(
            {
                "part_id": f"{row['instrument_id']}-BELL",
                "variant": row["variant"],
                "material": "contrasting hardwood or same blank offcut",
                "qty": "1",
                "rough_dimensions_in": f"{round3(float(row['bell_od_in']) + 0.375)} x {round3(float(row['bell_od_in']) + 0.375)} x 3.000",
                "final_dimensions_in": f"bell OD {row['bell_od_in']}; socket fits bore/body OD by CAD",
                "operation": "lathe turn bell flare and socket",
                "grain_orientation": "long grain parallel to bore",
                "yield_notes": "use a separate bell to simplify tuning and repair",
            }
        )
    write_csv("cut-list.csv", cut_rows)

    validation = [
        {
            "test_id": "VAL-001",
            "variant": "all",
            "target": "A4 reference",
            "target_value": "440.00 Hz",
            "measured_value": "",
            "tolerance": "tuner reads 440 within calibration",
            "environment": "record temp F, humidity percent",
            "result": "",
            "action": "Calibrate tuner/mic before instrument data.",
        },
        {
            "test_id": "VAL-010",
            "variant": "Soprano C",
            "target": "all holes closed",
            "target_value": "C4, 261.63 Hz",
            "measured_value": "",
            "tolerance": "+/- 15 cents before final tuning; +/- 8 cents after",
            "environment": "68-72 F preferred",
            "result": "",
            "action": "Trim bell end shorter to sharpen; add temporary tape/extension if sharp.",
        },
        {
            "test_id": "VAL-020",
            "variant": "all",
            "target": "tone-hole sweep",
            "target_value": "each row in data/tone-hole-schedule.csv",
            "measured_value": "",
            "tolerance": "+/- 12 cents after tuning",
            "environment": "same reed, same mouthpiece, same blowing pressure",
            "result": "",
            "action": "Open hole diameter to sharpen; use wax/tape collar to flatten during tests.",
        },
        {
            "test_id": "VAL-030",
            "variant": "keyed builds",
            "target": "pad leak test",
            "target_value": "no visible leak under leak light; suction holds 10 s",
            "measured_value": "",
            "tolerance": "zero audible hiss at normal blowing pressure",
            "environment": "before final tone-hole tuning",
            "result": "",
            "action": "Reseat pad, regulate cork, or lap tone-hole rim.",
        },
        {
            "test_id": "VAL-040",
            "variant": "experimental register key",
            "target": "overblown twelfth check",
            "target_value": "note + 19 semitones if vent is clarinet-like",
            "measured_value": "",
            "tolerance": "document response only; not a first-build pass/fail",
            "environment": "same reed and embouchure as low-register test",
            "result": "",
            "action": "Move/resize vent only after the core chalumeau speaks well.",
        },
    ]
    write_csv("validation.csv", validation)

    measurements = [
        {
            "build_id": "CLM-SOP-C4-P1",
            "date": "",
            "variant": "Soprano C",
            "reed": "",
            "mouthpiece": "",
            "temperature_f": "",
            "humidity_pct": "",
            "hole_state": "all closed",
            "target_note": "C4",
            "target_hz": "261.63",
            "measured_hz": "",
            "cents_error": "",
            "action_taken": "",
            "notes": "",
        }
    ]
    for row in hole_schedule():
        if row["variant_id"] == "CLM-SOP-C4":
            measurements.append(
                {
                    "build_id": "CLM-SOP-C4-P1",
                    "date": "",
                    "variant": row["variant"],
                    "reed": "",
                    "mouthpiece": "",
                    "temperature_f": "",
                    "humidity_pct": "",
                    "hole_state": row["hole_id"],
                    "target_note": row["note"],
                    "target_hz": row["target_freq_hz"],
                    "measured_hz": "",
                    "cents_error": "",
                    "action_taken": "",
                    "notes": "",
                }
            )
    write_csv("data/prototype-measurement-template.csv", measurements)

    key_rows = []
    for v in family:
        keyed = [r for r in schedule if r["variant_id"] == v["instrument_id"] and r["hole_id"].startswith("K")]
        for item in keyed:
            pad_od = round3(float(item["hole_dia_in"]) + 0.110)
            lever_len = round3(max(1.75, min(4.50, float(item["x_from_bell_in"]) + 0.75)))
            key_rows.append(
                {
                    "part_id": f"{v['instrument_id']}-{item['hole_id']}",
                    "variant": v["variant"],
                    "key_function": item["label"],
                    "tone_hole_note": item["note"],
                    "tone_hole_dia_in": item["hole_dia_in"],
                    "pad_od_in": pad_od,
                    "lever_length_in": lever_len,
                    "pivot_rod_in": "0.0625",
                    "sheet_thickness_in": "0.050",
                    "spring": "0.012-0.018 in phosphor bronze needle or flat spring",
                    "default_state": "closed pad; press lever to open",
                    "drawing_ref": "drawings/keywork-lever-detail.svg",
                }
            )
    write_csv("hardware/keywork-parts.csv", key_rows)

    sw_rows = []
    for row in family:
        sw = {
            "$CONFIGURATION": row["instrument_id"],
            "$DESCRIPTION": row["variant"],
            "CLM_Root_MIDI": row["root_midi"],
            "CLM_Root_Hz": row["root_frequency_hz"],
            "CLM_SOS_in_per_s": SOS_IN_PER_SEC,
            "CLM_Bore_ID_in": row["bore_id_in"],
            "CLM_Wall_T_in": row["wall_thickness_in"],
            "CLM_Body_OD_in": row["body_od_in"],
            "CLM_Bell_OD_in": row["bell_od_in"],
            "CLM_Body_L_Final_in": row["body_length_final_in"],
            "CLM_Blank_L_in": row["blank_length_in"],
        }
        for r in schedule:
            if r["variant_id"] == row["instrument_id"]:
                sw[f"CLM_{r['hole_id']}_X_Bell_in"] = r["x_from_bell_in"]
                sw[f"CLM_{r['hole_id']}_Dia_in"] = r["hole_dia_in"]
        sw_rows.append(sw)
    sw_fields = list(sw_rows[0].keys())
    write_csv("cad/solidworks-design-table.csv", sw_rows, sw_fields)


def write_markdown_docs() -> None:
    family = family_rows()
    family_table = md_table(
        [
            "ID",
            "Variant",
            "Root",
            "Bore ID",
            "Final body L",
            "Blank L",
            "Sections",
        ],
        [
            [
                r["instrument_id"],
                r["variant"],
                r["root_note"],
                r["bore_id_in"],
                r["body_length_final_in"],
                r["blank_length_in"],
                r["sections"],
            ]
            for r in family
        ],
    )

    write_text(
        "README.md",
        f"""
        # Chalumeau Family

        > A prototype validation packet for a family of single-reed chalumeaux:
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

        This repository now contains a first-pass engineering packet for
        designing and prototyping a family of chalumeaux in soprano C, alto G,
        tenor C, and bass F. The design is parametric: body length, bore,
        tone-hole positions, and optional levers are driven from formulas rather
        than hidden one-off dimensions. It is not yet a build-ready or
        empirically validated packet; the first soprano prototype still needs
        measured reed, mouthpiece, bore, tuning, and response data.

        The packet starts from attributed Dudy.eu chalumeau reference photos in
        `images/`, Tony's `Musical Instruments.xlsx` workbook, and especially
        the reed/bore lessons in the `Great Highland Bagpipe` sheet. The
        acoustic model is not copied from Native American style flute K2
        corrections. A chalumeau is a cylindrical, single-reed, effectively
        stopped pipe, so it gets its own validation loop.

        ## Family plan

        {family_table}

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
        | Reed/tuning validation | capture templates and validation loop ready; needs measured prototype data |
        | SolidWorks | variable conventions and design table ready |

        ## License

        Released under [CC-BY 4.0](LICENSE) for original written/design content
        in this repository. The Dudy.eu reference photos are attributed source
        images, not Tony-owned build photos; replace them with shop photos as
        prototypes are built.
        """,
    )

    write_text(
        "design.md",
        f"""
        # CLM-001 - Chalumeau Family

        Generated: {TODAY}

        ## Intent

        Design a family of chalumeaux that can be built in Tony's shop using
        lathe/CNC workflows, commercial reeds for early isolation tests, and
        optional handmade metal keywork. The family should cover a useful range
        without pretending the first-pass physics is final: all tone-hole
        coordinates are starting points that must be validated with a real reed,
        mouthpiece, bore, and player pressure.

        ## Source Artifacts

        - Repo: `https://github.com/tonykoop/chalumeau`
        - Attributed inspiration/reference photos: `images/chalumeau1.jpg` and
          `images/chalumeau5.jpg`, from Petr Skalicky / Dudy.eu:
          `https://www.dudy.eu/chalumeau.php`
        - Additional local inspiration image: `images/7173-372-1_1920x1080.avif`
        - Workbook inspected: `C:/Users/Tony/Documents/Claude/Projects/Career/flutes-staging/Musical Instruments.xlsx`
        - Relevant workbook source sheet: `Great Highland Bagpipe`, especially the
          contrast between conical double-reed chanter rows and cylindrical
          single-reed drone rows.
        - Done-bar reference style: `tongue-drum` repo packet and skill v3
          packet requirements.

        ## Governing Model

        The chalumeau is modeled as a cylindrical single-reed pipe that behaves
        like a stopped pipe in its low register.

        ```text
        f = c / (4 * L_eff)
        L_eff = c / (4 * f)
        c = 13552 in/s at about 68 F
        body_length = L_eff - bell_end_correction - reed_end_correction
        bell_end_correction = 0.61 * bore_radius
        reed_end_correction = 0.25 * bore_id   # first-pass assumption
        tone_hole_x_from_bell = body_length - (c/(4*f_note) - reed_corr - 0.30*hole_dia)
        cents_error = 1200 * log2(measured_hz / target_hz)
        ```

        The model deliberately does not use Tony's NAF K2 corrections. Those
        corrections are for open-open Native American style flutes in a specific
        bore range. The chalumeau reed, stopped-pipe boundary condition,
        mouthpiece volume, bore diameter, and tone-hole chimneys need their own
        empirical correction after prototype measurement.

        ## Family Spec

        {family_table}

        ## Tone-Hole Strategy

        - The keyless core uses seven front holes for a diatonic octave:
          offsets +2, +4, +5, +7, +9, +11, +12 semitones from the all-closed
          root.
        - `K01` is an optional normally closed semitone key near the bell. It
          gives the first chromatic note above the root without forcing an
          awkward low finger stretch.
        - `K02` is an optional upper chromatic side key. It gives a practical
          chromatic note between scale degrees 6 and 7 and doubles as a keywork
          fabrication exercise.
        - A clarinet-style register vent is listed only as an experimental
          future feature. The first chalumeau should be judged by the low
          register before chasing overblown twelfths.

        ## Hardware Alignment

        The hardware is intentionally small-shop manufacturable:

        | Hardware | Role | First-build method | Upgrade path |
        | --- | --- | --- | --- |
        | K01 lever | opens low semitone tone hole | brass strip lever, pivot post pair, leather/cork pad | nickel-silver lever with soldered pad cup |
        | K02 lever | opens upper chromatic tone hole | side lever with flat spring return | clarinet-style post/rod key with regulation cork |
        | Optional register vent | tests clarinet evolution | leave undrilled until the body speaks well | small lined vent tube near mouthpiece |
        | Raised tone-hole collars | ergonomic/aesthetic reference to photos | turn integral collars or add rings | separate stabilized-wood collars |

        ## SolidWorks Parameter Convention

        Use `CLM_` as the project prefix, keep units in the variable name, and
        use stable hole IDs that match the CSV and drawings:

        - `CLM_Bore_ID_in`, `CLM_Body_L_Final_in`, `CLM_Bell_OD_in`
        - `CLM_H01_X_Bell_in`, `CLM_H01_Dia_in`
        - `CLM_K01_X_Bell_in`, `CLM_K01_Dia_in`
        - `CLM_Key_Pivot_Rod_Dia_in`, `CLM_Pad_Overhang_in`

        The SolidWorks design table is `cad/solidworks-design-table.csv`. The
        equation snippets are in `cad/solidworks-equations.txt`.

        ## Assumptions And Risks

        | Risk | Why it matters | Mitigation |
        | --- | --- | --- |
        | Reed/mouthpiece compliance shifts pitch | the reed is not a hard closed end | test with one commercial reed/mouthpiece before final hole tuning |
        | Tone holes are first-pass estimates | small holes do not act as perfect open ends | drill undersized, tune larger, log every change |
        | Bass holes exceed finger comfort | low instruments become large quickly | use key pads for lower/bigger holes |
        | Handmade key pads leak | leaks ruin tuning and response | leak-light/suction test before pitch tuning |
        | Dense oily woods complicate machining | cocobolo/ipe dust and finish issues | prototype in cherry/maple first |

        ## Validation Plan

        1. Calibrate tuner/microphone at A4 = 440 Hz.
        2. Build `CLM-SOP-C4` with no levers and a commercial reed/mouthpiece.
        3. Tune the all-closed root by trimming the bell/foot only after reed
           response is stable.
        4. Open holes from the bell upward, enlarging in small increments and
           logging measured frequency and cents error.
        5. Add K01/K02 to either the same body or a second soprano body. Validate
           sealing before measuring pitch.
        6. Update the empirical correction column in the design workbook before
           scaling to alto, tenor, or bass.

        ## Next Actions

        - Confirm the actual reed and mouthpiece family for the soprano prototype.
        - Decide whether the first body gets raised collars like the inspiration
          image or plain chamfered holes for faster tuning.
        - Model `CLM-SOP-C4` in SolidWorks using the provided global variables.
        - After first measurements, add a `prototype_correction_pct` column to
          `data/tone-hole-schedule.csv`.
        """,
    )

    write_text(
        "research/chalumeau-keywork-history.md",
        """
        # Chalumeau Keywork: Why Some Have Levers And Some Do Not

        ## Short Answer

        Keyless chalumeaux are the simple form: a cylindrical single-reed pipe
        with finger holes placed where human fingers can reach them. Levers or
        keys appear when the maker wants a hole that is too far away, too large,
        too awkward to seal, or useful for a chromatic note. The clarinet
        evolved from this same family by making one of those keys work as a
        real register/speaker vent and then adding more keys for chromatic
        notes, low extensions, trills, and improved intonation.

        ## Historical Logic

        Britannica describes the chalumeau as a cylindrical single-reed stopped
        pipe and says Johann Christoph Denner added an extra finger hole and two
        keys around 1700, with later experimentation leading to the clarinet.
        It also notes that the chalumeau did not overblow into a register above
        the fundamental the way the clarinet does.

        Gregory Barrett's NIU clarinet history gives the design distinction in
        practical terms: the chalumeau was optimized for the low chalumeau
        register, while the early clarinet moved the back key higher and made it
        smaller so it functioned as a register/speaker key. On a cylindrical
        closed-pipe instrument, that register key produces notes a twelfth above
        the low-register fingering, not an octave above.

        The Baltimore Recorders chalumeau note makes the same point from the
        instrument-layout side: the chalumeau's two uppermost keys are placed
        differently from the clarinet's register key, which is why a chalumeau
        remains mostly a low-register instrument.

        ## What The Levers Do

        - Open a tone hole that is outside direct finger reach.
        - Close or open a hole that is too large for a fingertip to seal.
        - Add chromatic notes without awkward cross-fingering.
        - Improve tuning by putting the acoustically correct hole where the
          hand cannot comfortably go.
        - On clarinets, act as a register/speaker vent so the cylindrical bore
          overblows by a twelfth.
        - On later clarinets, link multiple holes so one finger can operate a
          pad somewhere else on the body.

        ## Design Choice For This Project

        Build the first soprano C chalumeau keyless so the bore, reed, and
        seven-hole scale can be debugged cleanly. Then add two handmade
        normally closed keys:

        - `K01`: a low semitone key near the bell.
        - `K02`: an upper chromatic side key.

        Treat the clarinet-style register vent as a later experiment, because a
        vent hole drilled too early can compromise the low-register chalumeau.

        ## Sources

        - Britannica, "chalumeau": https://www.britannica.com/art/chalumeau
        - Britannica, "clarinet": https://www.britannica.com/art/clarinet
        - Gregory Barrett, Northern Illinois University, "Development of the Clarinet": https://www.niu.edu/gbarrett/resources/development.shtml
        - Baltimore Recorders, "about the Chalumeau": https://www.baltimorerecorders.org/html/instruments/chalumeau.html
        """,
    )

    write_text(
        "hardware/lever-fabrication-guide.md",
        """
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
        """,
    )

    write_text(
        "cad/solidworks-global-variables.md",
        """
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
        """,
    )

    write_text(
        "cad/solidworks-equations.txt",
        f"""
        "CLM_SOS_in_per_s" = {SOS_IN_PER_SEC}
        "CLM_Root_Hz" = 440 * 2 ^ (("CLM_Root_MIDI" - 69) / 12)
        "CLM_Bell_End_Corr_in" = 0.61 * ("CLM_Bore_ID_in" / 2)
        "CLM_Reed_Corr_in" = 0.25 * "CLM_Bore_ID_in"
        "CLM_Acoustic_L_in" = "CLM_SOS_in_per_s" / (4 * "CLM_Root_Hz")
        "CLM_Body_L_Final_in" = "CLM_Acoustic_L_in" - "CLM_Bell_End_Corr_in" - "CLM_Reed_Corr_in"
        "CLM_Blank_L_in" = "CLM_Body_L_Final_in" + 1.5
        "CLM_Body_OD_in" = "CLM_Bore_ID_in" + 2 * "CLM_Wall_T_in"
        "CLM_Pad_Overhang_in" = 0.055
        "CLM_Key_Pivot_Rod_Dia_in" = 0.0625

        # Pattern for each hole H01-H07/K01-K02:
        # "CLM_H01_Hz" = 440 * 2 ^ (("CLM_Root_MIDI" + 2 - 69) / 12)
        # "CLM_H01_Eff_L_in" = "CLM_SOS_in_per_s" / (4 * "CLM_H01_Hz")
        # "CLM_H01_X_Bell_in" = "CLM_Body_L_Final_in" - ("CLM_H01_Eff_L_in" - "CLM_Reed_Corr_in" - 0.30 * "CLM_H01_Dia_in")
        """,
    )

    write_text(
        "assembly-manual.md",
        """
        # Chalumeau Assembly Manual

        ## Build Order

        Build the soprano C keyless version first. Do not add keywork until the
        bore, reed, and seven front holes speak reliably.

        ## Phase 0 - Design Freeze

        1. Pick the exact reed and mouthpiece.
        2. Print `data/tone-hole-schedule.csv` and mark which holes will be
           drilled in the first pass.
        3. Decide whether the prototype uses raised collars or plain chamfered
           holes. Plain holes tune faster; collars match the inspiration photo.
        4. Confirm the blank dimensions from `cut-list.csv`.

        ## Phase 1 - Body Blank And Bore

        1. Mill/turn the blank oversize and mark the bore centerline.
        2. Drill the bore from the reed-seat end with the longest stable drill
           setup available.
        3. Ream or lap to final bore diameter. Measure at both ends.
        4. Turn the exterior body profile, leaving extra length at the bell end.
        5. Cut the mouthpiece socket/tenon but keep the reed setup removable.

        ## Phase 2 - Root Tuning

        1. Assemble reed, mouthpiece, and body with all holes undrilled.
        2. Measure the all-closed pitch.
        3. Trim the bell/foot in small steps only after the reed is stable.
        4. Record every trim amount in `validation.csv`.

        ## Phase 3 - Tone Holes

        1. Lay out hole centers from `data/tone-hole-schedule.csv`, measuring
           from `DATUM_BELL_FACE`.
        2. Center punch lightly. A wandering bit will change tuning.
        3. Drill each hole 15-25 percent undersize.
        4. Open holes from low to high. After each enlargement, play the target
           note and log measured frequency.
        5. Chamfer only after pitch is close; chamfering can sharpen the note.

        ## Phase 4 - Optional K01/K02 Keywork

        1. Drill keyed tone holes undersize.
        2. Fabricate levers using `hardware/lever-fabrication-guide.md`.
        3. Install posts and pivot rods.
        4. Seat pads and leak-test before tuning.
        5. Tune keyed notes after the pad seal is stable.

        ## Phase 5 - Finish

        1. Sand exterior through 320 or finer.
        2. Seal the bore lightly; avoid thick buildup.
        3. Apply shellac/oil finish outside.
        4. Keep finish out of tone holes and under pads.
        5. Re-test all notes after finish cures.

        ## Maintenance Notes

        - Swab the bore after playing.
        - Check pad seating after humidity swings.
        - Keep a build log for each reed/mouthpiece combination; reed strength
          can make the same body read sharp or flat.
        """,
    )

    write_text(
        "drawing-brief.md",
        """
        # Chalumeau Drawing Brief

        Instrument: Chalumeau family
        Revision/date: REV-A
        Units: inches unless noted
        Source workbook/CAD/catalog ID: CLM-001 / SolidWorks design table

        ## Required Views

        - Family comparison side view with bore axis and body lengths.
        - Soprano C dimensioned side view with all H/K hole coordinates.
        - Cross-section through bore, tone-hole chimney, and raised collar.
        - Keywork detail for K01/K02: closed/open positions, pad, cup, pivot,
          posts, spring, touchpiece.
        - Exploded view: mouthpiece/reed, body, bell, K01, K02, pads, posts.
        - Ergonomic view: hand reach for keyless soprano and keyed bass notes.

        ## Critical Dimensions

        | Feature | Dimension source | Tolerance |
        | --- | --- | --- |
        | Bore ID | `family-spec.csv` | +/- 0.003 in after ream/lap |
        | Body length | `family-spec.csv` | leave trim allowance; final by tuning |
        | Hole X from bell | `data/tone-hole-schedule.csv` | +/- 0.020 in first prototype |
        | Hole diameter | `data/tone-hole-schedule.csv` | start undersize; final by tuning |
        | Pad seat flatness | `hardware/keywork-parts.csv` | no visible leak |
        | Pivot alignment | keywork drawing | lever moves freely without side shake |

        ## Drawing Outputs In This Packet

        - `drawings/chalumeau-family-sheet.svg`
        - `drawings/chalumeau-soprano-c4-dimensioned.svg`
        - `drawings/keywork-lever-detail.svg`

        ## Notes For SolidWorks

        Drive dimensions from global variables. Do not dimension hole centers
        manually in separate sketches unless the dimension names match the CSV.
        """,
    )

    write_text(
        "visual-bom-brief.md",
        """
        # Visual BOM Brief

        ## Layout

        Use the Ashiko visual BOM pattern: hero image at the top, spreadsheet
        rows below, and one part image/render per row. Use the actual local
        chalumeau photos for the hero/inspiration image until Tony has shop
        photos of the prototypes.

        ## Real Images Available

        - `images/chalumeau1.jpg`: full instrument inspiration, attributed to
          Petr Skalicky / Dudy.eu, `https://www.dudy.eu/chalumeau.php`.
        - `images/chalumeau5.jpg`: close-up of raised collars and wood finish,
          attributed to Petr Skalicky / Dudy.eu, `https://www.dudy.eu/chalumeau.php`.
        - `images/7173-372-1_1920x1080.avif`: additional inspiration image,
          not universally supported by all renderers.

        ## Part Rows To Show

        1. Turned body blank.
        2. Mouthpiece/reed assembly.
        3. Bell.
        4. H01-H07 tone-hole row with raised collars.
        5. K01 low semitone lever.
        6. K02 side chromatic lever.
        7. Pad/cork/felt stack.
        8. Pivot posts, rods, springs, screws.
        9. Finish and bore oil.

        ## Placeholder Policy

        Generated or schematic part images are acceptable for planning, but mark
        them as placeholders until replaced with supplier images or shop photos.
        Build-critical dimensions must come from the CSV/workbook/SolidWorks,
        not from pixels in the visual BOM.
        """,
    )

    write_text(
        "supplier-rfq.md",
        """
        # Supplier RFQ - Chalumeau Materials And Keywork

        Hello,

        I am sourcing materials for a small family of handmade single-reed
        chalumeaux. Please quote the items below, including unit price, volume
        price if applicable, lead time, shipping estimate, and any recommended
        substitutes.

        ## Wood Or Plastic Blanks

        - Straight-grain turning blanks suitable for woodwind bodies.
        - Prototype species: cherry, hard maple, walnut, or Delrin/acetal.
        - Keeper species: ipe, boxwood, cocobolo, rosewood, or grenadilla
          substitute.
        - Sizes range from about 1.25 x 1.25 x 15 in to 2.25 x 2.25 x 41 in.
          Exact dimensions are in `cut-list.csv`.

        ## Keywork Materials

        - Brass or nickel-silver sheet, 0.040-0.062 in thick.
        - 1/16 in rod or equivalent pivot stock.
        - Small screws, post stock, and phosphor bronze spring wire.
        - Clarinet/sax pads or pad leather/cork materials.

        ## Requirements

        - Material must be stable, dry, and suitable for fine drilling/turning.
        - Please identify any allergy/dust or finish compatibility concerns.
        - Substitutions are acceptable if dimensional stability and machinability
          are comparable.

        Thank you.
        """,
    )

    write_text(
        "cnc/cnc-lathe-plan.md",
        """
        # CNC And Lathe Plan

        ## Preferred First Prototype Method

        Use the lathe/drill-ream workflow for the soprano C prototype. The bore
        is short enough that a solid blank is practical and easier to validate
        than a split-blank glue-up.

        ## Operations

        1. Square and center the blank.
        2. Drill pilot bore from reed-seat end.
        3. Step drill/ream to target bore ID.
        4. Turn exterior cylinder and ornamental beads/collars.
        5. Cut mouthpiece socket and bell tenon/socket.
        6. Mark hole centers from bell datum using a V-block or rotary index.
        7. Drill holes undersize on drill press or CNC with a cradle fixture.
        8. Tune holes by hand reaming.
        9. Add keywork post holes only after key lever geometry is confirmed.

        ## CNC Fixture Concept

        - V-block cradle with two dowel pin datums.
        - Bore axis parallel to X.
        - Bell face against a fixed stop for `DATUM_BELL_FACE`.
        - Rotary/indexing marks for front-hole plane and side-key plane.
        - Use a peck cycle for clean hole walls; back up the bore with a
          removable mandrel if tearout appears.

        ## Tooling Notes

        - Long drill bits must be checked for runout.
        - Ream/lap the bore after drilling; do not rely on twist drill diameter.
        - Keep tone-hole drills small for first pass and open by hand.
        - For bass, consider split-blank routing if long drilling wanders.
        """,
    )

    write_text(
        "SKILLS.md",
        """
        # Skills Demonstrated

        ## stopped-cylindrical-reed-bore

        Models a single-reed cylindrical bore as a stopped pipe in the low
        register, with explicit reed and bell end-correction assumptions.

        ## handmade-woodwind-keywork

        Designs and fabricates simple early-woodwind levers using brass or
        nickel silver, pivot rods, pads, posts, and springs.

        ## solidworks-parametric-family-table

        Uses one design table to drive multiple instrument-family
        configurations, with stable named dimensions that match CSV, drawings,
        and validation logs.

        ## empirical-tone-hole-validation

        Starts with physics-derived hole positions, then tunes the real
        prototype by measured frequency and cents error rather than trusting the
        first-pass model blindly.
        """,
    )

    write_text(
        "data/workbook-inspection-summary.md",
        """
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
        """,
    )


def write_wolfram() -> None:
    write_text(
        "wolfram-starter.wl",
        """
        (* Chalumeau family acoustic starter - generated __TODAY__ *)

        ClearAll["Global`*"];

        speedOfSoundInPerSec = __SOS_IN_PER_SEC__;
        midiFrequency[m_] := 440*2^((m - 69)/12);
        centsError[measured_, target_] := 1200*Log2[measured/target];

        bodyLength[rootMidi_, boreID_] := Module[
          {f = midiFrequency[rootMidi], acoustic, bellCorr, reedCorr},
          acoustic = speedOfSoundInPerSec/(4*f);
          bellCorr = 0.61*(boreID/2);
          reedCorr = 0.25*boreID;
          acoustic - bellCorr - reedCorr
        ];

        holeXFromBell[rootMidi_, offset_, boreID_, holeRatio_] := Module[
          {f = midiFrequency[rootMidi + offset], holeDia, holeCorr, reedCorr, eff, body},
          holeDia = boreID*holeRatio;
          holeCorr = 0.30*holeDia;
          reedCorr = 0.25*boreID;
          eff = speedOfSoundInPerSec/(4*f);
          body = bodyLength[rootMidi, boreID];
          body - (eff - reedCorr - holeCorr)
        ];

        variants = {
          <|"ID" -> "CLM-SOP-C4", "RootMIDI" -> 60, "BoreID" -> 0.500|>,
          <|"ID" -> "CLM-ALT-G3", "RootMIDI" -> 55, "BoreID" -> 0.625|>,
          <|"ID" -> "CLM-TEN-C3", "RootMIDI" -> 48, "BoreID" -> 0.750|>,
          <|"ID" -> "CLM-BAS-F2", "RootMIDI" -> 41, "BoreID" -> 0.875|>
        };

        holeOffsets = {1, 2, 4, 5, 7, 9, 10, 11, 12};
        holeRatios = {0.32, 0.36, 0.38, 0.34, 0.38, 0.40, 0.30, 0.34, 0.32};

        familyTable = Table[
          With[{v = variants[[i]]},
            <|
              "ID" -> v["ID"],
              "RootHz" -> midiFrequency[v["RootMIDI"]],
              "BodyLengthIn" -> bodyLength[v["RootMIDI"], v["BoreID"]],
              "HolePositionsFromBellIn" -> MapThread[
                holeXFromBell[v["RootMIDI"], #1, v["BoreID"], #2]&,
                {holeOffsets, holeRatios}
              ]
            |>
          ],
          {i, Length[variants]}
        ];

        Dataset[familyTable]

        Manipulate[
          Plot[
            speedOfSoundInPerSec/(4*(x + 0.61*(bore/2) + 0.25*bore)),
            {x, 4, 42},
            PlotRange -> {80, 700},
            AxesLabel -> {"Body length (in)", "Frequency (Hz)"},
            PlotLabel -> "Stopped cylindrical reed bore first-pass model"
          ],
          {{bore, 0.5, "Bore ID (in)"}, 0.35, 1.0}
        ]
        """.replace("__TODAY__", TODAY).replace("__SOS_IN_PER_SEC__", str(SOS_IN_PER_SEC)),
    )


def write_openscad() -> None:
    write_text(
        "cad/chalumeau_family_master.scad",
        """
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
        """,
    )


def svg_header(width: int, height: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'


def write_drawings() -> None:
    family = family_rows()
    schedule = hole_schedule()

    lines = [
        svg_header(1600, 1000),
        '<rect width="1600" height="1000" fill="#f8fafc"/>',
        '<text x="60" y="70" font-family="Arial" font-size="34" font-weight="700">Chalumeau Family - First-Pass Stopped-Reed Design</text>',
        '<text x="60" y="105" font-family="Arial" font-size="16">Units: inches. Hole centers measured from bell datum. Validate by prototype tuning before final machining.</text>',
    ]
    max_len = max(float(r["body_length_final_in"]) for r in family)
    y = 180
    for row in family:
        body_len = float(row["body_length_final_in"])
        scale = 1200 / max_len
        x0 = 220
        x1 = x0 + body_len * scale
        od = 22 + float(row["bore_id_in"]) * 18
        lines += [
            f'<text x="60" y="{y+8}" font-family="Arial" font-size="20" font-weight="700">{row["instrument_id"]}</text>',
            f'<text x="60" y="{y+34}" font-family="Arial" font-size="14">{row["variant"]}, root {row["root_note"]}, bore {row["bore_id_in"]} in</text>',
            f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#334155" stroke-width="{od}" stroke-linecap="round"/>',
            f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#0f172a" stroke-width="2" stroke-dasharray="8 6"/>',
            f'<circle cx="{x0-36}" cy="{y}" r="{float(row["bell_od_in"])*scale*0.18}" fill="none" stroke="#92400e" stroke-width="6"/>',
            f'<text x="{x1+20}" y="{y+6}" font-family="Arial" font-size="14">L={row["body_length_final_in"]} in</text>',
        ]
        for h in [r for r in schedule if r["variant_id"] == row["instrument_id"]]:
            hx = x0 + float(h["x_from_bell_in"]) * scale
            color = "#dc2626" if str(h["hole_id"]).startswith("K") else "#111827"
            lines.append(f'<circle cx="{hx}" cy="{y}" r="{max(4, float(h["hole_dia_in"])*scale*0.25)}" fill="{color}" stroke="white" stroke-width="2"/>')
        y += 170
    lines += [
        '<rect x="60" y="870" width="1480" height="70" fill="none" stroke="#334155" stroke-width="2"/>',
        '<text x="80" y="902" font-family="Arial" font-size="16">REV-A. Generated from family-spec.csv and data/tone-hole-schedule.csv. Red holes are optional keyed K01/K02.</text>',
        '<text x="80" y="928" font-family="Arial" font-size="16">Primary datums: DATUM_BELL_FACE, DATUM_REED_SEAT, DATUM_BORE_AXIS.</text>',
        "</svg>",
    ]
    write_text("drawings/chalumeau-family-sheet.svg", "\n".join(lines))

    sop = next(r for r in family if r["instrument_id"] == "CLM-SOP-C4")
    sop_holes = [r for r in schedule if r["variant_id"] == "CLM-SOP-C4"]
    scale = 90
    x0 = 160
    y0 = 270
    body_len = float(sop["body_length_final_in"])
    x1 = x0 + body_len * scale
    lines = [
        svg_header(1600, 900),
        '<rect width="1600" height="900" fill="#ffffff"/>',
        '<text x="60" y="70" font-family="Arial" font-size="32" font-weight="700">CLM-SOP-C4 Soprano C Chalumeau - Dimensioned Prototype Sheet</text>',
        '<text x="60" y="105" font-family="Arial" font-size="16">First-pass dimensions. Drill undersize and tune. Do not treat hole diameters as final until measured.</text>',
        f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#8b5a2b" stroke-width="78" stroke-linecap="round"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#111827" stroke-width="2" stroke-dasharray="10 8"/>',
        f'<text x="{x0}" y="{y0-70}" font-family="Arial" font-size="14">DATUM_BELL_FACE</text>',
        f'<text x="{x1-80}" y="{y0-70}" font-family="Arial" font-size="14">DATUM_REED_SEAT</text>',
        f'<line x1="{x0}" y1="{y0-55}" x2="{x0}" y2="{y0+90}" stroke="#0f172a" stroke-width="2"/>',
        f'<line x1="{x1}" y1="{y0-55}" x2="{x1}" y2="{y0+90}" stroke="#0f172a" stroke-width="2"/>',
        f'<line x1="{x0}" y1="{y0+80}" x2="{x1}" y2="{y0+80}" stroke="#0f172a" stroke-width="1"/>',
        f'<text x="{(x0+x1)/2-60}" y="{y0+115}" font-family="Arial" font-size="16">Final body length {sop["body_length_final_in"]} in</text>',
    ]
    for idx, h in enumerate(sop_holes):
        hx = x0 + float(h["x_from_bell_in"]) * scale
        top = 160 - (idx % 2) * 38
        color = "#dc2626" if str(h["hole_id"]).startswith("K") else "#111827"
        lines += [
            f'<circle cx="{hx}" cy="{y0}" r="{max(7, float(h["hole_dia_in"])*scale*0.35)}" fill="{color}" stroke="#fff" stroke-width="2"/>',
            f'<line x1="{hx}" y1="{y0-42}" x2="{hx}" y2="{top+24}" stroke="#64748b" stroke-width="1"/>',
            f'<text x="{hx-28}" y="{top}" font-family="Arial" font-size="13" font-weight="700">{h["hole_id"]}</text>',
            f'<text x="{hx-38}" y="{top+17}" font-family="Arial" font-size="12">{h["note"]}</text>',
            f'<text x="{hx-42}" y="{top+34}" font-family="Arial" font-size="12">X {h["x_from_bell_in"]}</text>',
            f'<text x="{hx-42}" y="{top+51}" font-family="Arial" font-size="12">D {h["hole_dia_in"]}</text>',
        ]
    lines += [
        '<text x="60" y="610" font-family="Arial" font-size="20" font-weight="700">Manufacturing Notes</text>',
        '<text x="60" y="645" font-family="Arial" font-size="15">1. Bore ID 0.500 in, body OD 0.875 in, wall 0.1875 in. Use commercial reed/mouthpiece for first test.</text>',
        '<text x="60" y="672" font-family="Arial" font-size="15">2. H holes are finger holes. K holes are optional normally closed lever keys.</text>',
        '<text x="60" y="699" font-family="Arial" font-size="15">3. Coordinates are from bell datum. Re-check after final root trim.</text>',
        '<rect x="60" y="760" width="1480" height="78" fill="none" stroke="#0f172a" stroke-width="2"/>',
        '<text x="80" y="792" font-family="Arial" font-size="15">Title block: Chalumeau Soprano C, REV-A, units inch, source CLM-001 design table.</text>',
        '<text x="80" y="818" font-family="Arial" font-size="15">Tuning-critical features: bore ID, body length, hole center X, hole diameter, pad seal for K01/K02.</text>',
        "</svg>",
    ]
    write_text("drawings/chalumeau-soprano-c4-dimensioned.svg", "\n".join(lines))

    lines = [
        svg_header(1600, 900),
        '<rect width="1600" height="900" fill="#ffffff"/>',
        '<text x="60" y="70" font-family="Arial" font-size="32" font-weight="700">Chalumeau K01/K02 Lever Detail</text>',
        '<text x="60" y="105" font-family="Arial" font-size="16">Simple normally closed pad key. Press touchpiece to open tone hole.</text>',
        '<rect x="160" y="390" width="950" height="95" rx="40" fill="#8b5a2b" stroke="#4b2e12" stroke-width="4"/>',
        '<line x1="190" y1="438" x2="1080" y2="438" stroke="#111827" stroke-width="3" stroke-dasharray="12 8"/>',
        '<circle cx="620" cy="392" r="38" fill="#111827"/>',
        '<circle cx="620" cy="392" r="52" fill="none" stroke="#78350f" stroke-width="10"/>',
        '<rect x="548" y="285" width="410" height="28" rx="12" fill="#c9a227" stroke="#7c5b00" stroke-width="3"/>',
        '<circle cx="620" cy="299" r="54" fill="none" stroke="#c9a227" stroke-width="18"/>',
        '<circle cx="880" cy="299" r="18" fill="#64748b" stroke="#1f2937" stroke-width="3"/>',
        '<line x1="880" y1="250" x2="880" y2="348" stroke="#1f2937" stroke-width="8"/>',
        '<rect x="960" y="250" width="130" height="46" rx="18" fill="#c9a227" stroke="#7c5b00" stroke-width="3"/>',
        '<path d="M735 315 C760 365, 800 365, 830 315" fill="none" stroke="#334155" stroke-width="5"/>',
        '<text x="545" y="225" font-family="Arial" font-size="15">pad cup + leather/cork pad</text>',
        '<line x1="620" y1="240" x2="620" y2="286" stroke="#64748b" stroke-width="2"/>',
        '<text x="825" y="222" font-family="Arial" font-size="15">1/16 in pivot rod between posts</text>',
        '<line x1="880" y1="230" x2="880" y2="250" stroke="#64748b" stroke-width="2"/>',
        '<text x="967" y="225" font-family="Arial" font-size="15">touchpiece</text>',
        '<line x1="1010" y1="232" x2="1025" y2="250" stroke="#64748b" stroke-width="2"/>',
        '<text x="735" y="377" font-family="Arial" font-size="15">spring closes pad</text>',
        '<line x1="770" y1="363" x2="765" y2="324" stroke="#64748b" stroke-width="2"/>',
        '<text x="60" y="610" font-family="Arial" font-size="20" font-weight="700">Key Variables</text>',
        '<text x="60" y="644" font-family="Arial" font-size="15">CLM_K01_Dia_in, CLM_K01_Pad_OD_in, CLM_K01_Lever_L_in, CLM_Key_Pivot_Rod_Dia_in, CLM_Pad_Overhang_in.</text>',
        '<text x="60" y="674" font-family="Arial" font-size="15">Default state: pad closed. Press lever to open. Add cork/felt stops to set key lift around 0.060-0.100 in.</text>',
        '<text x="60" y="704" font-family="Arial" font-size="15">Leak-test before pitch tuning. A tiny leak will make the acoustic model look wrong.</text>',
        '<rect x="60" y="760" width="1480" height="78" fill="none" stroke="#0f172a" stroke-width="2"/>',
        '<text x="80" y="792" font-family="Arial" font-size="15">REV-A. This is a mechanism drawing, not a final decorative key shape.</text>',
        '<text x="80" y="818" font-family="Arial" font-size="15">Material: brass prototype, nickel silver upgrade. Pad: leather-over-cork or clarinet skin pad.</text>',
        "</svg>",
    ]
    write_text("drawings/keywork-lever-detail.svg", "\n".join(lines))


def xlsx_col(n: int) -> str:
    s = ""
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def sheet_xml(rows: list[list[dict[str, object]]]) -> str:
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">',
        "<sheetViews><sheetView workbookViewId=\"0\"><pane ySplit=\"1\" topLeftCell=\"A2\" activePane=\"bottomLeft\" state=\"frozen\"/></sheetView></sheetViews>",
        "<sheetData>",
    ]
    for r_idx, row in enumerate(rows, 1):
        out.append(f'<row r="{r_idx}">')
        for c_idx, cell in enumerate(row, 1):
            ref = f"{xlsx_col(c_idx)}{r_idx}"
            style = int(cell.get("style", 0))
            value = cell.get("value", "")
            formula = cell.get("formula")
            if formula:
                out.append(f'<c r="{ref}" s="{style}"><f>{html.escape(str(formula))}</f></c>')
            elif isinstance(value, (int, float)):
                out.append(f'<c r="{ref}" s="{style}"><v>{value}</v></c>')
            else:
                out.append(f'<c r="{ref}" s="{style}" t="inlineStr"><is><t>{html.escape(str(value))}</t></is></c>')
        out.append("</row>")
    out += ["</sheetData>", "</worksheet>"]
    return "\n".join(out)


def cell(value: object = "", style: int = 0, formula: str | None = None) -> dict[str, object]:
    return {"value": value, "style": style, "formula": formula}


def write_xlsx() -> None:
    family = family_rows()
    schedule = hole_schedule()
    key_rows_path = ROOT / "hardware/keywork-parts.csv"
    with key_rows_path.open(newline="", encoding="utf-8") as h:
        key_rows = list(csv.DictReader(h))

    sheets: list[tuple[str, list[list[dict[str, object]]]]] = []
    rows = [
        [cell("Chalumeau Family Parametric Design Table", 1)],
        [cell("Input", 2), cell("Unit", 2), cell("Value", 2), cell("Notes", 2)],
        [cell("Speed of sound", 0), cell("in/s"), cell(SOS_IN_PER_SEC, 3), cell("blue input; adjust for temperature")],
        [cell("Bell end correction factor", 0), cell("radius multiple"), cell(0.61, 3), cell("open-end first pass")],
        [cell("Reed end correction factor", 0), cell("bore ID multiple"), cell(0.25, 3), cell("first-pass reed/mouthpiece compliance")],
        [],
        [
            cell("Instrument ID", 2),
            cell("Variant", 2),
            cell("Root MIDI", 2),
            cell("Bore ID in", 2),
            cell("Wall in", 2),
            cell("Root Hz", 2),
            cell("Acoustic L in", 2),
            cell("Body L final in", 2),
            cell("Blank L in", 2),
            cell("Body OD in", 2),
            cell("Bell OD in", 2),
        ],
    ]
    for idx, v in enumerate(VARIANTS, 8):
        rows.append(
            [
                cell(v["id"]),
                cell(v["variant"]),
                cell(v["root_midi"], 3),
                cell(v["bore_id_in"], 3),
                cell(v["wall_in"], 3),
                cell(style=4, formula=f"440*POWER(2,(C{idx}-69)/12)"),
                cell(style=4, formula=f"$C$3/(4*F{idx})"),
                cell(style=4, formula=f"G{idx}-$C$4*(D{idx}/2)-$C$5*D{idx}"),
                cell(style=4, formula=f"H{idx}+1.5"),
                cell(style=4, formula=f"D{idx}+2*E{idx}"),
                cell(v["bell_od_in"], 3),
            ]
        )
    sheets.append(("Family Spec", rows))

    rows = [
        [cell("Tone Hole Schedule", 1)],
        [
            cell("Variant ID", 2),
            cell("Hole ID", 2),
            cell("Offset", 2),
            cell("Note", 2),
            cell("Target Hz", 2),
            cell("Hole Dia in", 2),
            cell("X From Bell in", 2),
            cell("Control", 2),
            cell("Tier", 2),
        ],
    ]
    for r in schedule:
        rows.append(
            [
                cell(r["variant_id"]),
                cell(r["hole_id"]),
                cell(r["semitone_offset"]),
                cell(r["note"]),
                cell(r["target_freq_hz"]),
                cell(r["hole_dia_in"], 3 if str(r["hole_id"]).startswith("K") else 0),
                cell(r["x_from_bell_in"]),
                cell(r["control"]),
                cell(r["tier"]),
            ]
        )
    sheets.append(("Tone Holes", rows))

    rows = [
        [cell("Keywork Levers", 1)],
        [cell(k, 2) for k in key_rows[0].keys()],
    ]
    for r in key_rows:
        rows.append([cell(r[k], 3 if k in {"tone_hole_dia_in", "pad_od_in", "lever_length_in"} else 0) for k in key_rows[0].keys()])
    sheets.append(("Keywork", rows))

    with (ROOT / "cad/solidworks-design-table.csv").open(newline="", encoding="utf-8") as h:
        sw = list(csv.reader(h))
    rows = [[cell("SolidWorks Export", 1)]]
    for idx, r in enumerate(sw):
        rows.append([cell(x, 2 if idx == 0 else 0) for x in r])
    sheets.append(("SolidWorks Export", rows))

    path = ROOT / "chalumeau-family-design-table.xlsx"
    with ZipFile(path, "w", ZIP_DEFLATED) as z:
        z.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            + "".join(
                f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
                for i in range(1, len(sheets) + 1)
            )
            + "</Types>",
        )
        z.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            "</Relationships>",
        )
        z.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            "<sheets>"
            + "".join(
                f'<sheet name="{html.escape(name)}" sheetId="{i}" r:id="rId{i}"/>'
                for i, (name, _) in enumerate(sheets, 1)
            )
            + "</sheets><calcPr calcMode=\"auto\"/></workbook>",
        )
        z.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(
                f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
                for i in range(1, len(sheets) + 1)
            )
            + f'<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            + "</Relationships>",
        )
        z.writestr(
            "xl/styles.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<fonts count="4">'
            '<font><sz val="11"/><name val="Calibri"/></font>'
            '<font><b/><sz val="16"/><color rgb="FF1F2937"/><name val="Calibri"/></font>'
            '<font><b/><sz val="11"/><color rgb="FFFFFFFF"/><name val="Calibri"/></font>'
            '<font><sz val="11"/><color rgb="FF0000FF"/><name val="Calibri"/></font>'
            '</fonts>'
            '<fills count="5">'
            '<fill><patternFill patternType="none"/></fill>'
            '<fill><patternFill patternType="gray125"/></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FFD6E4F0"/><bgColor indexed="64"/></patternFill></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FF1F4E79"/><bgColor indexed="64"/></patternFill></fill>'
            '<fill><patternFill patternType="solid"><fgColor rgb="FFE5E7EB"/><bgColor indexed="64"/></patternFill></fill>'
            '</fills>'
            '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
            '<cellXfs count="5">'
            '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
            '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
            '<xf numFmtId="0" fontId="2" fillId="3" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
            '<xf numFmtId="0" fontId="3" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/>'
            '<xf numFmtId="0" fontId="0" fillId="4" borderId="0" xfId="0" applyFill="1"/>'
            '</cellXfs>'
            '</styleSheet>',
        )
        for i, (_, rows) in enumerate(sheets, 1):
            z.writestr(f"xl/worksheets/sheet{i}.xml", sheet_xml(rows))


def main() -> None:
    ensure_dirs()
    write_core_csvs()
    write_markdown_docs()
    write_wolfram()
    write_openscad()
    write_drawings()
    write_xlsx()
    manifest = {
        "generated": TODAY,
        "root": str(ROOT),
        "primary_outputs": [
            "README.md",
            "design.md",
            "chalumeau-family-design-table.xlsx",
            "family-spec.csv",
            "data/tone-hole-schedule.csv",
            "hardware/lever-fabrication-guide.md",
            "cad/solidworks-design-table.csv",
            "drawings/chalumeau-family-sheet.svg",
        ],
    }
    write_text("data/generation-manifest.json", json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()

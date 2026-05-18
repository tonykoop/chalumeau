#!/usr/bin/env python3
"""Create lightweight presentation exports without third-party packages."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import textwrap
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
PRESENTATION_ROOT = ROOT / "build" / "presentation"


def plain_text(markdown: str) -> str:
    text = markdown
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("`", "")
    text = text.replace("*", "")
    text = text.replace("|", " | ")
    return text


def pdf_escape(text: str) -> str:
    safe = text.encode("latin-1", "replace").decode("latin-1")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_pdf(markdown_path: Path, pdf_path: Path) -> None:
    raw = plain_text(markdown_path.read_text(encoding="utf-8", errors="replace"))
    lines: list[str] = []
    for source in raw.splitlines():
        stripped = source.strip()
        if not stripped:
            lines.append("")
            continue
        if stripped.startswith("#"):
            stripped = stripped.lstrip("#").strip().upper()
        if stripped == "---":
            lines.append("\f")
            continue
        wrapped = textwrap.wrap(stripped, width=96) or [""]
        lines.extend(wrapped)

    pages: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if line == "\f" or len(current) >= 48:
            pages.append(current)
            current = []
            if line == "\f":
                continue
        current.append(line)
    if current:
        pages.append(current)

    objects: list[bytes] = []

    def add(obj: str | bytes) -> int:
        data = obj if isinstance(obj, bytes) else obj.encode("latin-1", "replace")
        objects.append(data)
        return len(objects)

    add("<< /Type /Catalog /Pages 2 0 R >>")
    pages_obj_index = add(b"")
    font_obj_index = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    page_obj_numbers: list[int] = []
    for page_num, page_lines in enumerate(pages, 1):
        stream_lines = ["BT", "/F1 10 Tf", "54 740 Td", "14 TL"]
        for idx, line in enumerate(page_lines):
            if idx == 0:
                stream_lines.append(f"({pdf_escape(line)}) Tj")
            else:
                stream_lines.append(f"T* ({pdf_escape(line)}) Tj")
        stream_lines.append("ET")
        stream = "\n".join(stream_lines).encode("latin-1", "replace")
        content_index = add(
            b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream"
        )
        page_index = add(
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_obj_index} 0 R >> >> "
            f"/Contents {content_index} 0 R >>"
        )
        page_obj_numbers.append(page_index)

    kids = " ".join(f"{n} 0 R" for n in page_obj_numbers)
    objects[pages_obj_index - 1] = f"<< /Type /Pages /Kids [{kids}] /Count {len(page_obj_numbers)} >>".encode("latin-1")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for idx, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref_pos = len(output)
    output.extend(f"xref\n0 {len(objects)+1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f\n")
    for off in offsets[1:]:
        output.extend(f"{off:010d} 00000 n\n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    pdf_path.write_bytes(bytes(output))


def extract_slides(deck_md: str) -> list[tuple[str, list[str]]]:
    slides: list[tuple[str, list[str]]] = []
    for chunk in re.split(r"\n---\n", deck_md):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = [line.rstrip() for line in chunk.splitlines()]
        title = "Slide"
        body: list[str] = []
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
            elif line.startswith("- "):
                body.append(line[2:].strip())
            elif line and not line.startswith("_Speaker notes"):
                if not line.startswith("|") and not line.startswith("```"):
                    body.append(line.strip())
        slides.append((title, body[:7]))
    return slides[:16]


def escape_xml(text: str) -> str:
    return html.escape(text.encode("ascii", "replace").decode("ascii"))


def text_shape(shape_id: int, x: int, y: int, cx: int, cy: int, text: str, size: int = 2400, bold: bool = False) -> str:
    bold_attr = ' b="1"' if bold else ""
    paragraphs = []
    for para in text.split("\n"):
        paragraphs.append(
            f'<a:p><a:r><a:rPr lang="en-US" sz="{size}"{bold_attr}/><a:t>{escape_xml(para)}</a:t></a:r></a:p>'
        )
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{shape_id}" name="Text {shape_id}"/>'
        '<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square"/><a:lstStyle/>{"".join(paragraphs)}</p:txBody></p:sp>'
    )


def slide_xml(title: str, bullets: list[str], slide_num: int) -> str:
    bullet_text = "\n".join(f"- {b}" for b in bullets)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></p:bgPr></p:bg>'
        '<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '<p:sp><p:nvSpPr><p:cNvPr id="2" name="Accent"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
        '<p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="9144000" cy="230000"/></a:xfrm>'
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="1F4E79"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>'
        f'{text_shape(3, 420000, 520000, 8300000, 780000, title, 3200, True)}'
        f'{text_shape(4, 620000, 1450000, 8000000, 4200000, bullet_text, 1900, False)}'
        f'{text_shape(5, 7400000, 6400000, 1200000, 280000, f"Slide {slide_num}", 1100, False)}'
        '</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'
    )


def make_pptx(deck_path: Path, pptx_path: Path) -> None:
    slides = extract_slides(deck_path.read_text(encoding="utf-8", errors="replace"))
    if not slides:
        slides = [("Chalumeau Family Capstone", ["See design.md and print-packet.md."])]

    with ZipFile(pptx_path, "w", ZIP_DEFLATED) as z:
        z.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>'
            '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>'
            '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>'
            '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            + "".join(
                f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
                for i in range(1, len(slides) + 1)
            )
            + "</Types>",
        )
        z.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            '</Relationships>',
        )
        z.writestr(
            "docProps/core.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>Chalumeau Family Capstone</dc:title><dc:creator>Codex</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{dt.datetime.now(dt.UTC).isoformat()}</dcterms:created></cp:coreProperties>',
        )
        z.writestr(
            "docProps/app.xml",
            f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Codex</Application><PresentationFormat>On-screen Show (16:9)</PresentationFormat><Slides>{len(slides)}</Slides></Properties>',
        )
        slide_id_list = "".join(
            f'<p:sldId id="{256+i}" r:id="rId{i}"/>' for i in range(1, len(slides) + 1)
        )
        z.writestr(
            "ppt/presentation.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId{len(slides)+1}"/></p:sldMasterIdLst><p:sldIdLst>{slide_id_list}</p:sldIdLst>'
            '<p:sldSz cx="9144000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>',
        )
        rels = [
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
            for i in range(1, len(slides) + 1)
        ]
        rels.append(
            f'<Relationship Id="rId{len(slides)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>'
        )
        z.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(rels)
            + "</Relationships>",
        )
        z.writestr(
            "ppt/slideMasters/slideMaster1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst></p:sldMaster>',
        )
        z.writestr(
            "ppt/slideMasters/_rels/slideMaster1.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>',
        )
        z.writestr(
            "ppt/slideLayouts/slideLayout1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld></p:sldLayout>',
        )
        z.writestr(
            "ppt/theme/theme1.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Chalumeau"><a:themeElements><a:clrScheme name="Chalumeau"><a:dk1><a:srgbClr val="111827"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="1F2937"/></a:dk2><a:lt2><a:srgbClr val="F8FAFC"/></a:lt2><a:accent1><a:srgbClr val="1F4E79"/></a:accent1><a:accent2><a:srgbClr val="92400E"/></a:accent2><a:accent3><a:srgbClr val="C9A227"/></a:accent3><a:accent4><a:srgbClr val="475569"/></a:accent4><a:accent5><a:srgbClr val="0F766E"/></a:accent5><a:accent6><a:srgbClr val="991B1B"/></a:accent6><a:hlink><a:srgbClr val="0563C1"/></a:hlink><a:folHlink><a:srgbClr val="954F72"/></a:folHlink></a:clrScheme><a:fontScheme name="Office"><a:majorFont><a:latin typeface="Arial"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/></a:minorFont></a:fontScheme><a:fmtScheme name="Office"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>',
        )
        for i, (title, bullets) in enumerate(slides, 1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml(title, bullets, i))
            z.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>',
            )


def update_manifest(canonical_root: Path | None) -> None:
    path = PRESENTATION_ROOT / "capstone-manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    canonical = canonical_root or ROOT
    outputs_root = canonical / "build" / "presentation"
    outputs = manifest.setdefault("outputs", {})
    outputs["capstone_deck_markdown"] = str(outputs_root / "capstone-deck.md")
    outputs["capstone_deck_pptx"] = str(outputs_root / "capstone-deck.pptx")
    outputs["print_packet_markdown"] = str(outputs_root / "print-packet.md")
    outputs["print_packet_html"] = str(outputs_root / "print-packet.html")
    outputs["print_packet_pdf"] = str(outputs_root / "print-packet.pdf")
    notes = manifest.setdefault("notes", [])
    note = "PPTX/PDF binaries generated by tools/export_capstone_binaries.py using standard-library exporters."
    manifest["notes"] = list(dict.fromkeys([*notes, note]))
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-root",
        help="Absolute repo root to record in capstone-manifest.json output paths.",
    )
    args = parser.parse_args()

    canonical_root = Path(args.canonical_root).resolve() if args.canonical_root else None
    make_pdf(PRESENTATION_ROOT / "print-packet.md", PRESENTATION_ROOT / "print-packet.pdf")
    make_pptx(PRESENTATION_ROOT / "capstone-deck.md", PRESENTATION_ROOT / "capstone-deck.pptx")
    update_manifest(canonical_root)


if __name__ == "__main__":
    main()

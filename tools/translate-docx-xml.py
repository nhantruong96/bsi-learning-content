from __future__ import annotations

import argparse
import importlib.util
import io
import json
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"

W_P = f"{{{W_NS}}}p"
W_T = f"{{{W_NS}}}t"
W_BR = f"{{{W_NS}}}br"
W_CR = f"{{{W_NS}}}cr"
W_TAB = f"{{{W_NS}}}tab"

PROCESSABLE_ROOTS = {
    f"{{{W_NS}}}document",
    f"{{{W_NS}}}hdr",
    f"{{{W_NS}}}ftr",
    f"{{{W_NS}}}footnotes",
    f"{{{W_NS}}}endnotes",
    f"{{{W_NS}}}comments",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Translate DOCX XML content to Vietnamese.")
    parser.add_argument("--input", required=True, help="Input DOCX path.")
    parser.add_argument("--output", required=True, help="Output DOCX path.")
    parser.add_argument("--config", required=True, help="Base translation config JSON.")
    parser.add_argument("--override", help="Optional deck-specific override JSON.")
    parser.add_argument("--cache", required=True, help="Translation cache JSON path.")
    return parser.parse_args()


def load_ppt_translation_module(script_dir: Path):
    module_path = script_dir / "build-ppt-translation-json.py"
    spec = importlib.util.spec_from_file_location("ppt_translation_builder", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load translation helpers from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_paragraph_content(root: ET.Element, current: ET.Element):
    if current is not root and current.tag == W_P:
        return

    yield current
    for child in list(current):
        yield from iter_paragraph_content(root, child)


def paragraph_segments(paragraph: ET.Element) -> list[list[ET.Element]]:
    segments: list[list[ET.Element]] = []
    current: list[ET.Element] = []

    for elem in iter_paragraph_content(paragraph, paragraph):
        if elem.tag == W_T:
            current.append(elem)
            continue

        if elem.tag in {W_BR, W_CR, W_TAB}:
            if current:
                segments.append(current)
                current = []

    if current:
        segments.append(current)

    return segments


def segment_text(segment: list[ET.Element]) -> str:
    return "".join(node.text or "" for node in segment)


def write_segment(segment: list[ET.Element], text: str) -> None:
    first = segment[0]
    first.text = text
    if text[:1].isspace() or text[-1:].isspace():
        first.set(f"{{{XML_NS}}}space", "preserve")
    else:
        first.attrib.pop(f"{{{XML_NS}}}space", None)

    for node in segment[1:]:
        node.text = ""
        node.attrib.pop(f"{{{XML_NS}}}space", None)


def should_process_xml(name: str, raw: bytes) -> bool:
    if not (name.startswith("word/") and name.endswith(".xml")):
        return False

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return False

    return root.tag in PROCESSABLE_ROOTS


def extract_namespaces(raw: bytes) -> list[tuple[str, str]]:
    namespaces: list[tuple[str, str]] = []
    for event, value in ET.iterparse(io.BytesIO(raw), events=("start-ns",)):
        prefix, uri = value
        namespaces.append((prefix or "", uri))
        ET.register_namespace(prefix or "", uri)
    return namespaces


def inject_missing_namespace_declarations(xml_bytes: bytes, namespaces: list[tuple[str, str]]) -> bytes:
    xml_text = xml_bytes.decode("utf-8")
    declaration_end = xml_text.find("?>")
    search_start = declaration_end + 2 if declaration_end != -1 else 0
    root_end = xml_text.find(">", search_start)
    if root_end == -1:
        return xml_bytes

    head = xml_text[:root_end]
    tail = xml_text[root_end:]
    additions: list[str] = []

    for prefix, uri in namespaces:
        attr = f'xmlns:{prefix}="{uri}"' if prefix else f'xmlns="{uri}"'
        if attr not in head:
            additions.append(attr)

    if not additions:
        return xml_bytes

    patched = f"{head} {' '.join(additions)}{tail}"
    return patched.encode("utf-8")


def translate_xml_part(
    xml_bytes: bytes,
    *,
    module,
    translator,
    cache: dict[str, str],
    config: dict,
) -> tuple[bytes, int]:
    namespaces = extract_namespaces(xml_bytes)
    root = ET.fromstring(xml_bytes)
    updated = 0

    for paragraph in root.iter(W_P):
        for segment in paragraph_segments(paragraph):
            original = segment_text(segment)
            if not original.strip():
                continue

            translated = module.translate_text(original, translator, cache, config)
            if module.normalize(translated) == module.normalize(original):
                continue

            write_segment(segment, translated)
            updated += 1

    serialized = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    serialized = inject_missing_namespace_declarations(serialized, namespaces)
    return serialized, updated


def main() -> int:
    args = parse_args()

    source = Path(args.input)
    output = Path(args.output)
    config_path = Path(args.config)
    override_path = Path(args.override) if args.override else None
    cache_path = Path(args.cache)
    output.parent.mkdir(parents=True, exist_ok=True)

    module = load_ppt_translation_module(Path(__file__).resolve().parent)
    config = module.load_config(config_path, override_path)
    config = module.normalize_override_maps(config)
    cache = module.load_cache(cache_path)
    translator = module.GoogleTranslator(source="auto", target=config["target_language"])

    updated_parts = 0
    updated_segments = 0

    with ZipFile(source, "r") as zin, ZipFile(output, "w") as zout:
        for info in zin.infolist():
            raw = zin.read(info.filename)
            if should_process_xml(info.filename, raw):
                translated_bytes, part_updates = translate_xml_part(
                    raw,
                    module=module,
                    translator=translator,
                    cache=cache,
                    config=config,
                )
                raw = translated_bytes
                if part_updates:
                    updated_parts += 1
                    updated_segments += part_updates

            zout.writestr(info, raw)

    module.save_cache(cache_path, cache)
    print(f"Translated DOCX saved to: {output}")
    print(json.dumps({"updated_parts": updated_parts, "updated_segments": updated_segments}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

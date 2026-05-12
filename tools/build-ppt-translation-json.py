from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: deep-translator. Install with `pip install deep-translator`."
    ) from exc


BREAK_RE = re.compile(r"(\r\n|\r|\n|\x0b|\f)")
SPACE_RE = re.compile(r"\s+")
ASCII_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9&'./:-]*")

DEFAULT_CONFIG = {
    "target_language": "vi",
    "thresholds": {
        "notes_bad_words": 4,
        "notes_ratio": 0.20,
        "slide_bad_words": 3,
        "slide_ratio": 0.28,
    },
    "allow_english": [],
    "keep_patterns": [],
    "protected_terms": [],
    "text_overrides": {},
    "full_overrides": {},
    "global_replacements": {},
    "path_overrides": {},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a PowerPoint translation updates JSON from extracted PPT JSON."
    )
    parser.add_argument("--source-json", required=True, help="Extracted JSON from the source PPT.")
    parser.add_argument(
        "--current-json",
        help="Extracted JSON from the current translated PPT. If omitted, all eligible text is translated.",
    )
    parser.add_argument("--config", required=True, help="Base translation config JSON.")
    parser.add_argument("--override", help="Optional deck-specific override JSON.")
    parser.add_argument("--cache", required=True, help="Translation cache JSON path.")
    parser.add_argument("--output", required=True, help="Output updates JSON path.")
    parser.add_argument(
        "--draft-only",
        action="store_true",
        help="Translate only English-heavy content from a single draft file when no source EN PPT exists.",
    )
    return parser.parse_args()


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def merge_config(base: dict, incoming: dict) -> dict:
    merged = json.loads(json.dumps(base))

    for key in ["target_language"]:
        if key in incoming:
            merged[key] = incoming[key]

    for key in ["allow_english", "keep_patterns", "protected_terms"]:
        if key in incoming:
            merged[key].extend(incoming[key])

    for key in ["text_overrides", "full_overrides", "global_replacements", "path_overrides"]:
        if key in incoming:
            merged[key].update(incoming[key])

    if "thresholds" in incoming:
        merged["thresholds"].update(incoming["thresholds"])

    return merged


def load_config(base_path: Path, override_path: Path | None) -> dict:
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    config = merge_config(config, load_json(base_path))
    if override_path:
        config = merge_config(config, load_json(override_path))
    config["allow_english"] = set(config["allow_english"])
    config["keep_patterns"] = [re.compile(pattern) for pattern in config["keep_patterns"]]
    config["protected_terms"] = [
        (re.compile(item["pattern"], flags=re.IGNORECASE), item["replacement"])
        for item in config["protected_terms"]
    ]
    return config


def load_cache(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(path: Path, cache: dict[str, str]) -> None:
    write_json(path, cache)


def normalize(text: str) -> str:
    text = text.replace("\x0b", "\n").replace("\f", "\n").replace("\r\n", "\n").replace("\r", "\n")
    return SPACE_RE.sub(" ", text).strip()


def has_direct_override(text: str, config: dict) -> bool:
    text_norm = normalize(text)
    return text_norm in config["full_overrides"] or text_norm in config["text_overrides"]


def normalize_override_maps(config: dict) -> dict:
    config["text_overrides"] = {
        normalize(key): value for key, value in config["text_overrides"].items()
    }
    config["full_overrides"] = {
        normalize(key): value for key, value in config["full_overrides"].items()
    }
    return config


def should_keep(text: str, config: dict) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    return any(pattern.match(stripped) for pattern in config["keep_patterns"])


def protect_terms(text: str, config: dict) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    protected = text
    counter = 0

    for pattern, replacement in sorted(
        config["protected_terms"], key=lambda item: -len(item[0].pattern)
    ):
        def repl(match: re.Match[str]) -> str:
            nonlocal counter
            token = f"ZZTERM{counter}ZZ"
            counter += 1
            placeholders[token] = replacement
            return token

        protected = pattern.sub(repl, protected)

    return protected, placeholders


def restore_terms(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for token, replacement in placeholders.items():
        restored = restored.replace(token, replacement)
    return restored


def apply_global_replacements(text: str, config: dict) -> str:
    out = text
    for old, new in config["global_replacements"].items():
        out = out.replace(old, new)

    out = re.sub(r"(?<!\w)Bạn(?!\w)", "Anh/chị", out)
    out = re.sub(r"(?<!\w)bạn(?!\w)", "anh/chị", out)
    out = out.replace("Giảng viên của anh/chị", "Giảng viên")
    out = out.replace("Giảng viên của bạn", "Giảng viên")
    out = re.sub(r"\s+([,.;:])", r"\1", out)
    return out


def english_score(text: str, config: dict) -> tuple[int, int]:
    total = 0
    bad = 0

    for token in ASCII_WORD_RE.findall(text):
        word = token.strip("'./:-")
        if not word:
            continue
        total += 1

        if word in config["allow_english"]:
            continue
        if re.fullmatch(r"[A-Z]{1,6}", word):
            continue
        if re.fullmatch(r"[A-Za-z]?\d+[A-Za-z0-9._/-]*", word):
            continue
        if re.fullmatch(r"\d+[A-Za-z0-9._/-]*", word):
            continue
        if "@" in word or word.startswith("http"):
            continue

        bad += 1

    return bad, total


def looks_english_heavy(text: str, path: str, config: dict) -> bool:
    stripped = text.strip()
    if not stripped or should_keep(stripped, config):
        return False
    if has_direct_override(stripped, config):
        return True

    bad, total = english_score(text, config)
    if total == 0:
        return False

    no_vi_chars = not re.search(
        r"[ăâđêôơưĂÂĐÊÔƠƯáàảãạắằẳẵặấầẩẫậéèẻẽẹếềểễệíìỉĩịóòỏõọốồổỗộớờởỡợúùủũụứừửữựýỳỷỹỵ]",
        text,
    )
    if no_vi_chars and total <= 8 and bad == total:
        return True

    thresholds = config["thresholds"]
    if path.startswith("notes:"):
        return bad >= thresholds["notes_bad_words"] and (bad / total) >= thresholds["notes_ratio"]

    return bad >= thresholds["slide_bad_words"] and (bad / total) >= thresholds["slide_ratio"]


def needs_translation(source_text: str, current_text: str | None, path: str, config: dict) -> bool:
    source_norm = normalize(source_text)
    if not source_norm or should_keep(source_norm, config):
        return False

    if current_text is None:
        return True

    current_norm = normalize(current_text)
    if source_norm == current_norm:
        return True

    bad, total = english_score(current_text, config)
    if total == 0:
        return False

    thresholds = config["thresholds"]
    if path.startswith("notes:"):
        return bad >= thresholds["notes_bad_words"] and (bad / total) >= thresholds["notes_ratio"]

    return bad >= thresholds["slide_bad_words"] and (bad / total) >= thresholds["slide_ratio"]


def translate_text(
    text: str,
    translator: GoogleTranslator,
    cache: dict[str, str],
    config: dict,
) -> str:
    text_norm = normalize(text)
    if text_norm in config["full_overrides"]:
        return config["full_overrides"][text_norm]
    if text_norm in config["text_overrides"]:
        return config["text_overrides"][text_norm]

    parts = BREAK_RE.split(text)
    translated_parts: list[str] = []

    for part in parts:
        if part is None:
            continue
        if BREAK_RE.fullmatch(part):
            translated_parts.append(part)
            continue

        stripped = part.strip()
        if not stripped or should_keep(stripped, config):
            translated_parts.append(part)
            continue

        stripped_norm = normalize(stripped)
        if stripped_norm in config["text_overrides"]:
            translated_parts.append(part.replace(stripped, config["text_overrides"][stripped_norm]))
            continue

        if stripped_norm in cache:
            translated = apply_global_replacements(cache[stripped_norm], config)
            cache[stripped_norm] = translated
        else:
            protected, placeholders = protect_terms(stripped, config)
            translated = translator.translate(protected)
            if translated is None:
                translated = stripped
            translated = restore_terms(translated, placeholders)
            translated = apply_global_replacements(translated, config)
            cache[stripped_norm] = translated

        translated_parts.append(part.replace(stripped, translated))

    return "".join(translated_parts)


def build_entry_map(payload: dict) -> dict[tuple[int, str], str]:
    return {
        (int(slide["slide"]), str(entry["path"])): str(entry["text"])
        for slide in payload["slides"]
        for entry in slide["entries"]
    }


def main() -> int:
    args = parse_args()

    source_path = Path(args.source_json)
    current_path = Path(args.current_json) if args.current_json else None
    config_path = Path(args.config)
    override_path = Path(args.override) if args.override else None
    cache_path = Path(args.cache)
    output_path = Path(args.output)

    source_payload = load_json(source_path)
    current_payload = load_json(current_path) if current_path else None
    config = load_config(config_path, override_path)
    config = normalize_override_maps(config)
    cache = load_cache(cache_path)

    source_map = build_entry_map(source_payload)
    current_map = build_entry_map(current_payload) if current_payload else {}
    translator = GoogleTranslator(source="auto", target=config["target_language"])

    updates: list[dict[str, object]] = []
    processed = 0

    for slide in source_payload["slides"]:
        slide_number = int(slide["slide"])
        for entry in slide["entries"]:
            path = str(entry["path"])
            source_text = str(entry["text"])
            key = (slide_number, path)
            key_str = f"{slide_number}|{path}"
            current_text = current_map.get(key)
            forced_text = config["path_overrides"].get(key_str)

            if forced_text is None:
                if args.draft_only:
                    if not looks_english_heavy(source_text, path, config):
                        continue
                elif not needs_translation(source_text, current_text, path, config):
                    continue

            translated = forced_text or translate_text(source_text, translator, cache, config)
            translated = translated.replace("\x0b", "\r")

            if (
                current_text is not None
                and not args.draft_only
                and normalize(translated) == normalize(current_text)
            ):
                continue

            updates.append(
                {
                    "slide": slide_number,
                    "path": path,
                    "text": translated,
                }
            )

            processed += 1
            if processed % 40 == 0:
                save_cache(cache_path, cache)
                time.sleep(0.1)

    save_cache(cache_path, cache)
    write_json(output_path, updates)
    print(f"Wrote {output_path} with {len(updates)} updates")
    return 0


if __name__ == "__main__":
    sys.exit(main())

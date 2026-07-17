from __future__ import annotations

import csv
import hashlib
import argparse
import os
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path


DRIVE_ROOT = Path(r"G:\Mi unidad")
INVENTORY_DIR = DRIVE_ROOT / "00_INVENTARIO"
CONVERSATIONS_DIR = DRIVE_ROOT / "01_CONVERSACIONES_POR_IA"
CANONICAL_DIR = DRIVE_ROOT / "00_CORPUS_CANONICO"

GDOCS_MANIFEST = INVENTORY_DIR / "00_GDOCS_CONVERSION_MANIFEST.csv"
DEDUP_OUTPUT = INVENTORY_DIR / "duplicados_md5_verificados.csv"
HASH_CACHE = INVENTORY_DIR / "hash_cache_size_dups.csv"
SUMMARY_OUTPUT = INVENTORY_DIR / "00_VERIFICACION_CORPUS_NEXUS_2026-06-07.md"

CHUNK_LIMIT_BYTES = 850_000


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def md5_file(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_stat(path: Path):
    try:
        st = path.stat()
        return st.st_size, datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds"), ""
    except Exception as exc:  # noqa: BLE001 - report every inaccessible file.
        return 0, "", f"stat_error: {exc}"


def infer_platform(path: Path) -> str:
    try:
        rel = path.relative_to(CONVERSATIONS_DIR)
        return rel.parts[0] if rel.parts else "unknown"
    except ValueError:
        try:
            path.relative_to(CANONICAL_DIR)
            return "CORPUS_CANONICO"
        except ValueError:
            return "unknown"


def infer_date_and_part(path: Path):
    name = path.stem
    date_match = re.search(r"(20\d{2})[-_](\d{2})[-_](\d{2})", name)
    date = "-".join(date_match.groups()) if date_match else ""
    part_match = re.search(r"(?:parte|part|chunk)[_-]?(\d+)", name, flags=re.IGNORECASE)
    part = part_match.group(1) if part_match else ""
    return date, part


def iter_manifest_sources():
    for root in (CONVERSATIONS_DIR, CANONICAL_DIR):
        if root.exists():
            yield from sorted(
                (p for p in root.rglob("*") if p.is_file()),
                key=lambda p: str(p).lower(),
            )


def gdoc_status(path: Path, bytes_len: int) -> tuple[str, str]:
    ext = path.suffix.lower()
    if ext == ".gdoc":
        return "already_native_marker", "Local .gdoc shortcut/marker; verify Drive URL if needed."
    if ext in {".docx", ".doc", ".odt", ".rtf", ".txt", ".html", ".htm"}:
        if bytes_len <= CHUNK_LIMIT_BYTES:
            return "ready_to_import_native_gdoc", "Accepted import type and below chunk limit."
        return "needs_split_before_import", f"Accepted import type but > {CHUNK_LIMIT_BYTES} bytes."
    if ext == ".md":
        if bytes_len <= CHUNK_LIMIT_BYTES:
            return "needs_txt_or_html_wrapper", "Markdown is not accepted directly by current import tool; convert to .txt/.html first."
        return "needs_split_and_txt_or_html_wrapper", "Markdown > chunk limit; split and wrap before import."
    return "not_a_document_import_candidate", f"Extension {ext or '(none)'} not targeted for GDocs conversion."


def write_gdocs_manifest():
    INVENTORY_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    counts = defaultdict(int)
    for path in iter_manifest_sources():
        bytes_len, modified, note = safe_stat(path)
        date, part = infer_date_and_part(path)
        try:
            digest = sha256_file(path)
        except Exception as exc:  # noqa: BLE001
            digest = ""
            note = (note + "; " if note else "") + f"sha256_error: {exc}"
        status, status_note = gdoc_status(path, bytes_len)
        notes = "; ".join(x for x in (status_note, note) if x)
        row = {
            "platform": infer_platform(path),
            "source_path": str(path),
            "title": path.stem,
            "date": date,
            "part": part,
            "bytes": bytes_len,
            "sha256": digest,
            "output_gdoc_url": "",
            "status": status,
            "notes": notes,
            "modified_time": modified,
        }
        rows.append(row)
        counts[(row["platform"], status)] += 1

    with GDOCS_MANIFEST.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "platform",
                "source_path",
                "title",
                "date",
                "part",
                "bytes",
                "sha256",
                "output_gdoc_url",
                "status",
                "notes",
                "modified_time",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)
    return rows, counts


def load_hash_cache() -> dict[tuple[str, str], str]:
    cache: dict[tuple[str, str], str] = {}
    if HASH_CACHE.exists():
        with HASH_CACHE.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cache[(row.get("ruta", ""), row.get("bytes", ""))] = row.get("md5", "")
    return cache


def save_hash_cache(cache_rows):
    with HASH_CACHE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ruta", "bytes", "md5", "status", "note"])
        writer.writeheader()
        writer.writerows(cache_rows)


def write_verified_duplicates(max_hash_files: int | None = None):
    inventory = INVENTORY_DIR / "inventario_completo.csv"
    if not inventory.exists():
        raise FileNotFoundError(f"Missing inventory: {inventory}")

    size_groups: dict[int, list[dict[str, str]]] = defaultdict(list)
    with inventory.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            try:
                size = int(float(row.get("bytes", "0") or 0))
            except ValueError:
                continue
            if size > 0:
                row["_bytes_int"] = size
                size_groups[size].append(row)

    candidates = [
        row
        for size, group in size_groups.items()
        if len(group) > 1
        for row in group
    ]
    candidates.sort(key=lambda r: (-int(r["_bytes_int"]), r.get("ruta", "")))
    if max_hash_files is not None:
        candidates = candidates[:max_hash_files]

    cache = load_hash_cache()
    cache_rows = []
    md5_groups: dict[tuple[int, str], list[dict[str, str]]] = defaultdict(list)
    hashed = 0
    missing = 0
    errors = 0

    for row in candidates:
        ruta = row.get("ruta", "")
        size_text = str(row["_bytes_int"])
        key = (ruta, size_text)
        digest = cache.get(key, "")
        status = "cached" if digest else "hashed"
        note = ""
        if not digest:
            try:
                digest = md5_file(Path(ruta))
                hashed += 1
            except FileNotFoundError:
                status = "missing"
                note = "file_not_found"
                missing += 1
            except Exception as exc:  # noqa: BLE001
                status = "error"
                note = str(exc)
                errors += 1
        cache_rows.append({"ruta": ruta, "bytes": size_text, "md5": digest, "status": status, "note": note})
        if digest:
            md5_groups[(int(row["_bytes_int"]), digest)].append(row)

    save_hash_cache(cache_rows)

    duplicate_rows = []
    group_id = 0
    reclaimable = 0
    for (size, digest), group in sorted(md5_groups.items(), key=lambda x: (-x[0][0], x[0][1])):
        if len(group) < 2:
            continue
        group_id += 1
        sorted_group = sorted(group, key=lambda r: r.get("ruta", "").lower())
        keep = sorted_group[0]
        for idx, row in enumerate(sorted_group):
            action = "KEEP" if idx == 0 else "MOVE_TO_99_DUPLICADOS_AFTER_OK"
            if idx > 0:
                reclaimable += size
            duplicate_rows.append(
                {
                    "group_id": group_id,
                    "action": action,
                    "md5": digest,
                    "bytes": size,
                    "nombre": row.get("nombre", ""),
                    "ruta": row.get("ruta", ""),
                    "keep_ruta": keep.get("ruta", ""),
                    "ext": row.get("ext", ""),
                }
            )

    with DEDUP_OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["group_id", "action", "md5", "bytes", "nombre", "ruta", "keep_ruta", "ext"],
        )
        writer.writeheader()
        writer.writerows(duplicate_rows)

    return {
        "inventory_rows": sum(len(group) for group in size_groups.values()),
        "size_duplicate_candidates": len(candidates),
        "hash_cache_rows": len(cache_rows),
        "hashed_this_run": hashed,
        "missing": missing,
        "errors": errors,
        "duplicate_groups": group_id,
        "duplicate_rows": len(duplicate_rows),
        "reclaimable_bytes_after_keep": reclaimable,
    }


def write_summary(manifest_rows, manifest_counts, dedup_summary):
    platform_counts = defaultdict(int)
    status_counts = defaultdict(int)
    for row in manifest_rows:
        platform_counts[row["platform"]] += 1
        status_counts[row["status"]] += 1

    lines = [
        "# Verificacion Corpus NEXUS - 2026-06-07",
        "",
        "## GDocs manifest",
        f"- Manifest: `{GDOCS_MANIFEST}`",
        f"- Source files indexed: {len(manifest_rows):,}",
        "",
        "### By platform",
    ]
    for platform, count in sorted(platform_counts.items()):
        lines.append(f"- {platform}: {count:,}")
    lines += ["", "### By conversion status"]
    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count:,}")

    lines += [
        "",
        "## MD5 duplicate verification",
        f"- Output: `{DEDUP_OUTPUT}`",
    ]
    for key, value in dedup_summary.items():
        if key.endswith("bytes_after_keep"):
            lines.append(f"- {key}: {value:,} bytes ({value / (1024 ** 3):.2f} GiB)")
        else:
            lines.append(f"- {key}: {value:,}")
    lines += [
        "",
        "## Safety",
        "- No files were deleted.",
        "- No duplicate files were moved; rows marked MOVE_TO_99_DUPLICADOS_AFTER_OK require explicit user approval.",
        "- Markdown files still need .txt/.html wrapping before native Google Docs import with the current connector.",
    ]
    SUMMARY_OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Audit NEXUS corpus manifests and duplicate candidates.")
    parser.add_argument("--manifest-only", action="store_true", help="Only create the GDocs conversion manifest.")
    parser.add_argument("--max-hash-files", type=int, default=None, help="Limit duplicate candidate files to hash.")
    args = parser.parse_args()
    manifest_rows, manifest_counts = write_gdocs_manifest()
    if args.manifest_only:
        dedup_summary = {
            "inventory_rows": 0,
            "size_duplicate_candidates": 0,
            "hash_cache_rows": 0,
            "hashed_this_run": 0,
            "missing": 0,
            "errors": 0,
            "duplicate_groups": 0,
            "duplicate_rows": 0,
            "reclaimable_bytes_after_keep": 0,
        }
    else:
        dedup_summary = write_verified_duplicates(max_hash_files=args.max_hash_files)
    write_summary(manifest_rows, manifest_counts, dedup_summary)
    print(f"manifest={GDOCS_MANIFEST}")
    print(f"dedup={DEDUP_OUTPUT}")
    print(f"summary={SUMMARY_OUTPUT}")
    print(f"manifest_rows={len(manifest_rows)}")
    for k, v in dedup_summary.items():
        print(f"{k}={v}")


if __name__ == "__main__":
    main()

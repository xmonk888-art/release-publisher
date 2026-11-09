"""Check a candidate or downloaded release file, optionally extract a validated ZIP."""

import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import shutil
import stat
import sys
import zipfile


def sha256(file):
    digest = hashlib.sha256()
    with file.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def zip_members(archive):
    members = []
    seen = set()
    files = set()
    for item in archive.infolist():
        name = item.orig_filename
        parts = name.rstrip("/").split("/")
        windows = PureWindowsPath(name)
        if (not name or "\\" in name or windows.drive or windows.root
                or any(p in ("", ".", "..") or p.rstrip(" .") != p or PureWindowsPath(p).is_reserved()
                       or re.search(r'[<>:"|?*\x00-\x1f]', p) for p in parts)):
            raise ValueError(f"Unsafe ZIP path: {name!r}")
        mode = stat.S_IFMT(item.external_attr >> 16)
        if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise ValueError(f"Unsupported ZIP member type: {name!r}")
        key = "/".join(parts).casefold()
        if key in seen:
            raise ValueError(f"Duplicate ZIP member path: {name!r}")
        seen.add(key)
        if not item.is_dir():
            files.add(key)
        members.append((item, parts))
    for _, parts in members:
        if any("/".join(parts[:i]).casefold() in files for i in range(1, len(parts))):
            raise ValueError(f"File and directory paths collide: {'/'.join(parts)!r}")
    return members


def inspect(file, expected, extract_to):
    if extract_to is not None and file.suffix.lower() != ".zip":
        raise ValueError("Extraction requires a ZIP archive.")
    digest = sha256(file)
    if expected and digest != expected:
        raise ValueError(f"SHA-256 mismatch: expected {expected}, got {digest}")
    result = {"file": file.name, "size_bytes": file.stat().st_size, "sha256": digest}
    if expected:
        result["sha256_matches"] = True
    if file.suffix.lower() != ".zip":
        return result
    with zipfile.ZipFile(file) as archive:
        members = zip_members(archive)
        damaged = archive.testzip()
        if damaged is not None:
            raise ValueError(f"ZIP CRC failed: {damaged!r}")
        result.update(zip_valid=True, file_count=sum(not i.is_dir() for i, _ in members))
        if extract_to is not None:
            extract_to.mkdir(exist_ok=False)
            for item, parts in members:
                target = extract_to.joinpath(*parts)
                if item.is_dir():
                    target.mkdir(parents=True, exist_ok=True)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(item) as data, target.open("xb") as output:
                        shutil.copyfileobj(data, output)
            result["extracted_to"] = str(extract_to)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--expected-sha256", type=str.lower, help="SHA-256 from the approved candidate")
    parser.add_argument("--extract-to", type=Path, help="Extract a ZIP into this new directory")
    args = parser.parse_args()
    if args.expected_sha256 and not re.fullmatch(r"[a-f0-9]{64}", args.expected_sha256):
        parser.error("--expected-sha256 requires 64 hexadecimal characters")
    try:
        result = inspect(args.file, args.expected_sha256, args.extract_to)
    except (ValueError, OSError, RuntimeError, zipfile.BadZipFile) as error:
        print(f"Release check failed: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

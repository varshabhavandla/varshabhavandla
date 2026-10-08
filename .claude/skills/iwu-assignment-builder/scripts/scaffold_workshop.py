#!/usr/bin/env python3
"""Create GPT-<n>/Workshop-<k>/ folders and unzip uploaded assignment .html.zip files.

Usage: scaffold_workshop.py ROOT COURSE_NUM WORKSHOPS [--unzip ZIP ...]
  e.g. scaffold_workshop.py . 1 5 --unzip ~/uploads/a.html.zip
Zip names like "1.1 Discussion ...html.zip" land in GPT-1/Workshop-1/1.1/.
"""
import argparse, re, zipfile
from pathlib import Path

ITEM = re.compile(r"(?:^|[_\s-])(\d+)\.(\d+)\b")

def scaffold(root, course, workshops):
    made = []
    for k in range(1, workshops + 1):
        p = Path(root) / f"GPT-{course}" / f"Workshop-{k}"
        p.mkdir(parents=True, exist_ok=True)
        keep = p / ".gitkeep"
        if not any(p.iterdir()):
            keep.touch()
        made.append(p)
    return made

def target_for(zip_name, root, course):
    m = ITEM.search(zip_name)
    if not m:
        raise ValueError(f"cannot find workshop item number (like 1.1) in {zip_name!r}")
    w, i = m.groups()
    return Path(root) / f"GPT-{course}" / f"Workshop-{w}" / f"{w}.{i}"

def unzip(zip_path, root, course):
    dest = target_for(Path(zip_path).name, root, course)
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if name.startswith("/") or ".." in Path(name).parts:
                raise ValueError(f"unsafe path in zip: {name}")
        z.extractall(dest)
    gk = dest.parent / ".gitkeep"
    if gk.exists():
        gk.unlink()
    return dest

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("course", type=int); ap.add_argument("workshops", type=int)
    ap.add_argument("--unzip", nargs="*", default=[])
    a = ap.parse_args()
    scaffold(a.root, a.course, a.workshops)
    for z in a.unzip:
        print(unzip(z, a.root, a.course))

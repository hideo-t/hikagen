#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from pathlib import Path
import re

# ===== 設定 =====
IMAGES_DIR = Path(".")   # hikagen/ で実行する前提。images内で実行なら Path(".")
DRY_RUN = False                # まず True で確認 → OKなら False

# 対象拡張子
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}

# slice_02_r01_c02 を読む（slice番号は使わない）
PATTERN = re.compile(r"^slice_\d+_r(\d+)_c(\d+)$", re.IGNORECASE)


def unique_path(dest: Path) -> Path:
    """同名衝突したら _01, _02... を付けて回避"""
    if not dest.exists():
        return dest
    stem, suffix, parent = dest.stem, dest.suffix, dest.parent
    i = 1
    while True:
        cand = parent / f"{stem}_{i:02d}{suffix}"
        if not cand.exists():
            return cand
        i += 1


def rename_file(src: Path, dest: Path) -> None:
    dest = unique_path(dest)
    if DRY_RUN:
        print(f"[DRY] {src.name} -> {dest.name}")
    else:
        print(f"[REN] {src.name} -> {dest.name}")
        src.rename(dest)


def main():
    if not IMAGES_DIR.exists():
        raise FileNotFoundError(f"フォルダが見つからない: {IMAGES_DIR.resolve()}")

    files = [p for p in IMAGES_DIR.iterdir()
             if p.is_file() and p.suffix.lower() in IMAGE_EXTS]

    for p in sorted(files, key=lambda x: x.name.lower()):
        m = PATTERN.match(p.stem)
        if not m:
            # 既に s1-1.png 形式は触らない
            if re.match(r"^s\d+-\d+$", p.stem, re.IGNORECASE):
                continue
            print(f"❓ 規則外: {p.name}（変更なし）")
            continue

        scene_no = int(m.group(1))      # r01 -> 1
        image_no = int(m.group(2))      # c02 -> 2

        new_name = f"s{scene_no}-{image_no}.png"
        rename_file(p, IMAGES_DIR / new_name)

    print("✅ 完了")


if __name__ == "__main__":
    main()

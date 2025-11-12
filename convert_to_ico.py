"""Convert any image into a Windows .ico file."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from PIL import Image


def parse_sizes(raw: str) -> Sequence[int]:
    try:
        sizes = [int(part) for part in raw.split(",") if part.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Sizes must be integers separated by commas.") from exc
    if not sizes:
        raise argparse.ArgumentTypeError("Provide at least one icon size.")
    return sizes


def convert_image_to_ico(input_path: Path, output_path: Path, sizes: Sequence[int]) -> None:
    image = Image.open(input_path).convert("RGBA")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, format="ICO", sizes=[(size, size) for size in sizes])


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert an image into an .ico file.")
    parser.add_argument("input", type=Path, help="Source image (PNG/JPG/etc.)")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Destination .ico path (defaults to source name with .ico)",
    )
    parser.add_argument(
        "--sizes",
        type=parse_sizes,
        default=[256, 128, 64, 32, 16],
        help="Comma-separated icon sizes (default: 256,128,64,32,16)",
    )
    args = parser.parse_args()

    input_path: Path = args.input
    output_path: Path = args.output or input_path.with_suffix(".ico")
    convert_image_to_ico(input_path, output_path, args.sizes)
    print(f"Saved icon to {output_path}")


if __name__ == "__main__":
    main()

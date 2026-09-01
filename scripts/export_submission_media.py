#!/usr/bin/env python3
"""Export reproducible Devpost and README media from verified product states."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
STATES = ROOT / "videos" / "pyroscan-challenge-film" / "product-states"
DOCS = ROOT / "docs" / "assets"
FONTS = ROOT / "videos" / "pyroscan-challenge-film" / "assets" / "fonts"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONTS / name, size)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    ratio = max(size[0] / image.width, size[1] / image.height)
    scaled = image.resize((round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS)
    left = (scaled.width - size[0]) // 2
    top = (scaled.height - size[1]) // 2
    return scaled.crop((left, top, left + size[0], top + size[1]))


def save_jpeg(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(path, quality=92, optimize=True, progressive=True)


def thumbnail(product: Image.Image) -> Image.Image:
    width, height = 1500, 1000
    y, x = np.mgrid[0:height, 0:width]
    glow = np.exp(-(((x - 1230) / 510) ** 2 + ((y - 130) / 390) ** 2))
    fire = np.exp(-(((x - 1180) / 520) ** 2 + ((y - 930) / 270) ** 2))
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    pixels[..., 0] = np.clip(7 + glow * 11 + fire * 19, 0, 255)
    pixels[..., 1] = np.clip(10 + glow * 25 + fire * 7, 0, 255)
    pixels[..., 2] = np.clip(8 + glow * 17 + fire * 3, 0, 255)
    canvas = Image.fromarray(pixels, "RGB")

    screen = cover(product.convert("RGB"), (1040, 694))
    screen_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    screen_layer.paste(screen, (460, 145))
    shade = Image.new("L", canvas.size, 0)
    shade_draw = ImageDraw.Draw(shade)
    shade_draw.rectangle((460, 145, 1499, 839), fill=255)
    screen_layer.putalpha(shade)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), screen_layer)

    overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.rectangle((0, 0, 885, height), fill=(6, 9, 7, 224))
    for index in range(0, width, 110):
        draw.line((index, 0, index, height), fill=(190, 220, 198, 8), width=1)
    for index in range(0, height, 110):
        draw.line((0, index, width, index), fill=(190, 220, 198, 8), width=1)
    canvas = Image.alpha_composite(canvas, overlay)
    draw = ImageDraw.Draw(canvas)

    # Original PyroScan ring mark.
    draw.ellipse((72, 54, 110, 92), outline=(215, 248, 93), width=3)
    draw.ellipse((86, 58, 119, 91), outline=(109, 230, 173), width=2)
    draw.ellipse((93, 62, 112, 87), outline=(255, 112, 72), width=2)
    draw.text((132, 56), "PYROSCAN", font=font("Inter-Bold.ttf", 26), fill=(239, 243, 239))
    draw.text((132, 87), "INCIDENT TWIN", font=font("Inter-Medium.ttf", 14), fill=(125, 138, 129))

    draw.text((72, 225), "OPENAI WEBMCP CHALLENGE", font=font("Inter-SemiBold.ttf", 17), fill=(215, 248, 93))
    draw.multiline_text(
        (72, 290),
        "Wildfire readiness,\nrehearsed together.",
        font=font("Inter-Bold.ttf", 67),
        fill=(245, 247, 245),
        spacing=10,
    )
    draw.multiline_text(
        (76, 500),
        "Public terrain and historical evidence.\nA synthetic what-if. One human decision gate.",
        font=font("Inter-Regular.ttf", 23),
        fill=(180, 192, 183),
        spacing=12,
    )
    draw.line((76, 630, 540, 630), fill=(215, 248, 93), width=2)
    for left, number, label in ((76, "6", "WEBMCP TOOLS"), (230, "25 m", "PUBLIC TERRAIN"), (440, "1", "HUMAN GATE")):
        draw.text((left, 666), number, font=font("Inter-Medium.ttf", 33), fill=(239, 243, 239))
        draw.text((left, 710), label, font=font("Inter-Medium.ttf", 11), fill=(113, 125, 116))

    draw.rounded_rectangle((72, 872, 610, 936), radius=32, fill=(23, 20, 13, 235), outline=(255, 183, 92), width=1)
    draw.text((100, 893), "PUBLIC CONTEXT · SYNTHETIC WHAT-IF", font=font("Inter-SemiBold.ttf", 15), fill=(255, 198, 124))
    return canvas.convert("RGB")


def main() -> None:
    images = {path.name: Image.open(path).convert("RGB") for path in sorted(STATES.glob("0*.png"))}
    if len(images) != 6:
        raise SystemExit("Run scripts/capture_demo_states.py first; six product-state PNGs are required.")

    save_jpeg(images["01-how-it-works.png"], DOCS / "pyroscan-incident-twin.jpg")
    save_jpeg(cover(images["01-how-it-works.png"], (1800, 1012)), DOCS / "devpost-hero-16x9.jpg")
    save_jpeg(thumbnail(images["06-staged-plan.png"]), DOCS / "devpost-thumbnail-3x2.jpg")

    gallery = {
        "01-shared-rehearsal-3x2.jpg": "01-how-it-works.png",
        "02-local-knowledge-3x2.jpg": "03-human-context.png",
        "03-webmcp-comparison-3x2.jpg": "05-compare-options.png",
        "04-human-review-3x2.jpg": "06-staged-plan.png",
    }
    for output, source in gallery.items():
        save_jpeg(images[source], DOCS / "gallery" / output)

    print("Exported README, hero, thumbnail and four gallery images from verified product states.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Rebuild the bundled public-data layers used by the PyroScan map.

This script is not part of the application build. It records the exact source
products and turns them into small, deterministic browser assets.

Requires Python 3 plus Pillow and NumPy.
"""

from __future__ import annotations

import hashlib
import io
import json
import math
import urllib.request
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_PATH = ROOT / "src" / "assets" / "la-palma-hillshade.png"
MODULE_PATH = ROOT / "src" / "domain" / "publicReference.ts"

COPERNICUS_URL = (
    "https://rapidmapping.emergency.copernicus.eu/backend/EMSR671/AOI01/"
    "DEL_PRODUCT/EMSR671_AOI01_DEL_PRODUCT_v2.zip"
)
COPERNICUS_MEMBER = "EMSR671_AOI01_DEL_PRODUCT_observedEventA_v2.json"
SITCAN_URL = "https://opendata.sitcan.es/upload/136/MDT/tif/136_MDT25_LP.zip"
SITCAN_MEMBER = "136_MDT25_LP.tif"

# The SVG coastline's data-space bounding box. It was derived independently
# from OSM and gives the public layers the same geographic registration.
MAP_BOUNDS = {
    "north": 28.8575767,
    "south": 28.4527066,
    "west": -18.0072521,
    "east": -17.7242195,
    "left": 213.7,
    "right": 586.3,
    "top": 45.3,
    "bottom": 652.2,
}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "PyroScanDataBuilder/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def project(point: list[float]) -> tuple[float, float]:
    lon, lat = point
    x_ratio = (lon - MAP_BOUNDS["west"]) / (MAP_BOUNDS["east"] - MAP_BOUNDS["west"])
    y_ratio = (MAP_BOUNDS["north"] - lat) / (MAP_BOUNDS["north"] - MAP_BOUNDS["south"])
    return (
        MAP_BOUNDS["left"] + x_ratio * (MAP_BOUNDS["right"] - MAP_BOUNDS["left"]),
        MAP_BOUNDS["top"] + y_ratio * (MAP_BOUNDS["bottom"] - MAP_BOUNDS["top"]),
    )


def point_line_distance(point, start, end) -> float:
    if start == end:
        return math.dist(point, start)
    dx, dy = end[0] - start[0], end[1] - start[1]
    numerator = abs(dy * point[0] - dx * point[1] + end[0] * start[1] - end[1] * start[0])
    return numerator / math.hypot(dx, dy)


def simplify(points: list[tuple[float, float]], tolerance: float = 0.34) -> list[tuple[float, float]]:
    """Douglas-Peucker simplification in SVG pixels, preserving closed rings."""
    if len(points) <= 4:
        return points
    closed = points[0] == points[-1]
    work = points[:-1] if closed else points
    if len(work) <= 3:
        return points

    def recurse(sequence):
        furthest_index = 0
        furthest_distance = 0.0
        for index in range(1, len(sequence) - 1):
            distance = point_line_distance(sequence[index], sequence[0], sequence[-1])
            if distance > furthest_distance:
                furthest_index = index
                furthest_distance = distance
        if furthest_distance > tolerance:
            left = recurse(sequence[: furthest_index + 1])
            right = recurse(sequence[furthest_index:])
            return left[:-1] + right
        return [sequence[0], sequence[-1]]

    # A closed loop has coincident endpoints, so split it at the furthest point
    # from the first vertex before applying the open-line simplifier.
    split = max(range(1, len(work)), key=lambda index: math.dist(work[0], work[index]))
    first = recurse(work[: split + 1])
    second = recurse(work[split:] + [work[0]])
    result = first[:-1] + second
    return result + [result[0]] if closed and result[-1] != result[0] else result


def svg_path(geojson: dict) -> str:
    segments: list[str] = []
    for feature in geojson["features"]:
        for ring in feature["geometry"]["coordinates"]:
            points = simplify([project(point) for point in ring])
            head, *tail = points
            parts = [f"M{head[0]:.1f} {head[1]:.1f}"]
            parts.extend(f"L{x:.1f} {y:.1f}" for x, y in tail)
            parts.append("Z")
            segments.append(" ".join(parts))
    return " ".join(segments)


def build_hillshade(tiff: bytes) -> bytes:
    elevation = np.asarray(Image.open(io.BytesIO(tiff)), dtype=np.float64)
    valid = elevation > -1e9
    filled = np.where(valid, elevation, 0)
    gradient_y, gradient_x = np.gradient(filled, 25, 25)
    slope = np.pi / 2 - np.arctan(np.sqrt(gradient_x * gradient_x + gradient_y * gradient_y))
    aspect = np.arctan2(-gradient_x, gradient_y)
    azimuth, altitude = math.radians(315), math.radians(38)
    shade = (
        np.sin(altitude) * np.sin(slope)
        + np.cos(altitude) * np.cos(slope) * np.cos(azimuth - aspect)
    )
    shade = np.clip(((shade + 1) / 2 - 0.2) / 0.65, 0, 1) ** 0.9

    rgba = np.zeros((*elevation.shape, 4), dtype=np.uint8)
    rgba[..., 0] = (22 + shade * 172).astype(np.uint8)
    rgba[..., 1] = (29 + shade * 180).astype(np.uint8)
    rgba[..., 2] = (24 + shade * 174).astype(np.uint8)
    rgba[..., 3] = np.where(valid, 235, 0).astype(np.uint8)

    output = io.BytesIO()
    Image.fromarray(rgba, "RGBA").resize((373, 607), Image.Resampling.LANCZOS).save(
        output, format="PNG", optimize=True
    )
    return output.getvalue()


def main() -> None:
    copernicus_zip = download(COPERNICUS_URL)
    with zipfile.ZipFile(io.BytesIO(copernicus_zip)) as archive:
        geojson_bytes = archive.read(COPERNICUS_MEMBER)
    geojson = json.loads(geojson_bytes)

    sitcan_zip = download(SITCAN_URL)
    with zipfile.ZipFile(io.BytesIO(sitcan_zip)) as archive:
        tiff_bytes = archive.read(SITCAN_MEMBER)
    hillshade = build_hillshade(tiff_bytes)

    ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
    ASSET_PATH.write_bytes(hillshade)

    area_hectares = sum(feature["properties"]["area"] for feature in geojson["features"])
    module = f"""/**
 * Public reference layers derived deterministically by scripts/derive_public_reference.py.
 * They are historical/geographic context only and never drive the synthetic simulator.
 */
export const COPERNICUS_BURN_SCAR_PATH = `{svg_path(geojson)}`

export const PUBLIC_REFERENCE = {{
  historicalEvent: {{
    id: 'EMSR671',
    label: 'La Palma wildfire · July 2023',
    areaName: 'Puntagorda',
    observedAt: '2023-07-16T11:46:00.000Z',
    product: 'EMSR671_AOI01_DEL_PRODUCT v2',
    productType: 'corrected delineation',
    areaHectares: {area_hectares:.3f},
    method: 'Pleiades photo-interpretation',
    status: 'historical_reference',
    sourceLabel: 'Copernicus Emergency Management Service (© 2023 European Union), EMSR671',
    sourceUrl: 'https://mapping.emergency.copernicus.eu/activations/EMSR671/',
    downloadUrl: '{COPERNICUS_URL}',
    sourceSha256: '{sha256(copernicus_zip)}',
    geometrySha256: '{sha256(geojson_bytes)}',
  }},
  terrain: {{
    id: 'SITCAN-MDT25-LP',
    label: 'La Palma public terrain',
    resolutionMeters: 25,
    sourceUpdatedAt: '2021-02-04',
    sourceLabel: 'GRAFCAN / Gobierno de Canarias · MDT 25 m La Palma',
    sourceUrl: 'https://opendata.sitcan.es/dataset/modelo-digital-de-terreno-mdt-de-25x25-metros/resource/90d97840-9bc9-4e31-a470-3cb631806fd5',
    license: 'CC BY · attribution required',
    sourceSha256: '{sha256(sitcan_zip)}',
    hillshadeSha256: '{sha256(hillshade)}',
  }},
  boundary: {{
    id: 'OSM-relation-11775386',
    label: 'La Palma coastline',
    sourceLabel: '© OpenStreetMap contributors',
    sourceUrl: 'https://www.openstreetmap.org/copyright',
  }},
  separationRule: 'Public layers are historical/geographic context. Active ignition, wind, spread, risk and response outputs are synthetic rehearsal fixtures.',
  drivesSimulation: false,
}} as const
"""
    MODULE_PATH.write_text(module, encoding="utf-8")

    print(f"wrote {ASSET_PATH.relative_to(ROOT)} ({len(hillshade):,} bytes)")
    print(f"wrote {MODULE_PATH.relative_to(ROOT)}")
    print(f"Copernicus ZIP sha256 {sha256(copernicus_zip)}")
    print(f"SITCAN ZIP sha256    {sha256(sitcan_zip)}")


if __name__ == "__main__":
    main()

"""Generate the STL and README's matching interactive model.

Run: python3 scripts/generate_cube.py
Requires Pillow 11.3.0, shapely 2.0.7, and mapbox-earcut 1.0.3.
The GitHub mark comes from GitHub's official logo assets.
"""

import io
import math
from pathlib import Path
from urllib.request import urlopen

import mapbox_earcut
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
MARK_URL = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
FACES = [
    ((0, 0, 1), (1, 0, 0), (0, 1, 0)),
    ((1, 0, 0), (0, 0, -1), (0, 1, 0)),
    ((0, 0, -1), (-1, 0, 0), (0, 1, 0)),
    ((-1, 0, 0), (0, 0, 1), (0, 1, 0)),
    ((0, 1, 0), (1, 0, 0), (0, 0, -1)),
    ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
]


def logo_outline():
    with urlopen(MARK_URL, timeout=30) as response:
        image = Image.open(io.BytesIO(response.read())).convert("L").resize((160, 160))
    runs = []
    for y in range(image.height):
        x = 0
        while x < image.width:
            if image.getpixel((x, y)) >= 128:
                x += 1
                continue
            start = x
            while x < image.width and image.getpixel((x, y)) < 128:
                x += 1
            runs.append(box(
                (start / 160 - 0.5) * 1.65, (0.5 - (y + 1) / 160) * 1.65,
                (x / 160 - 0.5) * 1.65, (0.5 - y / 160) * 1.65,
            ))
    return unary_union(runs).simplify(0.014, preserve_topology=True)


def polygons(geometry):
    return [geometry] if isinstance(geometry, Polygon) else list(geometry.geoms)


def rings(polygon):
    return [list(ring.coords)[:-1] for ring in [polygon.exterior, *polygon.interiors]]


def triangulate(polygon, height):
    contours = rings(polygon)
    vertices = np.array([point for ring in contours for point in ring], dtype=np.float64)
    ends = np.cumsum([len(ring) for ring in contours], dtype=np.uint32)
    indices = mapbox_earcut.triangulate_float64(vertices, ends)
    for a, b, c in indices.reshape((-1, 3)):
        triangle = [(float(vertices[i][0]), float(vertices[i][1]), height) for i in (a, b, c)]
        p, q, r = triangle
        if (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0]) < 0:
            triangle.reverse()
        yield triangle


def local_mesh(mark):
    triangles = []
    for polygon in polygons(box(-1, -1, 1, 1).difference(mark)):
        triangles.extend(triangulate(polygon, 1))
    for polygon in polygons(mark):
        polygon = orient(polygon, sign=1)
        triangles.extend(triangulate(polygon, 1.08))
        for ring in rings(polygon):
            for a, b in zip(ring, ring[1:] + ring[:1]):
                low_a, low_b = (*a, 1), (*b, 1)
                high_a, high_b = (*a, 1.08), (*b, 1.08)
                triangles.extend(((low_a, low_b, high_b), (low_a, high_b, high_a)))
    return triangles


def main():
    mesh = local_mesh(logo_outline())
    lines = ["solid github_cube"]
    for normal, horizontal, vertical in FACES:
        for triangle in mesh:
            vertices = [
                tuple(round(u * horizontal[i] + v * vertical[i] + w * normal[i], 6) for i in range(3))
                for u, v, w in triangle
            ]
            a, b, c = vertices
            ab = [b[i] - a[i] for i in range(3)]
            ac = [c[i] - a[i] for i in range(3)]
            cross = (
                ab[1] * ac[2] - ab[2] * ac[1],
                ab[2] * ac[0] - ab[0] * ac[2],
                ab[0] * ac[1] - ab[1] * ac[0],
            )
            length = math.sqrt(sum(value * value for value in cross))
            if length == 0:
                raise ValueError("Degenerate triangle in cube mesh")
            lines.append("  facet normal " + " ".join(f"{value / length:.6g}" for value in cross))
            lines.append("    outer loop")
            lines.extend("      vertex " + " ".join(f"{value:.6g}" for value in vertex) for vertex in vertices)
            lines.extend(("    endloop", "  endfacet"))
    lines.append("endsolid github_cube")
    stl = "\n".join(lines) + "\n"
    output = ROOT / "assets" / "github-cube.stl"
    output.parent.mkdir(exist_ok=True)
    output.write_text(stl)
    readme = ROOT / "README.md"
    before, opening, remainder = readme.read_text().partition("```stl\n")
    _, closing, after = remainder.partition("\n```")
    if not opening or not closing:
        raise ValueError("Expected an STL code block in README.md")
    readme.write_text(before + opening + stl.rstrip() + closing + after)
    print(f"Generated {len(mesh) * len(FACES)} triangles; STL size: {len(stl):,} bytes")


if __name__ == "__main__":
    main()

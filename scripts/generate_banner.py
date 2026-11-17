"""Generate the README banner: python3 scripts/generate_banner.py.

Requires Pillow 11.3.0. All sprites and lettering are drawn here on a pixel grid.
Mona is GitHub's mascot; this is an original fan-art interpretation.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SIZE = (600, 180)
FRAMES = 36
BACKGROUND = "#101923"
MINT = "#9aefc0"
INK = "#151d29"
OUTLINE = "#52677e"
CREAM = "#ffdabd"
FUR = "#233247"

LETTERS = {
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "b": ("10000", "10000", "10110", "11001", "10001", "10001", "11110"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "h": ("10000", "10000", "10110", "11001", "10001", "10001", "10001"),
    "i": ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    "m": ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ",": ("00000", "00000", "00000", "00000", "00000", "00100", "01000"),
    " ": ("00000",) * 7,
}


def text(draw, value, position, color, scale=4):
    x, y = position
    for character in value:
        for row, pixels in enumerate(LETTERS[character]):
            for col, pixel in enumerate(pixels):
                if pixel == "1":
                    left, top = x + col * scale, y + row * scale
                    draw.rectangle((left + 2, top + 3, left + scale + 1, top + scale + 2), fill="#080e17")
        x += 6 * scale
    x, y = position
    for character in value:
        for row, pixels in enumerate(LETTERS[character]):
            for col, pixel in enumerate(pixels):
                if pixel == "1":
                    left, top = x + col * scale, y + row * scale
                    draw.rectangle((left, top, left + scale - 1, top + scale - 1), fill=color)
        x += 6 * scale


def mona(frame):
    sprite = Image.new("RGBA", (122, 120))
    draw = ImageDraw.Draw(sprite)
    phase = (frame % 36) / 36
    kick = round(8 * max(0, math.cos(math.tau * phase)) ** 6)
    # Five tentacles, including a curled tail and the raised juggling foot.
    draw.line([(35, 83), (23, 89), (12, 88), (6, 82), (6, 74), (11, 70), (17, 72)],
              fill=OUTLINE, width=9)
    draw.line([(35, 83), (23, 89), (12, 88), (6, 82), (6, 74), (11, 70), (17, 72)],
              fill=FUR, width=5)
    for points in (
        [(41, 87), (35, 99), (26, 102), (20, 100)],
        [(49, 88), (48, 105), (40, 108), (35, 106)],
        [(58, 88), (62, 103), (70, 105), (75, 102)],
        [(65, 85), (78, 98), (98, 108 - kick), (110, 110 - kick)],
    ):
        draw.line(points, fill=OUTLINE, width=10)
        draw.line(points, fill=FUR, width=6)
    draw.ellipse((34, 65, 70, 97), fill=OUTLINE)
    draw.ellipse((36, 66, 68, 95), fill=FUR)
    draw.rectangle((44, 80, 60, 94), fill="#344b60")
    for x, y in ((27, 100), (41, 105), (68, 102), (99, 108 - kick)):
        draw.rectangle((x, y, x + 3, y + 2), fill="#b4bad0")

    silhouette = [
        (18, 30), (16, 11), (19, 3), (29, 7), (38, 15),
        (62, 15), (74, 6), (83, 4), (86, 13), (83, 32),
        (90, 43), (90, 57), (84, 68), (73, 76), (59, 80),
        (39, 79), (25, 74), (16, 66), (12, 54), (13, 41),
    ]
    draw.polygon(silhouette, fill=OUTLINE)
    draw.polygon([
        (20, 30), (19, 12), (21, 7), (30, 11), (38, 19),
        (63, 19), (76, 10), (81, 8), (83, 14), (80, 33),
        (86, 44), (86, 56), (81, 65), (71, 72), (58, 76),
        (40, 75), (27, 70), (19, 63), (16, 53), (17, 42),
    ], fill=INK)
    draw.polygon([(23, 13), (32, 21), (23, 25)], fill="#805d72")
    draw.polygon([(76, 14), (69, 22), (78, 25)], fill="#805d72")
    draw.polygon([
        (28, 35), (37, 32), (47, 35), (54, 35), (65, 32),
        (75, 36), (81, 44), (81, 56), (75, 64), (64, 69),
        (40, 69), (28, 65), (22, 57), (22, 46),
    ], fill="#ce9d87")
    draw.polygon([
        (29, 36), (38, 35), (47, 38), (55, 38), (65, 35),
        (74, 38), (78, 45), (78, 55), (73, 61), (63, 65),
        (40, 65), (30, 62), (25, 56), (25, 46),
    ], fill=CREAM)
    blink = frame in (26, 27)
    for x in (34, 63):
        if blink:
            draw.rectangle((x - 3, 48, x + 6, 50), fill="#6d3547")
        else:
            draw.ellipse((x - 3, 40, x + 6, 56), fill="#8e4d59")
            draw.rectangle((x, 43, x + 4, 53), fill="#3c2738")
            draw.rectangle((x, 42, x + 2, 45), fill="#fff5e8")
    draw.polygon([(47, 54), (54, 54), (51, 57)], fill="#ac6b6d")
    draw.line([(47, 60), (50, 62), (54, 60)], fill="#9b5b62", width=1)
    draw.line([(27, 55), (16, 53)], fill="#977b83")
    draw.line([(75, 55), (87, 52)], fill="#977b83")
    return sprite


def soccer_ball(angle):
    ball = Image.new("RGBA", (31, 31))
    draw = ImageDraw.Draw(ball)
    draw.ellipse((3, 3, 27, 27), fill="#f3f5e9", outline="#74899b", width=1)
    draw.arc((4, 4, 26, 26), 5, 95, fill="#b7c8d1", width=2)
    pentagon = [
        (15 + round(5 * math.cos(-math.pi / 2 + i * math.tau / 5)),
         15 + round(5 * math.sin(-math.pi / 2 + i * math.tau / 5)))
        for i in range(5)
    ]
    for x, y in pentagon:
        dx, dy = x - 15, y - 15
        outer = (15 + round(dx * 2.4), 15 + round(dy * 2.4))
        draw.line([(x, y), outer], fill="#b0bdc4")
        draw.ellipse((outer[0] - 3, outer[1] - 3, outer[0] + 3, outer[1] + 3), fill=INK)
    draw.polygon(pentagon, fill=INK)
    mask = Image.new("L", ball.size)
    ImageDraw.Draw(mask).ellipse((3, 3, 27, 27), fill=255)
    ball.putalpha(mask)
    return ball.rotate(angle, resample=Image.Resampling.NEAREST)


def waving_hand(angle):
    hand = Image.new("RGBA", (90, 90))
    draw = ImageDraw.Draw(hand)
    points = [
        (30, 77), (30, 64), (20, 54), (14, 43), (14, 38),
        (18, 35), (22, 36), (29, 44), (29, 24), (31, 21),
        (35, 21), (38, 24), (38, 41), (40, 41), (40, 14),
        (43, 11), (47, 11), (50, 14), (50, 40), (52, 40),
        (52, 12), (55, 9), (59, 10), (61, 13), (61, 41),
        (63, 41), (63, 23), (66, 20), (70, 21), (72, 24),
        (72, 52), (69, 63), (61, 73), (60, 77),
    ]
    draw.polygon(points, fill="#ffc76d", outline="#b77e45", width=2)
    draw.line([(19, 40), (24, 46), (31, 51), (35, 57)], fill="#e1a34f", width=2)
    draw.line([(36, 48), (44, 46), (54, 47)], fill="#e1a34f", width=2)
    draw.line([(40, 61), (48, 57), (57, 57)], fill="#e1a34f", width=2)
    draw.line([(33, 72), (56, 72)], fill="#ffe1a0", width=2)
    draw.rectangle((42, 16, 44, 35), fill="#ffe1a0")
    draw.rectangle((54, 15, 56, 34), fill="#ffe1a0")
    return hand.rotate(angle, resample=Image.Resampling.NEAREST, center=(46, 67))


def background():
    image = Image.new("RGB", SIZE, BACKGROUND)
    draw = ImageDraw.Draw(image)
    for x in range(0, SIZE[0], 15):
        for y in range(0, SIZE[1], 15):
            draw.point((x, y), fill="#24313e")
    draw.rectangle((8, 8, 591, 171), outline="#304357")
    for x, y, dx, dy in ((8, 8, 1, 1), (591, 8, -1, 1), (8, 171, 1, -1), (591, 171, -1, -1)):
        draw.line([(x, y + dy * 11), (x, y), (x + dx * 11, y)], fill=MINT, width=2)
    draw.rectangle((24, 148, 166, 149), fill="#345249")
    draw.rectangle((36, 148, 62, 149), fill=MINT)
    draw.rectangle((135, 148, 153, 149), fill=MINT)
    for y in range(37, 145, 8):
        draw.rectangle((184, y, 184, y + 2), fill="#3c5664")
    draw.rectangle((207, 135, 254, 136), fill=MINT)
    draw.rectangle((258, 135, 267, 136), fill="#4a8f7a")
    for x, y in ((449, 42), (466, 135), (155, 30)):
        draw.line((x - 3, y, x + 3, y), fill="#638e91")
        draw.line((x, y - 3, x, y + 3), fill="#638e91")
    text(draw, "Hi There,", (207, 52), "#eef5fa")
    text(draw, "I'm Rob", (207, 94), MINT)
    return image


def main():
    base = background()
    frames = []
    for frame in range(FRAMES):
        image = base.copy()
        draw = ImageDraw.Draw(image)
        phase = (frame % 36) / 36
        lift = 4 * phase * (1 - phase)
        ball_x = 140 + round(4 * math.sin(math.tau * phase))
        ball_y = 123 - round(69 * lift)
        draw.ellipse((51, 140, 123, 146), fill="#080f18")
        shadow_width = round(10 - 5 * lift)
        draw.ellipse((ball_x - shadow_width, 143, ball_x + shadow_width, 146), fill="#080f18")
        sprite = mona(frame)
        image.paste(sprite, (30, 34), sprite)
        ball = soccer_ball(-frame * 10)
        image.paste(ball, (ball_x - 15, ball_y - 15), ball)
        wave = 17 * math.sin(math.tau * frame / 36)
        hand = waving_hand(wave)
        image.paste(hand, (487, 48), hand)
        draw.arc((485, 47, 517, 79), 175, 250, fill="#8baac3", width=2)
        draw.arc((478, 40, 520, 82), 180, 246, fill="#46617b", width=2)
        draw.arc((552, 47, 581, 79), 284, 355, fill="#8baac3", width=2)
        draw.arc((551, 40, 588, 82), 290, 355, fill="#46617b", width=2)
        frames.append(image.resize((1200, 360), Image.Resampling.NEAREST))

    # One shared palette keeps flat pixel-art colors stable across frames.
    palette = frames[0].quantize(colors=96, method=Image.Quantize.MEDIANCUT)
    frames = [image.quantize(palette=palette, dither=Image.Dither.NONE) for image in frames]
    output = ROOT / "assets" / "mona-soccer-banner.gif"
    output.parent.mkdir(exist_ok=True)
    frames[0].save(
        output, save_all=True, append_images=frames[1:],
        duration=60, loop=0, disposal=1, optimize=True,
    )
    print(f"Generated {output.relative_to(ROOT)} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()

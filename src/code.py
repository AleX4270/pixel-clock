import math
import time
import board
import displayio
import framebufferio
import rgbmatrix

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=32,
    bit_depth=6,
    rgb_pins=[board.GP0, board.GP1, board.GP2,
              board.GP3, board.GP4, board.GP5],
    addr_pins=[board.GP6, board.GP7, board.GP8, board.GP9],
    clock_pin=board.GP11,
    latch_pin=board.GP12,
    output_enable_pin=board.GP13,
)
display = framebufferio.FramebufferDisplay(matrix)

JASNOSC = 0.6
ODCIENIE = 4

palette = displayio.Palette(ODCIENIE + 1)
palette[0] = 0x000000
for i in range(1, ODCIENIE + 1):
    v = int(255 * (i / ODCIENIE) ** 1.6 * JASNOSC)
    palette[i] = (v << 8) | v

bitmap = displayio.Bitmap(64, 32, ODCIENIE + 1)

group = displayio.Group()
group.append(displayio.TileGrid(bitmap, pixel_shader=palette))
display.root_group = group

WIERZCHOLKI = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
]

KRAWEDZIE = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

slad = []


def linia(x0, y0, x1, y1, kolor):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    while True:
        if 0 <= x0 < 64 and 0 <= y0 < 32:
            bitmap[x0, y0] = kolor
            slad.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


print("animacja: szescian 3D")

kat_a = 0.0
kat_b = 0.0

while True:
    for x, y in slad:
        bitmap[x, y] = 0
    del slad[:]

    sa, ca = math.sin(kat_a), math.cos(kat_a)
    sb, cb = math.sin(kat_b), math.cos(kat_b)

    ekran = []
    for wx, wy, wz in WIERZCHOLKI:
        x, z = wx * ca - wz * sa, wx * sa + wz * ca
        y, z = wy * cb - z * sb, wy * sb + z * cb
        f = 18.0 / (z + 4.0)
        ekran.append((int(32 + x * f), int(16 + y * f), z))

    for a, b in KRAWEDZIE:
        x0, y0, z0 = ekran[a]
        x1, y1, z1 = ekran[b]
        glebia = (z0 + z1) * 0.5
        kolor = ODCIENIE - int((glebia + 1.8) / 3.6 * (ODCIENIE - 1) + 0.5)
        if kolor < 1:
            kolor = 1
        elif kolor > ODCIENIE:
            kolor = ODCIENIE
        linia(x0, y0, x1, y1, kolor)

    kat_a += 0.06
    kat_b += 0.025

    time.sleep(0.02)
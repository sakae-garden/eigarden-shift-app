import zlib, struct
S = 512
ACCENT = (63, 91, 74)
WHITE = (255, 255, 255)
GREY = (200, 205, 200)
img = [[ACCENT for _ in range(S)] for _ in range(S)]
def fill_rrect(x0, y0, x1, y1, r, color):
    for y in range(max(0, y0), min(S, y1)):
        for x in range(max(0, x0), min(S, x1)):
            inside = True
            if x < x0 + r and y < y0 + r:
                if (x - (x0 + r)) ** 2 + (y - (y0 + r)) ** 2 > r * r: inside = False
            elif x > x1 - r - 1 and y < y0 + r:
                if (x - (x1 - r - 1)) ** 2 + (y - (y0 + r)) ** 2 > r * r: inside = False
            elif x < x0 + r and y > y1 - r - 1:
                if (x - (x0 + r)) ** 2 + (y - (y1 - r - 1)) ** 2 > r * r: inside = False
            elif x > x1 - r - 1 and y > y1 - r - 1:
                if (x - (x1 - r - 1)) ** 2 + (y - (y1 - r - 1)) ** 2 > r * r: inside = False
            if inside: img[y][x] = color
def fill_circle(cx, cy, rad, color):
    for y in range(max(0, cy - rad), min(S, cy + rad + 1)):
        for x in range(max(0, cx - rad), min(S, cx + rad + 1)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= rad * rad: img[y][x] = color
cal_w, cal_h = 280, 270
x0 = (S - cal_w) // 2
y0 = (S - cal_h) // 2 + 12
fill_rrect(x0, y0, x0 + cal_w, y0 + cal_h, 28, WHITE)
fill_rrect(x0 + 58, y0 - 26, x0 + 88, y0 + 24, 12, WHITE)
fill_rrect(x0 + cal_w - 88, y0 - 26, x0 + cal_w - 58, y0 + 24, 12, WHITE)
gx0, gy0 = x0 + 44, y0 + 108
gap_x, gap_y = 92, 64
for row in range(3):
    for col in range(3):
        cx = gx0 + col * gap_x; cy = gy0 + row * gap_y
        if row == 1 and col == 1:
            fill_circle(cx, cy, 22, ACCENT)
        else:
            fill_circle(cx, cy, 18, GREY)
raw = bytearray()
for y in range(S):
    raw.append(0)
    for x in range(S):
        r, g, b = img[y][x]
        raw += bytes((r, g, b))
comp = zlib.compress(bytes(raw), 9)
def chunk(typ, data):
    return struct.pack('>I', len(data)) + typ + data + struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff)
png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('>IIBBBBB', S, S, 8, 2, 0, 0, 0))
png += chunk(b'IDAT', comp)
png += chunk(b'IEND', b'')
open('icon-512.png', 'wb').write(png)
print('wrote icon-512.png', len(png), 'bytes')

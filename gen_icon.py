import zlib, struct
S = 512
ACCENT = (63, 91, 74)
WHITE = (255, 255, 255)
DOTS = [
    (244, 63, 94), (245, 158, 11), (16, 185, 129),
    (14, 165, 233), (139, 92, 246), (249, 115, 22),
    (20, 184, 166), (236, 72, 153), (132, 204, 22),
]
img = [[ACCENT for _ in range(S)] for _ in range(S)]
def fill_rrect(x0, y0, x1, y1, r, color):
    for y in range(max(0, y0), min(S, y1)):
        for x in range(max(0, x0), min(S, x1)):
            inside = True
            if x < x0 + r and y < y0 + r:
                if (x-(x0+r))**2 + (y-(y0+r))**2 > r*r: inside = False
            elif x > x1 - r - 1 and y < y0 + r:
                if (x-(x1-r-1))**2 + (y-(y0+r))**2 > r*r: inside = False
            elif x < x0 + r and y > y1 - r - 1:
                if (x-(x0+r))**2 + (y-(y1-r-1))**2 > r*r: inside = False
            elif x > x1 - r - 1 and y > y1 - r - 1:
                if (x-(x1-r-1))**2 + (y-(y1-r-1))**2 > r*r: inside = False
            if inside: img[y][x] = color
def fill_circle(cx, cy, rad, color):
    for y in range(max(0, cy-rad), min(S, cy+rad+1)):
        for x in range(max(0, cx-rad), min(S, cx+rad+1)):
            if (x-cx)**2 + (y-cy)**2 <= rad*rad: img[y][x] = color
cal_w, cal_h = 296, 286
x0 = (S - cal_w) // 2
y0 = (S - cal_h) // 2 + 14
fill_rrect(x0, y0, x0 + cal_w, y0 + cal_h, 34, WHITE)
fill_rrect(x0, y0, x0 + cal_w, y0 + 56, 34, ACCENT)
fill_rrect(x0, y0 + 28, x0 + cal_w, y0 + 56, 0, ACCENT)
fill_rrect(x0 + 64, y0 - 28, x0 + 96, y0 + 22, 14, WHITE)
fill_rrect(x0 + cal_w - 96, y0 - 28, x0 + cal_w - 64, y0 + 22, 14, WHITE)
gx0, gy0 = x0 + 52, y0 + 116
gap_x, gap_y = 96, 66
i = 0
for row in range(3):
    for col in range(3):
        cx = gx0 + col * gap_x
        cy = gy0 + row * gap_y
        fill_circle(cx, cy, 23, DOTS[i % len(DOTS)])
        i += 1
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

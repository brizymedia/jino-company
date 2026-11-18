# -*- coding: utf-8 -*-
"""로고가 따로 없어서 임시 마크(출입증 모양 J)와 og 그림을 만든다. 대표 로고를 받으면 assets/img 의 logo-mark.png · favicon.png · og.png 를 바꾸면 된다."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')
os.makedirs(OUT, exist_ok=True)
FONT = r'C:\Windows\Fonts\malgunbd.ttf'
INK, ORG, SUN, PAPER = (11, 18, 38), (255, 90, 31), (255, 210, 63), (246, 243, 236)


def mark(size):
    s = size * 4
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, s - 1, s - 1), radius=int(s * .24), fill=ORG)
    d.rounded_rectangle((int(s * .39), int(s * .09), int(s * .61), int(s * .15)), radius=int(s * .03), fill=INK)   # 출입증 구멍
    f = ImageFont.truetype(FONT, int(s * .6))
    d.text((s / 2, s * .60), 'J', font=f, fill=INK, anchor='mm')
    return im.resize((size, size), Image.LANCZOS)


mark(512).save(os.path.join(OUT, 'logo-mark.png'), optimize=True)
mark(192).save(os.path.join(OUT, 'favicon.png'), optimize=True)

# og 1200x630
W, H = 1200, 630
im = Image.new('RGB', (W, H), INK)
d = ImageDraw.Draw(im)
for x in range(0, W, 56):
    d.line((x, 0, x, H), fill=(24, 32, 58))
for y in range(0, H, 56):
    d.line((0, y, W, y), fill=(24, 32, 58))
d.ellipse((700, -120, 1400, 580), fill=(60, 36, 36))
for i in range(0, W + 40, 40):   # 안전띠
    d.polygon([(i, H - 22), (i + 20, H - 22), (i + 6, H), (i - 14, H)], fill=SUN)
big = ImageFont.truetype(FONT, 118)
d.text((70, 150), '현장은', font=big, fill=(255, 255, 255))
d.rounded_rectangle((70, 290, 330, 430), radius=18, fill=ORG)
d.text((200, 360), '사람', font=big, fill=INK, anchor='mm')
d.text((350, 290), '이', font=big, fill=(255, 255, 255))
d.text((70, 440), '만듭니다', font=big, fill=(255, 255, 255))
sm = ImageFont.truetype(FONT, 34)
d.text((72, 80), 'JINO CP.  ·  행사전문 인력에이전시', font=sm, fill=SUN)
d.text((72, 570), '지노컴퍼니  010-6755-5021', font=sm, fill=(210, 216, 232))
m = mark(150)
im.paste(m, (W - 230, 70), m)
im.save(os.path.join(OUT, 'og.png'), optimize=True)
print('brand ok')

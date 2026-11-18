# -*- coding: utf-8 -*-
"""
지노컴퍼니가 보낸 행사 사진 묶음(_raw/<행사 폴더>/*.jpg)에서 고른 컷을 assets/img/p/<코드>.webp 로 줄여 넣는다.

  python tools/import_photos.py

_raw/ 는 Desktop 큰길브리지 지노컴퍼니 폴더의 zip 22개를 푼 것(레포에 올리지 않는다).
고른 컷은 PICKS 에 (폴더 번호, 파일 번호) 로 적는다. 폴더 번호는 이름 정렬 순서, 파일 번호는 폴더 안 정렬 순서.
"""
import os
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, '_raw')
OUT = os.path.join(ROOT, 'assets', 'img', 'p')
os.makedirs(OUT, exist_ok=True)

DIRS = sorted(os.listdir(RAW))   # 00 체육대회 · 01 앨범 행사 · 02 강북 마켓 · … · 21 판타지아 대구페스타

PICKS = {
    'sports1': (0, 0), 'sports2': (0, 2), 'sports3': (0, 5),
    'album1': (1, 0), 'album2': (1, 3),
    'xmas1': (2, 1), 'xmas2': (2, 2), 'xmas3': (2, 6), 'xmas4': (2, 7),
    'sec1': (3, 1), 'sec2': (3, 5), 'sec3': (3, 7),
    'lav3': (4, 24), 'lav4': (4, 16),
    
    'nyj1': (5, 0), 'nyj2': (5, 2), 'nyj3': (5, 6),
    'hug1': (6, 0), 'hug2': (6, 2), 'hug3': (6, 5),
    'ddp1': (7, 1), 'ddp2': (7, 4), 'ddp3': (7, 6),
    'run1': (8, 6), 'run2': (8, 9), 'run3': (8, 12), 'run4': (8, 16), 'run5': (8, 20),
    'poke1': (9, 0), 'poke2': (9, 2), 'poke3': (9, 5),
    'agm1': (10, 4), 'agm2': (10, 7), 'agm3': (10, 10), 'agm4': (10, 11),
    'sk1': (11, 0), 'sk2': (11, 2), 'sk3': (11, 6), 'sk4': (11, 10),
    'snow1': (12, 0), 'snow2': (12, 3), 'snow3': (12, 6), 'snow4': (12, 9),
    'sf1': (13, 1), 'sf2': (13, 3), 'sf3': (13, 6),
    'scrub1': (14, 0), 'scrub2': (14, 2), 'scrub3': (14, 6),
    'a60a': (15, 0), 'a60b': (15, 3), 'a60c': (15, 5), 'a60d': (15, 8), 'a60e': (15, 11),
    'amhq1': (16, 2), 'amhq2': (16, 7), 'amhq3': (16, 9), 'amhq4': (16, 13),
    'bday1': (17, 0), 'bday2': (17, 2), 'bday3': (17, 8), 'bday4': (17, 12),
    'war1': (18, 0), 'war2': (18, 2),
    'jin1': (19, 0), 'jin2': (19, 1), 'jin3': (19, 5),
    'crun1': (20, 1), 'crun2': (20, 3), 'crun3': (20, 6),
    'fan1': (21, 1), 'fan2': (21, 6), 'fan3': (21, 8), 'fan4': (21, 10),
}
BIG = {'run2', 'poke2', 'xmas2', 'run1'}   # 대문 · 큰 칸에 쓰는 컷은 조금 크게


def main():
    n = 0
    for code, (di, fi) in PICKS.items():
        d = os.path.join(RAW, DIRS[di])
        fs = sorted(f for f in os.listdir(d) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
        src = os.path.join(d, fs[fi])
        im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        m = 1800 if code in BIG else 1280
        im.thumbnail((m, m), Image.LANCZOS)
        dst = os.path.join(OUT, code + '.webp')
        im.save(dst, 'WEBP', quality=74, method=6)
        n += 1
        print(f'{code:8s} {di:02d}/{fi:03d} {im.size} {os.path.getsize(dst)//1024}KB')
    print(n, 'photos')


if __name__ == '__main__':
    main()

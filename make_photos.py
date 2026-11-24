# photos/ 안의 1, 2, 3 … 번호 사진(jpg·jpeg·png·webp)을 팝업에 맞게 줄여서 photos/web/ 에 저장
import os, re, sys, glob
from PIL import Image, ImageOps
SRC, OUT, MAXW, Q = 'photos', 'photos/web', 900, 80
MAX_BYTES = 15 * 1024 * 1024        # 올릴 수 있는 원본 최대 크기 15MB (넘으면 건너뜀)
Image.MAX_IMAGE_PIXELS = 60_000_000  # 비정상적으로 큰 그림 차단
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(OUT + '/*'): os.remove(f)
found = {}
for f in os.listdir(SRC):
    m = re.fullmatch(r'(\d+)\.(jpe?g|png|webp)', f, re.I)
    if m and os.path.getsize(os.path.join(SRC, f)) <= MAX_BYTES and int(m.group(1)) <= 30: found[int(m.group(1))] = os.path.join(SRC, f)   # 번호는 1~30까지
for n, p in sorted(found.items()):
    try: im = ImageOps.exif_transpose(Image.open(p)).convert('RGB')   # 진짜 그림 파일인지 열어서 확인 (이름만 .jpg 인 가짜 파일 차단)
    except Exception as e: print('건너뜀', p, e); continue
    if im.width > MAXW: im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)   # 크면 줄이기만 하고 키우지는 않음
    q = Q
    while True:
        im.save(f'{OUT}/{n}.jpg', 'JPEG', quality=q, optimize=True, progressive=True)
        if os.path.getsize(f'{OUT}/{n}.jpg') <= 100_000 or q <= 50: break
        q -= 5
    print(n, p, '->', os.path.getsize(f'{OUT}/{n}.jpg') // 1024, 'KB')
if not found: sys.exit('photos/ 에 1.jpg 같은 번호 사진이 없습니다')

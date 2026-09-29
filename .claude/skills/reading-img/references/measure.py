"""시안 실측 도구 — reading-img.md 와 함께 쓴다.

표준 라이브러리만 쓴다(이미지 라이브러리 불필요). 스크래치패드에 복사해 두고
`from measure import *` 로 불러 쓴다. 호출 3~5줄로 끝나야 하고,
매번 이 안의 로직을 다시 타이핑하지 않는다.

출력은 결론만 찍는다. 원시 스캔 결과를 통째로 print 하지 않는다.
"""

import zlib, struct, statistics

__all__ = ['Img', 'save', 'crop', 'near', 'notnear', 'ink_box', 'col_runs',
           'row_bands', 'sub_edge', 'density', 'alpha_bbox', 'place', 'diff_count',
           'ClippedBox', 'TOL', 'survey', 'edges', 'radius_fit', 'font_probe', 'shot',
           'evaljs', 'audit',
           'diff_png']


# ── PNG 디코딩 ────────────────────────────────────────────────────────────
class Img:
    """PNG 를 RGBA 로 디코딩. 8bit, non-interlaced 만 지원."""

    def __init__(self, path):
        data = open(path, 'rb').read()
        assert data[:8] == b'\x89PNG\r\n\x1a\n', path
        pos, idat, plte, trns = 8, b'', None, None
        while pos < len(data):
            ln, = struct.unpack('>I', data[pos:pos + 4])
            typ, chunk = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + ln]
            if typ == b'IHDR':
                w, h, bitd, ct, _, _, inter = struct.unpack('>IIBBBBB', chunk)
                assert bitd == 8 and inter == 0, '8bit non-interlaced 만 지원'
            elif typ == b'IDAT': idat += chunk
            elif typ == b'PLTE': plte = chunk
            elif typ == b'tRNS': trns = chunk
            pos += 12 + ln
        raw = zlib.decompress(idat)
        nch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[ct]
        stride = w * nch
        out, prev, p = bytearray(h * stride), bytearray(stride), 0
        for y in range(h):
            f = raw[p]; p += 1
            line = bytearray(raw[p:p + stride]); p += stride
            if f == 1:
                for i in range(nch, stride): line[i] = (line[i] + line[i - nch]) & 255
            elif f == 2:
                for i in range(stride): line[i] = (line[i] + prev[i]) & 255
            elif f == 3:
                for i in range(stride):
                    a = line[i - nch] if i >= nch else 0
                    line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
            elif f == 4:
                for i in range(stride):
                    a = line[i - nch] if i >= nch else 0
                    b = prev[i]; c = prev[i - nch] if i >= nch else 0
                    pp = a + b - c
                    pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                    pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                    line[i] = (line[i] + pr) & 255
            out[y * stride:(y + 1) * stride] = line
            prev = line
        px = bytearray(w * h * 4)
        for i in range(w * h):
            if ct == 6: px[i * 4:i * 4 + 4] = out[i * 4:i * 4 + 4]
            elif ct == 2: px[i * 4:i * 4 + 3] = out[i * 3:i * 3 + 3]; px[i * 4 + 3] = 255
            elif ct == 0: g = out[i]; px[i * 4:i * 4 + 4] = bytes((g, g, g, 255))
            elif ct == 4: g = out[i * 2]; px[i * 4:i * 4 + 4] = bytes((g, g, g, out[i * 2 + 1]))
            elif ct == 3:
                j = out[i]
                px[i * 4:i * 4 + 3] = plte[j * 3:j * 3 + 3]
                px[i * 4 + 3] = trns[j] if (trns and j < len(trns)) else 255
        self.w, self.h, self.px = w, h, px

    def get(self, x, y):
        i = (y * self.w + x) * 4
        return tuple(self.px[i:i + 4])

    def a(self, x, y):
        return self.px[(y * self.w + x) * 4 + 3]

    def hex(self, x, y):
        r, g, b, al = self.get(x, y)
        return '#%02x%02x%02x' % (r, g, b) + ('' if al == 255 else '/a%d' % al)


def save(path, w, h, px):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += px[y * w * 4:(y + 1) * w * 4]
    def ck(t, d):
        return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
    open(path, 'wb').write(
        b'\x89PNG\r\n\x1a\n'
        + ck(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
        + ck(b'IDAT', zlib.compress(bytes(raw), 6)) + ck(b'IEND', b''))


def crop(im, x0, y0, x1, y1, scale=1, path='crop.png'):
    """확대는 형태 판독이 필요할 때만. 2배를 넘기지 않는다."""
    w, h = (x1 - x0) * scale, (y1 - y0) * scale
    px = bytearray(w * h * 4)
    for y in range(h):
        sy = y0 + y // scale
        for x in range(w):
            i, o = ((sy * im.w) + x0 + x // scale) * 4, (y * w + x) * 4
            px[o:o + 4] = im.px[i:i + 4]
    save(path, w, h, px)
    return path


# ── 색 판정자 ─────────────────────────────────────────────────────────────
def near(ref, tol=10):
    """ref 색과 같으면 True 인 판정자를 만든다."""
    return lambda c: max(abs(c[i] - ref[i]) for i in range(3)) <= tol

def notnear(ref, tol=10):
    """ref(배경)와 다르면 True. 잉크 판정에 쓴다."""
    return lambda c: max(abs(c[i] - ref[i]) for i in range(3)) > tol


# ── 측정 ─────────────────────────────────────────────────────────────────
class ClippedBox(Exception):
    """잉크가 탐색 창에 닿았다 = 잘린 값. 폰트·크기 판정에 쓰면 결론이 통째로 틀어진다."""


def ink_box(im, x0, y0, x1, y1, test, allow=''):
    """(l, t, r, b). 창에 닿으면 ClippedBox 를 던진다 — 창을 넓혀 다시 잰다.

    allow: 일부러 자른 변만 'ltrb' 문자로 허용(예: 긴 문자열의 좌우를 잘라 세로만 잴 때 allow='lr').
    세로(t/b)를 allow 로 여는 것은 크기·굵기 판정을 망가뜨리므로 하지 말 것."""
    xs = [x for y in range(y0, y1) for x in range(x0, x1) if test(im.get(x, y))]
    ys = [y for y in range(y0, y1) for x in range(x0, x1) if test(im.get(x, y))]
    if not xs:
        return None
    box = (min(xs), min(ys), max(xs), max(ys))
    hit = [n for n, c in (('l', box[0] == x0), ('t', box[1] == y0),
                          ('r', box[2] == x1 - 1), ('b', box[3] == y1 - 1))
           if c and n not in allow]
    if hit:
        raise ClippedBox(
            '창(%d,%d,%d,%d)의 %s 변에 잉크가 닿음 → %s 는 잘린 값이다. '
            '해당 변을 20px 이상 넓혀 다시 재라(의도적으로 자른 변이면 allow=%r).'
            % (x0, y0, x1, y1, '/'.join(hit), box, ''.join(hit)))
    return box


def col_runs(im, y0, y1, x0, x1, test, gap=1):
    """세로 구간 안에서 잉크가 있는 x 구간들. 글자 단위 advance 측정용."""
    out, cur, blank = [], None, 0
    for x in range(x0, x1):
        on = any(test(im.get(x, y)) for y in range(y0, y1))
        if on:
            if cur is None: cur = x
            blank = 0
        elif cur is not None:
            blank += 1
            if blank >= gap:
                out.append((cur, x - blank)); cur = None
    if cur is not None: out.append((cur, x1 - 1))
    return out


def row_bands(im, x0, x1, y0, y1, test):
    """가로 구간 안에서 잉크가 있는 y 구간들. 행(줄) 위치 측정용."""
    out, cur = [], None
    for y in range(y0, y1):
        on = any(test(im.get(x, y)) for x in range(x0, x1))
        if on and cur is None: cur = y
        if not on and cur is not None: out.append((cur, y - 1)); cur = None
    if cur is not None: out.append((cur, y1 - 1))
    return out


def sub_edge(im, fixed, start, fill, bg, horiz=True, step=1, limit=140):
    """서브픽셀 경계(알파 50% 교차점). 색 임계값으로 잡으면 크기가 작게 나온다.

    horiz=True 면 y=fixed 행에서 x=start 부터 step 방향으로 훑는다."""
    ch = max(range(3), key=lambda i: abs(fill[i] - bg[i]))
    prev = None
    for k in range(limit):
        p = start + step * k
        c = im.get(p, fixed) if horiz else im.get(fixed, p)
        a = (c[ch] - bg[ch]) / (fill[ch] - bg[ch])
        if prev is not None and prev[1] < 0.5 <= a:
            return prev[0] + step * (0.5 - prev[1]) / (a - prev[1]) + step * 0.5
        prev = (p, a)
    return None


def density(im, box, fg, bg):
    """잉크 밀도(박스 안 평균 alpha). 굵기 판정용.
    후보는 반드시 시안과 같은 배경색 위에 렌더해서 같은 값을 구해 비교한다."""
    l, t, r, b = box
    ch = max(range(3), key=lambda i: abs(fg[i] - bg[i]))
    tot = n = 0
    for y in range(t, b + 1):
        for x in range(l, r + 1):
            a = (im.get(x, y)[ch] - bg[ch]) / (fg[ch] - bg[ch])
            tot += max(0.0, min(1.0, a)); n += 1
    return round(tot / n, 4)


def alpha_bbox(path, thr=10):
    """에셋의 잉크 bbox 와 캔버스 크기. CSS 크기는 '캔버스 × 배율' 이다."""
    s = Img(path)
    xs = [x for y in range(s.h) for x in range(s.w) if s.a(x, y) > thr]
    ys = [y for y in range(s.h) for x in range(s.w) if s.a(x, y) > thr]
    return {'canvas': (s.w, s.h), 'ink': (min(xs), min(ys), max(xs), max(ys)),
            'pad': (min(ys), s.h - 1 - max(ys), min(xs), s.w - 1 - max(xs))}  # 상하좌우


def place(design, src_path, scale, win, band, bg, thr=60):
    """가려진 이미지의 (left, top). 여백은 대조하지 않고 소스에서 읽어 뺀다.

    win  = (x0, x1)  그 에셋만 있는 x 범위. 다른 요소가 들어오면 오염된다.
    band = (y0, y1)  잉크가 노출되고 배경이 균일한 y 범위.
                     **y0 은 반드시 실제 잉크 상단보다 위여야 한다**(아니면 top 이 그만큼 틀어진다).
    반환 dict 의 spread 가 3px 이하면 left 를 그대로 채택,
    크면 top 고정 후 left 만 1D 탐색으로 다시 잡는다."""
    s = Img(src_path)
    x0, x1 = win; y0, y1 = band
    nz = notnear(bg)
    s_top = min(y for y in range(s.h) for x in range(s.w) if s.a(x, y) > thr)
    d_top = min(y for y in range(y0, y1) for x in range(x0, x1) if nz(design.get(x, y)))
    if d_top == y0:
        print('  !! band 상단에 닿음 — 실제 잉크 상단이 더 위일 수 있다. band 를 넓혀 다시.')
    top = d_top - s_top * scale
    v = []
    for dy in range(y0, y1, 3):
        sy = int(round((dy - top) / scale))
        if not 0 <= sy < s.h: continue
        sr = [x for x in range(s.w) if s.a(x, sy) > thr]
        dr = [x for x in range(x0, x1) if nz(design.get(x, dy))]
        if sr and dr: v.append(dr[0] - sr[0] * scale)
    if not v:
        return {'left': None, 'top': round(top + 0.5), 'size': (s.w * scale, s.h * scale),
                'spread': None, 'note': 'left 표본 없음 — win/band 를 다시 잡을 것'}
    return {'left': round(statistics.median(v) + 0.5), 'top': round(top + 0.5),
            'size': (s.w * scale, s.h * scale), 'spread': round(max(v) - min(v), 1)}


def diff_count(a_path, b_path, tol=40):
    """두 PNG 의 차이 픽셀 수. 구현 검증은 이미지를 눈으로 보는 대신 이 수치로 반복한다."""
    a, b = Img(a_path), Img(b_path)
    n = 0
    for i in range(0, min(len(a.px), len(b.px)), 4):
        if max(abs(a.px[i + k] - b.px[i + k]) for k in range(3)) > tol: n += 1
    return n


# ── 종료 조건 ─────────────────────────────────────────────────────────────
# 이 오차 안이면 더 재지 말고 넘어간다. 여기서 멈추는 게 규칙이다.
TOL = {
    'text': 1,        # 본문·제목 잉크 좌표
    'component': 1,   # 버튼·카드·배너 박스
    'asset': 2,       # 이미지 배치
    'radius': 2,      # 모서리 반경
    'deco': 10,       # 배경 곡선·워터마크 등 장식
}


# ── 1패스 덤프 ────────────────────────────────────────────────────────────
def survey(im, specs, ref=None):
    """섹션 전체를 한 번에 재서 한 줄씩 찍는다. 왕복을 항목 수만큼 늘리지 말 것.

    specs = [(name, (x0, y0, x1, y1), test, allow?), ...]
    ref   = 구현 화면 Img. 주면 design/impl 을 나란히 찍고 델타까지 낸다.
    잘린 항목이 하나라도 있으면 전부 출력한 뒤 ClippedBox 로 실패한다."""
    bad = []
    for spec in specs:
        name, box, test = spec[0], spec[1], spec[2]
        allow = spec[3] if len(spec) > 3 else ''
        try:
            a = ink_box(im, *box, test, allow=allow)
        except ClippedBox as e:
            bad.append((name, str(e))); print('%-14s !! 잘림' % name); continue
        if a is None:
            print('%-14s (없음)' % name); continue
        line = '%-14s %s w%-4d h%-3d' % (name, a, a[2] - a[0] + 1, a[3] - a[1] + 1)
        if ref is not None:
            try:
                b = ink_box(ref, *box, test, allow=allow)
            except ClippedBox:
                b = None
            line += '  impl %s  d %s' % (
                b, tuple(b[k] - a[k] for k in range(4)) if b else None)
        print(line)
    if bad:
        print('\n!! 다시 잴 항목 %d개 — 창을 넓혀 재측정할 것' % len(bad))
        for n, m in bad:
            print('   -', n, ':', m)
        raise ClippedBox('%d개 항목이 잘렸다. 이 값들로 판정하지 말 것.' % len(bad))


def edges(im, boxes, n=6, tol=12):
    """면의 네 변을 스캔해 테두리 유무·색·굵기를 판정한다. **채움색만 보고 넘어가지 말 것.**

    boxes = [(name, (x0, y0, x1, y1)), ...]  — 잉크박스(테두리 포함 바깥 경계)
    안티에일리어싱(배경↔채움 사이 보간색)과 실제 테두리색을 자동으로 가른다."""
    res = {}
    for name, (x0, y0, x1, y1) in boxes:
        cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
        scans = {
            '좌': [im.get(x, cy) for x in range(x0 - n, x0 + n)],
            '우': [im.get(x, cy) for x in range(x1 + n, x1 - n, -1)],
            '상': [im.get(cx, y) for y in range(y0 - n, y0 + n)],
            '하': [im.get(cx, y) for y in range(y1 + n, y1 - n, -1)],
        }
        found = {}
        for side, sc in scans.items():
            bg, fill = sc[0], sc[-1]
            band = []
            for c in sc[1:-1]:
                if max(abs(c[k] - bg[k]) for k in range(3)) <= tol: continue
                if max(abs(c[k] - fill[k]) for k in range(3)) <= tol: break
                # 배경↔채움 보간선에서 얼마나 벗어나는가 = 진짜 테두리색인가
                num = den = 0
                for k in range(3):
                    d = fill[k] - bg[k]
                    if abs(d) > 8: num += (c[k] - bg[k]) / d; den += 1
                # 안티에일리어싱이면 배경↔채움 사이의 '혼합'이므로 t 는 0~1 안에 있다.
                # 밖으로 나가면(외삽) 그 색은 혼합이 아니라 별도의 테두리색이다.
                t = min(1.0, max(0.0, num / den if den else 0.0))
                resid = max(abs(c[k] - (bg[k] + t * (fill[k] - bg[k]))) for k in range(3))
                band.append((c, resid))
            real = [c for c, r in band if r > tol]
            if real or len(band) >= 2:
                px = real or [c for c, _ in band]
                found[side] = ('#%02x%02x%02x' % px[len(px) // 2][:3], len(px))
        if found:
            print('%-12s 테두리 있음  %s' % (name, {k: '%s %dpx' % v for k, v in found.items()}))
            if len(found) < 4:
                print('%-12s   !! %s 변에만 있음 — 한쪽 테두리 디자인인지 확인'
                      % ('', '/'.join(found)))
        else:
            print('%-12s 테두리 없음' % name)
        res[name] = found
    return res


def radius_fit(im, x_edge, y_flat, inside, outside, side='bl', span=280, skip=4, step=3):
    """평탄한 변에서 이어지는 모서리 반경을 서브픽셀 경계로 피팅한다.

    x_edge : 도형의 바깥 경계 x (좌측 모서리면 왼쪽 끝, 우측이면 오른쪽 끝)
    y_flat : 평탄부의 바깥 경계 y
    side   : 'bl' | 'br' | 'tl' | 'tr'
    **모서리 끝 skip px 는 버린다** — 그 지점은 곡선이 수직 접선이라 한 열의 커버리지가
    여러 행에 퍼져 50% 교차점이 의미를 잃는다. 그 한 점을 반경 기준으로 삼으면
    원이 타원으로 둔갑한다(실제로 R=203 원이 rx220/ry184 타원으로 오판된 사례가 있다).
    **원(단일값)부터 본다.** RMSE ≤ 2px 면 채택하고 `/` 타원 문법은 쓰지 않는다."""
    import math
    down = side[0] == 'b'
    right = side[1] == 'r'
    pts = []
    for k in range(skip, span, step):
        x = x_edge - k if right else x_edge + k
        y0 = y_flat - span - 20 if down else y_flat + span + 20
        e = sub_edge(im, x, y0, outside, inside, horiz=False,
                     step=1 if down else -1, limit=span + 60)
        if e is not None:
            pts.append((k, abs(e - y_flat)))
    if len(pts) < 5:
        return {'error': '표본 부족 — span/색 지정을 확인할 것', 'n': len(pts)}

    def err_circle(R):
        s = 0.0
        for k, d in pts:
            m = R - math.sqrt(max(0.0, R * R - (R - k) ** 2)) if k < R else 0.0
            s += (m - d) ** 2
        return math.sqrt(s / len(pts))

    def err_ell(rx, ry):
        s = 0.0
        for k, d in pts:
            m = ry - ry * math.sqrt(max(0.0, 1 - ((rx - k) / rx) ** 2)) if k < rx else 0.0
            s += (m - d) ** 2
        return math.sqrt(s / len(pts))

    R = min((round(r * 0.5, 1) for r in range(20, span * 2)), key=err_circle)
    eR = err_circle(R)
    best = (eR * 2, R, R)
    for rx in range(int(R * 0.6), int(R * 1.7), 2):
        for ry in range(int(R * 0.6), int(R * 1.7), 2):
            e = err_ell(rx, ry)
            if e < best[0]:
                best = (e, rx, ry)
    out = {'R': R, 'rmse': round(eR, 2), 'n': len(pts),
           'ellipse': (best[1], best[2]), 'ellipse_rmse': round(best[0], 2)}
    snap = round(R)
    if eR <= 2:
        out['css'] = '원 %dpx — border-radius 단일값으로 쓸 것' % snap
    elif best[0] < eR * 0.7:
        out['css'] = '타원 %d/%dpx — 원(RMSE %.2f)보다 뚜렷이 낫다' % (best[1], best[2], eR)
    else:
        out['css'] = '원 %dpx (RMSE %.2f) — 표본/색 지정을 다시 볼 것' % (snap, eR)
    return out


# ── 브라우저 ──────────────────────────────────────────────────────────────
def chrome_bin():
    import os, shutil
    cand = [os.environ.get('CHROME'),
            '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            shutil.which('google-chrome'), shutil.which('chromium')]
    for c in cand:
        if c and os.path.exists(c):
            return c
    raise RuntimeError('Chrome 을 찾지 못했다. CHROME 환경변수로 경로를 지정할 것.')


def _run(args):
    import subprocess
    return subprocess.run([chrome_bin(), '--headless', '--disable-gpu',
                           '--hide-scrollbars', '--force-device-scale-factor=1',
                           '--allow-file-access-from-files',
                           '--virtual-time-budget=6000'] + args,
                          capture_output=True, text=True).stdout


def shot(path, w, h, out='shot.png'):
    """1x 스크린샷. h 는 전체 페이지가 담길 만큼 크게 준다(뷰포트만 찍힌다).
    headless 창 폭 하한은 500px — 그보다 좁은 폭은 evaljs/audit 의 iframe 경로를 쓴다."""
    import os
    _run(['--window-size=%d,%d' % (w, h), '--screenshot=' + out,
          'file://' + os.path.abspath(path)])
    return out


def evaljs(path, js, w=1920, h=1200):
    """페이지에 js 를 주입해 실행하고 반환 문자열을 받는다(왕복 1회).
    js 는 마지막 표현식이 결과가 되는 본문. 원본 파일은 건드리지 않는다."""
    import os, re, html, tempfile
    src = open(path, encoding='utf-8').read()
    tag = ('<script>window.addEventListener("load",()=>{setTimeout(()=>{'
           'let r;try{r=(function(){%s})()}catch(e){r="ERR "+e}'
           'const p=document.createElement("pre");p.id="__probe";'
           'p.textContent=String(r);document.body.appendChild(p)},400)})</script>' % js)
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(suffix='.html', dir=d)
    os.close(fd)
    try:
        open(tmp, 'w', encoding='utf-8').write(src.replace('</body>', tag + '</body>'))
        dom = _run(['--window-size=%d,%d' % (w, h), '--dump-dom', 'file://' + tmp])
        m = re.search(r'<pre id="__probe">(.*?)</pre>', dom, re.S)
        return html.unescape(m.group(1)) if m else 'FAIL(주입 결과 없음)'
    finally:
        os.remove(tmp)


def audit(path, widths=(360, 768, 1200, 1400, 1920), skip=()):
    """분기별 넘침·찌그러짐을 한 번에 점검한다(reading-img.md §8-2). 360 같은 좁은 폭은 iframe 뷰포트로 본다.
    skip: 의도적으로 화면 밖에 두는 장식 요소의 class 목록."""
    import os, re, html, tempfile
    sk = '[' + ','.join('"%s"' % c for c in skip) + ']'
    body = '''
      const SK=%s, o=[];
      const W=innerWidth, D=document;
      o.push("W"+W+" scrollW"+D.documentElement.scrollWidth+" H"+D.body.scrollHeight);
      D.querySelectorAll("body *").forEach(e=>{const r=e.getBoundingClientRect();
        if(!r.width&&!r.height) return;
        if(SK.some(c=>e.classList&&e.classList.contains(c))) return;
        if(r.right>W+0.5||r.left<-0.5) o.push("넘침 "+(e.className||e.tagName)+" "+r.left.toFixed(0)+"~"+r.right.toFixed(0));});
      D.querySelectorAll("img").forEach(e=>{const r=e.getBoundingClientRect();
        if(!r.width||!e.naturalWidth) return;
        const n=e.naturalWidth/e.naturalHeight, c=r.width/r.height;
        if(Math.abs(n-c)/n>0.02) o.push("비율 "+e.className+" "+r.width.toFixed(0)+"x"+r.height.toFixed(0));});
      return o.join(" | ");''' % sk
    out = []
    for w in widths:
        if w >= 500:
            out.append('%5d %s' % (w, evaljs(path, body, w, 900)))
        else:  # headless 창 폭 하한(500) 회피 — iframe 이 곧 뷰포트가 된다
            d = os.path.dirname(os.path.abspath(path))
            fd, tmp = tempfile.mkstemp(suffix='.html', dir=d); os.close(fd)
            try:
                open(tmp, 'w', encoding='utf-8').write(
                    '<!DOCTYPE html><meta charset="utf-8"><body style="margin:0">'
                    '<iframe id=f src="%s" width=%d height=3000 style="border:0"></iframe>'
                    '<pre id="__probe"></pre><script>'
                    'document.getElementById("f").addEventListener("load",()=>{setTimeout(()=>{'
                    'const w=document.getElementById("f").contentWindow;'
                    'document.getElementById("__probe").textContent='
                    '(function(){const innerWidth=w.innerWidth,document=w.document;%s})()'
                    '},600)})</script>' % (os.path.basename(path), w, body))
                dom = _run(['--window-size=%d,900' % (w + 40), '--dump-dom', 'file://' + tmp])
                m = re.search(r'<pre id="__probe">(.*?)</pre>', dom, re.S)
                out.append('%5d %s' % (w, html.unescape(m.group(1)) if m else 'FAIL'))
            finally:
                os.remove(tmp)
    print('\n'.join(out))
    return out


def diff_png(a_path, b_path, out='diff.png', tol=40, size=None):
    """시안 위에 구현을 겹친 차이 맵을 그리고 차이 픽셀 수를 돌려준다.
    면·모서리·이미지가 밝게 남으면 실제 오류. 텍스트 윤곽은 정상."""
    a, b = Img(a_path), Img(b_path)
    w, h = size or (min(a.w, b.w), min(a.h, b.h))
    px, n = bytearray(w * h * 4), 0
    for y in range(h):
        for x in range(w):
            o = (y * w + x) * 4
            if max(abs(a.get(x, y)[k] - b.get(x, y)[k]) for k in range(3)) > tol:
                px[o] = 255; px[o + 2] = 60; n += 1
            px[o + 3] = 255
    save(out, w, h, px)
    return n


# ── 폰트 확정(종류·크기·굵기·자간을 한 번에) ────────────────────────────
_WEIGHT = {'thin': 100, 'extralight': 200, 'ultralight': 200, 'light': 300,
           'regular': 400, 'normal': 400, 'medium': 500, 'semibold': 600,
           'demibold': 600, 'bold': 700, 'extrabold': 800, 'ultrabold': 800,
           'heavy': 800, 'black': 900}


def font_faces(font_dir):
    """폰트 폴더를 훑어 {family: {weight: path}} 를 만든다. 파일명에서 굵기를 읽는다."""
    import os, re
    fam = {}
    for f in sorted(os.listdir(font_dir)):
        if not f.endswith('.woff2'):
            continue
        stem = f[:-6]
        m = re.match(r'^([A-Za-z]+?)[-_]?(%s)$' % '|'.join(_WEIGHT), stem, re.I)
        if not m:
            continue
        fam.setdefault(m.group(1), {})[_WEIGHT[m.group(2).lower()]] = \
            os.path.abspath(os.path.join(font_dir, f))
    return fam


def _amap(img, box, fg, bg):
    x0, y0, x1, y1 = box
    out = []
    for y in range(y0, y1 + 1):
        row = []
        for x in range(x0, x1 + 1):
            c = img.get(x, y); num = den = 0
            for k in range(3):
                d = fg[k] - bg[k]
                if abs(d) > 40:
                    num += (c[k] - bg[k]) / d; den += 1
            row.append(max(0.0, min(1.0, num / den if den else 0.0)))
        out.append(row)
    return out


def font_probe(design, box, text, fg, bg, cands, font_dir, out='probe.png',
               smoothing=True):
    """후보를 시안과 같은 배경 위에 1x 로 렌더해 폭·높이·밀도·실루엣을 한 번에 대조한다.

    box   = 시안의 잉크박스(ink_box 로 잘림 없이 잰 값)
    cands = [(family, weight, size_px, ls_em), ...]
    차이(실루엣 평균 알파 오차)가 가장 작은 후보가 답이다.
    **굵기 판정은 한 어절짜리 짧은 문자열로 한다** — 긴 문장은 자간 누적 오차가 굵기 신호를 덮는다.

    smoothing: 리셋의 `-webkit-font-smoothing: antialiased` 를 후보 렌더에도 적용한다(기본 켜짐).
    **끄면 획이 두껍게 렌더돼 밀도가 통째로 어긋나 굵기를 한두 단계 무겁게 오판한다.**
    대상 페이지가 그 속성을 쓰지 않을 때만 False."""
    import os, html as _h
    faces = font_faces(font_dir)
    used, css, rows = {}, [], []
    for fam, w, fs, ls in cands:
        if fam not in faces or w not in faces[fam]:
            raise RuntimeError('%s %d 웨이트 파일이 %s 에 없다' % (fam, w, font_dir))
        used[(fam, w)] = faces[fam][w]
    for (fam, w), path in used.items():
        css.append("@font-face{font-family:%s;font-weight:%d;src:url(file://%s) format('woff2')}"
                   % (fam, w, path))
    for fam, w, fs, ls in cands:
        rows.append('<p style="background:%s;color:%s;font-family:%s;font-weight:%d;'
                    'font-size:%gpx;letter-spacing:%gem">%s</p>'
                    % (bg, fg, fam, w, fs, ls, _h.escape(text)))
    H = 90
    sm = ('-webkit-font-smoothing:antialiased;font-synthesis:none;' if smoothing else '')
    doc = ('<!DOCTYPE html><meta charset="utf-8"><style>%s *{margin:0;padding:0}'
           'body{width:2400px;%s}p{height:%dpx;line-height:%dpx;white-space:nowrap;'
           'padding-left:8px}</style><body>%s</body>'
           % (''.join(css), sm, H, H, ''.join(rows)))
    tmp = os.path.join(os.path.dirname(os.path.abspath(out)) or '.', '_probe.html')
    open(tmp, 'w', encoding='utf-8').write(doc)
    try:
        _run(['--window-size=2400,%d' % (H * len(cands) + 40), '--screenshot=' + out,
              'file://' + tmp])
    finally:
        os.remove(tmp)

    def hx(c):
        c = c.lstrip('#')
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    FG, BG = hx(fg), hx(bg)
    im = Img(out)
    A = _amap(design, box, FG, BG)
    dh, dw = len(A), len(A[0])
    print('시안  w%-4d h%-3d den %.3f  "%s"'
          % (dw, dh, density(design, box, FG, BG), text))
    res = []
    for i, (fam, w, fs, ls) in enumerate(cands):
        b = ink_box(im, 0, i * H, 2400, (i + 1) * H, notnear(BG, 20))
        if b is None:
            continue
        B = _amap(im, b, FG, BG); bh, bw = len(B), len(B[0])
        best = 9.0
        for oy in range(-2, 3):
            for ox in range(-2, 3):
                s = n = 0
                for y in range(max(dh, bh)):
                    for x in range(max(dw, bw)):
                        av = A[y][x] if y < dh and x < dw else 0
                        bv = B[y + oy][x + ox] if 0 <= y + oy < bh and 0 <= x + ox < bw else 0
                        s += abs(av - bv); n += 1
                best = min(best, s / n)
        res.append((best, '%s %d / %gpx / ls%g' % (fam, w, fs, ls),
                    bw, bh, density(im, b, FG, BG)))
    for v, lab, bw, bh, de in sorted(res):
        print('  %-26s w%-4d h%-3d den %.3f  차이 %.4f  %s'
              % (lab, bw, bh, de, v,
                 '←' if (v, lab, bw, bh, de) == min(res) else ''))
    return sorted(res)

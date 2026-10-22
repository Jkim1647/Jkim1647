"""프로젝트별 개념도 애니메이션 SVG. render_cards.main()이 테마마다 호출한다.

수치는 모두 portfolio 저장소의 프로젝트 문서와 각 저장소 README에 적힌 측정값이다.
점 위치 · 확률 막대처럼 그림을 위해 만든 값은 각 그림 아래에 "개념도"로 밝힌다.
"""
from xml.sax.saxutils import escape

from render_cards import MONO, t

W = 1200
WARN = {"light": "#CF222E", "dark": "#F85149"}


HEAD = 30  # 제목 아래 부제 한 줄만큼 본문을 내린다


def _open(c, H, title, note, aria):
    H += HEAD
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{escape(aria)}">', "",
            f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
            t(40, 48, title, 20, c["ink"], W - 80, 700),
            t(40, 74, note, 13, c["muted"], W - 80),
            f'<g transform="translate(0,{HEAD})">']


def _close(out, css, foot, c, H):
    css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
    out[1] = f'<style>{"".join(css)}</style>'
    out.append("</g>")
    out.append(t(40, H + HEAD - 18, foot, 12, c["faint"], W - 80))
    out.append("</svg>")
    return "\n".join(out)


def _box(x, y, w, h, c, stroke=None, fill=None, sw=1.5):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill or c["bg"]}" '
            f'stroke="{stroke or c["line"]}" stroke-width="{sw}"/>')


def _show(name, t0, t1, C, fade=.3):
    """t0~t1초 동안만 보이는 키프레임. 모션 줄이기에서는 기본값(보임)으로 남는다."""
    p = lambda s: f"{max(0, min(100, s / C * 100)):.2f}%"
    return (f"@keyframes {name}{{0%,{p(t0 - fade)}{{opacity:0}}{p(t0)},{p(t1)}{{opacity:1}}"
            f"{p(t1 + fade)},100%{{opacity:0}}}}")


# ── 1. 통합사원증: 인사 데이터가 다섯 시스템으로 흘러가고, 장애는 계층별로 좁힌다 ──────────────

def hds_flow(c, mode) -> str:
    H, C = 452, 12.0
    warn = WARN[mode]
    out = _open(c, H, "통합사원증 시스템 — 인사 데이터가 출입 · 식당 · 버스까지",
                "20개 계열사 · 175개 사업장 · 임직원 약 12.8만 명 (2023-07)",
                "통합사원증 시스템 구조: 계열사 인사 시스템과 통합사원증 서버가 송수신하고, 서버가 카드사 · 출입통제 · 식수 관리 · 자가문진 · 통근버스로 연동된다. "
                "출입 장애는 ACU, 카드리더, 서버 로그 순으로 좁힌다.")
    css = [".a{animation:12s linear infinite}"]

    # 왼쪽: 인사 시스템, 가운데: 서버, 오른쪽: 연동 시스템 5개
    hr = (40, 160, 230, 100)
    sv = (450, 128, 300, 164)
    outs = [("카드사", "사원증 발급 · 재발급"), ("출입통제", "ACU → 카드리더 · 게이트"), ("식수 관리", "식당 태깅 · 정산"),
            ("자가문진", "코로나기 출근 검증"), ("통근버스", "사원증 탑승")]
    ox, ow, oh = 890, 270, 48
    oy = [80 + i * 58 for i in range(len(outs))]

    out += [_box(*hr, c), t(hr[0] + 20, hr[1] + 42, "계열사 인사 시스템", 16, c["ink"], 200, 700),
            t(hr[0] + 20, hr[1] + 70, "20개 계열사", 13, c["muted"], 200)]
    out += [_box(*sv, c, stroke=c["accent"]), t(sv[0] + 24, sv[1] + 44, "통합사원증 서버", 18, c["ink"], 260, 700),
            t(sv[0] + 24, sv[1] + 72, "MSSQL · Windows · VB6", 13, c["accent"], 260, 600, MONO),
            t(sv[0] + 24, sv[1] + 104, "1인 1카드 권한", 13, c["muted"], 260),
            t(sv[0] + 24, sv[1] + 126, "데이터 정합성", 13, c["muted"], 260)]

    # 연결선
    x0, x1 = hr[0] + hr[2], sv[0]
    for y in (198, 222):
        out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["line"]}" stroke-width="1.5"/>')
    out.append(t((x0 + x1) / 2, 186, "송수신", 12, c["faint"], 80, 500, MONO, anchor="middle"))
    sx, sy = sv[0] + sv[2], sv[1] + sv[3] / 2
    for i, y in enumerate(oy):
        out.append(f'<line x1="{sx}" y1="{sy}" x2="{ox}" y2="{y + oh / 2}" stroke="{c["line"]}" stroke-width="1.5"/>')

    # 데이터 패킷: 인사 → 서버(위 선), 서버 → 인사(아래 선), 서버 → 각 시스템
    def packet(name, a, b, t0, dur):
        css.append(f"@keyframes {name}{{0%,{t0 / C * 100:.2f}%{{transform:none;opacity:0}}"
                   f"{(t0 + .05) / C * 100:.2f}%{{opacity:1}}"
                   f"{(t0 + dur) / C * 100:.2f}%{{transform:translate({b[0] - a[0]:.0f}px,{b[1] - a[1]:.0f}px);opacity:1}}"
                   f"{(t0 + dur + .05) / C * 100:.2f}%,100%{{transform:translate({b[0] - a[0]:.0f}px,{b[1] - a[1]:.0f}px);opacity:0}}}}")
        out.append(f'<circle class="a" cx="{a[0]}" cy="{a[1]}" r="5" fill="{c["accent"]}" style="animation-name:{name};opacity:0"/>')

    for k in range(3):
        packet(f"up{k}", (x0, 198), (x1, 198), .3 + k * .5, .8)
        packet(f"dn{k}", (x1, 222), (x0, 222), 1.0 + k * .5, .8)
    for wave in range(2):
        for i, y in enumerate(oy):
            packet(f"o{wave}_{i}", (sx, sy), (ox, y + oh / 2), 2.2 + wave * 1.6 + i * .18, .7)

    # 연동 시스템 상자 (출입통제는 장애 장면에서 경고색 테두리)
    for i, ((name, sub), y) in enumerate(zip(outs, oy)):
        out.append(_box(ox, y, ow, oh, c))
        out.append(t(ox + 16, y + 21, name, 14, c["ink"], 110, 700))
        out.append(t(ox + 16, y + 39, sub, 12, c["muted"], ow - 24))
    gate_y = oy[1]
    css.append(_show("warnbox", 6.6, 11.3, C))
    out.append(f'<g class="a" style="animation-name:warnbox">{_box(ox, gate_y, ow, oh, c, stroke=warn, fill="none", sw=2.5)}'
               + t(ox + ow - 14, gate_y + 21, "⚠ 출입 불가", 12, warn, 110, 700, anchor="end") + "</g>")

    # 장애 추적: ACU → 카드리더 → 서버 로그 순서로 하나씩 켜진다
    ty = 384
    out.append(t(40, ty + 6, "출입 장애 추적 순서", 14, c["ink"], 200, 700))
    steps = ["① ACU", "② 카드리더", "③ 서버 로그"]
    for i, s in enumerate(steps):
        x = 230 + i * 190
        name = f"st{i}"
        css.append(f"@keyframes {name}{{0%,{(7.2 + i) / C * 100:.2f}%{{opacity:.25}}{(7.5 + i) / C * 100:.2f}%,"
                   f"{11.3 / C * 100:.2f}%{{opacity:1}}{11.6 / C * 100:.2f}%,100%{{opacity:.25}}}}")
        out.append(f'<g class="a" style="animation-name:{name}">'
                   f'<rect x="{x}" y="{ty - 16}" width="160" height="32" rx="16" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
                   + t(x + 80, ty + 5, s, 13, c["accent"], 150, 700, MONO, anchor="middle") + "</g>")
        if i < len(steps) - 1:
            out.append(t(x + 175, ty + 5, "→", 14, c["faint"], 20, anchor="middle"))
    css.append(_show("concl", 10.2, 11.3, C))
    out.append(f'<g class="a" style="animation-name:concl">'
               + t(820, ty + 5, "→ 하드웨어 · 소프트웨어 원인 분리", 14, c["ink"], 340, 600) + "</g>")
    return _close(out, css, "2021.02–2024.01 · 수도권 사업장 담당 · 운영 · 유지보수 · 장애 대응 중심. 시스템 구조는 portfolio 문서 기준.", c, H)


# ── 2. 리팩토링: 고정 → 측정 → 개선 → 실제 DB 검증, 그리고 측정값 ──────────────────────────────

REFACTOR = [  # (무엇을, 전, 후, 단위, 후/전 비율)
    ("꼬리표 이미지 150장 생성", "29.9", "9.9", "s", 9.9 / 29.9),
    ("신청 폼 전화번호 13자 입력 시 렌더", "882", "14", "회", 14 / 882),
    ("관리자 First Load JS (GBS 라인업)", "781", "273", "kB", 273 / 781),
    ("리더 포털 첫 화면 (요청당 300ms 지연 가정)", "2,508", "1,467", "ms", 1467 / 2508),
]


def refactor_loop(c, mode) -> str:
    H, C = 470, 12.0
    out = _open(c, H, "수양회 시스템 2026 리팩토링 — 고치기 전에 먼저 고정하고 잰다",
                "커밋 64건 · 테스트 Jest 78 · Vitest 95 · E2E 176",
                "리팩토링 진행 순서: 특성화 테스트로 현재 동작 고정, 측정 도구 먼저, 리팩토링과 성능 개선, 로컬 DB에 붙여 38개 화면 검증으로 버그 12건 추가 발견. "
                "측정값: 꼬리표 이미지 29.9초에서 9.9초, 신청 폼 렌더 882회에서 14회, First Load JS 781kB에서 273kB, 리더 포털 첫 화면 2508ms에서 1467ms.")
    css = [".a{animation:12s linear infinite}"]

    steps = [("1", "특성화 테스트로", "현재 동작 고정"), ("2", "측정 도구 먼저", "벤치 · 렌더 카운터"),
             ("3", "리팩토링 ·", "성능 개선"), ("4", "로컬 DB로 38개 화면", "→ 버그 12건 추가 발견")]
    sw, gap, sy = 255, 24, 78
    for i, (n, a, b) in enumerate(steps):
        x = 40 + i * (sw + gap)
        name = f"step{i}"
        css.append(f"@keyframes {name}{{0%,{(i * 1.1) / C * 100:.2f}%{{opacity:.35}}{(i * 1.1 + .3) / C * 100:.2f}%,"
                   f"{11.4 / C * 100:.2f}%{{opacity:1}}{11.8 / C * 100:.2f}%,100%{{opacity:.35}}}}")
        out.append(f'<g class="a" style="animation-name:{name}">{_box(x, sy, sw, 76, c, stroke=c["accent"])}'
                   f'<circle cx="{x + 28}" cy="{sy + 38}" r="14" fill="{c["accent"]}"/>'
                   + t(x + 28, sy + 43, n, 14, "#FFFFFF", 20, 700, MONO, anchor="middle")
                   + t(x + 54, sy + 33, a, 15, c["ink"], sw - 64, 700)
                   + t(x + 54, sy + 55, b, 13, c["muted"], sw - 64) + "</g>")
        if i < len(steps) - 1:
            out.append(t(x + sw + gap / 2, sy + 44, "→", 16, c["faint"], 20, anchor="middle"))

    # 측정값: 개선 전 막대(회색) 위로 개선 후 막대가 줄어든다
    bx, bw, ry0 = 440, 520, 200
    for i, (what, before, after, unit, ratio) in enumerate(REFACTOR):
        y = ry0 + i * 56
        out.append(t(40, y + 16, what, 14, c["ink"], 380, 600))
        out.append(f'<rect x="{bx}" y="{y + 4}" width="{bw}" height="14" rx="7" fill="{c["track"]}"/>')
        name = f"bar{i}"
        css.append(f"@keyframes {name}{{0%,{(4.6 + i * .25) / C * 100:.2f}%{{transform:scaleX({1 / ratio:.3f})}}"
                   f"{(6.0 + i * .25) / C * 100:.2f}%,{11.4 / C * 100:.2f}%{{transform:none}}"
                   f"{11.8 / C * 100:.2f}%,100%{{transform:scaleX({1 / ratio:.3f})}}}}")
        out.append(f'<rect class="a" x="{bx}" y="{y + 4}" width="{bw * ratio:.1f}" height="14" rx="7" fill="{c["accent"]}" '
                   f'style="animation-name:{name};transform-box:fill-box;transform-origin:0 50%"/>')
        out.append(t(bx + bw + 20, y + 17, f"{before} → {after}{unit}", 15, c["accent"], 200, 700, MONO))
    return _close(out, css, "막대는 개선 전 값을 100%로 둔 비율. 측정 조건은 portfolio 문서의 결과 표 기준(벤치 150장 · 전화번호 13자 입력 · 요청당 300ms 지연 가정).", c, H)


# ── 3. 방문 순서 최적화: 사용자가 정한 순서 → Held-Karp로 다시 그린 경로 ─────────────────────────

def _route_points():
    import random
    rng = random.Random(10)
    pts = []
    while len(pts) < 10:  # 너무 붙지 않게 배치
        p = (rng.uniform(80, 600), rng.uniform(100, 360))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 60 ** 2 for q in pts):
            pts.append(p)
    return pts


def _held_karp_path(pts):
    """0번에서 출발하는 최단 방문 순서(돌아오지 않음). 10곳이라 비트마스크 DP로 정확히 푼다."""
    from math import dist
    n = len(pts)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    par = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == INF or not mask >> last & 1:
                continue
            for nxt in range(n):
                if mask >> nxt & 1:
                    continue
                m2, v = mask | 1 << nxt, dp[mask][last] + dist(pts[last], pts[nxt])
                if v < dp[m2][nxt]:
                    dp[m2][nxt], par[m2][nxt] = v, last
    full = (1 << n) - 1
    last = min(range(n), key=lambda j: dp[full][j])
    order, mask = [], full
    while last != -1:
        order.append(last)
        mask, last = mask & ~(1 << last), par[mask][last]
    return order[::-1]


def route(c, mode) -> str:
    from math import dist
    H, C = 452, 10.0
    out = _open(c, H, "여행 동선 최적화 — 관광지 10곳 방문 순서를 다시 계산",
                "SSAFY 1학기 관통 프로젝트 4차 · Java 17 · Spring Boot",
                "방문 순서 최적화 개념도: 사용자가 정한 순서 1,400.6km를 Held-Karp 비트마스크 DP와 2-opt로 570.3km로 줄였다. "
                "충전소 경유 경로는 Dijkstra로 충전소 8,072곳에서 중앙값 17ms.")
    css = [".a{animation:10s linear infinite}"]
    pts = _route_points()
    naive = [0, 7, 2, 9, 4, 1, 8, 3, 6, 5]
    best = _held_karp_path(pts)
    path = lambda order: "M" + " L".join(f"{pts[i][0]:.0f} {pts[i][1]:.0f}" for i in order)
    length = lambda order: sum(dist(pts[a], pts[b]) for a, b in zip(order, order[1:]))

    out.append(_box(40, 74, 600, 330, c))
    # 사용자가 정한 순서(회색 점선) → 최적 경로(강조색)가 그려진다
    css.append(_show("naive", .4, 9.4, C))
    out.append(f'<path class="a" d="{path(naive)}" fill="none" stroke="{c["faint"]}" stroke-width="2" '
               f'stroke-dasharray="6 6" style="animation-name:naive"/>')
    L = length(best)
    css.append(f"@keyframes draw{{0%,{2 / C * 100:.2f}%{{stroke-dashoffset:{L:.0f}}}{5 / C * 100:.2f}%,"
               f"{9.4 / C * 100:.2f}%{{stroke-dashoffset:0}}{9.8 / C * 100:.2f}%,100%{{stroke-dashoffset:{L:.0f}}}}}")
    out.append(f'<path class="a" d="{path(best)}" fill="none" stroke="{c["accent"]}" stroke-width="3.5" stroke-linecap="round" '
               f'stroke-linejoin="round" stroke-dasharray="{L:.0f}" style="animation-name:draw"/>')
    for i, (x, y) in enumerate(pts):
        r = 9 if i == 0 else 7
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{c["bg"]}" stroke="{c["ink"] if i == 0 else c["accent"]}" stroke-width="2.5"/>')
    out.append(t(pts[0][0] + 14, pts[0][1] - 12, "출발", 12, c["ink"], 60, 700))

    # 오른쪽: 결과와 방법
    rx = 680
    out.append(t(rx, 116, "사용자가 정한 순서", 14, c["muted"], 300))
    out.append(t(rx, 150, "1,400.6km", 30, c["faint"], 300, 700, extra=' text-decoration="line-through"'))
    css.append(_show("res", 5.0, 9.4, C))
    out.append(f'<g class="a" style="animation-name:res">'
               + t(rx, 196, "Held-Karp DP · 2-opt", 14, c["accent"], 300, 600)
               + t(rx, 240, "570.3km", 44, c["accent"], 400, 700) + "</g>")
    for i, line in enumerate(["Held-Karp 비트마스크 DP (≤15곳) · 2-opt",
                              "충전소 경유: \"80%까지 충전\" 모델 + Dijkstra",
                              "충전소 8,072곳에서 중앙값 17ms",
                              "완전탐색 · JDK · RFC 벡터와 비교 검증"]):
        out.append(t(rx, 290 + i * 26, "· " + line, 14, c["ink"], 480))
    return _close(out, css, "개념도 — 점 위치는 그림용이고(그림 속 최적 경로는 실제로 Held-Karp로 계산), 거리 값은 프로젝트의 실측 결과(관광지 10곳)입니다.", c, H)


# ── 4. AI 챌린지 2차: 확대해서 읽고 고르기 → 여러 모델 확률 평균 ──────────────────────────────

def ai2_pipeline(c, mode) -> str:
    H, C = 470, 13.0
    out = _open(c, H, "AI 챌린지 2차 — 모델을 키우는 대신 잘 보여 주고, 여러 모델의 확률을 모았다",
                "사진 속 글자 읽기 VQA · 217팀 중 2위",
                "1단계: 원본 사진에 네 조각으로 나눠 두 배로 키운 조각 4장을 함께 넣는다. 2단계: 질문과 관련된 글자를 먼저 받아 적게 한 뒤 a부터 d 중 하나를 고른다. "
                "35B 모델이 추가 학습 없이 0.9445에서 0.9655로. 3단계: 9B부터 397B까지 8종의 a~d 확률을 평균해 Private 0.98093.")
    css = [".a{animation:13s linear infinite}"]
    acc, track = c["accent"], c["track"]

    # ① 원본 → 4조각 ×2
    out.append(t(40, 96, "① 잘라서 확대", 16, c["ink"], 300, 700))
    px, py, pw, ph = 60, 118, 150, 100   # 원본 사진(작게)
    out.append(_box(px, py, pw, ph, c))
    for k in range(4):  # 사진 속 작은 글자를 흉내 낸 줄
        out.append(f'<rect x="{px + 14 + (k % 2) * 70}" y="{py + 24 + (k // 2) * 44}" width="{52 - (k % 3) * 10}" height="5" rx="2.5" fill="{c["faint"]}"/>')
    out.append(t(px + pw + 14, py + 56, "원본", 12, c["muted"], 60, 600, MONO))
    # 네 조각이 원래 자리에서 떨어져 나와, 아래 2×2 자리로 가며 커진다(그림에서는 1.4배)
    tiles = [(0, 0), (1, 0), (0, 1), (1, 1)]
    qw, qh, k_scale = pw / 2 - 4, ph / 2 - 4, 1.4
    for i, (gx, gy) in enumerate(tiles):
        tx, ty = px + gx * pw / 2 + 2, py + gy * ph / 2 + 2
        gx_to, gy_to = px + gx * (qw * k_scale + 10), 240 + gy * (qh * k_scale + 10)
        name = f"tile{i}"
        css.append(f"@keyframes {name}{{0%,{.8 / C * 100:.2f}%{{transform:none;opacity:0}}{1.0 / C * 100:.2f}%{{transform:none;opacity:1}}"
                   f"{2.2 / C * 100:.2f}%,{12.4 / C * 100:.2f}%{{transform:translate({gx_to - tx:.0f}px,{gy_to - ty:.0f}px) scale({k_scale});opacity:1}}"
                   f"{12.8 / C * 100:.2f}%,100%{{opacity:0}}}}")
        out.append(f'<rect class="a" x="{tx:.0f}" y="{ty:.0f}" width="{qw:.0f}" height="{qh:.0f}" rx="5" '
                   f'fill="{c["bg"]}" stroke="{acc}" stroke-width="1.5" style="animation-name:{name};transform-box:fill-box;transform-origin:0 0"/>')
    css.append(_show("x2", 2.2, 12.4, C))
    out.append(f'<g class="a" style="animation-name:x2">' + t(px + qw * k_scale * 2 + 30, 300, "+ 4조각", 13, acc, 110, 700, MONO)
               + t(px + qw * k_scale * 2 + 30, 320, "× 2배 확대", 13, acc, 110, 700, MONO) + "</g>")

    # ② 받아 적고 고르기
    sx = 420
    out.append(t(sx, 96, "② 읽고 나서 고르기", 16, c["ink"], 320, 700))
    out.append(_box(sx, 118, 320, 92, c))
    out.append(t(sx + 16, 142, "\"질문과 관련된 글자를 그대로 받아 적어라\"", 12, c["muted"], 296))
    css.append(f"@keyframes type{{0%,{3.0 / C * 100:.2f}%{{transform:scaleX(0)}}{4.6 / C * 100:.2f}%,{12.4 / C * 100:.2f}%{{transform:scaleX(1)}}"
               f"{12.8 / C * 100:.2f}%,100%{{transform:scaleX(0)}}}}")
    for k, wdt in enumerate((250, 180)):
        out.append(f'<rect class="a" x="{sx + 16}" y="{160 + k * 22}" width="{wdt}" height="10" rx="5" fill="{acc}" opacity=".55" '
                   f'style="animation-name:type;animation-delay:{k * .3}s;transform-box:fill-box;transform-origin:0 50%"/>')
    one = [.08, .12, .71, .09]  # 그림용 확률
    for k, (lab, p) in enumerate(zip("abcd", one)):
        y = 236 + k * 34
        out.append(t(sx + 8, y + 13, lab, 14, c["ink"], 20, 700, MONO))
        out.append(f'<rect x="{sx + 34}" y="{y}" width="260" height="16" rx="8" fill="{track}"/>')
        name = f"p{k}"
        css.append(f"@keyframes {name}{{0%,{4.8 / C * 100:.2f}%{{transform:scaleX(0)}}{5.8 / C * 100:.2f}%,{12.4 / C * 100:.2f}%{{transform:none}}"
                   f"{12.8 / C * 100:.2f}%,100%{{transform:scaleX(0)}}}}")
        out.append(f'<rect class="a" x="{sx + 34}" y="{y}" width="{260 * p:.0f}" height="16" rx="8" fill="{acc if lab == "c" else c["faint"]}" '
                   f'style="animation-name:{name};transform-box:fill-box;transform-origin:0 50%"/>')
    out.append(t(sx, 392, "글로 답하게 하지 않고 a~d 각각의 확률을 받는다", 12, c["muted"], 330))

    # ③ 8종 확률 평균
    ex = 800
    out.append(t(ex, 96, "③ 8종 확률 평균", 16, c["ink"], 360, 700))
    import random
    rng = random.Random(2)
    rows = []
    for m in range(8):  # 모델마다 조금씩 다른 확률(그림용) — 대부분 c, 일부는 다른 답에 쏠림
        base = [rng.uniform(.03, .2) for _ in range(4)]
        base[2] += rng.uniform(.25, .7) if m not in (3, 6) else .05
        if m in (3, 6):
            base[1] += .5
        s = sum(base)
        rows.append([b / s for b in base])
    avg = [sum(r[k] for r in rows) / 8 for k in range(4)]
    for m, r in enumerate(rows):
        y = 118 + m * 26
        out.append(t(ex, y + 12, f"모델 {m + 1}", 12, c["muted"], 60, 500, MONO))
        x = ex + 64
        for k, p in enumerate(r):
            out.append(f'<rect x="{x}" y="{y + 2}" width="{60 * p + 2:.0f}" height="12" rx="3" fill="{acc if k == 2 else c["faint"]}" opacity=".8"/>')
            x += 74
    css.append(_show("avg", 7.0, 12.4, C))
    out.append(f'<g class="a" style="animation-name:avg">'
               f'<line x1="{ex}" y1="334" x2="{ex + 360}" y2="334" stroke="{c["line"]}"/>'
               + t(ex, 362, "평균", 13, c["ink"], 60, 700, MONO)
               + "".join(f'<rect x="{ex + 64 + k * 74}" y="350" width="{60 * p * 1.6 + 2:.0f}" height="16" rx="4" fill="{acc if k == 2 else c["faint"]}"/>'
                         + t(ex + 64 + k * 74, 386, "abcd"[k], 12, c["muted"], 20, 600, MONO) for k, p in enumerate(avg))
               + "</g>")

    # 결과
    css.append(_show("ai2res", 8.2, 12.4, C))
    out.append(f'<g class="a" style="animation-name:ai2res">'
               + t(404, 420, "35B · 입력만 바꿔 0.9445 → 0.9655 (추가 학습 없음)", 14, acc, 392, 700)
               + t(800, 420, "8종 평균 → Private 0.98093 · 2위", 14, acc, 360, 700) + "</g>")
    return _close(out, css, "개념도 — 사진 · 확률 막대는 그림용입니다. 점수는 저장소 README의 실측값(35B val 정확도, 최종 Private 점수)입니다.", c, H)


# ── 5. AI 챌린지 1차: 선택지 회전 TTA로 위치 편향을 지운다 ───────────────────────────────────

def ai1_tta(c, mode) -> str:
    H, C = 452, 12.0
    out = _open(c, H, "AI 챌린지 1차 — 선택지를 돌려 가며 물어 위치 편향을 지운다",
                "재활용품 VQA · 954명 중 18위 (상위 약 1.9%)",
                "선택지 회전 TTA 개념도: 선택지 순서를 네 번 순환 이동해 추론하고, 확률을 원래 선택지 위치로 복원해 평균한다. "
                "첫 번째 자리를 선호하는 편향이 있으면 회전 없이는 a를 고르지만, 평균하면 정답 c를 고른다.")
    css = [".a{animation:12s linear infinite}"]
    acc = c["accent"]
    true = {"a": .15, "b": .2, "c": .5, "d": .15}  # 그림용 실제 점수
    bias = [.45, 0, 0, 0]                        # 첫 번째 자리 선호(그림용)
    choices = list("abcd")
    restored = {k: 0.0 for k in choices}
    for r in range(4):
        order = choices[r:] + choices[:r]
        raw = [true[ch] + bias[pos] for pos, ch in enumerate(order)]
        s = sum(raw)
        probs = [v / s for v in raw]
        y = 100 + r * 66
        name = f"row{r}"
        css.append(f"@keyframes {name}{{0%,{(.4 + r * 1.2) / C * 100:.2f}%{{opacity:0;transform:translateX(-12px)}}"
                   f"{(.8 + r * 1.2) / C * 100:.2f}%,{11.4 / C * 100:.2f}%{{opacity:1;transform:none}}{11.8 / C * 100:.2f}%,100%{{opacity:0}}}}")
        g = [f'<g class="a" style="animation-name:{name}">', t(40, y + 30, f"회전 {r}", 13, c["muted"], 70, 600, MONO)]
        for pos, (ch, p) in enumerate(zip(order, probs)):
            x = 120 + pos * 120
            g.append(f'<rect x="{x}" y="{y}" width="104" height="48" rx="8" fill="{c["bg"]}" stroke="{c["line"]}"/>')
            g.append(t(x + 12, y + 20, f"{pos + 1}번 자리: {ch}", 12, c["ink"], 90, 600, MONO))
            g.append(f'<rect x="{x + 12}" y="{y + 30}" width="{80 * p:.0f}" height="8" rx="4" fill="{acc if ch == "c" else c["faint"]}"/>')
            restored[ch] += p / 4
        if r == 0:
            g.append(t(612, y + 30, "← 회전 없이: a (편향)", 13, WARN[mode], 220, 600))
        g.append("</g>")
        out += g

    # 원래 선택지로 복원해 평균
    fx = 860
    css.append(_show("avg1", 5.6, 11.4, C))
    g = [f'<g class="a" style="animation-name:avg1">', t(fx, 120, "원래 선택지로 복원 → 평균", 15, c["ink"], 340, 700)]
    for k, ch in enumerate(choices):
        y = 150 + k * 46
        g.append(t(fx, y + 18, ch, 16, c["ink"], 20, 700, MONO))
        g.append(f'<rect x="{fx + 30}" y="{y + 4}" width="260" height="18" rx="9" fill="{c["track"]}"/>')
        g.append(f'<rect x="{fx + 30}" y="{y + 4}" width="{260 * restored[ch]:.0f}" height="18" rx="9" fill="{acc if ch == "c" else c["faint"]}"/>')
    g.append(t(fx, 352, "→ 정답 c", 18, acc, 300, 700))
    g.append("</g>")
    out += g
    out.append(t(40, 392, "그 밖에: 모델별 a~d 확률 soft ensemble · SHA-256 이미지 해시 단위 grouped validation으로 누수 차단 · Public 0.92116 → 0.94324",
                 13, c["ink"], W - 80))
    return _close(out, css, "개념도 — 점수 · 편향 크기는 원리를 보여 주기 위한 그림용 값입니다. 방법(순환 이동 → 복원 → 평균)은 저장소 README 그대로입니다.", c, H)


# ── 6. SafeLaw: 가리고 → 찾고 → 답하고 → 인용이 원문에 있는지 확인한다 ─────────────────────────

def safelaw_flow(c, mode) -> str:
    """SafeLaw의 세 축: 개인정보 마스킹 · 일상어 → 법률 용어 · 원문 근거 RAG."""
    H, C = 452, 13.0
    ok, warn = ("#1A7F37", WARN[mode]) if mode == "light" else ("#3FB950", WARN[mode])
    out = _open(c, H, "SafeLaw — 가리고, 법률 용어로 바꿔 찾고, 원문에 있는 근거로만 답한다",
                "개인정보 보호형 생활법률 RAG · 근로 · 임대차 · 상속 · SSAFY 16기 AI 코어 프로젝트 2회차 · 개인",
                "SafeLaw 파이프라인: 1. 외부 모델 호출 전 로컬에서 이름 · 전화번호 · 주소 등을 플레이스홀더로 바꾸고 원문과 매핑은 저장하지 않는다. "
                "2. 일상 표현을 법률 용어로 바꾸고 원문 질문과 함께 검색한다. 3. 법령 381개 조문과 판례 50건을 Chroma에서 찾는다. "
                "4. LangGraph로 답하고 인용 문구가 원문에 그대로 있는지 확인해, 확인되지 않으면 답하지 않는다.")
    css = [".a{animation:13s linear infinite}"]
    acc = c["accent"]
    bw, bh, by = 260, 196, 96
    xs = [40 + i * 284 for i in range(4)]
    stages = [("① 개인정보 마스킹", "외부 호출 전, 로컬에서"), ("② 일상어 → 법률 용어", "원문 질문도 함께 검색"),
              ("③ 근거 검색 · RAG", "Chroma · 법령 381조 · 판례 50건"), ("④ 근거로만 답변", "LangGraph · 인용 원문 검증")]
    starts = [.3, 2.8, 5.6, 8.0]
    for i, (x, (t1, t2)) in enumerate(zip(xs, stages)):
        name = f"stg{i}"
        css.append(f"@keyframes {name}{{0%,{starts[i] / C * 100:.2f}%{{opacity:.35}}{(starts[i] + .3) / C * 100:.2f}%,"
                   f"{12.4 / C * 100:.2f}%{{opacity:1}}{12.8 / C * 100:.2f}%,100%{{opacity:.35}}}}")
        out.append(f'<g class="a" style="animation-name:{name}">{_box(x, by, bw, bh, c, stroke=acc)}'
                   + t(x + 16, by + 30, t1, 15, c["ink"], bw - 32, 700) + t(x + 16, by + 52, t2, 12, c["muted"], bw - 32) + "</g>")
        if i < 3:
            out.append(t(x + bw + 12, by + bh / 2 + 6, "→", 16, c["faint"], 20, anchor="middle"))

    # ① 원문 → 플레이스홀더 (가상의 값)
    x = xs[0]
    rows = [("홍길동", "[이름]"), ("010-1234-5678", "[전화번호]"), ("서울시 ○○구 ○○로", "[주소]")]
    for k, (raw, masked) in enumerate(rows):
        y = by + 72 + k * 30
        out.append(f'<rect x="{x + 14}" y="{y}" width="{bw - 28}" height="22" rx="5" fill="{c["track"]}"/>'
                   + t(x + 24, y + 16, raw, 12, c["ink"], bw - 48, 600, MONO))
        css.append(_show(f"mask{k}", .9 + k * .35, 12.4, C))
        out.append(f'<g class="a" style="animation-name:mask{k}"><rect x="{x + 14}" y="{y}" width="{bw - 28}" height="22" rx="5" fill="{c["ink"]}"/>'
                   + t(x + 24, y + 16, masked, 12, c["panel"], bw - 48, 700, MONO) + "</g>")
    out.append(t(x + 16, by + 176, "\"누가\"는 가리고 \"무슨 일\"은 남긴다", 12, c["muted"], bw - 32, 600))

    # ② 일상 표현 → 법률 용어 칩
    x = xs[1]
    out.append(f'<rect x="{x + 14}" y="{by + 70}" width="{bw - 28}" height="40" rx="8" fill="{c["track"]}"/>'
               + t(x + 24, by + 95, "\"문자 한 통으로 잘렸어요\"", 13, c["ink"], bw - 48, 600))
    css.append(_show("arrow2", 3.3, 12.4, C))
    out.append(f'<g class="a" style="animation-name:arrow2">' + t(x + bw / 2, by + 130, "↓", 16, acc, 20, 700, anchor="middle") + "</g>")
    cx, cy = x + 14, by + 142
    for k, term in enumerate(["해고", "서면통지", "근로기준법 제27조"]):
        w = max(56, sum(13 if ord(ch) > 0x2E80 else 7.8 for ch in term) + 22)
        if cx + w > x + bw - 14:  # 상자를 넘으면 다음 줄로
            cx, cy = x + 14, cy + 30
        css.append(_show(f"term{k}", 3.7 + k * .35, 12.4, C))
        out.append(f'<g class="a" style="animation-name:term{k}"><rect x="{cx:.0f}" y="{cy}" width="{w:.0f}" height="26" rx="13" fill="{acc}" opacity=".16"/>'
                   + t(cx + w / 2, cy + 18, term, 12, acc, w, 700, anchor="middle") + "</g>")
        cx += w + 6

    # ③ 후보 중 Top-5
    x = xs[2]
    for k in range(9):
        y = by + 72 + k * 11
        w = 214 - k * 18
        out.append(f'<rect x="{x + 16}" y="{y}" width="{w}" height="7" rx="3.5" fill="{c["track"]}"/>')
        if k < 5:
            css.append(_show(f"top{k}", 6.0 + k * .12, 12.4, C))
            out.append(f'<rect class="a" x="{x + 16}" y="{y}" width="{w}" height="7" rx="3.5" fill="{acc}" style="animation-name:top{k}"/>')
    css.append(_show("top5", 6.8, 12.4, C))
    out.append(f'<g class="a" style="animation-name:top5">' + t(x + bw - 16, by + 182, "Top-5 근거", 12, acc, 120, 700, anchor="end") + "</g>")

    # ④ 인용 = 원문이면 답변, 아니면 답하지 않음
    x = xs[3]
    css.append(_show("chk", 8.6, 12.4, C))
    out.append(f'<g class="a" style="animation-name:chk"><rect x="{x + 14}" y="{by + 76}" width="{bw - 28}" height="34" rx="6" fill="{ok}" opacity=".14"/>'
               + t(x + 26, by + 98, "✓ 인용 = 원문 → 답변", 13, ok, bw - 48, 700) + "</g>")
    css.append(_show("rej", 9.6, 12.4, C))
    out.append(f'<g class="a" style="animation-name:rej"><rect x="{x + 14}" y="{by + 120}" width="{bw - 28}" height="34" rx="6" fill="{warn}" opacity=".12"/>'
               + t(x + 26, by + 142, "✕ 확인 안 되면 답하지 않음", 13, warn, bw - 48, 700) + "</g>")
    out.append(t(x + 16, by + 180, "어려운 용어는 50개 용어집으로 풀이", 12, c["muted"], bw - 32, 600))

    # 결과 지표
    metrics = ["일상어 질문 Top-5 17/17 (초기 10/17)", "법령 Recall@5 1.000", "판례 Recall@5 0.933", "인용 정확성 1.000"]
    mx = 40
    for k, m in enumerate(metrics):
        w = sum(13 if ord(ch) > 0x2E80 else 7.8 for ch in m) + 34
        css.append(_show(f"met{k}", 10.4 + k * .25, 12.4, C))
        out.append(f'<g class="a" style="animation-name:met{k}"><rect x="{mx:.0f}" y="320" width="{w:.0f}" height="34" rx="17" fill="{acc}" opacity=".12"/>'
                   + t(mx + 17, 342, m, 13, acc, w, 700) + "</g>")
        mx += w + 12
    return _close(out, css, "예시 질문 · 값은 그림용(가상) · 30문항 평가, 정답 라벨은 개발자 작성으로 법률 전문가 검수 전 · 응답 31.8~64.0초 → 8.3~16.7초(E2E 0.750 → 0.667) · 테스트 168개", c, H)


ALL = {"hds": hds_flow, "refactor": refactor_loop, "route": route, "ai2": ai2_pipeline, "ai1": ai1_tta,
       "safelaw": safelaw_flow}

"""프로필 README용 SVG(히어로 배너 · 프로젝트 카드 · 빌드 로그)를 라이트/다크 두 벌로 생성한다.

    python scripts/fetch_contributions.py   # 기여 달력 갱신(히어로 입자의 원본)
    python scripts/render_cards.py

수치를 바꿀 때는 아래 CARDS · CHAPTERS만 고치고 다시 실행하면 assets/ 가 갱신된다.
SVG는 <img>로 렌더링되어 웹폰트를 못 불러오므로, 보는 사람 OS 글꼴 폭이 달라도
넘치지 않도록 fit()으로 예상 폭을 검사한다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

SANS = "-apple-system, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Consolas, 'D2Coding', monospace"

THEMES = {
    "light": dict(bg="#FFFFFF", panel="#F6F8FA", line="#D0D7DE", ink="#1F2328",
                  muted="#59636E", faint="#8C959F", accent="#0969DA", track="#E6EAEF"),
    "dark": dict(bg="#0D1117", panel="#161B22", line="#30363D", ink="#E6EDF3",
                 muted="#9198A1", faint="#6E7681", accent="#4493F8", track="#21262D"),
}

HERO = dict(
    name="김진영",
    name_en="Jinyoung Kim",
    role="운영을 아는 백엔드 개발자",
    motto=["느린 곳은 먼저 재고, 숫자로 고치고,", "결과는 직접 만든 기준으로 검증합니다."],
    target="백엔드 개발 · IT 시스템 운영 · AI 서비스",
    track=[("2019", "기능경기대회"), ("2021", "HDS 시스템 운영"), ("2024", "공군 관제 체계"),
           ("2025", "수양회 백엔드"), ("2026", "SSAFY 16기 · AI"), ("NEXT", "?")],
)

# before/after가 있으면 막대로 비율을 보여준다. ratio는 과장하지 않도록 보수적인 쪽(3~5분 → 3분 기준)으로 잡는다.
CARDS = [
    dict(slug="hds", tag="OPERATIONS · 2021–2024",
         title="현대자동차그룹 통합사원증·출입통제 운영",
         sub="에이치디에스㈜ 사원 · MSSQL · Windows Server · VB6",
         metric="12.8만 명", note="임직원 규모",
         caption="20개 계열사 · 175개 사업장 · 서버 교체 · 장애 대응"),
    dict(slug="sarang", tag="BACKEND · 2025",
         title="수양회 관리 시스템 백엔드",
         sub="7인 팀 · Node.js · PostgreSQL · 참가자 약 1,500명 실사용",
         before="3~5분", metric="22.8초", ratio=22.8 / 180,
         caption="라벨 이미지 ZIP 생성 · 브라우저 풀 + 환경별 동시성 제어"),
    dict(slug="refactor", tag="REFACTORING · 2026",
         title="수양회 시스템 2026 리팩토링",
         sub="1인 · 특성화 테스트로 동작을 고정한 뒤 측정",
         before="29.9s", metric="9.9s", ratio=9.9 / 29.9,
         caption="폼 리렌더 882 → 14 · First Load JS −65% · E2E 176"),
    dict(slug="ssafy", tag="ALGORITHM · 2026",
         title="SSAFY 1학기 관통 프로젝트",
         sub="2~3인 팀 · Java 17 · Spring Boot 3.5 · FastAPI",
         before="1,400km", metric="570km", ratio=570 / 1400,
         caption="Held-Karp DP로 방문 순서 최적화 · 4차에 걸쳐 확장"),
    dict(slug="ai2", tag="AI · VQA · TEAM",
         title="AI 챌린지 2차 · 사진 속 글자 읽기",
         sub="5인 팀 · vLLM · Qwen3.5 · Gemma 4 · LoRA",
         metric="2위", note="/ 217팀",
         caption="Public 11위 → Private 2위 · 자체 채점표 401문제"),
    dict(slug="ai1", tag="AI · VQA · SOLO",
         title="AI 챌린지 1차 · 재활용품",
         sub="개인전 · Qwen3-VL · QLoRA · RunPod A100",
         metric="18위", note="/ 954명 · 상위 1.9%",
         caption="선택지 회전 TTA · 해시 기반 grouped validation"),
]


def width(text: str, size: float) -> float:
    """한글·전각은 글자 크기만큼, 나머지는 그 0.6배로 잡는 보수적 추정."""
    return sum(size if ord(ch) > 0x2E80 else size * 0.6 for ch in text)


def fit(text: str, size: float, room: float) -> str:
    assert width(text, size) <= room, f"너무 김({width(text, size):.0f} > {room}): {text}"
    return escape(text)


def t(x, y, text, size, fill, room, weight=400, family=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>'
            f'{fit(text, size, room)}</text>')


# ── 히어로: 지난 1년 기여 달력의 칸들이 줌아웃 → 변신 → 줌인을 반복하며 커리어 단계의 모양이 된다 ──
# 모양은 360×200 기준 좌표에서 "점이 이 안에 있나"로 정의하고, 히어로에서는 SCALE배로 키워 쓴다.

BASE_W, BASE_H = 360, 200
SCALE = 1.45
STAGE_X, STAGE_Y = 608, 18
STAGE_W, STAGE_H = BASE_W * SCALE, BASE_H * SCALE
PHASE_SEC = 4.5
TOKENS = ["{", "}", "<>", "=>", "fn", "0", "1", ";", "//", "[]", "()", "if", "&&", "λ", "#", "::", "$", "*"]
N_PARTICLES = 120  # 빌드 로그 카드용(코드 토큰)

CONTRIB = ROOT / "data" / "contributions.json"


def _in_poly(x, y, poly):
    inside, j = False, len(poly) - 1
    for i, (xi, yi) in enumerate(poly):
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def _in_circle(x, y, cx, cy, r):
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def _in_ellipse(x, y, cx, cy, rx, ry):
    return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1


def _in_rect(x, y, x0, y0, x1, y1):
    return x0 <= x <= x1 and y0 <= y <= y1


CAR_BODY = [(16, 148), (26, 120), (118, 106), (165, 78), (238, 78), (290, 110), (342, 118), (350, 148)]
WHEELS = [(92, 168), (282, 168)]
ROTORS = [(72, 64), (288, 64)]

SHAPES = {
    "robot": lambda x, y: (_in_rect(x, y, 152, 8, 208, 54) or _in_rect(x, y, 132, 62, 228, 134)
                           or _in_rect(x, y, 102, 66, 122, 128) or _in_rect(x, y, 238, 66, 258, 128)
                           or _in_rect(x, y, 146, 142, 172, 194) or _in_rect(x, y, 188, 142, 214, 194)),
    # 로드스터 옆모습: 바퀴 자리(휠하우스)를 비운 차체 + 링 모양 바퀴 둘
    "car": lambda x, y: ((_in_poly(x, y, CAR_BODY)
                          and not any(_in_circle(x, y, cx, cy, 30) for cx, cy in WHEELS))
                         or any(_in_circle(x, y, cx, cy, 25) and not _in_circle(x, y, cx, cy, 11)
                                for cx, cy in WHEELS)),
    # 쿼드콥터 정면: 몸통 · 팔 · 로터 · 카메라 · 착륙 스키드
    "drone": lambda x, y: (_in_rect(x, y, 138, 82, 222, 122) or _in_rect(x, y, 62, 94, 298, 104)
                           or any(_in_rect(x, y, cx - 6, cy, cx + 6, 96) for cx, cy in ROTORS)
                           or any(_in_ellipse(x, y, cx, cy, 52, 7) for cx, cy in ROTORS)
                           or _in_circle(x, y, 180, 134, 13)
                           or _in_rect(x, y, 148, 122, 156, 158) or _in_rect(x, y, 204, 122, 212, 158)
                           or _in_rect(x, y, 124, 156, 236, 164)),
    "rocket": lambda x, y: (_in_rect(x, y, 160, 40, 200, 150)
                            or _in_poly(x, y, [(160, 41), (180, 0), (200, 41)])
                            or _in_poly(x, y, [(161, 104), (132, 156), (161, 148)])
                            or _in_poly(x, y, [(199, 104), (228, 156), (199, 148)])
                            or _in_poly(x, y, [(166, 156), (194, 156), (180, 198)])),
    # 비행접시: 원반 + 돔 + 아래 링
    "ufo": lambda x, y: (_in_ellipse(x, y, 180, 112, 140, 24)
                         or (_in_circle(x, y, 180, 100, 48) and y <= 100)
                         or _in_ellipse(x, y, 180, 136, 62, 9)),
}

# 커리어 단계: (모양, 히어로 하단 트랙에서 밝힐 노드, 캡션). 첫 단계는 기여 달력 그 자체.
CHAPTERS = [
    ("robot", [0], "2017–2019 · 서울로봇고 공업전자기기 — 전국기능경기대회 장려상"),
    ("car", [1], "2021–2024 · 현대자동차그룹 통합사원증 운영 — 임직원 약 12.8만 명"),
    ("drone", [2], "2024–2025 · 공군 방공관제 — 24시간 관제 체계 운용 지원"),
    ("rocket", [3, 4], "2025–2026 · 백엔드 3~5분 → 22.8초 · AI 챌린지 2위/217팀"),
    ("ufo", [5], "NEXT · 백엔드 · IT 운영 · AI 서비스 — 함께할 팀을 찾습니다"),
]

RAMP = {  # 기여 단계 0~4 색. 단계가 높을수록 진하다(다크는 밝다)
    "light": ["#E3E8EE", "#B4D2FF", "#6EA8FE", "#2F7FF0", "#0550AE"],
    "dark": ["#21262D", "#0D3A73", "#1663C7", "#3B8BF5", "#79B8FF"],
}


def _sample(shape, n, rng, g=8):
    """기준 좌표의 (x, y, 외곽선 여부) n개. 외곽선을 먼저 채워 실루엣을 또렷하게, 남는 입자로 안쪽을 채운다."""
    fn = SHAPES[shape]
    inside = [(x, y) for y in range(-4, BASE_H + 5, g) for x in range(-4, BASE_W + 5, g) if fn(x, y)]
    edge = [(x, y) for x, y in inside
            if not all(fn(x + dx, y + dy) for dx, dy in ((g, 0), (-g, 0), (0, g), (0, -g)))]
    fill = [p for p in inside if p not in edge]

    def pick(pts, k):  # 무작위로 솎아낸다 — 래스터 순서로 일정 간격을 뽑으면 세로 줄무늬가 생긴다
        if k <= len(pts):
            return rng.sample(pts, k)
        return pts + [rng.choice(pts) for _ in range(k - len(pts))]

    k_edge = min(len(edge), int(n * 0.7))
    picked = [(*p, True) for p in pick(edge, k_edge)] + [(*p, False) for p in pick(fill, n - k_edge)]
    rng.shuffle(picked)  # 입자마다 목적지를 섞어야 "모여드는" 움직임이 된다
    return picked


def _scatter(n, rng):
    return [(rng.uniform(-10, BASE_W + 10), rng.uniform(-6, BASE_H + 6)) for _ in range(n)]


def load_contrib() -> dict:
    import json
    return json.loads(CONTRIB.read_text(encoding="utf-8"))


def _calendar_xy(days):
    """GitHub 달력과 같은 배치(열 = 주, 행 = 요일, 일요일 위)를 스테이지 가운데에 놓는다."""
    from datetime import date, timedelta
    first = date.fromisoformat(days[0]["date"])
    sunday = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = (date.fromisoformat(days[-1]["date"]) - sunday).days // 7 + 1
    pitch = STAGE_W / cols
    top = (STAGE_H - pitch * 7) / 2
    xy = []
    for d in days:
        dd = date.fromisoformat(d["date"])
        xy.append((((dd - sunday).days // 7 + 0.5) * pitch, top + ((dd.weekday() + 1) % 7 + 0.5) * pitch))
    return xy, pitch


def calendar_swarm(c, ramp, contrib) -> tuple[str, str]:
    """(스테이지 SVG, 캡션 SVG). 입자 하나 = 지난 1년의 하루."""
    import random
    rng = random.Random(1647)
    days = contrib["days"]
    n = len(days)
    grid, pitch = _calendar_xy(days)
    size = max(4.0, pitch * 0.78)
    shapes = [[(x * SCALE, y * SCALE, e) for x, y, e in _sample(s, n, rng, g=5)] for s, _, _ in CHAPTERS]

    phases = len(CHAPTERS) + 1  # 달력 + 모양들
    cycle = PHASE_SEC * phases
    span = 100 / phases
    cx, cy = STAGE_W / 2, STAGE_H / 2

    # 줌: 단계마다 아주 작게(줌아웃) 회전하며 들어와 → 커지고(줌인) → 머물다 → 다시 작아진다
    zoom = []
    for k in range(phases):
        s = k * span
        zoom += [f"{s:.2f}%{{transform:scale(.06) rotate(-80deg)}}",
                 f"{s + span * .16:.2f}%{{transform:scale(1) rotate(0)}}",
                 f"{s + span * .80:.2f}%{{transform:scale(1) rotate(0)}}",
                 f"{s + span:.2f}%{{transform:scale(.06) rotate(80deg)}}"]

    def window(k, inner):  # k번째 단계 동안만 켜지는 키프레임
        s, e = k * span, (k + 1) * span
        return (f"0%,{s + span * .14:.2f}%{{{inner[0]}}}{s + span * .2:.2f}%,{s + span * .76:.2f}%{{{inner[1]}}}"
                f"{s + span * .8:.2f}%,100%{{{inner[0]}}}")

    css = [f".z{{animation:z {cycle}s cubic-bezier(.65,0,.35,1) infinite;transform-origin:{cx:.0f}px {cy:.0f}px}}",
           f".mo{{animation:mo {cycle}s ease-in-out infinite;transform-origin:{cx:.0f}px {cy:.0f}px}}",
           f".p{{animation:{cycle}s cubic-bezier(.5,0,.2,1) infinite}}",
           f".cap{{opacity:0;animation:{cycle}s linear infinite}}",
           f".hl{{opacity:0;animation:{cycle}s linear infinite}}",
           f".fx{{opacity:0;animation:{cycle}s linear infinite}}",
           "@keyframes z{" + "".join(zoom) + "}"]

    # 모양별 움직임: 로봇은 춤, 자동차는 주행, 드론은 호버링, 로켓은 상승, UFO는 기울며 떠 있기
    def seg(k, a, b):
        return k * span + span * a, k * span + span * b
    mo = ["0%{transform:none}"]
    r0, r1 = seg(1, .2, .76)
    mo += [f"{r0 + (r1 - r0) * i / 6:.2f}%{{transform:rotate({(-6, 6)[i % 2] if 0 < i < 6 else 0}deg)}}"
           for i in range(7)]
    c0, c1 = seg(2, .2, .76)
    mo += [f"{c0:.2f}%{{transform:none}}", f"{(c0 + c1) / 2:.2f}%{{transform:translateX(18px)}}",
           f"{c1:.2f}%{{transform:none}}"]
    d0, d1 = seg(3, .2, .76)
    mo += [f"{d0 + (d1 - d0) * i / 4:.2f}%{{transform:translateY({(0, -9, 0, -9, 0)[i]}px)}}" for i in range(5)]
    k0, k1 = seg(4, .2, .76)
    mo += [f"{k0:.2f}%{{transform:none}}", f"{k0 + 1:.2f}%{{transform:translateX(-2px)}}",
           f"{k0 + 2:.2f}%{{transform:translateX(2px)}}", f"{k1:.2f}%{{transform:translateY(-22px)}}"]
    u0, u1 = seg(5, .2, .76)
    mo += [f"{u0:.2f}%{{transform:none}}", f"{(u0 * 2 + u1) / 3:.2f}%{{transform:translateY(-8px) rotate(-4deg)}}",
           f"{(u0 + u1 * 2) / 3:.2f}%{{transform:translateY(-4px) rotate(4deg)}}", f"{u1:.2f}%,100%{{transform:none}}"]
    css.append("@keyframes mo{" + "".join(mo) + "}")

    # 효과: 드론 로터 회전, 로켓 불꽃, UFO 광선 — 해당 단계에서만 보인다
    fx_on = {"drone": 3, "ufo": 5}
    for name, k in fx_on.items():
        css.append(f"@keyframes fx_{name}{{{window(k, ('opacity:0', 'opacity:1'))}}}")
    css.append("@keyframes spin{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.25)}}"
               ".spin{animation:spin .16s linear infinite;transform-box:fill-box;transform-origin:50% 50%}")
    S = SCALE
    fx_top = [f'<g class="fx" style="animation-name:fx_drone" stroke="{c["accent"]}" stroke-opacity=".7" stroke-width="2" fill="none">'
          + "".join(f'<ellipse class="spin" cx="{x * S:.0f}" cy="{y * S:.0f}" rx="{58 * S:.0f}" ry="{6 * S:.0f}"/>'
                    for x, y in ROTORS) + "</g>"]
    fx = [f'<g class="fx" style="animation-name:fx_ufo"><path d="M{150 * S:.0f} {146 * S:.0f} L{210 * S:.0f} {146 * S:.0f} '
          f'L{250 * S:.0f} {204 * S:.0f} L{110 * S:.0f} {204 * S:.0f} Z" fill="{c["accent"]}" opacity=".14"/></g>']

    # 입자: 달력 칸 → 모양들 → 달력. 활동한 날(단계 1 이상)은 모양 안에서도 진한 색으로 반짝인다
    parts = []
    for i, d in enumerate(days):
        lv = d["level"]
        bx, by = grid[i]
        j = rng.uniform(0, span * .08)

        def at(p, pt, fill):
            return f"{p:.2f}%{{transform:translate({pt[0] - bx:.0f}px,{pt[1] - by:.0f}px);fill:{fill}}}"

        frames = [at(0, (bx, by), ramp[lv]), at(span * .8, (bx, by), ramp[lv])]
        for k, pts in enumerate(shapes, start=1):
            x, y, edge = pts[i]
            fill = ramp[max(lv, 3 if edge else 1)]
            if CHAPTERS[k - 1][0] == "rocket" and y > 154 * SCALE:  # 로켓 아래 삼각형 = 불꽃
                fill = "#F0883E" if edge else "#FFB454"
            frames += [at(k * span + span * .05 + j, (x, y), fill), at(k * span + span * .8, (x, y), fill)]
        frames.append(at(100, (bx, by), ramp[lv]))  # 마지막 줌아웃 동안 달력으로 돌아가 반복
        css.append(f"@keyframes k{i}{{{''.join(frames)}}}")
        parts.append(f'<rect class="p" x="{bx - size / 2:.1f}" y="{by - size / 2:.1f}" width="{size:.1f}" '
                     f'height="{size:.1f}" rx="1.5" fill="{ramp[lv]}" style="animation-name:k{i}"/>')

    # 캡션: 단계마다 하나씩, 스테이지 아래 가운데
    caps = [f"지난 1년 {contrib['total']} contributions · 활동 {contrib['active_days']}일 · "
            f"최장 연속 {contrib['longest_streak']}일"] + [cap for _, _, cap in CHAPTERS]
    cap_svg = []
    for k, cap in enumerate(caps):
        css.append(f"@keyframes cap{k}{{{window(k, ('opacity:0', 'opacity:1'))}}}")
        cap_svg.append(t(STAGE_X + STAGE_W / 2, STAGE_Y + STAGE_H + 26, cap, 15,
                         c["ink"] if k else c["muted"], STAGE_W, 600 if k else 500, anchor="middle",
                         extra=f' class="cap{" c0" if k == 0 else ""}" style="animation-name:cap{k}"'))
    # 모션 줄이기에서는 정지된 달력과 그 캡션만 보인다
    css.append("@media (prefers-reduced-motion:reduce){.z,.mo,.p,.cap,.hl,.fx,.spin{animation:none}"
               ".c0{opacity:1}}")

    stage = (f'<g transform="translate({STAGE_X},{STAGE_Y})"><g class="z"><g class="mo">'
             f'{"".join(fx)}{"".join(parts)}{"".join(fx_top)}</g></g></g>')
    return f'<style>{"".join(css)}</style>' + stage, "".join(cap_svg)


def hero(c, mode) -> str:
    contrib = load_contrib()
    W, H = 1200, 418
    stage, captions = calendar_swarm(c, RAMP[mode], contrib)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{escape(HERO["name"])} · {escape(HERO["role"])}">',
           f'<rect width="{W}" height="{H}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           f'<clipPath id="stageclip"><rect x="{STAGE_X - 30}" y="2" width="{STAGE_W + 50}" height="{STAGE_H + 6}"/></clipPath>',
           f'<g clip-path="url(#stageclip)">{stage}</g>',
           captions,
           # 왼쪽 글은 스테이지(x≥578)를 넘지 않게 폭을 제한한다
           t(56, 78, "TARGET  ·  " + HERO["target"], 15, c["accent"], 510, 600, MONO),
           t(56, 156, HERO["name"], 56, c["ink"], 300, 700),
           t(56 + width(HERO["name"], 56) + 20, 156, HERO["name_en"], 22, c["muted"], 300),
           t(56, 204, HERO["role"], 26, c["ink"], 510, 600)]
    for k, line in enumerate(HERO["motto"]):
        out.append(t(56, 244 + k * 26, line, 17, c["muted"], 510))

    # 걸어온 길: 하단 트랙. 정적으로는 현재(2026)만 강조하고, 애니메이션 중에는 지금 보이는 단계의 노드가 켜진다
    y, x0, x1 = 362, 80, W - 80
    track = HERO["track"]
    step = (x1 - x0) / (len(track) - 1)
    css = []
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["line"]}" stroke-width="2"/>')
    for i, (year, label) in enumerate(track):
        x = x0 + step * i
        now = year == "2026"
        nxt = year == "NEXT"
        dash = ' stroke-dasharray="3 3"' if nxt else ""
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="6" fill="{c["accent"] if now else c["bg"]}" '
                   f'stroke="{c["accent"] if now else c["faint"]}" stroke-width="2"{dash}/>')
        out.append(t(x, y + 30, f"{year}  {label}", 14, c["ink"] if now else c["muted"], step - 12,
                     600 if now else 400, anchor="middle"))
        lit = [k for k, (_, nodes, _) in enumerate(CHAPTERS, start=1) if i in nodes]
        if lit:
            phases = len(CHAPTERS) + 1
            span = 100 / phases
            k = lit[0]
            s = k * span
            css.append(f"@keyframes hl{i}{{0%,{s + span * .14:.2f}%{{opacity:0}}{s + span * .2:.2f}%,"
                       f"{s + span * .76:.2f}%{{opacity:1}}{s + span * .8:.2f}%,100%{{opacity:0}}}}")
            out.append(f'<g class="hl" style="animation-name:hl{i}">'
                       f'<circle cx="{x:.0f}" cy="{y}" r="13" fill="{c["accent"]}" opacity=".18"/>'
                       f'<circle cx="{x:.0f}" cy="{y}" r="6" fill="{c["accent"]}"/></g>')
    out.insert(2, f'<style>{"".join(css)}</style>')
    out.append("</svg>")
    return "\n".join(out)


def card(d, c) -> str:
    W, H, P = 600, 270, 32
    room = W - 2 * P
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{escape(d["title"])}">',
           f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           t(P, 50, d["tag"], 13, c["accent"], room, 600, MONO, extra=' letter-spacing="1"'),
           t(P, 86, d["title"], 22, c["ink"], room, 700),
           t(P, 114, d["sub"], 14, c["muted"], room)]

    # 핵심 수치: 개선 전 값은 흐리게, 개선 후 값은 크게
    my = 178
    if "before" in d:
        out.append(t(P, my, d["before"], 22, c["faint"], 160, 500,
                     extra=' text-decoration="line-through"'))
        bx = P + width(d["before"], 22) + 14
        out.append(t(bx, my, "→", 22, c["faint"], 40))
        out.append(t(bx + 36, my, d["metric"], 40, c["accent"], room - bx, 700))
    else:
        out.append(t(P, my, d["metric"], 40, c["accent"], 260, 700))
        if "note" in d:
            out.append(t(P + width(d["metric"], 40) + 12, my, d["note"], 18, c["muted"], 300, 500))

    # 비율 막대: 회색 = 개선 전 100%, 강조색 = 개선 후 비율
    if "ratio" in d:
        by = 198
        out.append(f'<rect x="{P}" y="{by}" width="{room}" height="6" rx="3" fill="{c["track"]}"/>')
        out.append(f'<rect x="{P}" y="{by}" width="{room * d["ratio"]:.1f}" height="6" rx="3" fill="{c["accent"]}"/>')

    out.append(t(P, 240, d["caption"], 14, c["muted"], room))
    out.append("</svg>")
    return "\n".join(out)


# ── Build with me: 방문자가 이슈로 요청한 모양을 코드 입자로 그려 주는 빌드 로그 카드 ──────────

BUILDS = ROOT / "data" / "builds.json"


def load_builds() -> dict:
    import json
    if BUILDS.exists():
        return json.loads(BUILDS.read_text(encoding="utf-8"))
    return {"counts": {s: 0 for s in SHAPES}, "recent": []}


def build_log(c, builds) -> str:
    import random
    W, H = 1200, 300
    recent = builds["recent"]
    latest = recent[0]["shape"] if recent else "car"
    rng = random.Random(len(recent) * 31 + 7)
    pts = _sample(latest, N_PARTICLES, rng)
    scatter = _scatter(N_PARTICLES, rng)

    # 왼쪽: 최근 요청된 모양이 한 번 조립된 뒤 그대로 머문다(무한 반복 아님 — 눈이 덜 피곤하다)
    ox, oy = 50, 50
    css = [f".q{{font:600 11px {MONO};fill:{c['accent']};animation:2.4s cubic-bezier(.2,.8,.2,1) both}}",
           "@media (prefers-reduced-motion:reduce){.q{animation:none}}"]
    parts = []
    for i, (x, y, is_edge) in enumerate(pts):
        sx, sy = scatter[i]
        op = 1 if is_edge else 0.4
        if not recent:
            op *= 0.35  # 아직 아무도 안 만들었으면 흐린 자리표시
        delay = rng.uniform(0, 0.6)
        css.append(f"@keyframes q{i}{{from{{transform:translate({sx - x:.0f}px,{sy - y:.0f}px);opacity:0}}"
                   f"to{{transform:none;opacity:{op}}}}}")
        parts.append(f'<text class="q" x="{x}" y="{y}" text-anchor="middle" dominant-baseline="central" '
                     f'style="animation-name:q{i};animation-delay:{delay:.2f}s">'
                     f'{escape(TOKENS[i % len(TOKENS)])}</text>')

    # 오른쪽: 터미널 로그
    tx = 470
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="Build with me 로그">',
           f'<style>{"".join(css)}</style>',
           f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           f'<g transform="translate({ox},{oy})">{"".join(parts)}</g>',
           f'<line x1="{tx - 30}" y1="28" x2="{tx - 30}" y2="{H - 28}" stroke="{c["line"]}"/>']
    for k, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        out.append(f'<circle cx="{tx + 6 + k * 18}" cy="44" r="5" fill="{col}"/>')
    out.append(t(tx + 70, 49, "build-with-me", 13, c["faint"], 300, 500, MONO))
    out.append(t(tx, 92, "$ git log --builds --last 5", 15, c["ink"], 600, 600, MONO))

    if recent:
        for r, b in enumerate(recent[:5]):
            y = 126 + r * 26
            out.append(t(tx, y, f"{b['shape']:<7}", 15, c["accent"], 90, 600, MONO, extra=' xml:space="preserve"'))
            out.append(t(tx + 90, y, "@" + b["user"], 15, c["ink"], 400, 400, MONO))
            out.append(t(W - 50, y, b["at"], 15, c["faint"], 140, 400, MONO, anchor="end"))
    else:
        out.append(t(tx, 132, "(아직 빌드 기록이 없어요)", 15, c["muted"], 600, 400, MONO))
        out.append(t(tx, 160, "아래 버튼으로 첫 번째 빌더가 되어주세요", 15, c["muted"], 600, 400, MONO))

    n = builds["counts"]
    total = sum(n.values())
    summary = " · ".join(f"{s} {n.get(s, 0)}" for s in SHAPES) + f"  ·  total {total}"
    out.append(t(tx, H - 34, summary, 14, c["muted"], 680, 500, MONO))
    out.append("</svg>")
    return "\n".join(out)


def main():
    ASSETS.mkdir(exist_ok=True)
    builds = load_builds()
    for mode, c in THEMES.items():
        (ASSETS / f"hero_{mode}.svg").write_text(hero(c, mode), encoding="utf-8")
        (ASSETS / f"buildlog_{mode}.svg").write_text(build_log(c, builds), encoding="utf-8")
        for d in CARDS:
            (ASSETS / f"card_{d['slug']}_{mode}.svg").write_text(card(d, c), encoding="utf-8")
    print(f"{len(THEMES) * (len(CARDS) + 2)} files → {ASSETS}")


if __name__ == "__main__":
    main()

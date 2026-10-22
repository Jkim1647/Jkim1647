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
         metric="2위", note="/ 217팀", rank=(11, 2, 20),
         caption="Public 11위 → Private 2위 · 자체 채점표 401문제"),
    dict(slug="ai1", tag="AI · VQA · SOLO",
         title="AI 챌린지 1차 · 재활용품",
         sub="개인전 · Qwen3-VL · QLoRA · RunPod A100",
         metric="18위", note="/ 954명 · 상위 1.9%", rank=(12, 18, 30),
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
GLOBE = (180, 100, 92)      # 지구: 중심 x, y, 반지름
SEOUL = (212, 72)           # 지구 위 서울 핀 자리(그림용)


def _on_globe(x, y):
    """선으로 그린 지구: 테두리 · 가운데 경선 · 경선 두 쌍 · 위선 셋."""
    cx, cy, r = GLOBE
    d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
    if d > r + 3:
        return False
    if abs(d - r) <= 3 or abs(x - cx) <= 2.5:
        return True
    for k in (.45, .82):
        rx = r * k
        if abs((((x - cx) / rx) ** 2 + ((y - cy) / r) ** 2) ** .5 - 1) * rx <= 2.8:
            return True
    return any(abs(y - (cy + r * s)) <= 2.5 for s in (-.55, 0, .55))

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
    "earth": _on_globe,
}

# 커리어 단계: (모양, 히어로 하단 트랙에서 밝힐 노드, 캡션). 첫 단계는 기여 달력 그 자체.
CHAPTERS = [
    ("robot", [0], "2017–2019 · 서울로봇고 공업전자기기 — 전국기능경기대회 장려상"),
    ("car", [1], "2021–2024 · 현대자동차그룹 통합사원증 운영 — 임직원 약 12.8만 명"),
    ("drone", [2], "2024–2025 · 공군 방공관제 — 24시간 관제 체계 운용 지원"),
    ("rocket", [3, 4], "2025–2026 · 백엔드 3~5분 → 22.8초 · AI 챌린지 2위/217팀"),
    ("earth", [5], "NEXT · 백엔드 · IT 운영 · AI 서비스 — 함께할 팀을 찾습니다"),
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


PHASES = len(CHAPTERS) + 1           # 달력 + 모양들
SPAN = 100 / PHASES                   # 한 단계가 차지하는 % 구간
ZOOM_OUT_END, ZOOM_IN_START = .16, .62  # 단계 안에서: 줌아웃(빠져나옴) → 머묾 → 줌인(파고듦)


def _vis(t0, t1, on="opacity:1", off="opacity:0", fade=.6):
    """t0~t1(%) 동안만 on인 키프레임 본문. 100%를 넘어가면 처음으로 이어 붙인다."""
    if t1 <= 100:
        a, b = max(t0 - fade, 0), min(t1 + fade, 100)
        return f"0%,{a:.2f}%{{{off}}}{t0:.2f}%,{t1:.2f}%{{{on}}}{b:.2f}%,100%{{{off}}}"
    t1 -= 100
    return (f"0%,{t1:.2f}%{{{on}}}{t1 + fade:.2f}%,{t0 - fade:.2f}%{{{off}}}{t0:.2f}%,100%{{{on}}}")


def _focal_days(days, k):
    """줌으로 파고들 날: 기여가 많은 날부터 k개(모자라면 반복)."""
    ranked = sorted(range(len(days)), key=lambda i: (-days[i]["count"], -days[i]["level"], days[i]["date"]))
    active = [i for i in ranked if days[i]["count"] > 0] or ranked[-1:]
    return [active[i % len(active)] for i in range(k)]


def calendar_swarm(c, ramp, contrib) -> tuple[str, str]:
    """(스테이지 SVG, 캡션 SVG). 입자 하나 = 지난 1년의 하루.

    단계가 바뀔 때 카메라가 하루 한 칸으로 지수적으로 줌인해 그 칸이 창을 가득 채우면(그날 날짜 표시),
    가려진 동안 나머지 칸이 다음 모양으로 재배치되고, 같은 날에서 줌아웃하면 주변이 바뀌어 있다.
    """
    import random
    rng = random.Random(1647)
    days = contrib["days"]
    n = len(days)
    grid, pitch = _calendar_xy(days)
    size = max(4.0, pitch * 0.78)
    shapes = [[(x * SCALE, y * SCALE, e) for x, y, e in _sample(s, n, rng, g=5)] for s, _, _ in CHAPTERS]
    pos = [[(x, y) for x, y in grid]] + [[(x, y) for x, y, _ in sh] for sh in shapes]
    cycle = PHASE_SEC * PHASES
    focal = _focal_days(days, PHASES)  # focal[k] = k단계 → 다음 단계로 넘어갈 때 파고드는 날
    cover = ramp[4]
    r, g, b = (int(cover[i:i + 2], 16) for i in (1, 3, 5))
    on_cover = "#FFFFFF" if .2126 * r + .7152 * g + .0722 * b < 140 else "#0D1117"  # 진한 칸엔 흰 글씨

    # 창(클립) 영역: 이 사각형을 다 덮을 만큼 확대해야 전환이 보이지 않는다
    clip = (-12, -10, STAGE_W + 12, STAGE_H + 6)

    def max_scale(p):
        reach = max(abs(p[0] - clip[0]), abs(clip[2] - p[0]), abs(p[1] - clip[1]), abs(clip[3] - p[1]))
        return reach / (size / 2) * 1.08

    # 카메라: 줌 구간은 배율을 지수적으로(같은 시간에 같은 배수) 키워야 카메라가 다가가는 느낌이 난다
    cam, steps = [], 8
    for k in range(PHASES):
        a = k * SPAN
        p_out = pos[k][focal[k - 1]]      # 이전 단계에서 파고든 날 — 여기서 빠져나온다
        p_in = pos[k][focal[k]]           # 다음 단계로 넘어가며 파고들 날
        s_out, s_in = max_scale(p_out), max_scale(p_in)
        o_out = f"transform-origin:{p_out[0]:.1f}px {p_out[1]:.1f}px"
        o_in = f"transform-origin:{p_in[0]:.1f}px {p_in[1]:.1f}px"
        for i in range(steps + 1):
            at_ = a + SPAN * ZOOM_OUT_END * i / steps
            cam.append(f"{at_:.2f}%{{transform:scale({s_out ** (1 - i / steps):.3f});{o_out}}}")
        for i in range(steps + 1):
            at_ = a + SPAN * (ZOOM_IN_START + (1 - ZOOM_IN_START - .02) * i / steps)
            cam.append(f"{at_:.2f}%{{transform:scale({s_in ** (i / steps):.3f});{o_in}}}")
        cam.append(f"{a + SPAN - .01:.2f}%{{transform:scale({s_in:.3f});{o_in}}}")
    cam.append(f"100%{{transform:scale({max_scale(pos[0][focal[-1]]):.3f});"
               f"transform-origin:{pos[0][focal[-1]][0]:.1f}px {pos[0][focal[-1]][1]:.1f}px}}")

    css = [f".cam{{animation:cam {cycle}s linear infinite}}",
           f".mo{{animation:mo {cycle}s ease-in-out infinite;transform-origin:{STAGE_W / 2:.0f}px {STAGE_H / 2:.0f}px}}",
           f".p{{animation:{cycle}s linear infinite}}",
           f".cap,.hl,.fx,.cv,.day{{opacity:0;animation:{cycle}s linear infinite}}",
           "@keyframes cam{" + "".join(cam) + "}"]

    # 머무는 동안의 움직임: 로봇은 춤, 자동차는 주행, 드론은 호버링, 로켓은 떨림, 지구는 천천히 떠 있기
    def seg(k, f0=.2, f1=.58):
        return k * SPAN + SPAN * f0, k * SPAN + SPAN * f1
    mo = ["0%{transform:none}"]
    r0, r1 = seg(1)
    mo += [f"{r0 + (r1 - r0) * i / 6:.2f}%{{transform:rotate({(-6, 6)[i % 2] if 0 < i < 6 else 0}deg)}}"
           for i in range(7)]
    c0, c1 = seg(2)
    mo += [f"{c0:.2f}%{{transform:none}}", f"{(c0 + c1) / 2:.2f}%{{transform:translateX(16px)}}",
           f"{c1:.2f}%{{transform:none}}"]
    d0, d1 = seg(3)
    mo += [f"{d0 + (d1 - d0) * i / 4:.2f}%{{transform:translateY({(0, -8, 0, -8, 0)[i]}px)}}" for i in range(5)]
    k0, k1 = seg(4)
    mo += [f"{k0 + (k1 - k0) * i / 8:.2f}%{{transform:translate({(0, -2, 2, -2, 2, -2, 2, -1, 0)[i]}px,"
           f"{(0, -2, -3, -4, -5, -6, -7, -4, 0)[i]}px)}}" for i in range(9)]
    u0, u1 = seg(5)
    mo += [f"{u0:.2f}%{{transform:none}}", f"{(u0 + u1) / 2:.2f}%{{transform:translateY(-5px)}}",
           f"{u1:.2f}%,100%{{transform:none}}"]
    css.append("@keyframes mo{" + "".join(mo) + "}")

    # 효과: 드론 로터 회전, 지구의 도는 경선과 서울 핀 — 줌이 시작되기 전, 머무는 동안만
    for name, k in {"drone": 3, "earth": 5}.items():
        css.append(f"@keyframes fx_{name}{{{_vis(k * SPAN + SPAN * ZOOM_OUT_END, k * SPAN + SPAN * (ZOOM_IN_START - .02))}}}")
    css.append("@keyframes spin{0%,100%{transform:scaleX(1)}50%{transform:scaleX(.25)}}"
               ".spin{animation:spin .16s linear infinite;transform-box:fill-box;transform-origin:50% 50%}"
               # 오른쪽 반원 경선을 왼쪽 끝까지 뒤집어 지구가 도는 것처럼 보인다
               "@keyframes sweep{0%{transform:scaleX(1)}100%{transform:scaleX(-1)}}"
               ".sweep{animation:sweep 3s linear infinite;transform-box:fill-box;transform-origin:0 50%}"
               "@keyframes pulse{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.8);opacity:0}}"
               ".pulse{animation:pulse 1.4s ease-out infinite;transform-box:fill-box;transform-origin:50% 50%}")
    S = SCALE
    fx_top = [f'<g class="fx" style="animation-name:fx_drone" stroke="{c["accent"]}" stroke-opacity=".7" stroke-width="2" fill="none">'
              + "".join(f'<ellipse class="spin" cx="{x * S:.0f}" cy="{y * S:.0f}" rx="{58 * S:.0f}" ry="{6 * S:.0f}"/>'
                        for x, y in ROTORS) + "</g>"]
    gx, gy, gr = (v * S for v in GLOBE)
    px, py = SEOUL[0] * S, SEOUL[1] * S
    pin = "#F0883E"
    fx_top.append(f'<g class="fx" style="animation-name:fx_earth">'
                  f'<path class="sweep" d="M{gx:.0f} {gy - gr:.0f} A{gr:.0f} {gr:.0f} 0 0 1 {gx:.0f} {gy + gr:.0f}" '
                  f'fill="none" stroke="{c["accent"]}" stroke-opacity=".6" stroke-width="2.5"/>'
                  f'<circle class="pulse" cx="{px:.0f}" cy="{py:.0f}" r="8" fill="{pin}"/>'
                  f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="{pin}" stroke="{c["panel"]}" stroke-width="2.5"/>'
                  f'<line x1="{px + 8:.0f}" y1="{py - 6:.0f}" x2="{px + 34:.0f}" y2="{py - 26:.0f}" stroke="{pin}" stroke-width="2"/>'
                  # 글자 둘레를 배경색으로 감싸 아래 칸 위에서도 읽히게
                  + t(px + 38, py - 24, "SEOUL", 15, pin, 90, 700, MONO,
                      extra=f' stroke="{c["panel"]}" stroke-width="5" paint-order="stroke" stroke-linejoin="round"') + "</g>")
    fx = []

    # 입자: 단계 동안 제자리에 있다가, 화면이 한 칸으로 가려진 경계 순간에만 다음 자리로 옮긴다
    parts = []
    for i, d in enumerate(days):
        lv = d["level"]
        bx, by = grid[i]

        def at(p, pt, fill):
            return f"{p:.2f}%{{transform:translate({pt[0] - bx:.0f}px,{pt[1] - by:.0f}px);fill:{fill}}}"

        frames = []
        for k in range(PHASES):
            x, y = pos[k][i]
            if k == 0:
                fill = ramp[lv]
            else:
                edge = shapes[k - 1][i][2]
                fill = ramp[max(lv, 3 if edge else 1)]
                if CHAPTERS[k - 1][0] == "rocket" and y > 154 * SCALE:  # 로켓 아래 삼각형 = 불꽃
                    fill = "#F0883E" if edge else "#FFB454"
            frames += [at(k * SPAN + .05 if k else 0, (x, y), fill), at((k + 1) * SPAN - .05, (x, y), fill)]
        frames.append(at(100, grid[i], ramp[lv]))
        css.append(f"@keyframes k{i}{{{''.join(frames)}}}")
        parts.append(f'<rect class="p" x="{bx - size / 2:.1f}" y="{by - size / 2:.1f}" width="{size:.1f}" '
                     f'height="{size:.1f}" rx="1.5" fill="{ramp[lv]}" style="animation-name:k{i}"/>')

    # 덮개: 파고드는 날의 칸 위에 같은 크기 칸을 맨 위에 올려, 확대됐을 때 창 전체를 한 색으로 가린다
    covers, day_labels = [], []
    for k in range(PHASES):
        f, nxt = focal[k], (k + 1) % PHASES
        end = (k + 1) * SPAN
        for idx, (pk, t0, t1) in enumerate(((k, k * SPAN + SPAN * ZOOM_IN_START, end),
                                            (nxt, end, end + SPAN * ZOOM_OUT_END))):
            x, y = pos[pk][f]
            name = f"cv{k}_{idx}"
            css.append(f"@keyframes {name}{{{_vis(t0, t1, fade=.01)}}}")
            covers.append(f'<rect class="cv" x="{x - size / 2:.1f}" y="{y - size / 2:.1f}" width="{size:.1f}" '
                          f'height="{size:.1f}" rx="1.5" fill="{cover}" style="animation-name:{name}"/>')
        # 가려진 순간에 그날이 언제였는지 보여준다
        dd = days[f]
        css.append(f"@keyframes day{k}{{{_vis(end - SPAN * .07, end + SPAN * .008, fade=.3)}}}")  # 줌아웃 시작 전에 사라진다
        label = f"{dd['date'].replace('-', '.')}"
        sub = f"{dd['count']} contribution{'s' if dd['count'] != 1 else ''}"
        day_labels.append(
            f'<g class="day" style="animation-name:day{k}">'
            + t(STAGE_W / 2, STAGE_H / 2 - 4, label, 34, on_cover, STAGE_W, 700, MONO, anchor="middle")
            + t(STAGE_W / 2, STAGE_H / 2 + 26, sub, 16, on_cover, STAGE_W, 500, MONO, anchor="middle")
            + "</g>")

    # 캡션: 단계마다 하나, 화면이 가려진 순간에 바뀐다
    caps = [f"지난 1년 {contrib['total']} contributions · 활동 {contrib['active_days']}일 · "
            f"최장 연속 {contrib['longest_streak']}일"] + [cap for _, _, cap in CHAPTERS]
    cap_svg = []
    for k, cap in enumerate(caps):
        css.append(f"@keyframes cap{k}{{{_vis(k * SPAN + .4, (k + 1) * SPAN - .4, fade=.4)}}}")
        cap_svg.append(t(STAGE_X + STAGE_W / 2, STAGE_Y + STAGE_H + 30, cap, 15,
                         c["ink"] if k else c["muted"], STAGE_W, 600 if k else 500, anchor="middle",
                         extra=f' class="cap{" c0" if k == 0 else ""}" style="animation-name:cap{k}"'))
    # 모션 줄이기에서는 정지된 달력과 그 캡션만 보인다
    css.append("@media (prefers-reduced-motion:reduce){.cam,.mo,.p,.cap,.hl,.fx,.cv,.day,.spin,.sweep,.pulse{animation:none}"
               ".c0{opacity:1}}")

    cx0, cy0, cx1, cy1 = clip
    stage = (f'<clipPath id="win"><rect x="{cx0}" y="{cy0}" width="{cx1 - cx0:.0f}" height="{cy1 - cy0:.0f}" rx="14"/></clipPath>'
             f'<g transform="translate({STAGE_X},{STAGE_Y})"><g clip-path="url(#win)">'
             f'<g class="cam"><g class="mo">{"".join(fx)}{"".join(parts)}{"".join(fx_top)}{"".join(covers)}</g></g>'
             f'{"".join(day_labels)}</g></g>')
    return f'<style>{"".join(css)}</style>' + stage, "".join(cap_svg)


def hero(c, mode) -> str:
    contrib = load_contrib()
    W, H = 1200, 418
    stage, captions = calendar_swarm(c, RAMP[mode], contrib)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{escape(HERO["name"])} · {escape(HERO["role"])}">',
           f'<rect width="{W}" height="{H}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           stage,
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
            s = lit[0] * SPAN
            css.append(f"@keyframes hl{i}{{{_vis(s + SPAN * ZOOM_OUT_END, s + SPAN * .9)}}}")
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

    # 8초 주기: 개선 전 상태로 잠깐 머문 뒤 개선 후로 바뀌고, 한동안 유지. 모션 줄이기에서는 개선 후 상태로 정지.
    loop = ("@keyframes go{0%,15%{transform:var(--from)}32%,92%{transform:none}"
            "92.01%,100%{transform:var(--from)}}"
            ".go{animation:go 8s cubic-bezier(.6,0,.2,1) infinite;transform-box:fill-box}"
            "@media (prefers-reduced-motion:reduce){.go,.fade{animation:none}}")

    # 비율 막대: 회색 = 개선 전 100%, 강조색이 100%에서 개선 후 비율까지 줄어든다
    if "ratio" in d:
        by = 198
        out.insert(1, f"<style>{loop}</style>")
        out.append(f'<rect x="{P}" y="{by}" width="{room}" height="6" rx="3" fill="{c["track"]}"/>')
        out.append(f'<rect class="go" x="{P}" y="{by}" width="{room * d["ratio"]:.1f}" height="6" rx="3" '
                   f'fill="{c["accent"]}" style="--from:scaleX({1 / d["ratio"]:.3f});transform-origin:0 50%"/>')

    # 순위 띠: 상위 n위 구간을 점으로 펼치고, 내 점이 Public 순위에서 Private 순위로 움직인다
    if "rank" in d:
        pub, pri, n = d["rank"]
        by, pitch = 202, room / n
        x_of = lambda r: P + (r - .5) * pitch
        out.insert(1, f"<style>{loop}@keyframes fade{{0%,22%{{opacity:1}}30%,92%{{opacity:0}}92.01%,100%{{opacity:1}}}}"
                      f".fade{{opacity:0;animation:fade 8s linear infinite}}</style>")
        out += [f'<circle cx="{x_of(r):.1f}" cy="{by}" r="2.6" fill="{c["track"] if r != pri else c["line"]}"/>'
                for r in range(1, n + 1)]
        out.append(f'<circle class="go" cx="{x_of(pri):.1f}" cy="{by}" r="6" fill="{c["accent"]}" '
                   f'style="--from:translateX({x_of(pub) - x_of(pri):.1f}px)"/>')
        out.append(t(x_of(pub), by + 20, f"Public {pub}위", 11, c["faint"], 90, 500, MONO, anchor="middle",
                     extra=' class="fade"'))
        out.append(t(P + room, by + 20, f"상위 {n}위 구간", 11, c["faint"], 120, 500, MONO, anchor="end"))

    out.append(t(P, 240 if "rank" not in d else 248, d["caption"], 14, c["muted"], room))
    out.append("</svg>")
    return "\n".join(out)


# ── 경로 선택 버튼: 방문자 유형별로 README 안의 해당 섹션으로 이동 ──────────────────────────────

PATHS = [
    dict(slug="recruiter", tag="FOR RECRUITERS", title="채용담당자라면", sub="30초 요약 보기"),
    dict(slug="developer", tag="FOR DEVELOPERS", title="개발자라면", sub="기술 깊이 보기"),
    dict(slug="incident", tag="INTERACTIVE · 3 SCENARIOS", title="장애 대응 시뮬레이터", sub="골라 가며 풀어 보기"),
]


def path_button(d, c, delay) -> str:
    W, H, P = 400, 112, 26
    # 화살표가 살짝 앞으로 밀렸다 돌아온다 — 세 버튼이 차례로 움직이게 지연을 준다
    css = (f"@keyframes nudge{{0%,70%,100%{{transform:none}}80%{{transform:translateX(7px)}}90%{{transform:none}}}}"
           f".arw{{animation:nudge 3s ease-in-out {delay}s infinite}}"
           "@media (prefers-reduced-motion:reduce){.arw{animation:none}}")
    sub_w = width(d["sub"], 15)
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{escape(d["title"])} — {escape(d["sub"])}">',
        f"<style>{css}</style>",
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>',
        f'<rect x="1" y="1" width="5" height="{H - 2}" rx="2" fill="{c["accent"]}"/>',
        t(P, 36, d["tag"], 12, c["accent"], W - 2 * P, 700, MONO, extra=' letter-spacing="1"'),
        t(P, 70, d["title"], 22, c["ink"], W - 2 * P, 700),
        t(P, 96, d["sub"], 15, c["muted"], W - 2 * P - 40, 500),
        f'<g class="arw">' + t(P + sub_w + 10, 96, "→", 16, c["accent"], 30, 700) + "</g>",
        "</svg>"])


# ── 최적화 설명: 라벨 ZIP 생성 3~5분 → 22.8초를 "작업이 흘러가는 모습"으로 보여준다 ──────────────
# 동시성 수 · 작업 수는 개념도용 예시. 두 줄이 끝나는 시점의 비율만 실제(3분 기준 vs 22.8초)를 따른다.

def explainer(c) -> str:
    W, H = 1200, 404
    C, START, WORK = 14.0, 0.5, 12.0          # 주기, 시작, BEFORE가 끝나기까지(= 3분)
    after_work = WORK * 22.8 / 180              # AFTER가 끝나는 시점 — 실제 비율
    RESET0, RESET1 = 13.5, 13.8
    J, POOL = 24, 4
    pc = lambda s: f"{s / C * 100:.2f}%"
    css = ["@media (prefers-reduced-motion:reduce){*{animation:none!important}}",
           f".a{{animation:{C}s linear infinite}}"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="라벨 ZIP 생성 최적화 개념도: 이미지마다 Chromium을 띄우던 순차 처리 3~5분 → 브라우저 풀과 동시성 제어 22.8초">',
           f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           t(40, 48, "라벨 이미지 ZIP 생성 — 참가자 약 1,500명분", 20, c["ink"], 700, 700),
           t(W - 40, 48, "시간은 실제 비율대로 압축 (3분 기준)", 13, c["muted"], 400, anchor="end")]

    # 시간 축: 0 → 3분, 커서가 흐르고 22.8초 지점에 표시
    ax0, ax1, ay = 300, W - 40, 88
    out.append(f'<line x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}" stroke="{c["line"]}" stroke-width="2"/>')
    for sec, lab in ((0, "0"), (60, "1분"), (120, "2분"), (180, "3분")):
        x = ax0 + (ax1 - ax0) * sec / 180
        out.append(f'<line x1="{x:.0f}" y1="{ay - 5}" x2="{x:.0f}" y2="{ay + 5}" stroke="{c["faint"]}"/>')
        out.append(t(x, ay + 22, lab, 12, c["faint"], 60, 500, MONO, anchor="middle"))
    x228 = ax0 + (ax1 - ax0) * 22.8 / 180
    out.append(f'<line x1="{x228:.0f}" y1="{ay - 8}" x2="{x228:.0f}" y2="{ay + 8}" stroke="{c["accent"]}" stroke-width="2"/>')
    out.append(t(x228, ay - 14, "22.8초", 12, c["accent"], 60, 700, MONO, anchor="middle"))
    out.append(t(40, ay + 5, "경과 시간", 13, c["muted"], 200, 500))
    css.append(f"@keyframes cur{{0%,{pc(START)}{{transform:none}}{pc(START + WORK)},{pc(RESET0)}{{transform:translateX({ax1 - ax0}px)}}"
               f"{pc(RESET1)},100%{{transform:none;opacity:0}}}}")
    out.append(f'<g class="a" style="animation-name:cur"><circle cx="{ax0}" cy="{ay}" r="5" fill="{c["ink"]}"/></g>')

    lanes = [dict(y=128, tag="BEFORE", title="이미지마다 Chromium 실행", sub="순차 처리 · 매번 기동 비용",
                  pool=1, slot=WORK / J, result="3~5분", done=START + WORK, tagc=c["faint"]),
             dict(y=258, tag="AFTER", title="브라우저 풀 + 동시성 제어", sub="띄워 둔 브라우저 재사용 · 병렬",
                  pool=POOL, slot=after_work / (J / POOL), result="22.8초", done=START + after_work, tagc=c["accent"])]
    qx, bx0, zx, rx = 310, 520, 800, 930
    for li, L in enumerate(lanes):
        y = L["y"]
        out += [t(40, y + 22, L["tag"], 13, L["tagc"], 200, 700, MONO, extra=' letter-spacing="1"'),
                t(40, y + 50, L["title"], 17, c["ink"], 240, 700),
                t(40, y + 74, L["sub"], 13, c["muted"], 240)]
        if li == 0:
            out.append(f'<line x1="40" y1="{y + 112}" x2="{W - 40}" y2="{y + 112}" stroke="{c["line"]}" stroke-dasharray="4 6"/>')

        # 브라우저: BEFORE는 1개(작업마다 켜졌다 꺼짐), AFTER는 미리 띄워 둔 4개
        if L["pool"] == 1:
            boxes = [(bx0 + 40, y + 10, 140, 76)]
        else:
            boxes = [(bx0 + (k % 2) * 108, y + 4 + (k // 2) * 46, 96, 38) for k in range(POOL)]
        for k, (x, by, w, h) in enumerate(boxes):
            name = f"br{li}_{k}"
            if L["pool"] == 1:  # 작업마다 기동: 켜졌다 꺼지는 깜박임
                ks = [f"0%{{opacity:.15}}"]
                for i in range(J):
                    s0 = START + i * L["slot"]
                    ks += [f"{pc(s0 + .06)}{{opacity:.15}}", f"{pc(s0 + .12)}{{opacity:1}}",
                           f"{pc(s0 + L['slot'] * .85)}{{opacity:1}}", f"{pc(s0 + L['slot'] * .95)}{{opacity:.15}}"]
                ks.append("100%{opacity:.15}")
            else:  # 계속 켜져 있다가 일하는 동안 테두리가 밝아진다
                ks = [f"0%,{pc(START)}{{opacity:.75}}", f"{pc(START + .05)},{pc(L['done'])}{{opacity:1}}",
                      f"{pc(L['done'] + .2)},100%{{opacity:.75}}"]
            css.append(f"@keyframes {name}{{{''.join(ks)}}}")
            out.append(f'<g class="a" style="animation-name:{name}">'
                       f'<rect x="{x}" y="{by}" width="{w}" height="{h}" rx="6" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
                       f'<line x1="{x}" y1="{by + 10}" x2="{x + w}" y2="{by + 10}" stroke="{c["line"]}"/>'
                       + "".join(f'<circle cx="{x + 7 + d * 7}" cy="{by + 5}" r="1.8" fill="{c["faint"]}"/>' for d in range(3))
                       + "</g>")
        label = "Chromium × 작업 수만큼 기동" if L["pool"] == 1 else "Chromium 풀"
        out.append(t(bx0 + 110, y + 104, label, 12, c["faint"], 260, 500, MONO, anchor="middle"))

        # ZIP 상자: 작업이 들어올수록 차오른다
        zy = y + 14
        out.append(f'<rect x="{zx}" y="{zy}" width="80" height="70" rx="8" fill="none" stroke="{c["line"]}" stroke-width="1.5"/>')
        css.append(f"@keyframes zf{li}{{0%,{pc(START)}{{transform:scaleY(0)}}{pc(L['done'])},{pc(RESET0)}{{transform:scaleY(1)}}"
                   f"{pc(RESET1)},100%{{transform:scaleY(0)}}}}")
        out.append(f'<rect class="a" x="{zx + 4}" y="{zy + 4}" width="72" height="62" rx="5" fill="{c["accent"]}" opacity=".25" '
                   f'style="animation-name:zf{li};transform-box:fill-box;transform-origin:50% 100%"/>')
        out.append(t(zx + 40, zy + 42, "ZIP", 14, c["ink"], 60, 700, MONO, anchor="middle"))

        # 결과: 끝나는 순간 나타난다
        css.append(f"@keyframes rs{li}{{0%,{pc(L['done'])}{{opacity:0}}{pc(L['done'] + .25)},{pc(RESET0)}{{opacity:1}}"
                   f"{pc(RESET1)},100%{{opacity:0}}}}")
        out.append(f'<g class="a" style="animation-name:rs{li}">'  # 모션 줄이기에서는 결과가 그대로 보인다
                   + t(rx, y + 58, L["result"], 36, c["accent"] if li else c["ink"], 230, 700)
                   + t(rx, y + 84, "완료" if li else "완료 (서버 상황에 따라)", 13, c["muted"], 230)
                   + "</g>")

        # 작업 카드: 대기열 → 브라우저 → ZIP
        for i in range(J):
            qx_i, qy_i = qx + (i % 6) * 22, y + 18 + (i // 6) * 16
            k, order = (0, i) if L["pool"] == 1 else (i % POOL, i // POOL)
            x, by, w, h = boxes[k]
            bxc, byc = x + w / 2 - 7, by + 10 + (h - 10) / 2 - 5
            s0 = START + order * L["slot"]
            sl = L["slot"]
            mv = lambda px, py: f"transform:translate({px - qx_i:.0f}px,{py - qy_i:.0f}px)"
            frames = [f"0%,{pc(s0)}{{{mv(qx_i, qy_i)};opacity:1}}",
                      f"{pc(s0 + sl * .25)},{pc(s0 + sl * .75)}{{{mv(bxc, byc)};opacity:1}}",
                      f"{pc(s0 + sl * .98)}{{{mv(zx + 33, zy + 30)};opacity:1}}",
                      f"{pc(s0 + sl + .02)},{pc(RESET1)}{{{mv(zx + 33, zy + 30)};opacity:0}}",
                      f"{pc(RESET1 + .01)}{{{mv(qx_i, qy_i)};opacity:0}}",
                      f"100%{{{mv(qx_i, qy_i)};opacity:1}}"]
            css.append(f"@keyframes j{li}_{i}{{{''.join(frames)}}}")
            out.append(f'<rect class="a" x="{qx_i}" y="{qy_i}" width="14" height="10" rx="2" fill="{c["accent"]}" '
                       f'style="animation-name:j{li}_{i}"/>')

    out.append(t(40, H - 18, "개념도 — 동시성 수 · 작업 수는 예시이고, 두 줄이 끝나는 시점의 비율만 실제(3분 기준 vs 22.8초)를 따릅니다.",
                 12, c["faint"], W - 80))
    out.insert(1, f'<style>{"".join(css)}</style>')
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
    import explainers  # 프로젝트별 개념도 — 이 모듈의 t() 등을 쓰므로 여기서 불러온다
    ASSETS.mkdir(exist_ok=True)
    builds = load_builds()
    for mode, c in THEMES.items():
        (ASSETS / f"hero_{mode}.svg").write_text(hero(c, mode), encoding="utf-8")
        (ASSETS / f"buildlog_{mode}.svg").write_text(build_log(c, builds), encoding="utf-8")
        (ASSETS / f"explainer_{mode}.svg").write_text(explainer(c), encoding="utf-8")
        for name, draw in explainers.ALL.items():
            (ASSETS / f"ex_{name}_{mode}.svg").write_text(draw(c, mode), encoding="utf-8")
        for i, d in enumerate(PATHS):
            (ASSETS / f"path_{d['slug']}_{mode}.svg").write_text(path_button(d, c, i * .4), encoding="utf-8")
        for d in CARDS:
            (ASSETS / f"card_{d['slug']}_{mode}.svg").write_text(card(d, c), encoding="utf-8")
    print(f"{len(THEMES) * (len(CARDS) + len(PATHS) + 3 + len(explainers.ALL))} files → {ASSETS}")


if __name__ == "__main__":
    main()

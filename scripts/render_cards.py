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
    dict(slug="safelaw", tag="RAG · PRIVACY · 2026",
         title="SafeLaw 생활법률 RAG",
         sub="로컬 개인정보 마스킹 · 일상어 → 법률 용어 · 근거 검증",
         metric="17/17", note="일상어 질문 Top-5 (초기 10/17)", grow=(10 / 17, 1.0),
         caption="법령 381조 · 판례 50건 · 법령 Recall@5 1.000 · 인용 정확성 1.000"),
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
SCOPE = (180, 100, 92)      # 레이더 스코프: 중심 x, y, 반지름


def _near_seg(x, y, a, b, w):
    """점이 선분 a-b에서 w 이내인가."""
    (ax, ay), (bx, by) = a, b
    dx, dy = bx - ax, by - ay
    k = max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / (dx * dx + dy * dy)))
    return (x - ax - k * dx) ** 2 + (y - ay - k * dy) ** 2 <= w * w


def _on_radar(x, y):
    """레이더 스코프: 바깥 테두리 · 거리 링 둘 · 십자선."""
    cx, cy, r = SCOPE
    d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
    if d > r + 3.5:
        return False
    return (abs(d - r) <= 3.5 or abs(d - r * .66) <= 2.5 or abs(d - r * .33) <= 2.5
            or abs(x - cx) <= 2 or abs(y - cy) <= 2)


# 대한민국: 경위도 윤곽을 등장방형 투영(위도 36° 보정)으로 옮긴 그림용 근사. 작은 섬은 보이게 키운다.
KOREA_LONLAT = [(126.15, 37.75), (126.7, 37.95), (127.1, 38.25), (127.6, 38.3), (128.1, 38.33), (128.35, 38.6),
                (128.6, 38.15), (128.95, 37.75), (129.2, 37.45), (129.35, 37.0), (129.45, 36.6), (129.57, 36.08),
                (129.45, 35.55), (129.25, 35.15), (128.9, 35.05), (128.7, 34.85), (128.2, 34.85), (127.7, 34.72),
                (127.4, 34.5), (126.9, 34.4), (126.53, 34.3), (126.25, 34.5), (126.35, 34.95), (126.45, 35.4),
                (126.6, 35.9), (126.45, 36.35), (126.15, 36.75), (126.5, 36.95), (126.65, 37.35), (126.5, 37.5)]
JEJU = (126.55, 33.38, .40, .19)            # 중심 경도 · 위도, 반경(경도 · 위도)
ULLEUNG, DOKDO = (130.87, 37.50), (131.87, 37.24)
_K, _LON0, _LAT0 = 34.5, 125.95, 38.62


def _proj(lon, lat):
    return 96 + (lon - _LON0) * .81 * _K, 6 + (_LAT0 - lat) * _K


KOREA = [_proj(*p) for p in KOREA_LONLAT]
SEOUL = _proj(126.98, 37.57)
ISLANDS = [_proj(*ULLEUNG), _proj(*DOKDO)]


def _on_korea(x, y):
    jx, jy = _proj(JEJU[0], JEJU[1])
    return (_in_poly(x, y, KOREA) or _in_ellipse(x, y, jx, jy, JEJU[2] * .81 * _K, JEJU[3] * _K)
            or any(_in_circle(x, y, ix, iy, 4.5) for ix, iy in ISLANDS))


NET = [[(90, 50), (90, 100), (90, 150)],                       # 신경망: 층마다 노드 좌표
       [(180, 35), (180, 80), (180, 125), (180, 170)],
       [(270, 75), (270, 125)]]
NET_EDGES = [(a, b) for l in range(len(NET) - 1) for a in NET[l] for b in NET[l + 1]]


def _on_net(x, y):
    """신경망: 노드(원) + 층 사이 연결선."""
    return (any(_in_circle(x, y, nx, ny, 12) for layer in NET for nx, ny in layer)
            or any(_near_seg(x, y, a, b, 2.4) for a, b in NET_EDGES))


def _on_scale(x, y):
    """정의의 저울: 기둥 · 받침 · 가로대 · 꼭대기 장식 · 양쪽 줄과 접시."""
    return (_in_rect(x, y, 176, 36, 184, 182) or _in_rect(x, y, 136, 180, 224, 192)
            or _in_rect(x, y, 78, 36, 282, 44) or _in_circle(x, y, 180, 28, 8)
            or any(_near_seg(x, y, (px, 44), (px + dx, 118), 2.6) for px in (90, 270) for dx in (-34, 34))
            or any(_in_ellipse(x, y, px, 120, 44, 16) and y >= 118 for px in (90, 270)))


SHAPES = {
    "robot": lambda x, y: (_in_rect(x, y, 152, 8, 208, 54) or _in_rect(x, y, 132, 62, 228, 134)
                           or _in_rect(x, y, 102, 66, 122, 128) or _in_rect(x, y, 238, 66, 258, 128)
                           or _in_rect(x, y, 146, 142, 172, 194) or _in_rect(x, y, 188, 142, 214, 194)),
    # 로드스터 옆모습: 바퀴 자리(휠하우스)를 비운 차체 + 링 모양 바퀴 둘
    "car": lambda x, y: ((_in_poly(x, y, CAR_BODY)
                          and not any(_in_circle(x, y, cx, cy, 30) for cx, cy in WHEELS))
                         or any(_in_circle(x, y, cx, cy, 25) and not _in_circle(x, y, cx, cy, 11)
                                for cx, cy in WHEELS)),
    "radar": _on_radar,
    "rocket": lambda x, y: (_in_rect(x, y, 160, 40, 200, 150)
                            or _in_poly(x, y, [(160, 41), (180, 0), (200, 41)])
                            or _in_poly(x, y, [(161, 104), (132, 156), (161, 148)])
                            or _in_poly(x, y, [(199, 104), (228, 156), (199, 148)])),  # 불꽃은 입자가 아니라 효과로 그린다
    "ai": _on_net,
    "scale": _on_scale,
    "korea": _on_korea,
}
MUST = {"korea": ISLANDS}   # 격자 샘플링에서 빠지기 쉬운 작은 섬은 입자를 꼭 하나씩 둔다

# 커리어 단계: (모양, 히어로 하단 트랙에서 밝힐 노드, 캡션). 첫 단계는 기여 달력 그 자체.
CHAPTERS = [
    ("robot", [0], "2017–2019 · 서울로봇고 공업전자기기 — 전국기능경기대회 장려상"),
    ("car", [1], "2021–2024 · 현대자동차그룹 통합사원증 운영 — 임직원 약 12.8만 명"),
    ("radar", [2], "2024–2025 · 공군 방공관제 — 24시간 관제 체계 운용 지원"),
    ("rocket", [3], "2025 · 수양회 백엔드 — 라벨 ZIP 생성 3~5분 → 22.8초"),
    ("ai", [4], "2026 · SSAFY AI 챌린지 — 2차 2위/217팀 · 1차 18위/954명"),
    ("scale", [4], "2026 · SafeLaw — 개인정보 마스킹 · 일상어 → 법률 용어 · RAG"),
    ("korea", [5], "NEXT · 백엔드 · IT 운영 · AI 서비스 — 함께할 팀을 찾습니다"),
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
    if not fill:  # 선으로만 된 모양(레이더 · 저울)은 안쪽 칸이 거의 없다
        k_edge = n
    picked = [(*p, True) for p in pick(edge, k_edge)] + [(*p, False) for p in pick(fill, n - k_edge)]
    for i, (mx, my) in enumerate(MUST.get(shape, [])):
        picked[i] = (mx, my, True)
    rng.shuffle(picked)  # 입자마다 목적지를 섞어야 "모여드는" 움직임이 된다
    return picked


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

    # 머무는 동안의 움직임: 로봇은 춤, 자동차는 주행, 로켓은 떨림, 저울은 기울었다 수평, 지도는 천천히 떠 있기
    idx = {name: k for k, (name, _, _) in enumerate(CHAPTERS, start=1)}

    def seg(name, f0=.2, f1=.58):
        k = idx[name]
        return k * SPAN + SPAN * f0, k * SPAN + SPAN * f1

    def frames(name, values):  # 구간을 고르게 나눠 transform 값을 차례로
        a0, a1 = seg(name)
        return [f"{a0 + (a1 - a0) * i / (len(values) - 1):.2f}%{{transform:{v}}}" for i, v in enumerate(values)]

    mo = ["0%{transform:none}"]
    mo += frames("robot", ["none"] + [f"rotate({(-6, 6)[i % 2]}deg)" for i in range(5)] + ["none"])
    mo += frames("car", ["none", "translateX(16px)", "none"])
    mo += frames("rocket", ["none"] + [f"translate({x}px,{y}px)" for x, y in
                                       ((-2, -2), (2, -3), (-2, -4), (2, -5), (-2, -6), (2, -7), (-1, -4))] + ["none"])
    mo += frames("scale", ["none", "rotate(-4deg)", "rotate(3deg)", "rotate(-1.5deg)", "none"])
    mo += frames("korea", ["none", "translateY(-5px)", "none"])
    mo.append("100%{transform:none}")
    css.append("@keyframes mo{" + "".join(mo) + "}")

    # 효과: 레이더 스윕 · 로켓 불꽃 · 서울 핀 — 줌이 시작되기 전, 머무는 동안만
    for name in ("radar", "rocket", "ai", "scale", "korea"):
        k = idx[name]
        css.append(f"@keyframes fx_{name}{{{_vis(k * SPAN + SPAN * ZOOM_OUT_END, k * SPAN + SPAN * (ZOOM_IN_START - .02))}}}")
    sweep_s = 2.4
    css.append("@keyframes flick{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.3)}}"
               ".flick{animation:flick .18s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 0}"
               "@keyframes pulse{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.8);opacity:0}}"
               ".pulse{animation:pulse 1.4s ease-out infinite;transform-box:fill-box;transform-origin:50% 50%}"
               # 스윕 묶음에 투명한 원을 넣어 묶음 상자의 가운데 = 스코프 중심이 되게 한다
               f"@keyframes rot{{to{{transform:rotate(360deg)}}}}"
               f".rot{{animation:rot {sweep_s}s linear infinite;transform-box:fill-box;transform-origin:50% 50%}}"
               f"@keyframes blip{{0%,100%{{opacity:0}}6%{{opacity:1}}55%{{opacity:.15}}}}"
               f".blip{{animation:blip {sweep_s}s linear infinite;opacity:0}}")
    # 신경망 신호: 입력 → 은닉 → 출력으로 점이 차례로 지나간다
    sig_s, paths = 1.8, [(NET[0][0], NET[1][1], NET[2][0]), (NET[0][2], NET[1][2], NET[2][1]), (NET[0][1], NET[1][0], NET[2][0])]
    S = SCALE
    from math import cos, radians, sin
    rx, ry, rr = (v * S for v in SCOPE)
    wedge = 38
    ex, ey = rx + rr * cos(radians(-wedge)), ry + rr * sin(radians(-wedge))
    blips = [(40, .55), (150, .8), (255, .4)]  # (각도 · 중심에서 거리 비율) — 그림용 접촉점
    fx_top = [f'<g class="fx" style="animation-name:fx_radar">'
              f'<g class="rot"><circle cx="{rx:.0f}" cy="{ry:.0f}" r="{rr:.0f}" fill="none"/>'
              f'<path d="M{rx:.0f} {ry:.0f} L{rx + rr:.0f} {ry:.0f} A{rr:.0f} {rr:.0f} 0 0 0 {ex:.0f} {ey:.0f} Z" fill="{c["accent"]}" opacity=".22"/>'
              f'<line x1="{rx:.0f}" y1="{ry:.0f}" x2="{rx + rr:.0f}" y2="{ry:.0f}" stroke="{c["accent"]}" stroke-width="3" stroke-linecap="round"/></g>'
              + "".join(f'<circle class="blip" cx="{rx + rr * d * cos(radians(a)):.0f}" cy="{ry + rr * d * sin(radians(a)):.0f}" r="6" '
                        f'fill="#3FB950" style="animation-delay:{a / 360 * sweep_s:.2f}s"/>' for a, d in blips)
              + "</g>"]
    sig = []
    for n, (a, b, c3) in enumerate(paths):
        name = f"sig{n}"
        css.append(f"@keyframes {name}{{0%{{transform:translate(0,0);opacity:0}}8%{{opacity:1}}"
                   f"45%{{transform:translate({(b[0] - a[0]) * S:.0f}px,{(b[1] - a[1]) * S:.0f}px)}}"
                   f"90%{{transform:translate({(c3[0] - a[0]) * S:.0f}px,{(c3[1] - a[1]) * S:.0f}px);opacity:1}}100%{{opacity:0}}}}")
        sig.append(f'<circle class="sig" cx="{a[0] * S:.0f}" cy="{a[1] * S:.0f}" r="6" fill="#3FB950" '
                   f'style="animation:{name} {sig_s}s linear {n * sig_s / 3:.2f}s infinite;opacity:0"/>')
    fx_top.append(f'<g class="fx" style="animation-name:fx_ai">{"".join(sig)}</g>')
    # 저울 접시 아래: 왼쪽은 가린 개인정보, 오른쪽은 근거 — 무엇을 재는지
    halo = f' stroke="{c["panel"]}" stroke-width="5" paint-order="stroke" stroke-linejoin="round"'
    chips = [(90, "개인정보 [가림]"), (270, "§ 법령 · 판례 근거")]
    fx_top.append(f'<g class="fx" style="animation-name:fx_scale">'
                  + "".join(f'<rect x="{cx * S - 74:.0f}" y="{142 * S:.0f}" width="148" height="28" rx="14" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
                            + t(cx * S, 142 * S + 19, lab, 13, c["accent"], 140, 700, anchor="middle", extra=halo) for cx, lab in chips)
                  + "</g>")
    px, py = SEOUL[0] * S, SEOUL[1] * S
    pin = "#F0883E"
    fx_top.append(f'<g class="fx" style="animation-name:fx_korea">'
                  f'<circle class="pulse" cx="{px:.0f}" cy="{py:.0f}" r="8" fill="{pin}"/>'
                  f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="{pin}" stroke="{c["panel"]}" stroke-width="2.5"/>'
                  f'<line x1="{px - 8:.0f}" y1="{py - 6:.0f}" x2="{px - 34:.0f}" y2="{py - 26:.0f}" stroke="{pin}" stroke-width="2"/>'
                  # 글자 둘레를 배경색으로 감싸 아래 칸 위에서도 읽히게
                  + t(px - 38, py - 24, "SEOUL", 15, pin, 90, 700, MONO, anchor="end",
                      extra=f' stroke="{c["panel"]}" stroke-width="5" paint-order="stroke" stroke-linejoin="round"') + "</g>")
    # 로켓 불꽃: 기여 칸(파랑)과 섞이지 않게 노즐 아래에 따로 그린다
    fl = lambda w, depth: (f"M{(180 - w) * S:.0f} {152 * S:.0f} Q{180 * S:.0f} {(152 + depth) * S:.0f} "
                           f"{(180 + w) * S:.0f} {152 * S:.0f} Z")
    fx = [f'<g class="fx" style="animation-name:fx_rocket">'
          f'<path class="flick" d="{fl(15, 56)}" fill="#F0883E" opacity=".85"/>'
          f'<path class="flick" d="{fl(8, 36)}" fill="#FFD33D" style="animation-delay:.09s"/></g>']

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
    css.append("@media (prefers-reduced-motion:reduce){.cam,.mo,.p,.cap,.hl,.fx,.cv,.day,.pulse,.flick,.rot,.blip{animation:none}.sig{animation:none!important}"
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


TRACK_SHORT = ["기능경기", "HDS 운영", "공군", "백엔드", "SSAFY · AI", "?"]  # 휴대폰 폭용 짧은 표기


def hero_mobile(c, mode) -> str:
    """휴대폰 폭용 세로 배너: 글자를 위에 크게, 같은 무대를 폭 가득 키워 아래에, 타임라인은 짧게."""
    contrib = load_contrib()
    W, H, PAD = 720, 850, 40
    stage, captions = calendar_swarm(c, RAMP[mode], contrib)
    s = (W - 2 * PAD) / STAGE_W                # 데스크톱 무대를 그대로 키운다
    top = 300
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{escape(HERO["name"])} · {escape(HERO["role"])}">', "",
           f'<rect width="{W}" height="{H}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           t(PAD, 66, "TARGET  ·  " + HERO["target"], 17, c["accent"], W - 2 * PAD, 600, MONO),
           t(PAD, 150, HERO["name"], 64, c["ink"], 300, 700),
           t(PAD + width(HERO["name"], 64) + 20, 150, HERO["name_en"], 26, c["muted"], 300),
           t(PAD, 206, HERO["role"], 32, c["ink"], W - 2 * PAD, 600)]
    for k, line in enumerate(HERO["motto"]):
        out.append(t(PAD, 246 + k * 30, line, 21, c["muted"], W - 2 * PAD))
    out.append(f'<g transform="translate({PAD - STAGE_X * s:.1f},{top - STAGE_Y * s:.1f}) scale({s:.4f})">{stage}{captions}</g>')

    # 타임라인: 연도와 짧은 표기만
    y, x0, x1 = 772, 70, W - 70
    track = HERO["track"]
    step = (x1 - x0) / (len(track) - 1)
    css = []
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["line"]}" stroke-width="2"/>')
    for i, ((year, _), short) in enumerate(zip(track, TRACK_SHORT)):
        x = x0 + step * i
        now, nxt = year == "2026", year == "NEXT"
        dash = ' stroke-dasharray="3 3"' if nxt else ""
        out.append(f'<circle cx="{x:.0f}" cy="{y}" r="7" fill="{c["accent"] if now else c["bg"]}" '
                   f'stroke="{c["accent"] if now else c["faint"]}" stroke-width="2"{dash}/>')
        out.append(t(x, y + 34, year, 18, c["ink"] if now else c["muted"], step - 8, 700 if now else 600, MONO, anchor="middle"))
        out.append(t(x, y + 58, short, 14, c["ink"] if now else c["muted"], step - 8, 500, anchor="middle"))
        lit = [k for k, (_, nodes, _) in enumerate(CHAPTERS, start=1) if i in nodes]
        if lit:
            st = lit[0] * SPAN
            css.append(f"@keyframes hl{i}{{{_vis(st + SPAN * ZOOM_OUT_END, st + SPAN * .9)}}}")
            out.append(f'<g class="hl" style="animation-name:hl{i}">'
                       f'<circle cx="{x:.0f}" cy="{y}" r="15" fill="{c["accent"]}" opacity=".18"/>'
                       f'<circle cx="{x:.0f}" cy="{y}" r="7" fill="{c["accent"]}"/></g>')
    out[1] = f'<style>{"".join(css)}</style>'
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

    # 늘어나는 막대: 개선 전 비율에서 개선 후 비율까지 자란다
    if "grow" in d:
        g0, g1 = d["grow"]
        by = 198
        out.insert(1, f"<style>{loop}</style>")
        out.append(f'<rect x="{P}" y="{by}" width="{room}" height="6" rx="3" fill="{c["track"]}"/>')
        out.append(f'<rect class="go" x="{P}" y="{by}" width="{room * g1:.1f}" height="6" rx="3" '
                   f'fill="{c["accent"]}" style="--from:scaleX({g0 / g1:.3f});transform-origin:0 50%"/>')

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


# ── 기술 스택 키보드: 실제 65% 배치(68키). 글자 키 자리에 기술 로고 키캡을 꽂는다 ─────────────────────
# 윗줄 Q~P = 주력(파란 키), 가운데 A~L · 아랫줄 Z~B = 써 본 기술(흰 키 + 파란 로고), 나머지는 평범한 키.

ICONS = ROOT / "data" / "simple-icons.json"   # simple-icons(CC0) 경로를 버전 고정해 저장해 둔 것
MAIN_TECH = [("Java", "openjdk"), ("Node.js", "nodedotjs"), ("Express", "express"), ("TypeScript", "typescript"),
             ("PostgreSQL", "postgresql"), ("MSSQL", None), ("Python", "python"), ("PyTorch", "pytorch"),
             ("vLLM", "vllm"), ("Playwright", None)]
USED_TECH = [("Spring Boot", "springboot"), ("FastAPI", "fastapi"), ("Chroma", None), ("Hugging Face", "huggingface"),
             ("LangChain", "langchain"), ("LangGraph", "langgraph"), ("AWS", None), ("Docker", "docker"), ("Git", "git"),
             ("Next.js", "nextdotjs"), ("Vue 3", "vuedotjs"), ("Streamlit", "streamlit"), ("C", "c"), ("ATmega128", None)]
MONOGRAM = {"MSSQL": "SQL", "Chroma": "Ch", "Playwright": "PW", "AWS": "aws", "ATmega128": "AVR"}
KEY_LABEL = {"Hugging Face": "HuggingFace"}   # 1u 키에 들어가도록 줄인 표기
SPACEBAR = "김진영 · 운영을 아는 백엔드 개발자"
# 65% 배치: (글자, 폭(u), 종류) — 종류 mod = 기능 키, key = 글자 키, space = 스페이스바
LAYOUT = [
    [("Esc", 1, "mod")] + [(ch, 1, "key") for ch in "1234567890-="] + [("⌫", 2, "mod"), ("Del", 1, "mod")],
    [("Tab", 1.5, "mod")] + [(ch, 1, "key") for ch in "QWERTYUIOP[]"] + [("\\", 1.5, "key"), ("PgUp", 1, "mod")],
    [("Caps", 1.75, "mod")] + [(ch, 1, "key") for ch in "ASDFGHJKL;'"] + [("Enter", 2.25, "mod"), ("PgDn", 1, "mod")],
    [("Shift", 2.25, "mod")] + [(ch, 1, "key") for ch in "ZXCVBNM,./"] + [("Shift", 1.75, "mod"), ("↑", 1, "mod"), ("End", 1, "mod")],
    [("Ctrl", 1.25, "mod"), ("Win", 1.25, "mod"), ("Alt", 1.25, "mod"), (SPACEBAR, 6.25, "space"), ("Alt", 1, "mod"),
     ("Fn", 1, "mod"), ("Ctrl", 1, "mod"), ("←", 1, "mod"), ("↓", 1, "mod"), ("→", 1, "mod")],
]
TECH_AT = {**dict(zip("QWERTYUIOP", [(n, s, True) for n, s in MAIN_TECH])),
           **dict(zip("ASDFGHJKLZXCVB", [(n, s, False) for n, s in USED_TECH]))}
KEYS = {  # 윗면 그라데이션(위 → 아래), 옆면, 글자
    "light": dict(case=("#D8DEE4", "#AFB8C1"), main=("#3B8EF7", "#0969DA", "#0550AE", "#FFFFFF"),
                  key=("#FFFFFF", "#EEF1F4", "#C4CBD3", "#57606A"), mod=("#C9D1D9", "#B6BFC8", "#8C959F", "#24292F")),
    "dark": dict(case=("#010409", "#30363D"), main=("#4C9AFF", "#1F6FEB", "#0D419D", "#FFFFFF"),
                 key=("#373E47", "#2D333B", "#161B22", "#ADBAC7"), mod=("#22272E", "#1C2128", "#0D1117", "#768390")),
}


def keycaps(c, mode) -> str:
    import json
    icons = json.loads(ICONS.read_text(encoding="utf-8"))
    k = KEYS[mode]
    W, U, GAP, KH = 1200, 68, 6, 60
    kb_w = 16 * U                              # 한 줄이 16u
    PX, PY = (W - kb_w) // 2, 92               # 첫 키 위치
    css = ["@keyframes press{0%,3%,100%{transform:none}1.5%{transform:translateY(3px)}}",
           ".tap{animation:press 9s ease-in-out infinite}",
           "@keyframes led{0%,100%{opacity:1}50%{opacity:.35}}",
           "@media (prefers-reduced-motion:reduce){.tap,.led{animation:none}}"]
    defs = "".join(f'<linearGradient id="g{kind}" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop offset="0" stop-color="{k[kind][0]}"/><stop offset="1" stop-color="{k[kind][1]}"/></linearGradient>'
                   for kind in ("main", "key", "mod"))
    out = []
    taps = [ch for ch in "QWERTYUIOPASDFGHJKLZXCVB"] + ["space"]  # 타자 치듯 눌리는 순서

    def cap(x, y, w, kind, inner, tap=None):
        _, _, side, _ = k[kind]
        border = f' stroke="{c["line"]}"' if kind == "key" and mode == "light" else ""
        anim = f' class="tap" style="animation-delay:{taps.index(tap) * .28:.2f}s"' if tap in taps else ""
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{KH}" rx="8" fill="{side}"{border}/>'
                   f'<g{anim}><rect x="{x + 4:.0f}" y="{y + 3}" width="{w - 8:.0f}" height="{KH - 13}" rx="7" fill="url(#g{kind})"/>'
                   f'<rect x="{x + 8:.0f}" y="{y + 5}" width="{w - 16:.0f}" height="2" rx="1" fill="#FFFFFF" opacity=".22"/>'
                   + inner + "</g>")

    for r, row in enumerate(LAYOUT):
        y = PY + r * (KH + GAP)
        x = PX
        for label, units, kind in row:
            w = units * U - GAP
            cx = x + w / 2
            tech = TECH_AT.get(label) if kind == "key" else None
            if tech:
                name, slug, main = tech
                face = "main" if main else "key"
                ink = k["main"][3] if main else c["accent"]
                if slug:
                    logo = f'<path transform="translate({cx - 10:.1f},{y + 9}) scale(.833)" d="{icons[slug]}" fill="{ink}"/>'
                else:
                    mono = MONOGRAM[name]
                    logo = (f'<rect x="{cx - 11:.1f}" y="{y + 8}" width="22" height="22" rx="5" fill="none" stroke="{ink}" stroke-width="1.6"/>'
                            + t(cx, y + 23, mono, 8.5 if len(mono) > 2 else 10, ink, 22, 700, MONO, anchor="middle"))
                cap(x, y, w, face, logo + t(cx, y + 44, KEY_LABEL.get(name, name), 8, ink, w - 6, 700, anchor="middle"), tap=label)
            elif kind == "space":
                cap(x, y, w, "key", t(cx, y + 30, label, 14, c["accent"], w - 30, 700, anchor="middle"), tap="space")
            else:
                face = "mod" if kind == "mod" else "key"
                cap(x, y, w, face, t(x + 9, y + 21, label, 11 if kind == "mod" else 12, k[face][3], w - 14, 600, MONO))
            x += units * U
    kb_h = 5 * (KH + GAP) - GAP
    case_x, case_y = PX - 22, PY - 22
    case_w, case_h = kb_w - GAP + 44, kb_h + 44
    H = case_y + case_h + 26
    # 키보드 오른쪽 위 표시등(Caps · Num · Scroll) — 하나만 천천히 깜박
    leds = "".join(f'<circle cx="{case_x + case_w - 74 + i * 22}" cy="{case_y - 14}" r="4" fill="{c["accent"] if i == 0 else c["line"]}"'
                   + (' class="led" style="animation:led 2.4s ease-in-out infinite"' if i == 0 else "") + "/>" for i in range(3))
    legend = (f'<rect x="40" y="{case_y - 22}" width="14" height="14" rx="3" fill="{k["main"][1]}"/>'
              + t(60, case_y - 10, "주력 · 수치로 결과를 낸 기술 (Q~P)", 13, c["muted"], 300, 600)
              + f'<rect x="330" y="{case_y - 22}" width="14" height="14" rx="3" fill="{k["key"][0]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
              + t(350, case_y - 10, "써 본 기술 (A~L · Z~B)", 13, c["muted"], 260, 600))
    names = ("기술 스택 키보드. 주력(Q~P, 파란 키): " + ", ".join(n for n, _ in MAIN_TECH)
             + ". 써 본 기술(A~L, Z~B): " + ", ".join(n for n, _ in USED_TECH) + f". 스페이스바: {SPACEBAR}")
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
                      f'role="img" aria-label="{escape(names)}">', f"<style>{''.join(css)}</style>", f"<defs>{defs}</defs>",
                      f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
                      legend, leds,
                      f'<rect x="{case_x}" y="{case_y}" width="{case_w}" height="{case_h}" rx="18" fill="{k["case"][0]}" '
                      f'stroke="{k["case"][1]}" stroke-width="2"/>',
                      *out, "</svg>"])


def macropad(c, mode) -> str:
    """휴대폰 폭용: 기술 키 24개만 4열 매크로패드로. 주력 10개(파란 키)를 먼저, 써 본 기술 14개를 이어서."""
    import json
    icons = json.loads(ICONS.read_text(encoding="utf-8"))
    k = KEYS[mode]
    W, PAD, COLS, GAP, KH = 720, 40, 4, 12, 96
    case_pad = 20
    kw = (W - 2 * PAD - 2 * case_pad - GAP * (COLS - 1)) / COLS
    keys = [(n, sl, True) for n, sl in MAIN_TECH] + [(n, sl, False) for n, sl in USED_TECH]
    rows = -(-len(keys) // COLS)
    top = 92
    case_h = rows * (KH + GAP) - GAP + 2 * case_pad
    H = top + case_h + 30
    defs = "".join(f'<linearGradient id="g{kind}" x1="0" y1="0" x2="0" y2="1">'
                   f'<stop offset="0" stop-color="{k[kind][0]}"/><stop offset="1" stop-color="{k[kind][1]}"/></linearGradient>'
                   for kind in ("main", "key"))
    css = ("@keyframes press{0%,3%,100%{transform:none}1.5%{transform:translateY(3px)}}"
           ".tap{animation:press 9s ease-in-out infinite}"
           "@media (prefers-reduced-motion:reduce){.tap{animation:none}}")
    out = []
    for i, (name, slug, main) in enumerate(keys):
        x = PAD + case_pad + (i % COLS) * (kw + GAP)
        y = top + case_pad + (i // COLS) * (KH + GAP)
        face = "main" if main else "key"
        _, _, side, _ = k[face]
        ink = k["main"][3] if main else c["accent"]
        cx = x + kw / 2
        border = f' stroke="{c["line"]}"' if face == "key" and mode == "light" else ""
        if slug:
            logo = f'<path transform="translate({cx - 16:.1f},{y + 14}) scale(1.333)" d="{icons[slug]}" fill="{ink}"/>'
        else:
            mono = MONOGRAM[name]
            logo = (f'<rect x="{cx - 17:.1f}" y="{y + 13}" width="34" height="34" rx="7" fill="none" stroke="{ink}" stroke-width="2"/>'
                    + t(cx, y + 35, mono, 13 if len(mono) > 2 else 15, ink, 34, 700, MONO, anchor="middle"))
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{kw:.0f}" height="{KH}" rx="12" fill="{side}"{border}/>'
                   f'<g class="tap" style="animation-delay:{i * .28:.2f}s">'
                   f'<rect x="{x + 5:.0f}" y="{y + 4}" width="{kw - 10:.0f}" height="{KH - 15}" rx="10" fill="url(#g{face})"/>'
                   f'<rect x="{x + 10:.0f}" y="{y + 6}" width="{kw - 20:.0f}" height="2" rx="1" fill="#FFFFFF" opacity=".22"/>'
                   + logo + t(cx, y + 70, name, 16, ink, kw - 12, 700, anchor="middle") + "</g>")
    legend = (f'<rect x="{PAD}" y="40" width="16" height="16" rx="3" fill="{k["main"][1]}"/>'
              + t(PAD + 24, 54, "주력 · 수치로 결과를 낸 기술", 16, c["muted"], 300, 600)
              + f'<rect x="{PAD + 330}" y="40" width="16" height="16" rx="3" fill="{k["key"][0]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
              + t(PAD + 354, 54, "써 본 기술", 16, c["muted"], 200, 600))
    names = ("기술 스택. 주력: " + ", ".join(n for n, _ in MAIN_TECH) + ". 써 본 기술: " + ", ".join(n for n, _ in USED_TECH))
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
                      f'role="img" aria-label="{escape(names)}">', f"<style>{css}</style>", f"<defs>{defs}</defs>",
                      f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
                      legend,
                      f'<rect x="{PAD}" y="{top}" width="{W - 2 * PAD}" height="{case_h}" rx="18" fill="{k["case"][0]}" '
                      f'stroke="{k["case"][1]}" stroke-width="2"/>',
                      *out, "</svg>"])


def main():
    import explainers  # 프로젝트별 개념도 — 이 모듈의 t() 등을 쓰므로 여기서 불러온다
    ASSETS.mkdir(exist_ok=True)
    for mode, c in THEMES.items():
        (ASSETS / f"hero_{mode}.svg").write_text(hero(c, mode), encoding="utf-8")
        (ASSETS / f"stack_{mode}.svg").write_text(keycaps(c, mode), encoding="utf-8")
        # 휴대폰 폭(README의 <picture media="(max-width: 600px)">)용
        (ASSETS / f"hero_mobile_{mode}.svg").write_text(hero_mobile(c, mode), encoding="utf-8")
        (ASSETS / f"stack_mobile_{mode}.svg").write_text(macropad(c, mode), encoding="utf-8")
        (ASSETS / f"explainer_{mode}.svg").write_text(explainer(c), encoding="utf-8")
        for name, draw in explainers.ALL.items():
            (ASSETS / f"ex_{name}_{mode}.svg").write_text(draw(c, mode), encoding="utf-8")
        for i, d in enumerate(PATHS):
            (ASSETS / f"path_{d['slug']}_{mode}.svg").write_text(path_button(d, c, i * .4), encoding="utf-8")
        for d in CARDS:
            (ASSETS / f"card_{d['slug']}_{mode}.svg").write_text(card(d, c), encoding="utf-8")
    print(f"{len(THEMES) * (len(CARDS) + len(PATHS) + 5 + len(explainers.ALL))} files → {ASSETS}")


if __name__ == "__main__":
    main()

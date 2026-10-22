"""프로필 README용 SVG(히어로 배너 · 프로젝트 카드)를 라이트/다크 두 벌로 생성한다.

    python scripts/render_cards.py

수치를 바꿀 때는 아래 CARDS만 고치고 다시 실행하면 assets/ 가 갱신된다.
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
    motto="느린 곳은 먼저 재고, 숫자로 고치고, 결과는 직접 만든 기준으로 검증합니다.",
    target="백엔드 개발 · IT 시스템 운영 · AI 서비스",
    track=[("2019", "기능경기대회"), ("2021", "HDS 시스템 운영"), ("2024", "공군 관제 체계"),
           ("2025", "수양회 백엔드"), ("2026", "SSAFY 16기 · AI")],
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


# ── 코드 스웜: 코드 조각이 모여 자동차 → 로봇 → 로켓이 되는 히어로 애니메이션 ──────────────
# 스테이지 로컬 좌표 360×200. 각 모양은 "점이 이 안에 있나"로 정의하고 격자로 샘플링한다.

STAGE_X, STAGE_Y, STAGE_W, STAGE_H = 790, 22, 360, 200
CYCLE = 18  # 초
TOKENS = ["{", "}", "<>", "=>", "fn", "0", "1", ";", "//", "[]", "()", "if", "&&", "λ", "#", "::", "$", "*"]
N_PARTICLES = 120


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


def _in_rect(x, y, x0, y0, x1, y1):
    return x0 <= x <= x1 and y0 <= y <= y1


CAR_BODY = [(16, 148), (26, 120), (118, 106), (165, 78), (238, 78), (290, 110), (342, 118), (350, 148)]
WHEELS = [(92, 168), (282, 168)]

SHAPES = {
    # 로드스터 옆모습: 바퀴 자리(휠하우스)를 비운 차체 + 링 모양 바퀴 둘
    "car": lambda x, y: ((_in_poly(x, y, CAR_BODY)
                          and not any(_in_circle(x, y, cx, cy, 30) for cx, cy in WHEELS))
                         or any(_in_circle(x, y, cx, cy, 25) and not _in_circle(x, y, cx, cy, 11)
                                for cx, cy in WHEELS)),
    "robot": lambda x, y: (_in_rect(x, y, 152, 8, 208, 54) or _in_rect(x, y, 132, 62, 228, 134)
                           or _in_rect(x, y, 102, 66, 122, 128) or _in_rect(x, y, 238, 66, 258, 128)
                           or _in_rect(x, y, 146, 142, 172, 194) or _in_rect(x, y, 188, 142, 214, 194)),
    "rocket": lambda x, y: (_in_rect(x, y, 160, 40, 200, 150)
                            or _in_poly(x, y, [(160, 41), (180, 0), (200, 41)])
                            or _in_poly(x, y, [(161, 104), (132, 156), (161, 148)])
                            or _in_poly(x, y, [(199, 104), (228, 156), (199, 148)])
                            or _in_poly(x, y, [(166, 156), (194, 156), (180, 198)])),
}


def _sample(shape, n, rng):
    """(x, y, 외곽선 여부) n개. 외곽선을 먼저 채워 실루엣을 또렷하게, 남는 입자로 안쪽을 채운다."""
    fn, g = SHAPES[shape], 8
    inside = [(x, y) for y in range(-4, STAGE_H + 5, g) for x in range(-4, STAGE_W + 5, g) if fn(x, y)]
    edge = [(x, y) for x, y in inside
            if not all(fn(x + dx, y + dy) for dx, dy in ((g, 0), (-g, 0), (0, g), (0, -g)))]
    fill = [p for p in inside if p not in edge]

    def even(pts, k):  # 무작위로 솎아낸다 — 래스터 순서로 일정 간격을 뽑으면 세로 줄무늬가 생긴다
        if k <= len(pts):
            return rng.sample(pts, k)
        return pts + [rng.choice(pts) for _ in range(k - len(pts))]

    k_edge = min(len(edge), int(n * 0.78))
    picked = [(*p, True) for p in even(edge, k_edge)] + [(*p, False) for p in even(fill, n - k_edge)]
    rng.shuffle(picked)  # 입자마다 목적지를 섞어야 "모여드는" 움직임이 된다
    return picked


def _scatter(n, rng):
    return [(rng.uniform(-10, STAGE_W + 10), rng.uniform(-6, STAGE_H + 6)) for _ in range(n)]


def code_swarm(c) -> str:
    import random
    rng = random.Random(1647)
    car, robot, rocket = (_sample(s, N_PARTICLES, rng) for s in ("car", "robot", "rocket"))
    s0, s1, s2 = (_scatter(N_PARTICLES, rng) for _ in range(3))

    css = [f".p{{font:600 11px {MONO};fill:{c['accent']};"
           f"animation:{CYCLE}s cubic-bezier(.55,0,.25,1) infinite both}}",
           f".stage{{animation:stage {CYCLE}s ease-in-out infinite;transform-origin:180px 120px}}",
           f".lbl{{font:500 12px {MONO};fill:{c['muted']};opacity:0;animation:{CYCLE}s linear infinite}}",
           # 단계: 흩어짐 → 자동차(주행) → 흩어짐 → 로봇(춤) → 흩어짐 → 로켓(발사, 위로 빠져나감) → 반복
           "@keyframes stage{0%,14%{transform:none}20%{transform:translateX(16px)}26%{transform:translateX(-10px)}"
           "30%,42%{transform:none}45%{transform:rotate(-7deg) translateY(-6px)}48%{transform:rotate(7deg)}"
           "51%{transform:rotate(-7deg) translateY(-6px)}54%{transform:rotate(7deg)}"
           "57%{transform:rotate(-4deg) translateY(-4px)}60%,76%{transform:none}"
           "78%{transform:translateX(-2px)}79%{transform:translateX(2px)}80%{transform:translateX(-1px)}"
           "90%{transform:translateY(-300px)}93%{transform:translateY(-300px)}94%,100%{transform:none}}",
           "@keyframes l0{0%,9%{opacity:0}13%,28%{opacity:1}31%,100%{opacity:0}}",
           "@keyframes l1{0%,37%{opacity:0}41%,60%{opacity:1}63%,100%{opacity:0}}",
           "@keyframes l2{0%,69%{opacity:0}73%,90%{opacity:1}92%,100%{opacity:0}}",
           "@media (prefers-reduced-motion:reduce){.p,.stage,.lbl{animation:none}.lbl0{opacity:1}}"]

    css.append("@keyframes sp{0%,14%{opacity:0;transform:none}18%{opacity:.9}24%{opacity:.9;transform:translateX(-24px)}"
               "28%,100%{opacity:0;transform:translateX(-40px)}}"
               "@keyframes ex{0%,75%{opacity:0}77%,89%{opacity:1}90%,100%{opacity:0}}"
               "@keyframes fl{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.35)}}"
               ".sp{animation:sp 18s linear infinite;opacity:0}"
               ".ex{animation:ex 18s linear infinite;opacity:0}"
               ".fl{animation:fl .18s ease-in-out infinite;transform-box:fill-box;transform-origin:50% 0}")

    # 배경 → 앞: 속도선(자동차), 불꽃(로켓), 코드 입자
    sp = c["faint"]
    body = [f'<g class="sp" stroke="{sp}" stroke-width="2" stroke-linecap="round">'
            f'<line x1="-30" y1="100" x2="0" y2="100"/><line x1="-50" y1="124" x2="-4" y2="124"/>'
            f'<line x1="-24" y1="146" x2="2" y2="146"/></g>',
            '<g class="ex"><path class="fl" d="M168 198 Q180 236 192 198 Z" fill="#F0883E" opacity=".55"/>'
            '<path class="fl" d="M173 198 Q180 222 187 198 Z" fill="#FFD33D" opacity=".8"/></g>']
    for i in range(N_PARTICLES):
        bx, by, _ = car[i]  # 애니메이션이 꺼지면 자동차 모양으로 서 있도록 기준점을 자동차에 둔다
        j = rng.uniform(0, 3)  # 입자마다 도착 시각을 살짝 어긋나게
        flame = rocket[i][1] > 152  # 로켓 아래 삼각형(불꽃) 자리는 주황색

        def at(p, pt, op=None, fill=None):
            dx, dy = pt[0] - bx, pt[1] - by
            if op is None:  # 외곽선 입자는 진하게, 안쪽 입자는 흐리게 — 입체감
                op = 1 if len(pt) < 3 or pt[2] else 0.4
            # 불꽃 입자는 모든 키프레임에 색을 박아야 한다 — 일부에만 있으면 타임라인 전체에서 보간된다
            f = f";fill:{fill or c['accent']}" if flame else ""
            return f"{p:.1f}%{{transform:translate({dx:.0f}px,{dy:.0f}px);opacity:{op}{f}}}"

        orange = "#F0883E" if flame else None
        frames = [at(0, s0[i], .55), at(4 + j, s0[i], .55),
                  at(11 + j, car[i]), at(30, car[i]),
                  at(34 + j / 2, s1[i], .55), at(38 + j, robot[i]), at(61, robot[i]),
                  at(64 + j / 2, s2[i], .55), at(70 + j, rocket[i], fill=orange), at(88, rocket[i], fill=orange),
                  at(90, rocket[i], 0, orange), at(94, s0[i], 0), at(100, s0[i], .55)]
        css.append(f"@keyframes k{i}{{{''.join(frames)}}}")
        body.append(f'<text class="p" x="{bx}" y="{by}" text-anchor="middle" dominant-baseline="central" '
                    f'style="animation-name:k{i}">{escape(TOKENS[i % len(TOKENS)])}</text>')

    labels = "".join(
        f'<text class="lbl lbl{k}" x="{STAGE_W / 2}" y="{STAGE_H + 30}" text-anchor="middle" '
        f'style="animation-name:l{k}">{escape(s)}</text>'
        for k, s in enumerate(["$ build car    // 달리고", "$ build robot  // 춤추고", "$ build rocket // 날아간다"]))

    return (f'<style>{"".join(css)}</style>'
            f'<clipPath id="stageclip"><rect x="{STAGE_X - 40}" y="1" width="{STAGE_W + 80}" height="300"/></clipPath>'
            f'<g clip-path="url(#stageclip)"><g transform="translate({STAGE_X},{STAGE_Y})">'
            f'<g class="stage">{"".join(body)}</g>{labels}</g></g>')


def hero(c) -> str:
    W, H = 1200, 330
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="{escape(HERO["name"])} · {escape(HERO["role"])}">',
           f'<rect width="{W}" height="{H}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
           code_swarm(c),
           # 왼쪽 글은 스테이지(x≥750)를 넘지 않게 폭을 제한한다
           t(56, 72, "TARGET  ·  " + HERO["target"], 15, c["accent"], 680, 600, MONO),
           t(56, 140, HERO["name"], 56, c["ink"], 300, 700),
           t(56 + width(HERO["name"], 56) + 20, 140, HERO["name_en"], 22, c["muted"], 300),
           t(56, 186, HERO["role"], 26, c["ink"], 680, 600),
           t(56, 220, HERO["motto"], 17, c["muted"], 680)]

    # 걸어온 길: 하단 가로 트랙, 마지막(현재) 지점만 강조색
    y, x0, x1 = 268, 72, W - 120
    step = (x1 - x0) / (len(HERO["track"]) - 1)
    out.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{c["line"]}" stroke-width="2"/>')
    for i, (year, label) in enumerate(HERO["track"]):
        x = x0 + step * i
        last = i == len(HERO["track"]) - 1
        dot = c["accent"] if last else c["bg"]
        ring = c["accent"] if last else c["faint"]
        out.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{dot}" stroke="{ring}" stroke-width="2"/>')
        out.append(t(x, y + 30, f"{year}  {label}", 14, c["ink"] if last else c["muted"], step - 12,
                     600 if last else 400, anchor="middle"))
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
SHAPE_NAMES = {"car": "car", "robot": "robot", "rocket": "rocket"}


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
            out.append(t(tx, y, f"{SHAPE_NAMES[b['shape']]:<7}", 15, c["accent"], 90, 600, MONO, extra=' xml:space="preserve"'))
            out.append(t(tx + 90, y, "@" + b["user"], 15, c["ink"], 400, 400, MONO))
            out.append(t(W - 50, y, b["at"], 15, c["faint"], 140, 400, MONO, anchor="end"))
    else:
        out.append(t(tx, 132, "(아직 빌드 기록이 없어요)", 15, c["muted"], 600, 400, MONO))
        out.append(t(tx, 160, "아래 버튼으로 첫 번째 빌더가 되어주세요", 15, c["muted"], 600, 400, MONO))

    n = builds["counts"]
    total = sum(n.values())
    summary = f"car {n['car']} · robot {n['robot']} · rocket {n['rocket']}  ·  total {total}"
    out.append(t(tx, H - 34, summary, 14, c["muted"], 680, 500, MONO))
    out.append("</svg>")
    return "\n".join(out)


def main():
    ASSETS.mkdir(exist_ok=True)
    builds = load_builds()
    for mode, c in THEMES.items():
        (ASSETS / f"hero_{mode}.svg").write_text(hero(c), encoding="utf-8")
        (ASSETS / f"buildlog_{mode}.svg").write_text(build_log(c, builds), encoding="utf-8")
        for d in CARDS:
            (ASSETS / f"card_{d['slug']}_{mode}.svg").write_text(card(d, c), encoding="utf-8")
    print(f"{len(THEMES) * (len(CARDS) + 2)} files → {ASSETS}")


if __name__ == "__main__":
    main()

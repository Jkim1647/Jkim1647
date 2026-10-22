"""장애 대응 시뮬레이터(incident.md)와 화면별 장면 SVG를 함께 만든다.

    python scripts/incident.py

화면 내용은 아래 SCREENS 하나에 모여 있다. 이야기와 수치는 portfolio 저장소의 프로젝트 문서 기준이고,
장면 속 그래프 모양 · 칸 배치 같은 그림 요소는 분위기를 위한 개념도다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from render_cards import MONO, THEMES, t, width

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "incident"
MD = ROOT / "incident.md"
W = 1200
TONE = {"light": dict(ok="#1A7F37", warn="#CF222E", amber="#9A6700"),
        "dark": dict(ok="#3FB950", warn="#F85149", amber="#D29922")}
SPACER = "<br/>" * 50  # 다음 화면 제목이 미리 보여 답을 흘리지 않게


def wrap(text, size, room):
    """글자 폭 추정으로 줄을 나눈다(공백 기준)."""
    lines, cur = [], ""
    for word in text.split(" "):
        cand = f"{cur} {word}".strip()
        if width(cand, size) <= room or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


class Scene:
    """장면 하나: 위쪽 HUD(시나리오 · 단계 · 상태등) + 본문 + 반복 애니메이션."""

    def __init__(self, c, tn, hud, step, status, tone, blink=False, cycle=8.0, H=300):
        self.c, self.tn, self.C, self.H = c, tn, cycle, H
        self.css = [f".a{{animation:{cycle}s linear infinite}}",
                    "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.2}}",
                    ".blink{animation:blink 1s infinite}"]
        col = tn[tone] if tone in tn else c["accent"]
        pill_w = width(status, 13) * .9 + 44
        self.out = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="{c["panel"]}" stroke="{c["line"]}"/>',
                    f'<rect x="1" y="1" width="{W - 2}" height="44" rx="16" fill="{c["bg"]}"/>',
                    f'<line x1="1" y1="45" x2="{W - 1}" y2="45" stroke="{c["line"]}"/>',
                    f'<rect x="1" y="1" width="6" height="{H - 2}" rx="3" fill="{col}"/>',
                    t(32, 29, hud, 13, col, 600, 700, MONO, extra=' letter-spacing="1"'),
                    t(W - 60 - pill_w, 29, step, 13, c["muted"], 200, 600, MONO, anchor="end"),
                    f'<g class="{"blink" if blink else ""}">'
                    f'<rect x="{W - 28 - pill_w:.0f}" y="12" width="{pill_w:.0f}" height="22" rx="11" fill="{col}" opacity=".15"/>'
                    f'<circle cx="{W - 28 - pill_w + 14:.0f}" cy="23" r="4" fill="{col}"/>'
                    + t(W - 28 - pill_w + 26, 28, status, 13, col, pill_w, 700, MONO) + "</g>"]
        self.n = 0

    def pc(self, s):
        return f"{max(0.0, min(100.0, s / self.C * 100)):.2f}%"

    def _name(self):
        self.n += 1
        return f"k{self.n}"

    def appear(self, svg, t0, t1=None):
        """t0초에 나타나 t1초(기본: 주기 끝 직전)까지 보인다. 모션 줄이기에서는 그냥 보인다."""
        t1 = self.C - .4 if t1 is None else t1
        name = self._name()
        self.css.append(f"@keyframes {name}{{0%,{self.pc(t0 - .01)}{{opacity:0}}{self.pc(t0 + .15)},{self.pc(t1)}{{opacity:1}}"
                        f"{self.pc(t1 + .2)},100%{{opacity:0}}}}")
        self.out.append(f'<g class="a" style="animation-name:{name}">{svg}</g>')

    def text(self, *a, **k):
        return t(*a, **k)

    def chart(self, x, y, w, h, ys, color, t0=.3, t1=2.6, label=None, marks=()):
        c = self.c
        if label:
            self.out.append(t(x, y - 10, label, 13, c["muted"], w, 600))
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["bg"]}" stroke="{c["line"]}"/>')
        for g in (.33, .66):
            self.out.append(f'<line x1="{x + 8}" y1="{y + h * g:.0f}" x2="{x + w - 8}" y2="{y + h * g:.0f}" stroke="{c["track"]}"/>')
        pts = [(x + 14 + (w - 28) * i / (len(ys) - 1), y + h - 12 - (h - 24) * v) for i, v in enumerate(ys)]
        L = sum(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** .5 for a, b in zip(pts, pts[1:]))
        d = "M" + " L".join(f"{px:.0f} {py:.0f}" for px, py in pts)
        name = self._name()
        self.css.append(f"@keyframes {name}{{0%,{self.pc(t0)}{{stroke-dashoffset:{L:.0f}}}{self.pc(t1)},{self.pc(self.C - .4)}{{stroke-dashoffset:0}}"
                        f"100%{{stroke-dashoffset:{L:.0f}}}}}")
        self.out.append(f'<path class="a" d="{d}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" '
                        f'stroke-linejoin="round" stroke-dasharray="{L:.0f}" style="animation-name:{name}"/>')
        for i, lab in marks:  # 세로 표시선(예: 재시작 시점)
            mx = pts[i][0]
            self.appear(f'<line x1="{mx:.0f}" y1="{y + 6}" x2="{mx:.0f}" y2="{y + h - 6}" stroke="{c["faint"]}" stroke-dasharray="4 4"/>'
                        + t(mx + 6, y + 20, lab, 12, c["muted"], 120, 600, MONO), t0 + (t1 - t0) * i / (len(ys) - 1))

    def terminal(self, x, y, w, title, lines, t0=.4, step=.7):
        c, tn = self.c, self.tn
        h = 44 + len(lines) * 30
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                        + "".join(f'<circle cx="{x + 18 + k * 16}" cy="{y + 16}" r="4.5" fill="{col}"/>'
                                  for k, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")))
                        + t(x + 72, y + 21, title, 12, c["faint"], w - 90, 500, MONO))
        for i, (line, hl) in enumerate(lines):
            ly = y + 54 + i * 30
            col = tn["warn"] if hl else c["ink"]
            self.appear(t(x + 18, ly, ("▶ " if hl else "  ") + line, 15, col, w - 36, 700 if hl else 500, MONO,
                          extra=' xml:space="preserve"'), t0 + i * step)
        return t0 + len(lines) * step

    def checklist(self, x, y, items, t0=.6, step=.8, gap=40):
        c, ok = self.c, self.tn["ok"]
        for i, (head, body) in enumerate(items):
            iy = y + i * gap
            self.out.append(f'<circle cx="{x + 12}" cy="{iy}" r="12" fill="none" stroke="{c["line"]}" stroke-width="2"/>')
            self.appear(f'<circle cx="{x + 12}" cy="{iy}" r="12" fill="{ok}"/>'
                        f'<path d="M{x + 6} {iy} l4 4 l8 -8" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>'
                        + t(x + 34, iy + 5, head, 15, c["ink"], 150, 700)
                        + t(x + 34 + width(head, 15) + 12, iy + 5, body, 14, c["muted"], 520), t0 + i * step)

    def tiles(self, x, y, cols, n, cell, finals, t0=.3, step=.04, base=None, gap=6):
        """n칸을 차례로 채운다. finals[i] = 최종 색(없으면 accent)."""
        c = self.c
        for i in range(n):
            cx, cy = x + (i % cols) * (cell + gap), y + (i // cols) * (cell + gap)
            self.out.append(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="3" fill="{base or c["track"]}"/>')
            self.appear(f'<rect x="{cx}" y="{cy}" width="{cell}" height="{cell}" rx="3" fill="{finals.get(i, c["accent"])}"/>',
                        t0 + i * step)

    def svg(self, aria):
        self.css.append("@media (prefers-reduced-motion:reduce){*{animation:none!important}}")
        return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{self.H}" viewBox="0 0 {W} {self.H}" '
                          f'role="img" aria-label="{escape(aria)}">', f'<style>{"".join(self.css)}</style>', *self.out, "</svg>"])


def env_card(s, x, y, w, name, ok, label):
    """LOCAL / EC2 같은 실행 환경 카드."""
    c, tn = s.c, s.tn
    col = tn["ok"] if ok else tn["warn"]
    s.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="150" rx="12" fill="{c["bg"]}" stroke="{col}" stroke-width="2"/>'
                 + t(x + 24, y + 38, name, 20, c["ink"], w - 48, 700, MONO)
                 + t(x + 24, y + 70, label, 15, c["muted"], w - 48)
                 + f'<rect x="{x + 24}" y="{y + 96}" width="{w - 48}" height="12" rx="6" fill="{c["track"]}"/>')
    if ok:
        s.appear(f'<rect x="{x + 24}" y="{y + 96}" width="{w - 48}" height="12" rx="6" fill="{col}"/>'
                 + t(x + w - 24, y + 136, "✓ 성공", 15, col, 120, 700, anchor="end"), .8)
    else:
        s.out.append(f'<rect x="{x + 24}" y="{y + 96}" width="{(w - 48) * .3:.0f}" height="12" rx="6" fill="{col}"/>')
        s.out.append(f'<g class="blink">' + t(x + w - 24, y + 136, "✕ 실패", 15, col, 120, 700, anchor="end") + "</g>")


# ── 화면별 장면 ─────────────────────────────────────────────────────────────────────────────

def sc_s1(c, tn):
    s = Scene(c, tn, "SCENARIO 1 · 통합사원증", "STEP 1/2", "SERVICE DOWN", "warn", blink=True)
    s.chart(40, 86, 540, 150, [.2, .22, .25, .3, .28, .4, .55, .72, .88, .96, .99, .98, 1], tn["warn"], label="요청 수")
    s.chart(620, 86, 540, 150, [.15, .16, .15, .18, .2, .22, .3, .5, .75, .92, .99, 1, 1], tn["warn"], .9, 3.2, label="응답 시간 · 실패")
    s.out.append(t(40, 276, "20개 계열사 · 175개 사업장이 같은 시스템을 씁니다", 14, c["muted"], 700))
    return s.svg("요청 수와 응답 시간이 치솟고 서비스가 멈춘 상황")


def sc_s1_restart(c, tn):
    s = Scene(c, tn, "SCENARIO 1 · 선택 A", "재시작", "다시 폭주", "warn", blink=True)
    s.chart(40, 86, 1120, 150, [.95, .97, .96, .14, .12, .15, .24, .42, .66, .86, .95, .98, .99], tn["warn"], .3, 4.2,
            label="요청 처리 지연", marks=[(3, "재시작")])
    s.out.append(t(40, 276, "원인을 모른 채 재시작하면, 다음 장애도 같은 자리에서 시작합니다", 14, c["muted"], 900))
    return s.svg("재시작 직후 잠깐 회복했다가 다시 치솟는 그래프")


def sc_s1_logs(c, tn):
    s = Scene(c, tn, "SCENARIO 1 · 통합사원증", "STEP 2/2", "원인 확인", "amber")
    end = s.terminal(40, 64, 720, "로그 분석 요약 (재구성)", [("$ MSSQL · Windows 로그 확인", False), ("동시 인증 요청 급증", False),
                                                       ("DB 세션 락 누적", True), ("쿼리 실행계획 비효율", True),
                                                       ("사용자 대기 계속", False)])
    s.out.append(t(800, 96, "발견", 15, c["muted"], 300, 600))
    for i, lab in enumerate(["세션 락 누적", "비효율 실행계획"]):
        s.appear(f'<rect x="800" y="{116 + i * 56}" width="340" height="42" rx="21" fill="{tn["warn"]}" opacity=".14"/>'
                 + t(822, 143 + i * 56, "● " + lab, 16, tn["warn"], 300, 700), end + i * .3)
    return s.svg("로그에서 DB 세션 락 누적과 비효율 실행계획을 찾는 터미널")


def sc_s1_index(c, tn):
    s = Scene(c, tn, "SCENARIO 1 · 선택 A", "인덱스부터", "대기 증가", "amber", blink=True)
    s.out.append(t(40, 100, "인덱스 조정 · 검증 중…", 16, c["ink"], 500, 700))
    s.out.append(f'<rect x="40" y="118" width="500" height="16" rx="8" fill="{c["track"]}"/>')
    name = s._name()
    s.css.append(f"@keyframes {name}{{0%{{transform:scaleX(.02)}}{s.pc(7.4)}{{transform:scaleX(.32)}}100%{{transform:scaleX(.02)}}}}")
    s.out.append(f'<rect class="a" x="40" y="118" width="500" height="16" rx="8" fill="{tn["amber"]}" '
                 f'style="animation-name:{name};transform-box:fill-box;transform-origin:0 50%"/>')
    s.out.append(t(620, 100, "기다리는 사용자", 16, c["ink"], 400, 700))
    for i in range(48):
        x, y = 620 + (i % 16) * 32, 120 + (i // 16) * 32
        s.appear(f'<circle cx="{x + 10}" cy="{y + 10}" r="9" fill="{tn["warn"]}" opacity=".75"/>', .2 + i * .14)
    s.out.append(t(40, 276, "맞는 방향이지만, 서비스를 먼저 살리지 않으면 줄은 계속 길어집니다", 14, c["muted"], 900))
    return s.svg("인덱스 작업이 진행되는 동안 기다리는 사용자가 늘어나는 장면")


def sc_s1_end(c, tn):
    s = Scene(c, tn, "SCENARIO 1 · CLEAR", "실제 대응", "RECOVERED", "ok")
    s.chart(40, 86, 460, 170, [.98, .97, .96, .6, .38, .3, .28, .27, .27, .26], tn["ok"], .3, 2.4, label="응답 시간")
    s.checklist(540, 112, [("복구", "문제 세션 분리 · 처리 우선순위 조정"), ("근본 원인", "인덱스 조정 · 락 경합 테이블 분할"),
                           ("재발 방지", "재현 환경 검증 · Profiler 모니터링 · 로그 분석 자동화")], gap=56)
    return s.svg("응답 시간이 정상으로 돌아오고 복구 · 근본 원인 · 재발 방지 체크리스트가 채워지는 장면")


def sc_s2(c, tn):
    s = Scene(c, tn, "SCENARIO 2 · 수양회 D-6", "STEP 1/2", "EC2 실패", "warn", blink=True)
    env_card(s, 40, 72, 540, "LOCAL", True, "라벨 이미지 생성")
    env_card(s, 620, 72, 540, "EC2 (운영)", False, "라벨 이미지 생성")
    s.out.append(t(40, 276, "참가자 약 1,500명분 라벨 · 행사까지 6일", 14, c["muted"], 700))
    return s.svg("로컬에서는 이미지 생성이 성공하고 운영 서버에서만 실패하는 장면")


def sc_s2_code(c, tn):
    s = Scene(c, tn, "SCENARIO 2 · 선택 A", "코드 다시 읽기", "변화 없음", "amber")
    for k, (x, name, ok) in enumerate(((40, "로컬 코드", True), (640, "운영 코드", False))):
        s.out.append(f'<rect x="{x}" y="64" width="520" height="168" rx="10" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                     + t(x + 20, 92, name, 14, c["muted"], 300, 600, MONO))
        for i, wdt in enumerate((300, 380, 240, 340)):
            s.out.append(f'<rect x="{x + 20 + (i % 2) * 24}" y="{110 + i * 26}" width="{wdt}" height="10" rx="5" fill="{c["faint"]}" opacity=".55"/>')
        col = tn["ok"] if ok else tn["warn"]
        s.appear(t(x + 500, 222, "✓ 성공" if ok else "✕ 실패", 15, col, 120, 700, anchor="end"), 1.2)
    s.out.append(t(600, 156, "=", 34, c["ink"], 40, 700, anchor="middle"))
    s.out.append(t(40, 276, "같은 코드가 로컬에서는 돕니다. 다른 건 코드가 도는 환경입니다", 14, c["muted"], 900))
    return s.svg("로컬과 운영 서버의 코드가 같은데 결과만 다른 장면")


def sc_s2_env(c, tn):
    s = Scene(c, tn, "SCENARIO 2 · 수양회 D-6", "STEP 2/2", "후보 3개", "amber")
    rows = ["Chromium 실행 파일", "리눅스 권한 · sandbox", "서버 속도 · 타임아웃"]
    s.out.append(t(360, 82, "LOCAL", 14, c["muted"], 200, 700, MONO) + t(640, 82, "EC2 (운영)", 14, c["muted"], 200, 700, MONO))
    for i, r in enumerate(rows):
        y = 100 + i * 52
        s.out.append(f'<rect x="40" y="{y}" width="1120" height="42" rx="8" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                     + t(60, y + 27, r, 15, c["ink"], 280, 700)
                     + t(360, y + 27, "✓ 문제 없음", 14, tn["ok"], 240, 600))
        s.appear(t(640, y + 27, "? 원인 후보", 14, tn["amber"], 240, 700)
                 + f'<rect x="900" y="{y + 10}" width="240" height="22" rx="11" fill="{tn["amber"]}" opacity=".15"/>'
                 + t(1020, y + 26, "운영에서만 다를 수 있음", 12, tn["amber"], 230, 600, anchor="middle"), .6 + i * .9)
    s.out.append(t(40, 276, "환경 차이를 나열하자 후보가 세 가지로 좁혀졌습니다", 14, c["muted"], 900))
    return s.svg("로컬과 운영 서버의 실행 환경을 비교해 원인 후보 세 가지를 찾는 표")


def sc_s2_all(c, tn):
    s = Scene(c, tn, "SCENARIO 2 · 선택 A", "전부 아니면 전무", "전체 실패", "warn", blink=True, cycle=9)
    finals = {i: tn["ok"] for i in range(60)}
    finals[37] = tn["warn"]
    s.tiles(40, 70, 20, 60, 34, finals, t0=.2, step=.06)
    s.appear(f'<rect x="40" y="66" width="{20 * 40}" height="{3 * 40 + 2}" rx="6" fill="{c["panel"]}" opacity=".85"/>'
             + t(440, 140, "1장 실패 → ZIP 전체 실패 → 처음부터", 22, tn["warn"], 780, 700, anchor="middle"), 5.0)
    s.out.append(t(880, 110, "1,500장 중", 15, c["muted"], 280, 600) + t(880, 140, "단 1장만 실패해도", 15, c["muted"], 280, 600))
    s.out.append(t(40, 276, "그림의 칸 60개는 1,500장을 줄여 그린 개념도입니다", 13, c["faint"], 900))
    return s.svg("한 장이 실패하자 ZIP 전체가 실패하는 장면")


def sc_s2_end(c, tn):
    s = Scene(c, tn, "SCENARIO 2 · CLEAR", "실제 대응", "ZIP 완료", "ok", cycle=9)
    finals = {i: tn["ok"] for i in range(40)}
    finals[23] = tn["amber"]
    s.tiles(40, 72, 10, 40, 30, finals, t0=.2, step=.05)
    s.appear(t(40, 260, "■ 실패한 장은 따로 · 나머지로 ZIP 완성", 13, tn["amber"], 400, 700), 2.4)
    s.checklist(470, 92, [("Chromium", "운영에서는 시스템 경로 /usr/bin/chromium-browser"), ("sandbox", "--no-sandbox · --disable-setuid-sandbox"),
                          ("타임아웃", "느린 서버에 맞춰 연장"), ("부분 실패", "Promise.allSettled")], t0=2.8, step=.7)
    return s.svg("나머지 이미지로 ZIP을 완성하고 대응 체크리스트가 채워지는 장면")


def sc_s3(c, tn):
    s = Scene(c, tn, "SCENARIO 3 · 배포 전", "STEP 1/2", "ALL GREEN", "ok")
    s.checklist(40, 92, [("서버", "Jest 44"), ("관리자", "Jest 34"), ("참가자", "Vitest 95"), ("화면", "mock E2E 172")], t0=.4, step=.6, gap=44)
    s.appear(t(1160, 160, "배포해도 될까?", 34, c["ink"], 500, 700, anchor="end"), 3.0)
    return s.svg("서버 · 관리자 · 참가자 테스트와 mock E2E가 모두 통과한 장면")


def sc_s3_ship(c, tn):
    s = Scene(c, tn, "SCENARIO 3 · 선택 A", "바로 배포", "500", "warn", blink=True)
    boxes = [(40, "관리자", "입금 확인 클릭"), (440, "서버", "처리 중"), (840, "DB", "")]
    for x, name, sub in boxes:
        s.out.append(f'<rect x="{x}" y="80" width="320" height="100" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                     + t(x + 24, 118, name, 18, c["ink"], 270, 700) + t(x + 24, 150, sub, 14, c["muted"], 270))
    s.out.append(t(400, 136, "→", 22, c["faint"], 30, anchor="middle") + t(800, 136, "→", 22, c["faint"], 30, anchor="middle"))
    s.appear(t(1136, 150, "PAID ✓ 저장됨", 15, tn["ok"], 260, 700, anchor="end"), 1.0)
    s.appear(f'<rect x="40" y="204" width="320" height="44" rx="10" fill="{tn["warn"]}" opacity=".14"/>'
             + t(60, 232, "← 응답 500 ✕", 16, tn["warn"], 280, 700, MONO), 1.8)
    s.appear(f'<g class="blink">' + t(600, 232, "저장은 됐는데 실패로 보인다", 16, tn["warn"], 520, 700, anchor="middle") + "</g>", 2.6)
    s.out.append(t(40, 276, "다시 누르면 \"대기 상태가 아닙니다\", 재신청하면 \"이미 신청\"", 14, c["muted"], 900))
    return s.svg("입금 확인 요청이 DB에는 저장됐는데 응답은 500으로 실패하는 장면")


def sc_s3_click(c, tn):
    s = Scene(c, tn, "SCENARIO 3 · 실제 DB", "STEP 2/2", "버그 12건", "amber", cycle=9)
    bugs = {2, 5, 9, 13, 16, 20, 22, 26, 29, 31, 34, 37}  # 그림 속 위치는 임의, 개수는 실제
    finals = {i: (tn["warn"] if i in bugs else c["accent"]) for i in range(38)}
    s.tiles(40, 72, 19, 38, 46, finals, t0=.3, step=.12, gap=12)
    s.appear(t(40, 236, "38개 화면 순회", 18, c["ink"], 300, 700) + t(300, 236, "● 버그 12건 추가 발견", 18, tn["warn"], 400, 700), 5.0)
    s.out.append(t(40, 276, "mock 테스트가 모두 통과한 뒤에 나온 버그들 · 빨간 칸의 위치는 그림용", 13, c["faint"], 900))
    return s.svg("로컬 DB에 붙여 38개 화면을 차례로 눌러 보며 12건의 버그를 찾는 장면")


def sc_s3_rollback(c, tn):
    s = Scene(c, tn, "SCENARIO 3 · 선택 A", "트랜잭션에 넣기", "되돌릴 수 없음", "warn", blink=True)
    s.out.append(f'<rect x="40" y="70" width="520" height="170" rx="12" fill="{c["bg"]}" stroke="{c["line"]}"/>'
                 + t(64, 104, "BEGIN", 16, c["muted"], 200, 700, MONO) + t(64, 134, "  입금 확인 저장", 15, c["ink"], 400, 500, MONO)
                 + t(64, 164, "  문자 발송", 15, c["ink"], 400, 500, MONO))
    s.appear(t(64, 210, "ROLLBACK", 16, tn["warn"], 200, 700, MONO), 2.4)
    # 문자 봉투가 이미 밖으로 날아간다
    name = s._name()
    s.css.append(f"@keyframes {name}{{0%,{s.pc(1.0)}{{transform:none;opacity:0}}{s.pc(1.2)}{{opacity:1}}"
                 f"{s.pc(2.4)},{s.pc(7.6)}{{transform:translate(520px,-6px);opacity:1}}100%{{opacity:0}}}}")
    s.out.append(f'<g class="a" style="animation-name:{name}"><rect x="420" y="146" width="56" height="38" rx="5" fill="{c["bg"]}" stroke="{c["accent"]}" stroke-width="2"/>'
                 f'<path d="M420 148 L448 168 L476 148" fill="none" stroke="{c["accent"]}" stroke-width="2"/></g>')
    s.appear(t(1040, 210, "이미 발송됨 · 회수 불가", 16, tn["warn"], 300, 700, anchor="middle"), 2.6)
    s.out.append(t(40, 276, "DB는 되돌아가도 나간 문자는 되돌릴 수 없는 외부 효과입니다", 14, c["muted"], 900))
    return s.svg("트랜잭션은 롤백됐지만 문자는 이미 발송되어 회수할 수 없는 장면")


def sc_s3_end(c, tn):
    s = Scene(c, tn, "SCENARIO 3 · CLEAR", "실제 대응", "CLEAR", "ok")
    chips = [("커밋 ✓", tn["ok"]), ("문자 발송 ✕", tn["warn"]), ("응답 성공 + 경고", tn["ok"])]
    for i, (lab, col) in enumerate(chips):
        x = 40 + i * 380
        s.appear(f'<rect x="{x}" y="70" width="320" height="48" rx="24" fill="{col}" opacity=".14"/>'
                 + t(x + 160, 101, lab, 17, col, 300, 700, anchor="middle")
                 + (t(x + 350, 101, "→", 20, c["faint"], 30, anchor="middle") if i < 2 else ""), .3 + i * .6)
    s.checklist(40, 160, [("14곳", "notifyAfterCommit() 으로 커밋 뒤 문자 분리"), ("3곳", "문자가 목적인 요청은 그대로 실패를 알림"),
                          ("관리자", "\"처리는 완료됐지만 문자가 발송되지 않았습니다\" 경고")], t0=2.2, step=.7, gap=38)
    return s.svg("커밋은 성공, 문자만 실패해도 요청은 성공으로 응답하고 경고를 띄우는 장면")


def banner(c, tn):
    s = Scene(c, tn, "INCIDENT SIMULATOR", "3 SCENARIOS · 15 SCREENS", "ON CALL", "warn", blink=True, H=240)
    name = s._name()
    s.css.append(f"@keyframes {name}{{0%{{transform:scale(1);opacity:.5}}100%{{transform:scale(2.6);opacity:0}}}}")
    s.out.append(f'<circle class="a" cx="92" cy="140" r="22" fill="{tn["warn"]}" style="animation:{name} 1.6s ease-out infinite;transform-box:fill-box;transform-origin:50% 50%"/>'
                 f'<circle cx="92" cy="140" r="22" fill="{tn["warn"]}"/>'
                 + t(92, 148, "!", 26, "#FFFFFF", 20, 700, MONO, anchor="middle"))
    s.out.append(t(150, 136, "장애 대응 시뮬레이터", 38, c["ink"], 900, 700))
    s.out.append(t(150, 176, "제가 실제로 겪은 장애 3가지를 골라 가며 풀어 보세요. 끝에는 실제 대응과 기록 문서가 있습니다.", 16, c["muted"], 1000))
    return s.svg("장애 대응 시뮬레이터 — 실제로 겪은 장애 3가지를 골라 가며 풀어 보기")


# ── 버튼 카드 ────────────────────────────────────────────────────────────────────────────────

def choice_card(c, tn, letter, text):
    Wc, Hc = 600, 104
    lines = wrap(text, 17, Wc - 140)[:2]
    css = ("@keyframes nudge{0%,70%,100%{transform:none}80%{transform:translateX(6px)}90%{transform:none}}"
           ".arw{animation:nudge 3s ease-in-out infinite}@media (prefers-reduced-motion:reduce){.arw{animation:none}}")
    ty = Hc / 2 + 6 - (len(lines) - 1) * 12
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}" role="img" aria-label="{escape(letter + ". " + text)}">',
                      f"<style>{css}</style>",
                      f'<rect x="1" y="1" width="{Wc - 2}" height="{Hc - 2}" rx="14" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/>',
                      f'<circle cx="46" cy="{Hc / 2}" r="22" fill="{c["accent"]}"/>',
                      t(46, Hc / 2 + 7, letter, 20, "#FFFFFF", 30, 700, MONO, anchor="middle"),
                      *[t(84, ty + i * 24, ln, 17, c["ink"], Wc - 140, 700) for i, ln in enumerate(lines)],
                      '<g class="arw">' + t(Wc - 30, Hc / 2 + 7, "→", 20, c["accent"], 30, 700, anchor="middle") + "</g>",
                      "</svg>"])


def menu_card(c, tn, n, title, stage):
    Wc, Hc = 400, 150
    lines = wrap(title, 17, Wc - 48)[:2]
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}" role="img" aria-label="{escape(f"시나리오 {n}: {title}")}">',
                      f'<rect x="1" y="1" width="{Wc - 2}" height="{Hc - 2}" rx="14" fill="{c["panel"]}" stroke="{c["line"]}"/>',
                      f'<rect x="1" y="1" width="{Wc - 2}" height="6" rx="3" fill="{tn["warn"]}"/>',
                      t(24, 40, f"SCENARIO {n}", 13, tn["warn"], 200, 700, MONO, extra=' letter-spacing="1"'),
                      *[t(24, 74 + i * 24, ln, 17, c["ink"], Wc - 48, 700) for i, ln in enumerate(lines)],
                      t(24, 132, stage, 13, c["muted"], Wc - 48),
                      "</svg>"])


def small_button(c, tn, label):
    Wc, Hc = 300, 56
    return "\n".join([f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wc}" height="{Hc}" viewBox="0 0 {Wc} {Hc}" role="img" aria-label="{escape(label)}">',
                      f'<rect x="1" y="1" width="{Wc - 2}" height="{Hc - 2}" rx="28" fill="{c["panel"]}" stroke="{c["line"]}"/>',
                      t(Wc / 2, Hc / 2 + 6, label, 16, c["ink"], Wc - 40, 700, anchor="middle"),
                      "</svg>"])


# ── 화면 목록: (id, 제목, 장면, 본문, 선택지[(글자, 문장, 이동)], 마무리) ───────────────────────────────

DOCS = {1: ("통합사원증 시스템 운영 기록", "https://github.com/Jkim1647/portfolio/blob/main/projects/05-hds-integrated-id-card.md"),
        2: ("수양회 관리 시스템 기록", "https://github.com/Jkim1647/portfolio/blob/main/projects/04-sarang-retreat.md"),
        3: ("수양회 시스템 2026 리팩토링 기록", "https://github.com/Jkim1647/portfolio/blob/main/projects/07-sarang-retreat-refactor.md")}
MENU = [(1, "로그인 · 출입 요청이 폭주해 서비스가 멈춘다", "현대자동차그룹 통합사원증 · 2021–2024", "s1"),
        (2, "행사 6일 전, 운영 서버에서만 이미지가 안 만들어진다", "수양회 관리 시스템 · 2025", "s2"),
        (3, "mock 테스트가 전부 통과했다. 배포해도 될까?", "수양회 시스템 리팩토링 · 2026", "s3")]

SCREENS = [
    dict(id="s1", title="1-1. 요청 폭주, 서비스 중단", scene=sc_s1,
         body="사원증 로그인과 출입 요청이 한꺼번에 몰리면서 **서비스가 멈췄습니다.** 무엇부터 하시겠어요?",
         choices=[("A", "일단 서버를 재시작한다", "s1-restart"), ("B", "MSSQL · Windows 로그부터 본다", "s1-logs")]),
    dict(id="s1-restart", title="🤔 잠깐 살아납니다, 그런데…", scene=sc_s1_restart,
         body="재시작하면 몇 분은 버팁니다. 하지만 요청이 다시 몰리면 **같은 일이 반복**됩니다.", retry="s1"),
    dict(id="s1-logs", title="1-2. 로그가 말해 준 것", scene=sc_s1_logs,
         body="**동시 인증 부하 속에 DB 세션 락이 쌓이고** 있었고, **쿼리 실행계획도 비효율적**이었습니다. 사용자들은 지금도 기다리는 중입니다. 지금 당장은?",
         choices=[("A", "인덱스와 쿼리부터 제대로 고친다", "s1-index-first"), ("B", "문제 세션을 먼저 분리하고 처리 우선순위를 조정한다", "s1-end")]),
    dict(id="s1-index-first", title="🤔 맞는 방향, 틀린 순서", scene=sc_s1_index,
         body="인덱스 조정은 근본 대책이 맞습니다. 하지만 검증까지 시간이 걸리고, 그동안 **사용자들은 계속 기다립니다.** 먼저 서비스를 살리고, 근본 원인은 그다음입니다.",
         retry="s1-logs"),
    dict(id="s1-end", title="🏁 실제로는 이렇게 했어요", scene=sc_s1_end,
         body="> 여러 회사가 같은 시스템을 쓰면 작은 오류도 파급이 큽니다. 추측보다 로그 · 데이터로 범위를 먼저 좁히고, 대응 순서는 문서로 남깁니다.",
         doc=1),
    dict(id="s2", title="2-1. 행사 6일 전", scene=sc_s2,
         body="참가자 약 1,500명의 라벨 이미지를 만드는 기능이 **운영 서버(EC2)에서만 실패**합니다. 어디부터 보시겠어요?",
         choices=[("A", "이미지 생성 코드의 로직을 다시 읽는다", "s2-code"), ("B", "로컬과 운영 서버의 실행 환경 차이를 나열한다", "s2-env")]),
    dict(id="s2-code", title="🤔 같은 코드인데요", scene=sc_s2_code,
         body="코드가 아니라 **코드가 도는 환경**이 다를 가능성이 훨씬 큽니다.", retry="s2"),
    dict(id="s2-env", title="2-2. 원인 후보 세 가지", scene=sc_s2_env,
         body="후보를 모두 막았습니다. 그런데 1,500장 중 **몇 장이 실패하면** ZIP은 어떻게 할까요?",
         choices=[("A", "하나라도 실패하면 ZIP 생성 전체를 실패로 처리한다", "s2-all-or-nothing"),
                  ("B", "실패한 장만 따로 처리하고 나머지로 ZIP을 만든다", "s2-end")]),
    dict(id="s2-all-or-nothing", title="🤔 한 장 때문에 전부 다시", scene=sc_s2_all,
         body="안전해 보이지만, 행사 직전에 **한 장의 실패가 1,500장 전체를 다시 만들게** 합니다.", retry="s2-env"),
    dict(id="s2-end", title="🏁 실제로는 이렇게 했어요", scene=sc_s2_end,
         body="> 아쉬운 점도 남깁니다. 운영 서버와 같은 환경에서 미리 돌려 보지 않아 행사 직전에 장애를 만났습니다.", doc=2),
    dict(id="s3", title="3-1. 초록불이 가득하다", scene=sc_s3,
         body="세 저장소를 리팩토링했고, 테스트가 **전부 통과**했습니다. 이제 어떻게 할까요?",
         choices=[("A", "배포한다", "s3-ship"), ("B", "로컬 DB에 실제로 붙여 화면을 하나씩 눌러 본다", "s3-click")]),
    dict(id="s3-ship", title="🤔 입금 확인을 눌렀더니 500", scene=sc_s3_ship,
         body="응답은 `500`인데 DB에는 이미 `PAID`가 저장돼 있습니다. mock 데이터로는 보이지 않던 버그입니다.", retry="s3"),
    dict(id="s3-click", title="3-2. 38개 화면을 눌러 보니 버그 12건", scene=sc_s3_click,
         body="그중 하나: 입금 확인은 저장됐는데 **커밋 뒤에 보내는 문자 한 통이 실패하면서** 요청 전체가 `500`이 됐습니다. 어떻게 고칠까요?",
         choices=[("A", "문자 발송을 트랜잭션 안에 넣어, 실패하면 함께 롤백한다", "s3-rollback"),
                  ("B", "커밋 뒤 문자는 실패해도 요청은 성공으로, 결과만 따로 알린다", "s3-end")]),
    dict(id="s3-rollback", title="🤔 문자는 되돌릴 수 없어요", scene=sc_s3_rollback,
         body="DB는 롤백되지만 **이미 나간 문자는 회수할 수 없는 외부 효과**입니다.", retry="s3-click"),
    dict(id="s3-end", title="🏁 실제로는 이렇게 했어요", scene=sc_s3_end,
         body="> mock 테스트가 모두 통과한 상태에서도 **실제 DB로 화면을 눌러 본 단계에서 12건이 더** 나왔습니다.", doc=3),
]


def pic(name, alt, w="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/incident/{name}_dark.svg">'
            f'<img src="./assets/incident/{name}_light.svg" width="{w}" alt="{escape(alt, {chr(34): "&quot;"})}" /></picture>')


def write_markdown():
    md = ['<a id="start"></a>', "", '<p align="center">' + pic("banner", "장애 대응 시뮬레이터 — 실제로 겪은 장애 3가지") + "</p>", "",
          '<p align="center">' + "\n".join(f'<a href="#{to}">{pic(f"menu{n}", f"시나리오 {n}: {title}", "32%")}</a>'
                                           for n, title, _, to in MENU) + "</p>", "",
          '<p align="center"><sub><a href="https://github.com/Jkim1647">↩ 프로필로 돌아가기</a></sub></p>', "", SPACER, "", "---", ""]
    for s in SCREENS:
        md += [f'<a id="{s["id"]}"></a>', "", f'## {s["title"]}', "", '<p align="center">' + pic(f'sc_{s["id"]}', s["title"]) + "</p>", "", s["body"], ""]
        if "choices" in s:
            md.append('<p align="center">' + "\n".join(f'<a href="#{to}">{pic(f"ch_{s["id"]}_{L}", f"{L}. {text}", "49%")}</a>'
                                                       for L, text, to in s["choices"]) + "</p>")
        if "retry" in s:
            md.append(f'<p align="center"><a href="#{s["retry"]}">{pic("btn_retry", "↩ 다시 고르기", "25%")}</a></p>')
        if "doc" in s:
            name, url = DOCS[s["doc"]]
            md.append(f'<p align="center">📄 <a href="{url}">{name}</a></p>')
            md.append(f'<p align="center"><a href="#start">{pic("btn_menu", "↩ 다른 시나리오", "25%")}</a></p>')
        md += ["", SPACER, "", "---", ""]
    md.append('<sub><a href="https://github.com/Jkim1647">프로필로 돌아가기</a></sub>')
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    count = 0
    for mode, c in THEMES.items():
        tn = TONE[mode]
        files = {"banner": banner(c, tn), "btn_retry": small_button(c, tn, "↩ 다시 고르기"),
                 "btn_menu": small_button(c, tn, "↩ 다른 시나리오")}
        for n, title, stage, _ in MENU:
            files[f"menu{n}"] = menu_card(c, tn, n, title, stage)
        for s in SCREENS:
            files[f'sc_{s["id"]}'] = s["scene"](c, tn)
            for L, text, _ in s.get("choices", []):
                files[f'ch_{s["id"]}_{L}'] = choice_card(c, tn, L, text)
        for name, svg in files.items():
            (OUT / f"{name}_{mode}.svg").write_text(svg, encoding="utf-8")
            count += 1
    write_markdown()
    print(f"{count} files → {OUT}, {MD.name}")


if __name__ == "__main__":
    main()

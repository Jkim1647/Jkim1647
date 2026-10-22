"""공개 기여 달력(github.com/users/<id>/contributions)을 읽어 data/contributions.json에 저장한다.

    python scripts/fetch_contributions.py

방문자에게 보이는 그대로의 숫자를 쓴다. 비공개 저장소 기여까지 세려면 GitHub 설정의
"Include private contributions on my profile"을 켜야 한다. 마크업이 바뀌어 파싱이 실패하면
기존 파일을 건드리지 않고 0이 아닌 코드로 끝나서, 배너는 마지막으로 성공한 데이터로 남는다.
"""
import json
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

USER = "Jkim1647"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

CELL = re.compile(r'<td\b[^>]*\bdata-date="(\d{4}-\d{2}-\d{2})"[^>]*>')
ATTR = lambda name: re.compile(rf'\b{name}="([^"]*)"')
TIP = re.compile(r'<tool-tip\b[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>')
TOTAL = re.compile(r"([\d,]+)\s+contributions?\s+in the last year")


def fetch(user: str) -> str:
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-readme-renderer"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def parse(html: str) -> dict:
    counts = {}
    for cid, label in TIP.findall(html):
        m = re.match(r"(\d+) contributions? on", label.strip())
        counts[cid] = int(m.group(1)) if m else 0  # "No contributions on ..."

    days = []
    for tag in CELL.finditer(html):
        td = tag.group(0)
        cid, level = ATTR("id").search(td), ATTR("data-level").search(td)
        days.append({"date": tag.group(1),
                     "level": int(level.group(1)) if level else 0,
                     "count": counts.get(cid.group(1), 0) if cid else 0})
    days.sort(key=lambda d: d["date"])

    total = TOTAL.search(re.sub(r"\s+", " ", html))
    if len(days) < 300 or not total:
        raise ValueError(f"달력 파싱 실패: {len(days)}일, 합계 {'있음' if total else '없음'}")
    return {"total": int(total.group(1).replace(",", "")), "days": days, **stats(days)}


def stats(days) -> dict:
    active = [date.fromisoformat(d["date"]) for d in days if d["count"] > 0 or d["level"] > 0]
    longest = run = 0
    prev = None
    for d in active:
        run = run + 1 if prev and d - prev == timedelta(days=1) else 1
        longest, prev = max(longest, run), d
    return {"active_days": len(active), "longest_streak": longest}


def main() -> None:
    try:
        data = parse(fetch(USER))
    except Exception as e:  # 네트워크·마크업 변경 — 기존 데이터를 지킨다
        print(f"skip: {e}", file=sys.stderr)
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{data['total']} contributions · 활동 {data['active_days']}일 · 최장 연속 {data['longest_streak']}일")


if __name__ == "__main__":
    main()

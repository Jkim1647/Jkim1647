"""'build: car|robot|rocket' 이슈 하나를 처리해 data/builds.json과 빌드 로그 SVG를 갱신한다.

GitHub Actions(.github/workflows/build-with-me.yml)에서 호출된다. 이슈 제목·작성자는
방문자가 정하는 값이라 환경변수로만 받고, 허용 목록과 정규식으로 검증한 값만 기록한다.
결과 모양은 $GITHUB_OUTPUT 의 shape= 로 넘기고, 형식이 틀리면 빈 값으로 넘긴다.
"""
import json
import os
import re
from datetime import datetime, timedelta, timezone

import render_cards

TITLE = re.compile(r"^\s*build:\s*(car|robot|rocket)\s*$", re.IGNORECASE)
LOGIN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")  # GitHub 아이디 규칙
KEEP = 20


def set_output(shape: str) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"shape={shape}\n")


def main() -> None:
    m = TITLE.match(os.environ.get("BUILD_TITLE", ""))
    user = os.environ.get("BUILD_USER", "")
    if not m or not LOGIN.match(user):
        print("ignored: title or login did not validate")
        set_output("")
        return

    shape = m.group(1).lower()
    builds = render_cards.load_builds()
    builds["counts"][shape] += 1
    at = datetime.now(timezone(timedelta(hours=9))).strftime("%m/%d %H:%M")
    builds["recent"] = ([{"shape": shape, "user": user, "at": at}] + builds["recent"])[:KEEP]

    render_cards.BUILDS.parent.mkdir(exist_ok=True)
    render_cards.BUILDS.write_text(json.dumps(builds, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    render_cards.main()
    set_output(shape)


if __name__ == "__main__":
    main()

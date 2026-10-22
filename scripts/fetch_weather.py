"""오늘 광주 날씨(Open-Meteo, 키 없음)를 data/weather.json에 저장한다. 인사말 말풍선에 쓰인다.

    python scripts/fetch_weather.py

실패하면 기존 파일을 건드리지 않고 0이 아닌 코드로 끝난다. 인사말은 날짜가 오늘이 아닌
날씨 데이터를 쓰지 않으므로, 실패한 날에는 날씨 없이 요일 인사만 나간다.
"""
import json
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "weather.json"
URL = ("https://api.open-meteo.com/v1/forecast?latitude=35.1595&longitude=126.8526"
       "&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=Asia%2FSeoul&forecast_days=1")


def main() -> None:
    try:
        with urllib.request.urlopen(URL, timeout=20) as r:
            daily = json.load(r)["daily"]
        data = {"date": daily["time"][0], "code": int(daily["weather_code"][0]),
                "tmax": round(daily["temperature_2m_max"][0]), "tmin": round(daily["temperature_2m_min"][0])}
    except Exception as e:  # 네트워크·응답 형식 변경
        print(f"skip: {e}", file=sys.stderr)
        sys.exit(1)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data) + "\n", encoding="utf-8")
    print(data)


if __name__ == "__main__":
    main()

<div align="center">

# 김진영 · Jinyoung Kim

**엔터프라이즈 시스템 운영 3년 → 백엔드 · AI 개발자**<br>
현장에서 시스템을 "돌려본" 경험을 바탕으로, 느린 곳을 측정하고 숫자로 개선하는 개발을 합니다.

![SSAFY](https://img.shields.io/badge/SSAFY-16기-3396F4?style=flat-square)
![Kaggle](https://img.shields.io/badge/AI%20Challenge-Top%201.3%25-20BEFF?style=flat-square&logo=kaggle&logoColor=white)
![Skills](https://img.shields.io/badge/전국기능경기대회-장려상-d4a017?style=flat-square)

</div>

---

## 🏆 Highlights

| | 내용 | 결과 |
|---|---|---|
| 🤖 | **SSAFY 16기 AI 챌린지** — 한국어 4지선다 VLM-VQA | Public LB **955명 중 12위 (상위 1.3%)**, 0.92116 → **0.94324** |
| ⛪ | **사랑의교회 대학부 수련회 통합 관리 시스템** — 실서비스 운영 | 백엔드 담당 (Node.js · PostgreSQL · REST API · 성능 최적화) |
| 🔌 | **전국기능경기대회 공업전자기기** | 2019 전국 **장려상** · 2019 서울 **금상** · 2018 서울 우수상 (공식 검증 가능) |
| 🧩 | **알고리즘** — SWEA · 프로그래머스 | **84문제** (Java · C++ · JavaScript) |

## 📌 Projects

### [ssafy-vlm-vqa-pipeline](https://github.com/Jkim1647/ssafy-vlm-vqa-pipeline) &nbsp;`Python` `Qwen3-VL` `QLoRA` `RunPod A100`
재활용품 이미지 + 한국어 질문 → a~d 정답을 고르는 VQA 파이프라인.
- 로컬 RTX 5060 Ti의 **Qwen3-VL-4B QLoRA**에서 시작해 A100의 **Qwen3.5-35B-A3B**까지 확장
- **선택지 회전 TTA**로 위치 편향 제거, 모델별 확률 **soft ensemble**
- 이미지 SHA-256 기준 **grouped validation**으로 train/dev 누수 차단
- 실패한 시도(고해상도 TTA dev 과적합, margin router)까지 한/영 실험 로그로 기록

### [sarang-univ-admin](https://github.com/Jkim1647/sarang-univ-admin) &nbsp;`Node.js` `PostgreSQL` `Next.js` `TypeScript`
대학부 수련회의 신청 · 숙소 배정 · 셔틀버스 · 식사 체크 · GBS 라인업을 관리하는 운영 시스템.
- 본인 담당: **백엔드 API 설계 및 성능 최적화** (백엔드 코드는 비공개 repo)
- 공개 repo는 팀 관리자 프런트엔드 스냅샷입니다

### [industrial-electronics-skills-competition](https://github.com/Jkim1647/industrial-electronics-skills-competition) &nbsp;`C` `ATmega128` `OrCAD`
기능경기대회 준비 기록 — PCB 설계, 2대 엘리베이터 제어(UART), PWM 모터 제어, 회로설계 연습 39세션.

## 🛠 Tech Stack

**Backend** &nbsp;
![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=openjdk&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)

**AI / ML** &nbsp;
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

**Frontend** &nbsp;
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)

**Embedded** &nbsp;
![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![AVR](https://img.shields.io/badge/ATmega128-555555?style=flat-square)


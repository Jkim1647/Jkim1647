<div align="center">

# 김진영 · Jinyoung Kim

**엔터프라이즈 시스템 운영 3년 → 백엔드 · AI 개발자**<br>
현장에서 시스템을 "돌려본" 경험을 바탕으로, 느린 곳을 측정하고 숫자로 개선하는 개발을 합니다.

![SSAFY](https://img.shields.io/badge/SSAFY-16기-3396F4?style=flat-square)
![Kaggle](https://img.shields.io/badge/AI%20Challenge%202차-2위%2F217팀-FFB000?style=flat-square&logo=kaggle&logoColor=white)
![Kaggle](https://img.shields.io/badge/AI%20Challenge%201차-18위%2F954명-20BEFF?style=flat-square&logo=kaggle&logoColor=white)
![Skills](https://img.shields.io/badge/전국기능경기대회-장려상-d4a017?style=flat-square)

</div>

---

## 🏆 Highlights

| | 내용 | 결과 |
|---|---|---|
| 🥈 | [**SSAFY 16기 AI 챌린지 2차 · 사진 속 글자 읽기 VQA**](https://github.com/Jkim1647/ssafy16-ai-challenge-2) (5인 팀) | **217팀 중 최종 2위** (Private 0.98093) · 데이터 촬영·출제부터 재라벨링까지 직접 |
| 🤖 | [**SSAFY 16기 AI 챌린지 1차 · 재활용품 VQA**](https://github.com/Jkim1647/ssafy16-ai-challenge-1) (개인전) | **954명 중 최종 18위 (상위 1.9%)** (Private 0.93851) · Public 12위, 0.92116 → 0.94324 |
| ⛪ | **사랑의교회 수련회 관리 시스템** | 실서비스 백엔드 담당 (Node.js · PostgreSQL · REST API) |
| 🔌 | **전국기능경기대회 공업전자기기** | 2019 전국 **장려상** · 2019 서울 **금상** · 2018 서울 우수상 (공식 검증 가능) |

## 📌 Projects

### [ssafy16-ai-challenge-2](https://github.com/Jkim1647/ssafy16-ai-challenge-2) &nbsp;`Python` `Qwen3.5/3.6` `Gemma 4` `vLLM` `LoRA`
SSAFY 16기 AI 챌린지 2차 · 사진 속 글자 읽기 VQA — 사진 속 작은 글자를 읽고 4지선다에 답한다. **217팀 중 최종 2위**.
- 교육생이 직접 찍고 출제한 데이터를 팀원 5명이 다시 라벨링(dev 350문제 검수, 179문제 재작성) → 자체 채점표 401문제
- 모델을 9B→122B로 키우는 대신 **4분할 2배 확대 + 받아 적기** 입력으로 0.9445 → 0.9655 (추가 학습 없음)
- 9B\~397B 8종의 a\~d 확률을 저장해 **확률 평균 앙상블**, 제출 54회 실험을 GPU 없이 재계산

### [ssafy16-ai-challenge-1](https://github.com/Jkim1647/ssafy16-ai-challenge-1) &nbsp;`Python` `Qwen3-VL` `QLoRA` `RunPod A100`
SSAFY 16기 AI 챌린지 1차 · 재활용품 VQA — 재활용품 이미지 + 한국어 질문 → a~d 정답을 고른다. **954명 중 최종 18위**.
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


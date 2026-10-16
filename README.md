<div align="center">

# 김진영 · Jinyoung Kim

**운영을 아는 백엔드 개발자** — 엔터프라이즈 시스템 운영 3년 → 백엔드 · AI<br>
느린 곳은 먼저 재고, 숫자로 고치고, 결과는 직접 만든 기준으로 검증합니다.

![SSAFY](https://img.shields.io/badge/SSAFY-16기-3396F4?style=flat-square)
![AI Challenge 2](https://img.shields.io/badge/AI%20Challenge%202차-2위%2F217팀-FFB000?style=flat-square&logo=kaggle&logoColor=white)
![AI Challenge 1](https://img.shields.io/badge/AI%20Challenge%201차-18위%2F954명-20BEFF?style=flat-square&logo=kaggle&logoColor=white)
![정보처리기사](https://img.shields.io/badge/정보처리기사-2025.09-2f855a?style=flat-square)
![Skills](https://img.shields.io/badge/전국기능경기대회-장려상-d4a017?style=flat-square)

📄 [**포트폴리오 PDF**](https://github.com/Jkim1647/portfolio/blob/main/kim-jinyoung-portfolio.pdf) (14쪽) &nbsp;·&nbsp;
📂 [**프로젝트 상세 문서**](https://github.com/Jkim1647/portfolio) (트러블슈팅 · 기술 선택 이유 · 회고) &nbsp;·&nbsp;
✉️ kjy164777@gmail.com

</div>

---

## 한눈에

| | 무엇을 | 결과 |
|---|---|---|
| 🏢 | **현대자동차그룹 통합사원증·출입통제 시스템 운영** · 에이치디에스㈜ 2021–2024 | 20개 계열사 · 175개 사업장 · 임직원 약 12.8만 명 · 서버 교체 · 장애 대응 |
| ⚙️ | **수양회 관리 시스템 백엔드** · Node.js · PostgreSQL · 참가자 약 1,500명 실사용 | 라벨 이미지 ZIP 생성 **3~5분 → 22.8초** · 2026 리팩토링에서 다시 **29.9s → 9.9s** |
| 🥈 | **SSAFY AI 챌린지 2차 · 사진 속 글자 읽기 VQA** · 5인 팀 | **217팀 중 최종 2위** (Private 0.98093) |
| 🤖 | **SSAFY AI 챌린지 1차 · 재활용품 VQA** · 개인전 | **954명 중 18위** (상위 1.9%, Private 0.93851) |

## 걸어온 길

| 시기 | 내용 |
|---|---|
| 2026.07 – | **SSAFY 16기** (광주) — Java · Spring · 알고리즘 · AI. 부반장 · 스타트캠프 팀장 |
| 2025.04 – 07 | 사랑의교회 대학부 **수양회 관리 시스템 백엔드** — 복무 중 개인 시간에 참여, 2026년 수양회에서도 재사용 |
| 2024.03 – 2025.12 | **공군** 방공관제 지휘소 — 24시간 관제 체계 운용 지원 · 병장 만기전역 |
| 2021.02 – 2024.01 | **에이치디에스㈜** 사원 — 현대자동차그룹 통합사원증 시스템 운영 (MSSQL · Windows Server · VB6) |
| 2020.03 – 2023.02 | **한양대학교 ERICA** 스마트ICT융합전공 — 조기취업형 계약학과로 재직 병행 · GPA 4.0/4.5 |
| 2017 – 2019 | 서울로봇고 공업전자기기 — **전국기능경기대회 장려상 · 서울 금상** · 기능반 동아리장 |

## 프로젝트

### 🔧 Backend

**[사랑의교회 대학부 수양회 관리 시스템](https://github.com/Jkim1647/portfolio/blob/main/projects/04-sarang-retreat.md)** · 2025.04–07 · 7인 팀 백엔드 &nbsp;`Node.js` `Express` `TypeScript` `PostgreSQL` `AWS S3/CloudFront` `Puppeteer`
- 신청 · 입금 · 숙소 · 셔틀 · 조 편성을 한 시스템에서 관리. 조 편성(GBS) 모듈 공동 개발 — git blame 기준 모듈의 40%, 이미지 생성 유틸 2개 파일 100%
- 이미지 1장마다 Chromium을 띄우던 라벨 생성을 **브라우저 풀 + 환경별 동시성 제어**로 바꿔 ZIP 생성 **3~5분 → 22.8초**
- 행사 일주일 전 운영 서버(EC2)에서만 실패하던 이미지 생성 장애 해결 · 관리자 웹 스냅샷: [sarang-univ-admin](https://github.com/Jkim1647/sarang-univ-admin)

**[수양회 시스템 2026 리팩토링 기록](https://github.com/Jkim1647/sarang-retreat-refactor-notes)** · 2026.10 · 1인 (Claude Code 페어 프로그래밍) &nbsp;`Express` `Knex` `Next.js 14` `SWR` `React Query` `Playwright` `Jest/Vitest`
- 서버 · 관리자 웹 · 참가자 웹 세 저장소, 커밋 64건 · 테스트 Jest 79 · Vitest 95 · E2E 176
- 고치기 전에 **특성화 테스트로 동작을 고정**하고 벤치 · 렌더 카운터 · 번들 크기로 측정 → 라벨 생성 29.9s → 9.9s · 폼 리렌더 882 → 14 · First Load JS −65%
- mock 테스트가 모두 통과한 뒤 **로컬 DB에 붙여 38개 화면을 직접 순회**해 버그 12건을 더 발견 (커밋 뒤 문자 실패가 요청 전체를 500으로 만들던 문제 등)

**[LocalHub — 광주·전라 맛집 커뮤니티](https://github.com/sc-teamproject/Frontend)** · 2026.07 · 3일 · 3인 **팀장** &nbsp;`Vue 3` `Pinia` `Tailwind` `Leaflet` `FastAPI` `Netlify/Render`
- 맛집 416곳 지도 탐색 · 익명 게시판 · AI 추천 챗봇을 3일 만에 기획부터 배포까지. 프론트 커밋 20건 중 16건, 배포 설정 · 환경 차이 버그 해결

**SSAFY 1학기 관통 프로젝트** · 2026.07–10 · 2~3인 팀 &nbsp;`Java 17` `Spring Boot 3.5` `Maven` `FastAPI` `LangChain` `ChromaDB`
- 같은 여행 도메인을 4차에 걸쳐 확장 — Java Swing(1차) → RAG 챗봇(2차, RAGAS Context Recall 0.36 → 1.00) → 공공 API 5종 웹 플래너(3차) → **알고리즘 9종 + Spring Boot 백엔드**(4차)
- 4차: Held-Karp DP로 방문 순서 1,400km → 570km, 배터리 제약 Dijkstra, 자모 단위 편집 거리 오타 검색 — 모두 완전탐색 · JDK · RFC 벡터와 비교 검증 (저장소 공개 준비 중)

### 🤖 AI

**[ssafy16-ai-challenge-2](https://github.com/Jkim1647/ssafy16-ai-challenge-2)** · 사진 속 글자 읽기 VQA · **217팀 중 최종 2위** &nbsp;`Python` `vLLM` `Qwen3.5` `Gemma 4` `LoRA`
- 교육생이 직접 찍고 출제한 데이터를 팀원 5명이 다시 라벨링(dev 350문제 검수, 179문제 재작성) → 자체 채점표 401문제로 모든 채택을 판단
- 모델을 9B → 122B로 키우는 대신 **4분할 2배 확대 + 받아 적기** 입력으로 0.9445 → 0.9655 (추가 학습 없음)
- 9B~397B 8종의 a~d 확률을 저장해 **확률 평균 앙상블**, 제출 54회의 조합을 GPU 없이 재계산 · Public 11위 → Private 2위

**[ssafy16-ai-challenge-1](https://github.com/Jkim1647/ssafy16-ai-challenge-1)** · 재활용품 VQA · **954명 중 18위** &nbsp;`Python` `Qwen3-VL` `QLoRA` `RunPod A100`
- 로컬 RTX 5060 Ti의 Qwen3-VL-4B QLoRA에서 시작해 A100의 Qwen3.5-35B-A3B까지 확장
- **선택지 회전 TTA**로 위치 편향 제거 · 모델별 확률 soft ensemble · 이미지 해시 기준 grouped validation으로 누수 차단
- Public 12위 → Private 18위의 리더보드 과적합을 2차의 채택 규칙(자체 채점표 비하락)으로 바꿈

**사출성형 공정데이터 기반 품질불량 사전예측** · 2026 K-인공지능 제조데이터 분석 경진대회 · 1인 제출 &nbsp;`Python` `LightGBM` `이상탐지`
- KAMP 사출성형기 데이터로 최종검사 전 불량을 예측하고 검사 우선순위를 정함 · `run_all.py` 한 번으로 표 · 그림 · 보고서 재현 (심사 후 공개 예정)

### 🧱 Foundation

- **[industrial-electronics-skills-competition](https://github.com/Jkim1647/industrial-electronics-skills-competition)** &nbsp;`C` `ATmega128` `OrCAD` — 전국기능경기대회 준비 기록. PCB 설계 Gerber, 엘리베이터 2대 제어(UART), PWM 모터 제어, 회로설계 연습 39세션. 입상은 마이스터넷에서 공식 확인 가능
- **[Algorithm](https://github.com/Jkim1647/Algorithm)** &nbsp;`Java` — SWEA · 프로그래머스 96문제, BaekjoonHub 자동 커밋

## 🛠 Tech Stack

**Backend** &nbsp;
![Java](https://img.shields.io/badge/Java-007396?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=flat-square&logo=express&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MSSQL](https://img.shields.io/badge/MSSQL-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white)

**AI / ML** &nbsp;
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![vLLM](https://img.shields.io/badge/vLLM-30A2FF?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)

**Infra / Tools** &nbsp;
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazonwebservices&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)

**Frontend / Embedded** &nbsp;
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Vue](https://img.shields.io/badge/Vue%203-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=flat-square&logo=c&logoColor=black)
![AVR](https://img.shields.io/badge/ATmega128-555555?style=flat-square)

## 자격 · 수상

정보처리기사 (2025.09) · 전자산업기사 (2019.07) · TOEIC Speaking IM2 (2025.01)<br>
제54회 전국기능경기대회 공업전자기기 장려상 (2019.10) · 서울특별시 지방기능경기대회 금상 (2019.04)

## 일하는 방식

- **측정 먼저** — 동시성 값도 감이 아니라 실험 커밋으로 환경별 수치를 재서 정합니다
- **기준은 직접 만든다** — AI 대회에서는 Public 점수 대신 팀이 재라벨링한 채점표로 채택을 판단했습니다
- **AI 보조는 밝힌다** — AI와 페어로 만든 작업은 어디까지 AI가 했고 무엇을 직접 결정했는지 함께 적습니다

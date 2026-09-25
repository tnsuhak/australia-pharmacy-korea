# TNS 호주약대 2027 · 작업 인계

기준일: 2026-09-25

## 현재 운영 상태

- Repository: `tnsuhak/australia-pharmacy-korea`
- Branch: `feature/australia-pharmacy-2027-v1`
- PR: #1 · open · main 미병합
- Deploy Preview: https://deploy-preview-1--australia-pharmacy-korea.netlify.app
- Production: 미반영. 사용자 최종 승인 전 main merge 금지.
- 중앙 관리: `tnsuhak/tns-site-manager`의 OPERATING_SYSTEM / WEBSITE_BUILD_STANDARD / SEARCH_DISCOVERY_SYSTEM / DATA_STANDARD / policies.yaml / sites.yaml을 우선한다.
- 중앙 `sites.yaml`에는 아직 이 사이트 등록이 없으므로 사이트 안정화 후 별도 안전한 PR로 등록한다.

## 사이트 범위

- 대학 16개
- 학부 시작 프로그램 17개
- 입학경로 30개
- 장학 레코드 17개
- 숙소 레코드 23개
- 대학 상세페이지 중심 구조: `/universities/`
- 주요 허브: `/admission-pathways/`, `/direct-entry/`, `/foundation/`, `/diploma/`, `/graduate-entry/`, `/tuition-scholarships/`, `/after-graduation/`, `/pharmacist-registration/`

UWA는 16번째 비교 대학으로 포함돼 있으며, 학교졸업자용 4년 Bachelor of Human Sciences (Pharmaceutical Health) + Doctor of Pharmacy 구조와 대졸자용 별도 Doctor of Pharmacy를 구분한다.

## 데이터 원칙

현재 fact 상태 집계:
- 2027 확인: 387
- 최신 공개 기준: 394
- 2027 확인 중: 458
- 공식자료 충돌: 2

`docs/pending-facts.json`은 현재 `data/catalog.json`에서 다시 생성한 스냅샷이다. 미확정값을 2027 확정값으로 보이지 않게 유지한다.

## 2026-09-25 핵심 검증·수정

- Newcastle 2027 Pharmacy 학비를 **A$51,665**로 수정. A$49,205는 2026 금액.
- Newcastle 영어는 2027 Degree Guide의 IELTS 6.5/각 6.5와 현재 과정 페이지 English proficiency section의 7.0/각 7.0이 충돌하므로 자동 충족 판정에서 제외.
- Newcastle 2027 International Excellence Scholarship 20%는 Bachelor of Pharmacy (Honours) 제외과정으로 표시.
- Newcastle CIE Foundation을 구체화:
  - Pharmacy 진급 전체 평균 65%+
  - Academic English A&B 평균 75%+
  - Foundation 입학 IELTS 5.5 / 각 5.0
  - 한국 학생은 고2 수료(pass grades)부터 Foundation 입학 가능
  - Pharmacy는 본과 mid-year intake가 없어 2월 Foundation 시작 기준
  - 2027 Foundation Studies 학비 A$31,400
- Curtin 본과 공식 course URL이 기존 `BH-PHARM`에서 새 `BH-PHARMA` 페이지로 변경된 것을 확인하고 source registry와 fact provenance를 교체했습니다. 새 공식 페이지 기준으로 3년 9개월, 최소 ATAR/Selection Rank 80, Chemistry + Mathematics Applications, IELTS 7.0/각 7.0을 반영했습니다. 현재 페이지는 국제학생 2027 Direct 시작월과 학비를 표시하지 않아 해당 두 항목은 pending으로 유지합니다.
- Curtin College Pharmacy Diploma를 최신 공식 페이지 기준으로 정리:
  - Diploma 완료 후 175 credits 인정
  - Stage 2 CWA 70%
  - PHAR1002 Pharmacy Practice 1을 12월 추가 이수 후 약대 2학년 진학
  - Stage 2 Pharmacy IELTS 6.5 / 각 6.0
  - 한국 Stage 2: 고3 Rank 6 또는 고교 졸업 + CSAT 280/600, Mathematics + Chemistry prerequisite
  - 구 페이지 65%는 현재 메인 공식페이지가 70%를 명시하므로 active conflict에서 제거.
- La Trobe Pharmacy 페이지의 Health Innovation Scholarship 30%를 추가. High Achiever 20–25%와 별도 레코드로 관리.
- Monash Pharmacy Merit는 일반 P6007 전원 장학으로 과장하지 않고 Scholars Program/Doctor of Pharmacy 대상 범위를 유지.
- UNSW는 2027 Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy 명칭 변경을 반영하되, APC 최신 목록은 기존 Master 명칭을 사용하므로 인증 반영 상태를 재확인 대상으로 유지.
- JCU 25% International Excellence는 Pharmacy가 공식 제외목록에 없음을 확인하고 scholarship-specific 공식 링크로 교체.
- Canberra A$42,500은 2027 Guide에 실려 있어도 표 자체가 **2026 Annual Fee**이므로 2027 학비로 승격하지 않음.
- 경쟁사 한국 경로는 공개 페이지·SEO·CTA·source registry에서 제외.

- Monash Foundation: 현재 Monash College destination-degree live page는 새 P6007을 Foundation score 75%, English 65%, Maths 50% + Chemistry 50%로 표시합니다. 반면 2027 Pathway Programs PDF Pharmacy 표에는 legacy P6001이 남아 있어 `source_conflict`로 유지했습니다. Standard 2027 일정은 2월/8월 시작, 약 12개월로 반영했습니다.
- La Trobe: 2027 course page의 Semester 1 · 2027년 3월 시작을 Direct route에도 동기화했습니다. 국제학생 2027 학비는 아직 확정값을 넣지 않았습니다.

- 2026-09-25 추가 점검: Curtin 최신 공식 Pharmacy 페이지는 fees를 “not currently available”, intake를 “No intakes available”로 표시합니다. 따라서 2027 국제학생 학비와 Direct 시작월은 계속 pending으로 유지합니다.
- La Trobe Pharmacy 공식 페이지는 국제학생이 연중 지원 가능하다고 안내하므로 `international_recruitment=true`로 전환하되, 페이지의 2027 정보 변경 가능성 고지와 국제학생 학비 미표시를 감안해 `latest_published`로 보수적으로 처리했습니다.
- Queensland: 2026-27 QSOL consultation은 2026-07-07 종료됐지만 새 QSOL이 아직 공개되지 않았습니다. 공개 중인 onshore list는 2025-26이며 Hospital/Retail Pharmacist는 491만 표시되므로 새 회계연도 확정 자격으로 이식하지 않습니다.

## Source conflict / 적용 범위

| 항목 | 상태 | 처리 |
|---|---|---|
| Newcastle 영어 | source conflict | 6.5/각6.5 vs 7.0/각7.0. 자동 충족 판정 금지, 지원 전 Admissions 서면 확인 |
| Monash Foundation | source conflict | live destination page=P6007 75%/English 65%/Maths·Chemistry 50%, 2027 PDF=legacy P6001. 자동 확정 판정 금지 |
| RMIT 영어 | 적용 범위 pending | Pharmacy 전용 국제학생 적용 확인 전 자동 통과 금지 |
| UQ 신설 PharmD | 승인 pending | APC/Pharmacy Board 승인 완료 전 기존 BPharm 인증을 자동 승계하지 않음 |

## 현재 2027 학비 상태 요약

2027 confirmed: UTas, UQ BPharm, QUT, RMIT, Newcastle, Monash, Sydney, UQ 신설 PharmD.

최신 공개값이지만 2027로 확정하지 않는 항목: JCU(2026), Canberra(2026), UniSQ(2026), UNSW(2026), UWA(2026). Adelaide는 현재 공개값의 연도 적용 범위를 더 확인한다. Curtin·Griffith·La Trobe는 2027 국제학생 Pharmacy 학비를 계속 확인한다.

## QA / 배포 원칙

- GitHub Preview QA와 Netlify Deploy Preview를 매 변경 후 확인한다.
- Preview가 성공하더라도 Production 완료로 보고하지 않는다.
- 사용자 화면 확인 및 최종 승인 후에만 main merge → Production 1회 배포.
- Production 후 commit / Netlify production deploy / 실제 운영 URL 반영을 모두 확인한다.
- 새 디자인·문구·데이터 수정은 같은 PR #1에 계속 누적한다.

## 다음 우선순위

1. 최신 HEAD의 GitHub Preview QA + Netlify Deploy Preview 성공 재확인.
2. Curtin·Griffith·La Trobe의 2027 국제학생 Pharmacy 학비 공식값 확인. Curtin은 새 course page가 현재 fee를 ‘not available’로 표시하므로 추정값을 넣지 않는다.
3. Monash Foundation P6007 2027 progression 범위 확정.
4. 대학별 2027 캠퍼스·기숙사/숙소 실비 자료 보강.
5. 2026-27 주정부 nomination 자료의 현재 공개상태 점검.
6. 모바일/데스크톱 Preview에서 실제 브라우저 시각 QA 후 사용자 확인.
7. 사용자 승인 뒤에만 Production.

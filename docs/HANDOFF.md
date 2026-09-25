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
- 대학 상세페이지 중심: `/universities/`
- 주요 허브: `/admission-pathways/`, `/direct-entry/`, `/foundation/`, `/diploma/`, `/graduate-entry/`, `/tuition-scholarships/`, `/after-graduation/`, `/pharmacist-registration/`

UWA는 비교 대학에 포함하며, 고교 졸업자용 4년 Bachelor of Human Sciences (Pharmaceutical Health) + Doctor of Pharmacy 구조와 대졸자용 Doctor of Pharmacy를 구분한다.

## 데이터 상태

- 2027 확인: 401
- 최신 공개 기준: 408
- 2027 확인 중: 430
- source_conflict fact: 4
- active conflict record: 2

`docs/pending-facts.json`은 현재 `data/catalog.json`에서 다시 생성한 스냅샷이다. 미확정값을 자동 합격/충족으로 판정하지 않는다.

## 2026-09-25 핵심 검증·수정

### Newcastle
- 2027 Pharmacy 학비 **A$51,665**. A$49,205는 2026 금액.
- 2027 Degree Guide IELTS 6.5/각6.5 vs 현재 과정 페이지 7.0/각7.0 → `source_conflict`, 자동 판정 금지.
- 2027 International Excellence Scholarship 20%는 Bachelor of Pharmacy (Honours) 제외.
- CIE Foundation: 한국 고2 수료부터, IELTS 5.5/각5.0, Pharmacy 진급 전체 65%+ 및 Academic English A&B 평균 75%+, 2027 학비 A$31,400.

### Curtin
- 최신 BH-PHARMA 공식 페이지 기준: 3년 9개월, ATAR/Selection Rank 80, Chemistry + Mathematics Applications, IELTS 7.0/각7.0.
- 현재 공식 페이지가 2027 international fee/intake를 제공하지 않아 둘 다 pending.
- Curtin College Pharmacy Diploma: 175 credits, Stage 2 CWA 70%, PHAR1002 추가 이수, Stage 2 IELTS 6.5/각6.0, 한국 Stage 2 학력조건 반영.

### Griffith
- 공개 Diploma 경로는 **Griffith College Diploma of Health Sciences**만 유지.
- 2026/2027 Diploma → Bachelor of Pharmacy (Honours) **80CP** 인정.
- Diploma 기간 **8개월(2 trimesters) 또는 12개월(3 trimesters)**.
- 2027 live key dates: T1 3월 1일 / T2 6월 28일 / T3 10월 25일.
- Pharmacy 연결 영어: IELTS 6.5/각6.0 · PTE 58/각50 · TOEFL 79/각19.
- Pharmacy는 progression quota 대상이며 정원 초과 시 completed Diploma GPA 순 선발.
- 2027 Diploma 정확한 학비는 검증한 공식자료에서 확인하지 못해 pending. 다른 연도 값을 2027로 승격하지 않음.
- 경쟁사 한국 경로는 공개 페이지·source registry·SEO·CTA에서 제외.

### La Trobe
- 2027 course page의 Semester 1 · 2027년 3월 시작 반영.
- 국제학생 지원 가능은 current course page 기준 반영하되 2027 국제학생 학비는 pending.
- Health Innovation Scholarship 30%와 High Achiever 20–25%를 별도 관리.
- Bendigo 숙소 current live 시작가: The Units A$255/week, Villas A$270/week, utilities 포함. 정확한 2027 contract 주수는 pending.

### Monash
- P6007 2027 학비 A$49,740.
- Pharmacy Merit 장학은 일반 P6007 전원 장학으로 표시하지 않고 공식 대상 범위를 유지.
- Foundation live page: P6007 progression 75%, English 65%, Maths 50% + Chemistry 50%.
- 2027 Pathway Programs PDF에는 legacy P6001이 남아 있어 `source_conflict`. Standard 2027 Foundation은 2월/8월 시작, 약 12개월.

### RMIT
- 2027 BPharm(Hons) 학비 **A$49,920**, Semester 1 수업 시작 2027년 3월 1일.
- Pharmacy 영어: IELTS 7.0/각6.5 · PTE 65/각58 · TOEFL 94(R19/L20/S20/W24).
- 한국 학력 Direct 기준과 Chemistry + Mathematics prerequisite를 route에 동기화.
- RMIT Foundation Studies 2027: **A$34,250**, 1년, 2월/7월 시작, IELTS 5.5/각5.0, Year 11 동등 학력 + 평균 50%/pass average + 만 16세.
- 2027 BH102 apply page에서 Associate Degree in Applied Science packaged pathway 확인. 총 5년(Associate 2년 + Pharmacy 3년); exact credit/진입학년은 별도 확인.

### Sydney
- 현재 Pharmacy Course Resolutions 기준 1~4학년 192cp 완료 시 **Bachelor of Pharmacy (Honours)** 수여 가능.
- 따라서 `bachelor_award_year=4`, `four_year_exit=true`, `exit_degree=Bachelor of Pharmacy (Honours)`로 확정.
- 5학년 48cp는 Master of Pharmacy Practice.
- 남은 확인: 2027 Mathematics prerequisite 적용 및 USFP 수학 progression.

### UQ 신설 PharmD
- 2027 Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy 국제학생 모집 확인.
- 5년, 2월 22일 / 7월 26일 시작, 2027 학비 A$60,952.
- IELTS 6.5/각6.0 · PTE 64/각60 · TOEFL 87.
- 2학년부터 700시간+ supervised clinical placement, 4~5학년 compulsory intern training 설계.
- **모집은 확인됐지만 APC accreditation 및 Pharmacy Board approval은 아직 미획득**. route availability=true와 accreditation pending을 분리.
- 새 과정의 CSAT/IB/SAT 등 qualification-specific 점수와 학사 중간 Exit 여부는 pending.

### UNSW / JCU / Canberra
- UNSW 2027 과정명 Doctor of Pharmacy 변경을 반영하되 APC 최신 목록은 기존 Master 명칭이므로 새 명칭의 regulator 반영 상태 재확인.
- JCU 25% International Excellence는 Pharmacy가 공식 제외목록에 없음을 확인.
- Canberra A$42,500은 2027 Guide 안의 표라도 **2026 Annual Fee**이므로 2027 학비로 승격하지 않음.

## Active source conflict

| 항목 | 상태 | 처리 |
|---|---|---|
| Newcastle 영어 | source conflict | 2027 공식자료 6.5/각6.5 vs 7.0/각7.0. 자동 충족 판정 금지 |
| Monash Foundation | source conflict | live P6007 75%/English65%/Maths·Chem50% vs 2027 PDF legacy P6001. 자동 확정 판정 금지 |

RMIT 영어는 더 이상 conflict/pending 항목이 아니다. 현재 공식 Pharmacy-specific English requirement를 반영했다.

## 2027 학비 상태

2027 confirmed: UTas, UQ BPharm, QUT, RMIT, Newcastle, Monash, Sydney, UQ 신설 PharmD.

최신 공개값이지만 2027 확정으로 승격하지 않는 대표 항목: JCU(2026), Canberra(2026), UniSQ(2026), UNSW(2026), UWA(2026). Adelaide는 current page 금액의 연도 적용 범위를 계속 구분한다. Curtin·Griffith·La Trobe는 2027 국제학생 Pharmacy 본과 학비를 계속 확인한다.

## 졸업 후 / nomination

- NSW: current Skills List에서 Pharmacists(ANZSCO unit group 2515) 190·Regional 491 포함.
- Tasmania: 2026-27 program active, Hospital/Industrial/Retail Pharmacist Health/Allied Health 목록 포함.
- ACT: current occupation list에 Hospital/Industrial/Retail Pharmacist 포함, 2026-27 allocation은 별도 확인.
- Queensland: 2026-27 QSOL consultation은 2026-07-07 종료됐지만 새 QSOL 미공개. 2025-26 약사 491 표시를 2026-27 자격으로 자동 이식하지 않음.
- WA·SA·Victoria: 새 회계연도 공고가 확인되기 전 과거 조건을 현재 확정조건으로 표시하지 않음.

## QA / 배포 원칙

- 변경마다 GitHub Preview QA와 Netlify Deploy Preview를 확인한다.
- Preview 성공을 Production 완료로 표현하지 않는다.
- 사용자 최종 승인 전 main merge 금지.
- Production 반영 후에는 commit → Netlify production deploy → 실제 운영 URL을 모두 확인한다.
- 디자인/문구/데이터 수정은 같은 PR #1에 누적한다.

## 다음 우선순위

1. 최신 HEAD의 GitHub Preview QA + Netlify Deploy Preview 재검증.
2. Griffith·Curtin·La Trobe의 2027 국제학생 본과 학비 공식값이 새로 공개됐는지 계속 확인.
3. Monash Foundation P6007 vs 2027 PDF conflict 해소 여부 모니터링.
4. RMIT Associate packaged pathway exact credit/진입학년 및 Foundation stream 세부 선수과목 보강.
5. UQ 신설 PharmD APC/Pharmacy Board 승인 상태 확인.
6. 대학별 2027 숙소 실비와 남은 qualification 환산값 보강.
7. 모바일/데스크톱 Preview 실제 시각 QA 후 사용자 확인.
8. 사용자 승인 뒤에만 Production.

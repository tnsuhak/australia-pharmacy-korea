# TNS 호주약대 2027 · V1 제작 및 인계 보고

기준일: 2026-09-24

**V1 코드와 데이터, 오프라인 검토본을 제작했습니다. GitHub 원격 저장소·PR·Netlify Deploy Preview는 아직 생성되지 않았으며, 실제 브라우저 QA도 남아 있습니다. Production 반영은 하지 않았습니다.**

## 1. Repository

로컬 프로젝트: `australia-pharmacy-korea`. 예정 원격 이름은 `tnsuhak/australia-pharmacy-korea`입니다. 연결된 GitHub에서 동일 목적 저장소를 찾지 못했고 신규 저장소 생성 작업은 현재 연결 기능에서 제공되지 않습니다. 다른 TNS 사이트 저장소나 중앙 설정 저장소에 사이트 코드를 넣지 않았습니다.

중앙 main의 OPERATING_SYSTEM, WEBSITE_BUILD_STANDARD, SEARCH_DISCOVERY_SYSTEM, DATA_STANDARD, policies.yaml, sites.yaml을 확인했습니다. 파일 SHA는 central-baseline.json에 있습니다. 중앙 등록은 아직 하지 않았으며 초안만 docs/central-draft에 포함했습니다.

## 2. Feature branch

`feature/australia-pharmacy-2027-v1` — 로컬 Git 브랜치. 원격 push 전입니다.

## 3. Pull Request

중앙 운영 현황 문서 Draft PR: https://github.com/tnsuhak/tns-site-manager/pull/9 — open, draft, 미병합. 중앙 브랜치는 `feature/australia-pharmacy-2027-v1-status`입니다. 웹사이트 코드 PR과는 별개입니다.

웹사이트 PR은 미생성. PR 본문 초안은 docs/PR_BODY.md에 준비했습니다. 원격 저장소를 만든 다음 최신 main을 기준으로 현재 파일을 feature branch에 반영해야 합니다.

## 4. Netlify Deploy Preview

URL 없음. Git 연결과 PR 배포 전입니다. Preview noindex, robots, sitemap, canonical, Production 승인 보호 설정은 구현했습니다. Production build는 사용자 승인 환경변수와 설정, 확정 도메인이 모두 없으면 실패합니다.

## 5. 생성 페이지

- `/` — 2027 호주 약대 비교 · 내 조건에 맞는 입학경로
- `/compare/` — 2027 호주 약대 비교 · 입학경로·화학·입학시기 필터
- `/universities/jcu-pharmacy/` — 2027 제임스쿡대학교 약대 · 입학조건·경로·학비
- `/universities/utas-pharmacy/` — 2027 태즈메이니아대학교 약대 · 입학조건·경로·학비
- `/universities/curtin-pharmacy/` — 2027 커틴대학교 약대 · 입학조건·경로·학비
- `/universities/uq-pharmacy/` — 2027 퀸즐랜드대학교 약대 · 입학조건·경로·학비
- `/universities/adelaide-pharmacy/` — 2027 애들레이드대학교 약대 · 입학조건·경로·학비
- `/universities/griffith-pharmacy/` — 2027 그리피스대학교 약대 · 입학조건·경로·학비
- `/universities/latrobe-pharmacy/` — 2027 라트로브대학교 약대 · 입학조건·경로·학비
- `/universities/qut-pharmacy/` — 2027 퀸즐랜드공과대학교 약대 · 입학조건·경로·학비
- `/universities/rmit-pharmacy/` — 2027 RMIT대학교 약대 · 입학조건·경로·학비
- `/universities/newcastle-pharmacy/` — 2027 뉴캐슬대학교 약대 · 입학조건·경로·학비
- `/universities/canberra-pharmacy/` — 2027 캔버라대학교 약대 · 입학조건·경로·학비
- `/universities/unisq-pharmacy/` — 2027 서던퀸즐랜드대학교 약대 · 입학조건·경로·학비
- `/universities/monash-pharmacy/` — 2027 모나쉬대학교 약대 · 입학조건·경로·학비
- `/universities/sydney-pharmacy/` — 2027 시드니대학교 약대 · 입학조건·경로·학비
- `/universities/unsw-pharmacy/` — 2027 뉴사우스웨일스대학교 약대 · 입학조건·경로·학비
- `/admission-requirements/` — 2027 호주 약대 입학조건 · 수능·IB·SAT·선수과목
- `/foundation/` — 호주 약대 파운데이션 · 2027 대학별 진급조건
- `/diploma/` — 호주 약대 디플로마 · Griffith·Curtin 학점인정
- `/tuition-scholarships/` — 2027 호주 약대 학비·장학금·숙소 비교
- `/pharmacist-registration/` — 호주 약사 되는 과정 · 학위·인턴십·등록시험
- `/korea-pharmacist/` — 호주 약대 졸업 후 한국 약사면허 · 확인 절차
- `/3-year-pharmacy/` — 호주 3년 약대 · JCU·UTas Fast-track 비교
- `/methodology/` — 자료 기준·2027 업데이트 상태
- `/consult/` — TNS 호주 약대 상담 준비
- `/privacy/` — 개인정보 안내
- `/404/` — 페이지를 찾을 수 없습니다

총 29개 HTML 페이지입니다(404 포함). 28개 콘텐츠 URL을 sitemap에 넣었습니다. 핵심 사실은 HTML에 존재하며 필터 JavaScript만으로 제공되지 않습니다. 모바일 카드, 메뉴, sticky filter, 최대 3개 비교창, 예산 가정 계산기, 상담 준비 복사, OG 이미지와 TNS 파비콘을 포함합니다.

## 6. 포함 대학

James Cook University, University of Tasmania, Curtin University, University of Queensland, Adelaide University, Griffith University, La Trobe University, Queensland University of Technology, RMIT University, University of Newcastle, University of Canberra, University of Southern Queensland, Monash University, University of Sydney, UNSW Sydney.

15개 대학, 16개 프로그램, 27개 입학경로를 저장했습니다. UQ 기존 BPharm과 신설 PharmD를 별도 프로그램으로 관리합니다. 국제학생 모집 등이 미확인인 과정은 확정 추천이 아닌 추가 확인 후보입니다. UWA·CDU·UTS의 대학원 전용 약대는 기본 학부 비교에서 제외했습니다.

## 7. Pending 정보

사실 필드 1117개 중 2027 확인 229개, 최신 공개 기준 247개, 확인 중 639개, source conflict 2개입니다. 이는 중복된 메타 필드를 포함한 데이터 수이며 독립된 입학조건 수나 검증률이 아닙니다.


확인 중에는 '대학 미발표'뿐 아니라 '이번 작업에서 원문 미확보/적용 범위 대조 미완료'도 포함됩니다. 공개되지 않았다고 일괄 단정하지 않았습니다. 필드별 URL·상태·메모는 pending-facts.json에 있습니다.

- 대부분 대학의 2027 CSAT/SAT/IB/A-level/OSSD 환산, 일반고 내신·검정고시 인정
- JCU 등 다수 대학의 2027 Pharmacy 연간 학비 및 수강량
- Foundation별 학력·시작월·전체/영어/수학/화학 진급조건, Diploma 입학 학력과 본과 진급 조건
- Sydney 4년 Exit 및 2027 수학 조건, Monash Foundation 구/신 과정 코드 적용
- UQ 신설 PharmD APC·Board 승인, UNSW 새 학위명 인증 반영
- La Trobe 2027 국제학생 모집과 선수과목, UniSQ 최종 T1 개설 일정
- 다수 장학금의 Pharmacy 적용·한국 국적·제외과정·유지조건
- UTas/La Trobe 외 대부분 대학의 현실적인 공식 숙소와 2027 계약 요금
- 한국 보건복지부 개별 대학 인정 여부와 최신 국시원 세부 절차

Griffith H1 성적표, UniSQ 학비, UTas 영어 및 La Trobe 숙소는 2026 참고값을 2027 확정으로 표시하지 않았습니다. Monash 최상위 경쟁장학과 UNSW의 한국 국적 비대상 일반 장학은 기본 비용에서 차감하지 않습니다.

## 8. Source conflict / 적용 범위 확인

| 항목 | 상태 | 처리 |
|---|---|---|
| Newcastle 영어 | source conflict | 국제학생 상세 IELTS 7.0/각7.0과 다른 6.5 표시 대조 필요. 영어 필터 통과 금지 |
| Curtin College progression | source conflict 기록 | 현재 페이지 CWA70을 우선하고 구 안내65 기록 유지. 최종 입학팀 확인 필요 |
| Monash Foundation | 적용 범위 pending | 구 P6001 progression을 새 P6007에 이식하지 않음 |
| RMIT 영어 | 적용 범위 pending | Pharmacy 전용 영어표의 국제학생 적용 대조 전 자동 통과 금지 |

Newcastle 영어의 2개 fact가 source_conflict 상태입니다. Curtin progression은 최신 페이지를 우선한 값과 별도의 conflict record를 함께 유지합니다.

## 9. QA 결과

- 필터 판정 검사: 24개 통과. 성적 경계값, 이전 연도, 미확인과 불가 구분, 화학, 영어, 입학시기, GE, 장학 국가, 4년 Exit, 통합 인턴십, UQ 신설 인증을 포함합니다.
- 29개 페이지 정적 검사: H1/메타 중복, 로컬 링크·앵커·자산, JSON 파싱, 출처 필드, 프로그램 연결, noindex 및 Production 차단 통과.
- Python 3.11 문법 호환 확인. 외부 패키지 없이 빌드됩니다.
- 모바일: 반응형 카드·표·메뉴·비교창 구현. **실제 화면 크기에서 조작/가로넘침/가독성 QA 미실시.**
- 데스크톱: 정적 검사 통과. **실제 브라우저 시각·조작 QA 미실시.**
- OG: 1200×630 텍스트 그래픽 제작 및 이미지 확인. 웹사이트 스크린샷이 아닙니다.
- 제한: 사용 가능한 브라우저가 로컬 파일 접근을 차단했고 호스팅 Preview가 없어 UI QA를 완료하지 못했습니다. 이 차단을 우회하지 않았습니다.

## 10. Production 전 남은 작업

1. 새 GitHub 저장소 생성. 현재 사용자에게 필요한 최소 단계는 `tnsuhak/australia-pharmacy-korea` 저장소를 만들고 URL을 전달하는 것입니다. 로그인 정보나 토큰은 보내지 않아도 됩니다.
2. 해당 저장소의 최신 main을 기준으로 feature branch 업로드와 PR 생성.
3. Netlify에서 해당 저장소 Git 연결, build/publish 설정 및 PR Deploy Preview 활성화. Production 브랜치 배포는 현재 코드의 승인 보호로 차단됩니다.
4. Preview HTTP 응답·canonical/robots/schema·404·OG 검사와 모바일/데스크톱 주요 흐름 QA. 390px/768px/1440px 권장.
5. 중요 pending과 자료 충돌 검증, TNS 호주 전용 오픈채팅 URL 확인, 기존 3개 상담 목적지 실기 테스트.
6. 중앙 사이트 등록/예외/수동 작업 내역 반영. 실제 repository와 배포 식별자가 확정된 뒤 초안을 적용합니다.
7. 사용자 Preview 검토 후에만 Production 도메인·승인 설정 변경과 main merge 검토.
8. Production 검증 후 Google Search Console·Naver Search Advisor 소유권/사이트맵/색인 및 필요 시 분석 도구 연결.

## 검토본 열기

ZIP 압축을 푼 뒤 `offline-preview/index.html`을 브라우저에서 여세요. 내부 페이지, CSS, 폰트, 필터 스크립트가 함께 들어 있습니다. `dist`는 호스팅용, `offline-preview`는 상대경로 검토용입니다. 어느 쪽도 실제 Netlify Deploy Preview URL을 대체했다고 보고하지 않습니다.


## Netlify preview trigger

- Netlify project linked to GitHub after PR creation.
- This feature-branch update is intended to trigger a Deploy Preview only; do not merge to main yet.


## Site-specific commercial content policy

- Do not promote, link to, create landing pages for, or recommend the Korea-based Griffith pathway operated by UniCentre South Korea.
- Griffith University itself may remain in neutral university comparisons, and independently supportable routes may be shown when appropriate.
- The Korea-based competitor pathway must not appear in badges, filters, comparison tables, homepage features, SEO landing pages, CTAs, or consultation copy.


## 2026-09-25 beginner-first homepage revision

- Homepage order changed to: beginner overview → 3/4/5-year degree structures → Foundation/Diploma/Direct → self-selection by student profile → Finder.
- Finder remains intact but moved below the beginner explanation layer.
- UWA added as the 16th comparison university with a 4-year combined Bachelor + Doctor of Pharmacy pathway.
- UWA general registration still requires a post-graduation supervised internship year and registration requirements; do not treat the 4-year PharmD structure as internship-integrated.
- Graduate Entry remains a separate special route, not a fourth standard school-leaver method.
- Current PR Preview: https://deploy-preview-1--australia-pharmacy-korea.netlify.app
- Production remains unchanged and requires explicit approval.


## 2026-09-25 IA simplification

- Removed the standalone homepage route-self-selection section because it duplicated the three-route explanation. Its shortcuts now sit next to the Finder.
- Replaced the Hero's duplicate 3/4/5-year explainer with a compact comparison-scope summary.
- Added /admission-pathways/ as the real top-level admission-method hub. Header navigation now points there instead of sending the admission-route label to Foundation only.
- Simplified the Compare advanced filter so duration handles 3/4/5-year choices while degree/registration structure is limited to structural distinctions such as 4-year Exit and internship integration.
- Grouped university detail pages from roughly 15 small sections into 8 major sections without dropping the underlying facts.
- Removed the per-university duplicate consultation section because the global TNS consultation CTA follows every page.
- Updated stale Compare copy so UWA's 4-year school-leaver Bachelor + Doctor of Pharmacy is included, while graduate-only routes remain out of the undergraduate comparison.
- Production remains unchanged; review in PR #1 Deploy Preview before merge.


## Plain-language copy rule — 2026-09-25

- User-facing copy must be understood on the first read by a Korean student or parent with no Australia-pharmacy background.
- Lead with the direct outcome: e.g. "Diploma → 약대 2학년", not "대학 1학년 상당 과정 + 학점인정".
- Avoid vague or bureaucratic phrasing such as "상당 과정", "검토", "구조상", "가깝습니다", "이해하면 됩니다", "일 수 있습니다" when a direct statement is supported.
- Put the main fact in the headline/body. Move exceptions or uncertainty into a short secondary note.
- Prefer Korean labels before technical English. Keep English only when it is the actual course/registration term.
- Do not weaken factual safeguards: when official information is genuinely pending, say "발표 대기", "승인 대기", or name the exact missing fact instead of using a vague hedge.
- Keep this rule for all future copy changes in this site.


## 2026-09-25 university-first redesign

- Core product changed from a Finder-centric comparison site to a university-by-university pharmacy analysis site.
- Homepage no longer contains the large Finder. It leads with why Australian pharmacy schools differ, then links directly to all universities.
- Added `/universities/` as the primary directory.
- Added `/graduate-entry/` for verified graduate-entry routes, including UWA's separate 2-year Doctor of Pharmacy.
- Added `/after-graduation/` for 485 / Regional rules and university campus categories.
- Current Home Affairs rule used in Preview: Bachelor and Masters coursework/extended first 485 = 2 years; eligible second 485 adds 1 year in Category 2 or 2 years in Category 3.
- JCU 2027 Pharmacy campuses: Townsville, Cairns, Mackay. UTas 2027 Pharmacy locations: Hobart, Launceston, Cradle Coast.
- University detail pages now include a dedicated "졸업 후 485·지역" section.
- State nomination is intentionally not shown as an automatic outcome; it remains a separate current-policy data layer.
- `/compare/` remains available only as a secondary tool.
- Production remains unchanged. Review the PR #1 Deploy Preview before merge.

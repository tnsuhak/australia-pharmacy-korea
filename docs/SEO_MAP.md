# SEO / Search Intent Map — Australia Pharmacy Korea

Last reviewed: 2026-09-26
Market: South Korea
Language: Korean
Primary engines: Google + Naver
Site state: Deploy Preview / noindex

## Evidence limitations

- No keyword volume, CPC, ranking probability or trend numbers are asserted because verified market-tool data is not currently connected.
- Google/general-web SERP samples were reviewed on 2026-09-26.
- Direct Naver SERP retrieval was not available in the current research tool and Naver Blog/Cafe pages are robots-restricted. Naver SERP review therefore remains an explicit pre/post-launch task rather than being guessed from Google results.
- After Production launch, validate actual impressions/queries with Google Search Console and Naver Search Advisor.

## Search-landscape observations

Current Korean results repeatedly combine these intents:
- broad "호주 약대" overview;
- 2027 school-specific entry requirements and tuition;
- CSAT/direct-entry routes;
- Foundation and Diploma routes for lower scores / missing subjects;
- Korean pharmacist licence questions;
- pharmacist employment / migration;
- individual school pages such as QUT, Griffith and Monash.

Observed competing content often bundles many claims into one long landing page. This site should differentiate through year-labelled official-source data, school-by-school structure, route-specific progression, registration/internship distinctions and explicit uncertainty rather than unsupported "easy admission / guaranteed PR / guaranteed Korean licence" language.

## Query-to-URL map

| Primary intent / query family | Preferred URL | Secondary terms | Page role |
| --- | --- | --- | --- |
| 호주 약대 / 2027 호주 약대 | / | 호주 약학과, 호주 약대 유학 | Main discovery hub; school differences first |
| 호주 약대 대학 / 호주 약대 비교 | /universities/ | 16개 대학, 기간 비교, 약대 리스트 | University directory |
| 호주 약대 입학조건 | /admission-requirements/ | 수능, IB, SAT, A-level, OSSD, 내신, 검정고시, 문과, 선수과목 | One authoritative admissions-intent page; do not split thin pages yet |
| 호주 약대 수능 | /admission-requirements/ | CSAT, 수능 점수 | Sub-intent section + university detail internal links |
| 호주 약대 검정고시 | /admission-requirements/ | GED, Foundation, Diploma | Sub-intent; use route guidance rather than blanket eligibility |
| 문과 호주 약대 | /admission-requirements/ | 화학 없음, 선수과목 없음 | Sub-intent; explain prerequisite vs assumed knowledge |
| 호주 약대 파운데이션 | /foundation/ | Foundation 약대 진급, 고2 유학 | Route hub with progression conditions and timing |
| 호주 약대 디플로마 / 약대 2학년 편입 | /diploma/ | Griffith College, Curtin College, 학점 인정 | Route hub; distinguish real 80CP/175-credit articulation from generic pathway marketing |
| 호주 약대 학비 | /tuition-scholarships/ | 장학금, 기숙사, 유학비용 | Fee / scholarship / housing intent |
| 호주 약대 장학금 | /tuition-scholarships/ | 20%, 25%, 30%, 자동심사 | Same intent cluster; avoid separate thin scholarship URL for now |
| 호주 3년 약대 | /3-year-pharmacy/ | JCU 약대, UTas 약대, 빠른 약대 | Dedicated distinct intent |
| 호주 약사 되는 법 | /pharmacist-registration/ | 약사 등록, 인턴십, ITP, APC, Pharmacy Board | Professional-registration intent |
| 호주 약대 한국 약사면허 | /korea-pharmacist/ | 외국 약대 인정, 예비시험, 국시원 | Korea-return / licence intent |
| 호주 약사 영주권 | /after-graduation/ | 485, Regional, 190, 491, 주정부 nomination | Post-study / migration information intent; no guaranteed-PR claims |
| 대졸자 호주 약대 | /graduate-entry/ | Graduate Entry, Monash GE, UWA PharmD | Graduate-entry intent |
| [대학명] 약대 2027 입학조건 학비 | /universities/<school>-pharmacy/ | 영어, 학비, 장학금, Pathway, 숙소, 485 | School-specific long-tail landing page |

## Architecture decisions

1. Do not create separate thin pages for "수능", "검정고시", "문과" yet. They share the same eligibility intent and should strengthen /admission-requirements/ unless Search Console later shows clearly different demand/CTR behaviour.
2. Keep /foundation/ and /diploma/ separate because their progression/credit mechanics and user questions are materially different.
3. Keep /3-year-pharmacy/ separate because course duration is a distinct decision/search intent.
4. Keep /korea-pharmacist/ separate from /pharmacist-registration/: one is Korean licensing after foreign study, the other is Australian professional registration.
5. Keep /after-graduation/ factual and conditional. Never use "호주 약대 = 영주권 보장" language.
6. University detail pages are the primary long-tail SEO assets. Use full university names plus "약대", year, entry/tution/pathway facts naturally.
7. The Finder is decision support, not the primary SEO surface. Important answers must remain in static HTML.

## Page-copy / metadata review

Current titles already map well to the main intents:
- Home: "2027 호주 약대 가이드 · 대학별 과정·입학방법·485 | TNS"
- Universities: "2027 호주 약대 16개 대학별 상세 비교 | TNS"
- Admissions: "2027 호주 약대 입학조건 · 수능·IB·SAT·선수과목 | TNS"
- Tuition: "2027 호주 약대 학비·장학금·숙소 비교 | TNS"
- 3-year: "호주 3년 약대 · JCU·UTas Fast-track 비교 | TNS"
- Korea licence: "호주 약대 졸업 후 한국 약사면허 · 확인 절차 | TNS"

No title rewrite is recommended solely for keyword repetition at this stage.

## Content gaps to monitor, not blindly add

- verified 2027 university-specific tuition values still pending for several schools;
- current Korean-equivalency tables for schools that only expose older/latest references;
- Newcastle Pharmacy English conflict;
- UQ/UNSW new PharmD accreditation/Board status;
- 2026-27 state nomination program updates;
- user-demand evidence for "순위", "연봉", "취업률" before making dedicated landing pages.

## Launch / measurement checklist

Before Production approval:
- keep Preview noindex;
- confirm production canonical HTTPS URL;
- production robots allow crawl and sitemap points to production canonical;
- verify title/description/H1 uniqueness and internal links (automated QA already covers the technical baseline);
- do representative mobile viewport review;
- test all TNS consultation destinations;
- perform direct Naver SERP review manually or with an accessible source;
- submit sitemap to Google Search Console and Naver Search Advisor after Production;
- use real query/impression data before splitting new SEO pages.

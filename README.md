# TNS · 2027 호주약대 가이드

한국 학생의 학력·과목·영어·입학시기와 Direct / Foundation / Diploma / Graduate Entry를 비교하는 한국어 정적 포털입니다.

현재 상태: PR #1과 Netlify Deploy Preview에서 V1 개편 검토 중. Production 승인·main merge 없음.

## 실행

Python 3.11+와 Node 20+를 사용합니다. 빌드에 외부 패키지가 필요하지 않습니다.

```sh
python3 scripts/build.py
node --test tests/matcher.test.cjs
python3 scripts/validate.py
python3 -m http.server 8080 --directory dist
```

ZIP 안의 `offline-preview/index.html`을 일반 브라우저에서 열어도 전체 내부 페이지를 둘러볼 수 있습니다. 파일 모드의 저장·클립보드 지원은 브라우저에 따라 다릅니다. 실제 서비스 환경 QA는 아직 수행하지 못했습니다.

## 파일 역할

- `data/catalog.json`: 16개 대학, 17개 프로그램과 입학경로·출처를 연결한 데이터
- `data/site.json`: 운영자·승인된 TNS 채널·Production 승인 상태
- `scripts/seed_data.py`: 초기 편집 원본. 수정 후 재생성하면 catalog/site JSON을 덮어씁니다.
- `scripts/build.py`: 홈·비교·입학방법 허브·대학 상세·가이드를 포함한 정적 페이지, robots/sitemap/schema 및 오프라인 미러 생성
- `assets/matcher.js`: 미확정 조건을 통과시키지 않는 필터 판정
- `tests/matcher.test.cjs`: 주요 입학조건 오판 방지 검사 24개
- `docs/HANDOFF.md`: 작업 상태와 남은 배포 절차
- `docs/pending-facts.json`: 필드별 확인 대기 목록
- `docs/sources.md`: 공식자료 목록 및 검색 계획
- `docs/central-draft/`: 중앙 설정에 반영할 초안. 실제 중앙 저장소를 수정한 것은 아닙니다.

## 변경 원칙

반복 숫자를 HTML에 직접 추가하지 말고 데이터와 출처를 수정합니다. 값마다 학년도, 출처 연도, URL, 확인일, 상태를 유지합니다. 이전 연도의 수치를 새 학년도의 확정값으로 변경하지 않습니다. 사이트 업데이트 시 seed와 catalog를 함께 변경하거나 seed를 명시적으로 폐기해야 합니다.

## 배포

Netlify: build `python3 scripts/build.py`, publish `dist`. PR Deploy Preview에서 `DEPLOY_PRIME_URL`을 canonical 기준으로 사용하고 noindex를 유지합니다. `CONTEXT=production`은 환경변수 `PRODUCTION_APPROVED=true`, 설정 파일 승인, 승인된 HTTPS 도메인이 모두 있어야 빌드됩니다. 사용자 승인 전 이 보호 조건을 해제하지 마세요.

브랜치: `feature/australia-pharmacy-2027-v1` · PR #1 · Preview: https://deploy-preview-1--australia-pharmacy-korea.netlify.app

폰트: Noto Sans KR, SIL Open Font License. 라이선스는 assets에 포함되어 있습니다. OG 이미지는 코드로 제작한 텍스트 그래픽입니다. 대학 로고·사진을 임의로 사용하지 않았습니다.


## 정보구조 원칙

- 이 사이트의 중심은 Finder가 아니라 **대학별 약대 상세페이지**입니다.
- 호주 약대 수는 많지 않지만 대학마다 기간, 학위, 입학월, 선수과목, Foundation/Diploma, 인턴십, 485 지역조건이 크게 다르므로 학교 하나씩 깊게 설명합니다.
- 메인은 “호주 약대는 학교마다 다르다” → 대학별 전체 목록 → 입학방법 허브 → 졸업 후 485/Regional → 약사등록 순서입니다.
- `/universities/`와 각 대학 상세페이지가 핵심 탐색 경로입니다. `/compare/` Finder는 보조 도구로 유지합니다.
- Foundation / Diploma / Direct / Graduate Entry 페이지는 같은 입학방법을 가진 대학들을 다시 묶어 보는 허브입니다. 세부 사실의 원본은 대학 상세페이지에 둡니다.
- 대학 상세페이지는 과정·학위 구조 / 입학방법 / Direct 조건 / 비용 / 졸업 후 485·지역 / 호주 약사등록 / 한국 약사면허 / FAQ / 출처를 한 페이지에 모읍니다.
- 485 표시는 현재 Home Affairs 기준을 사용하며, 지역 추가기간은 Second Post-Higher Education Work stream의 별도 자격 충족을 전제로 합니다.
- 주정부 nomination은 대학 위치만으로 자동 가능하다고 표시하지 않고 주별 최신 공고를 별도 관리합니다.
- UWA의 4년 school-leaver Bachelor + Doctor of Pharmacy와 별도 2년 Graduate Entry Doctor of Pharmacy를 구분합니다.

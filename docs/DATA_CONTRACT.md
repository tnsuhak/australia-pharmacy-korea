# 데이터 계약

`catalog.json`의 식별자는 DB의 외래키로 이전할 수 있는 고정 문자열입니다. 대학과 프로그램을 구분하고 UQ 기존 BPharm과 신설 PharmD는 별도 프로그램으로 유지합니다.

컬렉션: universities, programs, entry_routes, qualifications, requirements, english, intakes, tuition, scholarships, accommodation, professional_registration, sources, conflicts.

변동 사실은 `{value, academic_year, source_year, source_id, source_url, source_type, verified_date, status, note}` 구조입니다. `null`은 미확인, `false`는 확인된 부정값으로 구분합니다. 출처 미확보 시 출처 URL과 확인일도 null을 허용하며 확정 판정은 금지합니다.

- confirmed_2027: 2027 문서/과정 기준으로 확인
- latest_published: 확인한 최신 공개 기준. source_year가 2026이면 2026 참고로 노출
- pending_2027: 자료 미확보, 적용 범위 미검증, 향후 발표/인증 대기 포함
- source_conflict: 공식 표시 간 차이가 있어 판정 보류

pending은 '대학이 아직 발표하지 않았다'는 뜻으로 단정하지 않습니다. 웹 접근 실패 또는 본 작업의 대조 미완료도 포함됩니다.

학위기간, 학사 취득 시점, 4년 Exit, Exit 학위, 최종 학위, supervised practice, ITP, 졸업 후 internship은 독립된 필드입니다. Direct 입학성적과 준비과정 입학성적 및 진급성적을 분리합니다. 학비 official_total은 공식 총액만 저장합니다. 화면의 예산 계산은 별도 사용자 가정입니다.

장학금은 자동심사·별도신청·경쟁·국가대상·약대적용·제외과정·유지조건·인원을 구분합니다. 한국 국적 및 Pharmacy 적용이 확인되지 않은 장학금은 비용 필터에서 확정 통과시키지 않습니다.

웹용 JSON은 성능을 위해 판정 필드만 추린 view model입니다. 전체 provenance는 catalog와 정적 상세페이지 출처에 유지합니다. 모든 주요 사실은 JavaScript 실행 전 HTML에도 존재합니다.

미지원 범위: 성적표 자동 업로드/OCR, 대학의 자동 합격 판정, 실시간 환율, 온라인 원서, 개인신상 서버 저장. 상담 준비 내용은 사용자가 직접 복사합니다.

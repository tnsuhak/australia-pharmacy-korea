const test=require('node:test');
const assert=require('node:assert/strict');
const catalog=require('../data/catalog.json');
const {classify}=require('../assets/matcher.js');
function program(id){const p=structuredClone(catalog.programs.find(p=>p.id===id));for(const c of ['requirements','english','intakes','tuition','professional_registration'])p[c]=catalog[c].find(x=>x.program_id===id);for(const c of ['entry_routes','qualifications'])p[c]=catalog[c].filter(x=>x.program_id===id);for(const c of ['scholarships','accommodation'])p[c]=catalog[c].filter(x=>x.university_id===p.university_id);return p;}
const check=(id,f)=>classify(program(id),f);
test('화학 없음: JCU는 검토 가능, Monash Direct는 제외',()=>{assert.equal(check('jcu-bpharm-hons',{chemistry:'no',route:'direct'}).state,'match');assert.equal(check('monash-bpharm-hons',{chemistry:'no',route:'direct'}).state,'excluded');});
test('La Trobe는 현재 공식자료상 별도 과학 선수과목 없음 + 국제학생 지원 가능',()=>{assert.equal(check('latrobe-bpharm-hons',{chemistry:'no'}).state,'match');const t=catalog.tuition.find(x=>x.program_id==='latrobe-bpharm-hons');assert.equal(t.annual.value,null);assert.equal(t.annual.status,'pending_2027');});
test('IELTS 6.5 필터 실제 차등: UQ 통과, Canberra 7.0 제외',()=>{assert.equal(check('uq-bpharm-hons',{english:'6.5'}).state,'match');assert.equal(check('canberra-bpharm-hons',{english:'6.5'}).state,'excluded');});
test('Newcastle 영어 공식자료 충돌은 자동 통과시키지 않음',()=>assert.equal(check('newcastle-bpharm-hons',{english:'7'}).state,'pending'));
test('UTas 2027 영어 IELTS 6.5는 공식 확인값으로 필터 통과',()=>assert.equal(check('utas-bpharm-hons',{english:'6.5'}).state,'match'));
test('Sydney CSAT Pharmacy 346 경계값',()=>{assert.equal(check('sydney-bpharm-hons',{qualification:'csat',score:'346',route:'direct'}).state,'match');assert.equal(check('sydney-bpharm-hons',{qualification:'csat',score:'345',route:'direct'}).state,'excluded');});
test('전체 경로 모드: 낮은 Direct 점수라도 Foundation은 별도 검토',()=>{const r=check('sydney-bpharm-hons',{qualification:'csat',score:'345'});assert.equal(r.state,'pending');assert.ok(r.unknown.some(x=>x.includes('Direct 조건 미충족')));});
test('모든 학교에 수능 숫자를 채우지 않음',()=>assert.equal(check('uq-bpharm-hons',{qualification:'csat',score:'500',route:'direct'}).state,'pending'));
test('Sydney 내신만으로 Direct 평가 불가, Foundation 선택은 개별 확인',()=>{assert.equal(check('sydney-bpharm-hons',{qualification:'korean_high_school',route:'direct'}).state,'excluded');assert.equal(check('sydney-bpharm-hons',{qualification:'korean_high_school',route:'foundation'}).state,'pending');});
test('UQ 7월 빠른 과정과 2월 빠른 과정을 구분',()=>{assert.equal(check('uq-bpharm-hons',{duration:'fast',intake:'7'}).state,'match');assert.equal(check('uq-bpharm-hons',{duration:'fast',intake:'2'}).state,'excluded');});
test('7월 본과와 2월 Accelerated Foundation 시작을 혼동하지 않음',()=>{assert.equal(check('uq-bpharm-hons',{route:'foundation',intake:'2'}).state,'match');assert.equal(check('uq-bpharm-hons',{route:'foundation',intake:'7'}).state,'excluded');});
test('UQ 신설 PharmD는 모집 중이지만 전문인증 미승인 때문에 기본 pending',()=>{assert.equal(catalog.entry_routes.find(x=>x.id==='uq-pharmd-direct').availability.value,true);assert.equal(check('uq-pharmd',{}).state,'pending');});
test('신설 PharmD는 기존 BPharm 수능을 복사하지 않음',()=>assert.equal(check('uq-pharmd',{qualification:'csat',score:'999',route:'direct'}).state,'pending'));
test('등록 실무 통합 필터: Monash는 통합, Adelaide 일반 placement와 UNSW는 별도',()=>{assert.equal(check('monash-bpharm-hons',{structure:'integrated'}).state,'match');assert.equal(check('adelaide-bpharm-hons',{structure:'integrated'}).state,'excluded');assert.equal(check('unsw-bpharm-hons',{structure:'integrated'}).state,'excluded');});
test('4년 Exit: Monash와 Sydney는 공식 학사 Exit 확인',()=>{assert.equal(check('monash-bpharm-hons',{structure:'exit'}).state,'match');assert.equal(check('sydney-bpharm-hons',{structure:'exit'}).state,'match');const p=catalog.programs.find(x=>x.id==='sydney-bpharm-hons');assert.equal(p.bachelor_award_year.value,4);assert.equal(p.exit_degree.value,'Bachelor of Pharmacy (Honours)');});
test('졸업자는 Monash GE도 추가 대학 과목 심사 필요',()=>{assert.equal(check('monash-bpharm-hons',{qualification:'graduate'}).state,'pending');assert.equal(check('jcu-bpharm-hons',{qualification:'graduate'}).state,'excluded');});
test('UNSW 20%는 한국 국적 기본 장학 필터에 포함되지 않음',()=>{assert.equal(check('unsw-bpharm-hons',{cost:'20'}).state,'excluded');assert.equal(check('sydney-bpharm-hons',{cost:'20'}).state,'match');});
test('Curtin 2027 Global Merit 20%는 약대 장학 필터에 포함',()=>assert.equal(check('curtin-bpharm-hons',{cost:'20'}).state,'match'));
test('UWA 2027 Global Excellence 20%는 combined Pharmacy 과정 장학 필터에 포함',()=>{assert.equal(check('uwa-bpharm-hons',{cost:'20'}).state,'match');const r=catalog.entry_routes.find(x=>x.id==='uwa-bpharm-hons-direct');assert.equal(r.progression.value,'Combined degree 내 Doctor of Pharmacy assurance: WAM 65%');});
test('Newcastle 20% International Excellence는 Pharmacy 제외',()=>assert.equal(check('newcastle-bpharm-hons',{cost:'20'}).state,'excluded'));
test('Griffith 공개 Diploma 경로는 Griffith College만 유지',()=>{assert.equal(check('griffith-bpharm-hons',{route:'diploma'}).state,'match');const r=catalog.entry_routes.filter(x=>x.program_id==='griffith-bpharm-hons'&&x.type==='diploma');assert.equal(r.length,1);assert.equal(r[0].id,'griffith-college');assert.equal(r[0].credit.value,80);assert.deepEqual(r[0].intake_months.value,[3,6,10]);assert.match(r[0].duration.value,/8개월/);assert.match(r[0].progression.value,/GPA/);assert.equal(r[0].pathway_fee.status,'pending_2027');assert.equal(catalog.entry_routes.some(x=>x.id==='unicentre-korea'),false);});
test('RMIT Associate Degree는 1년 Diploma가 아니라 2027 packaged 5년 경로',()=>{const r=catalog.entry_routes.find(x=>x.id==='rmit-associate');assert.equal(r.type,'other');assert.equal(r.availability.value,true);assert.equal(r.availability.status,'confirmed_2027');assert.match(r.duration.value,/총 5년/);assert.equal(r.credit.value,96);assert.equal(r.entry_year.value,2);assert.equal(r.pathway_fee.value,38400);assert.match(r.progression.value,/guaranteed entry/);});
test('공식 총학비를 연간금액×기간으로 생성하지 않음',()=>{assert.equal(catalog.tuition.find(x=>x.program_id==='utas-bpharm-hons').official_total.value,198050);assert.equal(catalog.tuition.find(x=>x.program_id==='sydney-bpharm-hons').official_total.value,null);});

test('Canberra 2027 Selection Rank 75 equivalencies: IB 28 / OSSD 74',()=>{assert.equal(check('canberra-bpharm-hons',{qualification:'ib',score:'28',route:'direct'}).state,'match');assert.equal(check('canberra-bpharm-hons',{qualification:'ib',score:'27',route:'direct'}).state,'excluded');assert.equal(check('canberra-bpharm-hons',{qualification:'ossd',score:'74',route:'direct'}).state,'match');});
test('UNSW 2027 international IB threshold is 33, not current domestic-offer IB 36',()=>{assert.equal(check('unsw-bpharm-hons',{qualification:'ib',score:'33',route:'direct'}).state,'match');assert.equal(check('unsw-bpharm-hons',{qualification:'ib',score:'32',route:'direct'}).state,'excluded');});
test('UniSQ 2027 remains a four-year international Trimester 1 program',()=>{assert.equal(check('unisq-bpharm-hons',{duration:'4',intake:'2'}).state,'match');assert.equal(check('unisq-bpharm-hons',{duration:'fast'}).state,'excluded');});
test('Griffith 2026 H1 점수를 2027 충족으로 판정하지 않음',()=>{assert.equal(check('griffith-bpharm-hons',{qualification:'csat',score:'400',route:'direct'}).state,'pending');assert.equal(check('griffith-bpharm-hons',{qualification:'csat',score:'200',route:'direct'}).state,'pending');});
test('Curtin 3년 9개월과 졸업 후 internship 구별',()=>{assert.equal(check('curtin-bpharm-hons',{structure:'3.75'}).state,'match');assert.equal(check('curtin-bpharm-hons',{structure:'integrated'}).state,'excluded');});
test('UniSQ 2027은 3년 가속 과정으로 포함하지 않음',()=>assert.equal(check('unisq-bpharm-hons',{duration:'fast'}).state,'excluded'));
test('Sydney Pharmacy는 Mathematics prerequisite, Chemistry·Biology assumed knowledge',()=>{const r=catalog.requirements.find(x=>x.program_id==='sydney-bpharm-hons');assert.equal(r.mathematics.value,'required');assert.equal(r.chemistry.value,'assumed');assert.equal(r.biology.value,'assumed');assert.equal(r.physics.value,'recommended');});
test('JCU 2027 캠퍼스는 확인하되 A$31,710은 2026 학비로만 유지',()=>{const u=catalog.universities.find(x=>x.id==='jcu');const t=catalog.tuition.find(x=>x.program_id==='jcu-bpharm-hons');assert.equal(u.campus.status,'confirmed_2027');assert.match(u.campus.value,/Mackay/);assert.equal(t.annual.value,31710);assert.equal(t.annual.source_year,2026);assert.equal(t.annual.status,'latest_published');});
test('UTas Pharmacy Foundation은 2027 Standard와 Fast-track을 구분',()=>{const r=catalog.entry_routes.filter(x=>x.program_id==='utas-bpharm-hons'&&x.type==='foundation');assert.equal(r.length,2);const std=r.find(x=>x.id==='utas-foundation-standard');const fast=r.find(x=>x.id==='utas-foundation-fast');assert.equal(std.pathway_fee.value,21975);assert.equal(fast.pathway_fee.value,25450);assert.match(std.progression.value,/FCWAM 60%/);assert.match(std.qualification.value,/고2/);assert.deepEqual(std.intake_months.value,[2,6,10]);});

test('QUT 수학·화학은 필수 prerequisite가 아니라 assumed knowledge',()=>{const p=program('qut-bpharm-hons');assert.equal(p.requirements.chemistry.value,'assumed');assert.equal(p.requirements.mathematics.value,'assumed');assert.equal(check('qut-bpharm-hons',{chemistry:'no',route:'direct'}).state,'match');});
test('UniSQ 2027 국제학생은 T1 2월 시작, accelerated는 2028부터',()=>{const p=program('unisq-bpharm-hons');assert.deepEqual(p.intakes.months.value,[2]);assert.equal(check('unisq-bpharm-hons',{intake:'2'}).state,'match');assert.equal(check('unisq-bpharm-hons',{duration:'fast'}).state,'excluded');});

test('Adelaide 2027 ATAR 90/IB 35.25는 확정하고 한국 CSAT 환산은 재사용하지 않음',()=>{
  assert.equal(check('adelaide-bpharm-hons',{qualification:'csat',score:'999',route:'direct'}).state,'pending');
  assert.equal(check('adelaide-bpharm-hons',{qualification:'ib',score:'35.25',route:'direct'}).state,'match');
  const route=catalog.entry_routes.find(x=>x.id==='adelaide-bpharm-hons-direct');
  assert.deepEqual(route.intake_months.value,[2,7]);
  assert.match(route.qualification.value,/Guaranteed ATAR 90/);
  const t=catalog.tuition.find(x=>x.program_id==='adelaide-bpharm-hons');
  assert.equal(t.annual.value,52200);
  assert.equal(t.annual.source_year,2026);
  assert.equal(t.annual.status,'latest_published');
});


test('3월 본과 필터가 RMIT와 La Trobe를 찾는다',()=>{
  assert.equal(check('rmit-bpharm-hons',{intake:'3'}).state,'match');
  assert.equal(check('latrobe-bpharm-hons',{intake:'3'}).state,'match');
  assert.equal(check('rmit-bpharm-hons',{intake:'2'}).state,'excluded');
});

test('Sydney USFP 2027 Standard와 Intensive를 분리하고 학비를 구분',()=>{
  const routes=catalog.entry_routes.filter(x=>x.program_id==='sydney-bpharm-hons'&&x.type==='foundation');
  assert.equal(routes.length,2);
  assert.equal(routes.find(x=>x.id==='sydney-usfp').pathway_fee.value,49800);
  assert.equal(routes.find(x=>x.id==='sydney-usfp-intensive').pathway_fee.value,47690);
  assert.match(routes.find(x=>x.id==='sydney-usfp').progression.value,/Mathematics/);
});

test('UWA Foundation 8개월과 12개월 영어·한국 학력표를 구분',()=>{
  const eight=catalog.entry_routes.find(x=>x.id==='uwa-foundation-8');
  const twelve=catalog.entry_routes.find(x=>x.id==='uwa-foundation-12');
  assert.match(eight.english.value,/6\.0/);
  assert.match(twelve.english.value,/5\.5/);
  assert.match(eight.qualification.value,/CSAT 260/);
  assert.match(twelve.qualification.value,/CSAT 230/);
  assert.equal(eight.qualification.source_year,2025);
});

test('Adelaide 영어 동등점수와 BPharm registration internship 구조를 분리',()=>{
  const e=catalog.english.find(x=>x.program_id==='adelaide-bpharm-hons');
  const r=catalog.professional_registration.find(x=>x.program_id==='adelaide-bpharm-hons');
  assert.equal(e.pte_overall.value,64);
  assert.equal(e.pte_each.value,60);
  assert.equal(e.toefl.value.overall,79);
  assert.equal(r.supervised_practice_in_degree.value,true);
  assert.equal(r.itp_in_degree.value,false);
  assert.equal(r.post_graduation_internship.value,true);
});

test('Canberra 10~30% 국제장학은 Pharmacy 제외목록이 아니고 자동심사',()=>{
  const s=catalog.scholarships.find(x=>x.id==='canberra-international-2027');
  assert.equal(s.automatic_assessment.value,true);
  assert.equal(s.separate_application.value,false);
  assert.equal(s.pharmacy_eligible.value,true);
  assert.match(s.renewal_condition.value,/5\.0/);
  assert.equal(check('canberra-bpharm-hons',{cost:'20'}).state,'match');
});

test('UniSQ 2027 10% 장학은 Pharmacy 대상이지만 offshore/non-award는 제외',()=>{
  const s=catalog.scholarships.find(x=>x.id==='unisq-support');
  assert.equal(s.pharmacy_eligible.value,true);
  assert.match(s.course_exclusion.value,/offshore/);
  assert.equal(check('unisq-bpharm-hons',{cost:'scholarship'}).state,'match');
});

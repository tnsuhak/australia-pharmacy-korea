"""Reproducible, source-linked editorial seed. Run only when regenerating catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-25'
sources = {}
def source(key, title, url, year=None, kind='official_course'):
    sources[key] = dict(id=key, title=title, url=url, source_year=year,
                        source_type=kind, verified_date=DATE)
    return key
def fact(value=None, src=None, year=None, status=None, note=''):
    s=sources.get(src,{})
    return dict(value=value, academic_year=2027, source_year=year or s.get('source_year'),
                source_id=src, source_url=s.get('url'), source_type=s.get('source_type'),
                verified_date=DATE if src else None,
                status=status or ('pending_2027' if value is None else 'confirmed_2027' if (year or s.get('source_year'))==2027 else 'latest_published'),
                note=note)

source('apc','APC 호주 약학 학위 인증 목록 · 2026-07-08 기준','https://www.pharmacycouncil.org.au/education-provider/accreditation/pharmacy-degree-programs-australia/accredited-pharmacy-degree-programs/',2026,'accreditation')
source('board','Pharmacy Board · Internships','https://www.pharmacyboard.gov.au/Registration/Internships.aspx',None,'regulator')
source('apc-exam','APC · Intern written examination','https://www.pharmacycouncil.org.au/pharmacist/skills-assessment/intern-written-exam/',None,'regulator')
source('korea-law','약사법 제3조 · 2026-09-11 시행','https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000328184',2026,'government')
source('kuksiwon','국시원 · 외국대학 인정기준','https://www.kuksiwon.or.kr/infoOpen/list.do?seq=82',None,'government')
course_urls={
 'jcu':'https://www.jcu.edu.au/courses/bachelor-of-pharmacy-honours',
 'utas':'https://www.utas.edu.au/courses/health/courses/54d-bachelor-of-pharmacy-with-honours',
 'curtin':'https://www.curtin.edu.au/study/offering/course-ug-bachelor-of-pharmacy-honours--bh-pharm/?region=int',
 'uq':'https://study.uq.edu.au/study-options/programs/bachelor-pharmacy-honours-2373',
 'uq-pharmd':'https://study.uq.edu.au/study-options/programs/bachelor-pharmaceutics-and-therapeutic-science-doctor-pharmacy-2577?year=2027',
 'adelaide':'https://adelaide.edu.au/study/degrees/bachelor-of-pharmacy-honours/',
 'griffith':'https://www.griffith.edu.au/study/degrees/bachelor-of-pharmacy-honours-1614',
 'latrobe':'https://www.latrobe.edu.au/courses/bachelor-of-pharmacy-honours',
 'qut':'https://www.qut.edu.au/courses/bachelor-of-pharmacy-honours',
 'rmit':'https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/honours-degrees/bachelor-of-pharmacy-honours-bh102',
 'newcastle':'https://www.newcastle.edu.au/degrees/bachelor-of-pharmacy-honours',
 'canberra':'https://www.canberra.edu.au/about-uc/faculties/health/study/pharmacy',
 'unisq':'https://course-offer-guide.unisq.edu.au/2027/BPHH.html',
 'monash':'https://www.monash.edu/study/courses/find-a-course/pharmacy-p6007',
 'sydney':'https://www.sydney.edu.au/dam/corporate/documents/study/how-to-apply/international-admission-guide.pdf',
 'unsw':'https://www.unsw.edu.au/study/undergraduate/bachelor-of-pharmaceutical-medicine-master-of-pharmacy',
 'uwa':'https://www.uwa.edu.au/study/courses/bachelor-of-human-sciences-pharmaceutical-health-and-doctor-of-pharmacy'}
for k,v in course_urls.items(): source(k,k.upper()+' Pharmacy · 공식 과정/입학 안내',v,2027 if k in ['utas','uq','uq-pharmd','unisq','monash','sydney'] else None)
source('jcu-guide','JCU 2027 Undergraduate Guide','https://www.jcu.edu.au/__data/assets/pdf_file/0010/2316889/2027-Undergraduate-Guide.pdf',2027,'official_guide')
source('utas-2026','UTas 2026 Pharmacy course','https://www.utas.edu.au/courses/health/courses/54d-bachelor-of-pharmacy-with-honours?year=2026',2026)
source('qut-guide','QUT 2027 international Year 12 guide','https://cms.qut.edu.au/__data/assets/pdf_file/0003/1566471/27516-Year-12-International-Guide-2027_DIGITAL_F.pdf',2027,'official_guide')
source('rmit-english','RMIT · Minimum English language requirements','https://www.rmit.edu.au/study-with-us/applying-to-rmit/local-student-applications/entry-requirements/minimum-english-language-requirement',None,'official_admissions')
source('sydney-structure','Sydney Pharmacy · Course resolutions','https://www.sydney.edu.au/handbooks/medicine-health/coursework/pharmacy/course-resolutions.html',None,'official_handbook')
source('sydney-guide','Sydney international guide','https://www.sydney.edu.au/dam/corporate/documents/study/guides/usyd-international-guide.pdf',2027,'official_guide')
source('griffith-korea','Griffith · UniCentre South Korea articulation 107341','https://credit-precedent.sds.na.ce.griffith.edu.au/credit_detail.php?pk1=107341',2027,'official_articulation')
source('griffith-college','Griffith · College articulation 107343','https://credit-precedent.sds.na.ce.griffith.edu.au/credit_detail.php?pk1=107343',2027,'official_articulation')
source('curtin-college','Curtin College · Pharmacy Diploma','https://www.curtincollege.edu.au/courses/diplomas/health-sciences/pharmacy/',None,'official_pathway')
source('curtin-old','Curtin College · 旧 course information','https://sites.google.com/a/study.curtincollege.edu.au/courseinformation/Courses/testdhsi/pharmacy',None,'official_pathway')
source('uq-foundation','UQ College · Foundation progression','https://uqcollege.uq.edu.au/study/pathways-uq/foundation-program',None,'official_pathway')
source('uq-accelerated','UQ College · Accelerated Foundation','https://uqcollege.uq.edu.au/study/pathways-uq/foundation-program/accelerated-foundation-program',2027,'official_pathway')
source('uq-calendar','UQ College · Academic calendar','https://uqcollege.uq.edu.au/current-students/academic-calendar',2027,'official_calendar')
source('monash-foundation','Monash Pathway Programs 2027 · 과정 코드 재확인 필요','https://www.monashcollege.edu.au/__data/assets/pdf_file/0005/4349102/2027-Monash-Pathway-Programs.pdf',2027,'official_pathway')
source('newcastle-foundation','University of Newcastle International College · Foundation','https://internationalcollege.newcastle.edu.au/foundation-studies',None,'official_pathway')
source('rmit-pathway','RMIT 2026 degree and diploma guide','https://www.rmit.edu.au/content/dam/rmit/au/en/docs/study/career-advisers/brochures/2026-degree-diploma-guide-rmit-university.pdf',2026,'official_guide')
source('griffith-scholarship','Griffith International Academic Merit Scholarship','https://www.griffith.edu.au/international/scholarships-finance/scholarships/international-academic-merit-scholarship',2027,'official_scholarship')
source('monash-scholarship','Monash Pharmacy and Pharmaceutical Science International Merit Scholarship','https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/pharmacy-international-merit-scholarship-5745',None,'official_scholarship')
source('sydney-scholarship','Sydney International Student Award 2027','https://www.sydney.edu.au/study/fees-and-loans/scholarships/sydney-international-student-award.html',2027,'official_scholarship')
source('unsw-scholarship','UNSW International Student Award · 국가 목록','https://www.scholarships.unsw.edu.au/sites/default/files/2026-04/International%20Student%20Award_List%20of%20Eligible%20Countries.pdf',2026,'official_scholarship')
source('newcastle-scholarship','Newcastle International Excellence Scholarship 2027','https://www.newcastle.edu.au/scholarships/UNI_053',2027,'official_scholarship')
source('jcu-scholarship','JCU · International scholarships','https://www.jcu.edu.au/international-students/scholarships-and-financial-aid',None,'official_scholarship')
source('utas-housing','UTas · Hobart accommodation 2027','https://www.utas.edu.au/uni-life/accommodation/hobart',2027,'official_accommodation')
source('utas-christ','UTas · Christ College','https://www.utas.edu.au/uni-life/accommodation/hobart/christ-college',2027,'official_accommodation')
source('latrobe-housing','La Trobe · Bendigo accommodation rates 2026','https://www.latrobe.edu.au/__data/assets/pdf_file/0008/1388663/Bendigo-Accommodation-Rates-2026.pdf',2026,'official_accommodation')
source('latrobe-units','La Trobe · The Units','https://www.latrobe.edu.au/accommodation/bendigo-campus/units',None,'official_accommodation')

university_rows=[
 ('jcu','James Cook University','제임스쿡대학교','QLD','Townsville · Cairns · Mackay','JCU'),
 ('utas','University of Tasmania','태즈메이니아대학교','TAS','Tasmania · 국제학생 캠퍼스 확인','UTas'),
 ('curtin','Curtin University','커틴대학교','WA','Perth · Bentley','Curtin'),
 ('uq','University of Queensland','퀸즐랜드대학교','QLD','Brisbane · Dutton Park','UQ'),
 ('adelaide','Adelaide University','애들레이드대학교','SA','Adelaide','Adelaide'),
 ('griffith','Griffith University','그리피스대학교','QLD','Gold Coast','Griffith'),
 ('latrobe','La Trobe University','라트로브대학교','VIC','Bendigo','La Trobe'),
 ('qut','Queensland University of Technology','퀸즐랜드공과대학교','QLD','Brisbane · Gardens Point','QUT'),
 ('rmit','RMIT University','RMIT대학교','VIC','Melbourne · Bundoora','RMIT'),
 ('newcastle','University of Newcastle','뉴캐슬대학교','NSW','Newcastle','Newcastle'),
 ('canberra','University of Canberra','캔버라대학교','ACT','Canberra','Canberra'),
 ('unisq','University of Southern Queensland','서던퀸즐랜드대학교','QLD','Toowoomba','UniSQ'),
 ('monash','Monash University','모나쉬대학교','VIC','Melbourne · Parkville','Monash'),
 ('sydney','University of Sydney','시드니대학교','NSW','Sydney · Camperdown','Sydney'),
 ('unsw','UNSW Sydney','뉴사우스웨일스대학교','NSW','Sydney · Kensington','UNSW'),
 ('uwa','The University of Western Australia','서호주대학교','WA','Perth · Crawley','UWA')]
universities=[dict(id=i,name=n,name_ko=k,state=s,campus=fact(c,'apc' if i not in ['uq','qut','monash'] else i),short=short,slug=i+'-pharmacy') for i,n,k,s,c,short in university_rows]
programs=[]; qualifications=[]; requirements=[]; english=[]; intakes=[]; tuition=[]; registration=[]; routes=[]; scholarships=[]; accommodation=[]
for u in universities:
 i=u['id']; p=i+'-bpharm-hons'
 title='Bachelor of Pharmacy (Honours)'
 if i=='utas': title='Bachelor of Pharmacy with Honours'
 if i=='monash': title='Bachelor of Pharmacy (Honours) / Doctor of Pharmacy'
 if i=='sydney': title='Bachelor of Pharmacy (Honours) / Master of Pharmacy Practice'
 if i=='unsw': title='Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy'
 if i=='uwa': title='Bachelor of Human Sciences (Pharmaceutical Health) / Doctor of Pharmacy'
 duration=3 if i in ['jcu','utas'] else 5 if i in ['monash','sydney','unsw'] else 4
 src='jcu-guide' if i=='jcu' else i if i in ['utas','uq','monash','sydney','uwa'] else 'apc'
 programs.append(dict(id=p,university_id=i,name=fact(title,i),duration_years=fact(duration,src),
   duration_label=fact('3년 Fast-track' if duration==3 else '5년 통합' if duration==5 else '4년',src),
   bachelor_award_year=fact(4,'monash') if i=='monash' else fact(None,i,note='학사 수여 시점과 통합과정 종료를 별도 확인') if duration==5 else fact(duration,src),
   four_year_exit=fact(True,'monash') if i=='monash' else fact(None,i) if duration==5 else fact(False,src,note='통합 5년 과정의 중간 Exit와 구분'),
   exit_degree=fact('Bachelor of Pharmacy (Honours)','monash') if i=='monash' else fact(None,i),
   final_degree=fact(title,i),
   international_recruitment=fact(True,i) if i in ['jcu','utas','uq','adelaide','griffith','qut','rmit','newcastle','unisq','monash','sydney','unsw','curtin','uwa'] else fact(None,i,note='2027 국제학생 모집·대면 과정 최종 확인 중'),
   accreditation=fact('APC accredited with conditions' if i in ['curtin','qut','newcastle','unisq','unsw'] else 'APC accredited','apc',note='2026-07-08 목록. 학위명 변경·캠퍼스·갱신은 지원 전 재확인.'),
   highlights=[], editorial='', review_items=[]))
 for q in ['csat','sat','ib','alevel','ossd','korean_high_school','ged','other']:
  qualifications.append(dict(id=p+'-'+q,program_id=p,qualification=q,score=fact(None,i,note='Pharmacy 전용 2027 환산 기준 확인 중'),scale=None,calculation=None))
 requirements.append(dict(program_id=p,chemistry=fact(None,i),mathematics=fact(None,i),biology=fact(None,i),physics=fact(None,i),minimum_grade=fact(None,i)))
 english.append(dict(program_id=p,ielts_overall=fact(None,i),ielts_bands=fact(None,i),pte_overall=fact(None,i),pte_each=fact(None,i),toefl=fact(None,i)))
 intakes.append(dict(program_id=p,route_id=p+'-direct',months=fact(None,i),label=fact(None,i)))
 tuition.append(dict(program_id=p,annual=fact(None,i),official_total=fact(None,i),currency='AUD',load_basis=fact(None,i),increase_note='연도별 인상 및 실제 수강량에 따라 달라질 수 있습니다.'))
 integrated=i in ['monash','sydney']
 rsrc=i if integrated or i in ['uq','rmit','newcastle','utas','unsw','uwa'] else 'apc'
 registration.append(dict(program_id=p,supervised_practice_in_degree=fact(integrated,rsrc) if integrated or i in ['uq','utas','rmit','unsw','uwa'] else fact(None,i),
   itp_in_degree=fact(integrated,rsrc) if integrated or i in ['uq','utas','rmit','unsw','uwa'] else fact(None,i),
   post_graduation_internship=fact(not integrated,rsrc) if integrated or i in ['uq','utas','rmit','unsw','uwa'] else fact(None,i),
   provisional_registration=fact('실습 시작 전 Board 승인·등록 요건 확인','apc-exam'),
   exams=fact('등록 필기·구술시험 및 일반등록 심사 별도','apc-exam'),
   note='학위 취득만으로 호주 약사 일반등록이 자동 완료되지는 않습니다.'))
 routes.append(dict(id=p+'-direct',program_id=p,type='direct',title='Direct · 본과 1학년',availability=fact(True,i),credit=fact(0,i),
   entry_year=fact(1,i),duration=fact(None,i),intake=fact(None,i),progression=fact(None,i),english=fact(None,i),qualification=fact(None,i),note='학력·성적, 선수과목, 영어조건을 각각 충족해야 합니다.'))

def row(collection,p): return next(x for x in collection if x['program_id']==p+'-bpharm-hons')
def prog(i): return next(x for x in programs if x['university_id']==i)
def setp(i,**kwargs): prog(i).update(kwargs)
def req(i,chem=None,math=None,bio=None,physics=None,grade=None,src=None):
 r=row(requirements,i); src=src or i
 for k,v in [('chemistry',chem),('mathematics',math),('biology',bio),('physics',physics),('minimum_grade',grade)]:
  if v is not None:r[k]=fact(v,src)
def eng(i,overall,bands,src=None,pte=None,pte_each=None,toefl=None,status=None):
 r=row(english,i); src=src or i
 for k,v in [('ielts_overall',overall),('ielts_bands',bands),('pte_overall',pte),('pte_each',pte_each),('toefl',toefl)]:
  if v is not None:r[k]=fact(v,src,status=status)
def intake(i,months,label,src=None): row(intakes,i).update(months=fact(months,src or i),label=fact(label,src or i))
def fee(i,amount,src=None,year=None,total=None,load='표준 연간 수강량 기준'):
 r=row(tuition,i); r.update(annual=fact(amount,src or i,year),load_basis=fact(load,src or i,year))
 if total:r['official_total']=fact(total,src or i,year)
def qual(i,q,score,scale,calc=''):
 r=next(x for x in qualifications if x['program_id']==i+'-bpharm-hons' and x['qualification']==q)
 r.update(score=fact(score,i),scale=scale,calculation=calc)

setp('jcu',highlights=['3년 Fast-track','화학 권장','2월 입학'],editorial='고교 화학이 필수 선수과목은 아닙니다. 압축된 학사 일정과 수학·영어 준비를 함께 살펴보세요.',review_items=['2027 국제학생 캠퍼스별 모집','3년 개편 과정의 국제학생 연간 학비','한국 학력 환산표'])
req('jcu','recommended','required',grade='English와 General Mathematics 또는 동등 수준. Chemistry 권장.',src='jcu-guide'); intake('jcu',[2],'2월','jcu-guide')
setp('utas',highlights=['3년 Fast-track','2027 학비 공개','Hobart 숙소'],editorial='4년 상당의 학습량을 3년에 이수합니다. 연간 수강량이 일반 1년과 달라 단순 연간 학비 비교에 주의해야 합니다.')
fee('utas',61267,total=198050,load='연간 133 credit points 기준'); eng('utas',6.5,{'L':6,'R':6,'W':6,'S':6},src='utas-2026')
setp('curtin',highlights=['College → Year 2','175 credits','진급 CWA 확인'],editorial='College Pharmacy Diploma는 인정학점 외에 12월 추가 Pharmacy unit이 필요합니다. CWA와 실제 학사 일정을 함께 확인하세요.',review_items=['약 3년 9개월 운영 일정 재확인','국제학생 2027 학비','Global Merit의 Pharmacy 제외 여부'])
setp('uq',duration_label=fact('2월 4년 · 7월 약 3.5년','uq'),highlights=['2월 4년','7월 3.5년','Accelerated Foundation'],editorial='기존 BPharm은 입학 학기에 따라 일정이 다릅니다. 신설 통합 PharmD와 별도 과정으로 비교하세요.')
req('uq','required','required','recommended',grade='English·수학·Chemistry: Queensland Year 12 C 또는 동등 수준.'); intake('uq',[2,7],'2월 22일 / 7월 26일'); fee('uq',60952,load='16 units 기준')
eng('uq',6.5,{'L':6,'R':6,'W':6,'S':6},pte=64,pte_each=60,toefl={'overall':87,'L':19,'R':19,'W':21,'S':19})
setp('adelaide',highlights=['4년 학사','7월은 학점인정 조건부'],editorial='7월 입학은 일반 고졸 Direct 입학으로 단정할 수 없습니다. 기존 학점 인정이 있는 국제학생에 대한 개별 검토 조건을 확인하세요.')
intake('adelaide',[2],'2월 · 7월은 학점 인정 시 개별 심사')
setp('griffith',highlights=['한국 Diploma','80CP 인정','20% 자동심사'],editorial='Direct, Griffith College, 한국 UniCentre 경로를 비교할 수 있습니다. 80CP 인정과 최종 입학허가는 별도입니다.')
setp('latrobe',highlights=['Bendigo','4년 학사','숙소 2026 참고'],editorial='Bendigo 약학 과정과 숙소를 함께 비교합니다. 화학을 일괄 필수로 처리하지 않고 2027 선수과목 확인 상태를 표시합니다.',review_items=['2027 국제학생 모집','2027 선수과목·영어·학비','Health Innovation 및 High Achiever 약대 적용'])
setp('qut',highlights=['수학 + 화학','4년 학사','영어 조건 비교'],editorial='수학과 화학 선수과목을 별도로 검토해야 합니다. 영어는 Pharmacy 과정 페이지의 기준을 비교합니다.')
req('qut','required','required',grade='Mathematical Methods 계열 및 Chemistry 동등 과목 확인',src='qut-guide'); eng('qut',6.5,{'L':6,'R':6,'W':6,'S':6},pte=58,pte_each=50,toefl={'overall':79,'L':16,'R':16,'W':21,'S':18})
setp('rmit',highlights=['4년 학사','2027 학비 공개','Other Pathway'],editorial='일반 학부 영어기준을 약대에 적용하지 않습니다. Associate Degree 연계는 1년 Diploma와 구분해 검토합니다.')
req('rmit','required','required',grade='VCE Chemistry 25, Mathematics 25 또는 인정되는 동등 수준.'); fee('rmit',49920,year=2027)
eng('rmit',7,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='rmit-english',status='pending_2027')
for k in ['ielts_overall','ielts_bands']:row(english,'rmit')[k]['note']='Pharmacy 전용 표는 확인. 국제학생 course 조건과 적용 범위 대조 완료 전 자동 충족 판정 제외.'
setp('newcastle',highlights=['4년 학사','Foundation 연계','영어 재확인'],editorial='영어조건의 자료 차이를 숨기지 않습니다. 국제학생 Pharmacy 페이지와 2027 안내서 기준의 일치 여부를 재확인해야 합니다.',review_items=['Pharmacy 영어조건 자료 충돌','2027 CSAT·SAT·IB course-specific 값','APC 인증 갱신: 현재 목록 종료일 2026-12-31'])
eng('newcastle',7,{'L':7,'R':7,'W':7,'S':7},status='source_conflict')
for k in ['ielts_overall','ielts_bands']:row(english,'newcastle')[k]['note']='과정 페이지 국제학생 상세 7.0/각7.0, 다른 표시 6.5. 2027 입학팀 서면 확인 필요.'
intake('newcastle',[2],'Semester 1 · 2월')
setp('canberra',highlights=['Canberra','학부 약학 과정','모집 확인 중'],editorial='APC 학부 약학 인증 목록과 실제 국제학생 모집은 서로 다른 확인 항목입니다. 2027 국제학생 course offer를 확인 중입니다.')
setp('unisq',highlights=['T1 only','Toowoomba','2027 개설표'],editorial='2027 국제학생 대면 수업은 Trimester 1에 표시됩니다. 개설 안내서는 9월 28일 확정 예정이므로 최종 일정 확인이 필요합니다.')
intake('unisq',None,'2027 국제학생 Trimester 1 only · 최종 개설 확정 대기')
row(intakes,'unisq')['months']=fact(None,'unisq',note='T1 시작월을 달력과 대조 후 확정')
setp('monash',highlights=['4년 Exit','5년 PharmD','Internship 통합'],editorial='4년 학사 Exit와 5년 통합 완료를 구분합니다. 관련 학사 졸업자는 Graduate Entry도 함께 검토할 수 있습니다.')
req('monash','required','required',grade='VCE Methods/Specialist Maths 25 + Chemistry 25. IB Math AA SL4 또는 AA/AI HL3, Chemistry SL4 또는 HL3.'); intake('monash',[2],'2월')
setp('sydney',highlights=['5년 통합','2027 환산표','Internship 통합'],editorial='2027 국제학생 Pharmacy 행의 성적과 학비를 사용합니다. 5년차 실무 과정과 학사 Exit 조건은 따로 확인하세요.',review_items=['4년 학사 Exit 조건과 학위명','2027 Mathematics prerequisite 적용 여부','USFP 수학 progression 조건'])
eng('sydney',6.5,{'L':6,'R':6,'W':6,'S':6},toefl={'overall':85,'bands_note':'공식표 각영역 17/19 구분 상세 확인'}); intake('sydney',[2],'2월'); fee('sydney',63600)
qual('sydney','csat',346,'표준점수 4개 합','국어 + 수학 + 사회/과학 탐구 상위 2개 과목의 표준점수 합. 등급이나 백분위 합계가 아닙니다.')
qual('sydney','sat',1300,'1600'); qual('sydney','ib',31,'45'); qual('sydney','alevel',14,'대학 환산점수','3과목/4과목 각각 14. A-level 성적을 대학 공식 환산식으로 계산해야 합니다.')
q=next(x for x in qualifications if x['program_id']=='sydney-bpharm-hons' and x['qualification']=='korean_high_school');q['score']=fact(False,'sydney',note='Korean Senior High School Diploma는 이 Direct 환산표에서 assessable qualification이 아님')
setp('unsw',highlights=['2027 PharmD 전환','5년 학위','졸업 후 Internship'],editorial='2027 학위명 변경과 인턴십 통합은 같은 의미가 아닙니다. 현재 과정 안내는 학위 후 별도 supervised internship을 설명합니다.',review_items=['새 PharmD 명칭의 APC/Board 승인 반영','신규 과정 2027 국가별 환산·학비'])
setp('uwa',highlights=['4년 Bachelor + PharmD','고교 졸업 후 진학','졸업 후 Internship'],editorial='고교 졸업 후 시작하는 4년 통합 Bachelor + Doctor of Pharmacy 과정입니다. 학위 안의 실습과 졸업 후 Pharmacy Board 등록을 위한 supervised internship year를 구분해야 하며, 별도의 2년 Graduate Entry Doctor of Pharmacy 과정과도 다릅니다.',review_items=['2027 국제학생 학비','Foundation·브리징 경로 세부조건'])
req('uwa','assumed','assumed',grade='Chemistry 및 Mathematics Applications/Methods 수준을 권장하며, 미충족 시 UWA 규정에 따라 foundation/bridging units가 요구될 수 있습니다.'); eng('uwa',7,{'L':7,'R':7,'W':7,'S':7}); intake('uwa',[2],'Semester 1 · 2월')
qual('uwa','csat',329,'UWA 국제학력 환산점수'); qual('uwa','sat',1220,'1600'); qual('uwa','ib',30,'45'); qual('uwa','alevel',10,'UWA A-level 환산점수')

# New UQ program remains a separate record with accreditation gate.
import copy
p=copy.deepcopy(prog('uq'));p.update(id='uq-pharmd',name=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),duration_years=fact(5,'uq-pharmd'),duration_label=fact('5년 통합','uq-pharmd'),bachelor_award_year=fact(None,'uq-pharmd'),four_year_exit=fact(None,'uq-pharmd'),exit_degree=fact(None,'uq-pharmd'),final_degree=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),highlights=['신설 5년 통합','Internship 통합 설계','인증 승인 대기'],editorial='신설 과정은 대학 공식 페이지에서 APC 인증과 Pharmacy Board 승인을 추진 중이라고 명시합니다. 기존 BPharm의 인증을 이 과정에 적용할 수 없습니다.',accreditation=fact('APC 인증·Pharmacy Board 승인 아직 미획득','uq-pharmd',status='pending_2027'),review_items=['APC accreditation 및 Board approval','신규 과정 qualification별 기준','학사 중간 Exit 여부'])
programs.append(p)
for coll in [requirements,english,intakes,tuition,registration]:
 r=copy.deepcopy(row(coll,'uq'));r['program_id']='uq-pharmd'
 for k,v in r.items():
  if isinstance(v,dict) and 'source_url' in v:v.update(source_id='uq-pharmd',source_url=course_urls['uq-pharmd'])
 if coll is registration:
  for k in ['supervised_practice_in_degree','itp_in_degree']:r[k]=fact(True,'uq-pharmd',note='학위 설계 기준 · 인증 승인 전')
  r['post_graduation_internship']=fact(False,'uq-pharmd',note='학위 내 인턴십 설계. 인증·등록 최종 요구 확인 필요.')
 if coll is intakes:r['route_id']='uq-pharmd-direct'
 coll.append(r)
for q in ['csat','sat','ib','alevel','ossd','korean_high_school','ged','other']:
 qualifications.append(dict(id='uq-pharmd-'+q,program_id='uq-pharmd',qualification=q,score=fact(None,'uq-pharmd',note='기존 BPharm 환산점수 자동 적용 금지'),scale=None,calculation=None))
routes.append(dict(id='uq-pharmd-direct',program_id='uq-pharmd',type='direct',title='Direct · 신설 통합과정',availability=fact(None,'uq-pharmd',note='인증·승인 완료 여부 확인 후 판단'),credit=fact(0,'uq-pharmd'),entry_year=fact(1,'uq-pharmd'),duration=fact(5,'uq-pharmd'),intake=fact('2월 / 7월','uq-pharmd'),progression=fact(None,'uq-pharmd'),english=fact(None,'uq-pharmd'),qualification=fact(None,'uq-pharmd'),note='기존 BPharm과 독립된 과정입니다.'))

def route(i,id,type,title,src,credit=None,entry=None,duration=None,intake=None,progression=None,note='',verified=True):
 r=dict(id=id,program_id=i+'-bpharm-hons',type=type,title=title,availability=fact(True if verified else None,src),credit=fact(credit,src),entry_year=fact(entry,src),duration=fact(duration,src),intake=fact(intake,src),progression=fact(progression,src),english=fact(None,src),qualification=fact(None,src),note=note)
 routes.append(r);return r
route('griffith','unicentre-korea','diploma','한국 UniCentre · Diploma of Health Science', 'griffith-korea',80,2,'한국 Diploma 1년 + 본과 T1 3년 또는 T2 3.5년','본과 T1 / T2 · 한국과정 시작월 확인 중','Diploma 수료 및 Griffith 입학조건 충족 후 80CP 인정','2027 entry onwards. 학점인정 협약은 입학·영어·장학금 보장이 아닙니다.')
route('griffith','griffith-college','diploma','Griffith College · Diploma of Health Sciences','griffith-college',80,2,'본과 잔여 240CP · T1 3년 / T2 3.5년','본과 T1 / T2 · Diploma 개강월 별도 확인','지정 Diploma 과목 이수 + 최종 입학허가','2026/2027 Diploma → 2027 본과부터. Diploma 자체 학비·진급 GPA는 확인 중.')
route('curtin','curtin-college','diploma','Curtin College · Pharmacy Diploma','curtin-college',175,2,'Stage 2: 12개월 · Stage 1 필요 시 8–12개월 추가','Stage 1: 2월/6월 · Stage 2: 2월','Stage 2 CWA 70% + PHAR1002(12월) 추가 이수','현재 College 페이지 70%를 우선합니다. 구 course information의 65%와 충돌 기록을 유지합니다.')
route('uq','uq-accelerated','foundation','UQ College · Accelerated Foundation','uq-accelerated',0,1,'약 4개월','2027-02-15 시작 → 07-09 완료 · 본과 07-26','BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','일정상 7월 본과 연결이 가능한 구조입니다. Foundation 입학자격, 과목 조합, 성적 발표·오퍼·비자 일정까지 충족해야 합니다.')
routes[-1]['progression']=fact('BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','uq-foundation')
route('sydney','sydney-usfp','foundation','USFP · University of Sydney Foundation Program','sydney',0,1,None,None,'Pharmacy GPA 7.3 / English C','2027 Pharmacy 행 기준. 수학 이수 및 프로그램별 입학자격은 별도 확인합니다.')
route('monash','monash-foundation','foundation','Monash University Foundation Year','monash-foundation',0,1,None,None,None,'2027 Pathway guide의 구 P6001 표를 새 P6007에 자동 적용하지 않습니다. 총점·영어·수학·화학 기준 확인 중.',False)
route('newcastle','newcastle-foundation','foundation','Newcastle International College · Foundation Studies','newcastle-foundation',0,1,None,None,None,'Pharmacy 연결 과정은 확인했습니다. 성적표의 academic/English 열과 2027 조건 대조를 완료한 뒤 수치를 표시합니다.')
route('monash','monash-ge','graduate','Monash · Graduate Entry','monash',None,3,'관련 학위 + 여름 집중과정 후 3학년 진입',None,'최근 10년 이내 관련 학사 · 평균 70% 이상 · 대학 수준 Human Physiology','최소 기준을 충족해도 선발은 경쟁적이며 학점·과목 심사가 필요합니다.')
route('rmit','rmit-associate','other','RMIT · Associate Degree pathway','rmit-pathway',None,None,'Associate 2년 + Bachelor 3년',None,None,'2026 공개 경로 참고. 1년 Diploma/IYO로 분류하지 않으며 2027 국제학생 적용 여부 확인 중.',False)
for i,title in [('latrobe','Foundation · Health / Life Sciences'),('utas','International Foundation')]:
 route(i,i+'-foundation','foundation',title,i,0,1,note='2027 Pharmacy-specific progression과 국제학생 모집 확인 중. 진학 가능 경로로 확정하지 않습니다.',verified=False)

def scholarship(i,id,name,src,pct=None,kind='pending',automatic=None,competitive=None,eligible=None,duration=None,threshold=None,renewal=None,number=None,exclude=None,note=''):
 scholarships.append(dict(id=id,university_id=i,name=name,amount=fact(pct,src),award_type='percentage' if pct else None,assessment=kind,
  automatic_assessment=fact(automatic,src),separate_application=fact(not automatic,src) if automatic is not None else fact(None,src),competitive=fact(competitive,src),country_eligibility=fact(eligible,src),duration=fact(duration,src),academic_threshold=fact(threshold,src),renewal_condition=fact(renewal,src),number_available=fact(number,src),course_exclusion=fact(exclude,src),pharmacy_eligible=fact(True,src) if i in ['griffith','sydney'] else fact(None,src),note=note))
scholarship('griffith','griffith-merit','International Academic Merit','griffith-scholarship',20,'automatic',True,False,True,'학위 잔여 기간 · 인정학점 제외','GPA 4.5/7 또는 동등 성적','매 학기 전 과목 통과·풀타임 유지',exclude='Diploma 자체 및 제휴기관 제공과정 등 제외',note='한국 국적 대상. Pathway 패키지는 최종 성적 제출 후 심사합니다.')
scholarship('sydney','sydney-award','Sydney International Student Award','sydney-scholarship',20,'application',False,False,True,'과정 기간','입학조건 충족 + personal statement','미납 없음·허가 없는 파트타임 전환 금지·정해진 기간 이수',exclude='MBA/EMBA·교환·원격·일부 법학 복수과정 등',note='2027 한국 국적 포함. Personal statement는 3개 항목 각 최대 200단어입니다.')
scholarship('monash','monash-merit','Pharmacy and Pharmaceutical Science International Merit','monash-scholarship',[25,50],'competitive',True,True,True,'최소 졸업학점 이수까지','각 대상 과정군 최상위·차상위','매 학기 WAM 70 유지',8,'공식 목록의 P6007 Scholars Program 등 대상 과정 확인','전체 4개 과정군 합계 연 8명. 일반 학생의 기본 비용에 적용하지 않습니다.')
scholarship('newcastle','newcastle-excellence','International Excellence 2027','newcastle-scholarship',20,'automatic',True,None,True,'대상 과정 잔여 학점',None,'약관·학업·거주 조건 충족',500,'인원 할당 과정 등 Appendix A 제외 여부 재확인','자동심사는 보장이 아닙니다. 수여 인원은 변동 가능하며 Pharmacy 제외목록 최종 대조가 남았습니다.')
scholarship('jcu','jcu-excellence','International Excellence','jcu-scholarship',25,'automatic',True,None,None,'승인된 과정 기간',None,None,None,None,'제도는 확인. Pharmacy 적용·국가·GPA 유지 조건 확인 전 비용에 차감하지 않습니다.')
scholarship('unsw','unsw-award','International Student Award','unsw-scholarship',20,'not_eligible',None,None,False,note='공식 eligible-country 목록에 South Korea 없음. 한국 국적 기본 장학으로 표시하지 않습니다.')
for i,name in [('curtin','Global Merit'),('qut','International Talent'),('latrobe','Health Innovation / High Achiever'),('canberra','High Achievers'),('unisq','International Student Support 2027'),('utas','International scholarships'),('uq','International scholarships'),('adelaide','International scholarships'),('rmit','International scholarships')]:
 scholarship(i,i+'-pending',name,i,note='2027 Pharmacy 적용, 한국 국적 자격, 금액·기간·유지 조건을 확인 중입니다.')

def housing(i,id,name,src,weekly=None,weeks=None,utilities=None,meals=None,campus=None,note=''):
 accommodation.append(dict(id=id,university_id=i,name=name,weekly_cost=fact(weekly,src),contract_weeks=fact(weeks,src),official_contract_total=fact(None,src),utilities=fact(utilities,src),meals=fact(meals,src),campus_distance=fact(campus,src),note=note))
housing('utas','utas-christ','Christ College','utas-housing',316,42,True,False,'Sandy Bay 교내 · 무료 교내 셔틀','2027 주당 요금. 42주 계약은 College 안내 기준. 방 형태·입주 자격·보증금 확인 필요.')
housing('utas','utas-john','John Fisher College','utas-housing',316,42,True,False,'Sandy Bay 교내','2027 주당 요금. 약학 수업 캠퍼스와 통학 동선을 확인하세요.')
housing('latrobe','latrobe-units','The Units','latrobe-housing',240,41,None,None,'Bendigo 캠퍼스','2026 latest reference. 보증금 A$1,000, 퇴실 청소 A$130 별도. 2027 금액 확인 중.')
housing('latrobe','latrobe-villas','The Villas','latrobe-housing',250,41,None,None,'Bendigo 캠퍼스','2026 latest reference. 2027 가격으로 표시하지 않습니다.')
for u in universities:
 if u['id'] not in ['utas','latrobe']:housing(u['id'],u['id']+'-housing-pending','공식 학생숙소 확인 중',None,note='저렴한 대면 학생숙소 1–2개와 2027 계약 요금을 검증 후 반영합니다.')

conflicts=[
 dict(id='curtin-progression',entity_id='curtin-college',field='progression',source_ids=['curtin-college','curtin-old'],status='source_conflict',summary='Stage 2 CWA: 현재 College 70% / 구 과정 안내 65%',decision='현재 메인 College 70% 우선. 입학팀 확인 전 충돌 기록 유지.'),
 dict(id='newcastle-english',entity_id='newcastle-bpharm-hons',field='english',source_ids=['newcastle'],status='source_conflict',summary='국제학생 상세 IELTS 7.0/각7.0과 다른 페이지 표시 6.5',decision='필터 충족 판정에서 제외. 2027 prospectus·입학팀 서면 대조 필요.'),
 dict(id='monash-foundation-version',entity_id='monash-foundation',field='progression',source_ids=['monash-foundation','monash'],status='pending_2027',summary='Pathway guide 구 P6001과 새 P6007 과정 코드 차이',decision='기존 progression 점수 이식 금지.'),
 dict(id='rmit-english-scope',entity_id='rmit-bpharm-hons',field='english',source_ids=['rmit-english','rmit'],status='pending_2027',summary='Pharmacy 전용 영어표의 국제학생 적용 범위 대조 필요',decision='수치는 참고값으로 표시. 자동 충족 판정 제외.'),
]
# Canberra 2027 course PDF verified after initial seed.
source('canberra-2027','Canberra Bachelor of Pharmacy HLB301 · 2027','https://www.canberra.edu.au/course/HLB301/1/2027.pdf',2027,'official_course')
setp('canberra',name=fact('Bachelor of Pharmacy','canberra-2027'),final_degree=fact('Bachelor of Pharmacy; embedded Honours option','canberra-2027'),international_recruitment=fact(True,'canberra-2027'),highlights=['4년 학사','2월 입학','IELTS 각 7.0'],editorial='2027 Bruce 캠퍼스 국제학생 모집이 확인되었습니다. Honours는 별도 성적 기준을 충족한 학생의 embedded option입니다.')
eng('canberra',7,{'L':7,'R':7,'W':7,'S':7},src='canberra-2027');intake('canberra',[2],'2027-02-15 · Semester 1','canberra-2027')
req('canberra','assumed','assumed','assumed','assumed','수학 + Biology/Human Movement, Chemistry/Physics는 assumed knowledge로 안내. 필수 prerequisite와 구분.',src='canberra-2027')
for route_record in routes:
 route_record['intake_months']=fact([2],'uq-accelerated') if route_record['id']=='uq-accelerated' else fact([2],'curtin-college') if route_record['id']=='curtin-college' else fact(None,route_record['availability']['source_id'])

# Additional course-specific official checks, 2026-09-24.
source('curtin-structure','Curtin · 2026 개편 Pharmacy 구조','https://www.curtin.edu.au/news/advice/how-to-become-a-pharmacist/',2026,'official_course')
setp('curtin',duration_years=fact(3.75,'curtin-structure'),duration_label=fact('3년 9개월','curtin-structure'),bachelor_award_year=fact(3.75,'curtin-structure'),highlights=['3년 9개월','College → Year 2','인턴십 별도'],review_items=['국제학생 2027 학비','Global Merit의 Pharmacy 제외 여부'])
req('curtin','required','required','recommended',grade='Chemistry와 Mathematics ATAR 또는 인정 동등 과목. Biology/Human Biology는 권장.',src='curtin-structure')
row(registration,'curtin').update(supervised_practice_in_degree=fact(False,'curtin-structure'),post_graduation_internship=fact(True,'curtin-structure'))
source('unisq-course','UniSQ · International Bachelor of Pharmacy (Honours)','https://www.unisq.edu.au/study/degrees-and-courses/bachelor-of-pharmacy-honours?studentType=international',None,'official_course')
eng('unisq',7,{'L':7,'R':7,'W':6.5,'S':7},src='unisq-course')
req('unisq','assumed','assumed','assumed','assumed','English C, Mathematical Methods/Specialist C, Biology/Chemistry/Physics 중 하나 C는 assumed knowledge.',src='unisq-course')
fee('unisq',34280,src='unisq-course',year=2026,load='8 units / year · 2026 국제학생 참고값')
setp('unisq',editorial='2027 국제학생 개설표는 Trimester 1만 안내합니다. 공식 과정 페이지의 3년 가속 일정은 2028년부터이며 2027 과정에 적용하지 않습니다.',review_items=['2027 학비','T1 최종 개설 일정','2027 장학금 적용'])
row(registration,'unisq').update(supervised_practice_in_degree=fact(False,'unisq-course'),post_graduation_internship=fact(True,'unisq-course'))
source('griffith-2026','Griffith 2026 International Guide · Pharmacy H1','https://www.griffith.edu.au/__data/assets/pdf_file/0035/2193587/Griffith-University-2026-International-Study-Guide-Digital.pdf',2026,'official_guide')
for q,score,scale in [('csat',331,'대학 공식 CSAT 환산'),('sat',1080,'1600 · 미국 고교졸업 자격 동반'),('ib',28,'45'),('alevel',7,'대학 A-level 환산점수')]:
 record=next(x for x in qualifications if x['program_id']=='griffith-bpharm-hons' and x['qualification']==q)
 record.update(score=fact(score,'griffith-2026',note='Pharmacy 1614 = H1. 2026 공개 기준이며 2027 확정값이 아닙니다.'),scale=scale)
row(english,'griffith')['ielts_overall']=fact(7,'griffith-2026',note='2026 Pharmacy 행. 각 영역과 2027 조건은 별도 확인 중.')
source('griffith-college-entry','Griffith College · 국제학생 입학조건','https://www.griffithcollege.edu.au/international-students/entry-requirements/',None,'official_pathway')
gc=next(r for r in routes if r['id']=='griffith-college')
gc['english']=fact('Pharmacy 연결 Diploma: IELTS 6.5 / 각 6.0 · PTE 58 / 각 50 · TOEFL 79 / 각 19','griffith-college-entry',note='일반 Diploma 영어 5.5를 약대 연결 경로에 적용하지 않습니다. 본과 진급 영어조건은 별도 확인.')
gc['qualification']=fact('College 일반 학력표: 한국 고교 4개 학업과목 평균 Rank 6, 또는 고교 졸업 + CSAT 280 / 상위 3개 stanine 6, 또는 검정고시 평균 80','griffith-college-entry',status='pending_2027',note='College 입학용 참고표. Pharmacy 연결 과정의 학력 예외·2027 적용 검증 전이며 Griffith 본과 Direct 점수가 아닙니다.')
# Link Direct route summaries to their own program rather than duplicate unknowns.
for route_record in routes:
 if route_record['type']=='direct':
  program=next(p for p in programs if p['id']==route_record['program_id'])
  start=next(x for x in intakes if x['program_id']==program['id'])
  route_record['duration']=copy.deepcopy(program['duration_label'])
  route_record['intake']=copy.deepcopy(start['label'])
  route_record['intake_months']=copy.deepcopy(start['months'])
  route_record['note']='아래 Direct 학력별 성적·선수과목·영어 표를 함께 확인하세요. 최종 입학은 대학 심사로 결정됩니다.'
# A blocked source is not a completed verification.
sources['board']['verified_date']=None
sources['board']['retrieval_status']='blocked_403'

data=dict(schema_version='1.0.0',academic_year=2027,verified_date=DATE,universities=universities,programs=programs,entry_routes=routes,qualifications=qualifications,requirements=requirements,english=english,intakes=intakes,tuition=tuition,scholarships=scholarships,accommodation=accommodation,professional_registration=registration,sources=list(sources.values()),conflicts=conflicts)
(ROOT/'data/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
config=dict(site_name='호주약대 가이드',brand='TNS',language='ko',academic_year=2027,production_url=None,production_approved=False,
 channels=[dict(id='kakao',label='카카오톡 상담',detail='내 조건으로 1:1 상담',url='https://open.kakao.com/o/slehLvKi',source='tnsuhak/xjtlu-korea main index.html'),dict(id='phone',label='전화 상담',detail='02-3288-1733',url='tel:0232881733',source='tnsuhak/xjtlu-korea main index.html'),dict(id='australia-chat',label='호주 오픈채팅',detail='승인된 호주 전용 링크 확인 중',url=None,source=None),dict(id='cafe',label='네이버 카페',detail='TNS 유학 커뮤니티',url='https://cafe.naver.com/tnsuhak.cafe',source='tnsuhak/xjtlu-korea main index.html')])
(ROOT/'data/site.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(f'{len(universities)} universities / {len(programs)} programs / {len(routes)} routes / {len(sources)} sources')

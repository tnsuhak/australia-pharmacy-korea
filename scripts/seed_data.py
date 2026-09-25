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
source('homeaffairs-485','Australian Home Affairs · Temporary Graduate visa (subclass 485) Post-Higher Education Work','https://immi.homeaffairs.gov.au/Visa-subsite/Pages/work/485-post-study-work.aspx',2026,'government')
source('homeaffairs-second485','Australian Home Affairs · Second Post-Higher Education Work stream','https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/temporary-graduate-485/second-post-higher-education-work',2026,'government')
source('homeaffairs-regional','Australian Home Affairs · Designated regional area postcodes','https://immi.homeaffairs.gov.au/supporting/Pages/Work/187-regional-postcodes.aspx',2026,'government')
source('jcu-2027-campus','JCU · 2027 course changes · Pharmacy campuses','https://www.jcu.edu.au/future-students/schools/2027-course-changes',2027,'official_course')
source('utas-2027-campus','University of Tasmania · Bachelor of Pharmacy with Honours 2027','https://www.utas.edu.au/courses/health/courses/54d-bachelor-of-pharmacy-with-honours',2027,'official_course')
source('uwa-dpharm','UWA · Doctor of Pharmacy graduate entry','https://www.uwa.edu.au/study/courses/doctor-of-pharmacy',2027,'official_course')
source('migration-nsw-skills','NSW Government · NSW Skills Lists','https://www.nsw.gov.au/visas-and-migration/skilled-visas/nsw-skills-lists',2026,'government')
source('migration-qld-list','Migration Queensland · Queensland onshore skilled occupation list','https://migration.qld.gov.au/occupation-lists/queensland-onshore-skilled-occupation-list',2026,'government')
source('migration-qld-status','Migration Queensland · Skilled migration ROI status','https://migration.qld.gov.au/visa-options/skilled-visas/registering-your-interest-in-queenslands-migration-program',2026,'government')
source('migration-vic-status','Victoria · Skilled visa nomination program status','https://liveinmelbourne.vic.gov.au/migrate/skilled-migration-visas/2025-26-skilled-migration-visa-nomination-program',2026,'government')
source('migration-tas-program','Migration Tasmania · 2026-27 Program Opening','https://www.migration.tas.gov.au/news/2024-25_program_open_to_rois',2026,'government')
source('migration-tas-health','Migration Tasmania · Health, Allied Health and Teaching Occupations','https://www.migration.tas.gov.au/skilled_migration/health%2C-allied-health-and-teaching-occupations',2026,'government')
source('migration-act-list','ACT Government · Nominated Migration Program Occupation List','https://www.act.gov.au/migration/skilled-migrants/act-nominated-migration-program-occupation-list',2026,'government')
source('migration-act-program','ACT Government · ACT nomination pathways','https://www.act.gov.au/migration/skilled-migrants/act-government-nomination/act-nomination-pathways',2026,'government')
source('migration-sa-list','South Australia · Skilled Occupation List','https://migration.sa.gov.au/before-applying/work-in-sa/occupation-lists/occupations-list',2026,'government')
source('migration-sa-status','South Australia · 2026-27 program status','https://migration.sa.gov.au/news/registrations-of-interest-closing-2-june-2026',2026,'government')
source('migration-wa-criteria','WA Government · 2025-26 State Nominated Migration Program criteria','https://migration.wa.gov.au/sites/default/files/2025-09/2025-26%20WA%20SNMP%20Criteria%20-%20July%202025.pdf',2025,'government')
source('migration-wa-pharmacist','WA Government · December 2025 SNMP invited EOIs by occupation','https://migration.wa.gov.au/sites/default/files/2025-12/SNMP%20Invite%20Round%20-%20December%202025.pdf',2025,'government')
source('jcu-housing-2026','JCU · Casual Stay Rates 2026','https://www.jcu.edu.au/accommodation/casual-stays/casual-rates',2026,'official_accommodation')
source('uq-housing-current','UQ · Cost of living and UQ RES','https://study.uq.edu.au/university-life/living-in-queensland/cost-living',None,'official_accommodation')
source('adelaide-mattanya-2027','Adelaide University · Mattanya Student Residences 2027','https://adelaide.edu.au/life-at-adelaide/accommodation/student-accommodation/university-managed-student-accommodation/mattanya-student-residences/',2027,'official_accommodation')
source('adelaide-village-2027','Adelaide University · Adelaide University Village 2027','https://adelaide.edu.au/life-at-adelaide/accommodation/student-accommodation/university-managed-student-accommodation/adelaide-university-village/',2027,'official_accommodation')
source('griffith-village-2027','Griffith University Village · 2027 room rates','https://campuslivingvillages.com/australia/gold-coast/griffith-university-village',2027,'accommodation_provider')
source('griffith-accommodation','Griffith University · Gold Coast accommodation','https://www.griffith.edu.au/about-griffith/campuses-facilities/accommodation',None,'official_accommodation')
source('qut-living-current','QUT · Living in Brisbane cost guide','https://www.qut.edu.au/study/international/living-in-brisbane',None,'official_accommodation')
source('rmit-bundoora-2027','RMIT · UniLodge Bundoora Walert House 2027 rate reference','https://www.rmit.edu.au/scholarships/coursework/unilodge',2027,'official_accommodation')
source('newcastle-housing-2027','University of Newcastle · 2027 International Prospectus accommodation','https://www.newcastle.edu.au/__data/assets/pdf_file/0020/1102565/2025-1079-International-Prospectus-2027-ROW_V27.pdf',2027,'official_guide')
source('canberra-housing-2027','University of Canberra · 2027 accommodation guarantee and rates','https://www.canberra.edu.au/future-students/study-at-uc/international/international-student-experience-at-uc/2026/september/accomodation-guarantee',2027,'official_accommodation')
source('unisq-housing-current','UniSQ · International fees and accommodation guide','https://www.unisq.edu.au/international/fees-scholarships',None,'official_accommodation')
source('monash-parkville-rent','Monash · Parkville private rental guide','https://www.monash.edu/accommodation/off-campus/private-rental',None,'official_accommodation')
source('sydney-regiment-2026','University of Sydney · Regiment 2026 rates','https://www.sydney.edu.au/study/accommodation/camperdown-darlington/university-residences/regiment.html',2026,'official_accommodation')
source('sydney-qmb-2026','University of Sydney · Queen Mary Building 2026 rates','https://www.sydney.edu.au/study/accommodation/camperdown-darlington/university-residences/queen-mary-building.html',2026,'official_accommodation')
source('unsw-housing-2027','UNSW · 2027 accommodation status','https://www.unsw.edu.au/accommodation/apartments',2027,'official_accommodation')
source('uwa-trinity-2027','Trinity Residential College at UWA · 2027 fees','https://trc.uwa.edu.au/our-pricing/fees/',2027,'accommodation_provider')
source('curtin-housing-current','Curtin · Perth on-campus accommodation','https://www.curtin.edu.au/study/campus-life/accommodation/',None,'official_accommodation')
source('curtin-contract-2026','Curtin · 2026 on-campus contract dates','https://www.curtin.edu.au/study/help-support/app/answers/detail/a-id/2377/what-are-the-contract-dates-for-on-campus-accommodation/',2026,'official_accommodation')
source('qut-scholarship-2027','QUT 2027 International Guide · International Merit Scholarship','https://cms.qut.edu.au/__data/assets/pdf_file/0003/1566471/27516-Year-12-International-Guide-2027_DIGITAL_F.pdf',2027,'official_guide')
source('uq-scholarship-2027','UQ International Excellence Scholarship 2027','https://scholarships.uq.edu.au/scholarship/uq-international-excellence-scholarship',2027,'official_scholarship')
source('curtin-scholarship-2027','Curtin Global Merit Scholarship · 2027 commencement','https://scholarships.curtin.edu.au/Scholarship/?id=7986',2027,'official_scholarship')
source('utas-scholarship-2027','UTas Tasmanian International Merit Scholarship · 2027 terms','https://www.utas.edu.au/study/scholarships-fees-and-costs/international-scholarships/tasmanian-international-merit-scholarship',2027,'official_scholarship')
source('unisq-scholarship-2027','UniSQ International Student Support Scholarship 2027','https://www.unisq.edu.au/scholarships/unisqi-international-student-support-scholarship-2027',2027,'official_scholarship')
source('adelaide-scholarship','Adelaide Merit Scholarship 15%','https://adelaide.edu.au/study/scholarships/int/adelaide-merit-scholarship-15/',None,'official_scholarship')
source('latrobe-scholarship-2027','La Trobe High Achiever Scholarship · 2026/2027','https://www.latrobe.edu.au/study/scholarships/other/la-trobe-high-achiever-scholarship',2027,'official_scholarship')
source('latrobe-scholarship-courses','La Trobe · Courses offering international scholarships','https://www.latrobe.edu.au/study/scholarships/advice/courses-offering-international-scholarships',2027,'official_scholarship')
source('latrobe-health-innovation-2027','La Trobe Health Innovation Scholarship · 30% · 2026/2027 intakes','https://www.latrobe.edu.au/international/applying/scholarships',2027,'official_scholarship')
source('canberra-guide-2027','University of Canberra International Course Guide 2027 · Scholarships','https://www.canberra.edu.au/content/dam/uc/documents/agent-marketing-toolkit/international-course-guide/international-course-guide.pdf',2027,'official_guide')
source('uwa-scholarship-current','UWA Global Excellence Scholarship','https://www.uwa.edu.au/study/scholarships-and-fees/scholarships/international-scholarships/global-excellence-scholarship',2027,'official_scholarship')
source('newcastle-scholarship-2027-terms','Newcastle International Excellence Scholarship 2027 · Terms & Conditions · excluded programs','https://www.newcastle.edu.au/__data/assets/pdf_file/0014/1136300/UNI_053-International-Excellence-Scholarship-2027-T-and-Cs-07072026.pdf',2027,'official_scholarship')
source('uwa-foundation','UWA College · UWA Foundation Program','https://www.uwa.edu.au/uwa-college/Study/UWA-Foundation-Program',None,'official_pathway')
source('qut-college-foundation','QUT College · Foundation programs','https://www.qut.edu.au/study/qut-college/international/english-language-programs',None,'official_pathway')
source('qut-fee-2027','QUT · Bachelor of Pharmacy (Honours) 2027 fee','https://www.qut.edu.au/courses/bachelor-of-pharmacy-honours',2027,'official_course')
source('newcastle-fee-2027','University of Newcastle · 2027 International Student Degree Guide · Pharmacy','https://www.newcastle.edu.au/__data/assets/pdf_file/0020/1102565/2025-1079-International-Prospectus-2027-ROW_V27.pdf',2027,'official_guide')
source('monash-fee-2027','Monash · Pharmacy P6007 2027 fee','https://www.monash.edu/study/courses/find-a-course/pharmacy-p6007',2027,'official_course')
source('jcu-fee-2026','JCU · Bachelor of Pharmacy (Honours) 2026 fee','https://www.jcu.edu.au/courses/bachelor-of-pharmacy-honours',2026,'official_course')
source('unsw-fee-2026','UNSW · Pharmaceutical Medicine / Pharmacy 2026 fee','https://www.unsw.edu.au/study/undergraduate/bachelor-of-pharmaceutical-medicine-master-of-pharmacy',2026,'official_course')
source('uwa-fee-2026','UWA · 2026 international undergraduate fees CM039','https://www.fees.uwa.edu.au/Browse/BrowseCourses?feeType=INTUG&feeYear=2026',2026,'official_fee')
source('adelaide-fee-current','Adelaide University · Bachelor of Pharmacy (Honours) international fee','https://adelaide.edu.au/study/degrees/bachelor-of-pharmacy-honours/',None,'official_course')
source('rmit-2027-apply','RMIT Bachelor of Pharmacy (Honours) · 2027 intake','https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/honours-degrees/bachelor-of-pharmacy-honours-bh102/apply-now',2027,'official_course')
source('unsw-2027-course','UNSW Pharmaceutical Medicine / Doctor of Pharmacy · 2027','https://www.unsw.edu.au/study/undergraduate/bachelor-of-pharmaceutical-medicine-master-of-pharmacy',2027,'official_course')
source('unsw-english-current','UNSW · English language requirements','https://www.unsw.edu.au/study/how-to-apply/english-language-requirements',None,'official_admissions')
source('latrobe-2027-course','La Trobe Bachelor of Pharmacy (Honours) · 2027 start','https://www.latrobe.edu.au/courses/bachelor-of-pharmacy-honours',2027,'official_course')
source('curtin-pharmacy-current-guide','Curtin · Pharmacy English requirement guide','https://publications.curtin.edu.au/chinese-student-guide/page/28-29',None,'official_guide')
source('newcastle-2027-course','University of Newcastle · Bachelor of Pharmacy (Honours) current 2027 entry','https://www.newcastle.edu.au/degrees/bachelor-of-pharmacy-honours',2027,'official_course')
source('newcastle-2026-ug','University of Newcastle · 2026 Undergraduate Degrees guide','https://www.newcastle.edu.au/__data/assets/pdf_file/0012/978438/2026-1088_UG-Prospectus_v3.6_WEB.pdf',2026,'official_guide')
source('monash-pps-2026','Monash Pharmacy and Pharmaceutical Sciences · International UG Course Guide 2026','https://www.monash.edu/__data/assets/pdf_file/0004/4091809/Monash-University-PPS-International-UG-Course-Guide-2026.pdf',2026,'official_guide')
source('rmit-korea-equiv','RMIT · South Korea academic entry equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/south-korea',2027,'official_admissions')
source('rmit-ib-equiv','RMIT · International Baccalaureate academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/international-baccalaureate',2027,'official_admissions')
source('rmit-uk-equiv','RMIT · United Kingdom academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/united-kingdom',2027,'official_admissions')
source('rmit-usa-equiv','RMIT · USA academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/usa',2027,'official_admissions')
source('rmit-foundation-equiv','RMIT · Foundation Studies equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/foundation-equivalencies',2027,'official_pathway')
source('jcu-intl-2025','JCU 2025 International Guide · Pharmacy entry scores','https://www.jcu.edu.au/__data/assets/pdf_file/0018/2205414/2025-International-Guide.pdf',2025,'official_guide')
source('newcastle-prospectus-2027','University of Newcastle · 2027 International Prospectus','https://www.newcastle.edu.au/__data/assets/pdf_file/0020/1102565/2025-1079-International-Prospectus-2027-ROW.pdf',2027,'official_guide')
source('adelaide-pharmacy-current','Adelaide University · Bachelor of Pharmacy (Honours) international entry requirements','https://adelaide.edu.au/study/degrees/bachelor-of-pharmacy-honours/',None,'official_course')
source('latrobe-health-guide','La Trobe · International Health Discipline Handbook · Pharmacy','https://www.latrobe.edu.au/international/documents/international-handbooks/LTU-Health-Discipline-Handbook.pdf',2026,'official_guide')
source('griffith-2026-guide','Griffith University · 2026 International Student Guide · Pharmacy','https://www.griffith.edu.au/__data/assets/pdf_file/0035/2193587/Griffith-University-2026-International-Study-Guide-Digital.pdf',2026,'official_guide')
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
source('jcu-scholarship','JCU · International Excellence Scholarship','https://www.jcu.edu.au/scholarships/search/international-excellence-scholarship',None,'official_scholarship')
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
source('unisq-pharmacy-current','UniSQ · Bachelor of Pharmacy (Honours) current international entry requirements','https://www.unisq.edu.au/study/degrees-and-courses/bachelor-of-pharmacy-honours?studentType=international',2027,'official_course')
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

setp('jcu',highlights=['3년 Fast-track','화학 권장','2월 입학'],editorial='화학은 필수가 아닙니다. 3년 Fast-track이라 학업 속도가 빠릅니다.',review_items=['2027 국제학생 학비','한국 학력 환산표'])
req('jcu','recommended','required',grade='English와 General Mathematics 또는 동등 수준. Chemistry 권장.',src='jcu-guide'); intake('jcu',[2],'2월','jcu-guide'); fee('jcu',31710,src='jcu-fee-2026',year=2026); eng('jcu',7.0,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='jcu-guide',pte=65,pte_each=58)
setp('utas',highlights=['3년 Fast-track','2027 학비 공개','Hobart 숙소'],editorial='4년 약학과를 3년에 압축해 공부합니다. 1년 수강량이 많습니다.')
fee('utas',61267,total=198050,load='연간 133 credit points 기준'); eng('utas',6.5,{'L':6,'R':6,'W':6,'S':6},src='utas'); intake('utas',None,'Semester 1 · Cradle Coast / Hobart / Launceston',src='utas'); req('utas','required','required','recommended','accepted','수학 1과목 + Chemistry 또는 Physical Sciences에서 satisfactory achievement',src='utas')
setp('curtin',highlights=['College → Year 2','175 credits','진급 CWA 확인'],editorial='Curtin College Diploma 후 약대 2학년으로 진학합니다. Stage 2 CWA 70%와 PHAR1002가 필요합니다.',review_items=['약 3년 9개월 운영 일정 재확인','국제학생 2027 학비','Global Merit의 Pharmacy 제외 여부']); eng('curtin',7.0,{'L':7,'R':7,'W':7,'S':7},src='curtin-pharmacy-current-guide')
setp('uq',duration_label=fact('2월 4년 · 7월 약 3.5년','uq'),highlights=['2월 4년','7월 3.5년','Accelerated Foundation'],editorial='2월 입학은 4년, 7월 입학은 약 3.5년입니다. 새 5년 PharmD와는 다른 과정입니다.')
req('uq','required','required','recommended',grade='English·수학·Chemistry: Queensland Year 12 C 또는 동등 수준.'); intake('uq',[2,7],'2월 22일 / 7월 26일'); fee('uq',60952,load='16 units 기준')
eng('uq',6.5,{'L':6,'R':6,'W':6,'S':6},pte=64,pte_each=60,toefl={'overall':87,'L':19,'R':19,'W':21,'S':19})
setp('adelaide',highlights=['4년 학사','7월은 학점인정 조건부'],editorial='일반 Direct는 2월 시작입니다. 7월 입학은 학점이 인정된 국제학생을 개별 심사합니다.')
intake('adelaide',[2],'2월 · 7월은 학점 인정 시 개별 심사'); fee('adelaide',54300,src='adelaide-fee-current'); req('adelaide','accepted','not_required','accepted','accepted','Biology, Chemistry 또는 Physics 중 1과목 또는 동등 수준',src='adelaide'); eng('adelaide',6.5,{'L':6,'R':6,'W':6,'S':6},src='adelaide')
setp('griffith',highlights=['Diploma → 2학년','80CP 인정','20% 자동심사'],editorial='Direct 입학과 Griffith College Diploma 경로가 있습니다. Griffith College Diploma 후 80CP를 인정받고 약대 2학년으로 진학합니다.'); intake('griffith',[3,7],'3월 · 7월 (2026 공개 기준)',src='griffith-2026-guide'); eng('griffith',7.0,None,src='griffith-2026-guide')
setp('latrobe',highlights=['Bendigo','4년 학사','숙소 2026 참고'],editorial='Bendigo 캠퍼스 약대입니다. 2027 학비는 업데이트 대기입니다.',review_items=['2027 국제학생 학비']); intake('latrobe',[3],'Semester 1 · 2027년 3월',src='latrobe-2027-course'); req('latrobe','not_required','not_required','not_required','not_required','별도 과학 선수과목 없음 · 영어 prerequisite만 적용',src='latrobe-health-guide'); eng('latrobe',6.5,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='latrobe-health-guide')
setp('qut',highlights=['수학 + 화학','4년 학사','영어 조건 비교'],editorial='수학과 화학이 필요합니다. 영어는 약대 기준을 적용합니다.')
req('qut','assumed','assumed',grade='Chemistry + Mathematical Methods/Specialist Mathematics는 assumed knowledge',src='qut-fee-2027'); eng('qut',6.5,{'L':6,'R':6,'W':6,'S':6},pte=58,pte_each=50,toefl={'overall':79,'L':16,'R':16,'W':21,'S':18}); intake('qut',[2],'2월',src='qut-fee-2027'); fee('qut',46200,src='qut-fee-2027',year=2027,load='96 credit points 기준')
setp('rmit',highlights=['4년','RMIT Foundation 가능','2027 학비 A$49,920'],editorial='Bundoora 캠퍼스 4년 약대입니다. 한국 고교·수능 환산표가 명확하고 RMIT Foundation으로도 준비할 수 있습니다.')
req('rmit','required','required',grade='VCE Chemistry 25, Mathematics 25 또는 인정되는 동등 수준.'); fee('rmit',49920,year=2027); intake('rmit',[2],'Semester 1 · 2027년 3월 1일 수업 시작',src='rmit-2027-apply')
eng('rmit',7,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='rmit-english',pte=65,pte_each=58,toefl={'overall':94,'R':19,'L':20,'S':20,'W':24})
setp('newcastle',highlights=['4년 학사','Foundation 연계','2027 영어자료 충돌'],editorial='2027 공식 Degree Guide는 IELTS 6.5/각 6.5, 현재 과정 페이지의 English proficiency section은 7.0/각 7.0으로 표시해 공식자료 간 차이가 남아 있습니다.',review_items=['Pharmacy 2027 영어조건 공식자료 충돌','2027 CSAT·SAT·IB course-specific 값','APC 인증 갱신: 현재 목록 종료일 2026-12-31'])
eng('newcastle',7,{'L':7,'R':7,'W':7,'S':7},src='newcastle-2027-course',status='source_conflict');
for _k in ['ielts_overall','ielts_bands']:
 row(english,'newcastle')[_k]['note']='2027 International Student Degree Guide는 IELTS 6.5/각 6.5, 현재 과정 페이지의 English proficiency section은 7.0/각 7.0으로 표시합니다. 자동 충족 판정에 사용하지 않고 지원 전 Newcastle Admissions 서면 확인이 필요합니다.'
for k in ['ielts_overall','ielts_bands']:row(english,'newcastle')[k]['note']='공식 과정페이지에 6.5/6.5와 7.0/7.0 표기가 함께 노출되고 공식 국제 가이드도 연도별 차이가 있어 2027 지원 전 서면 확인 필요.'
intake('newcastle',[2],'Semester 1 · 2027년 2월 22일',src='newcastle-2027-course'); req('newcastle','assumed','assumed',physics='assumed',grade='Assumed knowledge: Mathematics, English Advanced, Chemistry, Physics',src='newcastle-2026-ug'); fee('newcastle',51665,src='newcastle-fee-2027',year=2027,load='80 units 기준')
setp('canberra',highlights=['Canberra','4년 Bachelor of Pharmacy','2027 국제학생 모집 확인'],editorial='2027 HLB301 공식 course PDF와 International Course Guide에서 Semester 1 국제학생 모집과 연 A$42,500 학비를 확인했습니다.'); fee('canberra',42500,src='canberra-guide-2027',year=2027)
setp('unisq',highlights=['T1 only','Toowoomba','2027 개설표'],editorial='2027 국제학생 대면 수업은 Trimester 1에 표시됩니다. 개설 안내서는 9월 28일 확정 예정이므로 최종 일정 확인이 필요합니다.')
intake('unisq',[2],'Trimester 1 · 2027년 2월 15일',src='unisq-pharmacy-current'); req('unisq','accepted','assumed','accepted','accepted','수학 + Biology/Chemistry/Physics 중 1과목에서 Year 12 C 수준 assumed knowledge',src='unisq-pharmacy-current'); eng('unisq',7.0,{'L':7,'R':7,'W':6.5,'S':7},src='unisq-pharmacy-current')
setp('monash',highlights=['4년 Exit','5년 PharmD','Internship 통합'],editorial='4년 후 BPharm(Hons)로 졸업하거나 5년째 PharmD까지 이어갈 수 있습니다. 관련 학사 졸업자는 Graduate Entry도 있습니다.')
req('monash','required','required',grade='VCE Methods/Specialist Maths 25 + Chemistry 25. IB Math AA SL4 또는 AA/AI HL3, Chemistry SL4 또는 HL3.'); intake('monash',[2],'2월'); fee('monash',49740,src='monash-fee-2027',year=2027,load='48 credit points 기준'); eng('monash',6.5,{'L':6,'R':6,'W':6,'S':6},src='monash-pps-2026',pte=58,pte_each=50)
setp('sydney',highlights=['5년 통합','2027 환산표','Internship 통합'],editorial='5년 BPharm(Hons) / Master of Pharmacy Practice 과정입니다. 4년 후 학사 Exit가 있습니다.',review_items=['4년 학사 Exit 조건과 학위명','2027 Mathematics prerequisite 적용 여부','USFP 수학 progression 조건'])
eng('sydney',6.5,{'L':6,'R':6,'W':6,'S':6},toefl={'overall':85,'bands_note':'공식표 각영역 17/19 구분 상세 확인'}); intake('sydney',[2],'2월'); fee('sydney',63600); req('sydney','assumed','assumed','recommended',grade='Mathematics admission prerequisite와 Chemistry/Math assumed knowledge를 별도로 확인',src='sydney-structure')
qual('sydney','csat',346,'표준점수 4개 합','국어 + 수학 + 사회/과학 탐구 상위 2개 과목의 표준점수 합. 등급이나 백분위 합계가 아닙니다.')
qual('sydney','sat',1300,'1600'); qual('sydney','ib',31,'45'); qual('sydney','alevel',14,'대학 환산점수','3과목/4과목 각각 14. A-level 성적을 대학 공식 환산식으로 계산해야 합니다.')
q=next(x for x in qualifications if x['program_id']=='sydney-bpharm-hons' and x['qualification']=='korean_high_school');q['score']=fact(False,'sydney',note='Korean Senior High School Diploma는 이 Direct 환산표에서 assessable qualification이 아님')
setp('unsw',name=fact('Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy','unsw-2027-course'),final_degree=fact('Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy','unsw-2027-course'),highlights=['2027 PharmD 전환','5년 학위','졸업 후 Internship'],editorial='UNSW는 2027부터 Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy로 명칭을 변경한다고 공식 안내합니다. 졸업 후 일반등록을 위한 인턴십·시험 요건은 별도입니다.',review_items=['새 PharmD 명칭의 APC/Board 승인 반영','2027 국제학생 학비']); prog('unsw')['accreditation']['note']='APC 2026-07-08 목록은 기존 Bachelor of Pharmaceutical Medicine / Master of Pharmacy 명칭을 Accredited with conditions(종료 2028-06-30)로 게재합니다. UNSW가 공지한 2027 Doctor of Pharmacy 새 명칭의 APC/Pharmacy Board 반영은 지원·등록 전 재확인합니다.'; fee('unsw',63000,src='unsw-fee-2026',year=2026,total=349000,load='first-year full-time fee'); intake('unsw',[2],'Term 1 · 2027',src='unsw-2027-course'); eng('unsw',6.5,{'L':6,'R':6,'W':6,'S':6},src='unsw-english-current'); req('unsw','assumed','assumed',grade='Assumed knowledge: Chemistry, Mathematics Advanced',src='unsw')
setp('uwa',highlights=['4년 Bachelor + PharmD','고교 졸업 후 진학','졸업 후 Internship'],editorial='고교 졸업 후 4년 동안 Bachelor + Doctor of Pharmacy를 함께 취득합니다. 졸업 후 인턴십은 따로 합니다.',review_items=['2027 국제학생 학비'])
req('uwa','assumed','assumed',grade='Chemistry 및 Mathematics Applications/Methods 수준을 권장하며, 미충족 시 UWA 규정에 따라 foundation/bridging units가 요구될 수 있습니다.'); eng('uwa',7,{'L':7,'R':7,'W':7,'S':7}); intake('uwa',[2],'Semester 1 · 2월')
# RMIT Pharmacy 65% international academic requirement mapped through official country equivalency tables.
for qt,val,scale,src,note,calc in [
 ('korean_high_school',75,'한국 고교 졸업성적 평균 %','rmit-korea-equiv','RMIT Pharmacy 국제학생 academic requirement 65%의 한국 고교 환산값',''),
 ('csat',300,'표준점수 합','rmit-korea-equiv','한국 고교 졸업 + CSAT 기준','국어·수학을 포함한 best 4 graded subjects의 KICE standard score 계산'),
 ('ib',25,'45','rmit-ib-equiv','RMIT Bachelor 65% 기준의 IB 환산값',''),
 ('alevel',7,'RMIT A-level points','rmit-uk-equiv','3 A-level 기준 예시 CDD',''),
 ('sat',1060,'1600','rmit-usa-equiv','미국 High School Diploma GPA 2.5 이상과 함께 충족해야 함','')]:
 q=next(x for x in qualifications if x['program_id']=='rmit-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,src),scale=scale,calculation=calc); q['score']['note']=note
qual('uwa','csat',329,'UWA 국제학력 환산점수'); qual('uwa','sat',1220,'1600'); qual('uwa','ib',30,'45'); qual('uwa','alevel',10,'UWA A-level 환산점수'); fee('uwa',46000,src='uwa-fee-2026',year=2026,load='48 points 기준')
# Additional international qualification scores verified for 2027 site.
for qt,val,scale in [('csat',340,'대학 공식 CSAT 기준'),('ib',30,'45'),('sat',1220,'1600'),('alevel',10,'UK / Global GCE A-level 환산점수'),('ossd',80,'Ontario Secondary School Diploma 평균 %')]:
 q=next(x for x in qualifications if x['program_id']=='adelaide-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'adelaide-pharmacy-current'),scale=scale)
for qt,val,scale in [('ib',36,'45'),('alevel',15,'UNSW A-level aggregate')]:
 q=next(x for x in qualifications if x['program_id']=='unsw-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'unsw-2027-course'),scale=scale,calculation='2027 PharmD 명칭 변경에도 입학기준은 동일하다는 UNSW 안내 기준')
q=next(x for x in qualifications if x['program_id']=='newcastle-bpharm-hons' and x['qualification']=='ib'); q.update(score=fact(28,'newcastle-prospectus-2027'),scale='45')
q=next(x for x in qualifications if x['program_id']=='uq-bpharm-hons' and x['qualification']=='ib'); q.update(score=fact(30.25,'uq',2026,status='latest_published',note='2027 program page의 최신 threshold이며 Semester 1, 2026 offer 기준'),scale='45')
for qt,val,scale in [('ib',27,'45'),('sat',1020,'1600')]:
 q=next(x for x in qualifications if x['program_id']=='jcu-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'jcu-intl-2025',2025,status='latest_published',note='2025 International Guide 참고값 · 2027 국제환산표 확인 전'),scale=scale)


# New UQ program remains a separate record with accreditation gate.
import copy
p=copy.deepcopy(prog('uq'));p.update(id='uq-pharmd',name=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),duration_years=fact(5,'uq-pharmd'),duration_label=fact('5년 통합','uq-pharmd'),bachelor_award_year=fact(None,'uq-pharmd'),four_year_exit=fact(None,'uq-pharmd'),exit_degree=fact(None,'uq-pharmd'),final_degree=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),highlights=['신설 5년 통합','Internship 통합 설계','인증 승인 대기'],editorial='2027 신설 5년 PharmD입니다. Intern training을 학위에 포함하도록 설계됐고 APC·Pharmacy Board 승인을 진행 중입니다.',accreditation=fact('APC 인증·Pharmacy Board 승인 아직 미획득','uq-pharmd',status='pending_2027'),review_items=['APC accreditation 및 Board approval','신규 과정 qualification별 기준','학사 중간 Exit 여부'])
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
route('griffith','griffith-college','diploma','Griffith College · Diploma of Health Sciences','griffith-college',80,2,'본과 잔여 240CP · T1 3년 / T2 3.5년','본과 T1 / T2 · Diploma 개강월 별도 확인','지정 Diploma 과목 이수 + 최종 입학허가','80CP 인정. Diploma 학비·진급 GPA는 업데이트 대기입니다.')
route('curtin','curtin-college','diploma','Curtin College · Pharmacy Diploma','curtin-college',175,2,'Stage 2: 12개월 · Stage 1 필요 시 8–12개월 추가','Stage 1: 2월/6월 · Stage 2: 2월','Stage 2 CWA 70% + PHAR1002(12월) 추가 이수','Stage 2 CWA 70% 기준을 적용합니다.')
route('uq','uq-accelerated','foundation','UQ College · Accelerated Foundation','uq-accelerated',0,1,'약 4개월','2027-02-15 시작 → 07-09 완료 · 본과 07-26','BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','2월 Foundation → 7월 BPharm 일정입니다. GPA·영어·필수과목을 충족해야 합니다.')
routes[-1]['progression']=fact('BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','uq-foundation')
route('uwa','uwa-foundation','foundation','UWA College · Foundation Program','uwa-foundation',0,1,'8개월 또는 12개월','UWA College 일정','UWA College Foundation 70 + Pharmacy 입학·영어조건','Foundation 수료 후 UWA 약대 1학년으로 진학합니다. UWA 약대 공식 페이지에 UWA College Foundation 70이 입학점수로 공개돼 있습니다.')
routes[-1]['progression']=fact('UWA College Foundation 70 + Pharmacy 입학·영어조건','uwa')
route('qut','qut-foundation','foundation','QUT College · Foundation','qut-college-foundation',0,1,'6개월 Intensive 또는 12개월 Standard','QUT College 일정','Foundation 수료 + QUT Pharmacy 입학조건 충족','Foundation 후 QUT Bachelor 1학년으로 진학하는 경로입니다. Pharmacy 선수과목과 영어조건은 별도로 맞춰야 합니다.')
route('sydney','sydney-usfp','foundation','USFP · University of Sydney Foundation Program','sydney',0,1,None,None,'Pharmacy GPA 7.3 / English C','2027 Pharmacy 진학 기준입니다. 수학과 Foundation 입학조건을 충족해야 합니다.')
route('monash','monash-foundation','foundation','Monash University Foundation Year','monash-foundation',0,1,None,None,None,'새 P6007 진급점수는 아직 발표되지 않았습니다.',False)
route('newcastle','newcastle-foundation','foundation','Newcastle International College · Foundation Studies','newcastle-foundation',0,1,None,None,None,'2027 진급점수 발표 대기입니다.')
route('monash','monash-ge','graduate','Monash · Graduate Entry','monash',None,3,'관련 학위 + 여름 집중과정 후 3학년 진입',None,'최근 10년 이내 관련 학사 · 평균 70% 이상 · 대학 수준 Human Physiology','최소 기준을 충족한 뒤 경쟁 선발합니다.')
route('rmit','rmit-foundation','foundation','RMIT Foundation Studies','rmit-foundation-equiv',0,1,None,None,'Foundation 65% + Pharmacy Chemistry·Mathematics prerequisite 동등과목 충족','Foundation 후 Pharmacy 1학년으로 지원합니다. Pharmacy의 Chemistry·Mathematics prerequisite를 Foundation에서 충족해야 합니다.')
route('rmit','rmit-associate','other','RMIT · Associate Degree pathway','rmit-pathway',None,None,'Associate 2년 + Bachelor 3년',None,None,'2년 Associate Degree + 약대 3년 경로입니다. 1년 Diploma가 아닙니다.',False)
for i,title in [('latrobe','Foundation · Health / Life Sciences'),('utas','International Foundation')]:
 route(i,i+'-foundation','foundation',title,i,0,1,note='2027 약대 진급조건·유학생 모집 발표 대기입니다.',verified=False)

def scholarship(i,id,name,src,pct=None,kind='pending',automatic=None,competitive=None,eligible=None,duration=None,threshold=None,renewal=None,number=None,exclude=None,note='',pharmacy=None,amount_status=None,pharmacy_src=None):
 scholarships.append(dict(id=id,university_id=i,name=name,amount=fact(pct,src,status=amount_status),award_type='percentage' if pct is not None else None,assessment=kind,
  automatic_assessment=fact(automatic,src),separate_application=fact(not automatic,src) if automatic is not None else fact(None,src),competitive=fact(competitive,src),country_eligibility=fact(eligible,src),duration=fact(duration,src),academic_threshold=fact(threshold,src),renewal_condition=fact(renewal,src),number_available=fact(number,src),course_exclusion=fact(exclude,src),pharmacy_eligible=fact(pharmacy,pharmacy_src or src),note=note))
scholarship('griffith','griffith-merit','International Academic Merit','griffith-scholarship',20,'automatic',True,False,True,'학위 잔여 기간 · 인정학점 제외','GPA 4.5/7 또는 동등 성적','매 학기 전 과목 통과·풀타임 유지',exclude='Diploma 자체 및 제휴기관 제공과정 등 제외',note='한국 국적 대상. Pathway 패키지는 최종 성적 제출 후 심사합니다.',pharmacy=True)
scholarship('sydney','sydney-award','Sydney International Student Award','sydney-scholarship',20,'application',False,False,True,'과정 기간','입학조건 충족 + personal statement','미납 없음·허가 없는 파트타임 전환 금지·정해진 기간 이수',exclude='MBA/EMBA·교환·원격·일부 법학 복수과정 등',note='2027 한국 국적 포함. Personal statement는 3개 항목 각 최대 200단어입니다.',pharmacy=True)
scholarship('monash','monash-merit','Pharmacy and Pharmaceutical Science International Merit','monash-scholarship',[25,50],'competitive',True,True,True,'최소 졸업학점 이수까지','각 대상 과정군 최상위·차상위','매 학기 WAM 70 유지',8,'공식 목록은 P6007 Scholars Program/Doctor of Pharmacy를 대상 과정으로 명시','연 8명 경쟁장학입니다. 50%는 각 과정군 최상위, 25%는 차상위에 수여됩니다. 일반 P6007 전원 적용 장학으로 표시하지 않습니다.',pharmacy=None)
scholarship('jcu','jcu-excellence','International Excellence Scholarship','jcu-scholarship',25,'automatic',True,False,True,'학위 전체 기간','학부: ATAR 65 또는 동등 성적','매 학기 강한 GPA 유지',exclude='Medicine·Dentistry·Diploma·일부 비학위 과정',note='Bachelor of Pharmacy (Honours)는 공식 제외목록에 없습니다.',pharmacy=True)
scholarship('utas','utas-tims','Tasmanian International Merit Scholarship','utas-scholarship-2027',30,'automatic',True,False,True,'학위 전체 기간 · 최대 5년','최종 학력 성적표 기준 merit 심사','정상 등록·학업진행 유지',note='2027 약대는 제외과정 목록에 없습니다. 다른 UTas 장학과 중복 수혜는 불가하며 더 높은 장학이 적용됩니다.',pharmacy=True)
scholarship('curtin','curtin-global-merit','Curtin Global Merit Scholarship','curtin-scholarship-2027',20,'automatic',True,False,True,'학부 최대 4년','최근 학업성적 Distinction 수준','Offer·등록 조건 유지',exclude='공식 제외과정에 Pharmacy 없음',note='2027/2028 WA 캠퍼스 국제학생 대상.',pharmacy=True)
scholarship('uq','uq-excellence','UQ International Excellence Scholarship','uq-scholarship-2027',25,'competitive',True,True,True,'학위 전체 기간','Offer holder 중 대학이 정한 경쟁점수','UQ 장학 약관 충족',note='별도 신청 없이 자동심사합니다. 다른 UQ tuition reduction과 중복 적용하지 않습니다.',pharmacy=True)
scholarship('adelaide','adelaide-merit','Adelaide Merit Scholarship','adelaide-scholarship',15,'automatic',True,False,True,'표준 학위기간','IB 28 · A-level 9 · 기타 국제고교 ATAR 85 상당','Program Term GPA 4.5/7 유지',exclude='공식 제외과정에 Pharmacy 없음',note='Bachelor of Pharmacy (Honours)는 공식 제외과정 목록에 없습니다.',pharmacy=True)
scholarship('latrobe','latrobe-high-achiever','La Trobe High Achiever Scholarship','latrobe-scholarship-2027',[20,25],'automatic',True,False,True,'학위 전체 기간','WAM/ATAR 상당 60–74.9: 20% · 75+: 25%','Full-time 등록·정상 학업진행',note='Bendigo Bachelor of Pharmacy (Honours)는 국제장학 eligible-course 목록에 포함됩니다.',pharmacy=True,pharmacy_src='latrobe-scholarship-courses')
scholarship('latrobe','latrobe-health-innovation-30','La Trobe Health Innovation Scholarship · 30%','latrobe-health-innovation-2027',30,'pending',None,None,True,None,'Minimum WAM 75+','장학 약관 및 Offer 조건 충족',note='La Trobe Pharmacy 과정 페이지에 Future undergraduate · International 대상 30% Health Innovation Scholarship이 표시됩니다. 2026/2027 intake 약관이 적용되며 최종 수여·중복 가능 여부는 Offer에서 확인합니다.',pharmacy=True,pharmacy_src='latrobe-health-innovation-2027')
scholarship('qut','qut-merit','QUT International Merit Scholarship','qut-scholarship-2027',25,'automatic',True,False,True,'학위 전체 기간','입학 성적 기준 충족','QUT 최소 GPA 조건 유지',note='2027 국제학생 가이드 기준. 전 학부/faculty에 제공되는 International Merit Scholarship입니다.',pharmacy=True)
scholarship('newcastle','newcastle-excellence','International Excellence Scholarship 2027','newcastle-scholarship',20,'course_excluded',True,False,True,'해당 없음',None,None,500,'Bachelor of Pharmacy (Honours)','20% 장학 자체는 2027 국제학생 장학이지만 Bachelor of Pharmacy (Honours)는 공식 제외과정입니다.',pharmacy=False,pharmacy_src='newcastle-scholarship-2027-terms')
scholarship('canberra','canberra-international-2027','UC International Scholarships 2027','canberra-guide-2027',[10,20,30],'pending',None,None,None,'학위 조건에 따라 적용','Merit 10%: GPA 5/7 · High Achievers/Excellence는 더 높은 기준',None,note='2027 가이드에 10%·20%·30%가 공개됐지만 지역·과정 제외조건이 있어 한국 학생 Pharmacy 적용은 최종 확인 후 확정합니다.',pharmacy=None)
scholarship('unisq','unisq-support','International Student Support Scholarship 2027','unisq-scholarship-2027',10,'guaranteed',True,False,True,'학위 전체 기간','입학 학업·영어조건 충족','Satisfactory academic performance 유지',note='전 학문분야 국제학생이 대상이며, 조건을 충족하면 Admissions가 자동으로 Offer에 반영합니다.',pharmacy=True)
scholarship('uwa','uwa-global-excellence','UWA Global Excellence Scholarship','uwa-scholarship-current',20,'pending',True,False,True,'학위 전체 기간','2027 세부 점수표 업데이트 대기','장학 약관의 continuation 기준',note='현재 UWA 2027 안내는 최대 20% tuition discount로 표시됩니다. 상세 2027 점수구간 표가 완전히 반영되면 확정값으로 전환합니다.',pharmacy=True,amount_status='pending_2027')
scholarship('rmit','rmit-pending','2027 약대 학위 장학','rmit',None,'pending',None,None,None,note='한국 학생 대상 RMIT UP 영어과정 bursary는 확인됐지만 약대 학위 tuition scholarship은 별도로 확인 중입니다.',pharmacy=None)
scholarship('unsw','unsw-award','International Student Award','unsw-scholarship',20,'not_eligible',None,None,False,note='공식 eligible-country 목록에 South Korea 없음. 한국 국적 기본 장학으로 표시하지 않습니다.',pharmacy=None)

def housing(i,id,name,src,weekly=None,weeks=None,utilities=None,meals=None,campus=None,note=''):
 accommodation.append(dict(id=id,university_id=i,name=name,weekly_cost=fact(weekly,src),contract_weeks=fact(weeks,src),official_contract_total=fact(None,src),utilities=fact(utilities,src),meals=fact(meals,src),campus_distance=fact(campus,src),note=note))
housing('utas','utas-christ','Christ College','utas-housing',316,42,True,False,'Sandy Bay 교내 · 무료 교내 셔틀','2027 주당 요금. 42주 계약은 College 안내 기준. 방 형태·입주 자격·보증금 확인 필요.')
housing('utas','utas-john','John Fisher College','utas-housing',316,42,True,False,'Sandy Bay 교내','2027 주당 요금. 약학 수업 캠퍼스와 통학 동선을 확인하세요.')
housing('latrobe','latrobe-units','The Units','latrobe-housing',240,41,None,None,'Bendigo 캠퍼스','2026 latest reference. 보증금 A$1,000, 퇴실 청소 A$130 별도. 2027 금액 확인 중.')
housing('latrobe','latrobe-villas','The Villas','latrobe-housing',250,41,None,None,'Bendigo 캠퍼스','2026 latest reference. 2027 가격으로 표시하지 않습니다.')
housing('jcu','jcu-townsville-2026','Townsville · University Hall / Rotary','jcu-housing-2026',330,None,True,False,'Townsville 캠퍼스','2026 일반 장기체류 참고요금. Pharmacy 학생이 7일 이상 머무는 경우 별도 academic rate가 적용됩니다.')
housing('jcu','jcu-cairns-2026','Cairns · John Grey Hall Standard','jcu-housing-2026',431,None,True,False,'Cairns 캠퍼스','2026 일반 장기체류 참고요금. Pharmacy 학생의 academic rate는 별도입니다.')
housing('uq','uq-kev-carmody','UQ RES · Kev Carmody House','uq-housing-current',414,None,True,False,'St Lucia','현재 공개 최저가. Pharmacy는 Dutton Park 캠퍼스이므로 통학 동선을 함께 봐야 합니다.')
housing('uq','uq-walcott','UQ RES · Walcott Street','uq-housing-current',439,None,True,False,'St Lucia','현재 공개 최저가. Pharmacy Dutton Park까지 통학이 필요합니다.')
housing('adelaide','adelaide-mattanya-2027','Mattanya · Shared House','adelaide-mattanya-2027',320,52,True,False,'North Adelaide','2027 연 A$16,640 / 52주. 전기·가스·수도·인터넷 포함.')
housing('adelaide','adelaide-village-2027','Adelaide University Village · Shared Bathroom','adelaide-village-2027',380,52,True,False,'Adelaide City','2027 연 A$19,760 / 52주. 전기·가스·수도·인터넷 포함.')
housing('griffith','griffith-village-2027','Griffith University Village · Shared Apartment','griffith-village-2027',329.85,52,True,False,'Gold Coast 캠퍼스','2027 full-year 옵션의 shared-apartment 요금은 방 타입에 따라 달라집니다. A$329.85/week부터 확인됩니다.')
housing('curtin','curtin-perth-housing','Curtin Perth · UniLodge / St Catherine\'s','curtin-housing-current',None,48,None,None,'Bentley 캠퍼스','캠퍼스 안에서 5~10분 거리입니다. 2026 표준 full-year 계약은 48주였고 방별 2027 요금은 운영사에서 확인합니다.')
housing('qut','qut-brisbane-guide','Brisbane 학생숙소 비용 가이드','qut-living-current',None,None,None,None,'Brisbane','QUT 공식 생활비 가이드: student apartment A$1,600~2,200/month, catered accommodation A$2,400~2,650/month.')
housing('rmit','rmit-walert-2027','UniLodge @ RMIT Bundoora · Walert House','rmit-bundoora-2027',310,46,True,False,'Bundoora West 캠퍼스','2027 4-bedroom apartment 1인실 full bed value A$14,260 / 46주. Pharmacy Bundoora 캠퍼스와 가깝습니다.')
housing('newcastle','newcastle-2027','Student Living · Callaghan','newcastle-housing-2027',249.45,None,None,False,'Callaghan 캠퍼스','2027 국제학생 가이드: self-catered A$249.45~465.93/week, 5~7 meals 포함 A$334.45~580.93/week.')
housing('canberra','canberra-campus-west-2027','Campus West','canberra-housing-2027',210.5,None,True,False,'Bruce 캠퍼스','2027 안내 기준 가장 저렴한 12-bedroom apartment room A$210.50/week. 공과금 포함.')
housing('canberra','canberra-weeden-2027','Weeden Lodge · Shared Apartment','canberra-housing-2027',221,None,True,False,'Belconnen · 캠퍼스 도보권','3~7 bedroom apartment room A$221~252/week. 공과금 포함.')
housing('unisq','unisq-rescollege','UniSQ Residential Colleges · Single Bedroom','unisq-housing-current',155,None,None,False,'Toowoomba 캠퍼스','현재 공식 가이드 기준 약 A$155~220/week. Single-bedroom unit은 약 A$275~290+/week.')
housing('monash','monash-parkville-share','Parkville · Private Share Rental','monash-parkville-rent',290,None,None,False,'Parkville 약대 인근','Monash 공식 임대 가이드의 Parkville shared accommodation는 약 A$290~380/week입니다. 실제 매물·공과금 포함 여부는 계약마다 다릅니다.')
housing('sydney','sydney-qmb-2026','Queen Mary Building','sydney-qmb-2026',382,48,None,False,'Camperdown','2026 48주 Standard Room A$382/week. 2027 요금 발표 후 업데이트합니다.')
housing('sydney','sydney-regiment-2026','Regiment','sydney-regiment-2026',408,None,None,False,'Darlington · 캠퍼스 5분','2026 Standard Room A$408/week. 2027 요금 발표 후 업데이트합니다.')
housing('unsw','unsw-2027-status','UNSW 2027 학생숙소','unsw-housing-2027',None,None,True,False,'Kensington','Barker Street Apartments는 2027에 운영하지 않습니다. 다른 UNSW apartments/colleges의 2027 모집·요금을 공식 accommodation portal에서 확인해야 합니다.')
housing('uwa','uwa-trinity-2027','Trinity Residential College · Standard Room','uwa-trinity-2027',595,None,True,True,'UWA College Row · Crawley','2027 Standard Room A$595/week. 3 meals/day, utilities, Wi-Fi, room cleaning 등이 포함됩니다.')

conflicts=[
 dict(id='curtin-progression',entity_id='curtin-college',field='progression',source_ids=['curtin-college','curtin-old'],status='source_conflict',summary='Stage 2 CWA: 현재 College 70% / 구 과정 안내 65%',decision='현재 메인 College 70% 우선. 입학팀 확인 전 충돌 기록 유지.'),
 dict(id='newcastle-english',entity_id='newcastle-bpharm-hons',field='english',source_ids=['newcastle-2027-course','newcastle-fee-2027'],status='source_conflict',summary='Newcastle 2027 Degree Guide는 IELTS 6.5/각6.5, 현재 과정 페이지 English proficiency section은 7.0/각7.0으로 표기',decision='같은 대학의 2027 공식자료 간 차이이므로 자동 충족 판정에서 제외. 지원 전 Newcastle Admissions 서면 확인.'),
 dict(id='monash-foundation-version',entity_id='monash-foundation',field='progression',source_ids=['monash-foundation','monash'],status='pending_2027',summary='Pathway guide 구 P6001과 새 P6007 과정 코드 차이',decision='기존 progression 점수 이식 금지.'),
]
# Canberra 2027 course PDF verified after initial seed.
source('canberra-2027','Canberra Bachelor of Pharmacy HLB301 · 2027','https://www.canberra.edu.au/course/HLB301/1/2027.pdf',2027,'official_course')
setp('canberra',name=fact('Bachelor of Pharmacy · Honours option','canberra-2027'),final_degree=fact('Bachelor of Pharmacy · Honours option available','canberra-2027'),international_recruitment=fact(True,'canberra-2027'),highlights=['4년 Bachelor of Pharmacy','Honours 선택 가능','Canberra · Regional'],editorial='4년 Bachelor of Pharmacy 과정입니다. 성적과 Honours 요건을 충족하면 Bachelor of Pharmacy (Honours)로 졸업할 수 있습니다.')
eng('canberra',7,{'L':7,'R':7,'W':7,'S':7},src='canberra-2027');intake('canberra',[2],'2027-02-15 · Semester 1','canberra-2027')
req('canberra','assumed','assumed','assumed','assumed','수학 + Biology/Human Movement, Chemistry/Physics는 assumed knowledge로 안내. 필수 prerequisite와 구분.',src='canberra-2027')
for route_record in routes:
 route_record['intake_months']=fact([2],'uq-accelerated') if route_record['id']=='uq-accelerated' else fact([2],'curtin-college') if route_record['id']=='curtin-college' else fact(None,route_record['availability']['source_id'])

# Additional course-specific official checks, 2026-09-24.
source('curtin-structure','Curtin · 2026 개편 Pharmacy 구조','https://www.curtin.edu.au/news/advice/how-to-become-a-pharmacist/',2026,'official_course')
setp('curtin',duration_years=fact(3.75,'curtin-structure'),duration_label=fact('3년 9개월','curtin-structure'),bachelor_award_year=fact(3.75,'curtin-structure'),highlights=['3년 9개월','Diploma → 2학년','Perth · Regional'],editorial='Bachelor of Pharmacy (Honours)는 3년 9개월입니다. Curtin College Pharmacy Diploma 후에는 약대 2학년으로 진학합니다.',review_items=['2027 국제학생 학비']); intake('curtin',[2],'Semester 1 · 2월',src='curtin')
req('curtin','required','required','recommended',grade='Chemistry와 Mathematics ATAR 또는 인정 동등 과목. Biology/Human Biology는 권장.',src='curtin-structure')
row(registration,'curtin').update(supervised_practice_in_degree=fact(False,'curtin-structure'),post_graduation_internship=fact(True,'curtin-structure'))
source('unisq-course','UniSQ · International Bachelor of Pharmacy (Honours)','https://www.unisq.edu.au/study/degrees-and-courses/bachelor-of-pharmacy-honours?studentType=international',None,'official_course')
eng('unisq',7,{'L':7,'R':7,'W':6.5,'S':7},src='unisq-course')
req('unisq','assumed','assumed','assumed','assumed','English C, Mathematical Methods/Specialist C, Biology/Chemistry/Physics 중 하나 C는 assumed knowledge.',src='unisq-course')
fee('unisq',34280,src='unisq-course',year=2026,load='8 units / year · 2026 국제학생 참고값')
setp('unisq',editorial='2027은 Trimester 1 입학입니다. 3년 가속과정은 2028부터 시작합니다.',review_items=['2027 학비','T1 최종 개설 일정','2027 장학금 적용'])
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
  route_record['note']='아래 표에 성적·선수과목·영어 기준을 정리했습니다.'
# A blocked source is not a completed verification.
sources['board']['verified_date']=None
sources['board']['retrieval_status']='blocked_403'

decision_lenses={
  "jcu": {
    "why": [
      "3년 Fast-track",
      "Townsville·Cairns·Mackay 모두 Regional",
      "화학은 권장, 수학은 필요"
    ],
    "watch": [
      "2027 국제학생 학비 발표 대기"
    ]
  },
  "utas": {
    "why": [
      "3년 Fast-track",
      "Tasmania 요건 충족 시 두 번째 485 +2년",
      "2027 국제장학 30% 자동심사"
    ],
    "watch": [
      "Foundation의 2027 약대 진급조건 발표 대기"
    ]
  },
  "curtin": {
    "why": [
      "3년 9개월",
      "Curtin College Diploma → 약대 2학년",
      "Perth 지역요건 충족 시 두 번째 485 +1년"
    ],
    "watch": [
      "2027 국제학생 학비 발표 대기"
    ]
  },
  "uq": {
    "why": [
      "2월 4년 · 7월 약 3.5년",
      "Accelerated Foundation → 7월 BPharm 연결",
      "2027 국제장학 25% 경쟁 선발"
    ],
    "watch": [
      "신설 5년 PharmD는 APC·Pharmacy Board 승인 진행 중"
    ]
  },
  "adelaide": {
    "why": [
      "4년 Bachelor of Pharmacy (Honours)",
      "7월은 학점 인정 학생 개별 심사",
      "Adelaide 지역요건 충족 시 두 번째 485 +1년"
    ],
    "watch": [
      "7월 입학을 일반 고졸 Direct 입학으로 보면 안 됨"
    ]
  },
  "griffith": {
    "why": [
      "Griffith College Diploma → 약대 2학년",
      "Gold Coast Regional",
      "2027 International Academic Merit 20%"
    ],
    "watch": [
      "2027 Direct 학비·국제학생 입학점수 최종 업데이트 대기"
    ]
  },
  "latrobe": {
    "why": [
      "Bendigo Regional · Category 3",
      "과학 선수과목 별도 요구 없음",
      "2027 Health Innovation 30% · High Achiever 20~25%"
    ],
    "watch": [
      "2027 국제학생 학비 발표 대기"
    ]
  },
  "qut": {
    "why": [
      "Chemistry·Math는 필수가 아니라 assumed knowledge",
      "QUT College Foundation 경로",
      "2027 International Merit 25%"
    ],
    "watch": [
      "Brisbane은 지역 추가 485 대상 아님"
    ]
  },
  "rmit": {
    "why": [
      "한국 고교 75% 또는 고교 졸업 + 수능 300부터 Direct 기준",
      "RMIT Foundation → 약대 1학년 가능",
      "2027 학비 A$49,920"
    ],
    "watch": [
      "Chemistry + Mathematics prerequisite 필요",
      "Associate Degree 경로는 1년 Diploma와 다름",
      "약대 학위 장학은 별도 확인 중"
    ]
  },
  "newcastle": {
    "why": [
      "2027 학비 A$51,665",
      "Newcastle Regional",
      "Foundation 경로 있음"
    ],
    "watch": [
      "공식 영어자료가 6.5와 7.0으로 충돌해 지원 전 서면 확인 필요",
      "2027 20% International Excellence는 Pharmacy 제외"
    ]
  },
  "canberra": {
    "why": [
      "4년 Bachelor of Pharmacy",
      "Honours 선택 가능",
      "Canberra Regional + ACT 약사 직종 nomination list 포함"
    ],
    "watch": [
      "2027 가이드의 A$42,500은 2026 Annual Fee 표기",
      "장학 10~30%의 Pharmacy/Korea 적용 최종 확인 필요"
    ]
  },
  "unisq": {
    "why": [
      "Toowoomba Category 3",
      "2027 국제학생 Trimester 1",
      "2027 국제장학 10% 조건 충족 시 자동"
    ],
    "watch": [
      "3년 가속과정은 2028부터이며 2027에는 적용하지 않음"
    ]
  },
  "monash": {
    "why": [
      "4년 BPharm(Hons) Exit + 5년 PharmD",
      "5년차 paid supervised practice",
      "Graduate Entry 있음"
    ],
    "watch": [
      "2027 Foundation → 새 P6007 진급점수 발표 대기",
      "Melbourne은 지역 추가 485 대상 아님"
    ]
  },
  "sydney": {
    "why": [
      "5년 BPharm(Hons) / Master of Pharmacy Practice",
      "2027 수능·IB·SAT·A-level 공식 점수 공개",
      "USFP Foundation 경로"
    ],
    "watch": [
      "Sydney는 지역 추가 485 대상 아님"
    ]
  },
  "unsw": {
    "why": [
      "2027부터 Doctor of Pharmacy 명칭",
      "5년 통합 과정",
      "2027 IB·A-level 기준 확인"
    ],
    "watch": [
      "졸업 후 인턴십은 별도",
      "2027 학비 발표 대기"
    ]
  },
  "uwa": {
    "why": [
      "고교 졸업 후 4년 Bachelor + PharmD",
      "UWA College Foundation → 약대 1학년",
      "Perth 지역요건 충족 시 두 번째 485 +1년"
    ],
    "watch": [
      "졸업 후 인턴십은 별도",
      "2027 국제학생 학비·Global Excellence 세부표 업데이트 대기"
    ]
  }
}
for p in programs:
 if p['university_id'] in decision_lenses:p['decision_lens']=decision_lenses[p['university_id']]

data=dict(schema_version='1.0.0',academic_year=2027,verified_date=DATE,universities=universities,programs=programs,entry_routes=routes,qualifications=qualifications,requirements=requirements,english=english,intakes=intakes,tuition=tuition,scholarships=scholarships,accommodation=accommodation,professional_registration=registration,sources=list(sources.values()),conflicts=conflicts)
(ROOT/'data/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
config=dict(site_name='호주약대 가이드',brand='TNS',language='ko',academic_year=2027,production_url=None,production_approved=False,
 channels=[dict(id='kakao',label='카카오톡 상담',detail='내 조건으로 1:1 상담',url='https://open.kakao.com/o/slehLvKi',source='tnsuhak/xjtlu-korea main index.html'),dict(id='phone',label='전화 상담',detail='02-3288-1733',url='tel:0232881733',source='tnsuhak/xjtlu-korea main index.html'),dict(id='australia-chat',label='호주 오픈채팅',detail='승인된 호주 전용 링크 확인 중',url=None,source=None),dict(id='cafe',label='네이버 카페',detail='TNS 유학 커뮤니티',url='https://cafe.naver.com/tnsuhak.cafe',source='tnsuhak/xjtlu-korea main index.html')])
(ROOT/'data/site.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(f'{len(universities)} universities / {len(programs)} programs / {len(routes)} routes / {len(sources)} sources')

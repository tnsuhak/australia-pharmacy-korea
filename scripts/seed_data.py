"""Reproducible, source-linked editorial seed. Run only when regenerating catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-09-25'
sources = {}
def source(key, title, url, year=None, kind='official_course', verified_date=None):
    sources[key] = dict(id=key, title=title, url=url, source_year=year,
                        source_type=kind, verified_date=verified_date or DATE)
    return key
def fact(value=None, src=None, year=None, status=None, note=''):
    s=sources.get(src,{})
    return dict(value=value, academic_year=2027, source_year=year or s.get('source_year'),
                source_id=src, source_url=s.get('url'), source_type=s.get('source_type'),
                verified_date=s.get('verified_date') if src else None,
                status=status or ('pending_2027' if value is None else 'confirmed_2027' if (year or s.get('source_year'))==2027 else 'latest_published'),
                note=note)

source('apc','APC 호주 약학 학위 인증 목록 · 2026-07-08 기준','https://www.pharmacycouncil.org.au/education-provider/accreditation/pharmacy-degree-programs-australia/accredited-pharmacy-degree-programs/',2026,'accreditation')
source('board','Pharmacy Board · Internships','https://www.pharmacyboard.gov.au/Registration/Internships.aspx',None,'regulator')
source('apc-exam','APC · Intern written examination','https://www.pharmacycouncil.org.au/pharmacist/skills-assessment/intern-written-exam/',None,'regulator')
source('korea-law','약사법 제3조 · 2026-09-11 시행','https://law.go.kr/lsLawLinkInfo.do?chrClsCd=010202&lsJoLnkSeq=1000328184',2026,'government')
source('kuksiwon','국시원 · 외국대학 인정기준','https://www.kuksiwon.or.kr/infoOpen/list.do?seq=82',None,'government')
source('korea-recognized-schools-20260602','국시원 · 보건복지부장관이 인정하는 외국학교 현황 · 2026-06-02','https://www.data.go.kr/data/15126577/fileData.do',2026,'government')
source('korea-foreign-school-process','보건복지부 · 외국학교 졸업자의 보건의료인국가시험 응시절차','https://www.mohw.go.kr/menu.es?mid=a10702020300',2026,'government')
source('korea-pharmacist-exam-current','국시원 · 약사 직종별 시험정보 · 2026/2027 일정','https://www.kuksiwon.or.kr/subcnt/c_2009/1/view.do?seq=7&itm_seq=06',2026,'government')
source('korea-pharmacist-exam-law','약사법 시행령 · 약사예비시험/국가시험 과목·합격기준','https://law.go.kr/lsLinkCommonInfo.do?chrClsCd=010202&lspttninfSeq=116746',2026,'government')
source('adelaide-new-entity-2026','Adelaide University · new legal entity from UniSA and University of Adelaide','https://adelaide.edu.au/about/organisational-structure/corporate/finance/suppliers-and-customers/',2026,'official_university')
source('homeaffairs-485','Australian Home Affairs · Temporary Graduate visa (subclass 485) Post-Higher Education Work','https://immi.homeaffairs.gov.au/Visa-subsite/Pages/work/485-post-study-work.aspx',2026,'government')
source('homeaffairs-second485','Australian Home Affairs · Second Post-Higher Education Work stream','https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/temporary-graduate-485/second-post-higher-education-work',2026,'government')
source('homeaffairs-regional','Australian Home Affairs · Designated regional area postcodes','https://immi.homeaffairs.gov.au/supporting/Pages/Work/187-regional-postcodes.aspx',2026,'government')
source('jcu-2027-campus','JCU · 2027 course changes · Pharmacy campuses','https://www.jcu.edu.au/future-students/schools/2027-course-changes',2027,'official_course')
source('jcu-english-band3a','JCU · Admissions Policy Schedule II · Band 3a English equivalencies','https://www.jcu.edu.au/policy/academic-governance/student-experience/admissions-policy-schedule-ii',None,'official_admissions')
source('jcu-prep-current','JCU Prep · current eligibility and pathway guidance','https://study.jcu.edu.au/jcu-prep',None,'official_pathway')
source('utas-2027-campus','University of Tasmania · Bachelor of Pharmacy with Honours 2027','https://www.utas.edu.au/courses/health/courses/54d-bachelor-of-pharmacy-with-honours',2027,'official_course')
source('utas-entry-country-current','UTas · Entry requirements by country','https://www.utas.edu.au/study/apply/admission-requirements/entry-requirements-by-country',None,'official_admissions')
source('utas-atar-equiv-current','UTas · Equivalent undergraduate entry requirements · current linked ATAR equivalency table','https://www.utas.edu.au/__data/assets/pdf_file/0011/1673759/MST-ISR-ATAR_Equivilance-Table.pdf',2023,'official_admissions')
source('uwa-dpharm','UWA · Doctor of Pharmacy graduate entry','https://www.uwa.edu.au/study/courses/doctor-of-pharmacy',2027,'official_course')
source('migration-nsw-skills','NSW Government · NSW Skills Lists','https://www.nsw.gov.au/visas-and-migration/skilled-visas/nsw-skills-lists',2026,'government')
source('migration-qld-list','Migration Queensland · Queensland onshore skilled occupation list','https://migration.qld.gov.au/occupation-lists/queensland-onshore-skilled-occupation-list',2026,'government')
source('migration-qld-status','Migration Queensland · Skilled migration ROI status','https://migration.qld.gov.au/visa-options/skilled-visas/registering-your-interest-in-queenslands-migration-program',2026,'government')
source('migration-qld-2026-consultation','Migration Queensland · 2026-27 QSOL consultation status','https://migration.qld.gov.au/dama-consultation',2026,'government')
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
source('uq-guaranteed-atar-2027','UQ · 2027 Guaranteed ATAR · Pharmacy 80','https://study.uq.edu.au/admissions/undergraduate/review-entry-requirements/guaranteed-atar',2027,'official_admissions')
source('uq-standard-foundation-2027','UQ College · Standard Foundation 2026/2027 dates and fees','https://uqcollege.uq.edu.au/study/pathways-uq/foundation-program/standard-foundation-program',2027,'official_pathway')
source('uq-foundation-entry-current','UQ College · Foundation academic entry requirements · Korea','https://uqcollege.uq.edu.au/files/8781/uq-college-foundation-program-academic-requirements.pdf',2026,'official_pathway',verified_date='2026-09-26')
source('curtin-scholarship-2027','Curtin Global Merit Scholarship · 2027 commencement','https://scholarships.curtin.edu.au/Scholarship/?id=7986',2027,'official_scholarship')
source('curtin-college-fees-2027','Curtin College · 2027 international Diploma fees','https://www.curtincollege.edu.au/how-apply/international/fees-payment/',2027,'official_pathway')
source('utas-scholarship-2027','UTas Tasmanian International Merit Scholarship · 2027 terms','https://www.utas.edu.au/study/scholarships-fees-and-costs/international-scholarships/tasmanian-international-merit-scholarship',2027,'official_scholarship')
source('utas-ipc-fees-2027','UTas International Pathway College · 2027 Foundation fees and intakes','https://utas.up.education/fees-and-intakes/',2027,'official_pathway')
source('utas-ipc-foundation','UTas International Pathway College · Foundation Pharmacy progression','https://utas.up.education/foundation-studies/',None,'official_pathway')
source('utas-ipc-entry','UTas International Pathway College · country and English entry requirements','https://utas.up.education/applying/entry-requirements/',None,'official_pathway')
source('unisq-scholarship-2027','UniSQ International Student Support Scholarship 2027','https://www.unisq.edu.au/scholarships/unisqi-international-student-support-scholarship-2027',2027,'official_scholarship')
source('unisq-scholarship-terms-2027','UniSQ · International Student Support Scholarship 2027 · Terms and Conditions','https://www.unisq.edu.au/-/media/usq/scholarships/unisq-intl-award-conditions/award-conditions_international-student-support-scholarship-2027.ashx',2027,'official_scholarship')
source('adelaide-scholarship','Adelaide Merit Scholarship 15%','https://adelaide.edu.au/study/scholarships/int/adelaide-merit-scholarship-15/',None,'official_scholarship')
source('latrobe-scholarship-2027','La Trobe High Achiever Scholarship · 2026/2027','https://www.latrobe.edu.au/study/scholarships/other/la-trobe-high-achiever-scholarship',2027,'official_scholarship')
source('latrobe-scholarship-courses','La Trobe · Courses offering international scholarships','https://www.latrobe.edu.au/study/scholarships/advice/courses-offering-international-scholarships',2027,'official_scholarship')
source('latrobe-health-innovation-2027','La Trobe Health Innovation Scholarship · 30% · 2026/2027 intakes','https://www.latrobe.edu.au/international/applying/scholarships',2027,'official_scholarship')
source('latrobe-vc-2027','La Trobe Vice Chancellor Scholarship · 50%/100% · 2027','https://www.latrobe.edu.au/study/scholarships/other/la-trobe-vice-chancellor-scholarship',2027,'official_scholarship',verified_date='2026-09-27')
source('latrobe-scholarship-terms-2027','La Trobe international scholarship terms · 2026/2027 intakes','https://www.latrobe.edu.au/international/tc/la-trobe-high-achievers-scholarship-terms-and-conditions',2027,'official_scholarship')
source('canberra-guide-2027','University of Canberra International Course Guide 2027 · Scholarships','https://www.canberra.edu.au/content/dam/uc/documents/agent-marketing-toolkit/international-course-guide/international-course-guide.pdf',2027,'official_guide')
source('canberra-scholarship-conditions-current','University of Canberra · International Scholarships Conditions of Award','https://www.canberra.edu.au/content/dam/uc/documents/scholarships/conditions/uc-international-scholarships.pdf',None,'official_scholarship')
source('uwa-scholarship-current','UWA Global Excellence Scholarship','https://www.uwa.edu.au/study/scholarships-and-fees/scholarships/international-scholarships/global-excellence-scholarship',2027,'official_scholarship')
source('newcastle-scholarship-2027-terms','Newcastle International Excellence Scholarship 2027 · Terms & Conditions · excluded programs','https://www.newcastle.edu.au/__data/assets/pdf_file/0014/1136300/UNI_053-International-Excellence-Scholarship-2027-T-and-Cs-07072026.pdf',2027,'official_scholarship')
source('uwa-foundation','UWA College · UWA Foundation Program','https://www.uwa.edu.au/uwa-college/Study/UWA-Foundation-Program',None,'official_pathway')
source('uwa-combined-rules-current','UWA Handbook · Combined Courses English requirements','https://www.handbooks.uwa.edu.au/rules?id=69909',2026,'official_handbook')
source('uwa-foundation-8-current','UWA Handbook · UWA Foundation Program 8 months','https://www.handbooks.uwa.edu.au/college/coursedetails?code=UWC00',2026,'official_handbook')
source('uwa-foundation-12-current','UWA Handbook · UWA Foundation Program Extended 12 months','https://www.handbooks.uwa.edu.au/college/coursedetails?code=UWC10',2026,'official_handbook')
source('uwa-college-brochure-2025','UWA College · 2025 pathway brochure · country entry table','https://www.uwa.edu.au/uwa-college/-/media/project/uwa/uwa/uwa-college/docs/2025-uwa-college-brochure.pdf',2025,'official_guide')
source('qut-college-foundation','QUT College · Foundation programs','https://www.qut.edu.au/study/qut-college/international/english-language-programs',None,'official_pathway')
source('qut-foundation-standard-2027','QUT College · Standard Foundation Program · 2027 fee and entry','https://www.qut.edu.au/courses/standard-foundation',2027,'official_pathway')
source('qut-foundation-intensive-2027','QUT College · Intensive Program · 2027 fee and entry','https://www.qut.edu.au/courses/intensive-program',2027,'official_pathway')
source('qut-college-merit-current','QUT College Merit Scholarship · South Korea criteria','https://www.qut.edu.au/study/fees-and-scholarships/scholarships/qut-college-merit-scholarship',None,'official_scholarship')
source('qut-fee-2027','QUT · Bachelor of Pharmacy (Honours) 2027 fee','https://www.qut.edu.au/courses/bachelor-of-pharmacy-honours',2027,'official_course')
source('newcastle-fee-2027','University of Newcastle · 2027 International Student Degree Guide · Pharmacy','https://www.newcastle.edu.au/__data/assets/pdf_file/0020/1102565/2025-1079-International-Prospectus-2027-ROW_V27.pdf',2027,'official_guide')
source('monash-fee-2027','Monash Pharmacy · 2027 international fee','https://www.monash.edu/study/courses/find-a-course/pharmacy-p6007',2027,'official_course',verified_date='2026-09-26')
source('monash-curriculum-2027','Monash · Undergraduate Pharmacy for International Students · 2027 curriculum','https://www.monash.edu/pharm/future/courses/undergraduate-pharmacy-international',2027,'official_course')
source('jcu-fee-2026','JCU · Bachelor of Pharmacy (Honours) 2026 fee','https://www.jcu.edu.au/courses/bachelor-of-pharmacy-honours',2026,'official_course')
source('unsw-fee-2026','UNSW · Pharmaceutical Medicine / Pharmacy 2026 fee','https://www.unsw.edu.au/study/undergraduate/bachelor-of-pharmaceutical-medicine-master-of-pharmacy',2026,'official_course')
source('uwa-fee-2026','UWA · 2026 international undergraduate fees CM039','https://www.fees.uwa.edu.au/Browse/BrowseCourses?feeType=INTUG&feeYear=2026',2026,'official_fee')
source('adelaide-fee-current','Adelaide University · Bachelor of Pharmacy (Honours) · published 2026 international fee','https://adelaide.edu.au/study/degrees/bachelor-of-pharmacy-honours/',2026,'official_course')
source('rmit-2027-apply','RMIT Bachelor of Pharmacy (Honours) · 2027 intake','https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/honours-degrees/bachelor-of-pharmacy-honours-bh102/apply-now',2027,'official_course')
source('unsw-2027-course','UNSW Pharmaceutical Medicine / Doctor of Pharmacy · 2027','https://www.unsw.edu.au/study/undergraduate/bachelor-of-pharmaceutical-medicine-master-of-pharmacy',2027,'official_course')
source('unsw-2027-guide','UNSW · 2027 Undergraduate Student Guide · international ATAR/IB table','https://www.unsw.edu.au/content/dam/pdfs/future-students/2027-DOM-UG-Guide.pdf',2027,'official_guide')
source('unsw-english-current','UNSW · English language requirements · Pharmacy exception','https://www.unsw.edu.au/study/how-to-apply/english-language-requirements',None,'official_admissions')
source('unsw-college-student-guide','UNSW College · Student Guide · Pharmacy Foundation progression','https://www.unswcollege.edu.au/content/dam/pdfs/unsw-college/college-student-guide.pdf',None,'official_pathway')
source('unsw-college-standard-2027','UNSW College · Standard Foundation Program · 2027 fee','https://www.unswcollege.edu.au/study/standard-program',2027,'official_pathway')
source('latrobe-2027-course','La Trobe Bachelor of Pharmacy (Honours) · 2027 start','https://www.latrobe.edu.au/courses/bachelor-of-pharmacy-honours',2027,'official_course')
source('latrobe-ug-guide-2027','La Trobe University · 2027 Undergraduate Course Guide','https://www.latrobe.edu.au/__data/assets/pdf_file/0010/1819288/La-Trobe-University-Undergraduate-Course-Guide-2027.pdf',2027,'official_guide',verified_date='2026-09-27')
source('curtin-pharmacy-current-guide','Curtin · Pharmacy English requirement guide','https://publications.curtin.edu.au/chinese-student-guide/page/28-29',None,'official_guide')
source('newcastle-2027-course','University of Newcastle · Bachelor of Pharmacy (Honours) current 2027 entry','https://www.newcastle.edu.au/degrees/bachelor-of-pharmacy-honours',2027,'official_course')
source('newcastle-nonstandard-english-2025','University of Newcastle · List of Non-Standard English Entry Programs · 28 Aug 2025','https://policies.newcastle.edu.au/download.php?associated=1&id=855&version=4',2025,'official_policy')
source('newcastle-english-procedure-current','University of Newcastle · English Language Proficiency Procedure · current test equivalencies','https://policies.newcastle.edu.au/document/view-current.php?id=166&version=9',None,'official_policy')
source('newcastle-2026-ug','University of Newcastle · 2026 Undergraduate Degrees guide','https://www.newcastle.edu.au/__data/assets/pdf_file/0012/978438/2026-1088_UG-Prospectus_v3.6_WEB.pdf',2026,'official_guide')
source('monash-pps-2026','Monash Pharmacy and Pharmaceutical Sciences · International UG Course Guide 2026','https://www.monash.edu/__data/assets/pdf_file/0004/4091809/Monash-University-PPS-International-UG-Course-Guide-2026.pdf',2026,'official_guide')
source('rmit-korea-equiv','RMIT · South Korea academic entry equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/south-korea',2027,'official_admissions')
source('rmit-ib-equiv','RMIT · International Baccalaureate academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/international-baccalaureate',2027,'official_admissions')
source('rmit-uk-equiv','RMIT · United Kingdom academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/united-kingdom',2027,'official_admissions')
source('rmit-usa-equiv','RMIT · USA academic equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/usa',2027,'official_admissions')
source('rmit-foundation-equiv','RMIT · Foundation Studies equivalency','https://www.rmit.edu.au/study-with-us/international-students/apply-to-rmit-international-students/entry-requirements/country-equivalency/foundation-equivalencies',2027,'official_pathway')
source('rmit-foundation-2027','RMIT Foundation Studies · 2027 fee and intake','https://www.rmit.edu.au/study-with-us/levels-of-study/pre-university-study/foundation-studies/foundation-studies-fs022/apply-now',2027,'official_pathway')
source('rmit-foundation-current','RMIT Foundation Studies · current entry requirements','https://www.rmit.edu.au/study-with-us/levels-of-study/pre-university-study/foundation-studies/fs022',None,'official_pathway')
source('rmit-medibank-2027','RMIT · Medibank High Achiever International Scholarship 2027','https://www.rmit.edu.au/scholarships/international-scholarships/medibank-high-achiever-international-scholarship',2027,'official_scholarship')
source('rmit-associate-current','RMIT Associate Degree in Applied Science · Pharmacy further study credit','https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/associate-degrees/ad012',None,'official_pathway')
source('rmit-associate-2027','RMIT Associate Degree in Applied Science · 2027 international fee/intake','https://www.rmit.edu.au/study-with-us/levels-of-study/undergraduate-study/associate-degrees/associate-degree-in-applied-science-ad012/apply-now',2027,'official_pathway')
source('jcu-intl-2025','JCU 2025 International Guide · Pharmacy entry scores','https://www.jcu.edu.au/__data/assets/pdf_file/0018/2205414/2025-International-Guide.pdf',2025,'official_guide')
source('newcastle-prospectus-2027','University of Newcastle · 2027 International Prospectus','https://www.newcastle.edu.au/__data/assets/pdf_file/0020/1102565/2025-1079-International-Prospectus-2027-ROW.pdf',2027,'official_guide')
source('adelaide-pharmacy-current','Adelaide University · Bachelor of Pharmacy (Honours) international entry requirements','https://adelaide.edu.au/study/degrees/bachelor-of-pharmacy-honours/',None,'official_course')
source('eynesbury-foundation-2027','Eynesbury · Foundation Studies Program · 2027','https://www.eynesbury.edu.au/programs/international/foundation-studies-program/',2027,'official_pathway',verified_date='2026-09-26')
source('eynesbury-foundation-progression-2026','Eynesbury · Adelaide University Foundation progression requirements · Pharmacy','https://www.eynesbury.edu.au/wp-content/uploads/2026-Eynesbury-Adelaide-University-FSP-Scores-Flyer-v5-FAW-WEB.pdf',2026,'official_pathway',verified_date='2026-09-26')
source('eynesbury-health-diploma-2027','Eynesbury · Diploma of Health Science · Adelaide Pharmacy pathway','https://www.eynesbury.edu.au/programs/international/diploma-programs/health-science/',2027,'official_pathway',verified_date='2026-09-26')
source('eynesbury-entry-current','Eynesbury · International entry requirements','https://www.eynesbury.edu.au/how-apply/international/entry-requirements/',None,'official_pathway',verified_date='2026-09-26')
source('eynesbury-dates-2027','Eynesbury · 2027 Diploma and Foundation key dates','https://www.eynesbury.edu.au/current-students/essential-information/important-dates/',2027,'official_pathway',verified_date='2026-09-26')
source('adelaide-english-current','Adelaide University · English language test equivalency table','https://adelaide.edu.au/study/international-students/how-to-apply/entry-requirements/english-language-proficiency/',None,'official_admissions')
source('latrobe-health-guide','La Trobe · International Health Discipline Handbook · Pharmacy','https://www.latrobe.edu.au/international/documents/international-handbooks/LTU-Health-Discipline-Handbook.pdf',2026,'official_guide')
source('latrobe-foundation-current','La Trobe College · Foundation Studies Health, Life Sciences and Engineering','https://www.latrobecollegeaustralia.edu.au/study-options/foundation-studies/health-life-sciences/',None,'official_pathway')
source('latrobe-foundation-transfer','La Trobe College · Foundation Studies transfer criteria','https://www.latrobecollegeaustralia.edu.au/study-options/transferring-university/',None,'official_pathway')
source('latrobe-foundation-plan','La Trobe College · Foundation Health and Life Sciences study plan','https://www.latrobecollegeaustralia.edu.au/wp-content/uploads/webpage-study-plan-guide.pdf',None,'official_pathway')
source('latrobe-foundation-fee-2026','La Trobe College · 2026 Foundation Studies fee','https://www.latrobecollegeaustralia.edu.au/how-apply/fees/',2026,'official_pathway')
source('latrobe-foundation-english-2026','La Trobe College · 2026 international English entry requirements','https://www.latrobecollegeaustralia.edu.au/wp-content/uploads/LTCA260107-1149-International-Guide-2026-Update-FAW_Web.pdf',2026,'official_pathway')
source('griffith-2026-guide','Griffith University · 2026 International Student Guide · Pharmacy','https://www.griffith.edu.au/__data/assets/pdf_file/0035/2193587/Griffith-University-2026-International-Study-Guide-Digital.pdf',2026,'official_guide')
course_urls={
 'jcu':'https://www.jcu.edu.au/courses/bachelor-of-pharmacy-honours',
 'utas':'https://www.utas.edu.au/courses/health/courses/54d-bachelor-of-pharmacy-with-honours',
 'curtin':'https://www.curtin.edu.au/study/offering/course-ug-bachelor-of-pharmacy-honours--bh-pharma/',
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
source('sydney-structure','Sydney Pharmacy · current course resolutions','https://www.sydney.edu.au/handbooks/medicine-health/coursework/pharmacy/course-resolutions.html',2026,'official_handbook')
source('sydney-prereqs-current','Sydney Academic Board · Pharmacy course prerequisites and assumed knowledge','https://www.sydney.edu.au/content/dam/corporate/documents/about-us/governance-and-structure/academic-board/ab-standards---guidelines-/course-prerquisite-assumed-knowledge-recommended-studies-table.pdf',2025,'official_admissions')
source('sydney-guide','Sydney international guide','https://www.sydney.edu.au/dam/corporate/documents/study/guides/usyd-international-guide.pdf',2027,'official_guide')
source('griffith-college','Griffith · College articulation 107343','https://credit-precedent.sds.na.ce.griffith.edu.au/credit_detail.php?pk1=107343',2027,'official_articulation')
source('griffith-college-2027-guide','Griffith College · International Quick Guide 2026–2027 · Health Sciences to Pharmacy','https://www.griffithcollege.edu.au/wp-content/uploads/Griffith-College-International-Quick-Guide-2026-2027.pdf',2027,'official_pathway')
source('griffith-guaranteed-2027','Griffith · 2027 Guaranteed Admission Scheme · Pharmacy rank 76','https://www.griffith.edu.au/apply/guaranteed-admission-scheme',2027,'official_admissions')
source('griffith-college-health','Griffith College · Diploma of Health Sciences','https://www.griffithcollege.edu.au/study-options/diploma/health-sciences/',None,'official_pathway')
source('griffith-college-dates-2027','Griffith College · 2027 key dates','https://www.griffithcollege.edu.au/student-life/key-dates/',2027,'official_pathway')
source('griffith-foundation-current','Griffith College · Foundation Program','https://www.griffithcollege.edu.au/study-options/foundation/',2027,'official_pathway',verified_date='2026-09-26')
source('griffith-foundation-pathways','Griffith College · Foundation pathway options','https://www.griffithcollege.edu.au/study-options/foundation/pathway-options/',2027,'official_pathway',verified_date='2026-09-26')
source('curtin-college','Curtin College · Pharmacy Diploma','https://www.curtincollege.edu.au/courses/diplomas/health-sciences/pharmacy/',None,'official_pathway')
source('curtin-college-entry','Curtin College · International academic entry requirements · Pharmacy','https://www.curtincollege.edu.au/how-apply/international/journey/academic-entry-requirements/',None,'official_pathway')
source('curtin-college-english','Curtin College · English requirements · Pharmacy Stage 2','https://www.curtincollege.edu.au/how-apply/international/journey/english-requirements/',None,'official_pathway')
source('uq-foundation','UQ College · Foundation progression','https://uqcollege.uq.edu.au/study/pathways-uq/foundation-program',None,'official_pathway')
source('uq-accelerated','UQ College · Accelerated Foundation','https://uqcollege.uq.edu.au/study/pathways-uq/foundation-program/accelerated-foundation-program',2027,'official_pathway')
source('uq-calendar','UQ College · Academic calendar','https://uqcollege.uq.edu.au/current-students/academic-calendar',2027,'official_calendar')
source('monash-foundation','Monash Pathway Programs 2027 · Pharmacy P6001 표기','https://www.monashcollege.edu.au/__data/assets/pdf_file/0005/4349102/2027-Monash-Pathway-Programs.pdf',2027,'official_pathway')
source('monash-foundation-p6007-current','Monash College · Foundation Year · 5년 Pharmacy/Doctor of Pharmacy 진급','https://www.monashcollege.edu.au/study/courses/foundation-year/fy-data/destination-degrees-2026-single-degrees/pharmacy-and-pharmaceutical-science',None,'official_pathway')
source('monash-foundation-dates-2027','Monash College · Foundation Year 2027 dates','https://www.monashcollege.edu.au/study/courses/foundation-year/dates-and-fees',2027,'official_pathway')
source('monash-direct-2027-guide','Monash 2027 International Undergraduate Course Guide · Pharmacy entry scores','https://www.monash.edu/__data/assets/pdf_file/0005/3941744/undergraduate-international-course-guide.pdf',2027,'official_guide',verified_date='2026-09-26')
source('monash-foundation-korea-current','Monash College Foundation Year · South Korea entry requirements','https://www.monashcollege.edu.au/study/courses/foundation-year/fy-data/2025/mufy-country-data/academic-entry-requirements-by-country2/south-korea',None,'official_pathway',verified_date='2026-09-26')
source('monash-foundation-english-current','Monash College Foundation Year Standard · English entry requirements','https://www.monashcollege.edu.au/study/courses/foundation-year/foundation-year-standard',None,'official_pathway',verified_date='2026-09-26')
source('monash-grad-entry-current','Monash Graduate Entry Pharmacy · current eligibility','https://www.monash.edu/pharm/future/courses/grad-pharmacy',None,'official_course',verified_date='2026-09-26')
source('newcastle-foundation','University of Newcastle College of International Education · Foundation Studies','https://internationalcollege.newcastle.edu.au/foundation-studies',None,'official_pathway')
source('newcastle-foundation-entry','Newcastle CIE · Foundation Studies entry requirements','https://internationalcollege.newcastle.edu.au/entry-requirements',None,'official_pathway')
source('newcastle-foundation-fee-2027','Newcastle CIE · 2027 Foundation Studies fees','https://internationalcollege.newcastle.edu.au/fees',2027,'official_pathway')
source('rmit-pathway','RMIT 2026 degree and diploma guide','https://www.rmit.edu.au/content/dam/rmit/au/en/docs/study/career-advisers/brochures/2026-degree-diploma-guide-rmit-university.pdf',2026,'official_guide')
source('griffith-scholarship','Griffith International Academic Merit Scholarship','https://www.griffith.edu.au/international/scholarships-finance/scholarships/international-academic-merit-scholarship',2027,'official_scholarship')
source('monash-scholarship','Monash Pharmacy and Pharmaceutical Science International Merit Scholarship','https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/pharmacy-international-merit-scholarship-5745',2026,'official_scholarship',verified_date='2026-09-26')
source('monash-international-merit-scholarship','Monash International Merit Scholarship','https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/international-merit-5770',2026,'official_scholarship',verified_date='2026-09-26')
source('monash-international-leadership-scholarship','Monash International Leadership Scholarship','https://www.monash.edu/study/fees-scholarships/scholarships/find-a-scholarship/monash-international-leadership-scholarship-5571Z',2026,'official_scholarship',verified_date='2026-09-26')
source('sydney-scholarship','Sydney International Student Award 2027','https://www.sydney.edu.au/study/fees-and-loans/scholarships/sydney-international-student-award.html',2027,'official_scholarship')
source('sydney-usfp-fees-2027','Taylors College · University of Sydney Foundation Program · 2027 tuition fees','https://www.taylorssydney.edu.au/how-apply/fees/',2027,'official_pathway')
source('sydney-usfp-dates-current','Taylors College · University of Sydney Foundation Program · current term dates','https://www.taylorssydney.edu.au/programs/term-dates/',None,'official_pathway')
source('unsw-scholarship','UNSW International Student Award · 국가 목록','https://www.scholarships.unsw.edu.au/sites/default/files/2026-04/International%20Student%20Award_List%20of%20Eligible%20Countries.pdf',2026,'official_scholarship')
source('newcastle-scholarship','Newcastle International Excellence Scholarship 2027','https://www.newcastle.edu.au/scholarships/UNI_053',2027,'official_scholarship')
source('jcu-scholarship','JCU · International Excellence Scholarship','https://www.jcu.edu.au/scholarships/search/international-excellence-scholarship',None,'official_scholarship')
source('utas-housing','UTas · Hobart accommodation 2027','https://www.utas.edu.au/uni-life/accommodation/hobart',2027,'official_accommodation')
source('utas-christ','UTas · Christ College','https://www.utas.edu.au/uni-life/accommodation/hobart/christ-college',2027,'official_accommodation')
source('latrobe-housing','La Trobe · Bendigo accommodation rates 2026','https://www.latrobe.edu.au/__data/assets/pdf_file/0008/1388663/Bendigo-Accommodation-Rates-2026.pdf',2026,'official_accommodation')
source('latrobe-units','La Trobe · The Units · current live rate','https://www.latrobe.edu.au/accommodation/bendigo-campus/units',None,'official_accommodation')
source('latrobe-villas-current','La Trobe · The Villas · current live rate','https://www.latrobe.edu.au/accommodation/bendigo-campus/villas',None,'official_accommodation')

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
next(u for u in universities if u['id']=='jcu')['campus']=fact('Townsville · Cairns · Mackay','jcu-2027-campus')
next(u for u in universities if u['id']=='utas')['campus']=fact('Cradle Coast · Hobart · Launceston','utas-2027-campus')
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

setp('jcu',highlights=['3년 Fast-track','Townsville · Cairns · Mackay','화학 권장 · 수학 필수'],editorial='2027 공식 course changes에서 Townsville·Cairns·Mackay 모두 2월 시작의 3년 Trimester 과정으로 확인됩니다. 현재 국제학생 course page도 세 캠퍼스를 모두 표시하지만 학비는 아직 2026 A$31,710을 보여주므로 2027 학비로 승격하지 않습니다.',review_items=['2027 국제학생 학비','한국 학력 환산표','JCU Prep의 국제학생 packaged pathway 적용 여부'])
req('jcu','recommended','required',grade='English와 General Mathematics 또는 동등 수준. Chemistry 권장.',src='jcu-guide'); intake('jcu',[2],'2월','jcu-guide'); fee('jcu',31710,src='jcu-fee-2026',year=2026); eng('jcu',7.0,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='jcu-guide',pte=65,pte_each=58)
row(english,'jcu')['pte_overall']=fact(65,'jcu-english-band3a'); row(english,'jcu')['pte_each']=fact(58,'jcu-english-band3a'); row(english,'jcu')['toefl']=fact({'overall':94,'L':23,'R':23,'W':23,'S':23},'jcu-english-band3a')
setp('utas',highlights=['3년 Fast-track','Cradle Coast · Hobart · Launceston','2027 학비·30% Merit'],editorial='2027 과정은 Cradle Coast·Hobart·Launceston 세 캠퍼스에서 국제학생이 전체 3년을 이수할 수 있습니다. 일반 4년 약학과 분량을 3년에 압축해 연간 수강량이 많은 편입니다.')
fee('utas',61267,total=198050,load='연간 133 credit points 기준'); eng('utas',6.5,{'L':6,'R':6,'W':6,'S':6},src='utas'); intake('utas',None,'Semester 1 · Cradle Coast / Hobart / Launceston',src='utas'); req('utas','Chemistry 또는 Physical Sciences 중 1과목','required','not_required','not_required','Mathematics 1과목 + Chemistry 또는 Physical Sciences에서 satisfactory achievement',src='utas-2027-campus')
setp('curtin',highlights=['College → Year 2','175 credits','진급 CWA 확인'],editorial='Curtin College Diploma 후 약대 2학년으로 진학합니다. Stage 2 CWA 70%와 PHAR1002가 필요합니다.',review_items=['국제학생 2027 학비','2027 국제학생 Direct 시작월','Global Merit의 Pharmacy 제외 여부']); eng('curtin',7.0,{'L':7,'R':7,'W':7,'S':7},src='curtin')
setp('uq',duration_label=fact('2월 4년 · 7월 약 3.5년','uq'),highlights=['2027 Guaranteed ATAR 80','2월 4년 · 7월 3.5년','Accelerated Foundation'],editorial='2027 BPharm(Hons)은 2월 입학 4년, 7월 입학 약 3.5년입니다. UQ가 2027 Pharmacy guaranteed ATAR를 80으로 공개했으며, 해외학력은 별도 동등성 환산이 필요합니다. 새 5년 PharmD와는 다른 과정입니다.')
req('uq','required','required','recommended',grade='English·수학·Chemistry: Queensland Year 12 C 또는 동등 수준.'); intake('uq',[2,7],'2월 22일 / 7월 26일'); fee('uq',60952,load='16 units 기준')
eng('uq',6.5,{'L':6,'R':6,'W':6,'S':6},pte=64,pte_each=60,toefl={'overall':87,'L':19,'R':19,'W':21,'S':19})
setp('adelaide',highlights=['4년 BPharm(Hons)','CSAT 345','5년 BPharm+Master 연계 가능'],editorial='일반 Direct는 2월 시작입니다. 7월 입학은 학점이 인정된 국제학생을 개별 심사합니다. 현재 과정 페이지의 A$54,300은 2026 입학생 학비라고 명시돼 있어 2027 학비로 사용하지 않습니다. BPharm 과정 안에는 약 12주 실무·임상 placement가 포함되지만, BPharm만 마친 뒤 약사 등록용 supervised internship/ITP는 별도입니다. Adelaide University는 이를 5년차 Master of Pharmacy로 이어 internship과 Intern Training Program을 통합하는 연계 경로도 안내합니다.')
intake('adelaide',[2],'2월 · 7월은 학점 인정 시 개별 심사'); fee('adelaide',54300,src='adelaide-fee-current',year=2026); req('adelaide','accepted','not_required','accepted','accepted','Biology, Chemistry 또는 Physics 중 1과목 또는 동등 수준',src='adelaide'); eng('adelaide',6.5,{'L':6,'R':6,'W':6,'S':6},src='adelaide-english-current',pte=64,pte_each=60,toefl={'overall':79,'L':12,'R':13,'W':21,'S':18})
_adelaide_reg=row(registration,'adelaide'); _adelaide_reg['supervised_practice_in_degree']=fact(True,'adelaide-pharmacy-current',note='BPharm 안에 약 12주 community/hospital 등 practical experience 포함'); _adelaide_reg['itp_in_degree']=fact(False,'adelaide-pharmacy-current',note='BPharm 단독 4년 과정에는 등록용 Intern Training Program이 통합되지 않음'); _adelaide_reg['post_graduation_internship']=fact(True,'adelaide-pharmacy-current',note='BPharm 후 등록 internship은 별도. 다만 5년 BPharm(Hons)+Master of Pharmacy 연계 경로는 Master year에 supervised internship/ITP를 통합할 수 있음')
setp('griffith',highlights=['Griffith College → 80CP','Gold Coast · Regional','Direct H1 최신 참고'],editorial='Direct 입학과 Griffith College Diploma 경로가 있습니다. Direct는 최신 공개 국제가이드(2026) H1 기준으로 CSAT 331 · IB 28 · SAT 1080 · A-level 7을 참고할 수 있으나 2027 확정 국제환산표는 아직 확인 중입니다. Griffith College의 2026/2027 Diploma of Health Sciences는 2027 Pharmacy 1614에 80CP가 공식 인정됩니다. 2027 국내 Guaranteed Admission Rank 76은 국제학생 Direct 점수로 사용하지 않습니다.',review_items=['2027 Direct 국제학력 환산표','2027 국제학생 본과 학비','Pharmacy 과목별 assumed knowledge/subject prerequisite 최신표']); intake('griffith',[3,7],'3월 · 7월 (2026 공개 기준)',src='griffith-2026-guide'); eng('griffith',7.0,None,src='griffith-2026-guide')
setp('latrobe',international_recruitment=fact(True,'latrobe-2027-course',status='latest_published',note='현재 Pharmacy course page는 국제학생이 연중 지원 가능하다고 안내합니다. 2027 국제학생 학비는 별도 확인 중입니다.'),highlights=['Bendigo Regional','4년 학사','30% Health Innovation'],editorial='Bendigo 캠퍼스 4년 약대입니다. 현재 과정 페이지는 2027년 3월 시작과 국제학생 연중 지원 가능을 안내하며, 졸업 후 1년 supervised internship이 별도입니다. 2027 국제학생 학비는 아직 확정 표시가 없어 계속 확인 중입니다.',review_items=['2027 국제학생 학비']); intake('latrobe',[3],'Semester 1 · 2027년 3월',src='latrobe-2027-course'); req('latrobe','not_required','not_required','not_required','not_required','별도 과학 선수과목 없음 · 영어 prerequisite만 적용',src='latrobe-health-guide'); eng('latrobe',6.5,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='latrobe-health-guide')
_latrobe_reg=row(registration,'latrobe'); _latrobe_reg['supervised_practice_in_degree']=fact(True,'latrobe-2027-course',note='과정 중 community/hospital 등 clinical placement 포함'); _latrobe_reg['itp_in_degree']=fact(False,'latrobe-2027-course',note='등록용 1년 supervised internship은 학위 밖에서 진행'); _latrobe_reg['post_graduation_internship']=fact(True,'latrobe-2027-course',note='졸업 후 1년 supervised internship + Pharmacy Board exams 필요')
setp('qut',highlights=['수학·화학 assumed knowledge','4년 학사','2027 학비 A$46,200'],editorial='QUT Pharmacy는 Chemistry와 Mathematical Methods/Specialist Mathematics를 필수 prerequisite가 아니라 assumed knowledge로 안내합니다. 미이수 학생은 지원 자체가 막히는 것으로 표시하지 않고 bridging study 안내와 함께 구분합니다.')
req('qut','assumed','assumed',grade='Chemistry + Mathematical Methods/Specialist Mathematics는 assumed knowledge',src='qut-fee-2027'); eng('qut',6.5,{'L':6,'R':6,'W':6,'S':6},pte=58,pte_each=50,toefl={'overall':79,'L':16,'R':16,'W':21,'S':18}); intake('qut',[2],'2월',src='qut-fee-2027'); fee('qut',46200,src='qut-fee-2027',year=2027,load='96 credit points 기준')
setp('rmit',highlights=['4년','RMIT Foundation 가능','2027 학비 A$49,920'],editorial='Bundoora 캠퍼스 4년 약대입니다. 한국 고교·수능 환산표가 명확하고 RMIT Foundation으로도 준비할 수 있습니다.')
req('rmit','required','required',grade='VCE Chemistry 25, Mathematics 25 또는 인정되는 동등 수준.'); fee('rmit',49920,year=2027); intake('rmit',[3],'Semester 1 · 2027년 3월 1일 수업 시작',src='rmit-2027-apply')
eng('rmit',7,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='rmit-english',pte=65,pte_each=58,toefl={'overall':94,'R':19,'L':20,'S':20,'W':24})
setp('newcastle',highlights=['4년 학사','Foundation 연계','영어 공식자료 불일치'],editorial='2027 Degree Guide와 2025-08-28 최신 Non-Standard English list는 Pharmacy를 IELTS 6.5/각 6.5로 안내하지만, 현재 degree page의 국제학생 섹션은 7.0/각 7.0을 표시합니다. 같은 현재 공식 시스템 안에서 값이 충돌하므로 사이트에서는 한 값을 확정하지 않고 지원 전 Newcastle Admissions 서면 확인 대상으로 유지합니다.',review_items=['Pharmacy 영어조건: 6.5/6.5 vs 국제학생 페이지 7.0/7.0 충돌','2027 CSAT·SAT·A-level·OSSD course-specific 값','APC 인증 갱신: 현재 목록 종료일 2026-12-31'])
eng('newcastle',6.5,{'L':6.5,'R':6.5,'W':6.5,'S':6.5},src='newcastle-nonstandard-english-2025',status='source_conflict');
for _k in ['ielts_overall','ielts_bands']:
 row(english,'newcastle')[_k]['note']='2025-08-28 최신 Non-Standard English list와 2027 Degree Guide는 6.5/각6.5이지만, 현재 degree page 국제학생 섹션은 7.0/각7.0입니다. 자동 충족 판정에 사용하지 않고 지원 전 서면 확인합니다.'
intake('newcastle',[2],'Semester 1 · 2027년 2월 22일',src='newcastle-2027-course'); req('newcastle','assumed','assumed',physics='assumed',grade='Assumed knowledge: Mathematics, English Advanced, Chemistry, Physics',src='newcastle-2026-ug'); fee('newcastle',51665,src='newcastle-fee-2027',year=2027,load='80 units 기준')
setp('canberra',highlights=['Canberra','학부 약학 과정','모집 확인 중'],editorial='APC 학부 약학 인증 목록과 실제 국제학생 모집은 서로 다른 확인 항목입니다. 2027 국제학생 course offer를 확인 중입니다.'); fee('canberra',42500,src='canberra-guide-2027',year=2026)
setp('unisq',highlights=['T1 only','Toowoomba','2027 개설표'],editorial='2027 국제학생 대면 수업은 Trimester 1에 표시됩니다. 개설 안내서는 9월 28일 확정 예정이므로 최종 일정 확인이 필요합니다.')
intake('unisq',[2],'Trimester 1 · 2027년 2월 15일',src='unisq-pharmacy-current'); req('unisq','accepted','assumed','accepted','accepted','수학 + Biology/Chemistry/Physics 중 1과목에서 Year 12 C 수준 assumed knowledge',src='unisq-pharmacy-current'); eng('unisq',7.0,{'L':7,'R':7,'W':6.5,'S':7},src='unisq-pharmacy-current')
setp('monash',highlights=['5년 PharmD','5년차 유급 인턴 통합','4년 BPharm(Hons) Exit'],editorial='P6007은 5년 Bachelor of Pharmacy (Honours) / Doctor of Pharmacy 통합과정입니다. 2~4학년에는 구조화된 실습이 있고 5학년에는 paid work-integrated learning과 Intern Training Program이 통합됩니다. 3년 144cp 후 Bachelor of Pharmacotherapeutics, 4년 192cp 후 BPharm(Hons), 5년에는 PharmD 또는 조건에 따라 BPharm(Hons)+Master of Pharmacy 대체 Exit가 있습니다. 2027 국내 Monash Guarantee ATAR는 80이지만 국제학력 Direct 점수로 자동 환산하지 않습니다. 관련 학사 졸업자는 Graduate Entry로 3학년 진입을 검토할 수 있습니다.')
req('monash','required','required',grade='VCE Methods/Specialist Maths 25 + Chemistry 25. IB Math AA SL4 또는 AA/AI HL3, Chemistry SL4 또는 HL3.'); intake('monash',[2],'2월'); fee('monash',63640,src='monash-fee-2027',year=2027,load='48 credit points 기준'); row(tuition,'monash')['increase_note']='Fees are subject to change annually.'; eng('monash',6.5,{'L':6,'R':6,'W':6,'S':6},src='monash-pps-2026',pte=58,pte_each=50)
for qt,val,scale,calc in [
 ('csat',350,'표준점수 상위 4과목 합','한국사·영어·직업탐구 제외'),
 ('korean_high_school',86,'Grade 10–12 academic subjects 평균 %','낙제 포함 학업과목 평균 · 비학업과목 제외'),
 ('alevel',12,'Monash GCE A Level 환산점수','Monash 공식 환산방식 적용'),
 ('ib',33,'45','IB Diploma 최종 총점'),
 ('sat',1290,'1600','SAT Evidence-Based Reading and Writing + Math')
]:
 q=next(x for x in qualifications if x['program_id']=='monash-bpharm-hons' and x['qualification']==qt)
 q['score']=fact(val,'monash-direct-2027-guide',year=2027,status='latest_published',note='2027 International Undergraduate Course Guide의 Pharmacy 5-year international entry table 기준. 가이드에는 기존 P6001 명칭이 남아 있어 P6007 live selector와 지원 전 재확인.')
 q['scale']=scale;q['calculation']=calc
setp('sydney',bachelor_award_year=fact(4,'sydney-structure'),four_year_exit=fact(True,'sydney-structure'),exit_degree=fact('Bachelor of Pharmacy (Honours)','sydney-structure'),highlights=['5년 통합','4년 BPharm(Hons) Exit','Mathematics prerequisite'],editorial='5년 Bachelor of Pharmacy (Honours) + Master of Pharmacy Practice 통합과정입니다. 현재 Course Resolutions는 1~4학년 192cp를 충족하면 Bachelor of Pharmacy (Honours)를 수여할 수 있고, 5학년 48cp가 Master of Pharmacy Practice임을 명시합니다. Mathematics는 공식 course prerequisite이며 Chemistry·Biology는 assumed knowledge, Physics는 recommended study입니다.',review_items=['USFP 수학 progression 조건'])
eng('sydney',6.5,{'L':6,'R':6,'W':6,'S':6},src='sydney',toefl={'overall':85,'L':17,'R':17,'W':19,'S':17}); intake('sydney',[2],'2월',src='sydney'); fee('sydney',63600,src='sydney',year=2027); req('sydney','assumed','required','assumed','recommended','Mathematics Advanced Band 4 또는 Mathematics Extension 1/2 Band E3 상당 prerequisite · Chemistry와 Biology는 assumed knowledge · Physics 권장',src='sydney-prereqs-current')
qual('sydney','csat',346,'표준점수 4개 합','국어 + 수학 + 사회/과학 탐구 상위 2개 과목의 표준점수 합. 등급이나 백분위 합계가 아닙니다.')
qual('sydney','sat',1300,'1600'); qual('sydney','ib',31,'45'); qual('sydney','alevel',14,'대학 환산점수','3과목/4과목 각각 14. A-level 성적을 대학 공식 환산식으로 계산해야 합니다.')
q=next(x for x in qualifications if x['program_id']=='sydney-bpharm-hons' and x['qualification']=='korean_high_school');q['score']=fact(False,'sydney',note='Korean Senior High School Diploma는 이 Direct 환산표에서 assessable qualification이 아님')
setp('unsw',name=fact('Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy','unsw-2027-course'),final_degree=fact('Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy','unsw-2027-course'),highlights=['2027 PharmD 전환','IELTS 7.0 · 각 6.0','5년 통합'],editorial='UNSW는 2027부터 Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy로 명칭을 변경합니다. 2027 공식 Guide의 국제 기준은 International ATAR 87 / IB 33이며, Pharmacy는 일반 Medicine & Health 영어기준보다 높은 IELTS 7.0(각 6.0)을 적용합니다. 새 PharmD 명칭의 APC/Board 반영과 2027 본과 학비는 별도 확인 중입니다.',review_items=['새 PharmD 명칭의 APC/Board 승인 반영','2027 국제학생 본과 학비']); prog('unsw')['accreditation']['note']='APC 2026-07-08 목록은 기존 Bachelor of Pharmaceutical Medicine / Master of Pharmacy 명칭을 Accredited with conditions(종료 2028-06-30)로 게재합니다. UNSW가 공지한 2027 Doctor of Pharmacy 새 명칭의 APC/Pharmacy Board 반영은 지원·등록 전 재확인합니다.'; fee('unsw',63000,src='unsw-fee-2026',year=2026,total=349000,load='first-year full-time fee'); intake('unsw',[2],'Term 1 · 2027',src='unsw-2027-course'); eng('unsw',7.0,{'L':6,'R':6,'W':6,'S':6},src='unsw-english-current',pte=65,pte_each=54,toefl={'overall':94,'L':23,'R':23,'W':25,'S':23}); req('unsw','assumed','assumed',grade='Assumed knowledge: Chemistry, Mathematics Advanced',src='unsw')
setp('uwa',highlights=['4년 Bachelor + PharmD','ATAR 85 · CBM WAM 65 assurance','2027 Global Excellence 10~20%'],editorial='고교 졸업 후 4년 동안 Bachelor of Human Sciences (Pharmaceutical Health) + Doctor of Pharmacy를 함께 이수하는 combined degree입니다. 공식 과정 페이지는 ATAR 85 입학과 combined degree 내 65% WAM assurance를 명시하며, 졸업 후에는 별도 internship과 Pharmacy Board 시험이 필요합니다.',review_items=['2027 국제학생 학비'])
req('uwa','assumed','assumed',grade='Chemistry 및 Mathematics Applications/Methods 수준을 권장하며, 미충족 시 UWA 규정에 따라 foundation/bridging units가 요구될 수 있습니다.'); eng('uwa',7,{'L':7,'R':7,'W':7,'S':7},src='uwa-combined-rules-current',pte=65,pte_each=65,toefl={'overall':94,'L':24,'R':24,'W':27,'S':23}); intake('uwa',[2],'Semester 1 · 2월')
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
for qt,val,scale in [('ib',28,'45'),('sat',1130,'1600'),('alevel',11,'UC A-level aggregate'),('ossd',74,'Grade 12 U/M average %')]:
 q=next(x for x in qualifications if x['program_id']=='canberra-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'canberra-intl-equiv'),scale=scale,calculation='UC Selection Rank 75 equivalent')
for qt,val,scale,src in [('ib',33,'45','unsw-2027-guide'),('alevel',15,'UNSW A-level aggregate','unsw-2027-course')]:
 q=next(x for x in qualifications if x['program_id']=='unsw-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,src),scale=scale,calculation='2027 PharmD 명칭 변경에도 입학기준은 동일하다는 UNSW 안내 기준')
q=next(x for x in qualifications if x['program_id']=='newcastle-bpharm-hons' and x['qualification']=='ib'); q.update(score=fact(28,'newcastle-prospectus-2027'),scale='45')
q=next(x for x in qualifications if x['program_id']=='uq-bpharm-hons' and x['qualification']=='ib'); q.update(score=fact(30.25,'uq',2026,status='latest_published',note='2027 program page의 최신 threshold이며 Semester 1, 2026 offer 기준'),scale='45')
for qt,val,scale in [('ib',27,'45'),('sat',1020,'1600')]:
 q=next(x for x in qualifications if x['program_id']=='jcu-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'jcu-intl-2025',2025,status='latest_published',note='2025 International Guide 참고값 · 2027 국제환산표 확인 전'),scale=scale)
# UTas 2027 Pharmacy minimum ATAR 70 mapped through the current official equivalency table linked by UTas admissions.
for qt,val,scale,calc in [('csat',305,'CSAT overall score','Upper Secondary Certificate + CSAT'),('ib',25,'45',''),('alevel',8,'UTas A-level points','2 or 3 H2 subjects'),('ossd',70,'best six Grade 12 subjects %','workplace/open 제외'),('sat',980,'1600','US High School completion also required')]:
 q=next(x for x in qualifications if x['program_id']=='utas-bpharm-hons' and x['qualification']==qt); q.update(score=fact(val,'utas-atar-equiv-current',2023,status='latest_published',note='현재 UTas country-entry 페이지가 연결하는 ATAR equivalency table의 ATAR 70 열 기준'),scale=scale,calculation=calc)
q=next(x for x in qualifications if x['program_id']=='utas-bpharm-hons' and x['qualification']=='korean_high_school'); q.update(score=fact(False,'utas-atar-equiv-current',2023,status='latest_published',note='한국 일반고는 Upper Secondary Certificate와 CSAT를 함께 요구하는 ATAR 환산표를 사용합니다.'),scale='고교 졸업장 단독 Direct 아님',calculation='')


# New UQ program remains a separate record with accreditation gate.
import copy
p=copy.deepcopy(prog('uq'));p.update(id='uq-pharmd',name=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),duration_years=fact(5,'uq-pharmd'),duration_label=fact('5년 통합','uq-pharmd'),bachelor_award_year=fact(None,'uq-pharmd'),four_year_exit=fact(None,'uq-pharmd'),exit_degree=fact(None,'uq-pharmd'),final_degree=fact('Bachelor of Pharmaceutics and Therapeutic Science / Doctor of Pharmacy','uq-pharmd'),international_recruitment=fact(True,'uq-pharmd'),highlights=['신설 5년 통합','700+시간 실습 + Intern training 통합','인증 승인 대기'],editorial='2027 신설 5년 PharmD입니다. 공식 2027 국제학생 페이지에서 2월·7월 입학과 A$60,952 학비를 공개하고 있으며, 2학년부터 700시간 이상의 supervised clinical placement와 4~5학년 compulsory intern training을 포함하도록 설계됐습니다. APC·Pharmacy Board 승인은 아직 진행 중입니다.',accreditation=fact('APC 인증·Pharmacy Board 승인 아직 미획득','uq-pharmd',status='pending_2027'),review_items=['APC accreditation 및 Board approval','신규 과정 qualification별 점수','학사 중간 Exit 여부'],decision_lens=dict(why=['2027 국제학생 모집 · 2월/7월 시작','5년 안에 700+시간 실습 + compulsory intern training 설계','2027 국제학생 학비 A$60,952'],watch=['APC accreditation 및 Pharmacy Board approval 아직 미획득','CSAT·IB·SAT 등 qualification-specific 점수는 새 과정 기준 별도 확인','학사 중간 Exit 여부 미확정']))
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
routes.append(dict(id='uq-pharmd-direct',program_id='uq-pharmd',type='direct',title='Direct · 신설 통합과정',availability=fact(True,'uq-pharmd',note='2027 국제학생 모집 페이지가 공개돼 있습니다. 단, 전문인증·Board 승인은 별도 pending입니다.'),credit=fact(0,'uq-pharmd'),entry_year=fact(1,'uq-pharmd'),duration=fact(5,'uq-pharmd'),intake=fact('2월 22일 / 7월 26일','uq-pharmd'),progression=fact(None,'uq-pharmd'),english=fact('IELTS 6.5 / 각 6.0 · PTE 64 / 각 60 · TOEFL 87','uq-pharmd'),qualification=fact('General English + Mathematics + Chemistry Queensland Year 12 C 동등 조건 · qualification별 점수는 별도 확인','uq-pharmd'),note='2027 국제학생 모집은 공개됐지만 APC accreditation 및 Pharmacy Board approval은 아직 미획득 상태입니다.'))

def route(i,id,type,title,src,credit=None,entry=None,duration=None,intake=None,progression=None,note='',verified=True):
 r=dict(id=id,program_id=i+'-bpharm-hons',type=type,title=title,availability=fact(True if verified else None,src),credit=fact(credit,src),entry_year=fact(entry,src),duration=fact(duration,src),intake=fact(intake,src),progression=fact(progression,src),english=fact(None,src),qualification=fact(None,src),note=note)
 routes.append(r);return r
mdr=next(x for x in routes if x['id']=='monash-bpharm-hons-direct')
mdr['qualification']=fact('수능 350 · 한국 고교 86% · A-Level 12 · IB 33 · AP 8 · SAT 1290','monash-direct-2027-guide',year=2027,status='latest_published',note='2027 국제학생 가이드 Pharmacy 5-year 기준. 인쇄 가이드의 과정명은 P6001로 남아 있어 P6007 live selector와 지원 전 재확인.')
mdr['english']=fact('IELTS 6.5 · 각 6.0','monash',year=2027,status='confirmed_2027')
mdr['progression']=fact('Maths + Chemistry 필수','monash',year=2027,status='confirmed_2027')
mdr['direct_scores']={
 'csat':fact(350,'monash-direct-2027-guide',year=2027,status='latest_published',note='표준점수 상위 4과목 합 · 한국사·영어·직업탐구 제외'),
 'korean_high_school':fact(86,'monash-direct-2027-guide',year=2027,status='latest_published',note='Grade 10–12 academic subjects 평균'),
 'alevel':fact(12,'monash-direct-2027-guide',year=2027,status='latest_published',note='Monash 환산점수'),
 'ib':fact(33,'monash-direct-2027-guide',year=2027,status='latest_published',note='IB Diploma /45'),
 'ap':fact(8,'monash-direct-2027-guide',year=2027,status='latest_published',note='가장 높은 AP 2개 합 · 각 AP 최소 3'),
 'sat':fact(1290,'monash-direct-2027-guide',year=2027,status='latest_published',note='1600점 만점')
}
mdr['note']='2027 국제학생 가이드의 Pharmacy 5-year 기준을 사용합니다. 가이드 과정명은 P6001로 남아 있어 신설 P6007의 live qualification selector와 지원 전 최종 재확인합니다.'

route('griffith','griffith-foundation','foundation','Griffith College · Foundation → Health Sciences Diploma → Pharmacy','griffith-foundation-pathways',0,2,'Foundation 8개월 + 1학년 Diploma','2027년 3월 1일 · 6월 28일 · 10월 25일','Foundation → Diploma of Health Sciences → Pharmacy 2학년','Foundation에서 Pharmacy 본과 1학년으로 바로 진학하는 경로로 표시하지 않습니다. Foundation 후 Diploma of Health Sciences를 거쳐 약대 2학년으로 연결합니다.')
routes[-1]['availability']=fact(True,'griffith-foundation-pathways',year=2027,status='confirmed_2027',note='Foundation Program can be packaged with any Diploma pathway; Pharmacy is excluded from the direct Foundation-to-Bachelor health list.')
routes[-1]['credit']=fact(0,'griffith-foundation-pathways',year=2027,status='confirmed_2027')
routes[-1]['entry_year']=fact(2,'griffith-college',year=2027,status='confirmed_2027',note='Foundation 후 Health Sciences Diploma를 거쳐 Pharmacy 2학년으로 연결되는 최종 목적지.')
routes[-1]['duration']=fact('Foundation 8개월 + 1학년 Diploma','griffith-foundation-current',year=2027,status='confirmed_2027')
routes[-1]['intake']=fact('2027년 3월 1일 · 6월 28일 · 10월 25일','griffith-college-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['intake_months']=fact([3,6,10],'griffith-college-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['progression']=fact('Foundation → Diploma of Health Sciences → Pharmacy 2학년','griffith-foundation-pathways',year=2027,status='confirmed_2027',note='현재 Foundation-to-Bachelor health pathways에서 Pharmacy는 direct 대상에서 제외되며 Foundation은 모든 Diploma pathway와 패키지 가능.')
routes[-1]['qualification']=fact('한국 고2 4개 학업과목 평균 Rank 7 · 또는 수능 260 / 상위 3개 Stanine 7 · 또는 검정고시 평균 70','griffith-college-entry',status='latest_published')
routes[-1]['english']=fact('IELTS 5.5 · 각 5.0','griffith-college-entry',status='latest_published')
routes[-1]['pathway_fee']=fact(None,'griffith-foundation-current',year=2027,status='pending_2027',note='2027 국제학생 Foundation 학비는 별도 검증 전 추정하지 않음.')
routes[-1]['destination_label']='1학년 Diploma → 약대 2학년'

_adelaide_direct=next(x for x in routes if x['id']=='adelaide-bpharm-hons-direct')
_adelaide_direct['qualification']=fact('수능 340 · IB 30 · A-Level 10 · SAT 1220 · OSSD 80% + Biology/Chemistry/Physics 중 1과목','adelaide-pharmacy-current',status='latest_published')
_adelaide_direct['intake']=fact('2월','adelaide-pharmacy-current',status='latest_published',note='7월은 학점 인정 국제학생만 case-by-case 심사')
_latrobe_direct=next(x for x in routes if x['id']=='latrobe-bpharm-hons-direct')
_latrobe_direct['qualification']=fact('2027 Guide 참고 ATAR 75.05 · 영어 prerequisite · 별도 과학 선수과목 없음 · 국제학력은 La Trobe 환산','latrobe-ug-guide-2027',year=2027,status='confirmed_2027',note='2027 Undergraduate Course Guide는 Pharmacy에 BEN ATAR 75.05를 표시합니다. 현재 live course page는 같은 75.05를 2026 lowest selection rank로 설명하므로, 보장 컷이 아닌 2027 지원 참고값으로만 사용합니다.')
_qut_direct=next(x for x in routes if x['id']=='qut-bpharm-hons-direct')
_qut_direct['qualification']=fact('Selection Rank 76 · Chemistry + Mathematical Methods/Specialist Mathematics는 assumed knowledge','qut',status='latest_published',note='Assumed knowledge는 prerequisite가 아니며 부족하면 bridging study 가능')

dr=next(x for x in routes if x['id']=='griffith-bpharm-hons-direct')
dr['intake']=fact('3월 · 7월 (2026 국제가이드 기준)','griffith-2026-guide')
dr['intake_months']=fact([3,7],'griffith-2026-guide')
dr['english']=fact('IELTS 7.0 overall · 각 영역 기준은 2027 과정자료에서 추가 확인','griffith-2026-guide')
dr['qualification']=fact('최신 공개 H1 참고: CSAT 331 · IB 28 · SAT 1080(+미국 고교졸업) · A-level 7','griffith-2026')
dr['note']='2026 국제가이드의 H1 환산표를 최신 공개 참고값으로 사용합니다. 2027 확정 환산표·과목별 assumed knowledge는 별도 확인 중입니다.'
route('adelaide','adelaide-eynesbury-foundation','foundation','Eynesbury · Foundation Studies → Pharmacy 1학년','eynesbury-foundation-2027',0,1,'8 또는 12개월','2027년 2월 22일 · 6월 21일 · 10월 11일','Foundation 395/500 + Pharmacy prerequisite 충족 → Bachelor of Pharmacy (Honours) 1학년','Foundation 후 Adelaide University Bachelor of Pharmacy (Honours) 1학년 진학 경로입니다.')
routes[-1]['availability']=fact(True,'eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['credit']=fact(0,'eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['entry_year']=fact(1,'eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['duration']=fact('8 또는 12개월','eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['intake']=fact('2027년 2월 22일 · 6월 21일 · 10월 11일','eynesbury-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['intake_months']=fact([2,6,10],'eynesbury-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['progression']=fact('Foundation 395/500 + Pharmacy prerequisite 충족 → Bachelor of Pharmacy (Honours) 1학년','eynesbury-foundation-progression-2026',year=2026,status='latest_published')
routes[-1]['qualification']=fact('Australian Year 11 또는 동등 학력','eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['english']=fact('IELTS 5.5 · 각 5.0','eynesbury-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['pathway_fee']=fact(36200,'eynesbury-foundation-2027',year=2027,status='confirmed_2027')

route('adelaide','adelaide-eynesbury-diploma','diploma','Eynesbury · Diploma of Health Science → Pharmacy 1학년','eynesbury-health-diploma-2027',4,1,'Stage 2 · 8 또는 12개월','2027년 2월 22일 · 6월 21일 · 10월 11일','Diploma GPA 5.0 → Pharmacy 1학년 · 4과목 인정 · 본과 4년 remaining','Griffith/Curtin과 달리 Pharmacy 2학년 직행이 아닙니다. Diploma 후 Pharmacy 1학년으로 진학하며 4개 과목만 인정됩니다.')
routes[-1]['availability']=fact(True,'eynesbury-health-diploma-2027',year=2027,status='confirmed_2027')
routes[-1]['credit']=fact(4,'eynesbury-health-diploma-2027',year=2027,status='confirmed_2027',note='Pharmacy에 4 Adelaide University courses granted; full Year 2 entry가 아님.')
routes[-1]['entry_year']=fact(1,'eynesbury-health-diploma-2027',year=2027,status='confirmed_2027',note='공식 pathway table은 4 courses granted와 4 years remaining을 명시.')
routes[-1]['duration']=fact('Stage 2 · 8 또는 12개월','eynesbury-health-diploma-2027',year=2027,status='confirmed_2027')
routes[-1]['intake']=fact('2027년 2월 22일 · 6월 21일 · 10월 11일','eynesbury-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['intake_months']=fact([2,6,10],'eynesbury-dates-2027',year=2027,status='confirmed_2027')
routes[-1]['progression']=fact('Diploma GPA 5.0 → Pharmacy 1학년 · 4과목 인정 · 본과 4년 remaining','eynesbury-health-diploma-2027',year=2027,status='confirmed_2027')
routes[-1]['qualification']=fact('Australian Year 12 또는 동등 학력 + Physics/Biology/Chemistry 중 1과목','eynesbury-entry-current',status='latest_published')
routes[-1]['english']=fact('IELTS 6.0 · 각 6.0','eynesbury-entry-current',status='latest_published')
routes[-1]['pathway_fee']=fact(41900,'eynesbury-health-diploma-2027',year=2027,status='confirmed_2027',note='2027 Stage 2 international fee')

route('griffith','griffith-college','diploma','Griffith College · Diploma of Health Sciences','griffith-college',80,2,'8개월(2 trimesters) 또는 12개월(3 trimesters)','2027 T1 3월 1일 · T2 6월 28일 · T3 10월 25일','Diploma 수료 + Pharmacy progression quota · 정원 초과 시 completed Diploma GPA 순 선발','80CP 인정 후 Bachelor of Pharmacy (Honours)로 연결됩니다. 2027 국제가이드는 Pharmacy에 progression quota가 있음을 명시합니다. T3 시작은 본과 intake와 progression gap을 함께 확인해야 합니다.')
routes[-1]['duration']=fact('8개월(2 trimesters) 또는 12개월(3 trimesters)','griffith-college-health')
routes[-1]['intake']=fact('2027 T1 3월 1일 · T2 6월 27일 · T3 10월 5일','griffith-college-2027-guide')
routes[-1]['intake_months']=fact([3,6,10],'griffith-college-2027-guide')
routes[-1]['progression']=fact('2026/2027 Diploma of Health Sciences 수료 + Pharmacy progression quota 충족 → 2027 Bachelor of Pharmacy (Honours) 1614에 80CP 인정 · 정원 초과 시 completed Diploma GPA 순 선발','griffith-college',note='공식 articulation은 80CP 인정 후 T1 대학 진학 시 본과 3년, T2 진학 시 약 3.5년이 남는다고 명시합니다.')
routes[-1]['note']='Griffith College Diploma of Health Sciences 2026/2027 → 2027 Pharmacy 1614에 80CP가 공식 인정됩니다. T1 진학 시 본과 240CP를 약 3년, T2 진학 시 약 3.5년에 이수합니다. 한국 내 UniCentre 경로는 TNS 사이트 정책상 별도 홍보하지 않습니다.'
routes[-1]['pathway_fee']=fact(None,'griffith-college-health',status='pending_2027',note='검증한 공식 2027 자료에서 Diploma of Health Sciences의 2027 tuition amount를 확인하지 못해 추정하지 않습니다.')
route('curtin','curtin-college','diploma','Curtin College · Pharmacy Diploma','curtin-college',175,2,'Stage 2: 12개월 · Stage 1 필요 시 8–12개월 추가','Stage 1: 2월/6월 · Stage 2: 2월','Stage 2 CWA 70% + PHAR1002 Pharmacy Practice 1(12월) 추가 이수','Diploma 완료 시 175 credits를 인정받고, 12월 PHAR1002를 추가 이수한 뒤 약대 2학년으로 진학합니다.')
routes[-1]['english']=fact('Stage 2 Pharmacy: IELTS 6.5 / 각 6.0 · PTE 58 / 각 50(2026년 8월 이전 시험 기준)','curtin-college-english')
routes[-1]['qualification']=fact('Stage 2 한국: 고3 Rank 6 또는 고교 졸업 + CSAT 280/600 · Mathematics + Chemistry prerequisite','curtin-college-entry')
routes[-1]['pathway_fee']=fact(44900,'curtin-college-fees-2027',year=2027,note='2027 Diploma of Health Sciences Stage 2 전체 학비. Stage 1이 필요한 학생은 2027 Stage 1 A$32,900이 추가됩니다.')
route('uq','uq-standard-2027-entry','foundation','UQ College · Standard Foundation','uq-standard-foundation-2027',0,1,'약 10개월','2026-09-07 시작 → 2027-07-09 완료 · 본과 2027 Semester 2','BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','2027년 7월 UQ Pharmacy 입학을 목표로 할 경우 Standard Foundation은 2026년 9월 시작 일정이 맞습니다. 2027년 2월 Standard 시작은 UQ 2028 Semester 1로 연결됩니다.')
routes[-1]['intake_months']=fact([9],'uq-standard-foundation-2027',year=2026,status='latest_published',note='2027 BPharm Semester 2 연결용 Foundation 시작월')
routes[-1]['progression']=fact('BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','uq-foundation')
routes[-1]['qualification']=fact('한국: 수능 260 · 검정고시 상위 4과목 평균 65% · 고2 상위 4과목 GPA 3(미)','uq-foundation-entry-current',year=2026,status='latest_published')
routes[-1]['english']=fact('IELTS 5.5 · 각 5.0','uq-standard-foundation-2027',year=2027,status='confirmed_2027')
routes[-1]['pathway_fee']=fact(36280,'uq-standard-foundation-2027',year=2027,note='2026/2027 offer 기준 tuition fee. Enrolment·Student Services·교재비 포함 총액은 A$39,172.')
route('uq','uq-accelerated','foundation','UQ College · Accelerated Foundation','uq-accelerated',0,1,'약 4개월','2027-02-15 시작 → 07-09 완료 · 본과 07-26','BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','2월 Foundation → 7월 BPharm 일정입니다. GPA·영어·필수과목을 충족해야 합니다.')
routes[-1]['progression']=fact('BPharm 진급 GPA 5.0 · Academic English 5 · 선수과목 충족','uq-foundation')
routes[-1]['qualification']=fact('한국: 수능 270 · 검정고시 상위 4과목 평균 70% · 고3 상위 4과목 GPA 4(우)','uq-foundation-entry-current',year=2026,status='latest_published')
routes[-1]['english']=fact('IELTS 6.0 · Writing 6.0 · Speaking/Listening/Reading 5.5 이상','uq-accelerated')
routes[-1]['pathway_fee']=fact(24940,'uq-accelerated',year=2027,note='2026/2027 offer 기준 tuition fee. Enrolment·Student Services·교재비 포함 총액은 A$27,490.')
route('uwa','uwa-foundation-8','foundation','UWA College · Foundation 8개월','uwa-foundation-8-current',0,1,'8개월','UWA College 일정','UWA College Foundation 70 + Pharmacy 입학·영어조건','8개월 Foundation은 IELTS 6.0/각5.5가 필요합니다. 한국 학생의 최근 공개 country table(2025 brochure)은 검정고시 60%, CSAT 260, 고2 70%, 고3 60%를 안내합니다. 이 학력표는 2025 자료이므로 최신 공개 참고값으로 표시합니다.')
routes[-1]['english']=fact('IELTS 6.0 / 각 5.5','uwa-foundation-8-current')
routes[-1]['qualification']=fact('한국 최신 공개 참고(2025): 검정고시 60% · CSAT 260 · 고2 70% · 고3 60%','uwa-college-brochure-2025',year=2025,status='latest_published')
routes[-1]['progression']=fact('UWA College Foundation 70 + Pharmacy 입학·영어조건','uwa')
route('uwa','uwa-foundation-12','foundation','UWA College · Foundation 12개월','uwa-foundation-12-current',0,1,'12개월','UWA College 일정','UWA College Foundation 70 + Pharmacy 입학·영어조건','12개월 Foundation은 IELTS 5.5/각5.0가 필요합니다. 한국 학생의 최근 공개 country table(2025 brochure)은 검정고시 60%, CSAT 230, 고2 65%, 고3 60%를 안내합니다. 이 학력표는 2025 자료이므로 최신 공개 참고값으로 표시합니다.')
routes[-1]['english']=fact('IELTS 5.5 / 각 5.0','uwa-foundation-12-current')
routes[-1]['qualification']=fact('한국 최신 공개 참고(2025): 검정고시 60% · CSAT 230 · 고2 65% · 고3 60%','uwa-college-brochure-2025',year=2025,status='latest_published')
routes[-1]['progression']=fact('UWA College Foundation 70 + Pharmacy 입학·영어조건','uwa')
_uwa_direct=next(x for x in routes if x['id']=='uwa-bpharm-hons-direct')
_uwa_direct['progression']=fact('Combined degree 내 Doctor of Pharmacy assurance: WAM 65%','uwa',note='UWA course page states an 85 ATAR entry and 65% WAM assurance in this combined degree.')
_uwa_direct['qualification']=fact('ATAR 85 equivalent · CSAT 329 · IB 30 · A-level 10 · SAT 1220 · UWAC Foundation 70','uwa')
_uwa_direct['english']=fact('IELTS 7.0 · 각 영역 7.0','uwa')
_uwa_direct['note']='고교 졸업 후 4년 combined degree로 시작합니다. Doctor of Pharmacy progression assurance는 WAM 65% 조건이며 졸업 후 internship과 Pharmacy Board 시험이 별도입니다.'
route('qut','qut-foundation-standard','foundation','QUT College · Standard Foundation','qut-foundation-standard-2027',0,1,'12개월','2월 · 7월','Foundation 수료 + Pharmacy package offer의 faculty progression 조건 충족','국제학생 전용 12개월 Foundation입니다. 수료 후 승인된 QUT Bachelor 1학년으로 연결되며 Pharmacy 패키지의 개별 progression 조건을 충족해야 합니다.')
routes[-1]['intake_months']=fact([2,7],'qut-foundation-standard-2027')
routes[-1]['english']=fact('IELTS 5.5 / 각 5.0 · PTE 46 / 각 38 · TOEFL 56 (L10/R10/W15/S14)','qut-foundation-standard-2027')
routes[-1]['qualification']=fact('Year 11 또는 Year 12 동등 학력 · 한국 학력은 QUT country-specific 심사','qut-foundation-standard-2027',note='QUT College Merit 장학의 한국 고2 5등급/80% 기준은 장학 기준이므로 일반 입학점수로 사용하지 않습니다.')
routes[-1]['pathway_fee']=fact(25536,'qut-foundation-standard-2027',year=2027,note='2027 Standard Foundation 전체 96 credit points 학비')
route('qut','qut-foundation-intensive','foundation','QUT College · Intensive Program','qut-foundation-intensive-2027',0,1,'6개월','2월 · 7월','Intensive 수료 + Pharmacy package offer의 faculty progression 조건 충족','고교 Year 12 동등 학력을 마치고 목표 QUT 학사 입학조건에 거의 도달한 학생을 위한 6개월 가속 Foundation입니다.')
routes[-1]['intake_months']=fact([2,7],'qut-foundation-intensive-2027')
routes[-1]['english']=fact('IELTS 6.0 / 각 5.0 · PTE 50 / 각 38 · TOEFL 71 (L10/R10/W15/S14)','qut-foundation-intensive-2027')
routes[-1]['qualification']=fact('Year 12 동등 학력 · 목표 Bachelor 입학조건에 거의 도달한 학생용','qut-foundation-intensive-2027')
routes[-1]['pathway_fee']=fact(12768,'qut-foundation-intensive-2027',year=2027,note='2027 Intensive Program 전체 48 credit points 학비')
route('sydney','sydney-usfp','foundation','USFP · Standard Program','sydney-usfp-fees-2027',0,1,'12개월','1월 · 7월','Pharmacy: USFP GPA 7.3 / English C + STEM 1 Mathematics prerequisite','2027 Standard tuition은 A$49,800입니다. 2027년에 Foundation을 시작하는 학생의 실제 University Pharmacy 입학연도는 Foundation 종료시점에 따라 2028이 될 수 있으므로 시작시기와 본과 2월 intake를 함께 맞춰야 합니다.')
routes[-1]['intake_months']=fact([1,7],'sydney-usfp-dates-current',status='latest_published')
routes[-1]['progression']=fact('Pharmacy: USFP GPA 7.3 / English C + STEM 1 Mathematics prerequisite','sydney')
routes[-1]['pathway_fee']=fact(49800,'sydney-usfp-fees-2027',year=2027,note='2027 Standard Program 12개월 tuition fee')
route('sydney','sydney-usfp-intensive','foundation','USFP · Intensive Program','sydney-usfp-fees-2027',0,1,'9개월','4월 · 10월','Pharmacy: USFP GPA 7.3 / English C + STEM 1 Mathematics prerequisite','2027 Intensive tuition은 A$47,690입니다. Foundation 수료 후 Pharmacy 본과는 2월 intake와 일정이 맞아야 하므로 시작월별 실제 진학연도를 확인해야 합니다.')
routes[-1]['intake_months']=fact([4,10],'sydney-usfp-dates-current',status='latest_published')
routes[-1]['progression']=fact('Pharmacy: USFP GPA 7.3 / English C + STEM 1 Mathematics prerequisite','sydney')
routes[-1]['pathway_fee']=fact(47690,'sydney-usfp-fees-2027',year=2027,note='2027 Intensive Program 9개월 tuition fee')
route('unsw','unsw-foundation-standard','foundation','UNSW College · Standard Foundation','unsw-college-standard-2027',0,1,'9개월','4월 · 10월','현재 Pharmacy progression reference: Foundation GPA 7.6 · Academic English B · Life Science/Physical Science · UNSW Term 1','UNSW College의 현재 progression 표는 기존 3895 Bachelor of Pharmaceutical Medicine/Master of Pharmacy 명칭을 사용합니다. UNSW는 2027 신입생을 새 Doctor of Pharmacy 명칭으로 전환한다고 안내하므로, GPA 7.6 / English B는 최신 pathway 참고값으로 표시하되 새 명칭 전용 2027 표가 갱신되기 전까지 자동 확정판정에는 사용하지 않습니다.')
routes[-1]['intake']=fact('4월 · 10월','unsw-college-standard-2027')
routes[-1]['intake_months']=fact([4,10],'unsw-college-standard-2027')
routes[-1]['progression']=fact('현재 3895 progression: GPA 7.6 · Academic English B · Life Science/Physical Science · Term 1','unsw-college-student-guide',status='latest_published',note='College 표에는 아직 기존 Master of Pharmacy 명칭이 남아 있습니다. 2027 Doctor of Pharmacy 명칭 전용 progression table 발표 후 재확인합니다.')
routes[-1]['pathway_fee']=fact(43650,'unsw-college-standard-2027',year=2027,note='2027 Standard Foundation tuition only · 기타 compulsory fee 별도')
route('monash','monash-foundation','foundation','Monash University Foundation Year','monash-foundation-p6007-current',0,1,'Standard 약 12개월','2월 · 8월','P6007: Foundation 75% · English 65% · Maths 50% + Chemistry 50%','약 12개월 Standard 기준. 2027 시작일은 2월·8월이며, P6007 진급은 현재 Monash College destination degree 기준을 사용합니다.')
routes[-1]['availability']=fact(True,'monash-foundation-p6007-current')
routes[-1]['duration']=fact('Standard 약 12개월','monash-foundation-dates-2027')
routes[-1]['intake']=fact('2월 · 8월','monash-foundation-dates-2027')
routes[-1]['intake_months']=fact([2,8],'monash-foundation-dates-2027')
routes[-1]['progression']=fact('P6007: Foundation 75% · English 65% · Maths 50% · Chemistry 50%','monash-foundation-p6007-current',year=2026,status='latest_published',note='현재 Monash College destination degree 표가 P6007을 직접 명시')
routes[-1]['english']=fact('IELTS 5.5 · 각 5.0','monash-foundation-english-current',status='latest_published',note='Foundation Year Standard 입학 영어')
routes[-1]['qualification']=fact('한국 고교 60% 또는 수능 260','monash-foundation-korea-current',status='latest_published',note='Foundation Year Standard 입학 기준')
route('newcastle','newcastle-foundation','foundation','Newcastle CIE · Foundation Studies','newcastle-foundation',0,1,'11개월 · Pharmacy 목적 2월 시작','2월 · Pharmacy는 본과 중간입학 없음','전체 평균 65%+ · Academic English A&B 평균 75%+','Foundation을 마치면 Bachelor of Pharmacy (Honours) 1학년으로 진학합니다. 2027 Foundation Studies 학비는 A$31,400입니다.')
routes[-1]['english']=fact('Foundation 입학: IELTS 5.5 / 각 5.0 · 본과 진급: Academic English A&B 평균 75%+','newcastle-foundation-entry')
routes[-1]['qualification']=fact('한국: 고2 수료(pass grades)부터 Foundation Studies 입학 가능','newcastle-foundation-entry')
routes[-1]['pathway_fee']=fact(31400,'newcastle-foundation-fee-2027',year=2027,note='2027 Foundation Studies program fee · 10 courses')
route('monash','monash-ge','graduate','Monash · Graduate Entry','monash-grad-entry-current',None,3,'Summer intensive 후 3학년 진입',None,'학사 평균 70%+ · Chemistry · Higher-level Maths · 대학 수준 Human Physiology','최소요건 충족자 중 경쟁선발 · Summer intensive 이수 후 약대 3학년 진입')
routes[-1]['qualification']=fact('관련 학사 · 최근 10년 이내','monash-grad-entry-current',status='latest_published',note='Biomedicine, Pharmaceutical Sciences, Science 등 관련 science-based degree')
routes[-1]['progression']=fact('학사 평균 70%+ · Chemistry · Higher-level Maths · 대학 수준 Human Physiology','monash-grad-entry-current',status='latest_published',note='Human Physiology는 최소 1과목을 tertiary level에서 이수')
routes[-1]['english']=fact('영어수업 학사 또는 IELTS 6.5 · 각 6.0','monash-grad-entry-current',status='latest_published',note='English Level A')
route('rmit','rmit-foundation','foundation','RMIT Foundation Studies','rmit-foundation-equiv',0,1,'1년','2월 · 7월','Foundation 65% + Pharmacy Chemistry·Mathematics prerequisite 동등과목 충족','Foundation 후 Pharmacy 1학년으로 지원합니다. 2027 Foundation Studies 총학비는 A$34,250이며 Pharmacy의 Chemistry·Mathematics prerequisite를 Foundation에서 충족해야 합니다.')
routes[-1]['duration']=fact('1년','rmit-foundation-2027')
routes[-1]['intake']=fact('Semester 1 · 2월 1일 / Semester 2 · 7월','rmit-foundation-2027')
routes[-1]['intake_months']=fact([2,7],'rmit-foundation-2027')
routes[-1]['english']=fact('IELTS 5.5 / 각 5.0','rmit-foundation-current')
routes[-1]['qualification']=fact('Australian Year 11 동등 학력 + 평균 50% 또는 pass average · 만 16세 이상','rmit-foundation-current')
routes[-1]['pathway_fee']=fact(34250,'rmit-foundation-2027',year=2027,note='2027 Foundation Studies total tuition fee')
route('rmit','rmit-associate','other','RMIT · Associate Degree pathway','rmit-2027-apply',96,2,'총 5년 · Associate Degree 2년 + Bachelor of Pharmacy 3년','Associate Semester 1 · 2027년 2월 8일 수업 시작','AD012P24 Biomedicine option 수료 + IELTS 7.0 / 각 6.5 → Pharmacy guaranteed entry','2027 BH102 packaged pathway가 공식 확인됩니다. AD012P24 Biomedicine option 완료 시 Bachelor of Pharmacy에 96 credit points(2 semesters) 인정되어 Bachelor 단계 3년이 남습니다.',True)
routes[-1]['credit']=fact(96,'rmit-associate-current',note='two semesters of credit · 96 credit points')
routes[-1]['entry_year']=fact(2,'rmit-associate-current',note='96 credit points = Bachelor full-time 1년 상당')
routes[-1]['duration']=fact('총 5년 · Associate Degree 2년 + Bachelor of Pharmacy 3년','rmit-2027-apply')
routes[-1]['intake']=fact('Associate Semester 1 · 2027년 2월 8일 수업 시작','rmit-associate-2027')
routes[-1]['intake_months']=fact([2],'rmit-associate-2027')
routes[-1]['progression']=fact('AD012P24 Biomedicine option 수료 + IELTS 7.0 / 각 6.5 → Pharmacy guaranteed entry','rmit-associate-current')
routes[-1]['english']=fact('Pharmacy 진급: IELTS 7.0 / 각 6.5 또는 동등점수','rmit-associate-current')
routes[-1]['pathway_fee']=fact(38400,'rmit-associate-2027',year=2027,note='2027 Associate Degree 국제학생 연간 학비 · 2년 총액 아님')
route('latrobe','latrobe-foundation','foundation','La Trobe College · Foundation Studies · Health, Life Sciences and Engineering','latrobe-foundation-current',0,1,'8개월 · 2 trimesters','2월 · 6월','Foundation 최소 WAM 60% + 해당 Bachelor 최소조건 · Pharmacy는 Advanced Mathematics 2 + Chemistry 2 이수 필요 · quota/추가조건 가능','국제학생 전용 Foundation이며 Pharmacy (Honours) Bendigo 1학년으로 연결됩니다. 현재 공개 페이지의 학비는 2026 A$29,780이므로 2027 학비로 표시하지 않습니다.')
routes[-1]['duration']=fact('8개월 · 2 trimesters','latrobe-foundation-current')
routes[-1]['intake']=fact('2월 · 6월','latrobe-foundation-current')
routes[-1]['intake_months']=fact([2,6],'latrobe-foundation-current')
routes[-1]['progression']=fact('Foundation 최소 WAM 60% + 해당 Bachelor 최소조건 · Pharmacy는 Advanced Mathematics 2 + Chemistry 2 이수 필요 · quota/추가조건 가능','latrobe-foundation-transfer',note='현재 transfer page의 공통 최소 WAM 60%와 Pharmacy study-plan 과목요건을 결합해 표시합니다. Pharmacy-specific 최종 WAM/정원은 지원 전 재확인합니다.')
routes[-1]['english']=fact('Foundation 입학: IELTS 5.5 / 각 5.0 · PTE 42 / 각 36 · TOEFL iBT 55 / Writing 16','latrobe-foundation-english-2026')
routes[-1]['qualification']=fact('Year 11 동등학력 · 한국 학력은 La Trobe College 심사','latrobe-foundation-current',status='latest_published')
routes[-1]['pathway_fee']=fact(29780,'latrobe-foundation-fee-2026',year=2026,note='2026 Foundation Studies international program fee · 2027 금액 아님')
route('utas','utas-foundation-standard','foundation','UTas IPC · Foundation Studies Standard','utas-ipc-foundation',0,1,'8–9개월 · 2 semesters','2027년 2월 22일 · 6월 21일 · 10월 11일','Pharmacy: Physical Science stream · FCWAM 60% · Chemistry + Statistics · Foundation English 평균 65%, 각 60% 이상','한국 고2(Senior Year 2) 60%부터 입학 가능. Foundation 종료 후 다음 가능한 Pharmacy Health Study Period 1 입학시기에 맞춰 진학합니다.')
routes[-1]['duration']=fact('8–9개월 · 2 semesters','utas-ipc-fees-2027')
routes[-1]['intake']=fact('2027년 2월 22일 · 6월 21일 · 10월 11일','utas-ipc-fees-2027')
routes[-1]['intake_months']=fact([2,6,10],'utas-ipc-fees-2027')
routes[-1]['progression']=fact('Pharmacy: Physical Science stream · FCWAM 60% · Chemistry + Statistics · Foundation English 평균 65%, 각 60% 이상','utas-ipc-foundation',note='IPC progression table의 Pharmacy 기준. 현재 학위명 표기는 구 명칭이 남아 있으나 Pharmacy pathway criteria로 사용됩니다.')
routes[-1]['english']=fact('입학 IELTS 5.5 / 각 5.0','utas-ipc-entry')
routes[-1]['qualification']=fact('한국: Senior Year 2(고2) 60% · 60%=pass 기준','utas-ipc-entry')
routes[-1]['pathway_fee']=fact(21975,'utas-ipc-fees-2027',year=2027,note='2027 Foundation Studies Standard tuition fee')
route('utas','utas-foundation-fast','foundation','UTas IPC · University Pathway Program Fast-track','utas-ipc-foundation',0,1,'4–5개월 · 1 semester','2027년 2월 22일 · 6월 21일 · 10월 11일','Pharmacy: Physical Science stream · FCWAM 60% · Chemistry + Statistics · Foundation English 평균 65%, 각 60% 이상','한국 고2(Senior Year 2) 65%부터 입학 가능. General Mathematics 또는 인정 동등과목이 필요하며 빠른 일정이라 본과 시작시기와 조합을 확인해야 합니다.')
routes[-1]['duration']=fact('4–5개월 · 1 semester','utas-ipc-fees-2027')
routes[-1]['intake']=fact('2027년 2월 22일 · 6월 21일 · 10월 11일','utas-ipc-fees-2027')
routes[-1]['intake_months']=fact([2,6,10],'utas-ipc-fees-2027')
routes[-1]['progression']=fact('Pharmacy: Physical Science stream · FCWAM 60% · Chemistry + Statistics · Foundation English 평균 65%, 각 60% 이상','utas-ipc-foundation',note='IPC progression table의 Pharmacy 기준. 현재 학위명 표기는 구 명칭이 남아 있으나 Pharmacy pathway criteria로 사용됩니다.')
routes[-1]['english']=fact('입학 IELTS 6.0 / 각 5.0','utas-ipc-entry')
routes[-1]['qualification']=fact('한국: Senior Year 2(고2) 65% · General Mathematics 또는 country-specific equivalent 필요','utas-ipc-entry')
routes[-1]['pathway_fee']=fact(25450,'utas-ipc-fees-2027',year=2027,note='2027 University Pathway Program Fast Track tuition fee')

def scholarship(i,id,name,src,pct=None,kind='pending',automatic=None,competitive=None,eligible=None,duration=None,threshold=None,renewal=None,number=None,exclude=None,note='',pharmacy=None,amount_status=None,pharmacy_src=None,award_type=None,scope=None):
 row=dict(id=id,university_id=i,name=name,amount=fact(pct,src,status=amount_status),award_type=award_type or ('percentage' if pct is not None else None),assessment=kind,
  automatic_assessment=fact(automatic,src),separate_application=fact(not automatic,src) if automatic is not None else fact(None,src),competitive=fact(competitive,src),country_eligibility=fact(eligible,src),duration=fact(duration,src),academic_threshold=fact(threshold,src),renewal_condition=fact(renewal,src),number_available=fact(number,src),course_exclusion=fact(exclude,src),pharmacy_eligible=fact(pharmacy,pharmacy_src or src),note=note)
 if scope: row['scope']=scope
 scholarships.append(row)
scholarship('griffith','griffith-merit','International Academic Merit','griffith-scholarship',20,'automatic',True,False,True,'학위 잔여 기간 · 인정학점 제외','GPA 4.5/7 또는 동등 성적','매 학기 전 과목 통과·풀타임 유지',exclude='Diploma 자체 및 제휴기관 제공과정 등 제외',note='한국 국적 대상. Pathway 패키지는 최종 성적 제출 후 심사합니다.',pharmacy=True)
scholarship('sydney','sydney-award','Sydney International Student Award','sydney-scholarship',20,'application',False,False,True,'과정 기간','입학조건 충족 + personal statement','미납 없음·허가 없는 파트타임 전환 금지·정해진 기간 이수',exclude='MBA/EMBA·교환·원격·일부 법학 복수과정 등',note='2027 한국 국적 포함. Personal statement는 3개 항목 각 최대 200단어입니다.',pharmacy=True)
scholarship('monash','monash-merit','Pharmacy and Pharmaceutical Science International Merit','monash-scholarship',[25,50],'competitive',True,True,True,'최소 졸업학점 이수까지','각 대상 과정군 최상위·차상위','매 학기 WAM 70 유지',8,'현재 공식 대상과정: P2001/P3002, P3001/P6001, P6005, P6006 · P6007 미표기','25%/50%·연 8명 구조는 현재 공식 장학 페이지에 유지되지만, 대상 과정코드에 P6007이 아직 없으므로 2027 P6007 적용은 확인 중으로 표시.',pharmacy=None,award_type='percentage',scope='p6007_not_confirmed')
scholarship('monash','monash-international-merit','Monash International Merit Scholarship','monash-international-merit-scholarship',15000,'competitive',True,True,True,'매년 · 최소 졸업학점 이수까지','학업성취도 기준 경쟁선발','매 학기 WAM 70 이상',20,'MD, Monash Pathway 등 공식 제외과정. P6007 Pharmacy는 제외목록에 없음','일반 국제학생 학부 오퍼 소지자는 별도 장학신청 없이 자동심사. 연 20명 경쟁선발.',pharmacy=True,award_type='aud_per_year')
scholarship('monash','monash-international-leadership','Monash International Leadership Scholarship','monash-international-leadership-scholarship',100,'competitive',True,True,True,'최소 졸업학점 이수까지','학업성취도 기준 최상위권 경쟁선발','매 학기 WAM 70 + Campus Ambassador Program 참여',4,'MD, Monash Pathway 등 공식 제외과정. P6007 Pharmacy는 제외목록에 없음','학비 100% 지원. 연 4명 경쟁선발.',pharmacy=True,award_type='percentage')
scholarship('jcu','jcu-excellence','International Excellence Scholarship','jcu-scholarship',25,'automatic',True,False,True,'학위 전체 기간','학부: ATAR 65 또는 동등 성적','매 학기 강한 GPA 유지',exclude='Medicine·Dentistry·Diploma·일부 비학위 과정',note='Bachelor of Pharmacy (Honours)는 공식 제외목록에 없습니다.',pharmacy=True)
scholarship('utas','utas-tims','Tasmanian International Merit Scholarship','utas-scholarship-2027',30,'automatic',True,False,True,'학위 전체 기간 · 최대 5년','최종 학력 성적표 기준 merit 심사','정상 등록·학업진행 유지',note='2027 약대는 제외과정 목록에 없습니다. 다른 UTas 장학과 중복 수혜는 불가하며 더 높은 장학이 적용됩니다.',pharmacy=True)
scholarship('curtin','curtin-global-merit','Curtin Global Merit Scholarship','curtin-scholarship-2027',20,'automatic',True,False,True,'학부 최대 4년','최근 학업성적 Distinction 수준','Offer·등록 조건 유지',exclude='공식 제외과정에 Pharmacy 없음',note='2027/2028 WA 캠퍼스 국제학생 대상.',pharmacy=True)
scholarship('uq','uq-excellence','UQ International Excellence Scholarship','uq-scholarship-2027',25,'competitive',True,True,True,'학위 전체 기간','Offer holder 중 대학이 정한 경쟁점수','UQ 장학 약관 충족',note='별도 신청 없이 자동심사합니다. 다른 UQ tuition reduction과 중복 적용하지 않습니다.',pharmacy=True)
scholarship('adelaide','adelaide-merit','Adelaide Merit Scholarship','adelaide-scholarship',15,'automatic',True,False,True,'표준 학위기간','IB 28 · A-level 9 · 기타 국제고교 ATAR 85 상당','Program Term GPA 4.5/7 유지',exclude='공식 제외과정에 Pharmacy 없음',note='Bachelor of Pharmacy (Honours)는 공식 제외과정 목록에 없습니다.',pharmacy=True)
scholarship('latrobe','latrobe-high-achiever','La Trobe High Achiever Scholarship','latrobe-scholarship-2027',[20,25],'automatic',True,False,True,'학위 전체 기간','WAM/ATAR 상당 60–74.9: 20% · 75+: 25%','Full-time 등록·정상 학업진행',note='Bendigo Bachelor of Pharmacy (Honours)는 국제장학 eligible-course 목록에 포함됩니다.',pharmacy=True,pharmacy_src='latrobe-scholarship-courses')
scholarship('latrobe','latrobe-health-innovation-30','La Trobe Health Innovation Scholarship · 30%','latrobe-health-innovation-2027',30,'automatic',True,False,True,None,'Minimum WAM 75+','장학 약관 및 Offer 조건 충족',note='30% Health Innovation은 현재 국제장학 안내에서 50%/100%와 달리 별도 신청이 필요한 장학으로 표시되지 않습니다. 2026/2027 intake 약관상 수량이 제한되고 offer acceptance 순으로 확보되므로 조기 수락 조건을 확인해야 합니다.',pharmacy=True,pharmacy_src='latrobe-health-innovation-2027')
scholarship('latrobe','latrobe-vc-2027','La Trobe Vice Chancellor Scholarship · 50%/100%','latrobe-vc-2027',[50,100],'competitive',False,True,True,'학위 전체 기간','Minimum WAM 80 + 영어 + written statement','Full-time 등록·정상 학업진행 + 장학생 활동 참여',exclude='Direct entry eligible course만',note='2027 국제학생 대상 별도 지원 경쟁장학입니다. La Trobe Pharmacy 과정 페이지가 이 장학을 해당 과정의 이용 가능 장학으로 표시합니다.',pharmacy=True,pharmacy_src='latrobe-2027-course')
scholarship('qut','qut-merit','QUT International Merit Scholarship','qut-scholarship-2027',25,'automatic',True,False,True,'학위 전체 기간','입학 성적 기준 충족','QUT 최소 GPA 조건 유지',note='2027 국제학생 가이드 기준. 전 학부/faculty에 제공되는 International Merit Scholarship입니다.',pharmacy=True)
scholarship('newcastle','newcastle-excellence','International Excellence Scholarship 2027','newcastle-scholarship',20,'course_excluded',True,False,True,'해당 없음',None,None,500,'Bachelor of Pharmacy (Honours)','20% 장학 자체는 2027 국제학생 장학이지만 Bachelor of Pharmacy (Honours)는 공식 제외과정입니다.',pharmacy=False,pharmacy_src='newcastle-scholarship-2027-terms')
scholarship('canberra','canberra-international-2027','UC International Scholarships 2027','canberra-guide-2027',[10,20,30],'automatic',True,True,True,'표준 학위기간','Merit 10%: GPA 5/7 · 상위 장학은 더 높은 성적/전략 기준','Course GPA 5.0 이상 유지',exclude='HDR·1년 standalone Honours·non-award·offshore·일부 보건계열 제외. Bachelor of Pharmacy는 제외목록에 없음',note='별도 장학 신청 없이 입학 지원 시 자동 심사합니다. 10/20/30%는 academic merit와 strategic recruitment priorities에 따라 결정되며 학업 중 GPA 5.0 이상을 유지해야 합니다.',pharmacy=True,pharmacy_src='canberra-scholarship-conditions-current')
scholarship('unisq','unisq-support','International Student Support Scholarship 2027','unisq-scholarship-2027',10,'guaranteed',True,False,True,'Offer에 기재된 학위 전체 기간','2027 최초 입학 + Offer의 학업·영어조건 충족','장학 약관 수락·해당 학위 등록 유지',exclude='non-award 및 offshore partner 제공과정 제외',note='2027 tuition 10% 장학입니다. 최초 입학 지원 시 평가되며 Offer 수락 때 장학 약관도 함께 수락해야 합니다. 다른 UniSQ-funded tuition scholarship과 중복되지 않으며 Pharmacy는 제외목록에 없습니다.',pharmacy=True,pharmacy_src='unisq-scholarship-terms-2027')
scholarship('uwa','uwa-global-excellence','UWA Global Excellence Scholarship','uwa-scholarship-current',[10,20],'automatic',True,False,False,'학위 전체 기간','2027: equivalent ATAR 85~89.95 = 10% · ATAR 90+ = 20%','장학 약관 continuation 기준',note='2027 공식 장학 페이지 기준. 모든 국가 대상이며 eligible combined bachelor degree도 포함됩니다. 별도 장학 신청 없이 final transcript 기준 자동 심사됩니다.',pharmacy=True,amount_status='confirmed_2027')
scholarship('rmit','rmit-pending','2027 한국 학생 대상 학위 장학 상태','rmit',None,'pending',None,None,None,note='현재 공개 목록에서 한국에서 바로 지원하는 일반 국제학생에게 자동 적용되는 RMIT Pharmacy 학위 tuition scholarship은 확인되지 않았습니다. 2027 Medibank High Achiever A$20,000 장학은 국제학생이어도 호주에서 Australian Year 12 또는 IB를 공부하고 2026년에 졸업하며 VTAC로 지원하는 학생만 대상이므로 일반 한국 고교/해외고 지원자 장학으로 표시하지 않습니다.',pharmacy=None)
# Medibank High Achiever는 현금성 장학이라 percentage scholarship helper에 넣지 않고 status note에서만 eligibility를 설명합니다.
scholarship('unsw','unsw-award','International Student Award','unsw-scholarship',20,'not_eligible',None,None,False,note='공식 eligible-country 목록에 South Korea 없음. 한국 국적 기본 장학으로 표시하지 않습니다.',pharmacy=None)

def housing(i,id,name,src,weekly=None,weeks=None,utilities=None,meals=None,campus=None,note=''):
 accommodation.append(dict(id=id,university_id=i,name=name,weekly_cost=fact(weekly,src),contract_weeks=fact(weeks,src),official_contract_total=fact(None,src),utilities=fact(utilities,src),meals=fact(meals,src),campus_distance=fact(campus,src),note=note))
housing('utas','utas-christ','Christ College','utas-housing',316,42,True,False,'Sandy Bay 교내 · 무료 교내 셔틀','2027 주당 요금. 42주 계약은 College 안내 기준. 방 형태·입주 자격·보증금 확인 필요.')
housing('utas','utas-john','John Fisher College','utas-housing',316,42,True,False,'Sandy Bay 교내','2027 주당 요금. 약학 수업 캠퍼스와 통학 동선을 확인하세요.')
housing('latrobe','latrobe-units','The Units','latrobe-units',255,None,True,False,'Bendigo 캠퍼스','현재 공식 residence page는 A$255/week부터, semester contract, utilities 포함으로 안내합니다. 계약기간의 정확한 주수와 2027 전용 rate card는 별도 확인합니다.')
housing('latrobe','latrobe-villas','The Villas','latrobe-villas-current',270,None,True,False,'Bendigo 캠퍼스','현재 공식 residence page는 A$270/week부터, semester contract, utilities 포함으로 안내합니다. 계약기간의 정확한 주수와 2027 전용 rate card는 별도 확인합니다.')
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
 dict(id='newcastle-english',entity_id='newcastle-bpharm-hons',field='english',source_ids=['newcastle-2027-course','newcastle-fee-2027','newcastle-nonstandard-english-2025'],status='source_conflict',summary='2027 Degree Guide + 2025-08-28 Non-Standard English list는 IELTS 6.5/각6.5, 현재 degree page 국제학생 섹션은 7.0/각7.0',decision='현재 공식자료끼리 불일치하므로 자동 충족 판정에서 제외. Newcastle Admissions 서면 확인 전 단일값으로 확정하지 않음.'),
 dict(id='monash-foundation-version',entity_id='monash-foundation',field='progression',source_ids=['monash-foundation','monash-foundation-p6007-current'],status='source_conflict',summary='2027 Pathway Programs PDF에는 Pharmacy가 P6001로, 현재 Monash College 웹페이지에는 P6007과 Foundation 75% · English 65% · Maths/Chemistry 50%로 표시됩니다.',decision='현재 약대 과정은 P6007로 안내되지만 문서 간 과정코드가 달라 Foundation 진급점수는 최종 확정값으로 표시하지 않습니다.'),
]
# Canberra 2027 course PDF verified after initial seed.
source('canberra-2027','Canberra Bachelor of Pharmacy HLB301 · 2027','https://www.canberra.edu.au/course/HLB301/1/2027.pdf',2027,'official_course')
source('canberra-course-guide-2027','University of Canberra · 2027 Domestic Course Guide','https://www.canberra.edu.au/campaign/uc-course-guide.pdf',2027,'official_guide')
source('canberra-intl-equiv','University of Canberra · International qualification equivalencies','https://www.canberra.edu.au/future-students/entry-requirements-options/academic-entry-requirements/international-qualifications',None,'official_admissions')
source('canberra-english-current','University of Canberra · Current English language requirements','https://www.canberra.edu.au/future-students/entry-requirements-options/core-admission-requirements/english-language-requirements',None,'official_admissions')
setp('canberra',name=fact('Bachelor of Pharmacy · Honours option','canberra-2027'),duration_years=fact(4,'canberra-course-guide-2027'),duration_label=fact('4년','canberra-course-guide-2027'),bachelor_award_year=fact(4,'canberra-course-guide-2027'),final_degree=fact('Bachelor of Pharmacy · Honours option available','canberra-2027'),international_recruitment=fact(True,'canberra-2027'),highlights=['4년 Bachelor of Pharmacy','Selection Rank 75','Canberra · Regional'],editorial='2027 Semester 1에 국제학생 모집이 열려 있는 4년 Bachelor of Pharmacy입니다. 2027 Course Guide의 Selection Rank는 75이며, 국제학력은 UC selection-rank equivalency로 환산합니다. 성적과 Honours 요건을 충족하면 Honours로 졸업할 수 있습니다.')
eng('canberra',7,{'L':7,'R':7,'W':7,'S':7},src='canberra-2027',pte=65,toefl={'overall':94,'R':25,'L':25,'S':23,'W':27});intake('canberra',[2],'2027-02-15 · Semester 1','canberra-2027')
req('canberra','assumed','assumed','assumed','assumed','수학 + Biology/Human Movement, Chemistry/Physics는 assumed knowledge로 안내. 필수 prerequisite와 구분.',src='canberra-2027')
for route_record in routes:
 route_record['intake_months']=fact([2],'uq-accelerated') if route_record['id']=='uq-accelerated' else fact([2],'curtin-college') if route_record['id']=='curtin-college' else fact([2],'newcastle-foundation') if route_record['id']=='newcastle-foundation' else fact(None,route_record['availability']['source_id'])

# Additional course-specific official checks, 2026-09-24.
source('curtin-structure','Curtin · 2026 개편 Pharmacy 구조','https://www.curtin.edu.au/news/advice/how-to-become-a-pharmacist/',2026,'official_course')
setp('curtin',duration_years=fact(3.75,'curtin'),duration_label=fact('3년 9개월','curtin'),bachelor_award_year=fact(3.75,'curtin'),highlights=['3년 9개월','Diploma → 2학년','Perth · Regional'],editorial='현재 Curtin 공식 과정 페이지는 Bachelor of Pharmacy (Honours)를 3년 9개월로 안내합니다. 2027 국제학생 Direct 시작월과 학비는 아직 과정 페이지에 표시되지 않아 확인 중입니다.',review_items=['2027 국제학생 학비','2027 국제학생 Direct 시작월']); intake('curtin',None,None,src='curtin')
req('curtin','required','required','recommended','not_required',grade='Chemistry와 Mathematics Applications 또는 인정 동등 과목. Biology/Human Biology는 권장.',src='curtin')
row(registration,'curtin').update(supervised_practice_in_degree=fact(False,'curtin-structure'),itp_in_degree=fact(False,'curtin-structure',note='등록용 internship/ITP는 학위 밖 졸업 후 과정'),post_graduation_internship=fact(True,'curtin-structure'))
source('unisq-course','UniSQ · International Bachelor of Pharmacy (Honours)','https://www.unisq.edu.au/study/degrees-and-courses/bachelor-of-pharmacy-honours?studentType=international',None,'official_course')
eng('unisq',7,{'L':7,'R':7,'W':6.5,'S':7},src='unisq-course')
req('unisq','assumed','assumed','assumed','assumed','English C, Mathematical Methods/Specialist C, Biology/Chemistry/Physics 중 하나 C는 assumed knowledge.',src='unisq-course')
fee('unisq',34280,src='unisq-course',year=2026,load='8 units / year · 2026 국제학생 참고값')
setp('unisq',duration_years=fact(4,'unisq'),duration_label=fact('4년','unisq'),bachelor_award_year=fact(4,'unisq'),editorial='2027 국제학생은 Trimester 1에만 입학하며 2월 15일 시작입니다. 2027은 4년 과정이고, 3년 accelerated option은 2028부터 시작합니다.',review_items=['2027 학비','2027 장학금 적용'])
row(registration,'unisq').update(supervised_practice_in_degree=fact(False,'unisq-course'),post_graduation_internship=fact(True,'unisq-course'))
source('griffith-2026','Griffith 2026 International Guide · Pharmacy H1','https://www.griffith.edu.au/__data/assets/pdf_file/0035/2193587/Griffith-University-2026-International-Study-Guide-Digital.pdf',2026,'official_guide')
for q,score,scale in [('csat',331,'대학 공식 CSAT 환산'),('sat',1080,'1600 · 미국 고교졸업 자격 동반'),('ib',28,'45'),('alevel',7,'대학 A-level 환산점수')]:
 record=next(x for x in qualifications if x['program_id']=='griffith-bpharm-hons' and x['qualification']==q)
 record.update(score=fact(score,'griffith-2026',note='Pharmacy 1614 = H1. 2026 공개 기준이며 2027 확정값이 아닙니다.'),scale=scale)
row(english,'griffith')['ielts_overall']=fact(7,'griffith-2026',note='2026 Pharmacy 행. 각 영역과 2027 조건은 별도 확인 중.')
source('griffith-college-entry','Griffith College · 국제학생 입학조건','https://www.griffithcollege.edu.au/international-students/entry-requirements/',None,'official_pathway')
gc=next(r for r in routes if r['id']=='griffith-college')
gc['english']=fact('Pharmacy 연결 Diploma: IELTS 6.5 / 각 6.0 · PTE 58 / 각 50 · TOEFL 79 / 각 19','griffith-college-entry',note='일반 Diploma 영어 5.5를 약대 연결 경로에 적용하지 않습니다. Pharmacy 연결 전용 영어기준입니다.')
gc['qualification']=fact('한국 Diploma 입학: 고3 졸업 + 4개 학업과목 평균 Rank 6, 또는 고교 졸업 + CSAT 280 / 상위 3개 stanine 6, 또는 검정고시 평균 80','griffith-college-entry',note='현재 Griffith College 국제학생 country entry table의 Diploma 기준입니다. Griffith University Pharmacy 본과 Direct 점수가 아닙니다.')
# Link Direct route summaries to their own program rather than duplicate unknowns.
for route_record in routes:
 if route_record['type']=='direct':
  program=next(p for p in programs if p['id']==route_record['program_id'])
  start=next(x for x in intakes if x['program_id']==program['id'])
  route_record['duration']=copy.deepcopy(program['duration_label'])
  route_record['intake']=copy.deepcopy(start['label'])
  route_record['intake_months']=copy.deepcopy(start['months'])
  route_record['note']='아래 표에 성적·선수과목·영어 기준을 정리했습니다.'

# Keep high-value Direct route summaries synchronized with verified course facts.
_utas_direct=next(r for r in routes if r['id']=='utas-bpharm-hons-direct')
_utas_direct['english']=fact('IELTS 6.5 / 각 6.0','utas')
_utas_direct['qualification']=fact('2027 minimum ATAR 70 상당 · CSAT 305 · IB 25 · A-level 8 · OSSD 70% · SAT 980','utas-atar-equiv-current',2023,status='latest_published',note='현재 UTas 공식 country-entry 페이지가 링크하는 equivalency table의 ATAR 70 열 기준')
_utas_direct['note']='2027 minimum ATAR 70 상당 학력 + Mathematics + Chemistry 또는 Physical Sciences 요건을 충족해야 합니다.'
_uq_direct=next(r for r in routes if r['id']=='uq-bpharm-hons-direct')
_uq_direct['english']=fact('IELTS 6.5 / 각 6.0 · PTE 64 / 각 60 · TOEFL 87 (L19/R19/W21/S19)','uq')
_uq_direct['qualification']=fact('2027 Guaranteed ATAR 80 + Mathematics + Chemistry · 해외학력은 UQ 동등성 환산','uq-guaranteed-atar-2027')
_uq_direct['note']='2027 guaranteed ATAR 80은 Australian ATAR 기준입니다. 한국·IB·A-level 등 해외학력은 UQ가 동등성 환산해 평가합니다.'
_sydney_direct=next(r for r in routes if r['id']=='sydney-bpharm-hons-direct')
_sydney_direct['english']=fact('IELTS 6.5 / 각 6.0 · TOEFL 85 (W19, L/R/S17)','sydney')
_sydney_direct['qualification']=fact('2027 CSAT 346 · IB 31 · A-level 14 · SAT 1300 + Mathematics prerequisite','sydney')
_sydney_direct['note']='한국 일반고 졸업장만으로는 이 Direct 환산표에서 평가하지 않으며, 수능 등 인정 학력과 Mathematics prerequisite를 함께 충족해야 합니다.'
_uwa_direct=next(r for r in routes if r['id']=='uwa-bpharm-hons-direct')
_uwa_direct['english']=fact('IELTS 7.0/각7.0 · PTE 65/각65 · TOEFL 94 (W27, S23, L/R24)','uwa-combined-rules-current')
_uwa_direct['qualification']=fact('ATAR 85 equivalent · CSAT 329 · IB 30 · A-level 10 · SAT 1220 · UWAC Foundation 70','uwa')
for uid in ['adelaide','qut','canberra','unisq','unsw']:
 dr=next(r for r in routes if r['id']==uid+'-bpharm-hons-direct')
 er=row(english,uid); rr=row(requirements,uid)
 if uid=='adelaide':
  dr['english']=fact('IELTS 6.5/각6.0 · PTE 64/각60 · TOEFL 79 (L12/R13/W21/S18)','adelaide-english-current')
  dr['qualification']=fact('SACE Stage 2 Biology, Chemistry 또는 Physics 중 1과목(또는 동등 수준) + 학력별 입학점수','adelaide')
  dr['note']='일반 Direct 시작은 2월입니다. 7월은 학점 인정이 있는 국제학생을 case-by-case로 심사합니다.'
 elif uid=='qut':
  dr['english']=fact('IELTS 6.5 / 각 6.0 · PTE 58 / 각 50 · TOEFL 79','qut')
  dr['qualification']=fact('Chemistry + Mathematical Methods/Specialist Mathematics는 assumed knowledge · 필수 prerequisite와 구분','qut-fee-2027')
  dr['note']='2027 본과는 2월 시작입니다. 수학·화학은 assumed knowledge이며 미이수 학생은 bridging study 안내를 확인합니다.'
 elif uid=='canberra':
  dr['duration']=fact('4년','canberra-course-guide-2027')
  dr['english']=fact('IELTS 7.0 / 각 7.0 · PTE 65 · TOEFL 94 (R25/L25/S23/W27)','canberra-english-current')
  dr['qualification']=fact('Selection Rank 75 + 국제학력 UC rank 환산 · 수학 + Biology/Human Movement + Chemistry/Physics assumed knowledge','canberra-course-guide-2027')
  dr['note']='2027 Semester 1은 2월 15일 시작입니다. 국제학생은 해외학력을 UC Selection Rank로 환산해 평가합니다.'
 elif uid=='unisq':
  dr['duration']=fact('4년','unisq')
  dr['english']=fact('IELTS 7.0 · Speaking/Reading/Listening 7.0 · Writing 6.5','unisq-pharmacy-current')
  dr['qualification']=fact('Mathematics + Biology/Chemistry/Physics 중 1과목 Year 12 C 수준 assumed knowledge','unisq-pharmacy-current')
  dr['note']='2027 국제학생은 Trimester 1 한 번만 입학하며 수업 시작은 2월 15일입니다. 3년 accelerated pathway는 2028부터입니다.'
 elif uid=='unsw':
  dr['intake']=fact('Term 1 · 2027','unsw-2027-course')
  dr['intake_months']=fact([2],'unsw-2027-course')
  dr['english']=fact('IELTS 7.0 / 각 6.0 · PTE 65 / 각 54 · TOEFL 94 (W25, R/L/S23)','unsw-english-current')
  dr['qualification']=fact('2027 Guide: International ATAR 87 / IB 33 · current A-level 15 · assumed knowledge Chemistry + Mathematics Advanced','unsw-2027-guide')
  dr['note']='2027부터 Doctor of Pharmacy 명칭으로 전환됩니다. 입학요건은 학교가 기존 기준과 동일하다고 안내하지만 새 명칭의 APC/Board 반영은 별도 확인합니다.'
_newcastle_direct=next(r for r in routes if r['id']=='newcastle-bpharm-hons-direct')
_newcastle_direct['english']=fact('공식자료 충돌: IELTS 6.5/각6.5 vs 국제학생 degree page 7.0/각7.0','newcastle-nonstandard-english-2025',status='source_conflict',note='2027 Degree Guide와 2025-08-28 정책 목록은 6.5/6.5, 현재 degree page 국제학생 섹션은 7.0/7.0입니다.')
_newcastle_direct['qualification']=fact('2027 IB 28 확인 · 기타 국제학력 course-specific 환산은 업데이트 대기','newcastle-prospectus-2027')
_newcastle_direct['note']='2027년 2월 22일 시작과 IB 28은 확인됐습니다. 영어는 현재 공식자료 간 충돌로 자동 판정하지 않습니다.'
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
      "현재 국제학생 course page 학비 A$31,710은 2026 표시값",
      "JCU Prep은 국내학생 안내가 중심이라 한국 국제학생 pathway로 확정하지 않음"
    ]
  },
  "utas": {
    "why": [
      "3년 Fast-track",
      "Tasmania 요건 충족 시 두 번째 485 +2년",
      "2027 국제장학 30% 자동심사"
    ],
    "watch": [
      "3년에 압축해 연간 수강량이 많음",
      "Foundation 시작시점과 다음 Pharmacy 입학시기 조합 확인 필요"
    ]
  },
  "curtin": {
    "why": [
      "3년 9개월",
      "Curtin College Diploma → 약대 2학년",
      "2027 Curtin College Stage 2 학비 A$44,900"
    ],
    "watch": [
      "Curtin 본과 2027 국제학생 학비·Direct 시작월은 계속 확인 중",
      "Stage 1이 필요한 경우 2027 A$32,900 추가"
    ]
  },
  "uq": {
    "why": [
      "2027 Guaranteed ATAR 80",
      "2월 4년 · 7월 약 3.5년",
      "Standard/Accelerated Foundation 모두 2027 7월 BPharm 연결 가능"
    ],
    "watch": [
      "해외학력은 ATAR 80 동등성 환산이 별도",
      "신설 5년 PharmD는 APC·Pharmacy Board 승인 진행 중"
    ]
  },
  "adelaide": {
    "why": [
      "4년 BPharm(Hons) + 약 12주 practical placement",
      "5년 BPharm(Hons)+Master 연계 시 internship/ITP 통합 가능",
      "Adelaide 지역요건 충족 시 두 번째 485 +1년"
    ],
    "watch": [
      "7월 입학은 학점 인정 학생 case-by-case이며 일반 고졸 Direct 7월 입학이 아님",
      "A$54,300은 2026 시작 학비이지 2027 확정 학비가 아님"
    ]
  },
  "griffith": {
    "why": [
      "Griffith College 2026/2027 Diploma → Pharmacy 1614에 80CP 공식 인정",
      "Gold Coast Regional",
      "2027 International Academic Merit 20%"
    ],
    "watch": [
      "2027 국내 Guaranteed Rank 76은 국제학생 Direct 점수가 아님",
      "2027 Direct 학비·국제학생 입학점수 최종 업데이트 대기"
    ]
  },
  "latrobe": {
    "why": [
      "Bendigo Regional · Category 3",
      "과학 선수과목 별도 요구 없음",
      "30% 자동장학 + 50%/100% Vice Chancellor 경쟁장학"
    ],
    "watch": [
      "ATAR 75.05는 2027 Guide 참고값이며 live page상 2026 lowest selection rank",
      "30% 장학은 수량 제한·offer acceptance 순 확보 조건 확인",
      "Vice Chancellor는 Direct Entry 대상 · 별도 지원·경쟁선발",
      "2027 국제학생 학비 발표 대기"
    ]
  },
  "qut": {
    "why": [
      "Chemistry·Math는 필수가 아니라 assumed knowledge",
      "QUT College Standard 12개월 / Intensive 6개월",
      "2027 International Merit 25%"
    ],
    "watch": [
      "Foundation 수료 후 Pharmacy package offer의 개별 progression 조건 확인",
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
      "한국에서 바로 지원하는 일반 학생에게 적용되는 Pharmacy 학위 tuition scholarship은 현재 공개목록에서 확인되지 않음",
      "Medibank A$20,000은 호주에서 Year 12/IB를 공부하는 국제학생용 별도 경쟁장학"
    ]
  },
  "newcastle": {
    "why": [
      "2027 학비 A$51,665",
      "Newcastle Regional",
      "Foundation 2027 A$31,400 경로 있음"
    ],
    "watch": [
      "2027 Degree Guide·2025 최신 정책목록은 IELTS 6.5/6.5, 현재 국제학생 degree page는 7.0/7.0으로 충돌",
      "2027 20% International Excellence는 Pharmacy 제외"
    ]
  },
  "canberra": {
    "why": [
      "4년 Bachelor of Pharmacy",
      "UC International Scholarship 10~30% 자동심사 · Pharmacy 제외목록 아님",
      "Canberra Regional + ACT 약사 직종 nomination list 포함"
    ],
    "watch": [
      "2027 가이드의 A$42,500은 2026 Annual Fee 표기",
      "장학률은 academic merit·strategic recruitment priorities에 따라 결정되고 GPA 5.0 유지 필요"
    ]
  },
  "unisq": {
    "why": [
      "Toowoomba Category 3",
      "2027 국제학생 Trimester 1",
      "2027 International Student Support Scholarship 10% · Pharmacy 제외 아님"
    ],
    "watch": [
      "3년 가속과정은 2028부터이며 2027에는 적용하지 않음",
      "2027 course offer guide는 9월 28일 최종화 예정이므로 현재 4년/T1 정보를 그 전에 2028 가속안과 혼동하지 않음"
    ]
  },
  "monash": {
    "why": [
      "5년 BPharm(Hons) / Doctor of Pharmacy",
      "5년차 paid supervised practice + Intern Training Program 통합",
      "관련 학사 졸업자는 Graduate Entry로 3학년 진입 가능"
    ],
    "watch": [
      "Foundation live page는 P6007, 2027 Pathway PDF는 legacy P6001이라 진급표 버전 충돌",
      "2027 ATAR 80은 국내 Monash Guarantee이며 국제학력 점수로 자동 환산하지 않음",
      "Melbourne은 지역 추가 485 대상 아님"
    ]
  },
  "sydney": {
    "why": [
      "5년 BPharm(Hons) / Master of Pharmacy Practice",
      "2027 수능346·IB31·SAT1300·A-level14 공식 점수",
      "USFP Standard 12개월 A$49,800 / Intensive 9개월 A$47,690"
    ],
    "watch": [
      "USFP에서 Pharmacy는 GPA 7.3 / English C 외 Mathematics prerequisite도 충족해야 함",
      "2027년에 Foundation을 시작하면 시작월에 따라 본과 진학은 2028이 될 수 있음",
      "Sydney는 지역 추가 485 대상 아님"
    ]
  },
  "unsw": {
    "why": [
      "2027부터 Doctor of Pharmacy 명칭",
      "5년 통합 과정",
      "Pharmacy 영어 IELTS 7.0 / 각 6.0"
    ],
    "watch": [
      "UNSW College progression 표는 아직 기존 Master of Pharmacy 명칭",
      "졸업 후 등록용 인턴십은 별도",
      "2027 본과 학비 발표 대기"
    ]
  },
  "uwa": {
    "why": [
      "고교 졸업 후 4년 Bachelor + PharmD",
      "UWA College Foundation 8개월/12개월 경로 구분",
      "Perth 지역요건 충족 시 두 번째 485 +1년"
    ],
    "watch": [
      "Foundation 한국 학력표는 최신 공개된 2025 brochure 값으로 연도 표시",
      "졸업 후 등록 internship은 별도",
      "2027 국제학생 본과 학비 업데이트 대기"
    ]
  }
}
for p in programs:
 if p['university_id'] in decision_lenses:p['decision_lens']=decision_lenses[p['university_id']]


# Public-copy layer: keep provenance/internal notes in data, but write student-facing summaries
# in short, decisive language. This runs after all factual records are assembled.
public_program_copy = {
  'jcu-bpharm-hons': dict(
    highlights=['3년 과정','Townsville · Cairns · Mackay','수학 필수 · 화학 권장'],
    editorial='2027 JCU Pharmacy는 Townsville·Cairns·Mackay에서 모두 2월 시작, 3년 과정입니다. 현재 공개 학비 A$31,710은 2026 금액이라 2027 학비에는 사용하지 않습니다.',
    review_items=['2027 본과 학비','한국 학력 Direct 점수','JCU Prep 국제학생 연계 여부'],
    decision_lens=dict(why=['3년 만에 학위 완료','세 캠퍼스 모두 Regional','화학은 권장, 수학은 필수'],watch=['2027 본과 학비 미확정','JCU Prep의 한국 국제학생 연계는 아직 미확정'])
  ),
  'utas-bpharm-hons': dict(
    highlights=['3년 과정','Cradle Coast · Hobart · Launceston','2027 학비 · 30% 장학'],
    editorial='Cradle Coast·Hobart·Launceston에서 모두 3년 만에 약학 학위를 마칩니다. 일반 4년 과정 분량을 3년에 압축한 과정이라 연간 학업량이 많습니다.',
    review_items=[],
    decision_lens=dict(why=['3년 Fast-track','Tasmania 지역혜택','2027 국제학생 장학 30% 자동심사'],watch=['3년 압축과정이라 학업 일정이 촘촘함','Foundation 시작월에 따라 Pharmacy 입학연도가 달라짐'])
  ),
  'curtin-bpharm-hons': dict(
    highlights=['3년 9개월','Curtin College → 2학년','Perth · Regional'],
    editorial='Curtin BPharm(Hons)은 3년 9개월 과정입니다. Direct 기준은 ATAR 80, Chemistry와 Mathematics, IELTS 7.0(각 7.0)입니다. 2027 본과 학비와 국제학생 시작일은 아직 미확정입니다.',
    review_items=['2027 본과 학비','2027 국제학생 시작일'],
    decision_lens=dict(why=['3년 9개월','Curtin College Diploma 후 약대 2학년','2027 Curtin College Stage 2 A$44,900'],watch=['2027 본과 학비·시작일 미확정','Stage 1이 필요한 학생은 A$32,900 추가'])
  ),
  'uq-bpharm-hons': dict(
    highlights=['2월 4년 · 7월 3.5년','2027 ATAR 80','Foundation → 7월 입학'],
    editorial='UQ BPharm(Hons)은 2월 입학 4년, 7월 입학 약 3.5년입니다. 2027 ATAR 기준은 80이며 해외학력은 UQ 환산점수로 평가합니다. 별도로 2027 신설 5년 PharmD가 있습니다.',
    review_items=[],
    decision_lens=dict(why=['2월 4년 · 7월 약 3.5년','2027 ATAR 80','Standard·Accelerated Foundation 모두 7월 BPharm 연결'],watch=['해외학력은 UQ 환산점수로 평가','신설 5년 PharmD는 별도 과정이며 승인 상태도 따로 봄'])
  ),
  'adelaide-bpharm-hons': dict(
    highlights=['4년 BPharm(Hons)','수능 345','5년 Master 연계'],
    editorial='Direct 신입은 2월 시작입니다. 7월은 학점 인정 학생만 개별 심사합니다. 4년 과정 안에 약 12주 실습이 있고, 졸업 후 등록 인턴십은 별도입니다. 5년 연계 Master 과정은 인턴십과 Intern Training Program을 마지막 해에 통합합니다.',
    review_items=['2027 본과 학비'],
    decision_lens=dict(why=['4년 BPharm(Hons) + 약 12주 실습','5년 Master 연계 시 인턴십·ITP 통합','Adelaide Regional'],watch=['7월은 고졸 신입 Direct 입학월이 아님','A$54,300은 2026 학비 · 2027 학비 미확정'])
  ),
  'griffith-bpharm-hons': dict(
    highlights=['Griffith College → 80CP','Gold Coast · Regional','Direct 점수는 2026 참고'],
    editorial='Direct 입학과 Griffith College Diploma 두 경로가 있습니다. 현재 Direct 참고점수는 2026 기준 수능 331 · IB 28 · SAT 1080 · A-level 7입니다. Griffith College Diploma를 마치면 80CP를 인정받고 약대 2학년으로 진학합니다.',
    review_items=['2027 Direct 국제학력 점수','2027 본과 학비','약대 선수과목 최신표'],
    decision_lens=dict(why=['Griffith College Diploma → 약대 2학년','Gold Coast Regional','2027 International Academic Merit 20%'],watch=['Direct 점수는 현재 2026 공식값 사용','2027 Direct 점수·본과 학비 미확정'])
  ),
  'latrobe-bpharm-hons': dict(
    highlights=['Bendigo · Regional','2027 Guide 참고 ATAR 75.05','최대 100% 장학'],
    editorial='Bendigo 캠퍼스 4년 약대이며 2027년 3월 시작입니다. 2027 Undergraduate Course Guide에는 ATAR 75.05가 표시되지만 live course page는 이를 2026 lowest selection rank로 설명하므로 보장 컷이 아닌 지원 참고값으로 봅니다. 별도 과학 선수과목은 없습니다.',
    review_items=['2027 국제학생 학비','지원 시점 최종 selection rank'],
    decision_lens=dict(why=['Bendigo Regional','과학 선수과목 별도 없음','30% 자동장학 + 50%/100% Vice Chancellor 경쟁장학'],watch=['ATAR 75.05는 2027 Guide 참고값이며 보장 컷 아님','30% 장학은 수량 제한 · 오퍼 수락 순','Vice Chancellor는 Direct Entry 대상 · 별도 지원·경쟁선발','2027 본과 학비 미확정'])
  ),
  'qut-bpharm-hons': dict(
    highlights=['4년','수학·화학 필수 아님','2027 학비 A$46,200'],
    editorial='QUT Pharmacy는 Chemistry와 수학을 필수 선수과목으로 요구하지 않습니다. 대신 선행지식으로 권장하며, 부족한 학생은 bridging study로 보완합니다. QUT College는 Standard 12개월과 Intensive 6개월 Foundation을 운영합니다.',
    review_items=[],
    decision_lens=dict(why=['수학·화학이 필수 선수과목 아님','Standard 12개월 · Intensive 6개월 Foundation','2027 International Merit 25%'],watch=['Foundation 패키지의 약대 진급조건 충족 필요','Brisbane은 지역 추가 485 없음'])
  ),
  'rmit-bpharm-hons': dict(
    highlights=['4년','2027 학비 A$49,920','Foundation · Associate 경로'],
    editorial='Bundoora 캠퍼스 4년 과정입니다. 2027년 3월 1일 시작, 학비 A$49,920, IELTS 7.0(각 6.5)입니다. Foundation은 약대 1학년, Biomedicine Associate Degree는 96CP를 인정받아 약대 본과 3년이 남습니다.',
    review_items=[],
    decision_lens=dict(why=['한국 고교 75% 또는 고교 졸업 + 수능 300부터 Direct','RMIT Foundation → 약대 1학년','2027 학비 A$49,920'],watch=['Chemistry + Mathematics 필수','Associate Degree는 1년 Diploma와 다른 경로','한국에서 바로 지원하는 일반 학생용 약대 학비장학은 현재 없음'])
  ),
  'newcastle-bpharm-hons': dict(
    highlights=['4년','2027 학비 A$51,665','Foundation A$31,400'],
    editorial='Newcastle의 영어 공식자료가 두 값으로 엇갈립니다. 2027 Degree Guide와 정책 목록은 IELTS 6.5(각 6.5), 현재 국제학생 과정 페이지는 7.0(각 7.0)입니다. 지원 준비는 안전하게 7.0(각 7.0) 기준으로 잡습니다.',
    review_items=['영어 최종 적용점수','2027 한국·SAT·A-level·OSSD Direct 점수','2027 이후 APC 인증 갱신'],
    decision_lens=dict(why=['2027 학비 A$51,665','Newcastle Regional','Foundation 2027 A$31,400'],watch=['영어 준비기준은 IELTS 7.0(각 7.0)','2027 International Excellence 20%는 Pharmacy 제외'])
  ),
  'canberra-bpharm-hons': dict(
    highlights=['4년','Selection Rank 75','Canberra · Regional'],
    editorial='2027 Semester 1에 시작하는 4년 Bachelor of Pharmacy입니다. Selection Rank 75, IELTS 7.0(각 7.0)이며 국제학력은 UC 환산표로 평가합니다. UC 국제장학금 10~30%는 입학 지원과 함께 심사합니다.',
    review_items=[],
    decision_lens=dict(why=['4년 Bachelor of Pharmacy','국제장학금 10~30% 자동심사','Canberra Regional'],watch=['A$42,500은 2026 학비','장학 유지조건은 Course GPA 5.0 이상'])
  ),
  'unisq-bpharm-hons': dict(
    highlights=['2027은 4년','2월 15일 시작','Toowoomba · Regional'],
    editorial='2027 국제학생은 Trimester 1 한 번만 입학하며 2월 15일 시작, 4년 과정입니다. 3년 Accelerated Pharmacy는 2028년부터 시작합니다.',
    review_items=['2027 본과 학비'],
    decision_lens=dict(why=['Toowoomba Category 3','2027년 2월 15일 시작','2027 국제장학금 10%'],watch=['3년 과정은 2028년부터','2027 본과 학비 미확정'])
  ),
  'monash-bpharm-hons': dict(
    highlights=['5년 PharmD','5년차 유급 인턴십','4년 BPharm(Hons) Exit'],
    editorial='Monash P6007은 5년 통합 PharmD 과정입니다. 4년을 마치면 BPharm(Hons)로 졸업할 수 있고, 5년차에는 유급 supervised practice와 Intern Training Program이 들어갑니다. 관련 학사 졸업자는 Graduate Entry로 3학년 진입을 준비할 수 있습니다.',
    review_items=[],
    decision_lens=dict(why=['5년 BPharm(Hons) / Doctor of Pharmacy','5년차 유급 supervised practice + ITP','관련 학사 졸업자는 Graduate Entry 가능'],watch=['Foundation 진급표의 과정코드가 웹과 2027 PDF에서 다름','2027 ATAR 80은 호주 국내 Monash Guarantee','Melbourne은 지역 추가 485 없음'])
  ),
  'sydney-bpharm-hons': dict(
    highlights=['5년 통합','4년 BPharm(Hons) Exit','수학 필수'],
    editorial='5년 Bachelor of Pharmacy (Honours) + Master of Pharmacy Practice 통합과정입니다. 4년을 마치면 BPharm(Hons)로 졸업할 수 있고 5년차에 Master of Pharmacy Practice를 이수합니다. 수학은 필수, Chemistry·Biology는 선행지식, Physics는 권장입니다.',
    review_items=[],
    decision_lens=dict(why=['5년 BPharm(Hons) / Master of Pharmacy Practice','2027 수능 346 · IB 31 · SAT 1300 · A-level 14','USFP Standard A$49,800 · Intensive A$47,690'],watch=['USFP 진급: GPA 7.3 + English C + Mathematics','Foundation 시작월에 따라 본과는 2028 입학','Sydney는 지역 추가 485 없음'])
  ),
  'unsw-bpharm-hons': dict(
    highlights=['2027 Doctor of Pharmacy','5년','IELTS 7.0 · 각 6.0'],
    editorial='UNSW는 2027부터 Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy로 바뀝니다. 5년 통합과정이며 Direct 기준은 International ATAR 87 · IB 33, 영어는 IELTS 7.0(각 6.0)입니다.',
    review_items=['새 Doctor of Pharmacy 명칭의 APC·Board 등재','2027 본과 학비'],
    decision_lens=dict(why=['2027부터 Doctor of Pharmacy','5년 통합과정','IELTS 7.0 · 각 6.0'],watch=['UNSW College 진급표는 아직 기존 Master 명칭 사용','졸업 후 등록 인턴십 별도','2027 본과 학비 미확정'])
  ),
  'uq-pharmd': dict(
    highlights=['2027 신설 5년','2027 학비 A$60,952','700+시간 실습 + 인턴훈련'],
    editorial='2027 신설 5년 Doctor of Pharmacy입니다. 2월·7월 입학, 2027 국제학생 학비 A$60,952이며 2학년부터 700시간 이상의 임상실습, 4~5학년 compulsory intern training이 포함됩니다. APC·Pharmacy Board 승인은 아직 받지 않았습니다.',
    review_items=['APC·Pharmacy Board 승인','CSAT·IB·SAT 등 해외학력 Direct 점수','중간 Exit 여부'],
    decision_lens=dict(why=['2027 국제학생 모집 · 2월/7월','5년 안에 700+시간 실습 + intern training','2027 학비 A$60,952'],watch=['APC·Pharmacy Board 승인 전','해외학력 Direct 점수 미확정','중간 Exit 여부 미확정'])
  ),
  'uwa-bpharm-hons': dict(
    highlights=['4년 Bachelor + PharmD','ATAR 85','2027 장학 10~20%'],
    editorial='고교 졸업 후 4년 동안 Bachelor of Human Sciences (Pharmaceutical Health) + Doctor of Pharmacy를 함께 이수합니다. 입학 기준은 ATAR 85이며, combined degree 안에서 Doctor of Pharmacy 진급 보장은 WAM 65%입니다. 졸업 후 등록 인턴십과 Pharmacy Board 시험은 별도입니다.',
    review_items=['2027 본과 학비'],
    decision_lens=dict(why=['고교 졸업 후 4년 Bachelor + PharmD','UWA College Foundation 8개월 / 12개월','Perth Regional'],watch=['Foundation 한국 학력점수는 현재 2025 공식표 사용','졸업 후 등록 인턴십 별도','2027 본과 학비 미확정'])
  )
}
for p in programs:
    if p['id'] in public_program_copy:
        p.update(public_program_copy[p['id']])

route_notes = {
 'jcu-bpharm-hons-direct':'',
 'utas-bpharm-hons-direct':'수학 1과목과 Chemistry 또는 Physical Sciences 1과목을 충족해야 합니다.',
 'curtin-bpharm-hons-direct':'Direct 기준은 ATAR 80, Chemistry, Mathematics Applications, IELTS 7.0(각 7.0)입니다.',
 'uq-bpharm-hons-direct':'2027 ATAR 80 기준이며 해외학력은 UQ 환산점수로 평가합니다.',
 'adelaide-bpharm-hons-direct':'고졸 Direct는 2월 시작입니다. 7월은 학점 인정 학생만 개별 심사합니다.',
 'griffith-bpharm-hons-direct':'현재 표시 점수는 2026 국제가이드 기준입니다. 2027 점수 발표 후 교체합니다.',
 'latrobe-bpharm-hons-direct':'',
 'uwa-foundation-8':'8개월 과정은 IELTS 6.0(각 5.5). 한국 학력점수는 2025 공식표를 사용합니다.',
 'uwa-foundation-12':'12개월 과정은 IELTS 5.5(각 5.0). 한국 학력점수는 2025 공식표를 사용합니다.',
 'qut-bpharm-hons-direct':'수학·화학은 필수가 아니라 선행지식입니다. 부족하면 bridging study로 보완합니다.',
 'qut-foundation-standard':'12개월 Foundation 후 약대 패키지의 진급조건을 충족하면 본과 1학년으로 갑니다.',
 'qut-foundation-intensive':'고3 동등학력을 마치고 QUT 학사 입학기준에 거의 도달한 학생을 위한 6개월 과정입니다.',
 'rmit-bpharm-hons-direct':'2027년 3월 1일 시작. 한국 학력기준 + Chemistry·Mathematics + 영어조건을 모두 충족해야 합니다.',
 'newcastle-bpharm-hons-direct':'2027년 2월 22일 시작, IB 28입니다. 영어 준비기준은 안전하게 IELTS 7.0(각 7.0)으로 잡습니다.',
 'canberra-bpharm-hons-direct':'2027년 2월 15일 시작. 해외학력은 UC Selection Rank로 환산합니다.',
 'unisq-bpharm-hons-direct':'2027년은 2월 15일 한 번만 입학하며 4년 과정입니다. 3년 과정은 2028년부터입니다.',
 'sydney-usfp':'2027 Standard 학비 A$49,800. 시작월에 따라 Sydney Pharmacy 본과 입학은 2028년이 됩니다.',
 'sydney-usfp-intensive':'2027 Intensive 학비 A$47,690. Pharmacy 본과 2월 입학에 맞춰 Foundation 일정을 잡아야 합니다.',
 'monash-bpharm-hons-direct':'',
 'sydney-bpharm-hons-direct':'한국 일반고 졸업장만으로는 Direct가 되지 않습니다. 수능 등 인정 학력과 Mathematics 조건을 함께 충족해야 합니다.',
 'unsw-bpharm-hons-direct':'2027부터 Doctor of Pharmacy 명칭을 사용합니다. 새 명칭의 APC·Board 등재는 아직 미확정입니다.',
 'uq-pharmd-direct':'2027 국제학생 모집은 시작됐지만 APC·Pharmacy Board 승인은 아직 받지 않았습니다.',
 'griffith-college':'Diploma를 마치면 80CP를 인정받고 Pharmacy 2학년으로 진학합니다. T1 진학 시 본과 3년, T2 진학 시 약 3.5년이 남습니다.',
 'curtin-college':'Diploma 후 175 credits를 인정받고 PHAR1002를 추가 이수한 뒤 Pharmacy 2학년으로 진학합니다.',
 'uq-standard-2027-entry':'2026년 9월 시작 → 2027년 7월 BPharm 입학. 2027년 2월 Standard 시작은 2028년 본과로 연결됩니다.',
 'uq-accelerated':'2027년 2월 시작 → 7월 BPharm 입학. GPA·영어·필수과목 진급기준을 충족해야 합니다.',
 'unsw-foundation-standard':'현재 공개 진급기준은 GPA 7.6 · Academic English B · Life Science/Physical Science입니다. 표에는 아직 기존 Master of Pharmacy 과정명이 남아 있습니다.',
 'monash-foundation':'현재 웹페이지는 P6007 기준 Foundation 75% · English 65%를 안내합니다. 2027 PDF에는 이전 코드 P6001이 남아 있어 최종 진급기준은 미확정입니다.',
 'newcastle-foundation':'Foundation 수료 후 Pharmacy 1학년으로 진학합니다. 2027 학비 A$31,400.',
 'monash-ge':'최소요건 충족자 중 경쟁 선발합니다.',
 'rmit-associate':'Biomedicine Associate Degree 완료 후 96CP를 인정받아 Pharmacy 본과 3년이 남습니다.',
 'latrobe-foundation':'Foundation 수료 후 Bendigo Pharmacy 1학년으로 진학합니다. 현재 공개 학비 A$29,780은 2026 금액입니다.',
 'uwa-bpharm-hons-direct':'고교 졸업 후 4년 combined degree로 시작합니다. Doctor of Pharmacy 진급보장은 WAM 65%, 졸업 후 등록 인턴십은 별도입니다.',
 'rmit-foundation':'2027 Foundation 학비 A$34,250. Foundation에서 Chemistry·Mathematics 조건을 채우고 Pharmacy 1학년으로 진학합니다.',
 'utas-foundation-standard':'한국 고2 평균 60%부터 입학. 수료 후 다음 Pharmacy 입학시기에 맞춰 진학합니다.',
 'utas-foundation-fast':'한국 고2 평균 65%부터 입학. General Mathematics가 필요하며 Standard보다 빠른 일정입니다.'
}
for r in routes:
    if r['id'] in route_notes:r['note']=route_notes[r['id']]

_adelaide_scholar=next((x for x in scholarships if x['id']=='adelaide-merit'),None)
if _adelaide_scholar:
 _adelaide_scholar['academic_threshold']=fact('ATAR 75 또는 국제 동등성적','adelaide-scholarship',status='latest_published')
 _adelaide_scholar['note']='Adelaide Merit Scholarship 15%. 국제학생은 입학 지원 시 자동심사되며 Pharmacy는 현재 제외과정 목록에 포함되지 않습니다.'

scholarship_notes = {
 'griffith-merit':'한국 학생 대상. Pathway 패키지는 최종 성적 제출 후 심사.',
 'sydney-award':'한국 학생 대상. Personal statement 3문항, 각 200단어 이내.',
 'monash-merit':'연 8명 선발. 50%는 과정군 최상위, 25%는 차상위.',
 'newcastle-excellence':'Bachelor of Pharmacy (Honours)는 2027 20% 장학 제외과정.',
 'jcu-excellence':'Pharmacy도 25% 장학 대상. 입학 지원과 함께 자동심사, 수혜 후 성적 유지조건 적용.',
 'unsw-award':'현재 한국 국적은 대상 국가가 아닙니다.',
 'curtin-global-merit':'2027/2028 WA 캠퍼스 국제학생 대상. Pharmacy도 포함.',
 'qut-merit':'2027 International Merit Scholarship. Pharmacy 포함, 입학 지원과 함께 심사.',
 'latrobe-high-achiever':'Bendigo Bachelor of Pharmacy (Honours)도 대상 과정.',
 'canberra-international-2027':'입학 지원과 함께 자동심사. 10·20·30% 중 선발되며 재학 중 Course GPA 5.0 이상 유지.',
 'unisq-support':'2027 학비 10% 감면. Pharmacy 포함, 다른 UniSQ 학비장학과 중복 불가.',
 'utas-tims':'Pharmacy 포함. 다른 UTas 장학과 중복되지 않으며 더 높은 장학 하나만 적용.',
 'uq-excellence':'별도 신청 없이 자동심사. 다른 UQ 학비감면과 중복 불가.',
 'adelaide-merit':'Bachelor of Pharmacy (Honours)도 대상 과정.',
 'rmit-pending':'한국에서 바로 지원하는 일반 학생용 Pharmacy 학비장학은 현재 공개된 것이 없습니다. Medibank A$20,000 장학은 호주에서 Year 12/IB를 이수하고 VTAC로 지원하는 국제학생 대상입니다.',
 'uwa-global-excellence':'모든 국가 대상. Eligible combined degree 포함, 별도 신청 없이 성적으로 자동심사.',
 'latrobe-health-innovation-30':'30% 장학. 별도 신청 없이 심사되며 수량이 제한되어 오퍼 수락 순서가 중요합니다.'
}
for x in scholarships:
    if x['id'] in scholarship_notes:x['note']=scholarship_notes[x['id']]

housing_notes = {
 'utas-christ':'2027 요금 · 42주 계약.',
 'utas-john':'2027 요금.',
 'latrobe-units':'Semester 계약 · 공과금 포함 · A$255/주부터.',
 'latrobe-villas':'Semester 계약 · 공과금 포함 · A$270/주부터.',
 'jcu-townsville-2026':'2026 일반 장기체류 참고요금. Pharmacy 장기체류는 academic rate가 따로 적용됩니다.',
 'jcu-cairns-2026':'2026 일반 장기체류 참고요금. Pharmacy 장기체류는 academic rate가 따로 적용됩니다.',
 'uq-kev-carmody':'현재 공개 최저가. Pharmacy Dutton Park 캠퍼스까지 통학합니다.',
 'uq-walcott':'현재 공개 최저가. Pharmacy Dutton Park 캠퍼스까지 통학합니다.',
 'adelaide-mattanya-2027':'2027 연 A$16,640 / 52주 · 전기·가스·수도·인터넷 포함.',
 'adelaide-village-2027':'2027 연 A$19,760 / 52주 · 전기·가스·수도·인터넷 포함.',
 'griffith-village-2027':'2027 full-year shared apartment A$329.85/주부터.',
 'curtin-perth-housing':'캠퍼스 도보 5~10분. 2026 표준 full-year 계약은 48주였습니다.',
 'qut-brisbane-guide':'QUT 생활비 가이드: student apartment A$1,600~2,200/월, catered accommodation A$2,400~2,650/월.',
 'rmit-walert-2027':'2027 4-bedroom apartment 1인실 A$14,260 / 46주 · Bundoora 캠퍼스 인근.',
 'newcastle-2027':'2027 self-catered A$249.45~465.93/주 · 식사 포함형 A$334.45~580.93/주.',
 'canberra-campus-west-2027':'2027 12-bedroom apartment room A$210.50/주 · 공과금 포함.',
 'canberra-weeden-2027':'3~7 bedroom apartment room A$221~252/주 · 공과금 포함.',
 'unisq-rescollege':'현재 약 A$155~220/주. Single-bedroom unit은 약 A$275~290+/주.',
 'monash-parkville-share':'Parkville shared accommodation 약 A$290~380/주.',
 'sydney-qmb-2026':'2026 48주 Standard Room A$382/주.',
 'sydney-regiment-2026':'2026 Standard Room A$408/주.',
 'unsw-2027-status':'Barker Street Apartments는 2027년 운영하지 않습니다.',
 'uwa-trinity-2027':'2027 Standard Room A$595/주 · 3식, 공과금, Wi-Fi, 방 청소 포함.'
}
for x in accommodation:
    if x['id'] in housing_notes:x['note']=housing_notes[x['id']]

for r in registration:
    if r['program_id']=='uwa-bpharm-hons':
        r['note']='졸업 후 supervised internship과 Pharmacy Board 등록시험을 마쳐야 General Registration을 받을 수 있습니다.'
    else:
        r['note']='학위에 포함된 실습 범위와 별개로, Pharmacy Board가 요구하는 등록 절차를 마쳐야 General Registration을 받을 수 있습니다.'


data=dict(schema_version='1.0.0',academic_year=2027,verified_date=DATE,universities=universities,programs=programs,entry_routes=routes,qualifications=qualifications,requirements=requirements,english=english,intakes=intakes,tuition=tuition,scholarships=scholarships,accommodation=accommodation,professional_registration=registration,sources=list(sources.values()),conflicts=conflicts)
(ROOT/'data/catalog.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
config=dict(site_name='호주약대 가이드',brand='TNS',language='ko',academic_year=2027,production_url=None,production_approved=False,
 channels=[dict(id='kakao',label='카카오톡 상담',detail='내 조건으로 1:1 상담',url='https://open.kakao.com/o/slehLvKi',source='tnsuhak/xjtlu-korea main index.html'),dict(id='phone',label='전화 상담',detail='02-3288-1733',url='tel:0232881733',source='tnsuhak/xjtlu-korea main index.html'),dict(id='australia-chat',label='호주 오픈채팅',detail='1,600명+ 참여중',url='https://open.kakao.com/o/gvHG0TYf',source='TNS Australia Kakao Open Chat · user-confirmed',last_verified='2026-09-26',participant_count_floor=1600),dict(id='cafe',label='네이버 카페',detail='TNS 유학 커뮤니티',url='https://cafe.naver.com/tnsuhak.cafe',source='tnsuhak/xjtlu-korea main index.html')])
(ROOT/'data/site.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(f'{len(universities)} universities / {len(programs)} programs / {len(routes)} routes / {len(sources)} sources')

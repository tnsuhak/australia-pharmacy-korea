"""Static/data QA. Does not claim a real viewport or browser interaction test."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,collections,subprocess,os,re
R=Path(__file__).resolve().parents[1];D=json.loads((R/'data/catalog.json').read_text());KD=json.loads((R/'data/korea_pharmacist.json').read_text());REG=json.loads((R/'data/pharmacist_registration.json').read_text());errors=[]
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=[];self.tags=[];self.scripts=[];self.in_script=False;self.script='';self.title='';self.in_title=False;self.h1=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.append(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='title':self.in_title=True
  if tag=='script':self.in_script=a.get('type') in ['application/json','application/ld+json'];self.script=''
 def handle_endtag(self,tag):
  if tag=='title':self.in_title=False
  if tag=='script' and self.in_script:self.scripts.append(self.script);self.in_script=False
 def handle_data(self,data):
  if self.in_title:self.title+=data
  if self.in_script:self.script+=data
pages={p:Page(p.read_text()) for p in (R/'dist').rglob('index.html')};titles=[];descriptions=[]
for path,p in pages.items():
 rel=str(path.relative_to(R/'dist'));titles.append(p.title)
 if p.h1!=1:errors.append(f'{rel}: H1 count {p.h1}')
 dup=[k for k,n in collections.Counter(p.ids).items() if n>1]
 if dup:errors.append(f'{rel}: duplicate IDs {dup}')
 for script in p.scripts:
  try:json.loads(script)
  except Exception as e:errors.append(f'{rel}: JSON invalid {e}')
 metas=[a for t,a in p.tags if t=='meta']
 ds=[a['content'] for a in metas if a.get('name')=='description'];descriptions+=ds
 if len(ds)!=1:errors.append(f'{rel}: description missing/duplicate')
 if not any(a.get('name')=='robots' and 'noindex' in a.get('content','') for a in metas):errors.append(f'{rel}: preview indexing enabled')
 if not any(t=='link' and a.get('rel')=='canonical' for t,a in p.tags):errors.append(f'{rel}: missing canonical')
 for tag,a in p.tags:
  url=a.get('href') if tag in ['a','link'] else a.get('src') if tag=='script' else None
  if not url:continue
  u=urlsplit(url)
  if u.scheme in ['https','http','tel','mailto']:
   if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):errors.append(f'{rel}: unsafe external target')
   if tag=='a' and any(x in url.lower() for x in ['applyonline','apply.unsw','applicationportal']):errors.append(f'{rel}: application portal link')
   continue
  target=R/'dist'/unquote(u.path.lstrip('/')) if u.path.startswith('/') else path.parent/unquote(u.path) if u.path else path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{rel}: missing internal URL {url}');continue
  if u.fragment and target.suffix=='.html':
   dest=pages.get(target) or Page(target.read_text())
   if unquote(u.fragment) not in dest.ids:errors.append(f'{rel}: missing anchor {url}')
for name,seq in [('title',titles),('description',descriptions)]:
 if len(set(seq))!=len(seq):errors.append(f'duplicate {name}')
if 'Disallow: /' not in (R/'dist/robots.txt').read_text():errors.append('preview robots is not blocked')
if 'noindex' not in (R/'dist/_headers').read_text():errors.append('preview HTTP noindex missing')
if not (R/'assets/og-image.png').exists():errors.append('OG raster asset missing')
public_copy_banned=['자동판정','legacy P6001','live page','승격하지','자료를 대조 중']
for path in pages:
 text=path.read_text()
 for phrase in public_copy_banned:
  if phrase in text:errors.append(f'{path.relative_to(R/"dist")}: developer-style public copy remains: {phrase}')
compact_batch={
 'jcu-pharmacy':(1,['JCU 약대 과정 구조','904시간 Placement','ATAR / Rank 76','IELTS 7.0 · 각 6.5','2027년 2월','2026 A$31,710 참고','자동심사 · 25%','3년 커리큘럼·실습','호주 약사등록 방법 →']),
 'utas-pharmacy':(3,['UTas 약대 과정 구조','최소 400시간 PEP','수능 305','한국 고2 60%','한국 고2 65% + General Mathematics','2027년 2월 22일 · 6월 21일 · 10월 11일','A$61,267 / 년','자동심사 · 30%','3년 커리큘럼·실습']),
 'curtin-pharmacy':(2,['커틴 약대 과정 구조','3년 9개월','1학년 Diploma (Pharmacy) → 약대 2학년','한국 고3 Rank 6 또는 수능 280/600','Stage 2 · 2월','A$44,900','자동심사 · 20%','Professional internship']),
 'griffith-pharmacy':(3,['그리피스 약대 과정 구조','입학방법 3가지','2027 Rank 76','수능 331','고2 → Foundation → 1학년 Diploma (Health Sciences) → 약대 2학년','한국 고2 Rank 7 · 수능 260 · 검정고시 평균 70','IELTS 5.5 · 각 5.0','3월 · 6월 · 10월','1학년 Diploma (Health Sciences) → 약대 2학년','한국 고3 Rank 6 또는 수능 280','2027년 3월 1일 · 6월 27일 · 10월 5일','자동심사 · 20%','A$329.85 / 주부터'])
}
for slug,(route_count,phrases) in compact_batch.items():
 page=R/f'dist/universities/{slug}/index.html'
 if not page.exists():
  errors.append(f'{slug}: compact detail page missing')
  continue
 txt=page.read_text()
 for phrase in phrases:
  if phrase not in txt:errors.append(f'{slug}: compact detail missing {phrase}')
 for label in ['입학조건','영어','입학시기']:
  if txt.count(f'<small>{label}</small>')<route_count:
   errors.append(f'{slug}: pathway cards not standardized for {label}')
 for old_heading in ['<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in txt:errors.append(f'{slug}: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in txt:errors.append(f'{slug}: per-school cost calculator should not render')
compact_batch_2={
 'uq-pharmacy':(3,['UQ 약대 과정 구조','입학방법 3가지','ATAR 80 · IB 30.25','수능 260 · 검정고시 65% · 고2 GPA 3(미)','수능 270 · 검정고시 70% · 고3 GPA 4(우)','A$60,952 / 년','A$36,280','A$24,940','경쟁선발 · 25%']),
 'adelaide-pharmacy':(3,['Adelaide 약대 과정 구조','입학방법 3가지','수능 340 · IB 30 · A-Level 10 · SAT 1220 · OSSD 80%','고2 → Foundation → 약대 1학년','IELTS 5.5 · 각 5.0','1학년 Diploma (Health Science) → 약대 1학년','IELTS 6.0 · 각 6.0','A$36,200','A$41,900','4년 과정·5년 Master 연계','자동심사 · 15%','A$320 / 주','A$380 / 주']),
 'latrobe-pharmacy':(2,['La Trobe 약대 과정 구조','Bendigo','별도 과학 선수과목 없음','Foundation → 약대 1학년','IELTS 6.5 · 각 6.5','Health Innovation','30%','A$255 / 주부터']),
 'qut-pharmacy':(3,['QUT 약대 과정 구조','Selection Rank 76','선행지식','12개월 Foundation → 약대 1학년','6개월 Intensive → 약대 1학년','A$46,200 / 년','자동심사 · 25%','A$25,536','A$12,768'])
}
for slug,(route_count,phrases) in compact_batch_2.items():
 page=R/f'dist/universities/{slug}/index.html'
 if not page.exists():
  errors.append(f'{slug}: compact batch 2 page missing')
  continue
 txt=page.read_text()
 for phrase in phrases:
  if phrase not in txt:errors.append(f'{slug}: compact batch 2 missing {phrase}')
 for label in ['입학조건','영어','입학시기']:
  if txt.count(f'<small>{label}</small>')<route_count:
   errors.append(f'{slug}: pathway cards not standardized for {label}')
 routes_match=re.search(r'<section class="article-section" id="routes">.*?</section>',txt,re.S)
 if routes_match:
  rt=routes_match.group(0)
  if '<p class="monash-route-meta">' in rt:errors.append(f'{slug}: pathway card secondary microcopy remains')
  if any('<span' in criteria for criteria in re.findall(r'<div class="route-criteria">(.*?)</div></article>',rt,re.S)):errors.append(f'{slug}: pathway criteria still contains secondary small copy')
  for clutter in ['(2026 공식 참고)','(국제학력은 2026 공식 참고)']:
   if clutter in rt:errors.append(f'{slug}: source-year card clutter remains {clutter}')
 for old_heading in ['<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in txt:errors.append(f'{slug}: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in txt:errors.append(f'{slug}: per-school cost calculator should not render')


compact_batch_3={
 'rmit-pharmacy':(3,['RMIT 약대 과정 구조','2027 A$49,920','한국 고교 75% 또는 고교 졸업 + 수능 300','Foundation → 약대 1학년','IELTS 5.5 · 각 5.0','2년 Associate Degree (Biomedicine) → 약대 2학년','A$34,250','A$38,400 / 년','약대 신입생 장학금','4년 과정과 졸업 후']),
 'newcastle-pharmacy':(2,['Newcastle 약대 과정 구조','A$51,665','IB 28','준비 기준 IELTS 7.0 · 각 7.0','고2 → Foundation → 약대 1학년','한국 고2 수료','A&amp;B 평균 75%','A$31,400','Pharmacy 제외','공식자료 두 기준이 함께 공개 중','Regional Category 2']),
 'canberra-pharmacy':(1,['Canberra 약대 과정 구조','Selection Rank 75','Biology/Human Movement + Chemistry/Physics 선행지식','IELTS 7.0 · 각 7.0','2027년 2월 15일','2027 국제학생 학비','A$42,500 / 년','2026 Annual Fee','자동심사 · 10~30%','Regional Category 2']),
 'unisq-pharmacy':(1,['UniSQ 약대 과정 구조','2027은 4년','2028부터 3년 Accelerated','온라인 이론 + 캠퍼스 집중수업','Mathematics + Biology/Chemistry/Physics 중 1과목 선행지식','Writing 6.5','2027년 2월 15일','A$34,280 / 년','자동심사 · 10%','Regional Category 3'])
}
for slug,(route_count,phrases) in compact_batch_3.items():
 page=R/f'dist/universities/{slug}/index.html'
 if not page.exists():
  errors.append(f'{slug}: compact batch 3 page missing')
  continue
 txt=page.read_text()
 for phrase in phrases:
  if phrase not in txt:errors.append(f'{slug}: compact batch 3 missing {phrase}')
 for label in ['입학조건','영어','입학시기']:
  if txt.count(f'<small>{label}</small>')<route_count:
   errors.append(f'{slug}: pathway cards not standardized for {label}')
 routes_match=re.search(r'<section class="article-section" id="routes">.*?</section>',txt,re.S)
 if routes_match:
  rt=routes_match.group(0)
  if '<p class="monash-route-meta">' in rt:errors.append(f'{slug}: pathway card secondary microcopy remains')
  if any('<span' in criteria for criteria in re.findall(r'<div class="route-criteria">(.*?)</div></article>',rt,re.S)):errors.append(f'{slug}: pathway criteria still contains secondary small copy')
  for clutter in ['(2026 공식 참고)','(국제학력은 2026 공식 참고)']:
   if clutter in rt:errors.append(f'{slug}: source-year card clutter remains {clutter}')
 for old_heading in ['<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in txt:errors.append(f'{slug}: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in txt:errors.append(f'{slug}: per-school cost calculator should not render')

rmit_direct=next((x for x in D['entry_routes'] if x['id']=='rmit-bpharm-hons-direct'),None)
rmit_foundation=next((x for x in D['entry_routes'] if x['id']=='rmit-foundation'),None)
rmit_associate=next((x for x in D['entry_routes'] if x['id']=='rmit-associate'),None)
if not rmit_direct or '수능 300' not in str(rmit_direct['qualification']['value']) or 'Chemistry + Mathematics' not in str(rmit_direct['qualification']['value']):
 errors.append('rmit-data: Direct Korea score/prerequisites missing')
if not rmit_foundation or rmit_foundation.get('pathway_fee',{}).get('value')!=34250 or rmit_foundation['entry_year']['value']!=1:
 errors.append('rmit-data: 2027 Foundation fee/destination missing')
if not rmit_associate or rmit_associate.get('pathway_fee',{}).get('value')!=38400 or rmit_associate['entry_year']['value']!=2:
 errors.append('rmit-data: Associate pathway fee/Pharmacy Year 2 destination missing')

newcastle_tuition=next((x for x in D['tuition'] if x['program_id']=='newcastle-bpharm-hons'),None)
newcastle_english=next((x for x in D['english'] if x['program_id']=='newcastle-bpharm-hons'),None)
newcastle_foundation=next((x for x in D['entry_routes'] if x['id']=='newcastle-foundation'),None)
if not newcastle_tuition or newcastle_tuition['annual']['value']!=51665 or newcastle_tuition['annual']['status']!='confirmed_2027':
 errors.append('newcastle-data: 2027 tuition must remain A$51,665 confirmed')
if not newcastle_english or newcastle_english['ielts_overall']['status']!='source_conflict':
 errors.append('newcastle-data: English conflict must remain explicit')
if not newcastle_foundation or newcastle_foundation.get('pathway_fee',{}).get('value')!=31400 or 'Academic English A&B' not in str(newcastle_foundation['progression']['value']):
 errors.append('newcastle-data: Foundation fee/progression missing')

canberra_tuition=next((x for x in D['tuition'] if x['program_id']=='canberra-bpharm-hons'),None)
if not canberra_tuition or canberra_tuition['annual']['value']!=42500 or canberra_tuition['annual']['source_year']!=2026 or canberra_tuition['annual']['status']=='confirmed_2027':
 errors.append('canberra-data: A$42,500 must remain a 2026 reference, not 2027 tuition')

unisq_program=next((x for x in D['programs'] if x['id']=='unisq-bpharm-hons'),None)
unisq_tuition=next((x for x in D['tuition'] if x['program_id']=='unisq-bpharm-hons'),None)
if not unisq_program or unisq_program['duration_years']['value']!=4 or unisq_program['duration_years']['source_year']!=2027:
 errors.append('unisq-data: 2027 international Pharmacy must remain 4 years')
if not unisq_tuition or unisq_tuition['annual']['value']!=34280 or unisq_tuition['annual']['source_year']!=2026:
 errors.append('unisq-data: A$34,280 must remain a 2026 fee reference')


compact_batch_4={
 'sydney-pharmacy':(3,['Sydney 약대 과정 구조','5년 통합','4년 BPharm(Hons) Exit','수능 346 · IB 31 · A-Level 14 · SAT 1300','12개월 Foundation → 약대 1학년','9개월 Intensive Foundation → 약대 1학년','GPA 7.3 + English C + Mathematics','A$63,600 / 년','A$49,800','A$47,690','Sydney International Student Award','20%','Master + supervised practice + ITP']),
 'unsw-pharmacy':(2,['UNSW 약대 과정 구조','2027년부터 Bachelor of Pharmaceutical Medicine / Doctor of Pharmacy','International ATAR 87 · IB 33 · A-Level 15','IELTS 7.0 · 각 6.0','9개월 Standard Foundation → 약대 1학년','GPA 7.6 + Academic English B + Science','A$63,000 / 년','A$43,650','한국 국적 대상 아님','과정명 변경 확인사항','5년 PharmD 과정·실습']),
 'uwa-pharmacy':(3,['UWA 약대 과정 구조','4년 Bachelor + PharmD','수능 329 · IB 30 · A-Level 10 · SAT 1220','8개월 Foundation → 통합과정 1학년','수능 260 · 고2 70% · 고3 60%','12개월 Foundation → 통합과정 1학년','수능 230 · 고2 65% · 고3 60%','IELTS 7.0 · 각 7.0','A$46,000 / 년','자동심사 · 10% / 20%','WAM 65%','Regional Category 2'])
}
for slug,(route_count,phrases) in compact_batch_4.items():
 page=R/f'dist/universities/{slug}/index.html'
 if not page.exists():
  errors.append(f'{slug}: compact batch 4 page missing')
  continue
 txt=page.read_text()
 for phrase in phrases:
  if phrase not in txt:errors.append(f'{slug}: compact batch 4 missing {phrase}')
 for label in ['입학조건','영어','입학시기']:
  if txt.count(f'<small>{label}</small>')<route_count:
   errors.append(f'{slug}: pathway cards not standardized for {label}')
 routes_match=re.search(r'<section class="article-section" id="routes">.*?</section>',txt,re.S)
 if routes_match:
  rt=routes_match.group(0)
  if '<p class="monash-route-meta">' in rt:errors.append(f'{slug}: pathway card secondary microcopy remains')
  if any('<span' in criteria for criteria in re.findall(r'<div class="route-criteria">(.*?)</div></article>',rt,re.S)):errors.append(f'{slug}: pathway criteria still contains secondary small copy')
  for clutter in ['(2026 공식 참고)','(2025 공식 참고)','(국제학력은 2026 공식 참고)']:
   if clutter in rt:errors.append(f'{slug}: source-year card clutter remains {clutter}')
 for old_heading in ['<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in txt:errors.append(f'{slug}: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in txt:errors.append(f'{slug}: per-school cost calculator should not render')

sydney_direct=next((x for x in D['entry_routes'] if x['id']=='sydney-bpharm-hons-direct'),None)
sydney_std=next((x for x in D['entry_routes'] if x['id']=='sydney-usfp'),None)
sydney_int=next((x for x in D['entry_routes'] if x['id']=='sydney-usfp-intensive'),None)
sydney_tuition=next((x for x in D['tuition'] if x['program_id']=='sydney-bpharm-hons'),None)
sydney_reg=next((x for x in D['professional_registration'] if x['program_id']=='sydney-bpharm-hons'),None)
if not sydney_direct or 'CSAT 346' not in str(sydney_direct['qualification']['value']) or 'Mathematics prerequisite' not in str(sydney_direct['qualification']['value']):
 errors.append('sydney-data: 2027 Direct score/Mathematics requirement missing')
if not sydney_std or sydney_std.get('pathway_fee',{}).get('value')!=49800 or not sydney_int or sydney_int.get('pathway_fee',{}).get('value')!=47690:
 errors.append('sydney-data: 2027 USFP Standard/Intensive fees missing')
if not sydney_tuition or sydney_tuition['annual']['value']!=63600 or sydney_tuition['annual']['status']!='confirmed_2027':
 errors.append('sydney-data: 2027 Pharmacy tuition must remain A$63,600 confirmed')
if not sydney_reg or sydney_reg['itp_in_degree']['value'] is not True or sydney_reg['post_graduation_internship']['value'] is not False:
 errors.append('sydney-data: integrated ITP/supervised practice must remain distinct from post-graduation internship')

unsw_direct=next((x for x in D['entry_routes'] if x['id']=='unsw-bpharm-hons-direct'),None)
unsw_foundation=next((x for x in D['entry_routes'] if x['id']=='unsw-foundation-standard'),None)
unsw_tuition=next((x for x in D['tuition'] if x['program_id']=='unsw-bpharm-hons'),None)
unsw_program=next((x for x in D['programs'] if x['id']=='unsw-bpharm-hons'),None)
if not unsw_direct or 'IB 33' not in str(unsw_direct['qualification']['value']) or 'assumed knowledge' not in str(unsw_direct['qualification']['value']):
 errors.append('unsw-data: 2027 IB 33 / assumed knowledge Direct data missing')
if not unsw_foundation or unsw_foundation.get('pathway_fee',{}).get('value')!=43650 or 'GPA 7.6' not in str(unsw_foundation['progression']['value']):
 errors.append('unsw-data: 2027 Standard Foundation fee/progression missing')
if not unsw_tuition or unsw_tuition['annual']['value']!=63000 or unsw_tuition['annual']['source_year']!=2026 or unsw_tuition['annual']['status']=='confirmed_2027':
 errors.append('unsw-data: A$63,000 must remain a 2026 fee reference, not 2027 tuition')
if not unsw_program or 'Doctor of Pharmacy' not in str(unsw_program['name']['value']) or 'Doctor of Pharmacy' not in str(unsw_program['accreditation']['note']):
 errors.append('unsw-data: 2027 PharmD naming/regulator follow-up must remain explicit')

uwa_direct=next((x for x in D['entry_routes'] if x['id']=='uwa-bpharm-hons-direct'),None)
uwa_f8=next((x for x in D['entry_routes'] if x['id']=='uwa-foundation-8'),None)
uwa_f12=next((x for x in D['entry_routes'] if x['id']=='uwa-foundation-12'),None)
uwa_tuition=next((x for x in D['tuition'] if x['program_id']=='uwa-bpharm-hons'),None)
uwa_sch=next((x for x in D['scholarships'] if x['id']=='uwa-global-excellence'),None)
if not uwa_direct or 'CSAT 329' not in str(uwa_direct['qualification']['value']) or 'WAM 65%' not in str(uwa_direct['progression']['value']):
 errors.append('uwa-data: Direct CSAT 329 / WAM 65 assurance missing')
if not uwa_f8 or 'CSAT 260' not in str(uwa_f8['qualification']['value']) or uwa_f8['english']['value']!='IELTS 6.0 / 각 5.5':
 errors.append('uwa-data: 8-month Foundation Korea/English criteria missing')
if not uwa_f12 or 'CSAT 230' not in str(uwa_f12['qualification']['value']) or uwa_f12['english']['value']!='IELTS 5.5 / 각 5.0':
 errors.append('uwa-data: 12-month Foundation Korea/English criteria missing')
if not uwa_tuition or uwa_tuition['annual']['value']!=46000 or uwa_tuition['annual']['source_year']!=2026:
 errors.append('uwa-data: A$46,000 must remain a 2026 fee reference')
if not uwa_sch or uwa_sch['amount']['value']!=[10,20] or uwa_sch['pharmacy_eligible']['value'] is not True or uwa_sch['automatic_assessment']['value'] is not True:
 errors.append('uwa-data: 2027 Global Excellence 10/20% Pharmacy eligibility missing')

adelaide_foundation=next((x for x in D['entry_routes'] if x['id']=='adelaide-eynesbury-foundation'),None)
adelaide_diploma=next((x for x in D['entry_routes'] if x['id']=='adelaide-eynesbury-diploma'),None)
if not adelaide_foundation or adelaide_foundation['entry_year']['value']!=1 or adelaide_foundation['pathway_fee']['value']!=36200:
 errors.append('adelaide-data: Eynesbury Foundation pathway missing or wrong')
if not adelaide_diploma or adelaide_diploma['entry_year']['value']!=1 or adelaide_diploma['credit']['value']!=4 or adelaide_diploma['pathway_fee']['value']!=41900:
 errors.append('adelaide-data: Health Science Diploma pathway must remain Pharmacy Year 1 with 4 courses credit')
adelaide_csat=next((x for x in D['qualifications'] if x['program_id']=='adelaide-bpharm-hons' and x['qualification']=='csat'),None)
if not adelaide_csat or adelaide_csat['score']['value']!=340:
 errors.append('adelaide-data: current official South Korea CSAT must be 340')
uq_std=next((x for x in D['entry_routes'] if x['id']=='uq-standard-2027-entry'),None)
uq_acc=next((x for x in D['entry_routes'] if x['id']=='uq-accelerated'),None)
if not uq_std or '수능 260' not in str(uq_std['qualification']['value']) or uq_std['english']['value']!='IELTS 5.5 · 각 5.0':
 errors.append('uq-data: Standard Foundation Korea entry/English missing')
if not uq_acc or '수능 270' not in str(uq_acc['qualification']['value']) or 'Writing 6.0' not in str(uq_acc['english']['value']):
 errors.append('uq-data: Accelerated Foundation Korea entry/English missing')
latrobe_foundation=next((x for x in D['entry_routes'] if x['id']=='latrobe-foundation'),None)
if not latrobe_foundation or latrobe_foundation['entry_year']['value']!=1 or 'Year 11' not in str(latrobe_foundation['qualification']['value']):
 errors.append('latrobe-data: Foundation to Pharmacy Year 1 route missing')
qut_direct=next((x for x in D['entry_routes'] if x['id']=='qut-bpharm-hons-direct'),None)
if not qut_direct or 'Selection Rank 76' not in str(qut_direct['qualification']['value']) or 'assumed knowledge' not in str(qut_direct['qualification']['value']):
 errors.append('qut-data: Rank 76 / assumed knowledge distinction missing')

griffith_page=R/'dist/universities/griffith-pharmacy/index.html'
if griffith_page.exists():
 gt=griffith_page.read_text()
 for phrase in ['(국제학력은 2026 공식 참고)','(2026 공식 참고)']:
  if phrase in gt:errors.append(f'griffith-pharmacy: unnecessary source-year parenthetical remains {phrase}')
for slug in ['jcu-pharmacy','utas-pharmacy','curtin-pharmacy','griffith-pharmacy']:
 page=R/f'dist/universities/{slug}/index.html'
 if page.exists():
  txt=page.read_text()
  routes_match=re.search(r'<section class="article-section" id="routes">.*?</section>',txt,re.S)
  if routes_match:
   rt=routes_match.group(0)
   if '<p class="monash-route-meta">' in rt:
    errors.append(f'{slug}: pathway card secondary microcopy remains')
   if re.search(r'<div class="route-criteria">.*?<span>',rt,re.S):
    errors.append(f'{slug}: pathway criteria still contains secondary small copy')
griffith_foundation=next((x for x in D['entry_routes'] if x['id']=='griffith-foundation'),None)
if not griffith_foundation:
 errors.append('griffith-data: Foundation pathway missing')
else:
 if griffith_foundation['availability']['value'] is not True:errors.append('griffith-data: Foundation pathway should be confirmed')
 if '고2 4개 학업과목 평균 Rank 7' not in str(griffith_foundation['qualification']['value']):errors.append('griffith-data: Korea Foundation entry criteria missing')
 if griffith_foundation['english']['value']!='IELTS 5.5 · 각 5.0':errors.append('griffith-data: Foundation English mismatch')
 if griffith_foundation.get('destination_label')!='1학년 Diploma → 약대 2학년':errors.append('griffith-data: Foundation destination must show Diploma before Pharmacy Year 2')
 if 'Foundation → Diploma of Health Sciences → Pharmacy 2학년' not in str(griffith_foundation['progression']['value']):errors.append('griffith-data: Foundation must not be shown as direct Pharmacy Year 1')
monash_page=R/'dist/universities/monash-pharmacy/index.html'
if not monash_page.exists():
 errors.append('monash-page: compact pilot page missing')
else:
 mt=monash_page.read_text()
 for phrase in ['모나쉬 약대 과정 구조','입학방법 3가지','수능 350','한국 내신 86%','A-Level 12','IB 33','AP 8','SAT 1290','한국 고교 60% 또는 수능 260','관련 학사 · 최근 10년 이내 · 평균 70%+','Higher-level Maths','Human Physiology','1월 초 Summer intensive 시작','5년 커리큘럼 한눈에 보기','2~3학년','유급 실무훈련 + ITP','과정 전반의 핵심 역량','2027 국제학생 학비','A$63,640','일반 국제학생 Merit','A$15,000 / 년','Leadership','학비 100%','약대 전용 25%·50% 장학','2027 신설 PharmD 적용 확인 중','일반 신입생에게 확정 적용되는 장학금으로 표시하지 않습니다.','5년 과정과 졸업 후','4년 후 학사로 졸업 가능']:
  if phrase not in mt:errors.append(f'monash-page: compact pilot missing {phrase}')
 for label in ['입학조건','영어','입학시기']:
  if mt.count(f'<small>{label}</small>')<3:errors.append(f'monash-page: pathway cards not standardized for {label}')
 routes_match=re.search(r'<section class="article-section" id="routes">.*?</section>',mt,re.S)
 if routes_match:
  rt=routes_match.group(0)
  if '<p class="monash-route-meta">' in rt:errors.append('monash-page: pathway card secondary microcopy remains')
  if any('<span' in criteria for criteria in re.findall(r'<div class="route-criteria">(.*?)</div></article>',rt,re.S)):errors.append('monash-page: pathway criteria still contains secondary small copy')
 visible_mt=re.sub(r'<script\b.*?</script>|<style\b.*?</style>', '', mt, flags=re.I|re.S)
 visible_mt=re.sub(r'<[^>]+>', ' ', visible_mt)
 for code in ['P6007','P6001']:
  if code in visible_mt:errors.append(f'monash-page: internal course code leaked into student-facing visible copy {code}')
 if 'A$49,740' in mt:errors.append('monash-page: domestic full-fee incorrectly shown as international tuition')
 if '2026 공식 A$60,100' in mt:errors.append('monash-page: old 2026 fee reference remains after 2027 fee confirmation')
 for old_heading in ['<h2>과정·학위 구조</h2>','<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in mt:errors.append(f'monash-page: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in mt:errors.append('monash-page: duplicated cost calculator should not render')
monash_direct=next((x for x in D['entry_routes'] if x['id']=='monash-bpharm-hons-direct'),None)
if not monash_direct or not monash_direct.get('direct_scores'):
 errors.append('monash-data: detailed Direct score set missing')
else:
 expected={'csat':350,'korean_high_school':86,'alevel':12,'ib':33,'ap':8,'sat':1290}
 for key,val in expected.items():
  if monash_direct['direct_scores'].get(key,{}).get('value')!=val:
   errors.append(f'monash-data: Direct score mismatch {key}')
monash_foundation=next((x for x in D['entry_routes'] if x['id']=='monash-foundation'),None)
if not monash_foundation or '한국 고교 60% 또는 수능 260' not in str(monash_foundation['qualification'].get('value')) or 'Foundation 75%' not in str(monash_foundation['progression'].get('value')):
 errors.append('monash-data: Foundation Korea entry/progression criteria missing')
monash_grad=next((x for x in D['entry_routes'] if x['id']=='monash-ge'),None)
if not monash_grad or '70%' not in str(monash_grad['progression'].get('value')) or 'Human Physiology' not in str(monash_grad['progression'].get('value')):
 errors.append('monash-data: Graduate Entry criteria missing')
monash_tuition=next((x for x in D['tuition'] if x['program_id']=='monash-bpharm-hons'),None)
if not monash_tuition or monash_tuition['annual']['value']!=63640 or monash_tuition['annual']['source_year']!=2027 or monash_tuition['annual']['status']!='confirmed_2027':
 errors.append('monash-data: 2027 international tuition must be official A$63,640 per 48 credit points')
monash_scholarships={x['id']:x for x in D['scholarships'] if x['university_id']=='monash'}
if monash_scholarships.get('monash-merit',{}).get('scope')!='p6007_not_confirmed' or monash_scholarships.get('monash-merit',{}).get('pharmacy_eligible',{}).get('value') is not None:
 errors.append('monash-data: 25/50% Pharmacy scholarship must remain pending for P6007 until officially listed')
for sid in ['monash-international-merit','monash-international-leadership']:
 if sid not in monash_scholarships or monash_scholarships[sid]['pharmacy_eligible']['value'] is not True:
  errors.append(f'monash-data: missing verified general international scholarship {sid}')
registration_page=R/'dist/pharmacist-registration/index.html'
if not registration_page.exists():
 errors.append('pharmacist-registration: page missing')
else:
 rt=registration_page.read_text()
 for phrase in ['호주 약사 되는 법','현재 1,575시간','1,181시간','75%','시험 2개','필기 2시간','구술 35분','75문항','3파트','18개월 안에 모두 합격','A$1,279','약 A$2,409','약 A$2,514','정식 약사등록','인턴약사 등록 + 근무처·지도약사 승인','인턴 교육과정 (ITP)','기존 표준 1,824시간 · 현재 운영 1,575시간','고정 합격점(예: 65%)은 공개하지 않습니다.','모든 학생이 IELTS를 다시 보는 것은 아닙니다.','한국은 Ahpra의 인정국가 목록에 포함되지 않기 때문에','Cambridge C1 Advanced','Cambridge C2 Proficiency','현재 공개 2025/26']:
  if phrase not in rt:errors.append(f'pharmacist-registration: missing {phrase}')
 for obsolete in ['총 1,824시간</strong>','75% = 1,368시간','1,368시간 · 전체의 75%','4주 동안 인정되는 시간</th><td>최소 80시간','Approved preceptor 단위']:
  if obsolete in rt:errors.append(f'pharmacist-registration: obsolete current-rule copy remains {obsolete}')
 if '합격점 65%' in rt:
  errors.append('pharmacist-registration: obsolete fixed 65% pass mark rendered as current')
if REG['supervised_practice']['total_hours']!=1575 or REG['supervised_practice']['registration_standard_hours']!=1824 or REG['supervised_practice']['exam_eligibility_hours']!=1181:
 errors.append('pharmacist-registration-data: current variation / underlying standard hours wrong')
if REG['supervised_practice'].get('waived_requirements') is None or len(REG['supervised_practice']['waived_requirements'])<2:
 errors.append('pharmacist-registration-data: current internship waivers not recorded')
if REG['written_exam']['questions']!=75 or REG['written_exam']['duration_minutes']!=120 or REG['written_exam']['fee_aud']!=790:
 errors.append('pharmacist-registration-data: written exam structure/fee wrong')
if sum(x['minutes'] for x in REG['oral_exam']['parts'])!=35 or REG['oral_exam']['fee_aud']!=489:
 errors.append('pharmacist-registration-data: oral exam structure/fee wrong')
pte=next((x for x in REG['english']['tests'] if x['test']=='PTE Academic'),None)
ielts=next((x for x in REG['english']['tests'] if x['test']=='IELTS Academic'),None)
c1=next((x for x in REG['english']['tests'] if x['test']=='Cambridge C1 Advanced'),None)
c2=next((x for x in REG['english']['tests'] if x['test']=='Cambridge C2 Proficiency'),None)
if not pte or pte['overall']!='63' or pte['speaking']!='76':
 errors.append('pharmacist-registration-data: current PTE scores wrong')
if not ielts or ielts['overall']!='7.0' or ielts['writing']!='6.5':
 errors.append('pharmacist-registration-data: current IELTS registration scores wrong')
if not c1 or c1['overall']!='178' or c1['speaking']!='194':
 errors.append('pharmacist-registration-data: Cambridge C1 scores wrong')
if not c2 or c2['overall']!='185' or c2['writing']!='176':
 errors.append('pharmacist-registration-data: Cambridge C2 scores wrong')
if REG['fees']['exam_total_aud'] != REG['written_exam']['fee_aud'] + REG['oral_exam']['fee_aud']:
 errors.append('pharmacist-registration-data: exam fee total mismatch')
if REG['fees'].get('national_regulatory_exam_total_aud')!=2409 or REG['fees'].get('nsw_regulatory_exam_total_aud')!=2514:
 errors.append('pharmacist-registration-data: current published fee totals wrong')

korea_page=R/'dist/korea-pharmacist/index.html'
if not korea_page.exists():
 errors.append('korea-pharmacist: page missing')
else:
 kt=korea_page.read_text()
 if len(KD.get('recognized_schools',[]))!=13:errors.append('korea-pharmacist: recognized Australia school count is not 13')
 for school in KD.get('recognized_schools',[]):
  if school['en'] not in kt:errors.append(f'korea-pharmacist: missing recognized school {school["en"]}')
 for phrase in ['보건복지부장관 인정 호주 약대 13곳','Adelaide University는 기존 UniSA 인정과 자동으로 같지 않습니다.','2026. 6. 28.(일)','220,000원','2027. 1. 21.(목)','약학 기초','생명약학','각 과목 만점의 40% 이상 + 전 과목 총점의 60% 이상']:
  if phrase not in kt:errors.append(f'korea-pharmacist: missing exam/recognition content {phrase}')
ids={p['id'] for p in D['programs']}
for coll in ['requirements','english','tuition','intakes','professional_registration']:
 if {r['program_id'] for r in D[coll]}!=ids:errors.append(f'{coll}: program coverage differs')
for collection in ['programs','universities','entry_routes','qualifications','scholarships','accommodation','sources']:
 i=[x['id'] for x in D[collection]]
 if len(set(i))!=len(i):errors.append(f'{collection}: duplicate record IDs')
count=0;states=collections.Counter()
def facts(obj,path=''):
 global count
 if isinstance(obj,dict):
  if 'value' in obj and 'status' in obj:
   count+=1;states[obj['status']]+=1
   for key in ['academic_year','source_year','source_url','source_type','verified_date']:
    if key not in obj:errors.append(f'{path}: fact missing {key}')
   if obj['value'] is not None and obj['status'] in ['confirmed_2027','latest_published'] and not all(obj.get(k) for k in ['source_url','source_type','verified_date']):errors.append(f'{path}: asserted value missing provenance')
   if obj['status']=='confirmed_2027' and obj['source_year']!=2027:errors.append(f'{path}: false 2027 label')
  for k,v in obj.items():facts(v,path+'.'+k)
 elif isinstance(obj,list):
  for i,v in enumerate(obj):facts(v,path+f'[{i}]')
facts(D)
gate=subprocess.run(['python3','scripts/build.py'],cwd=R,env={**os.environ,'CONTEXT':'production','PRODUCTION_APPROVED':'false'},capture_output=True,text=True)
if gate.returncode==0:errors.append('unapproved production build unexpectedly succeeded')
summary=dict(status='passed' if not errors else 'failed',static_pages=len(pages),facts=count,fact_statuses=dict(states),errors=errors,production_gate='blocked' if gate.returncode else 'FAILED',browser_qa='not_run: cloud browser rejected file URL; remote deploy preview unavailable',mobile_qa='CSS responsive rules implemented; real viewport QA not run',desktop_qa='static checks only; visual QA not run')
(R/'docs/qa-results.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2));raise SystemExit(1 if errors else 0)

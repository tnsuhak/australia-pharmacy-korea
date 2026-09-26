"""Static/data QA. Does not claim a real viewport or browser interaction test."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,collections,subprocess,os,re
R=Path(__file__).resolve().parents[1];D=json.loads((R/'data/catalog.json').read_text());KD=json.loads((R/'data/korea_pharmacist.json').read_text());errors=[]
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
 'curtin-pharmacy':(2,['커틴 약대 과정 구조','3년 9개월','Pharmacy Diploma → 약대 2학년','한국 고3 Rank 6 또는 수능 280/600','Stage 2 · 2월','A$44,900','자동심사 · 20%','Professional internship']),
 'griffith-pharmacy':(2,['그리피스 약대 과정 구조','2027 Rank 76','수능 331','Diploma of Health Sciences → 약대 2학년','한국 고3 Rank 6 또는 수능 280','2027년 3월 1일 · 6월 27일 · 10월 5일','자동심사 · 20%','A$329.85 / 주부터'])
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
  if re.search(r'<div class="route-criteria">.*?<span>',rt,re.S):errors.append('monash-page: pathway criteria still contains secondary small copy')
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

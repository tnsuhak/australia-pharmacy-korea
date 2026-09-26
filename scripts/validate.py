"""Static/data QA. Does not claim a real viewport or browser interaction test."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,collections,subprocess,os
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
monash_page=R/'dist/universities/monash-pharmacy/index.html'
if not monash_page.exists():
 errors.append('monash-page: compact pilot page missing')
else:
 mt=monash_page.read_text()
 for phrase in ['모나쉬 약대 과정 구조','입학방법 3가지','5년 커리큘럼 한눈에 보기','2~3학년','유급 실무훈련 + ITP','과정 전반의 핵심 역량','2027 국제학생 학비','2026 공식 A$60,100','일반 국제학생 Merit','A$15,000 / 년','Leadership','학비 100%','Scholars Program 별도 장학','25% 또는 50%','일반 P6007 약대 학생 전체 대상 장학금은 아닙니다.','5년 과정과 졸업 후','4년 후 학사로 졸업 가능']:
  if phrase not in mt:errors.append(f'monash-page: compact pilot missing {phrase}')
 if 'A$49,740' in mt:errors.append('monash-page: domestic full-fee incorrectly shown as international tuition')
 for old_heading in ['<h2>과정·학위 구조</h2>','<h2>Direct 입학조건</h2>','<h2>졸업 후 485·지역</h2>','<h2>호주 약사등록</h2>','<h2>자주 묻는 질문</h2>']:
  if old_heading in mt:errors.append(f'monash-page: old duplicate section remains {old_heading}')
 if 'id="cost-form"' in mt:errors.append('monash-page: duplicated cost calculator should not render')
monash_tuition=next((x for x in D['tuition'] if x['program_id']=='monash-bpharm-hons'),None)
if not monash_tuition or monash_tuition['annual']['value']!=60100 or monash_tuition['annual']['source_year']!=2026 or monash_tuition['annual']['status']!='latest_published':
 errors.append('monash-data: international tuition must remain 2026 official A$60,100 reference until 2027 fee is verified')
monash_scholarships={x['id']:x for x in D['scholarships'] if x['university_id']=='monash'}
if monash_scholarships.get('monash-merit',{}).get('scope')!='scholars_program':
 errors.append('monash-data: 25/50% Pharmacy scholarship must stay scoped to Scholars Program')
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

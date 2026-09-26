"""Dependency-free static build. Every factual page is complete without JavaScript."""
from pathlib import Path
from html import escape as esc
import json, os, re, shutil, sys
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/catalog.json').read_text()); C=json.loads((ROOT/'data/site.json').read_text()); K=json.loads((ROOT/'data/korea_pharmacist.json').read_text())
U={u['id']:u for u in D['universities']}; P={p['id']:p for p in D['programs']}; S={s['id']:s for s in D['sources']}
DATE=D['verified_date']; MODE=os.getenv('CONTEXT','deploy-preview')
PRODUCTION=MODE=='production'
BASE=(os.getenv('DEPLOY_PRIME_URL') or os.getenv('SITE_URL') or 'http://localhost:8080').rstrip('/')
if PRODUCTION:
    if os.getenv('PRODUCTION_APPROVED')!='true' or not C['production_approved']:
        sys.exit('Production blocked: explicit user approval and site configuration are required.')
    BASE=(C.get('production_url') or '').rstrip('/')
    if not BASE.startswith('https://'):sys.exit('Production blocked: approved HTTPS canonical domain required.')
OUT=ROOT/'dist'; OFF=ROOT/'offline-preview'
for directory in [OUT,OFF]:
    if directory.exists():shutil.rmtree(directory)
    directory.mkdir();shutil.copytree(ROOT/'assets',directory/'assets');shutil.copy2(ROOT/'assets/favicon.svg',directory/'favicon.svg')

STATUS={'confirmed_2027':'2027 공식','latest_published':'최신 공식','pending_2027':'2027 확인 중','source_conflict':'공식자료 불일치'}
QUAL={'csat':'수능 CSAT','ib':'IB','alevel':'A-level','sat':'SAT','ossd':'OSSD','korean_high_school':'한국 일반고 내신','ged':'검정고시','other':'기타 국제학교 자격','graduate':'대학 졸업'}
ROUTE={'direct':'Direct Entry','foundation':'Foundation','diploma':'Diploma / IYO','graduate':'Graduate Entry','other':'기타 입학방법'}
MAIN_ROUTE={'foundation':'Foundation','diploma':'Diploma / IYO · 학점인정 진학','direct':'Direct Entry'}
PREREQ={'required':'필수','recommended':'권장','not_required':'필수 아님','accepted':'인정','assumed':'필수 아님 · 선행지식 권장'}
ASSESS={'automatic':'입학 지원과 함께 심사','application':'별도 신청','competitive':'경쟁 선발','guaranteed':'조건 충족 시 적용','course_excluded':'약대 제외','not_eligible':'한국 학생 대상 아님','pending':'확인 중'}
pages={}
def E(x):return esc(str(x),quote=True)
def value(f,default='확인 중'):
    v=f.get('value') if isinstance(f,dict) else f
    if v is None:return default
    if isinstance(v,bool):return '예' if v else '아니요'
    if isinstance(v,list):return ' / '.join(map(str,v))
    if isinstance(v,dict):return ' · '.join(f'{k} {v}' for k,v in v.items())
    return PREREQ.get(str(v),str(v))
def money(f):return f"A${f['value']:,.0f}" if f.get('value') is not None else '2027 확인 중'
def status(f,force=False):
    s=f.get('status','pending_2027');year=f.get('source_year')
    if s=='confirmed_2027' and not force:return ''
    label=(f'{year} 공식 참고' if s=='latest_published' and year else STATUS[s])
    return f'<span class="status {s}">{label}</span>'
def fv(f,fmt=None):
    t=fmt(f) if fmt else value(f)
    st=status(f)
    note=f'<span class="fact-note">{E(f["public_note"])}</span>' if f.get('public_note') else ''
    return f'{E(t)}'+(f'<br>{st}' if st else '')+note
def related(collection,p=None,u=None):return [r for r in D[collection] if (not p or r.get('program_id')==p) and (not u or r.get('university_id')==u)]
def one(collection,p):return related(collection,p)[0]
def purl(p):return '/universities/'+U[p['university_id']]['slug']+'/'
def link(url,text,cls=''):return f'<a href="{E(url)}"'+(f' class="{cls}"' if cls else '')+f'>{text}</a>'
def table(rows,headers=('항목','내용'),responsive=False):
    heads=''.join(f'<th scope="col">{E(x)}</th>' for x in headers)
    body=''.join('<tr>'+''.join(f'<td data-label="{E(headers[j])}">{c}</td>' for j,c in enumerate(r))+'</tr>' for r in rows)
    return f'<table class="fact-table {"responsive" if responsive else ""}"><thead><tr>{heads}</tr></thead><tbody>{body}</tbody></table>'
def facts(rows):return '<table class="fact-table"><tbody>'+''.join(f'<tr><th scope="row">{E(k)}</th><td>{v}</td></tr>' for k,v in rows)+'</tbody></table>'
def callout(text,warn=False):return f'<div class="callout {"warn" if warn else ""}">{text}</div>'
def section(id,title,content):return f'<section class="article-section" id="{id}"><h2>{title}</h2>{content}</section>'
def source_ids(obj):
    ids=set()
    if isinstance(obj,dict):
        if obj.get('source_id'):ids.add(obj['source_id'])
        for v in obj.values():ids |= source_ids(v)
    elif isinstance(obj,list):
        for v in obj:ids |= source_ids(v)
    return ids
def sources(ids):
    rows=''.join(f'<li><a href="{E(S[s]["url"])}" target="_blank" rel="noopener noreferrer">{E(S[s]["title"])} ↗</a></li>' for s in sorted(set(ids)) if s in S)
    return f'<details class="sources"><summary>자료 출처 <span>{DATE} 기준</span></summary><ul>{rows}</ul></details>'
def faq(items):return '<div class="faq">'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)+'</div>'
def pagehero(title,desc,crumb='가이드',extra=''):
    return f'<section class="page-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="현재 위치"><a href="/">홈</a><span>/</span><span>{E(crumb)}</span></nav><span class="eyebrow">2027 AUSTRALIA PHARMACY GUIDE</span><h1>{title}</h1><p>{desc}</p>{extra}</div></section>'
def article(items,detail_class=''):
    toc_short={
        '모나쉬 약대 과정 구조':'과정 구조',
        '입학방법 3가지':'입학방법',
        '5년 커리큘럼 한눈에 보기':'5년 커리큘럼',
        '학비·장학금·생활비':'비용·장학금',
        '5년 과정과 졸업 후':'졸업 후',
        '자료 출처':'자료 출처'
    }
    toc='<aside class="toc"><strong>이 페이지에서</strong>'+''.join('<a href="#'+id+'"><span class="toc-full">'+E(title)+'</span><span class="toc-short">'+E(toc_short.get(title,title))+'</span></a>' for id,title,_ in items)+'</aside>'
    section_class='section'+((' '+detail_class) if detail_class else '')
    return '<div class="'+section_class+'"><div class="wrap content-grid">'+toc+'<div>'+''.join(section(*x) for x in items)+'</div></div></div>'
def register(path,title,desc,body,faqs=None):pages[path]=dict(title=title,description=desc,body=body,faqs=faqs or [])
def logo():return '<svg class="brand-symbol" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 1 47 24 24 47 1 24Z" fill="#e1b63f"/><text x="24" y="28" text-anchor="middle" font-size="12" font-weight="800" font-family="Arial,sans-serif" fill="#fff">TNS</text></svg>'
def header(path):
    links=[('/universities/','대학별 약대'),('/admission-pathways/','입학방법'),('/tuition-scholarships/','학비·장학금'),('/pharmacist-registration/','약사등록'),('/after-graduation/','졸업 후')]
    nav=''.join(f'<a href="{u}"'+(' aria-current="page"' if path==u else '')+f'>{t}</a>' for u,t in links)
    return f'<a class="skip" href="#main">본문 바로가기</a>'+('' if PRODUCTION else '<div class="preview-bar">Preview · 2027 정보는 공식 발표 기준으로 업데이트합니다</div>')+f'<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="TNS 호주약대 가이드 홈">{logo()}<span class="brand-title">호주약대 가이드<small>BY TNS · AUSTRALIA</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">메뉴</button><nav class="nav" id="main-nav" aria-label="주 메뉴">{nav}<a class="nav-cta" href="/consult/">TNS 상담 ↗</a></nav></div></header>'
def channels():
    content=''
    for c in C['channels']:
        inner=f'<strong>{E(c["label"])}</strong><small>{E(c["detail"])}</small>'
        if c['url']:content+=f'<a class="channel" href="{E(c["url"])}"'+(' target="_blank" rel="noopener noreferrer"' if c['url'].startswith('https') else '')+f'>{inner}<span class="arrow" aria-hidden="true">↗</span></a>'
        else:content+=f'<div class="channel disabled">{inner}</div>'
    return '<div class="channels">'+content+'</div>'
def footer():return f'''<section class="consult-section" id="tns-channels"><div class="wrap"><div class="consult-intro"><div><span class="eyebrow">YOUR NEXT STEP</span><h2>내 성적으로 갈 수 있는 약대 찾기</h2><p>학력·과목·영어·입학시기를 정리하면<br>지원할 대학과 입학방법을 더 쉽게 고를 수 있습니다.</p></div><a class="btn secondary" href="/consult/">상담 전 준비할 내용 <span>→</span></a></div>{channels()}</div></section><footer class="site-footer"><div class="wrap"><div class="footer-top"><div><strong>TNS · 호주약대 가이드</strong><br><small>한국 학생을 위한 입학방법·과정 비교</small></div><nav class="footer-links" aria-label="하단 메뉴"><a href="/universities/">대학별 약대</a><a href="/compare/">조건 비교 도구</a><a href="/korea-pharmacist/">한국 약사면허</a><a href="/methodology/">자료 기준·업데이트</a><a href="/privacy/">개인정보 안내</a></nav></div><div class="footer-note">자료 확인일 {DATE} · 조건 충족 여부와 최종 입학허가는 대학 심사로 결정됩니다.<br>© TNS. TNS 유학 · 한국어 약대 정보·상담 서비스</div></div></footer>'''
def drawer():return '''<div class="compare-bar" hidden><p><b id="selected-count">0</b>개 과정 선택<small>최대 3개 · 학위구조까지 비교</small></p><div class="button-row"><button class="clear" id="clear-compare">비우기</button><button id="open-compare">선택 비교 →</button></div></div><dialog class="drawer" id="compare-dialog" aria-labelledby="compare-title"><div class="drawer-head"><h2 id="compare-title">선택한 약대 비교</h2><button id="close-compare" aria-label="비교 창 닫기">닫기 ✕</button></div><div class="drawer-body"><p class="small">선택한 조건의 비교용 정보입니다. 최종 지원 자격과 합격을 의미하지 않습니다.</p><div class="comparison-grid" id="comparison-content"></div></div></dialog><div class="toast" role="status" hidden></div>'''

def options(items):return ''.join(f'<option value="{E(v)}">{E(t)}</option>' for v,t in items)
def select(name,label,items):return f'<label>{label}<select name="{name}">{options(items)}</select></label>'
def finder(home=False):
    first=select('qualification','학력 / 시험',[('','선택해 주세요')]+[(k,v) for k,v in QUAL.items() if k not in ('graduate',)])
    first+=select('chemistry','화학 이수',[('','상관없음'),('yes','화학 있음'),('no','화학 없음')])
    first+=select('intake','희망 입학시기',[('','상관없음'),('2','2월'),('3','3월'),('7','7월')])
    first+=select('duration','과정 기간',[('','상관없음'),('fast','빠른 과정'),('4','4년'),('5','5년 통합')])
    advanced=select('route','입학방법',[('','전체')]+list(MAIN_ROUTE.items()))
    advanced+=select('structure','학위·인턴십',[('','전체'),('exit','4년 Exit 가능'),('integrated','Internship 학위 내 통합')])
    advanced+=select('science','선수과목',[('','전체'),('chemistry','화학 필수'),('mathematics','수학 필수'),('biology','Biology 인정')])
    advanced+=select('english','영어 기준',[('','전체'),('6.5','IELTS overall 6.5 이하'),('7','IELTS overall 7.0 이하'),('pte','PTE 기준 공개')])
    advanced+=select('cost','비용·장학금',[('','전체'),('scholarship','한국학생 약대 적용 장학 확인'),('20','20% 이상 장학'),('housing','공식 숙소 주 A$350 이하')])
    advanced+='<label class="score-field" hidden>성적 <span id="score-scale"></span><input name="score" type="number" min="0" step="any" inputmode="decimal" aria-describedby="score-help" placeholder="점수 입력 (선택)"></label>'
    more=f'<details class="advanced"><summary>상세 조건 더 보기</summary><div class="filter-grid advanced-grid">{advanced}</div><p class="filter-note" id="score-help">성적 계산법은 대학마다 다릅니다. 영어는 Overall과 각 영역 기준을 함께 적용합니다.</p></details>'
    if home:more=''
    return f'''<form class="finder {'home-finder' if home else ''}" id="finder" action="/compare/" method="get" data-mode="{'navigate' if home else 'filter'}"><div class="finder-title"><h2>내 조건으로 호주약대 찾기</h2><p>학력·화학·입학월만 골라도 바로 비교됩니다.</p></div><div class="filter-grid">{first}</div>{more}<div class="finder-actions"><p>미확정 항목은 ‘2027 확인 중’으로 분리합니다.<br>최종 합격 여부는 대학이 심사합니다.</p><div class="button-row">{'' if home else '<button type="reset" id="reset-filters">초기화</button>'}<button class="btn" type="submit">내 조건에 맞는 약대 보기 <span aria-hidden="true">→</span></button></div></div></form>'''
def card(p):
    u=U[p['university_id']];pid=p['id'];fee=one('tuition',pid)['annual'];en=one('english',pid);rq=one('requirements',pid);it=one('intakes',pid)
    e='확인 중' if en['ielts_overall']['value'] is None else 'IELTS '+str(en['ielts_overall']['value']).removesuffix('.0')
    if en['ielts_overall']['status']=='source_conflict':e+=' · 공식자료 불일치'
    elif en['ielts_overall']['status']=='pending_2027':e+=' · 확인 중'
    elif en['ielts_overall']['source_year']==2026:e+=' · 2026 참고'
    elif en['ielts_overall']['value'] is not None:e+=' · 영역별 별도'
    chips=''.join(f'<span class="chip">{E(t)}</span>' for t in p['highlights'])
    name=u['name_ko']+(' · 신설 PharmD' if pid=='uq-pharmd' else '')
    warn='<div class="notice-inline">신설 과정: APC 인증·Board 승인 대기</div>' if pid=='uq-pharmd' else '<div class="notice-inline">2027 모집정보 확인 중</div>' if p['international_recruitment']['value'] is None else ''
    return f'''<article class="university-card" data-program="{pid}"><div class="card-top"><div class="card-location"><span>{E(value(u['campus']))}</span><span class="school-monogram">{E(u['short'])}</span></div><h3>{E(name)}<span class="school-en">{E(u['name'])}</span></h3><div class="chips">{chips}</div><p class="degree-name">{E(value(p['name']))}</p></div>{warn}<dl class="card-facts"><dt>과정</dt><dd>{E(value(p['duration_label']))}</dd><dt>영어</dt><dd>{E(e)}</dd><dt>화학</dt><dd>{E(value(rq['chemistry']))}</dd><dt>연간 학비</dt><dd>{E(money(fee))}{' · '+str(fee['source_year']) if fee['value'] is not None else ''}</dd></dl><div class="match-reason" hidden></div><div class="card-bottom"><a href="{purl(p)}{'#uq-pharmd' if pid=='uq-pharmd' else ''}">입학조건 보기 →</a><label class="compare-toggle"><input type="checkbox" data-compare="{pid}" aria-label="{E(name)} 비교에 추가"> 비교</label></div></article>'''

REGIONAL_485={
 'jcu':dict(category='Category 3',area='Townsville · Cairns · Mackay',extra='두 번째 485 +2년 가능',total='요건 충족 시 총 4년'),
 'utas':dict(category='Tasmania 특례',area='Hobart · Launceston · Cradle Coast',extra='두 번째 485 +2년 가능',total='요건 충족 시 총 4년'),
 'curtin':dict(category='Category 2',area='Perth · Bentley',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년'),
 'uq':dict(category='Major city',area='Brisbane',extra='지역 추가 485 없음',total='기본 485 2년'),
 'adelaide':dict(category='Category 2',area='Adelaide',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년'),
 'griffith':dict(category='Category 2',area='Gold Coast',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년'),
 'latrobe':dict(category='Category 3',area='Bendigo',extra='두 번째 485 +2년 가능',total='요건 충족 시 총 4년'),
 'qut':dict(category='Major city',area='Brisbane',extra='지역 추가 485 없음',total='기본 485 2년'),
 'rmit':dict(category='Major city',area='Melbourne',extra='지역 추가 485 없음',total='기본 485 2년'),
 'newcastle':dict(category='Category 2',area='Newcastle',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년'),
 'canberra':dict(category='Category 2',area='Canberra',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년'),
 'unisq':dict(category='Category 3',area='Toowoomba',extra='두 번째 485 +2년 가능',total='요건 충족 시 총 4년'),
 'monash':dict(category='Major city',area='Melbourne',extra='지역 추가 485 없음',total='기본 485 2년'),
 'sydney':dict(category='Major city',area='Sydney',extra='지역 추가 485 없음',total='기본 485 2년'),
 'unsw':dict(category='Major city',area='Sydney',extra='지역 추가 485 없음',total='기본 485 2년'),
 'uwa':dict(category='Category 2',area='Perth · Crawley',extra='두 번째 485 +1년 가능',total='요건 충족 시 총 3년')
}

STATE_NOMINATION={
 'WA':dict(status='2026-27 발표 대기',headline='WA 190·491 · 새 기준 발표 대기',detail='2025-26에는 healthcare and social assistance가 우선 업종이었고 Hospital·Industrial·Retail Pharmacist 초청 사례가 있습니다. 2026-27 직업목록과 조건은 새 공고가 나온 뒤 적용합니다.',sources=['migration-wa-criteria','migration-wa-pharmacist']),
 'SA':dict(status='2026-27 발표 대기',headline='SA 190·491 · 새 프로그램 개시 대기',detail='2025-26 ROI는 종료됐고 2026-27 프로그램이 시작되면 새 occupation list와 stream 조건을 적용합니다.',sources=['migration-sa-list','migration-sa-status']),
 'QLD':dict(status='2026-27 QSOL 미공개',headline='QLD 190·491 · 2026-27 새 QSOL 준비 중',detail='Migration Queensland는 2026-27 QSOL 개발을 위한 consultation을 2026년 7월 7일 종료했습니다. 현재 공개된 onshore list는 여전히 2025-26 기준이며 Hospital Pharmacist와 Retail Pharmacist는 491만 표시됩니다. 2026-27 QSOL 공개 전에는 이를 새 회계연도 자격으로 확정하지 않습니다.',sources=['migration-qld-list','migration-qld-status','migration-qld-2026-consultation']),
 'VIC':dict(status='2026-27 발표 대기',headline='Victoria 190·491 · 새 프로그램 발표 대기',detail='2025-26 프로그램은 마감됐습니다. 2026-27 nomination 조건은 공식 발표 후 업데이트합니다.',sources=['migration-vic-status']),
 'NSW':dict(status='현재 리스트 포함',headline='NSW 190·491 · Pharmacists 2515 포함',detail='현재 NSW Skills List에 Pharmacists(ANZSCO unit group 2515)가 190과 Regional 491 모두 포함돼 있습니다. 실제 초청은 EOI 순위와 NSW 선발기준을 따릅니다.',sources=['migration-nsw-skills']),
 'TAS':dict(status='2026-27 운영 중',headline='Tasmania 190·491 · 약사 3개 직종 포함',detail='2026-27 프로그램은 2026년 8월 개시됐습니다. Hospital Pharmacist 251511, Industrial Pharmacist 251512, Retail Pharmacist 251513이 Health/Allied Health 목록에 포함돼 있습니다.',sources=['migration-tas-program','migration-tas-health']),
 'ACT':dict(status='현재 리스트 포함',headline='ACT 190·491 · 약사 3개 직종 포함',detail='현재 ACT occupation list에 Hospital·Industrial·Retail Pharmacist가 포함돼 있으며 Canberra Matrix로 경쟁합니다. 2026-27 nomination allocation은 아직 발표 대기입니다.',sources=['migration-act-list','migration-act-program'])
}

def university_programs(uid):return [p for p in D['programs'] if p['university_id']==uid]
def university_routes(uid):
    pids={p['id'] for p in university_programs(uid)}
    return [r for r in D['entry_routes'] if r['program_id'] in pids]
def has_route(uid,t):
    return any(r['type']==t and r['availability']['value'] is True for r in university_routes(uid))
def months_for(uid):
    out=[]
    pids={p['id'] for p in university_programs(uid)}
    for it in D['intakes']:
        if it['program_id'] in pids and isinstance(it['months']['value'],list):
            out+=it['months']['value']
    return sorted(set(out))
def intake_text(uid):
    mm=months_for(uid)
    return ' · '.join('2월' if x==2 else '7월' if x==7 else str(x)+'월' for x in mm) if mm else '확인 중'
def pathway_badges(uid):
    labels=['Direct']
    if has_route(uid,'foundation'):labels.append('Foundation')
    if has_route(uid,'diploma'):labels.append('Diploma')
    if has_route(uid,'graduate') or uid=='uwa':labels.append('Graduate Entry')
    return ''.join('<span class="path-badge">'+E(x)+'</span>' for x in labels)
def internship_label(uid):
    ps=university_programs(uid)
    vals=[]
    for p in ps:
        rr=one('professional_registration',p['id'])
        if rr['post_graduation_internship']['value'] is True:vals.append('졸업 후 인턴십')
        elif rr['itp_in_degree']['value'] is True or rr['supervised_practice_in_degree']['value'] is True:vals.append('학위 안 실무훈련')
    return ' / '.join(dict.fromkeys(vals)) if vals else '확인 중'
def directory_card(u):
    ps=university_programs(u['id'])
    duration=' / '.join(dict.fromkeys(value(p['duration_label']) for p in ps))
    region=REGIONAL_485[u['id']]
    headline=E(ps[0]['editorial'])
    return f'''<article class="pharmacy-school-card"><div class="school-card-head"><div><span class="school-state">{E(u['state'])} · {E(region['area'])}</span><h3>{E(u['name_ko'])}<small>{E(u['name'])}</small></h3></div><span class="school-monogram large">{E(u['short'])}</span></div><p class="school-summary">{headline}</p><div class="path-badges">{pathway_badges(u['id'])}</div><dl class="school-keyfacts"><div><dt>과정</dt><dd>{E(duration)}</dd></div><div><dt>입학</dt><dd>{E(intake_text(u['id']))}</dd></div><div><dt>인턴십</dt><dd>{E(internship_label(u['id']))}</dd></div><div><dt>485</dt><dd>{E(region['total'])}</dd></div></dl><a class="school-detail-link" href="/universities/{E(ps[0]['id'].replace('-bpharm-hons','').replace('-pharmd',''))}-pharmacy/" data-fallback="{E(purl(ps[0]))}">이 약대 상세분석 →</a></article>'''
def state_nomination_html(u):
    s=STATE_NOMINATION.get(u['state'])
    if not s:return '<p>주정부 nomination 정보 업데이트 중입니다.</p>'
    return '<div class="state-nomination-card"><span class="state-status">'+E(s['status'])+'</span><h3>'+E(s['headline'])+'</h3><p>'+E(s['detail'])+'</p></div>'+sources(s['sources'])

def poststudy_html(u):
    r=REGIONAL_485[u['id']]
    return facts([('약대 캠퍼스',E(r['area'])),('첫 485','2년'),('지역 분류',E(r['category'])),('두 번째 485',E(r['extra'])),('가능 총기간',E(r['total']))])+callout('두 번째 485는 자동 연장이 아닙니다. 지역캠퍼스 졸업과 지역 거주 등 Second Post-Higher Education Work stream 요건을 충족해야 합니다.')+'<h3>주정부 nomination</h3>'+state_nomination_html(u)+link('/after-graduation/','485·Regional 전체 기준 →','btn text')

home=f'''<section class="hero school-first-hero"><div class="wrap hero-grid"><div><span class="eyebrow">2027 AUSTRALIA PHARMACY GUIDE</span><h1>호주 약대,<br><em>학교마다 길이 다릅니다.</em></h1><p class="hero-copy">3년·4년·5년 과정, Direct·Foundation·Diploma,<br>입학월과 졸업 후 인턴십까지 학교마다 다릅니다.<br>내 조건에 맞는 대학부터 바로 비교하세요.</p><div class="button-row"><a class="btn" href="#all-schools">대학별 약대 보기 <span>↓</span></a><a class="btn secondary" href="/admission-pathways/">입학방법으로 보기 →</a></div><div class="hero-meta"><span>{len(U)}개 대학</span><span>{len(P)}개 학부 시작 과정</span><span>대학별 상세분석</span></div></div><div class="route-illustration difference-panel"><div class="top"><h2>딱 네 가지만 비교하세요</h2><span class="live-dot">SCHOOL BY SCHOOL</span></div><div class="difference-list"><div><b>기간</b><span>3년 · 4년 · 5년</span></div><div><b>입학월</b><span>2월 · 3월 · 7월</span></div><div><b>입학방법</b><span>바로 입학 · Foundation · Diploma</span></div><div><b>졸업 후</b><span>인턴십 · 485 · 지역 혜택</span></div></div></div></div></section>'''

home+='''<section class="section school-differences"><div class="wrap"><div class="section-head"><div><span class="eyebrow">COURSE STRUCTURE</span><h2>호주 약대는 크게 3가지 구조입니다</h2><p>먼저 3년·4년·5년으로 나누면 훨씬 쉽게 비교할 수 있습니다.</p></div></div><div class="difference-cards course-type-cards"><div class="course-type-card"><strong>3 YEARS</strong><b>3년 학사 (Fast Track)</b><span>JCU · UTas</span><small>3년 안에 약학 학사 완료</small></div><div class="course-type-card"><strong>4 YEARS</strong><b>4년 학사</b><span>Griffith · La Trobe · QUT · RMIT · Newcastle · Canberra · UniSQ · Adelaide</span><small>가장 일반적인 호주 약대 구조</small></div><div class="course-type-card"><strong>5 YEARS</strong><b>5년 학·석사 통합</b><span>Monash · Sydney · UNSW · UQ PharmD</span><small>학사와 PharmD·석사급 과정을 한 번에 이수</small></div></div><p class="course-type-note"><strong>예외 구조</strong> Curtin 3년 9개월 · UQ BPharm은 7월 입학 시 약 3.5년 · UWA는 4년 Bachelor + PharmD 통합과정</p></div></section>'''

home+='<section class="section soft" id="all-schools"><div class="wrap"><div class="section-head"><div><span class="eyebrow">ALL PHARMACY SCHOOLS</span><h2>'+str(len(U))+'개 호주 약대를 하나씩 보세요</h2><p>관심 대학을 누르면 입학조건·학비·장학금·졸업 후 경로까지 한 번에 볼 수 있습니다.</p></div><a href="/universities/">대학별 전체 페이지 →</a></div><div class="pharmacy-school-grid">'+''.join(directory_card(u) for u in D['universities'])+'</div><div class="secondary-tool"><span>성적·화학·입학월로 다시 좁히고 싶다면</span><a href="/compare/">조건 비교 도구 사용 →</a></div></div></section>'

home+='''<section class="section pathway-hub-preview"><div class="wrap"><div class="section-head"><div><span class="eyebrow">ENTRY PATHWAYS</span><h2>입학방법으로 다시 모아보기</h2><p>내 학력에 맞는 시작점을 먼저 고르세요.</p></div><a href="/admission-pathways/">입학방법 전체보기 →</a></div><div class="pathway-hub-grid"><a href="/direct-entry/"><span>DIRECT</span><h3>고졸 Direct</h3><p>수능·IB·A-level·SAT·OSSD로 약대 1학년</p></a><a href="/foundation/"><span>FOUNDATION</span><h3>Foundation</h3><p>고2 수료부터 시작해 약대 1학년</p></a><a href="/diploma/"><span>DIPLOMA</span><h3>Diploma</h3><p>Griffith·Curtin은 약대 2학년</p></a><a href="/graduate-entry/"><span>GRADUATE ENTRY</span><h3>대졸자 입학</h3><p>Monash·UWA 등 학사 졸업자 과정</p></a></div></div></section>'''

home+='''<section class="section soft poststudy-preview"><div class="wrap"><div class="section-head"><div><span class="eyebrow">AFTER GRADUATION</span><h2>졸업 후 체류기간도 캠퍼스마다 다릅니다</h2><p>첫 485는 기본 2년입니다. Regional 졸업·거주 요건을 채우면 두 번째 485로 1~2년이 추가됩니다.</p></div><a href="/after-graduation/">485·Regional 전체보기 →</a></div><div class="visa-grid"><div><strong>2년</strong><h3>Sydney · Melbourne · Brisbane</h3><p>Major city · 지역 추가 485 없음</p></div><div><strong>3년</strong><h3>Perth · Adelaide · Gold Coast 등</h3><p>Category 2 · 요건 충족 시 +1년</p></div><div><strong>4년</strong><h3>Townsville · Bendigo · Toowoomba 등</h3><p>Category 3 · 요건 충족 시 +2년</p></div></div><p class="representative-note">두 번째 485는 Regional 졸업·거주 요건을 모두 충족해야 합니다. 주정부 이민은 485와 별도 제도입니다.</p></div></section>'''

home+='''<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">PROFESSIONAL PATH</span><h2>입학만큼 졸업 후 약사등록도 중요합니다</h2><p>같은 PharmD라도 인턴십을 학위 안에서 하는지, 졸업 후 따로 하는지가 다릅니다.</p></div></div><div class="guides">'''+''.join(f'<a class="guide-card" href="{url}"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{desc}</p><span class="arrow">자세히 보기 →</span></a>' for url,tag,title,desc in [('/pharmacist-registration/','AUSTRALIA','호주 약사등록','학위부터 인턴십·등록시험까지 순서대로 봅니다.'),('/korea-pharmacist/','KOREA','한국 약사면허','보건복지부 인정대학부터 예비시험·국가시험까지 봅니다.'),('/tuition-scholarships/','COST','학비·장학금·숙소','대학별 실제 비용과 장학금을 비교합니다.')])+'</div></div></section>'
register('/','2027 호주 약대 가이드 · 대학별 과정·입학방법·485 | TNS','호주 약대는 대학마다 기간, 학위, 입학월, 선수과목, Foundation·Diploma, 인턴십과 Regional 485 조건이 다릅니다. 16개 대학을 각각 상세 분석합니다.',home)

directory_body=pagehero('호주 약대 '+str(len(U))+'개 전체보기','16개 대학의 기간·입학월·입학방법·인턴십·485를 같은 기준으로 비교합니다.','대학별 약대')
directory_body+='<section class="section"><div class="wrap"><div class="university-directory-intro three-types"><div><strong>3년 학사</strong><span>JCU · UTas</span></div><div><strong>4년 학사</strong><span>Griffith · La Trobe · QUT · RMIT · Newcastle · Canberra · UniSQ · Adelaide</span></div><div><strong>5년 통합</strong><span>Monash · Sydney · UNSW · UQ PharmD</span></div></div><p class="course-type-note"><strong>예외</strong> Curtin 3년 9개월 · UQ BPharm 7월 약 3.5년 · UWA 4년 Bachelor + PharmD</p><div class="pharmacy-school-grid">'+''.join(directory_card(u) for u in D['universities'])+'</div><div class="secondary-tool"><span>성적·화학·입학월로 대학을 좁혀보세요.</span><a href="/compare/">내 조건으로 찾기 →</a></div></div></section>'
register('/universities/','2027 호주 약대 16개 대학별 상세 비교 | TNS','호주 약대 16개 대학의 기간, 입학시기, Direct·Foundation·Diploma, 인턴십, 485 지역조건을 대학별 상세페이지로 연결합니다.',directory_body)

ge=[r for r in D['entry_routes'] if r['type']=='graduate' and r['availability']['value'] is True]
monash_ge='<p>2027 공식 조건 업데이트 중입니다.</p>'
if ge:
    g=ge[0]
    monash_ge='<p><strong>'+E(g['title'])+'</strong></p>'+facts([('기간',fv(g['duration'])),('입학시기',fv(g['intake'])),('입학 학력',fv(g['qualification'])),('영어',fv(g['english'])),('선발·진급',fv(g['progression']))])+'<p>'+E(g['note'])+'</p>'+link('/universities/monash-pharmacy/','Monash 약대 전체 분석 →','btn text')
ge_items=[('overview','대졸자 약대는 별도 과정입니다','<p>고등학생용 Direct·Foundation·Diploma와 달리 이미 학사학위가 있는 학생이 지원하는 과정입니다.</p>'),('uwa','UWA · 2년 Doctor of Pharmacy','<p><strong>2년 · 2027년 1월 시작</strong></p><p>학사학위, sWAM 65+, Chemistry, Mathematics/Statistics, Microbiology, Pharmacology가 필요합니다. IELTS는 Overall 7.0, 각 영역 7.0입니다. 선발은 경쟁 방식입니다.</p>'+link('/universities/uwa-pharmacy/','UWA 약대 전체 분석 →','btn text')),('monash','Monash Graduate Entry',monash_ge),('note','대졸자 과정도 대학별로 다릅니다','<p>과정기간, 선수과목, 학부 전공 제한, 선발 방식이 다르므로 학사학위가 있다고 모두 지원할 수 있는 것은 아닙니다.</p>'+sources(['uwa-dpharm','monash']))]
register('/graduate-entry/','2027 호주 약대 Graduate Entry · UWA·Monash | TNS','학사 졸업자가 지원하는 호주 약대 Graduate Entry를 UWA 2년 Doctor of Pharmacy와 Monash 경로 중심으로 정리합니다.',pagehero('호주 약대 Graduate Entry','이미 학사학위가 있다면 고교생 경로가 아닌 대졸자 전형을 따로 봐야 합니다.','Graduate Entry')+article(ge_items))

regional_rows=[]
for u in D['universities']:
    r=REGIONAL_485[u['id']]
    regional_rows.append((link('/universities/'+university_programs(u['id'])[0]['id'].replace('-bpharm-hons','').replace('-pharmd','')+'-pharmacy/',E(u['short'])),E(r['area']),E(r['category']),E(r['total'])))
after_items=[('rule','485 기본기간','<p>현재 Home Affairs 기준으로 Bachelor와 Masters coursework/extended의 Post-Higher Education Work stream은 기본 2년입니다.</p>'),('regional','Regional이면 두 번째 485가 추가될 수 있습니다',table([('Category 2','+1년','요건 충족 시 총 3년'),('Category 3','+2년','요건 충족 시 총 4년'),('Tasmania','+2년','요건 충족 시 총 4년')],['지역','두 번째 485','가능 총기간'],True)+callout('Tasmania는 Second 485 전용 규칙에서 Category 2·3 모두 +2년으로 처리됩니다. 두 번째 485는 자동 연장이 아니며 지역캠퍼스 졸업과 지역 거주 등 별도 요건을 충족해야 합니다.')),('schools','약대별 캠퍼스와 485',table(regional_rows,['대학','약대 캠퍼스','지역 분류','485'],True)),('state','주정부 nomination','<p>주정부 nomination은 485와 별개입니다. NSW·Tasmania·ACT처럼 약사 직종이 현재 리스트에 확인되는 곳도 있고, 2026-27 새 기준 발표를 기다리는 주도 있습니다. 각 대학 상세페이지에 해당 주의 현재 상태를 표시합니다.</p>'),('sources','자료 출처',sources(['homeaffairs-485','homeaffairs-second485','homeaffairs-regional','jcu-2027-campus','utas-2027-campus','migration-nsw-skills','migration-tas-program','migration-tas-health','migration-act-list','migration-qld-status','migration-qld-2026-consultation','migration-vic-status','migration-sa-status','migration-wa-criteria']))]
register('/after-graduation/','호주 약대 졸업 후 485 · Regional · 주정부 이민 | TNS','호주 약대 졸업 후 485 기본 2년과 Regional Category 2·3의 두 번째 485, 대학별 캠퍼스 지역을 정리합니다.',pagehero('호주 약대 졸업 후 485·Regional','약대가 있는 도시와 캠퍼스에 따라 졸업 후 체류조건이 달라질 수 있습니다.','졸업 후')+article(after_items))

comp=pagehero('2027 호주 약대 비교',f'학력·선수과목·입학시기로 {len(U)}개 대학의 {len(P)}개 과정을 비교합니다.','전체 약대 비교')
comp+='<div class="compare-sticky"><a href="#finder">조건 수정 ↑</a><span>최대 3개 과정 비교</span></div><section class="section"><div class="wrap">'+finder()+'''<div class="results-head"><div><h2>비교 결과 <span class="results-count" id="result-count">'''+str(len(P))+'''</span></h2><p id="result-summary" role="status" aria-live="polite">조건을 고르면 맞는 과정만 남습니다.</p></div><p class="view-note">선택한 조건과 맞는 과정입니다.<br>최종 합격은 대학 심사로 결정됩니다.</p></div><div class="empty" id="empty-results" hidden><h3>현재 조건에 맞는 과정이 없습니다</h3><p>조건을 하나 줄이거나 ‘추가 확인 필요’ 과정까지 함께 보세요.</p><button type="button" id="reset-empty">필터 초기화</button></div><div class="card-grid" id="match-results">'''+''.join(card(p) for p in D['programs'])+'''</div><h2 class="pending-heading" id="pending-heading" hidden>추가 확인 필요 <span id="pending-count"></span></h2><p class="small" id="pending-note" hidden>2027 정보가 아직 확정되지 않았거나 공식자료가 서로 다른 과정입니다.</p><div class="card-grid" id="pending-results"></div>'''+callout('UWA 4년 Bachelor + Doctor of Pharmacy는 비교에 포함했습니다. 대학원 전용 과정은 제외했습니다.')+'</div></section>'
register('/compare/','2027 호주 약대 비교 · 입학방법·화학·입학시기 필터 | TNS',f'호주 약대 {len(U)}개 대학, {len(P)}개 과정을 조건별로 비교합니다. 3년·4년·5년, 화학, 7월 입학, Foundation·1학년 Diploma·Direct Entry를 구분합니다.',comp)

def qtable(pid):
    rows=[]
    for q in related('qualifications',pid):
        f=q['score']; display=fv(f)
        if f['value'] is False:display='이 자격만으로 Direct 입학 불가<br>'+status(f)
        if q.get('scale'):display+=f'<span class="fact-note">기준: {E(q["scale"])}</span>'
        if q.get('calculation'):display+=f'<span class="fact-note">{E(q["calculation"])}</span>'
        rows.append((QUAL[q['qualification']],display))
    return facts(rows)
def routecards(rs):
    html=''
    for r in rs:
        if r['type']=='direct':
            it=one('intakes',r['program_id'])
            fields=[('입학',('가능' if r['availability']['value'] is True else '2027 확인 중' if r['availability']['value'] is None else '불가')),('기간 / 시작월',fv(r['duration'])+'<br>'+fv(it['label']))]
        else:
            fields=[('경로',('운영' if r['availability']['value'] is True else '2027 확인 중' if r['availability']['value'] is None else '미운영')),('기간 / 시작월',fv(r['duration'])+'<br>'+fv(r['intake'])),('약대 진급조건',fv(r['progression'])),('입학 학력',fv(r['qualification'])),('영어',fv(r['english']))]
        if r.get('pathway_fee'):fields.append(('준비과정 학비',fv(r['pathway_fee'],money)))
        if isinstance(r['credit']['value'],(int,float)) and r['credit']['value']>0:fields.insert(1,('약대 인정학점',fv(r['credit'])+(' CP' if r['program_id'].startswith('griffith') else ' credits')))
        note_html=f'<p>{E(r["note"])}</p>' if r.get('note') else ''
        html+=f'<article class="route-detail"><span class="pill-label">{ROUTE[r["type"]]}</span><h3>{E(r["title"])}</h3><dl>'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in fields)+f'</dl>{note_html}</article>'
    return '<div class="route-cards">'+html+'</div>'
def pathway_status(uid,t):
    rr=[r for r in university_routes(uid) if r['type']==t]
    if t=='graduate' and uid=='uwa':return '<strong class="yes">있음</strong><span>2년 Doctor of Pharmacy</span>'
    if not rr:return '<strong class="none">현재 공개된 전용 연계 없음</strong>'
    confirmed=[r for r in rr if r['availability']['value'] is True]
    pending=[r for r in rr if r['availability']['value'] is None]
    if confirmed:
        r=confirmed[0]
        if t=='diploma' and r['entry_year']['value']==2:return '<strong class="yes">있음</strong><span>약대 2학년 진학</span>'
        if t=='foundation':return '<strong class="yes">있음</strong><span>약대 1학년 진학</span>'
        if t=='graduate':return '<strong class="yes">있음</strong><span>'+E(r['title'])+'</span>'
        return '<strong class="yes">있음</strong>'
    if pending:return '<strong class="pending">2027 확인 중</strong>'
    return '<strong class="none">공식 연계 미확인</strong>'
def pathway_matrix(uid):
    return '<div class="pathway-status-grid"><div><b>Direct</b><strong class="yes">가능</strong><span>약대 1학년</span></div><div><b>Foundation</b>'+pathway_status(uid,'foundation')+'</div><div><b>Diploma</b>'+pathway_status(uid,'diploma')+'</div><div><b>Graduate Entry</b>'+pathway_status(uid,'graduate')+'</div></div>'
def scholarcards(ss):
    out=''
    for s in ss:
        av=s['amount']['value']
        if av is None:amount='2027 확인 중'
        elif isinstance(av,list):amount=' / '.join(str(x)+'%' for x in av)
        else:amount=str(av)+'%'
        fields=[('장학금',fv(s['amount'],lambda _:amount)),('심사방식',ASSESS[s['assessment']])]
        optional=[('자동심사',s['automatic_assessment']),('별도 신청',s['separate_application']),('경쟁 선발',s['competitive']),('적용 기간',s['duration']),('성적 기준',s['academic_threshold']),('유지 조건',s['renewal_condition']),('한국 학생',s['country_eligibility']),('약대 적용',s['pharmacy_eligible']),('선발 인원',s['number_available']),('제외 과정',s['course_exclusion'])]
        fields += [(label,fv(f)) for label,f in optional if f.get('value') is not None]
        note_html=f'<p>{E(s["note"])}</p>' if s.get('note') else ''
        out+=f'<article class="route-detail scholarship-card"><span class="pill-label">{ASSESS[s["assessment"]]}</span><h3>{E(s["name"])}</h3><dl>'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in fields)+f'</dl>{note_html}</article>'
    return '<div class="route-cards">'+out+'</div>'
def housingcards(hh):
    out=''
    for h in hh:
        fields=[]
        if h['weekly_cost']['value'] is not None:fields.append(('주당',fv(h['weekly_cost'],money)))
        if h['contract_weeks']['value'] is not None:fields.append(('계약',fv(h['contract_weeks'],lambda f:str(value(f))+'주')))
        if h['official_contract_total']['value'] is not None:fields.append(('공식 총액',fv(h['official_contract_total'],money)))
        if h['utilities']['value'] is not None:fields.append(('공과금 포함',fv(h['utilities'])))
        if h['meals']['value'] is not None:fields.append(('식사 포함',fv(h['meals'])))
        if h['campus_distance']['value'] is not None:fields.append(('위치',fv(h['campus_distance'])))
        content=facts(fields) if fields else ''
        note_html=f'<p>{E(h["note"])}</p>' if h.get('note') else ''
        out+=f'<article class="route-detail housing-card"><h3>{E(h["name"])}</h3>{content}{note_html}</article>'
    return '<div class="route-cards">'+out+'</div>'
def structure(pid):
    p=P[pid];r=one('professional_registration',pid)
    rows=[('총 학업기간',fv(p['duration_label']))]
    def yn(f,yes,no):
        if f.get('value') is None:return '2027 확인 중'
        return yes if f['value'] else no
    if p['duration_years']['value']==5:
        rows.extend([('학사학위 취득',fv(p['bachelor_award_year'],lambda f:str(f['value'])+'년차' if f['value'] else '확인 중')),('4년 후 학사 Exit',yn(p['four_year_exit'],'가능','없음')),('4년 후 학위',fv(p['exit_degree']))])
    rows.extend([('최종 학위',fv(p['final_degree'])),('학위 중 등록 실무훈련',yn(r['supervised_practice_in_degree'],'포함','별도')),('Intern Training Program',yn(r['itp_in_degree'],'학위에 포함','별도')),('졸업 후 등록 인턴십',yn(r['post_graduation_internship'],'필요','별도 없음'))])
    return facts(rows)
def costcalculator():return '''<div class="cost-calculator"><h3>1년 예상비용 계산</h3><p class="small">학비·숙소·생활비를 넣으면 1년 예상비용을 바로 계산합니다. 기본값은 예시입니다.</p><form id="cost-form"><div class="cost-grid"><label>연간 학비 (AUD)<input name="tuition" type="number" min="0" max="200000" value="60000" step="100"></label><label>숙소 주당 (AUD)<input name="rent" type="number" min="0" max="3000" value="350"></label><label>계약 주 수<input name="weeks" type="number" min="1" max="52" value="52"></label><label>기타 생활비 주당 (AUD)<input name="living" type="number" min="0" max="3000" value="250"></label><label>적용할 장학률 (%)<input name="discount" type="number" min="0" max="100" value="0"></label><label>계산용 환율 (KRW / AUD)<input name="fx" type="number" min="1" max="10000" value="1000"></label></div><button class="btn" type="submit" style="margin-top:20px">1년 비용 계산</button></form><div class="cost-output" aria-live="polite" id="cost-output"><span>위 가정으로 계산한 1년 예산</span><strong>A$91,200</strong><p>약 9,120만 원 · 환율 A$1 = 1,000원 가정<br>학비 A$60,000 + 숙소 A$18,200 + 기타 생활비 A$13,000</p></div><p class="small muted" style="margin-top:14px">예상비용입니다. 장학금은 실제 오퍼 기준으로 입력하세요. 항공·비자·OSHC·교재·보증금·실습 이동비는 포함하지 않습니다.</p></div>'''

for u in D['universities']:
    pp=[p for p in D['programs'] if p['university_id']==u['id']];p=pp[0];pid=p['id'];rq=one('requirements',pid);en=one('english',pid);it=one('intakes',pid);t=one('tuition',pid);r=one('professional_registration',pid)
    rs=related('entry_routes',pid);ss=related('scholarships',u=u['id']);hh=related('accommodation',u=u['id'])
    extra='<div class="facts-grid">'+''.join(f'<div class="fact-tile"><small>{k}</small><strong>{v}</strong></div>' for k,v in [('과정',E(value(p['duration_label']))),('캠퍼스',E(value(u['campus']))),('입학시기',E(value(it['label']))),('유학생 모집',E(value(p['international_recruitment']))),('연간 학비',E(money(t['annual']))),('정보 기준일',DATE)])+'</div>'
    if u['id']=='monash':
        extra='''<div class="facts-grid monash-hero-facts">
<div class="fact-tile"><small>과정</small><strong>5년 PharmD</strong></div>
<div class="fact-tile"><small>캠퍼스</small><strong>Parkville</strong></div>
<div class="fact-tile"><small>입학</small><strong>2월</strong></div>
<div class="fact-tile"><small>2027 학비</small><strong>'''+E(money(t['annual']))+'''</strong></div>
<div class="fact-tile"><small>영어</small><strong>IELTS 6.5 · 각 6.0</strong></div>
<div class="fact-tile"><small>장학금</small><strong>경쟁선발 · 연 8명</strong><span class="fact-note">25% 또는 50%</span></div>
</div>'''
    body=pagehero(E(u['name_ko'])+' 약대',E(u['name'])+' · '+E(value(p['name'])),u['name_ko'],extra)
    intro='<p>'+E(p['editorial'])+'</p><div class="chips">'+''.join(f'<span class="chip">{E(h)}</span>' for h in p['highlights'])+'</div>'
    lens=p.get('decision_lens') or {}
    if lens:
        intro+='<div class="decision-lens"><div><span>이 학교를 고르는 이유</span><ul>'+''.join('<li>'+E(x)+'</li>' for x in lens.get('why',[]))+'</ul></div><div class="watch"><span>꼭 알아둘 점</span><ul>'+''.join('<li>'+E(x)+'</li>' for x in lens.get('watch',[]))+'</ul></div></div>'
    if p['review_items']:intro+=callout('<strong>현재 미확정 정보</strong><ul>'+''.join('<li>'+E(x)+'</li>' for x in p['review_items'])+'</ul>',True)
    anatomy=structure(pid)
    if len(pp)>1:
        other=pp[1];anatomy+='<h3 id="uq-pharmd">신설 UQ 통합 PharmD · 별도 과정</h3>'+callout(E(other['editorial']),True)+structure(other['id'])
    requirements_html=facts([(name,fv(rq[k])) for k,name in [('chemistry','Chemistry'),('mathematics','Mathematics'),('biology','Biology'),('physics','Physics'),('minimum_grade','과목 성적 기준')]])
    english_html=facts([(name,fv(en[k])) for k,name in [('ielts_overall','IELTS overall'),('ielts_bands','IELTS 영역별'),('pte_overall','PTE overall'),('pte_each','PTE each'),('toefl','TOEFL')]])+callout('대학 입학 영어와 약사등록 영어는 서로 다른 기준입니다.')
    fees=facts([('연간 국제학생 학비',fv(t['annual'],money)),('수강량 기준',fv(t['load_basis'])),('대학 공개 예상 총학비',fv(t['official_total'],money))])+'<p class="small muted">'+E(t['increase_note'])+' 연간 학비에 기간을 단순히 곱하지 않았습니다.</p>'
    registration_html=facts([('APC 인증',fv(p['accreditation'])),('학위 안 실무훈련',fv(r['supervised_practice_in_degree'])),('학위 안 Intern Training',fv(r['itp_in_degree'])),('졸업 후 인턴십',fv(r['post_graduation_internship']))])+callout(E(r['note']))+link('/pharmacist-registration/','약사등록 단계별 설명 →','btn text')
    fs=[('선수과목을 이수하지 않아도 지원할 수 있나요?',('JCU는 화학이 필수가 아닙니다. 수학·영어 등 다른 조건은 충족해야 합니다.' if u['id']=='jcu' else '대학마다 필수과목이 다릅니다. 화학·수학이 부족하면 Foundation으로 보완할 수 있는지 보세요.')),
        ('2027 학비가 미공개인 항목은 어떻게 보나요?','2027 학비가 없는 대학은 가장 최근 공식 학비와 연도를 함께 표시합니다.'),
        ('졸업하면 바로 호주나 한국 약사가 되나요?','아닙니다. 호주는 인턴십·시험·등록이 필요하고, 한국은 별도 면허 절차가 있습니다.')]
    allids=source_ids([p,rs,ss,hh,rq,en,it,t,r,related('qualifications',pid)])|{'apc','korea-law'}
    if u['id']=='uq':allids|={'uq-pharmd','uq-foundation','uq-calendar'}
    routes_html=pathway_matrix(u['id'])+routecards(rs)
    if u['id']=='uwa':routes_html+=callout('<strong>대졸자 별도 과정</strong><p>UWA에는 학사 졸업자가 지원하는 2년 Doctor of Pharmacy도 있습니다. 2027년 1월 시작, sWAM 65+와 Chemistry·Math/Statistics·Microbiology·Pharmacology가 필요합니다.</p>'+link('/graduate-entry/','UWA Graduate Entry 보기 →','btn text'))
    allids|={'homeaffairs-485','homeaffairs-second485','homeaffairs-regional'}
    allids|=set(STATE_NOMINATION.get(u['state'],{}).get('sources',[]))
    if u['id']=='jcu':allids|={'jcu-2027-campus'}
    if u['id']=='utas':allids|={'utas-2027-campus'}
    if u['id']=='uwa':allids|={'uwa-dpharm'}
    if u['id']=='monash':allids|={'monash-curriculum-2027'}
    if u['id']=='monash':
        monash_overview='''<div class="monash-snapshot"><p class="lead"><strong>4년까지 공부하면 BPharm(Hons), 5년차까지 마치면 Doctor of Pharmacy입니다.</strong></p><p>5년차에는 유급 supervised practice와 Intern Training Program이 포함됩니다.</p><div class="monash-keyline"><span>4년 학사 Exit</span><span>5년 PharmD</span><span>5년차 유급 실무훈련</span></div></div>'''
        monash_routes='''<div class="monash-route-grid">
<article><span class="route-label">DIRECT</span><h3>고졸 → 약대 1학년</h3><ul><li><strong>2월 입학</strong></li><li>Chemistry + Mathematics 필수</li><li>IELTS 6.5 · 각 6.0</li><li>2027 국제학력 환산점수 확인 중</li></ul></article>
<article><span class="route-label">FOUNDATION</span><h3>Foundation → 약대 1학년</h3><ul><li><strong>약 12개월 · 2월/8월 시작</strong></li><li>현재 안내: Foundation 75%</li><li>English 65% · Maths/Chemistry 50%</li><li>2027 문서의 과정코드 차이로 진급점수 최종확인</li></ul></article>
<article><span class="route-label">GRADUATE ENTRY</span><h3>관련 학사 → 약대 3학년</h3><ul><li><strong>최근 10년 이내 관련 학사</strong></li><li>평균 70% 이상</li><li>대학 수준 Human Physiology</li><li>Summer intensive 후 3학년 진입</li></ul></article>
</div>'''
        monash_curriculum='''<div class="monash-curriculum-grid">
<article><span class="year">1학년</span><h3>약학 기초 + 임상적 사고 시작</h3><p>의약품과 인체를 이해하는 기초를 쌓고, 환자 중심 치료와 임상적 의사결정의 기본 틀을 배웁니다.</p></article>
<article><span class="year">2~3학년</span><h3>임상학습 + 현장실습</h3><p>Community·Hospital Pharmacy에서 구조화된 실습을 시작하고, 실제 환자 케어에 필요한 판단과 의사소통을 훈련합니다.</p></article>
<article><span class="year">4학년</span><h3>실습 심화 + BPharm(Hons) 완성</h3><p>현장실습을 이어가며 학사과정을 마칩니다. 여기까지 이수하면 BPharm(Hons)로 졸업할 수 있습니다.</p></article>
<article><span class="year">5학년</span><h3>유급 실무훈련 + ITP</h3><p>병원 또는 지역약국에서 유급 supervised practice를 진행하면서 Intern Training Program과 심화 선택과목을 이수합니다.</p></article>
</div><div class="monash-curriculum-focus"><strong>과정 전반의 핵심 역량</strong><span>임상적 의사결정 · 환자 중심 치료 · 디지털 헬스</span></div>'''
        monash_cost='''<div class="monash-money-grid">
<div><small>2027 연간 학비</small><strong>A$49,740</strong><span>48 credit points 기준</span></div>
<div><small>장학금 유형</small><strong>경쟁선발 · 연 8명</strong><span>25% 또는 50%</span></div>
<div><small>장학 유지</small><strong>WAM 70</strong><span>별도 장학신청 없음</span></div>
<div><small>Parkville 인근 쉐어</small><strong>A$290~380 / 주</strong><span>현재 공식 생활비 참고</span></div>
</div><div class="section-link-list compact-links">'''+link('/tuition-scholarships/','호주 약대 전체 학비·생활비 비교 →')+'''</div>
        monash_after='''<div class="monash-flow"><div><b>1~4년차</b><strong>BPharm(Hons)</strong><span>4년 후 학사로 졸업 가능</span></div><i>↓</i><div><b>5년차</b><strong>Doctor of Pharmacy</strong><span>유급 supervised practice + Intern Training Program</span></div><i>↓</i><div><b>호주 약사등록</b><strong>등록시험·심사 완료</strong><span>General Registration</span></div><i>↓</i><div><b>졸업비자</b><strong>기본 485 · 2년</strong><span>Melbourne은 Regional 추가기간 없음</span></div></div><div class="section-link-list compact-links">'''+link('/pharmacist-registration/','호주 약사등록 자세히 →')+link('/korea-pharmacist/','한국 약사면허 · 모나쉬는 기인정 대학 →')+'''</div>'''
        items=[('overview','모나쉬 약대 과정 구조',monash_overview),('routes','입학방법 3가지',monash_routes),('curriculum','5년 커리큘럼 한눈에 보기',monash_curriculum),('cost','학비·장학금·생활비',monash_cost),('after','5년 과정과 졸업 후',monash_after),('sources','자료 출처',sources(allids))]
        register(purl(p),'2027 모나쉬 약대 · 5년 PharmD·입학조건·학비 | TNS','모나쉬대학교 5년 Pharmacy/Doctor of Pharmacy 과정의 Direct·Foundation·Graduate Entry, 2027 학비·장학금과 졸업 후 약사등록을 간단히 정리합니다.',body+article(items,'monash-detail'))
    else:
        items=[('overview','이 약대 핵심',intro),('structure','과정·학위 구조',anatomy),('routes','입학방법',routes_html),('admission','Direct 입학조건','<h3>학력·성적</h3>'+qtable(pid)+'<h3>선수과목</h3>'+requirements_html+'<h3>영어</h3>'+english_html+'<h3>입학시기</h3>'+fv(it['label'])+'<p class="small">Foundation·Diploma 일정은 위 ‘입학방법’에서 바로 볼 수 있습니다.</p>'),('cost','학비·장학금·생활비','<h3>학비</h3>'+fees+'<h3>장학금</h3>'+scholarcards(ss)+'<h3>기숙사·숙소</h3>'+housingcards(hh)+'<h3>1년 예산</h3>'+costcalculator()),('poststudy','졸업 후 485·지역',poststudy_html(u)),('registration','호주 약사등록',registration_html),('korea','한국 약사면허','<p>호주 약대 졸업만으로 한국 약사면허가 자동으로 나오지 않습니다. 대학 인정, 호주 면허, 예비시험·국가시험을 따로 거칩니다.</p>'+link('/korea-pharmacist/','한국 약사면허 확인 순서 →','btn text')),('faq','자주 묻는 질문',faq(fs)),('sources','자료 출처',sources(allids))]
        register(purl(p),f'2027 {u["name_ko"]} 약대 완전분석 · 입학·학비·485 | TNS',u['name']+' Pharmacy의 과정기간, 입학방법, 선수과목, 학비·장학금, 인턴십, 485 지역조건과 약사등록을 정리합니다.',body+article(items),fs)

pathway_items=[('overview','호주 약대 입학방법 3가지','<p>고등학생은 보통 Foundation, Diploma, Direct Entry 세 가지 방법으로 시작합니다.</p><div class="admission-grid"><article class="admission-card"><span class="route-label">FOUNDATION</span><h3>고2 → Foundation → 약대 1학년</h3><p>고2 수료 후 Foundation을 마치고 약대 1학년으로 진학합니다.</p><a href="/foundation/">Foundation 자세히 →</a></article><article class="admission-card"><span class="route-label">DIPLOMA / IYO</span><h3>Diploma → 약대 2학년</h3><p>Griffith·Curtin은 Diploma 후 약대 2학년으로 진학합니다.</p><p class="route-exception">Adelaide: 학점 인정 학생 → 7월 입학 심사</p><a href="/diploma/">Diploma 자세히 →</a></article><article class="admission-card"><span class="route-label">DIRECT ENTRY</span><h3>성적으로 바로 약대 1학년</h3><p>수능·IB·A-level·SAT·OSSD와 선수과목·영어로 바로 지원합니다.</p><a href="/direct-entry/">Direct 대학 보기 →</a></article></div>'),('profiles','내 학력에서 바로 찾기',table([('고2 수료','Foundation'),('고3 졸업','Direct / Diploma'),('검정고시','Diploma / 일부 Direct'),('수능·IB·A-level·SAT·OSSD','Direct Entry')],['현재 학력','먼저 볼 방법'],True)),('graduate','대학 졸업자','<p>Graduate Entry는 일부 대학만 운영합니다. 학사학위와 대학 선수과목이 필요합니다.</p>'+link('/graduate-entry/','Graduate Entry 보기 →','btn text'))]
register('/admission-pathways/','2027 호주 약대 입학방법 · Foundation·Diploma·Direct | TNS','호주 약대에 진학하는 대표적인 세 가지 방법인 Foundation, 1학년 Diploma/IYO, Direct Entry를 학력별로 비교하고 대졸자 특수경로를 구분합니다.',pagehero('호주 약대 입학방법','내 학력에 맞는 입학방법을 고르면 지원 가능한 대학이 빠르게 좁혀집니다.','입학방법')+article(pathway_items))

direct_rows=[]
for p in D['programs']:
    u=U[p['university_id']];rq=one('requirements',p['id']);en=one('english',p['id']);it=one('intakes',p['id'])
    direct_rows.append((link(purl(p),E(u['short'])+(' · 신설 PharmD' if p['id']=='uq-pharmd' else '')),E(value(p['duration_label'])),fv(it['label']),fv(rq['chemistry']),fv(rq['mathematics']),fv(en['ielts_overall'])))
direct_items=[('schools','Direct 입학 가능한 약대',table(direct_rows,['대학','기간','입학월','화학','수학','IELTS'],True)),('scores','대학별 Direct 점수 보기','<p>수능·IB·A-level·SAT·OSSD 기준은 대학마다 다릅니다. 대학명을 누르면 해당 학교 점수표가 바로 열립니다.</p>'+link('/admission-requirements/','학력별 성적·선수과목 설명 →','btn text')),('other','Direct가 어렵다면','<div class="section-link-list"><a href="/foundation/">Foundation → 약대 1학년</a><a href="/diploma/">Diploma → 약대 2학년</a><a href="/graduate-entry/">Graduate Entry</a></div>')]
register('/direct-entry/','2027 호주 약대 Direct 입학 · 대학별 수능·IB·선수과목 | TNS','호주 약대 Direct Entry를 대학별 기간, 입학월, 화학·수학 선수과목과 IELTS 기준으로 비교하고 각 대학 상세페이지로 연결합니다.',pagehero('고졸 Direct로 호주 약대 가기','수능·IB·A-level·SAT·OSSD로 약대 1학년에 바로 지원하는 대학을 한눈에 봅니다.','Direct Entry')+article(direct_items))

admission_rows=[]
for p in D['programs']:
    rq=one('requirements',p['id']);en=one('english',p['id']);admission_rows.append((link(purl(p),E(U[p['university_id']]['short'])+(' PharmD' if p['id']=='uq-pharmd' else '')),fv(rq['chemistry']),fv(rq['mathematics']),fv(en['ielts_overall'])))
admit_items=[('read','입학조건은 4가지만 보면 됩니다','<div class="process-grid four">'+''.join(f'<div class="process-card"><span class="number">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n,t,d in [('1','성적','약대에 필요한 성적을 봅니다.'),('2','선수과목','수학·화학 등 필요한 과목을 봅니다.'),('3','영어','IELTS·PTE 전체점수와 각 영역을 봅니다.'),('4','입학시기','2월·7월 입학 여부를 봅니다.')])+'</div>'+callout('같은 시험도 대학마다 요구 점수가 다릅니다. 선수과목과 영어도 함께 맞춰야 합니다.')),
 ('qualifications','한국 학생의 학력별 출발점',table([('수능','대학별 수능 기준'),('IB / A-level / SAT','시험점수 + 수학·과학 과목'),('OSSD','Grade 12 과목 + 평균 기준'),('한국 내신 / 검정고시','Direct 가능 여부 + Foundation·Diploma')],responsive=True)),
 ('scores','2027 Direct 입학점수', '<h3>Sydney · Pharmacy 과정 행</h3>'+qtable('sydney-bpharm-hons')+callout('Sydney 점수는 Sydney Pharmacy에만 적용됩니다. 다른 대학은 각 학교의 공식 점수를 사용합니다.',True)),
 ('latest-scores','Griffith · 2026 참고','<p>Griffith는 현재 2026 국제가이드 점수를 참고값으로 표시합니다. 2027 Direct 점수가 발표되면 2027 기준으로 교체합니다.</p>'+qtable('griffith-bpharm-hons')),
 ('prerequisites','선수과목·영어 핵심 비교',table(admission_rows,['과정','화학','수학','IELTS overall'],True)+callout('영어는 각 영역 점수까지 봅니다. ‘선행지식’은 ‘필수과목’과 다릅니다.')),
 ('chemistry','화학을 안 배웠다면','<p>화학 미이수라면 JCU Direct를 먼저 볼 수 있습니다. 화학이 필요한 대학은 Foundation에서 과목을 보완합니다.</p>'+link('/compare/?chemistry=no','화학 미이수 조건으로 비교 →','btn')),
 ('next','다음 단계','<p>성적과 선수과목을 정리한 뒤 Direct, Foundation, Diploma를 비교하세요.</p><div class="section-link-list"><a href="/foundation/">Foundation 진급조건</a><a href="/diploma/">Diploma 학점인정</a><a href="/consult/">상담 준비</a></div>'+sources(['sydney','griffith-2026','jcu-guide','uq','monash','qut-guide','rmit','newcastle','canberra-2027','unisq-course']))]
register('/admission-requirements/','2027 호주 약대 입학조건 · 수능·IB·SAT·선수과목 | TNS','호주 약대의 학력별 Direct 입학조건, 수학·화학 선수과목과 영어 기준을 비교합니다. 일반 대학 최소기준과 약대 전용 조건을 구분합니다.',pagehero('호주 약대 입학조건','성적, 선수과목, 영어, 입학시기 네 가지만 보면 됩니다.','입학조건')+article(admit_items))

foundation_routes=[r for r in D['entry_routes'] if r['type']=='foundation']
foundation_items=[('difference','Foundation은 약대 입학 전 준비과정입니다','<p>고2 수료 후 Foundation을 마치고 약대 1학년으로 진학합니다. Foundation 입학조건과 약대 진급조건은 서로 다릅니다.</p><div class="route-mini"><span>Foundation 입학</span>→<span>지정 과목·영어 이수</span>→<span>약대 진급 기준 충족</span>→<span>약대 1학년</span></div>'),
 ('routes','어느 대학으로 연결되나요?',routecards(foundation_routes)),
 ('uq','UQ · 2월 Foundation → 7월 약대','<p>UQ College Accelerated Foundation은 2027년 2월 15일 시작해 7월 9일 끝납니다. UQ BPharm은 7월 26일 시작합니다.</p>'+callout('Foundation 입학, 필수과목, GPA·영어 기준을 모두 충족해야 약대로 올라갑니다.')+'<p>BPharm 공개 진급 기준은 GPA 5.0, Academic English 5입니다. 새 UQ PharmD로 같은 조건이 적용된다고 가정하지 않습니다.</p>'),
 ('monash','Monash · 2027 새 과정 코드 확인','<p>Monash Foundation의 새 약대 과정은 P6007입니다. 현재 웹페이지는 Foundation 75%·English 65%를 안내하지만 2027 PDF에는 이전 코드 P6001이 남아 있어, 이 점수는 최종 진급기준으로 확정하지 않았습니다.</p>'),
 ('check','준비할 것','<ul><li>고교 졸업/재학 증명과 학년별 성적표</li><li>희망 약대에 필요한 수학·과학 과목 조합</li><li>Foundation 영어조건과 약대 진급 영어조건</li><li>Foundation 시작일, 약대 시작일, 성적 발표일</li><li>Foundation과 약대의 학비·숙소 예산</li></ul>'+sources(source_ids(foundation_routes)|{'uq-calendar','uq-foundation','uq'}))]
register('/foundation/','호주 약대 파운데이션 · 2027 대학별 진급조건 | TNS','UQ Accelerated Foundation, Sydney USFP, Monash 등 Foundation 진급 성적·영어·과목·약대 시작시기를 정리합니다.',pagehero('Foundation으로 호주 약대 준비하기','고교 성적이나 선수과목이 부족하다면 Foundation부터 약대 진급까지 한 번에 보세요.','Foundation')+article(foundation_items))

dip=[r for r in D['entry_routes'] if r['type'] in ['diploma','other']]
dip_items=[('start','Diploma 후 어디로 올라가나요?','<div class="diploma-summary"><div><strong>Griffith</strong><span>Diploma → 약대 2학년</span></div><div><strong>Curtin</strong><span>Diploma → 약대 2학년</span></div><div><strong>Adelaide</strong><span>학점 인정 → 7월 입학</span></div></div><p>Griffith와 Curtin은 약대 2학년으로 연결됩니다. Adelaide는 학점이 인정된 국제학생을 7월 입학으로 개별 심사합니다.</p>'),('routes','대학별 Diploma 경로',routecards([r for r in dip if r['type']=='diploma'])),('griffith','Griffith','<p><strong>80CP를 인정받고 약대 2학년으로 진학합니다.</strong></p>'+table([('Diploma','80CP 인정','약대 2학년'),('남은 기간','T1 시작 3년','T2 시작 3.5년')],['항목','조건','결과'],True)),('curtin','Curtin','<p><strong>175 credits를 인정받고 약대 2학년으로 진학합니다.</strong></p><p>Stage 2 CWA 70%와 PHAR1002 추가 이수가 필요합니다.</p>'),('adelaide','Adelaide','<p><strong>학점이 인정된 국제학생은 7월 입학 심사를 받을 수 있습니다.</strong></p><p>인정 학점은 학생별로 심사합니다.</p>'),('other','그 밖의 경로','<p>RMIT Associate Degree는 1년 Diploma가 아닙니다. 별도 경로로 구분합니다.</p>'),('questions','자주 묻는 질문',faq([('Diploma를 마치면 약대 2학년으로 가나요?','Griffith와 Curtin은 약대 2학년으로 진학합니다. 정해진 성적과 과목은 반드시 충족해야 합니다.'),('Adelaide도 Diploma 후 2학년인가요?','Adelaide는 학점 인정 방식입니다. 학점 인정 학생을 7월 입학으로 개별 심사합니다.')])+sources(source_ids(dip)|{'adelaide'}))]
register('/diploma/','호주 약대 Diploma · Griffith·Curtin 2학년 진학 | TNS','Griffith와 Curtin의 Diploma 후 약대 2학년 진학, Adelaide의 학점 인정 후 7월 입학을 비교합니다.',pagehero('Diploma 후 약대 2학년','Griffith·Curtin은 Diploma 후 약대 2학년으로 진학합니다. Adelaide는 학점 인정 학생을 7월 입학으로 개별 심사합니다.','Diploma / IYO')+article(dip_items))

fee_rows=[]
for p in D['programs']:
 t=one('tuition',p['id']);fee_rows.append((link(purl(p),E(U[p['university_id']]['short'])+(' PharmD' if p['id']=='uq-pharmd' else '')),fv(t['annual'],money),fv(t['official_total'],money)))
scholarship_rows=[]
for s in D['scholarships']:
    av=s['amount']['value']
    amount='확인 중' if av is None else ' / '.join(str(x)+'%' for x in av) if isinstance(av,list) else str(av)+'%'
    pharmacy='약대 적용' if s['pharmacy_eligible']['value'] is True else '약대 제외' if s['pharmacy_eligible']['value'] is False else '약대 적용 확인 중'
    scholarship_rows.append((link(purl(university_programs(s['university_id'])[0]),E(U[s['university_id']]['short'])),E(s['name']),E(amount),E(ASSESS[s['assessment']]),E(pharmacy)))
cost_items=[('tuition','대학별 1년 학비',table(fee_rows,['과정','연간 학비','대학 공개 예상 총학비'],True)+callout('대학마다 연간 수강량이 달라 단순히 1년 학비 × 과정기간으로 총학비를 계산하지 않습니다.')),('scholarship-types','장학금은 수여 방식이 다릅니다','<div class="process-grid"><div class="process-card"><span class="number">01</span><h3>조건 충족 시 자동</h3><p>UniSQ처럼 조건을 맞추면 Admissions가 자동으로 반영하는 장학이 있습니다.</p></div><div class="process-card"><span class="number">02</span><h3>자동심사</h3><p>JCU·QUT·UTas·Curtin·Adelaide·La Trobe처럼 입학 지원서로 장학을 함께 심사하는 대학이 있습니다.</p></div><div class="process-card"><span class="number">03</span><h3>경쟁 선발</h3><p>UQ·Monash처럼 성적이 좋아도 다른 지원자와 경쟁하는 장학이 있습니다.</p></div></div>'),('scholarships','대학별 장학금 한눈에 보기',table(scholarship_rows,['대학','장학금','금액','심사','약대'],True)+callout('Newcastle의 2027 International Excellence Scholarship 20%는 Bachelor of Pharmacy (Honours)가 제외과정입니다. UNSW International Student Award 20%는 현재 한국 국적이 대상 국가에 포함되지 않습니다.')),('housing','기숙사·숙소비',housingcards(D['accommodation'])+'<p class="small">금액이 공개된 숙소는 실제 주당·계약기간을 표시하고, 2027 요금이 아직 없는 학교는 최신 공식자료의 연도와 상태를 그대로 보여줍니다.</p>'),('calculator','1년 예산 계산',costcalculator()),('sources','자료 기준',sources(source_ids(D['tuition']+D['scholarships']+D['accommodation'])))]
register('/tuition-scholarships/','2027 호주 약대 학비·장학금·숙소 비교 | TNS','16개 호주 약대의 1년 학비, 2027 국제학생 장학금, 기숙사·숙소비를 대학별로 정리하고 1년 예산을 계산합니다.',pagehero('호주 약대 학비·장학금','대학별 학비와 장학금, 실제 숙소비를 같은 페이지에서 확인하세요.','학비·장학금')+article(cost_items))

reg_items=[('steps','호주 약사가 되는 순서','<p>재학 중 실습과 약사등록용 인턴십은 다릅니다. 학교에 따라 등록 준비 일부를 학위 안에서 끝낼 수 있습니다.</p><ol class="timeline">'+''.join(f'<li><strong>{t}</strong>{d}</li>' for t,d in [('승인된 학위·교육요건 확인','APC 인증·Pharmacy Board 승인 과정으로 졸업합니다.'),('Provisional registration','등록용 인턴십을 시작하기 전에 Provisional registration을 받습니다.'),('Supervised practice + Intern Training','감독 실무와 인정된 Intern Training Program을 이수합니다.'),('Written / Oral examinations','필요한 Written / Oral registration examination을 통과합니다.'),('General registration','교육·실무·시험 요건을 마치고 General Registration을 신청합니다.')])+'</ol>'+callout('인턴십 시간·시험·등록 영어기준은 졸업 시점의 Pharmacy Board 규정을 적용합니다.',True)),('integrated','5년 과정도 인턴십 방식이 다릅니다',table([(link('/universities/monash-pharmacy/','Monash'),'4년 학사 Exit · 5년 통합','5년차 supervised practice / ITP 통합 · 등록시험·심사 별도'),(link('/universities/sydney-pharmacy/','Sydney'),'5년 BPharm(Hons) / MPharmPractice','실무·인턴 과정 포함 · 4년 후 학사 Exit'),(link('/universities/unsw-pharmacy/','UNSW'),'2027 PharmD 명칭 전환','졸업 후 인턴십 따로'),(link('/universities/uq-pharmacy/#uq-pharmd','UQ 신설 PharmD'),'기존 BPharm과 별도 5년 과정','인턴십 통합 설계 · APC/Board 승인 아직 미획득')],['과정','학위구조','등록 준비'],True)),('accreditation','APC 인증 상태','<p>APC의 2026년 7월 8일 목록을 기준으로 합니다. ‘Accredited with conditions’도 정식 인증 상태이며 갱신 조건이 붙습니다.</p><p>UQ 신설 PharmD는 아직 APC·Pharmacy Board 승인을 받지 않았습니다. UNSW 새 PharmD 명칭과 Newcastle 갱신 상태는 최신 공식 목록에 맞춰 반영합니다.</p>'),('korea','한국 약사면허는 별도 절차','<p>호주 일반등록과 한국 약사면허는 다른 심사 체계입니다. 한국으로 돌아갈 계획이라면 입학 전에 대학 인정기준과 외국 면허·시험 요건을 따로 확인하세요.</p>'+link('/korea-pharmacist/','한국 약사면허 경로 →','btn text')+sources(['apc','apc-exam','board','monash','sydney-guide','unsw','uq-pharmd']))]
register('/pharmacist-registration/','호주 약사 되는 과정 · 학위·인턴십·등록시험 | TNS','호주 약사등록의 학위, provisional registration, supervised practice, intern training, 시험과 general registration을 구분합니다.',pagehero('학위 취득부터 호주 약사등록까지','3년 학사, 4년 학사, 5년 통합학위가 등록 준비의 어느 단계까지 포함하는지 확인하세요.','호주 약사등록')+article(reg_items))

# Korean pharmacist licence: recognized Australian schools + current exam route.
korea_school_rows=[]
for i,s in enumerate(K['recognized_schools'],1):
    ko=E(s['ko']);en=E(s['en'])
    if s.get('id') in U:
        school=link('/universities/'+U[s['id']]['slug']+'/',f'<strong>{ko}</strong><br><span class="small">{en}</span>')
    else:
        school=f'<strong>{ko}</strong><br><span class="small">{en}</span>'
    if s.get('legacy'):school+=f'<br><span class="fact-note">기인정 데이터의 과거 교명: {E(s["legacy"])}</span>'
    if s.get('note'):school+=f'<br><span class="fact-note">{E(s["note"])}</span>'
    korea_school_rows.append((str(i),school))

recognized_html='<p><strong>공식 명칭은 “보건복지부장관이 인정하는 외국학교”입니다.</strong> 2026년 6월 2일 국시원 공개자료 기준, 이미 인정된 호주 약대는 13곳입니다.</p>'
recognized_html+=callout('<strong>기인정 대학 졸업 + 호주 약사면허</strong>를 갖추면 별도의 외국학교 인정심사 없이 약사 예비시험으로 넘어갑니다. 목록에 없는 대학은 외국학교 인정심사를 먼저 받습니다.')
recognized_html+=table(korea_school_rows,['번호','기인정 호주 약대'],True)
recognized_html+=callout('<strong>Adelaide University는 기존 UniSA 인정과 자동으로 같지 않습니다.</strong><br>기인정 목록에는 University of South Australia가 들어 있지만 Adelaide University는 2026년에 출범한 새 법인입니다. 2027 Adelaide Pharmacy는 국시원 인정 여부를 별도로 확인해야 합니다.',True)

roadmap_html='<p>한국 약사면허 경로는 <strong>인정 대학 → 호주 약사면허 → 약사 예비시험 → 약사 국가시험 → 한국 약사면허</strong> 순서입니다.</p>'
roadmap_html+='<ol class="timeline"><li><strong>기인정 호주 약대 또는 외국학교 인정심사</strong>기인정 대학이면 바로 다음 단계로, 미등재 대학이면 외국학교 인정심사를 먼저 진행합니다.</li><li><strong>호주 약사면허 취득</strong>호주에서 요구하는 supervised practice·ITP·시험·General Registration을 완료합니다.</li><li><strong>약사 예비시험 합격</strong>약학 기초와 한국어 요건을 충족합니다.</li><li><strong>약사 국가시험 합격</strong>생명약학·산업약학·임상·실무약학·보건·의약 관계 법규를 응시합니다.</li><li><strong>한국 약사면허 교부</strong>국가시험 합격 후 한국 약사면허 교부를 신청합니다.</li></ol>'

pre=K['preliminary_exam']
prelim_rows=[
 ('응시원서 접수',E(pre['application']),f'응시수수료 {E(pre["fee"])}'),
 ('시험',E(pre['exam_date']),E(pre['locations'])),
 ('합격자 발표',E(pre['result_date']),'국시원 홈페이지 합격자조회')
]
prelim_html=f'<p><strong>{E(pre["title"])}</strong> 기준 일정입니다.</p>'+table(prelim_rows,['구분','일정','비고'],True)
prelim_html+=facts([('시험과목',E(' · '.join(pre['subjects']))),('합격기준',E(pre['pass_rule']))])
prelim_html+='<p class="small">한국어는 국시원 지정 한국어능력시험 기준을 충족하거나 법령상 면제요건에 해당해야 합니다.</p>'

nat=K['national_exam']
national_rows=[
 ('응시원서 접수',E(nat['application']),'외국대학 졸업자는 약사 예비시험 합격자에 한해 인터넷 접수 가능'),
 ('시험',E(nat['exam_date']),'시험장소는 국시원 별도 공고'),
 ('최종합격자 발표',E(nat['result_date']),'국시원 홈페이지 합격자조회')
]
national_html=f'<p><strong>{E(nat["title"])}</strong> 현재 공개 일정입니다.</p>'+table(national_rows,['구분','일정','비고'],True)
national_html+=facts([('시험과목',E(' · '.join(nat['subjects']))),('합격기준',E(nat['pass_rule']))])
national_html+=callout('약사 예비시험에 합격하면 다음 회의 약사국가시험부터 예비시험이 면제됩니다. 시험장소와 수수료는 국시원 해당 연도 공고를 따릅니다.')

korea_items=[
 ('recognized','보건복지부장관 인정 호주 약대 13곳',recognized_html),
 ('roadmap','호주 약대에서 한국 약사면허까지',roadmap_html),
 ('preliminary','약사 예비시험 · 2026 일정과 합격기준',prelim_html),
 ('national','약사 국가시험 · 2027 일정과 시험과목',national_html),
 ('documents','입학 전·응시 전 확인할 자료','<ul><li>입학 예정 대학의 정확한 법인명·학위명·캠퍼스·입학연도</li><li>학년별 교육과정과 실제 이수 방식</li><li>호주 약사 General Registration 및 면허 증빙</li><li>외국학교 인정심사 필요 여부</li><li>예비시험 한국어 요건과 해당 연도 원서접수 서류</li></ul><p>기인정 목록은 인정심사 신청 당시의 국가·교명을 바탕으로 만들어져 현재 교명과 다를 수 있고, 인정심사 기간 중 학교가 추가될 수도 있습니다.</p>'+sources(['korea-recognized-schools-20260602','korea-foreign-school-process','korea-pharmacist-exam-current','korea-pharmacist-exam-law','korea-law','adelaide-new-entity-2026']))
]
register('/korea-pharmacist/','보건복지부 인정 호주 약대 13곳 · 약사 예비시험·국가시험 | TNS','2026년 6월 2일 국시원 공개자료 기준 보건복지부장관 인정 호주 약대 13곳과 호주 약사면허 취득 후 한국 약사 예비시험·국가시험 일정과 합격기준을 정리합니다.',pagehero('보건복지부 인정 호주 약대와 한국 약사면허','기인정 호주 약대 13곳, 호주 약사면허, 약사 예비시험과 국가시험까지 한국 복귀 경로를 순서대로 확인하세요.','한국 약사면허')+article(korea_items))

fastitems=[('programs','3년 Fast-track · JCU와 UTas','<p>JCU와 UTas는 4년 약학과를 3년에 압축해 공부합니다. 1년 수강량이 많고 학업 일정이 빠릅니다.</p><div class="card-grid">'+card(P['jcu-bpharm-hons'])+card(P['utas-bpharm-hons'])+'</div>'),('uq','UQ의 7월 약 3.5년과 구분','<p>UQ 기존 BPharm은 2월 4년, 7월 약 3.5년입니다. 3년 Fast-track과 동일한 상품이 아니며, 수학·화학 요건과 7월 모집 여부를 함께 봐야 합니다.</p>'),('registration','학업기간 이후의 등록 준비','<p>3년 학위 수료 후에도 등록용 인턴십과 ITP·등록시험 등 요구가 남습니다. 5년 통합과 비교할 때는 학위만의 기간과 전체 등록 준비기간을 구분하세요.</p>'+link('/pharmacist-registration/','등록 구조 자세히 →','btn text')+sources(['jcu-guide','utas','uq','apc']))]
register('/3-year-pharmacy/','호주 3년 약대 · JCU·UTas Fast-track 비교 | TNS','호주 3년 약대 JCU·UTas의 압축 학사와 UQ 7월 3.5년 경로를 구분하고, 졸업 후 약사등록 준비기간을 확인합니다.',pagehero('호주 3년 약대, 빠른 만큼 확인할 것','3년 학위 완료와 약사등록 완료는 다릅니다. 압축 학사 일정과 졸업 후 준비를 함께 살펴보세요.','3년 약대')+article(fastitems))

method_items=[('scope','이 사이트의 비교 범위','<p>한국 학생이 고교 졸업 후 학부 단계부터 약사 과정을 시작할 수 있는 대학을 중심으로 구성합니다. 대학원 전용 과정과 국제학생 대면 모집 확인이 안 된 상품을 확정 진학 옵션으로 표시하지 않습니다.</p>'),('status','정보 상태 읽는 방법',table([(status({'status':s},force=True),t) for s,t in [('confirmed_2027','2027 공식 자료에서 해당 사실을 확인했습니다. 최종 입학허가를 뜻하지 않습니다.'),('latest_published','현재 확인한 최신 공개 자료입니다. 연도가 이전이면 명시하며 2027 확정으로 사용하지 않습니다.'),('pending_2027','2027 확인 중 상태입니다. 미발표, 접근 제한, 적용범위 미검증 또는 본 작업의 대조 미완료를 포함하며 공식 자료가 없다고 단정하지 않습니다.'),('source_conflict','공식 자료 간 수치·적용 범위 차이가 남아 있습니다. 자동 충족 판정에 사용하지 않습니다.')]],['상태','의미'],True)),('conflicts','자료 차이와 후속 확인',table([(E(c['summary']),E(c['decision'])) for c in D['conflicts']],responsive=True)),('order','자료 우선순위','<p>최신 대학 course page·official admissions guide, APC·Pharmacy Board, 정부 자료를 우선합니다. 일반 입학 최소기준을 약대 전용 기준으로 대체하지 않으며, 프로그램 코드가 바뀐 경우 이전 점수를 이식하지 않습니다.</p>'),('limits','현재 검증이 남은 범위','<p>여러 대학의 CSAT·SAT·IB·OSSD 환산, 내신·검정고시 인정, 준비과정별 진급조건, 장학 제외목록, 공식 숙소 요금이 확인 중입니다. 비교 결과에서는 해당 조건을 충족으로 간주하지 않습니다.</p><p>호주 전용 오픈채팅은 검증된 TNS 채널만 연결합니다.</p>')]
register('/methodology/','자료 기준·2027 업데이트 상태 | TNS 호주약대','호주 약대 정보의 출처 우선순위, 2027 확정·참고·확인 중·자료 차이 상태와 검증이 남은 범위를 설명합니다.',pagehero('자료 기준과 업데이트 상태','비교에 쓰이는 숫자가 어느 연도, 어느 과정의 조건인지 확인할 수 있도록 관리합니다.','자료 기준')+article(method_items))

consult_items=[('prepare','상담 전에 준비하면 좋은 정보','<p>성적표 전체를 공개 공간에 올릴 필요는 없습니다. 먼저 아래 항목을 정리하고, 구체적인 서류 제출은 상담 채널에서 안내받으세요.</p><ul><li>최종 학력과 졸업 예정일</li><li>수능·IB·SAT·A-level·내신 등 보유 성적</li><li>화학·수학·생물·물리 이수 과목과 성적</li><li>영어시험 종류·시험일·overall·각 영역 점수</li><li>희망 입학시기, 준비과정 가능 여부, 예산</li></ul>'),('summary','상담 메모 만들기','<p>아래 메모는 브라우저에서만 작성됩니다. 복사 후 원하는 상담 채널에 직접 전달하세요.</p><div class="consult-prep"><label for="consult-note">상담 메모<textarea id="consult-note">최종 학력 / 졸업 예정일:\n보유 학업 성적:\n수학·화학 등 이수 과목:\n영어 overall / 각 영역:\n희망 입학시기:\n관심 대학 / 입학방법:\n예산 / 궁금한 점:</textarea></label><div><button class="btn" id="copy-note">메모 복사</button></div><p class="small" id="copy-status" role="status"></p></div>')]
register('/consult/','TNS 호주 약대 상담 준비 | 학력·성적·입학방법','TNS 호주 약대 상담 전 학력, 성적, 선수과목, 영어점수, 입학시기를 정리하고 상담 채널로 연결합니다.',pagehero('내 조건으로 상담 준비하기','지금 가능한 입학방법과 앞으로 준비할 조건을 정리합니다.','TNS 상담')+article(consult_items))
register('/privacy/','개인정보 안내 | TNS 호주약대','이 사이트의 조건 비교와 상담 메모 처리 방식을 안내합니다.',pagehero('개인정보 안내','V1 조건 비교 기능의 정보 처리 범위입니다.','개인정보')+article([('filter','조건 비교와 상담 메모','<p>필터, 성적 입력, 예산 계산, 상담 메모는 사용자의 브라우저 안에서 처리되며 이 사이트의 서버로 전송되지 않습니다. 현재 별도의 분석 도구나 상담 접수 폼은 설치하지 않았습니다.</p><p>비교함의 과정 ID만 브라우저 sessionStorage에 저장하여 페이지 이동 중 선택을 유지합니다. 성적·상담 메모는 저장하지 않습니다.</p>'),('external','외부 상담 채널','<p>카카오톡·네이버 카페·전화 링크를 이용하면 해당 서비스로 이동합니다. 그 서비스에 직접 입력한 개인정보에는 해당 서비스와 상담 운영자의 정책이 적용됩니다. 운영자 개인정보처리방침과 상세 문의 창구는 공개 운영 전 확정해야 합니다.</p>')]))
register('/404/','페이지를 찾을 수 없습니다 | TNS 호주약대','요청한 페이지가 없습니다. 전체 약대 비교에서 원하는 과정을 찾아보세요.',pagehero('페이지를 찾을 수 없습니다','주소를 확인하거나 전체 약대 비교에서 다시 시작해 주세요.','404')+'<div class="section wrap"><a class="btn" href="/compare/">전체 약대 비교 →</a></div>')

def serialize_data(path,offline=False):
    result=[]
    for p in D['programs']:
        r=dict(p);r['university']=U[p['university_id']];r['url']=purl(p)+('#uq-pharmd' if p['id']=='uq-pharmd' else '')
        if offline:r['url']=offline_url(r['url'],path)
        for coll in ['requirements','english','intakes','tuition','professional_registration']:r[coll]=one(coll,p['id'])
        for coll in ['qualifications','entry_routes']:r[coll]=related(coll,p['id'])
        for coll in ['scholarships','accommodation']:r[coll]=related(coll,u=p['university_id'])
        result.append(r)
    def client_view(obj):
        if isinstance(obj,dict):
            if 'value' in obj and 'status' in obj:return {k:obj[k] for k in ['value','status','source_year']}
            return {k:client_view(v) for k,v in obj.items()}
        if isinstance(obj,list):return [client_view(v) for v in obj]
        return obj
    return json.dumps(client_view(result),ensure_ascii=False,separators=(',',':')).replace('<',chr(92)+'u003c')
def offline_url(url,path):
    if not url.startswith('/') or url.startswith('//'):return url
    from urllib.parse import urlsplit
    z=urlsplit(url);target=z.path.lstrip('/')
    if not Path(target).suffix:target=target.rstrip('/')+'/index.html' if target else 'index.html'
    rel=os.path.relpath(target,path.lstrip('/') or '.')
    return rel+('?' +z.query if z.query else '')+('#'+z.fragment if z.fragment else '')
def render(path,page,offline=False):
    canonical=BASE+path
    schemas=[{'@context':'https://schema.org','@type':'WebPage','name':page['title'],'description':page['description'],'url':canonical,'inLanguage':'ko-KR','dateModified':DATE,'publisher':{'@type':'Organization','name':'TNS'}}, {'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'홈','item':BASE+'/'},{'@type':'ListItem','position':2,'name':page['title'].split(' | ')[0],'item':canonical}]}] if path!='/' else [{'@context':'https://schema.org','@type':'WebSite','name':'TNS 호주약대 가이드','url':BASE+'/','inLanguage':'ko-KR'}]
    if page['faqs']:schemas.append({'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in page['faqs']]})
    robots='index,follow' if PRODUCTION and path!='/404/' else 'noindex,nofollow'
    html=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(page['title'])}</title><meta name="description" content="{E(page['description'])}"><meta name="robots" content="{robots}"><link rel="canonical" href="{E(canonical)}"><meta name="theme-color" content="#123f45"><meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:title" content="{E(page['title'])}"><meta property="og:description" content="{E(page['description'])}"><meta property="og:url" content="{E(canonical)}"><meta property="og:site_name" content="TNS 호주약대 가이드"><meta property="og:image" content="{BASE}/assets/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="2027 호주 약대 비교 · TNS"><meta name="twitter:card" content="summary_large_image"><link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="stylesheet" href="/assets/styles.css"><script type="application/ld+json">{json.dumps(schemas,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script></head><body>{header(path)}<main id="main">{page['body']}</main>{footer()}{drawer()}<script type="application/json" id="program-data">{serialize_data(path,offline)}</script><script defer src="/assets/matcher.js"></script><script defer src="/assets/app.js"></script></body></html>'''
    if offline:
        html=re.sub(r'(href|src|action)="(/[^\"]*)"',lambda m:m[1]+'="'+E(offline_url(m[2].replace('&amp;','&'),path))+'"',html)
    return html
for path,page in pages.items():
    for directory,offline in [(OUT,False),(OFF,True)]:
        target=directory/path.lstrip('/')/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(render(path,page,offline))
shutil.copyfile(OUT/'404/index.html',OUT/'404.html')
shutil.copyfile(OFF/'404/index.html',OFF/'404.html')
(OUT/'robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+BASE+'/sitemap.xml\n' if PRODUCTION else 'Disallow: /\n'))
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{esc(BASE+path)}</loc><lastmod>{DATE}</lastmod></url>' for path in pages if path!='/404/')+'</urlset>')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n'+('' if PRODUCTION else '  X-Robots-Tag: noindex, nofollow\n'))
(OUT/'_redirects').write_text('/index.html / 301\n')
(ROOT/'docs/pages.json').write_text(json.dumps([{'path':p,'title':v['title']} for p,v in pages.items()],ensure_ascii=False,indent=2))
print(f'Built {len(pages)} pages + offline mirror. Mode={MODE}; canonical={BASE}; production={PRODUCTION}')

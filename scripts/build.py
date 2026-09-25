"""Dependency-free static build. Every factual page is complete without JavaScript."""
from pathlib import Path
from html import escape as esc
import json, os, re, shutil, sys
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/catalog.json').read_text()); C=json.loads((ROOT/'data/site.json').read_text())
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

STATUS={'confirmed_2027':'2027 확인','latest_published':'최신 공개','pending_2027':'2027 발표 대기','source_conflict':'자료 차이'}
QUAL={'csat':'수능 CSAT','ib':'IB','alevel':'A-level','sat':'SAT','ossd':'OSSD','korean_high_school':'한국 일반고 내신','ged':'검정고시','other':'기타 국제학교 자격','graduate':'대학 졸업'}
ROUTE={'direct':'Direct Entry','foundation':'Foundation','diploma':'Diploma / IYO','graduate':'Graduate Entry','other':'기타 입학방법'}
MAIN_ROUTE={'foundation':'Foundation','diploma':'1학년 Diploma / IYO','direct':'Direct Entry'}
PREREQ={'required':'필수','recommended':'권장','not_required':'필수 아님','accepted':'인정','assumed':'선행지식 · 브리징 가능'}
ASSESS={'automatic':'자동심사형','application':'신청·서류심사형','competitive':'경쟁형','guaranteed':'보장형','not_eligible':'한국 국적 대상 아님','pending':'적용 확인 중'}
pages={}
def E(x):return esc(str(x),quote=True)
def value(f,default='확인 중'):
    v=f.get('value') if isinstance(f,dict) else f
    if v is None:return default
    if isinstance(v,bool):return '예' if v else '아니요'
    if isinstance(v,list):return ' / '.join(map(str,v))
    if isinstance(v,dict):return ' · '.join(f'{k} {v}' for k,v in v.items())
    return PREREQ.get(str(v),str(v))
def money(f):return f"A${f['value']:,.0f}" if f.get('value') is not None else '2027 업데이트 대기'
def status(f):
    s=f.get('status','pending_2027');year=f.get('source_year')
    label=STATUS[s]+(f' · {year}' if s=='latest_published' and year else '')
    return f'<span class="status {s}">{label}</span>'
def fv(f,fmt=None):
    t=fmt(f) if fmt else value(f)
    note=f'<span class="fact-note">{E(f["note"])}</span>' if f.get('note') else ''
    return f'{E(t)}<br>{status(f)}{note}'
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
    rows=''.join(f'<li><a href="{E(S[s]["url"])}" target="_blank" rel="noopener noreferrer">{E(S[s]["title"])} ↗</a> · {"확인 " + S[s]["verified_date"] if S[s].get("verified_date") else "원문 재확인 필요"}</li>' for s in sorted(set(ids)) if s in S)
    return f'<details class="sources"><summary>자료 출처 · 확인 기준일 {DATE}</summary><p class="small">2027 자료, 이전 연도 참고값, 확인 중인 항목을 구분합니다. 링크는 새 창에서 열립니다.</p><ul>{rows}</ul></details>'
def faq(items):return '<div class="faq">'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in items)+'</div>'
def pagehero(title,desc,crumb='가이드',extra=''):
    return f'<section class="page-hero"><div class="wrap"><nav class="breadcrumbs" aria-label="현재 위치"><a href="/">홈</a><span>/</span><span>{E(crumb)}</span></nav><span class="eyebrow">2027 AUSTRALIA PHARMACY GUIDE</span><h1>{title}</h1><p>{desc}</p>{extra}</div></section>'
def article(items):
    toc='<aside class="toc"><strong>이 페이지에서</strong>'+''.join(link('#'+id,E(title)) for id,title,_ in items)+'</aside>'
    return '<div class="section"><div class="wrap content-grid">'+toc+'<div>'+''.join(section(*x) for x in items)+'</div></div></div>'
def register(path,title,desc,body,faqs=None):pages[path]=dict(title=title,description=desc,body=body,faqs=faqs or [])
def logo():return '<svg class="brand-symbol" viewBox="0 0 48 48" aria-hidden="true"><path d="M24 1 47 24 24 47 1 24Z" fill="#e1b63f"/><text x="24" y="28" text-anchor="middle" font-size="12" font-weight="800" font-family="Arial,sans-serif" fill="#fff">TNS</text></svg>'
def header(path):
    links=[('/universities/','대학별 약대'),('/admission-pathways/','입학방법'),('/tuition-scholarships/','학비·장학금'),('/pharmacist-registration/','약사등록'),('/after-graduation/','졸업 후')]
    nav=''.join(f'<a href="{u}"'+(' aria-current="page"' if path==u else '')+f'>{t}</a>' for u,t in links)
    return f'<a class="skip" href="#main">본문 바로가기</a>'+('' if PRODUCTION else '<div class="preview-bar">V1 Preview · 2027 미발표 정보는 ‘발표 대기’로 표시합니다</div>')+f'<header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="TNS 호주약대 가이드 홈">{logo()}<span class="brand-title">호주약대 가이드<small>BY TNS · AUSTRALIA</small></span></a><button class="menu-toggle" aria-expanded="false" aria-controls="main-nav">메뉴</button><nav class="nav" id="main-nav" aria-label="주 메뉴">{nav}<a class="nav-cta" href="/consult/">TNS 상담 ↗</a></nav></div></header>'
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
    first+=select('intake','희망 입학시기',[('','상관없음'),('2','2월'),('7','7월')])
    first+=select('duration','과정 기간',[('','상관없음'),('fast','빠른 과정'),('4','4년'),('5','5년 통합')])
    advanced=select('route','입학방법',[('','전체')]+list(MAIN_ROUTE.items()))
    advanced+=select('structure','학위·인턴십',[('','전체'),('exit','4년 Exit 가능'),('integrated','Internship 학위 내 통합')])
    advanced+=select('science','선수과목',[('','전체'),('chemistry','화학 필수'),('mathematics','수학 필수'),('biology','Biology 인정')])
    advanced+=select('english','영어 기준',[('','전체'),('6.5','IELTS overall 6.5 이하'),('7','IELTS overall 7.0 이하'),('pte','PTE 기준 공개')])
    advanced+=select('cost','비용·장학금',[('','전체'),('scholarship','한국학생 약대 적용 장학 확인'),('20','20% 이상 장학'),('housing','공식 숙소 주 A$350 이하')])
    advanced+='<label class="score-field" hidden>성적 <span id="score-scale"></span><input name="score" type="number" min="0" step="any" inputmode="decimal" aria-describedby="score-help" placeholder="점수 입력 (선택)"></label>'
    more=f'<details class="advanced"><summary>상세필터 · 입학방법, 영어, 비용·장학금</summary><div class="filter-grid advanced-grid">{advanced}</div><p class="filter-note" id="score-help">같은 시험도 대학마다 점수 계산법이 다릅니다. 영어는 전체점수와 각 영역 점수를 함께 봅니다.</p></details>'
    if home:more=''
    return f'''<form class="finder {'home-finder' if home else ''}" id="finder" action="/compare/" method="get" data-mode="{'navigate' if home else 'filter'}"><div class="finder-title"><h2>내 조건으로 호주약대 찾기</h2><p>간단한 조건부터 시작하세요</p></div><div class="filter-grid">{first}</div>{more}<div class="finder-actions"><p>아직 발표되지 않은 조건은 ‘정보 대기’로 표시합니다.<br>검색 결과는 합격 보장이 아닙니다.</p><div class="button-row">{'' if home else '<button type="reset" id="reset-filters">초기화</button>'}<button class="btn" type="submit">가능한 약대 보기 <span aria-hidden="true">→</span></button></div></div></form>'''
def card(p):
    u=U[p['university_id']];pid=p['id'];fee=one('tuition',pid)['annual'];en=one('english',pid);rq=one('requirements',pid);it=one('intakes',pid)
    e='확인 중' if en['ielts_overall']['value'] is None else 'IELTS '+str(en['ielts_overall']['value']).removesuffix('.0')
    if en['ielts_overall']['status'] in ['source_conflict','pending_2027']:e+=' · 재확인'
    elif en['ielts_overall']['source_year']==2026:e+=' · 2026 참고'
    elif en['ielts_overall']['value'] is not None:e+=' · 영역별 별도'
    chips=''.join(f'<span class="chip">{E(t)}</span>' for t in p['highlights'])
    name=u['name_ko']+(' · 신설 PharmD' if pid=='uq-pharmd' else '')
    warn='<div class="notice-inline">신설 과정: APC 인증·Board 승인 대기</div>' if pid=='uq-pharmd' else '<div class="notice-inline">2027 모집 발표 대기</div>' if p['international_recruitment']['value'] is None else ''
    return f'''<article class="university-card" data-program="{pid}"><div class="card-top"><div class="card-location"><span>{E(value(u['campus']))}</span><span class="school-monogram">{E(u['short'])}</span></div><h3>{E(name)}<span class="school-en">{E(u['name'])}</span></h3><div class="chips">{chips}</div><p class="degree-name">{E(value(p['name']))}</p></div>{warn}<dl class="card-facts"><dt>과정</dt><dd>{E(value(p['duration_label']))}</dd><dt>영어</dt><dd>{E(e)}</dd><dt>화학</dt><dd>{E(value(rq['chemistry']))}</dd><dt>연간 학비</dt><dd>{E(money(fee))}{' · '+str(fee['source_year']) if fee['value'] is not None else ''}</dd></dl><div class="match-reason" hidden></div><div class="card-bottom"><a href="{purl(p)}{'#uq-pharmd' if pid=='uq-pharmd' else ''}">입학조건 보기 →</a><label class="compare-toggle"><input type="checkbox" data-compare="{pid}" aria-label="{E(name)} 비교에 추가"> 비교</label></div></article>'''

REGIONAL_485={
 'jcu':dict(category='Category 3',area='Townsville · Cairns · Mackay',extra='두 번째 485 +2년 가능',total='요건 충족 시 총 4년'),
 'utas':dict(category='캠퍼스별 다름',area='Hobart: Category 2 · Launceston/Cradle Coast: Category 3',extra='Hobart +1년 · Launceston/Cradle Coast +2년',total='요건 충족 시 총 3~4년'),
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
    return ' · '.join('2월' if x==2 else '7월' if x==7 else str(x)+'월' for x in mm) if mm else '발표 대기'
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
    return ' / '.join(dict.fromkeys(vals)) if vals else '업데이트 대기'
def directory_card(u):
    ps=university_programs(u['id'])
    duration=' / '.join(dict.fromkeys(value(p['duration_label']) for p in ps))
    region=REGIONAL_485[u['id']]
    headline=E(ps[0]['editorial'])
    return f'''<article class="pharmacy-school-card"><div class="school-card-head"><div><span class="school-state">{E(u['state'])} · {E(region['area'])}</span><h3>{E(u['name_ko'])}<small>{E(u['name'])}</small></h3></div><span class="school-monogram large">{E(u['short'])}</span></div><p class="school-summary">{headline}</p><div class="path-badges">{pathway_badges(u['id'])}</div><dl class="school-keyfacts"><div><dt>과정</dt><dd>{E(duration)}</dd></div><div><dt>입학</dt><dd>{E(intake_text(u['id']))}</dd></div><div><dt>인턴십</dt><dd>{E(internship_label(u['id']))}</dd></div><div><dt>485</dt><dd>{E(region['total'])}</dd></div></dl><a class="school-detail-link" href="/universities/{E(ps[0]['id'].replace('-bpharm-hons','').replace('-pharmd',''))}-pharmacy/" data-fallback="{E(purl(ps[0]))}">이 약대 상세분석 →</a></article>'''
def poststudy_html(u):
    r=REGIONAL_485[u['id']]
    return facts([('약대 캠퍼스',E(r['area'])),('485 기본기간','2년'),('지역 분류',E(r['category'])),('지역 추가 485',E(r['extra'])),('가능 총기간',E(r['total'])),('주정부',E(u['state'])+' 주 기준 별도 업데이트')])+callout('지역 추가 485는 자동으로 받는 기간이 아닙니다. 지역캠퍼스 졸업, 첫 485 기간 중 지역 거주 등 Second Post-Higher Education Work stream 요건을 충족해야 합니다.')+link('/after-graduation/','485·Regional 기준 자세히 →','btn text')

home=f'''<section class="hero school-first-hero"><div class="wrap hero-grid"><div><span class="eyebrow">2027 AUSTRALIA PHARMACY GUIDE</span><h1>호주 약대는<br><em>학교마다 다릅니다.</em></h1><p class="hero-copy">약대 수는 많지 않지만 과정은 제각각입니다.<br>3년·4년·5년, 2월·7월 입학, Foundation·Diploma,<br>인턴십과 졸업 후 485 지역조건까지 대학별로 봐야 합니다.</p><div class="button-row"><a class="btn" href="#all-schools">대학별 약대 보기 <span>↓</span></a><a class="btn secondary" href="/admission-pathways/">입학방법으로 보기 →</a></div><div class="hero-meta"><span>{len(U)}개 대학</span><span>{len(P)}개 학부 시작 과정</span><span>대학별 상세분석</span></div></div><div class="route-illustration difference-panel"><div class="top"><h2>학교마다 무엇이 다른가요?</h2><span class="live-dot">SCHOOL BY SCHOOL</span></div><div class="difference-list"><div><b>기간</b><span>3년 · 3.5년 · 4년 · 5년</span></div><div><b>입학월</b><span>2월 · 7월 · 대학별 다름</span></div><div><b>입학방법</b><span>Direct · Foundation · Diploma</span></div><div><b>졸업 후</b><span>인턴십 · 485 · Regional · 주정부</span></div></div></div></div></section>'''

home+='''<section class="section school-differences"><div class="wrap"><div class="section-head"><div><span class="eyebrow">WHY SCHOOL DETAILS MATTER</span><h2>같은 호주 약대라도 이렇게 다릅니다</h2><p>대학 이름보다 과정 구조를 먼저 봐야 합니다.</p></div></div><div class="difference-cards"><a href="/universities/jcu-pharmacy/"><strong>JCU</strong><b>3년 Fast-track</b><span>Townsville·Cairns·Mackay · Regional</span></a><a href="/universities/curtin-pharmacy/"><strong>Curtin</strong><b>3년 9개월 + Diploma</b><span>Diploma 후 약대 2학년</span></a><a href="/universities/griffith-pharmacy/"><strong>Griffith</strong><b>4년 + Diploma</b><span>Gold Coast · 지역 추가 485</span></a><a href="/universities/uwa-pharmacy/"><strong>UWA</strong><b>4년 Bachelor + PharmD</b><span>Perth · 졸업 후 인턴십</span></a><a href="/universities/monash-pharmacy/"><strong>Monash</strong><b>5년 PharmD</b><span>4년 학사 Exit · 5년차 실무훈련</span></a><a href="/universities/uq-pharmacy/"><strong>UQ</strong><b>4년 BPharm + 신설 5년 PharmD</b><span>2월·7월 입학 구조가 다름</span></a></div></div></section>'''

home+='<section class="section soft" id="all-schools"><div class="wrap"><div class="section-head"><div><span class="eyebrow">ALL PHARMACY SCHOOLS</span><h2>'+str(len(U))+'개 호주 약대를 하나씩 보세요</h2><p>검색 결과가 아니라 각 대학의 과정·입학방법·졸업 후 조건을 직접 비교합니다.</p></div><a href="/universities/">대학별 전체 페이지 →</a></div><div class="pharmacy-school-grid">'+''.join(directory_card(u) for u in D['universities'])+'</div><div class="secondary-tool"><span>성적·화학·입학월로 다시 좁히고 싶다면</span><a href="/compare/">조건 비교 도구 사용 →</a></div></div></section>'

home+='''<section class="section pathway-hub-preview"><div class="wrap"><div class="section-head"><div><span class="eyebrow">ENTRY PATHWAYS</span><h2>입학방법으로 다시 모아보기</h2><p>입학방법 페이지는 대학별 정보를 다시 묶어 보는 보조 허브입니다.</p></div><a href="/admission-pathways/">입학방법 전체보기 →</a></div><div class="pathway-hub-grid"><a href="/admission-requirements/"><span>DIRECT</span><h3>고졸 Direct</h3><p>수능·IB·A-level·SAT·OSSD로 약대 1학년</p></a><a href="/foundation/"><span>FOUNDATION</span><h3>Foundation</h3><p>고2 수료부터 시작해 약대 1학년</p></a><a href="/diploma/"><span>DIPLOMA</span><h3>Diploma</h3><p>Griffith·Curtin은 약대 2학년</p></a><a href="/graduate-entry/"><span>GRADUATE ENTRY</span><h3>대졸자 입학</h3><p>Monash·UWA 등 학사 졸업자 과정</p></a></div></div></section>'''

home+='''<section class="section soft poststudy-preview"><div class="wrap"><div class="section-head"><div><span class="eyebrow">AFTER GRADUATION</span><h2>졸업 후 체류기간도 캠퍼스마다 다릅니다</h2><p>일반적인 첫 485는 2년이지만, Regional 요건을 충족하면 두 번째 485가 추가될 수 있습니다.</p></div><a href="/after-graduation/">485·Regional 전체보기 →</a></div><div class="visa-grid"><div><strong>2년</strong><h3>Sydney · Melbourne · Brisbane</h3><p>Major city · 지역 추가 485 없음</p></div><div><strong>3년</strong><h3>Perth · Adelaide · Gold Coast 등</h3><p>Category 2 · 요건 충족 시 +1년</p></div><div><strong>4년</strong><h3>Townsville · Bendigo · Toowoomba 등</h3><p>Category 3 · 요건 충족 시 +2년</p></div></div><p class="representative-note">두 번째 485는 지역캠퍼스 졸업과 지역 거주 등 별도 자격을 충족해야 합니다. 주정부 nomination은 주별 최신 기준을 따로 확인합니다.</p></div></section>'''

home+='''<section class="section"><div class="wrap"><div class="section-head"><div><span class="eyebrow">PROFESSIONAL PATH</span><h2>입학만큼 졸업 후 약사등록도 중요합니다</h2><p>같은 PharmD라도 인턴십을 학위 안에서 하는지, 졸업 후 따로 하는지가 다릅니다.</p></div></div><div class="guides">'''+''.join(f'<a class="guide-card" href="{url}"><span class="eyebrow">{tag}</span><h3>{title}</h3><p>{desc}</p><span class="arrow">자세히 보기 →</span></a>' for url,tag,title,desc in [('/pharmacist-registration/','AUSTRALIA','호주 약사등록','학위·인턴십·시험·General Registration을 대학별로 봅니다.'),('/korea-pharmacist/','KOREA','한국 약사면허','외국대학 인정·호주 면허·예비시험·국가시험 순서를 봅니다.'),('/tuition-scholarships/','COST','학비·장학금·숙소','대학별 실제 비용과 장학금을 비교합니다.')])+'</div></div></section>'
register('/','2027 호주 약대 가이드 · 대학별 과정·입학방법·485 | TNS','호주 약대는 대학마다 기간, 학위, 입학월, 선수과목, Foundation·Diploma, 인턴십과 Regional 485 조건이 다릅니다. 16개 대학을 각각 상세 분석합니다.',home)

directory_body=pagehero('호주 약대 '+str(len(U))+'개 전체보기','호주 약대는 숫자보다 대학별 차이가 중요합니다. 과정기간, 입학월, Pathway, 인턴십과 졸업 후 지역조건을 대학별로 확인하세요.','대학별 약대')
directory_body+='<section class="section"><div class="wrap"><div class="university-directory-intro"><div><strong>3년</strong><span>JCU · UTas</span></div><div><strong>3.5~3.75년</strong><span>UQ 7월 · Curtin</span></div><div><strong>4년</strong><span>일반 BPharm + UWA 특수구조</span></div><div><strong>5년</strong><span>Monash · Sydney · UNSW · UQ 신설</span></div></div><div class="pharmacy-school-grid">'+''.join(directory_card(u) for u in D['universities'])+'</div><div class="secondary-tool"><span>조건 검색이 필요한 경우에만 사용하세요.</span><a href="/compare/">조건 비교 도구 →</a></div></div></section>'
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
after_items=[('rule','485 기본기간','<p>현재 Home Affairs 기준으로 Bachelor와 Masters coursework/extended의 Post-Higher Education Work stream은 기본 2년입니다.</p>'),('regional','Regional이면 두 번째 485가 추가될 수 있습니다',table([('Category 2','+1년','요건 충족 시 총 3년'),('Category 3','+2년','요건 충족 시 총 4년')],['지역','두 번째 485','가능 총기간'],True)+callout('두 번째 485는 자동 연장이 아닙니다. 지역 교육기관에서 학위를 받고, 첫 485 기간 중 지정 지역에서 최소 2년 거주하는 등 별도 요건을 충족해야 합니다.')),('schools','약대별 캠퍼스와 485',table(regional_rows,['대학','약대 캠퍼스','지역 분류','485'],True)),('state','주정부 이민은 별도로 봅니다','<p>주정부 nomination은 직업목록, 경력, 거주조건, 초청방식이 주마다 다르고 자주 바뀝니다. 대학이 Regional에 있다는 이유만으로 주정부 이민이 자동으로 되는 것은 아닙니다. 대학 상세페이지에서는 주(State)를 표시하고, 주정부 조건은 최신 공고를 기준으로 별도 업데이트합니다.</p>'),('sources','자료 출처',sources(['homeaffairs-485','homeaffairs-second485','homeaffairs-regional','jcu-2027-campus','utas-2027-campus']))]
register('/after-graduation/','호주 약대 졸업 후 485 · Regional · 주정부 이민 | TNS','호주 약대 졸업 후 485 기본 2년과 Regional Category 2·3의 두 번째 485, 대학별 캠퍼스 지역을 정리합니다.',pagehero('호주 약대 졸업 후 485·Regional','약대가 있는 도시와 캠퍼스에 따라 졸업 후 체류조건이 달라질 수 있습니다.','졸업 후')+article(after_items))

comp=pagehero('2027 호주 약대 비교',f'학력·선수과목·입학시기로 {len(U)}개 대학의 {len(P)}개 과정을 비교합니다.','전체 약대 비교')
comp+='<div class="compare-sticky"><a href="#finder">조건 수정 ↑</a><span>최대 3개 과정 비교</span></div><section class="section"><div class="wrap">'+finder()+'''<div class="results-head"><div><h2>비교 결과 <span class="results-count" id="result-count">'''+str(len(P))+'''</span></h2><p id="result-summary" role="status" aria-live="polite">조건을 바꾸면 결과가 바로 달라집니다.</p></div><p class="view-note">검색 결과는 선택한 조건 기준입니다.<br>최종 합격은 대학 심사로 결정됩니다.</p></div><div class="empty" id="empty-results" hidden><h3>확인된 조건에 맞는 과정이 없습니다</h3><p>조건을 줄이거나 아래 ‘추가 확인 필요’ 과정을 살펴보세요.</p><button type="button" id="reset-empty">필터 초기화</button></div><div class="card-grid" id="match-results">'''+''.join(card(p) for p in D['programs'])+'''</div><h2 class="pending-heading" id="pending-heading" hidden>정보 대기 <span id="pending-count"></span></h2><p class="small" id="pending-note" hidden>2027 조건이 아직 발표되지 않았거나 자료가 다른 과정입니다.</p><div class="card-grid" id="pending-results"></div>'''+callout('UWA 4년 Bachelor + Doctor of Pharmacy는 비교에 포함했습니다. 대학원 전용 과정은 제외했습니다.')+'</div></section>'
register('/compare/','2027 호주 약대 비교 · 입학방법·화학·입학시기 필터 | TNS',f'호주 약대 {len(U)}개 대학, {len(P)}개 과정을 조건별로 비교합니다. 3년·4년·5년, 화학, 7월 입학, Foundation·1학년 Diploma·Direct Entry를 구분합니다.',comp)

def qtable(pid):
    rows=[]
    for q in related('qualifications',pid):
        f=q['score']; display=fv(f)
        if f['value'] is False:display='이 자격 단독 Direct 평가 대상 아님<br>'+status(f)
        if q.get('scale'):display+=f'<span class="fact-note">기준: {E(q["scale"])}</span>'
        if q.get('calculation'):display+=f'<span class="fact-note">{E(q["calculation"])}</span>'
        rows.append((QUAL[q['qualification']],display))
    return facts(rows)
def routecards(rs):
    html=''
    for r in rs:
        fields=[('진학 가능',fv(r['availability'])),('기간 / 시작월',fv(r['duration'])+'<br>'+fv(r['intake'])),('약대 진급조건',fv(r['progression']))]
        if r['type']!='direct':fields.extend([('입학 학력',fv(r['qualification'])),('영어',fv(r['english']))])
        if r['credit']['value'] is not None:fields.insert(1,('약대 인정학점',fv(r['credit'])+(' CP' if r['program_id'].startswith('griffith') else ' credits')))
        html+=f'<article class="route-detail"><span class="pill-label">{ROUTE[r["type"]]}</span><h3>{E(r["title"])}</h3><dl>'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in fields)+f'</dl><p>{E(r["note"])}</p></article>'
    return '<div class="route-cards">'+html+'</div>'
def scholarcards(ss):
    out=''
    for s in ss:
        amount='확인 중' if s['amount']['value'] is None else value(s['amount'])+'%'
        fields=[('금액',fv(s['amount'],lambda _:amount)),('심사',ASSESS[s['assessment']]),('자동심사',fv(s['automatic_assessment'])),('별도 신청',fv(s['separate_application'])),('경쟁 선발',fv(s['competitive'])),('기간',fv(s['duration'])),('학업 기준',fv(s['academic_threshold'])),('유지 조건',fv(s['renewal_condition'])),('한국 국적 대상',fv(s['country_eligibility'])),('약대 적용',fv(s['pharmacy_eligible'])),('인원',fv(s['number_available'])),('과정 제외',fv(s['course_exclusion']))]
        out+=f'<article class="route-detail"><span class="pill-label">{ASSESS[s["assessment"]]}</span><h3>{E(s["name"])}</h3><dl>'+''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k,v in fields)+f'</dl><p>{E(s["note"])}</p></article>'
    return '<div class="route-cards">'+out+'</div>'
def housingcards(hh):
    out=''
    for h in hh:
        content=facts([('주당',fv(h['weekly_cost'],money)),('계약 기간',fv(h['contract_weeks'],lambda f:value(f)+'주' if f['value'] else '확인 중')),('공식 계약 총액',fv(h['official_contract_total'],money)),('공과금 포함',fv(h['utilities'])),('식사 포함',fv(h['meals'])),('위치',fv(h['campus_distance']))])
        out+=f'<article class="route-detail"><h3>{E(h["name"])}</h3>{content}<p>{E(h["note"])}</p></article>'
    return '<div class="route-cards">'+out+'</div>'
def structure(pid):
    p=P[pid];r=one('professional_registration',pid)
    return facts([('총 학업기간',fv(p['duration_label'])),('학사학위 취득',fv(p['bachelor_award_year'],lambda f:str(f['value'])+'년차' if f['value'] else '확인 중')),('4년 후 졸업 가능',fv(p['four_year_exit'])),('4년 후 학위',fv(p['exit_degree'])),('최종 학위',fv(p['final_degree'])),('학위 안 실무훈련',fv(r['supervised_practice_in_degree'])),('Intern Training 포함',fv(r['itp_in_degree'])),('졸업 후 인턴십',fv(r['post_graduation_internship']))])
def costcalculator():return '''<div class="cost-calculator"><h3>1년 예산 가늠하기</h3><p class="small">금액은 직접 조정할 수 있습니다. 숙소·생활비 기본값은 비교용 가정이며 공식 견적이나 현재 평균이 아닙니다.</p><form id="cost-form"><div class="cost-grid"><label>연간 학비 (AUD)<input name="tuition" type="number" min="0" max="200000" value="60000" step="100"></label><label>숙소 주당 (AUD)<input name="rent" type="number" min="0" max="3000" value="350"></label><label>계약 주 수<input name="weeks" type="number" min="1" max="52" value="52"></label><label>기타 생활비 주당 (AUD)<input name="living" type="number" min="0" max="3000" value="250"></label><label>적용할 장학률 (%)<input name="discount" type="number" min="0" max="100" value="0"></label><label>계산용 환율 (KRW / AUD)<input name="fx" type="number" min="1" max="10000" value="1000"></label></div><button class="btn" type="submit" style="margin-top:20px">가정한 예산 계산</button></form><div class="cost-output" aria-live="polite" id="cost-output"><span>위 가정으로 계산한 1년 예산</span><strong>A$91,200</strong><p>약 9,120만 원 · 환율 A$1 = 1,000원 가정<br>학비 A$60,000 + 숙소 A$18,200 + 기타 생활비 A$13,000</p></div><p class="small muted" style="margin-top:14px">공식 총학비가 아닙니다. 장학률 기본값은 0%이며 실제 오퍼에 장학이 명시된 경우 조정하세요. 항공·비자·OSHC·교재·보증금·실습 이동비는 별도입니다. 생활비는 52주 기준, 숙소는 입력한 계약 주 수 기준입니다.</p></div>'''

for u in D['universities']:
    pp=[p for p in D['programs'] if p['university_id']==u['id']];p=pp[0];pid=p['id'];rq=one('requirements',pid);en=one('english',pid);it=one('intakes',pid);t=one('tuition',pid);r=one('professional_registration',pid)
    rs=related('entry_routes',pid);ss=related('scholarships',u=u['id']);hh=related('accommodation',u=u['id'])
    extra='<div class="facts-grid">'+''.join(f'<div class="fact-tile"><small>{k}</small><strong>{v}</strong></div>' for k,v in [('과정',E(value(p['duration_label']))),('캠퍼스',E(value(u['campus']))),('입학시기',E(value(it['label']))),('유학생 모집',E(value(p['international_recruitment']))),('연간 학비',E(money(t['annual']))),('자료 업데이트',DATE)])+'</div>'
    body=pagehero(E(u['name_ko'])+' 약대',E(u['name'])+' · '+E(value(p['name'])),u['name_ko'],extra)
    intro='<p>'+E(p['editorial'])+'</p><div class="chips">'+''.join(f'<span class="chip">{E(h)}</span>' for h in p['highlights'])+'</div>'
    if p['review_items']:intro+=callout('<strong>2027 업데이트 대기</strong><ul>'+''.join('<li>'+E(x)+'</li>' for x in p['review_items'])+'</ul>',True)
    anatomy=structure(pid)
    if len(pp)>1:
        other=pp[1];anatomy+='<h3 id="uq-pharmd">신설 UQ 통합 PharmD · 별도 과정</h3>'+callout(E(other['editorial']),True)+structure(other['id'])
    requirements_html=facts([(name,fv(rq[k])) for k,name in [('chemistry','Chemistry'),('mathematics','Mathematics'),('biology','Biology'),('physics','Physics'),('minimum_grade','과목 성적 기준')]])
    english_html=facts([(name,fv(en[k])) for k,name in [('ielts_overall','IELTS overall'),('ielts_bands','IELTS 영역별'),('pte_overall','PTE overall'),('pte_each','PTE each'),('toefl','TOEFL')]])+callout('입학 영어와 졸업 후 약사등록 영어는 기준이 다릅니다.')
    fees=facts([('연간 국제학생 학비',fv(t['annual'],money)),('수강량 기준',fv(t['load_basis'])),('대학 공개 예상 총학비',fv(t['official_total'],money))])+'<p class="small muted">'+E(t['increase_note'])+' 연간 학비에 기간을 단순히 곱하지 않았습니다.</p>'
    registration_html=facts([('APC 인증',fv(p['accreditation'])),('학위 안 실무훈련',fv(r['supervised_practice_in_degree'])),('학위 안 Intern Training',fv(r['itp_in_degree'])),('졸업 후 인턴십',fv(r['post_graduation_internship']))])+callout(E(r['note']))+link('/pharmacist-registration/','약사등록 단계별 설명 →','btn text')
    fs=[('선수과목을 이수하지 않아도 지원할 수 있나요?',('JCU는 화학이 필수가 아닙니다. 수학·영어 등 다른 조건은 충족해야 합니다.' if u['id']=='jcu' else '대학마다 필수과목이 다릅니다. 화학·수학이 부족하면 Foundation으로 보완할 수 있는지 보세요.')),
        ('2027 학비가 미공개인 항목은 어떻게 보나요?','최신 공개 학비에 연도를 붙여 표시합니다. 2027 학비가 나오면 바로 업데이트합니다.'),
        ('졸업하면 바로 호주나 한국 약사가 되나요?','아닙니다. 호주는 인턴십·시험·등록이 필요하고, 한국은 별도 면허 절차가 있습니다.')]
    allids=source_ids([p,rs,ss,hh,rq,en,it,t,r,related('qualifications',pid)])|{'apc','korea-law'}
    if u['id']=='uq':allids|={'uq-pharmd','uq-foundation','uq-calendar'}
    routes_html=routecards(rs)
    if u['id']=='uwa':routes_html+=callout('<strong>대졸자 별도 과정</strong><p>UWA에는 학사 졸업자가 지원하는 2년 Doctor of Pharmacy도 있습니다. 2027년 1월 시작, sWAM 65+와 Chemistry·Math/Statistics·Microbiology·Pharmacology가 필요합니다.</p>'+link('/graduate-entry/','UWA Graduate Entry 보기 →','btn text'))
    allids|={'homeaffairs-485','homeaffairs-second485','homeaffairs-regional'}
    if u['id']=='jcu':allids|={'jcu-2027-campus'}
    if u['id']=='utas':allids|={'utas-2027-campus'}
    if u['id']=='uwa':allids|={'uwa-dpharm'}
    items=[('overview','이 약대 핵심',intro),('structure','과정·학위 구조',anatomy),('routes','입학방법',routes_html),('admission','Direct 입학조건','<h3>학력·성적</h3>'+qtable(pid)+'<h3>선수과목</h3>'+requirements_html+'<h3>영어</h3>'+english_html+'<h3>입학시기</h3>'+fv(it['label'])+'<p class="small">Foundation·Diploma 시작월은 위 입학방법에 표시했습니다.</p>'),('cost','학비·장학금·생활비','<h3>학비</h3>'+fees+'<h3>장학금</h3>'+scholarcards(ss)+'<h3>기숙사·숙소</h3>'+housingcards(hh)+'<h3>1년 예산</h3>'+costcalculator()),('poststudy','졸업 후 485·지역',poststudy_html(u)),('registration','호주 약사등록',registration_html),('korea','한국 약사면허','<p>호주 약대 졸업만으로 한국 약사면허가 자동으로 나오지 않습니다. 대학 인정, 호주 면허, 예비시험·국가시험을 따로 거칩니다.</p>'+link('/korea-pharmacist/','한국 약사면허 확인 순서 →','btn text')),('faq','자주 묻는 질문',faq(fs)),('sources','자료 출처',sources(allids))]
    register(purl(p),f'2027 {u["name_ko"]} 약대 완전분석 · 입학·학비·485 | TNS',u['name']+' Pharmacy의 과정기간, 입학방법, 선수과목, 학비·장학금, 인턴십, 485 지역조건과 약사등록을 정리합니다.',body+article(items),fs)

pathway_items=[('overview','호주 약대 입학방법 3가지','<p>고등학생은 보통 Foundation, Diploma, Direct Entry 세 가지 방법으로 시작합니다.</p><div class="admission-grid"><article class="admission-card"><span class="route-label">FOUNDATION</span><h3>고2 → Foundation → 약대 1학년</h3><p>고2 수료 후 Foundation을 마치고 약대 1학년으로 진학합니다.</p><a href="/foundation/">Foundation 자세히 →</a></article><article class="admission-card"><span class="route-label">DIPLOMA / IYO</span><h3>Diploma → 약대 2학년</h3><p>Griffith·Curtin은 Diploma 후 약대 2학년으로 진학합니다.</p><p class="route-exception">Adelaide: 학점 인정 학생 → 7월 입학 심사</p><a href="/diploma/">Diploma 자세히 →</a></article><article class="admission-card"><span class="route-label">DIRECT ENTRY</span><h3>성적으로 바로 약대 1학년</h3><p>수능·IB·A-level·SAT·OSSD와 선수과목·영어로 바로 지원합니다.</p><a href="/admission-requirements/">Direct 입학조건 →</a></article></div>'),('profiles','내 학력에서 바로 찾기',table([('고2 수료','Foundation'),('고3 졸업','Direct / Diploma'),('검정고시','Diploma / 일부 Direct'),('수능·IB·A-level·SAT·OSSD','Direct Entry')],['현재 학력','먼저 볼 방법'],True)),('graduate','대학 졸업자','<p>Graduate Entry는 일부 대학만 운영합니다. 학사학위와 대학 선수과목이 필요합니다.</p>'+link('/compare/?qualification=graduate','Graduate Entry 보기 →','btn text'))]
register('/admission-pathways/','2027 호주 약대 입학방법 · Foundation·Diploma·Direct | TNS','호주 약대에 진학하는 대표적인 세 가지 방법인 Foundation, 1학년 Diploma/IYO, Direct Entry를 학력별로 비교하고 대졸자 특수경로를 구분합니다.',pagehero('호주 약대 입학방법','입학방법을 먼저 고른 뒤, 해당 대학 상세페이지에서 실제 조건을 확인하세요.','입학방법')+article(pathway_items))

admission_rows=[]
for p in D['programs']:
    rq=one('requirements',p['id']);en=one('english',p['id']);admission_rows.append((link(purl(p),E(U[p['university_id']]['short'])+(' PharmD' if p['id']=='uq-pharmd' else '')),fv(rq['chemistry']),fv(rq['mathematics']),fv(en['ielts_overall'])))
admit_items=[('read','입학조건은 4가지만 보면 됩니다','<div class="process-grid four">'+''.join(f'<div class="process-card"><span class="number">{n}</span><h3>{t}</h3><p>{d}</p></div>' for n,t,d in [('1','성적','약대에 필요한 성적을 봅니다.'),('2','선수과목','수학·화학 등 필요한 과목을 봅니다.'),('3','영어','IELTS·PTE 전체점수와 각 영역을 봅니다.'),('4','입학시기','2월·7월 입학 여부를 봅니다.')])+'</div>'+callout('같은 시험도 대학마다 요구 점수가 다릅니다. 선수과목과 영어도 함께 맞춰야 합니다.')),
 ('qualifications','한국 학생의 학력별 출발점',table([('수능','대학별 수능 기준'),('IB / A-level / SAT','시험점수 + 수학·과학 과목'),('OSSD','Grade 12 과목 + 평균 기준'),('한국 내신 / 검정고시','Direct 가능 여부 + Foundation·Diploma')],responsive=True)),
 ('scores','2027 Direct 입학점수', '<h3>Sydney · Pharmacy 과정 행</h3>'+qtable('sydney-bpharm-hons')+callout('다른 대학의 한국 수능·SAT·IB 기준은 course-specific 공식표를 대조 중입니다. Sydney 점수를 다른 약대에 적용하지 않습니다.',True)),
 ('latest-scores','Griffith · 2026 참고','<p>2026 International Guide에서 Pharmacy 1614는 H1 기준입니다. 아래 점수는 2027 확정값이 아니며 필터에서도 추가 확인 대상으로 분류합니다.</p>'+qtable('griffith-bpharm-hons')),
 ('prerequisites','선수과목·영어 핵심 비교',table(admission_rows,['과정','화학','수학','IELTS overall'],True)+callout('영어는 각 영역 점수까지 봅니다. ‘선행지식’은 ‘필수과목’과 다릅니다.')),
 ('chemistry','화학을 안 배웠다면','<p>JCU는 화학이 필수가 아닙니다. 화학이 필요한 대학은 Foundation에서 보완할 수 있습니다.</p>'+link('/compare/?chemistry=no','화학 미이수 조건으로 비교 →','btn')),
 ('next','다음 단계','<p>성적과 선수과목을 정리한 뒤 Direct, Foundation, Diploma를 비교하세요.</p><div class="section-link-list"><a href="/foundation/">Foundation 진급조건</a><a href="/diploma/">Diploma 학점인정</a><a href="/consult/">상담 준비</a></div>'+sources(['sydney','griffith-2026','jcu-guide','uq','monash','qut-guide','rmit','newcastle','canberra-2027','unisq-course']))]
register('/admission-requirements/','2027 호주 약대 입학조건 · 수능·IB·SAT·선수과목 | TNS','호주 약대의 학력별 Direct 입학조건, 수학·화학 선수과목과 영어 기준을 비교합니다. 일반 대학 최소기준과 약대 전용 조건을 구분합니다.',pagehero('호주 약대 입학조건','성적, 선수과목, 영어, 입학시기 네 가지만 보면 됩니다.','입학조건')+article(admit_items))

foundation_routes=[r for r in D['entry_routes'] if r['type']=='foundation']
foundation_items=[('difference','Foundation은 약대 입학 전 준비과정입니다','<p>고2 수료 후 Foundation을 마치고 약대 1학년으로 진학합니다. Foundation 입학조건과 약대 진급조건은 서로 다릅니다.</p><div class="route-mini"><span>Foundation 입학</span>→<span>지정 과목·영어 이수</span>→<span>약대 진급 기준 충족</span>→<span>약대 1학년</span></div>'),
 ('routes','어느 대학으로 연결되나요?',routecards(foundation_routes)),
 ('uq','UQ · 2월 Foundation → 7월 약대','<p>UQ College Accelerated Foundation은 2027년 2월 15일 시작해 7월 9일 끝납니다. UQ BPharm은 7월 26일 시작합니다.</p>'+callout('Foundation 입학, 필수과목, GPA·영어 기준을 모두 충족해야 약대로 올라갑니다.')+'<p>BPharm 공개 진급 기준은 GPA 5.0, Academic English 5입니다. 새 UQ PharmD로 같은 조건이 적용된다고 가정하지 않습니다.</p>'),
 ('monash','Monash · 2027 새 과정 코드 확인','<p>구 P6001 점수는 새 P6007에 적용하지 않습니다. P6007 진급점수는 발표 대기입니다.</p>'),
 ('check','지원 전 체크','<ul><li>고교 졸업/재학 증명과 학년별 성적표</li><li>희망 약대에 필요한 수학·과학 과목 조합</li><li>Foundation 영어조건과 약대 진급 영어조건</li><li>Foundation 시작일, 약대 시작일, 성적 발표일</li><li>Foundation과 약대의 학비·숙소 예산</li></ul>'+sources(source_ids(foundation_routes)|{'uq-calendar','uq-foundation','uq'}))]
register('/foundation/','호주 약대 파운데이션 · 2027 대학별 진급조건 | TNS','UQ Accelerated Foundation, Sydney USFP, Monash 등 Foundation 진급 성적·영어·과목·약대 시작시기를 정리합니다.',pagehero('Foundation으로 호주 약대 준비하기','고교 성적이나 선수과목이 부족하다면 Foundation부터 약대 진급까지 한 번에 보세요.','Foundation')+article(foundation_items))

dip=[r for r in D['entry_routes'] if r['type'] in ['diploma','other']]
dip_items=[('start','Diploma 후 어디로 올라가나요?','<div class="diploma-summary"><div><strong>Griffith</strong><span>Diploma → 약대 2학년</span></div><div><strong>Curtin</strong><span>Diploma → 약대 2학년</span></div><div><strong>Adelaide</strong><span>학점 인정 → 7월 입학</span></div></div><p>Griffith와 Curtin은 약대 2학년으로 연결됩니다. Adelaide는 학점이 인정된 국제학생을 7월 입학으로 개별 심사합니다.</p>'),('routes','대학별 Diploma 경로',routecards([r for r in dip if r['type']=='diploma'])),('griffith','Griffith','<p><strong>80CP를 인정받고 약대 2학년으로 진학합니다.</strong></p>'+table([('Diploma','80CP 인정','약대 2학년'),('남은 기간','T1 시작 3년','T2 시작 3.5년')],['항목','조건','결과'],True)),('curtin','Curtin','<p><strong>175 credits를 인정받고 약대 2학년으로 진학합니다.</strong></p><p>Stage 2 CWA 70%와 PHAR1002 추가 이수가 필요합니다.</p>'),('adelaide','Adelaide','<p><strong>학점이 인정된 국제학생은 7월 입학 심사를 받을 수 있습니다.</strong></p><p>인정 학점은 학생별로 심사합니다.</p>'),('other','그 밖의 경로','<p>RMIT Associate Degree는 1년 Diploma가 아닙니다. 별도 경로로 구분합니다.</p>'),('questions','자주 묻는 질문',faq([('Diploma를 마치면 약대 2학년으로 가나요?','Griffith와 Curtin은 약대 2학년으로 진학합니다. 정해진 성적과 과목은 반드시 충족해야 합니다.'),('Adelaide도 Diploma 후 2학년인가요?','Adelaide는 학점 인정 방식입니다. 학점 인정 학생을 7월 입학으로 개별 심사합니다.')])+sources(source_ids(dip)|{'adelaide'}))]
register('/diploma/','호주 약대 Diploma · Griffith·Curtin 2학년 진학 | TNS','Griffith와 Curtin의 Diploma 후 약대 2학년 진학, Adelaide의 학점 인정 후 7월 입학을 비교합니다.',pagehero('Diploma 후 약대 2학년','Griffith·Curtin은 Diploma 후 약대 2학년으로 진학합니다. Adelaide는 학점 인정 학생을 7월 입학으로 개별 심사합니다.','Diploma / IYO')+article(dip_items))

fee_rows=[]
for p in D['programs']:
 t=one('tuition',p['id']);fee_rows.append((link(purl(p),E(U[p['university_id']]['short'])+(' PharmD' if p['id']=='uq-pharmd' else '')),fv(t['annual'],money),fv(t['official_total'],money)))
cost_items=[('tuition','대학별 1년 학비',table(fee_rows,['과정','연간 학비','대학 공개 예상 총학비'],True)+callout('UTas는 연간 133 credits, UQ는 16 units 등 수강량 기준이 다릅니다. 공식 총액도 추정치이며 향후 학비 인상과 수강계획에 따라 달라질 수 있습니다.')),('scholarship-types','장학금은 3가지로 나눠보세요','<div class="process-grid"><div class="process-card"><span class="number">01</span><h3>보장형</h3><p>명확한 보장 약정이 확인된 경우에만 사용합니다. 이번 검증 자료에서 일괄 보장형으로 분류한 장학은 없습니다.</p></div><div class="process-card"><span class="number">02</span><h3>자동심사형</h3><p>별도 장학 신청이 없어도 선발·자격 확인은 필요합니다. 오퍼에 수여가 명시됐는지 확인하세요.</p></div><div class="process-card"><span class="number">03</span><h3>경쟁형</h3><p>성적 상위 소수 선발입니다. 최대 장학률을 일반 학생 기본 비용에서 미리 빼지 않습니다.</p></div></div>'),('scholarships','주요 장학 조건',scholarcards([s for s in D['scholarships'] if s['university_id'] in ['griffith','sydney','monash','newcastle','unsw','jcu']])+callout('Sydney는 personal statement 제출이 필요합니다. UNSW 해당 20% 장학의 국가 목록에는 한국이 없어 한국 국적 기본 할인에 포함하지 않습니다. 나머지 대학은 상세페이지에서 적용 확인 상태를 볼 수 있습니다.')),('housing','기숙사·숙소비',housingcards([h for h in D['accommodation'] if h['weekly_cost']['value'] is not None])+'<p class="small">Sydney·UNSW 등 다른 도시의 검증된 공식 숙소 요금이 아직 부족해 도시 간 총비용 순위를 만들지 않았습니다. 보증금, 공과금, 식사와 계약기간을 같은 기준으로 맞춰야 합니다.</p>'),('calculator','1년 예산 계산',costcalculator()),('sources','자료 기준',sources(source_ids(D['tuition']+D['scholarships']+D['accommodation'])))]
register('/tuition-scholarships/','2027 호주 약대 학비·장학금·숙소 비교 | TNS','1년 학비, 대학 공개 예상 총학비, 장학금, 숙소비를 비교하고 1년 예산을 계산합니다.',pagehero('호주 약대 학비·장학금','1년 학비와 장학금, 숙소비를 한 번에 비교하세요.','학비·장학금')+article(cost_items))

reg_items=[('steps','호주 약사가 되는 순서','<p>대학 실습과 등록을 위한 supervised practice는 같은 항목이 아닙니다. 통합학위에서는 아래 일부 단계가 재학 중 진행될 수 있습니다.</p><ol class="timeline">'+''.join(f'<li><strong>{t}</strong>{d}</li>' for t,d in [('승인된 학위·교육요건 확인','APC 인증과 Pharmacy Board 승인 학위명·캠퍼스를 확인합니다.'),('Provisional registration','등록용 supervised practice 시작에 필요한 등록 및 실습 승인 절차를 확인합니다.'),('Supervised practice + Intern Training','인정되는 감독 실무와 accredited intern training을 이수합니다.'),('Written / Oral examinations','응시요건 충족 후 등록시험을 진행합니다. 학위만으로 시험이 면제된다고 가정하지 않습니다.'),('General registration','모든 교육·실무·시험·등록 적합성 요건을 충족한 후 일반등록을 신청합니다.')])+'</ol>'+callout('인턴십 시간·시험 시점·등록 영어점수는 시행 시점의 Pharmacy Board 기준을 따릅니다. 확인되지 않은 숫자는 넣지 않았습니다.',True)),('integrated','5년 과정도 인턴십 방식이 다릅니다',table([(link('/universities/monash-pharmacy/','Monash'),'4년 학사 Exit · 5년 통합','5년차 supervised practice / ITP 통합 · 등록시험·심사 별도'),(link('/universities/sydney-pharmacy/','Sydney'),'5년 BPharm(Hons) / MPharmPractice','실무·인턴 과정 포함 · 4년 후 학사 Exit'),(link('/universities/unsw-pharmacy/','UNSW'),'2027 PharmD 명칭 전환','졸업 후 인턴십 따로'),(link('/universities/uq-pharmacy/#uq-pharmd','UQ 신설 PharmD'),'기존 BPharm과 별도 5년 과정','인턴십 통합 설계 · APC/Board 승인 아직 미획득')],['과정','학위구조','등록 준비'],True)),('accreditation','APC 인증 상태','<p>APC의 2026년 7월 8일 목록을 기준으로 했습니다. ‘Accredited with conditions’도 인증 과정이며 조건과 갱신 시점이 붙어 있습니다.</p><p>UQ 신설 PharmD는 아직 승인 대기입니다. UNSW 새 PharmD와 Newcastle 인증 갱신도 최신 상태로 업데이트합니다.</p>'),('korea','한국 약사면허는 별도 절차','<p>호주 일반등록과 한국 약사면허는 다른 심사 체계입니다. 한국으로 돌아갈 계획이라면 입학 전에 대학 인정기준과 외국 면허·시험 요건을 따로 확인하세요.</p>'+link('/korea-pharmacist/','한국 약사면허 경로 →','btn text')+sources(['apc','apc-exam','board','monash','sydney-guide','unsw','uq-pharmd']))]
register('/pharmacist-registration/','호주 약사 되는 과정 · 학위·인턴십·등록시험 | TNS','호주 약사등록의 학위, provisional registration, supervised practice, intern training, 시험과 general registration을 구분합니다.',pagehero('학위 취득부터 호주 약사등록까지','3년 학사, 4년 학사, 5년 통합학위가 등록 준비의 어느 단계까지 포함하는지 확인하세요.','호주 약사등록')+article(reg_items))

korea_items=[('law','먼저 확인할 법적 요건','<p>2026년 9월 11일 시행 약사법 제3조는 외국 약학대학 졸업자의 경로에서 대학의 인정기준, 외국 약사면허, 약사예비시험과 약사국가시험 합격을 요구합니다. 호주 약대를 졸업했다는 사실만으로 한국 응시자격을 확정할 수 없습니다.</p>'),('checks','입학 전 체크 순서','<ol class="timeline"><li><strong>정확한 대학·학위·캠퍼스 특정</strong>학교 이름뿐 아니라 입학연도, 최종 학위명, 실제 교육과정과 이수 방식을 준비합니다.</li><li><strong>외국대학 인정기준·심사 확인</strong>보건복지부 고시와 국시원의 해당 절차에 따라 인정 여부를 확인합니다.</li><li><strong>호주 현지 약사면허 취득 경로 확인</strong>학위 후 필요한 인턴십·시험·등록을 봅니다.</li><li><strong>예비시험·국가시험 응시자격 확인</strong>해당 연도 서류, 한국어 요건 등 세부 절차를 국시원 공식 공고로 확인합니다.</li></ol>'),('schools','대학별 ‘가능’ 표시를 하지 않는 이유',callout('이 사이트는 확인되지 않은 대학을 ‘한국 약사면허 가능’으로 분류하지 않습니다. 학위명 변경이나 교육과정 개편이 있는 2027 과정은 과거 인정 사례를 그대로 적용하지 않습니다.',True)),('documents','확인을 위해 준비할 자료','<ul><li>입학 예정 과정명·코드·캠퍼스·학업 방식</li><li>학년별 교육과정·실습 구조·수업 및 이수 기간</li><li>수여되는 학사/석사/Doctor 학위명</li><li>호주 등록용 supervised practice·ITP·시험 경로</li><li>본인 학력·성적·면허 및 졸업 관련 증빙</li></ul><p>국시원 약사 직종의 해당 연도 세부 공고·개별 인정 결과 확인은 별도로 필요합니다.</p>'+sources(['korea-law','kuksiwon']))]
register('/korea-pharmacist/','호주 약대 졸업 후 한국 약사면허 · 확인 절차 | TNS','외국 약대 졸업자가 한국 약사면허를 받는 순서를 약사법 기준으로 설명합니다. 대학 인정, 외국 면허, 예비시험·국가시험이 필요합니다.',pagehero('호주 약대에서 한국 약사면허까지','호주 약대 졸업만으로 한국 약사면허가 자동으로 나오지 않습니다. 필요한 절차를 순서대로 정리했습니다.','한국 약사면허')+article(korea_items))

fastitems=[('programs','3년 Fast-track · JCU와 UTas','<p>JCU와 UTas는 4년 약학과를 3년에 압축해 공부합니다. 1년 수강량이 많고 학업 일정이 빠릅니다.</p><div class="card-grid">'+card(P['jcu-bpharm-hons'])+card(P['utas-bpharm-hons'])+'</div>'),('uq','UQ의 7월 약 3.5년과 구분','<p>UQ 기존 BPharm은 2월 4년, 7월 약 3.5년입니다. 3년 Fast-track과 동일한 상품이 아니며, 수학·화학 요건과 7월 모집 여부를 함께 봐야 합니다.</p>'),('registration','학업기간 이후의 등록 준비','<p>3년 학위 수료 후에도 등록용 인턴십과 ITP·등록시험 등 요구가 남습니다. 5년 통합과 비교할 때는 학위만의 기간과 전체 등록 준비기간을 구분하세요.</p>'+link('/pharmacist-registration/','등록 구조 자세히 →','btn text')+sources(['jcu-guide','utas','uq','apc']))]
register('/3-year-pharmacy/','호주 3년 약대 · JCU·UTas Fast-track 비교 | TNS','호주 3년 약대 JCU·UTas의 압축 학사와 UQ 7월 3.5년 경로를 구분하고, 졸업 후 약사등록 준비기간을 확인합니다.',pagehero('호주 3년 약대, 빠른 만큼 확인할 것','3년 학위 완료와 약사등록 완료는 다릅니다. 압축 학사 일정과 졸업 후 준비를 함께 살펴보세요.','3년 약대')+article(fastitems))

method_items=[('scope','이 사이트의 비교 범위','<p>한국 학생이 고교 졸업 후 학부 단계부터 약사 과정을 시작할 수 있는 대학을 중심으로 구성합니다. 대학원 전용 과정과 국제학생 대면 모집 확인이 안 된 상품을 확정 진학 옵션으로 표시하지 않습니다.</p>'),('status','정보 상태 읽는 방법',table([(status({'status':s}),t) for s,t in [('confirmed_2027','2027 공식 자료에서 해당 사실을 확인했습니다. 최종 입학허가를 뜻하지 않습니다.'),('latest_published','현재 확인한 최신 공개 자료입니다. 연도가 이전이면 명시하며 2027 확정으로 사용하지 않습니다.'),('pending_2027','2027 발표 대기, 접근 제한 또는 검증 미완료를 포함합니다. 공식 자료가 존재하지 않는다고 단정하지 않습니다.'),('source_conflict','공식 자료 간 수치·적용 범위 차이가 남아 있습니다. 자동 충족 판정에 사용하지 않습니다.')]],['상태','의미'],True)),('conflicts','자료 차이와 후속 확인',table([(E(c['summary']),E(c['decision'])) for c in D['conflicts']],responsive=True)),('order','자료 우선순위','<p>최신 대학 course page·official admissions guide, APC·Pharmacy Board, 정부 자료를 우선합니다. 일반 입학 최소기준을 약대 전용 기준으로 대체하지 않으며, 프로그램 코드가 바뀐 경우 이전 점수를 이식하지 않습니다.</p>'),('limits','현재 검증이 남은 범위','<p>여러 대학의 CSAT·SAT·IB·OSSD 환산, 내신·검정고시 인정, 준비과정별 진급조건, 장학 제외목록, 공식 숙소 요금이 확인 중입니다. 비교 결과에서는 해당 조건을 충족으로 간주하지 않습니다.</p><p>호주 전용 TNS 오픈채팅은 승인된 링크가 확보될 때까지 연결하지 않습니다. 참여자 수는 검증되지 않아 게시하지 않습니다.</p>')]
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

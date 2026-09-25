(()=>{'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const dataNode=$('#program-data');if(!dataNode)return;
const programs=JSON.parse(dataNode.textContent), byId=new Map(programs.map(p=>[p.id,p]));
const text=(tag,content,className)=>{const e=document.createElement(tag);e.textContent=content;if(className)e.className=className;return e;};
const rawval=f=>f?.value==null?'확인 중':typeof f.value==='boolean'?(f.value?'포함 / 가능':'별도 / 해당 없음'):Array.isArray(f.value)?f.value.join(' / '):typeof f.value==='object'?Object.entries(f.value).map(([k,v])=>`${k} ${v}`).join(' · '):String(f.value);
const val=f=>rawval(f)+(f?.value!=null&&f.status==='source_conflict'?' · 자료 차이 / 재확인':f?.value!=null&&f.status==='pending_2027'?' · 2027 확인 중':f?.value!=null&&f.source_year&&f.source_year<2027?' · '+f.source_year+' 참고':'');
const cash=f=>f?.value==null?'확인 중':`A$${Number(f.value).toLocaleString('en-AU')} · ${f.source_year||'기준연도 확인'}`;
let toastTimer;function toast(message){const e=$('.toast');e.textContent=message;e.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>e.hidden=true,3500);}
const menu=$('.menu-toggle'),nav=$('#main-nav');menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav?.classList.contains('open')){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');menu.focus();}});
document.addEventListener('click',e=>{if(nav?.classList.contains('open')&&!nav.contains(e.target)&&!menu.contains(e.target)){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');}});

let selected=[];try{selected=JSON.parse(sessionStorage.getItem('tns-pharmacy-compare')||'[]').filter(id=>byId.has(id)).slice(0,3);}catch{}
function syncCompare(){
  $$('.compare-toggle input').forEach(c=>{c.checked=selected.includes(c.dataset.compare);});
  $('.compare-bar').hidden=!selected.length;$('#selected-count').textContent=selected.length;
  try{sessionStorage.setItem('tns-pharmacy-compare',JSON.stringify(selected));}catch{}
}
$$('[data-compare]').forEach(box=>box.addEventListener('change',()=>{
  if(box.checked&&!selected.includes(box.dataset.compare)){
    if(selected.length===3){box.checked=false;toast('최대 3개까지 비교할 수 있습니다. 기존 선택을 해제해 주세요.');return;}
    selected.push(box.dataset.compare);
  }else selected=selected.filter(id=>id!==box.dataset.compare);
  syncCompare();
}));
$('#clear-compare')?.addEventListener('click',()=>{selected=[];syncCompare();});
const dialog=$('#compare-dialog');
$('#open-compare')?.addEventListener('click',()=>{
  const grid=$('#comparison-content');grid.replaceChildren();
  selected.forEach(id=>{const p=byId.get(id),item=text('article','','comparison-item');item.append(text('h3',p.university.name_ko+(id==='uq-pharmd'?' · 신설 PharmD':'')),text('p',val(p.name),'small'));const dl=document.createElement('dl');
    const rows=[['학위기간',val(p.duration_label)],['학사 취득',val(p.bachelor_award_year)+(p.bachelor_award_year.value?'년차':'')],['4년 Exit',val(p.four_year_exit)],['학위 내 실무',val(p.professional_registration.supervised_practice_in_degree)],['ITP 포함',val(p.professional_registration.itp_in_degree)],['졸업 후 인턴십',val(p.professional_registration.post_graduation_internship)],['화학',({required:'필수',recommended:'권장',assumed:'Assumed knowledge',accepted:'인정'})[p.requirements.chemistry.value]||'확인 중'],['입학시기',val(p.intakes.label)],['IELTS overall',val(p.english.ielts_overall)],['IELTS 영역별',val(p.english.ielts_bands)],['연간 학비',cash(p.tuition.annual)],['등록·인증',val(p.accreditation)],['입학경로',p.entry_routes.map(r=>r.title+(r.availability.value===null?' (확인 중)':'')).join(' / ')]];
    rows.forEach(([k,v])=>dl.append(text('dt',k),text('dd',v)));item.append(dl);const a=text('a','상세 조건 확인 →','btn secondary');a.href=p.url;item.append(a);grid.append(item);
  });dialog.showModal();
});
$('#close-compare')?.addEventListener('click',()=>dialog.close());
dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
syncCompare();

const form=$('#finder');
if(form){
 const params=new URLSearchParams(location.search);
 for(const el of form.elements){if(el.name&&params.has(el.name)&&el.name!=='score')el.value=params.get(el.name);}
 const score=form.elements.score;
 const limits={csat:[0,800,'수능 표준점수 합'],sat:[400,1600,'SAT / 1600'],ib:[0,45,'IB / 45'],alevel:[0,40,'대학 환산점수']};
 function setQualification(){
   if(!score)return;const q=form.elements.qualification.value;const box=$('.score-field',form);box.hidden=!limits[q];
   if(limits[q]){score.min=limits[q][0];score.max=limits[q][1];$('#score-scale').textContent=limits[q][2];score.disabled=false;}else{score.value='';score.disabled=true;}
   if(q==='graduate')form.elements.route.value='graduate';
   if(q==='csat')$('#score-help').textContent='Sydney: 국어 + 수학 + 탐구 상위 2과목 표준점수 합. 대학별 계산방식은 다릅니다. 점수는 URL에 저장하지 않습니다.';
   else $('#score-help').textContent='대학별 환산방식을 확인한 점수만 입력하세요. 영어 overall 필터는 각 영역 충족을 판정하지 않습니다. 점수는 URL에 저장하지 않습니다.';
 }
 setQualification();
 form.elements.qualification?.addEventListener('change',()=>{if(score)score.value='';setQualification();});
 if(form.dataset.mode==='filter'){
  const cards=new Map($$('.university-card[data-program]').map(el=>[el.dataset.program,el]));
  function applyFilters(updateUrl=true){
   if(!form.reportValidity())return;
   const f=Object.fromEntries(new FormData(form));const match=$('#match-results'),pending=$('#pending-results');let n=0,u=0,x=0;
   const active=Object.values(f).some(v=>v!=='');
   programs.forEach(p=>{const result=PharmacyMatcher.classify(p,f);const card=cards.get(p.id);if(!card)return;
    card.hidden=result.state==='excluded';if(card.hidden){x++;return;}
    const reason=$('.match-reason',card);reason.hidden=!active&&result.state==='match';reason.classList.toggle('pending',result.state==='pending');
    if(result.state==='pending'){u++;pending.append(card);reason.textContent=result.unknown.slice(0,2).join(' · ');}
    else{n++;match.append(card);reason.textContent=result.matches.length?'선택조건 일치 · '+result.matches.slice(0,2).join(' · '):'상세 입학조건을 확인하세요';}
   });
   $('#result-count').textContent=n;$('#pending-count').textContent=u+'개';$('#pending-heading').hidden=!u;$('#pending-note').hidden=!u;$('#empty-results').hidden=n>0;
   $('#result-summary').textContent=`선택조건 기준 ${n}개 · 추가 확인 ${u}개 · 현재 조건에서 제외 ${x}개`;
   if(updateUrl){const q=new URLSearchParams();Object.entries(f).forEach(([k,v])=>{if(v&&k!=='score')q.set(k,v);});try{history.replaceState(null,'',location.pathname+(q.size?'?'+q.toString():''));}catch{}}
  }
  form.addEventListener('submit',e=>{e.preventDefault();applyFilters();$('#result-summary').scrollIntoView({block:'center',behavior:'smooth'});});
  form.addEventListener('change',()=>applyFilters());
  let scoreTimer;score?.addEventListener('input',()=>{clearTimeout(scoreTimer);scoreTimer=setTimeout(()=>applyFilters(),300);});
  form.addEventListener('reset',()=>setTimeout(()=>{setQualification();applyFilters();},0));
  $('#reset-empty')?.addEventListener('click',()=>form.reset());
  const advanced=$('.advanced',form);if(['route','structure','science','english','cost'].some(k=>params.get(k)))advanced.open=true;
  applyFilters(false);
 }
}
const costForm=$('#cost-form');if(costForm){
 function calculate(){if(!costForm.reportValidity())return;const n=Object.fromEntries([...new FormData(costForm)].map(([k,v])=>[k,Number(v)]));if(Object.values(n).some(v=>!Number.isFinite(v)))return;const tuition=n.tuition*(1-n.discount/100),rent=n.rent*n.weeks,living=n.living*52,total=tuition+rent+living;const out=$('#cost-output');out.replaceChildren(text('span','입력한 가정으로 계산한 1년 예산'),text('strong','A$'+Math.round(total).toLocaleString('en-AU')),text('p',`약 ${Math.round(total*n.fx/10000).toLocaleString('ko-KR')}만 원 · 환율 A$1 = ${n.fx.toLocaleString('ko-KR')}원 가정`),text('p',`장학 가정 반영 학비 A$${Math.round(tuition).toLocaleString()} + 숙소 A$${rent.toLocaleString()} (${n.weeks}주) + 기타 생활비 A$${living.toLocaleString()} (52주)`));}
 costForm.addEventListener('submit',e=>{e.preventDefault();calculate();});
}
$('#copy-note')?.addEventListener('click',async()=>{const field=$('#consult-note');try{await navigator.clipboard.writeText(field.value);$('#copy-status').textContent='복사했습니다. 원하시는 상담 채널에 직접 붙여넣어 주세요.';}catch{field.focus();field.select();$('#copy-status').textContent='메모를 선택했습니다. 기기의 복사 기능으로 복사해 주세요.';}});
})();

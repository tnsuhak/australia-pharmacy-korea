/* Pure comparison rules. Unknown is never a pass; no admissions decision is made. */
(function(root){
  'use strict';
  const known=f=>f&&f.value!==null&&f.value!==undefined&&!['pending_2027','source_conflict'].includes(f.status);
  const read=f=>known(f)?f.value:null;
  function classify(p,f){
    const unknown=[],matches=[],misses=[];
    const check=(v,test,label)=>{if(v===null)unknown.push(label+' 정보 대기');else if(test(v))matches.push(label);else misses.push(label);};
    if(read(p.international_recruitment)!==true)unknown.push('2027 모집 발표 대기');
    if(p.accreditation.status==='pending_2027')unknown.push('APC·Board 승인 대기');
    const routeType=f.qualification==='graduate'?'graduate':f.route||'';
    const routes=p.entry_routes.filter(r=>!routeType||r.type===routeType);
    if(routeType&&routes.length===0)misses.push('선택한 입학방법 없음');
    if(routeType&&routes.length){
      if(!routes.some(r=>read(r.availability)===true))unknown.push('진학조건 발표 대기');
      else matches.push(routeType==='graduate'?'Graduate Entry 가능':'선택한 입학방법 가능');
    }
    const pathway=routeType&&routeType!=='direct';
    if(f.qualification&&f.qualification!=='graduate'){
      if(pathway)unknown.push('준비과정 학력조건 발표 대기');
      else{
        const q=p.qualifications.find(q=>q.qualification===f.qualification);const qv=q?read(q.score):null;
        if(qv===false)misses.push('해당 학력의 Direct 평가 불가');
        else if(qv===null)unknown.push('약대 성적기준 발표 대기');
        else if(q.score.source_year&&q.score.source_year<2027)unknown.push('성적표 '+q.score.source_year+' 참고 · 2027 재확인');
        else if(f.score!==''&&f.score!==undefined){
          if(!Number.isFinite(Number(f.score))||Number(f.score)<0)unknown.push('유효한 성적 입력 필요');
          else check(qv,v=>Number(f.score)>=v,'성적 기준');
        }else matches.push('해당 학력 기준 공개');
      }
    }
    if(f.qualification==='graduate'&&routes.length)unknown.push('관련 전공·대학 과목·성적 심사 필요');
    if(f.chemistry==='no'){
      if(pathway)unknown.push('준비과정 화학·진급조건 발표 대기');
      else check(read(p.requirements.chemistry),v=>['recommended','not_required','assumed'].includes(v),'화학 필수 아님');
    }
    if(f.chemistry==='yes')matches.push('화학 이수 · 과목 동등성 별도');
    if(f.science){const fct=p.requirements[f.science];check(read(fct),v=>f.science==='biology'?['accepted','required','recommended','assumed'].includes(v):v==='required','선수과목 분류');}
    if(f.intake){
      if(pathway){
        const starts=routes.map(r=>read(r.intake_months));
        if(starts.some(x=>Array.isArray(x)&&x.includes(Number(f.intake))))matches.push('선택한 입학월 가능');
        else if(starts.some(x=>x===null))unknown.push('시작월 발표 대기');
        else misses.push('선택한 입학월 가능');
      }else check(read(p.intakes.months),v=>v.includes(Number(f.intake)),'본과 시작월');
    }
    const years=read(p.duration_years);
    const duration=f.duration;
    if(duration){
      if(duration==='fast')check(years,v=>v<4||(p.id==='uq-bpharm-hons'&&f.intake!=='2'),'4년 미만 과정');
      else check(years,v=>v===Number(duration),'학위기간');
      if(pathway)unknown.push('준비과정 기간 추가');
    }
    if(f.structure){
      if(f.structure==='exit')check(read(p.four_year_exit),v=>v===true,'4년 Exit');
      else if(f.structure==='integrated')check(read(p.professional_registration.itp_in_degree),v=>v===true,'학위 내 ITP·등록 실무');
      else if(f.structure==='3.5')check(p.id==='uq-bpharm-hons'?true:years===null?null:false,v=>v&&f.intake!=='2','3.5년 경로');
      else if(f.structure==='3.75')check(years,v=>v===3.75,'3년 9개월');
      else check(years,v=>v===Number(f.structure),'세부 기간');
    }
    if(f.english){
      if(pathway)unknown.push('준비과정 영어 추가');
      else if(f.english==='pte')check(read(p.english.pte_overall),v=>typeof v==='number','PTE 공개');
      else{
        check(read(p.english.ielts_overall),v=>v<=Number(f.english),'IELTS overall 기준');
        if(p.english.ielts_overall.source_year&&p.english.ielts_overall.source_year<2027)unknown.push('2026 영어점수 참고');
      }
    }
    if(f.cost){
      if(f.cost==='housing'){
        const confirmed=p.accommodation.filter(h=>read(h.weekly_cost)!==null);
        if(!confirmed.length)unknown.push('공식 숙소비 미공개');
        else if(confirmed.some(h=>read(h.weekly_cost)<=350))matches.push('숙소 주 A$350 이하');
        else misses.push('숙소 주 A$350 이하');
      }else{
        const eligible=p.scholarships.filter(s=>read(s.country_eligibility)===true&&read(s.pharmacy_eligible)===true);
        const rates=s=>Array.isArray(read(s.amount))?Math.max(...read(s.amount)):read(s.amount);
        if(eligible.some(s=>rates(s)!==null&&(f.cost!=='20'||rates(s)>=20)))matches.push('한국학생 약대 장학 심사대상');
        else if(p.scholarships.some(s=>read(s.pharmacy_eligible)===null&&s.assessment!=='not_eligible'))unknown.push('약대 장학 적용 미확정');
        else misses.push('한국학생 약대 장학');
      }
    }
    // With "all routes", a failed Direct condition may still have a verified
    // preparation route. Keep it uncertain, never call it an eligible offer.
    if(!routeType && misses.some(x=>['성적 기준','해당 학력의 Direct 평가 불가','화학 필수 아님'].includes(x))){
      const alternatives=p.entry_routes.filter(r=>['foundation','diploma'].includes(r.type)&&read(r.availability)===true);
      if(alternatives.length){
        for(let i=misses.length-1;i>=0;i--)if(['성적 기준','해당 학력의 Direct 평가 불가','화학 필수 아님'].includes(misses[i]))misses.splice(i,1);
        unknown.push('Direct 조건 미충족 · '+alternatives.map(r=>r.title).join(' / ')+'');
      }
    }
    return {state:misses.length?'excluded':unknown.length?'pending':'match',matches,unknown,misses};
  }
  const api={known,read,classify};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.PharmacyMatcher=api;
})(typeof globalThis!=='undefined'?globalThis:this);

/* ============================================================
   WATER ON PAPER — viz + scroll engine
   Reveal/animation is driven by a throttled scroll checker
   (reliable in every render context). Everything is idempotent.
   ============================================================ */
(function(){
  const D = window.WOP;

  function inView(el, margin){
    const r = el.getBoundingClientRect();
    const vh = window.innerHeight || document.documentElement.clientHeight;
    const m = (margin==null? 0.10 : margin) * vh;     // reveal a little before fully in
    return r.top < (vh - m) && r.bottom > m*0.2;
  }

  /* ---------- count-up (idempotent) ---------- */
  function countUp(el){
    if(el.dataset.counted) return;
    el.dataset.counted = "1";
    const to = parseFloat(el.dataset.count);
    const dur = +(el.dataset.dur||1400), dec = +(el.dataset.dec||0), pre = el.dataset.pre||"", suf = el.dataset.suf||"";
    const start = performance.now();
    function frame(now){
      const t = Math.min(1,(now-start)/dur);
      const e = 1-Math.pow(1-t,3);
      const v = to*e;
      el.textContent = pre + (dec? v.toFixed(dec) : Math.round(v).toLocaleString('en-IN')) + suf;
      if(t<1) requestAnimationFrame(frame);
      else el.textContent = pre + (dec? to.toFixed(dec): to.toLocaleString('en-IN')) + suf;
    }
    requestAnimationFrame(frame);
  }

  /* ---------- Earth water dot-grid ---------- */
  function fillEarth(host){
    if(host.dataset.filled) return;
    host.dataset.filled = "1";
    host.classList.add('in');
    const { total, fresh, accessible } = D.EARTH;
    const dots = host.querySelectorAll('.d');
    setTimeout(()=>{
      for(let i=0;i<fresh;i++) dots[total-1-i] && dots[total-1-i].classList.add('fresh');
      for(let i=0;i<accessible;i++){ const d=dots[total-1-i]; if(d){ d.classList.remove('fresh'); d.classList.add('access'); } }
    }, 450);
  }
  function buildEarth(){
    const host = document.getElementById('earth-dots');
    if(!host) return;
    const frag = document.createDocumentFragment();
    for(let i=0;i<D.EARTH.total;i++){
      const d = document.createElement('span'); d.className='d';
      d.style.transitionDelay = (Math.random()*0.5).toFixed(2)+'s';
      frag.appendChild(d);
    }
    host.appendChild(frag);
  }

  /* ---------- bar charts ---------- */
  function fillBars(host){
    if(host.dataset.filled) return;
    host.dataset.filled = "1";
    host.querySelectorAll('.bfill').forEach((f,i)=>{ setTimeout(()=>{ f.style.width = f.dataset.w+'%'; }, 80*i); });
  }
  function buildBars(hostId, data, scaleMax){
    const host = document.getElementById(hostId);
    if(!host) return;
    const max = scaleMax || Math.max(...data.map(d=>d.val));
    data.forEach(d=>{
      const row = document.createElement('div'); row.className='bar';
      const pct = Math.max(1.2, (d.val/max)*100);
      row.innerHTML =
        `<div class="blabel">${d.label}${d.sub?`<small>${d.sub}</small>`:''}</div>
         <div class="btrack"><div class="bfill ${d.tone||''}" data-w="${pct}"></div></div>
         <div class="bval">${d.disp || d.val.toLocaleString('en-IN')}</div>`;
      host.appendChild(row);
    });
  }
  function buildGlobal(){
    buildBars('global-bars', D.GLOBAL.map(g=>({ label:g.label, sub:g.sub, val:g.pct, disp:`${g.val} ${g.unit}`, tone:g.tone })), 100);
  }
  function buildFootprints(){ buildBars('footprint-bars', D.FOOTPRINTS, 15400); }

  /* ---------- ten most water-affected countries (Chapter 03) ---------- */
  function buildCountries(){
    const list = document.getElementById('country-list');
    const detail = document.getElementById('country-detail');
    if(!list || !detail || !D.COUNTRIES) return;
    const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

    function renderDetail(c){
      const orgs = (c.orgs||[]).map(o=>{
        const tag = o.url ? 'a' : 'div';
        const href = o.url ? ` href="${o.url}" target="_blank" rel="noopener"` : '';
        return `<${tag} class="cd-org"${href}>
            <span class="on">${esc(o.name)}</span>
            <span class="ow">${esc(o.what)}</span>
          </${tag}>`;
      }).join('');
      const deep = c.deepdive
        ? `<a class="cd-deep" href="#ch04">Open the India deep dive ↓</a>` : '';
      detail.innerHTML = `
        <h3 class="cd-name">${esc(c.name)}</h3>
        <p class="cd-region">${esc(c.region)}</p>
        <div class="cd-stat">
          <span class="cd-big" style="color:var(--s${c.stress})">${esc(c.stat)}</span>
          <span class="cd-lbl">${esc(c.statLbl)}</span>
        </div>
        <div class="cd-block">
          <div class="k">The challenge</div>
          <div class="v">${esc(c.challenge)}</div>
        </div>
        <div class="cd-block">
          <div class="k">Where the water comes from</div>
          <div class="v src-v">${esc(c.source)}</div>
        </div>
        <div class="cd-orgs">
          <div class="k">Groups working on it</div>
          ${orgs}
        </div>
        ${deep}`;
    }

    D.COUNTRIES.forEach((c,i)=>{
      const row = document.createElement('button');
      row.type = 'button';
      row.className = 'crow' + (c.deepdive ? ' india' : '');
      row.setAttribute('role','listitem');
      row.dataset.key = c.key;
      row.innerHTML = `
        <span class="crank">${String(i+1).padStart(2,'0')}</span>
        <span class="cmain">
          <span class="cname">${esc(c.name)}</span>
          <span class="creg">${esc(c.region)}</span>
        </span>
        <span class="cmeta">
          <span class="cstat">${esc(c.stat)}</span>
          <span class="cdot" style="background:var(--s${c.stress})"></span>
        </span>`;
      row.addEventListener('click', ()=>{
        list.querySelectorAll('.crow').forEach(r=>r.classList.remove('active'));
        row.classList.add('active');
        renderDetail(c);
      });
      list.appendChild(row);
    });

    // open on India — it sets up the deep-dive that follows
    const start = D.COUNTRIES.find(c=>c.deepdive) || D.COUNTRIES[0];
    const startRow = list.querySelector(`.crow[data-key="${start.key}"]`);
    if(startRow) startRow.classList.add('active');
    renderDetail(start);
  }

  /* ---------- the one reliable checker ---------- */
  let ticking = false;
  function check(){
    ticking = false;
    document.querySelectorAll('[data-reveal]:not(.in)').forEach(el=>{ if(inView(el)) el.classList.add('in'); });
    document.querySelectorAll('[data-count]').forEach(el=>{ if(!el.dataset.counted && inView(el)) countUp(el); });
    const earth = document.getElementById('earth-dots'); if(earth && !earth.dataset.filled && inView(earth)) fillEarth(earth);
    document.querySelectorAll('.barchart').forEach(b=>{ if(!b.dataset.filled && inView(b,0.20)) fillBars(b); });
  }
  function onScroll(){ if(!ticking){ ticking = true; requestAnimationFrame(check); } }

  document.addEventListener('DOMContentLoaded', ()=>{
    buildEarth(); buildGlobal(); buildFootprints(); buildCountries();
    check();
    document.addEventListener('scroll', onScroll, {passive:true});
    window.addEventListener('resize', onScroll, {passive:true});
    // a couple of settle passes for fonts/layout shifts
    [120, 500, 1200].forEach(t=>setTimeout(check, t));
  });
  window.addEventListener('load', check);

  window.WOPviz = { check, countUp };
})();

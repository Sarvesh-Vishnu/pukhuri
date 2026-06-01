/* ============================================================
   WATER ON PAPER — nav, progress, chrome
   ============================================================ */
(function(){
  /* progress bar */
  const bar = document.getElementById('progress');
  function onScroll(){
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    const p = max>0 ? (h.scrollTop || document.body.scrollTop)/max : 0;
    if(bar) bar.style.width = (p*100).toFixed(2)+'%';
  }
  document.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* drawer */
  const drawer = document.getElementById('drawer');
  const openBtn = document.getElementById('menu-open');
  const closeBtn = document.getElementById('menu-close');
  const open = ()=> drawer && drawer.classList.add('open');
  const close = ()=> drawer && drawer.classList.remove('open');
  openBtn && openBtn.addEventListener('click', open);
  closeBtn && closeBtn.addEventListener('click', close);
  drawer && drawer.addEventListener('click', e=>{ if(e.target===drawer) close(); });
  document.querySelectorAll('.toc-item').forEach(a=>a.addEventListener('click', close));
  document.addEventListener('keydown', e=>{ if(e.key==='Escape') close(); });

  /* toggle dark chrome when a dark section is under the top bar */
  const darkSections = [...document.querySelectorAll('section.dark, section.clay-bg, .foot')];
  const darkObs = new IntersectionObserver((entries)=>{
    // a dark section counts as "under the bar" if its top is above 70px and bottom below 70px
    entries.forEach(()=>{});
    let dark = false;
    darkSections.forEach(s=>{
      const r = s.getBoundingClientRect();
      if(r.top <= 64 && r.bottom >= 64) dark = true;
    });
    document.body.classList.toggle('on-dark', dark);
  },{ threshold:[0,0.01,0.99,1], rootMargin:"0px" });
  // observer fires on enter/leave; also bind scroll for precision
  darkSections.forEach(s=>darkObs.observe(s));
  function checkDark(){
    let dark=false;
    darkSections.forEach(s=>{ const r=s.getBoundingClientRect(); if(r.top<=64 && r.bottom>=64) dark=true; });
    document.body.classList.toggle('on-dark', dark);
  }
  document.addEventListener('scroll', checkDark, {passive:true});
  checkDark();
})();

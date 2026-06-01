/* ============================================================
   WATER ON PAPER — India cartogram + the Neer tool
   (Neer नीर — the rename of Pukhuri, merged in as Chapter 06)
   ============================================================ */
(function(){
  const D = window.WOP;
  const stressColor = k => `var(--s${k})`;
  const stressLabel = k => (D.STRESS.find(s=>s.k===k)||{}).label || "";

  /* ---------- big cartogram (Chapter 04) ---------- */
  function buildCarto(){
    const grid = document.getElementById('carto-grid');
    if(!grid) return;
    const side = document.getElementById('carto-side');
    D.STATES.forEach(s=>{
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.style.gridColumn = s.c; cell.style.gridRow = s.r;
      cell.style.background = stressColor(s.stress);
      cell.dataset.ab = s.ab;
      cell.dataset.stress = s.stress;
      const dots = '<i></i>'.repeat(Math.min(4, s.cont.length));
      cell.innerHTML = `<span class="c-num">${s.stress}</span><span class="c-sym">${s.ab}</span><span class="c-dots">${dots}</span>`;
      cell.title = `${s.name} — ${stressLabel(s.stress)}`;
      cell.addEventListener('mouseenter', ()=> showSide(s, cell));
      cell.addEventListener('click', ()=> showSide(s, cell));
      grid.appendChild(cell);
    });
    function showSide(s, cell){
      grid.querySelectorAll('.cell').forEach(c=>c.classList.remove('active'));
      cell.classList.add('active');
      side.querySelector('.panel-title').textContent = s.name;
      side.querySelector('.panel-sub').textContent = s.region + " · " + stressLabel(s.stress);
      side.querySelector('[data-f="source"]').textContent = s.source;
      side.querySelector('[data-f="cont"]').textContent = s.cont.join(", ");
      const pill = side.querySelector('.stress-pill');
      pill.style.background = stressColor(s.stress);
      pill.querySelector('span.txt').textContent = stressLabel(s.stress);
    }
    // default selection
    const def = D.STATES.find(s=>s.ab==='PB');
    const defCell = grid.querySelector('[data-ab="PB"]');
    if(def && defCell) showSide(def, defCell);
  }

  /* ---------- Neer tool (Chapter 06) ---------- */
  function buildTool(){
    const host = document.getElementById('neer-tool');
    if(!host) return;

    const sel = host.querySelector('#neer-state');
    const miniGrid = host.querySelector('#neer-mini');
    const info = host.querySelector('#neer-info');

    // populate select (alpha by name)
    [...D.STATES].sort((a,b)=>a.name.localeCompare(b.name)).forEach(s=>{
      const o = document.createElement('option');
      o.value = s.ab; o.textContent = s.name;
      sel.appendChild(o);
    });

    // mini cartogram
    D.STATES.forEach(s=>{
      const cell = document.createElement('div');
      cell.className = 'cell';
      cell.style.gridColumn = s.c; cell.style.gridRow = s.r;
      cell.style.background = stressColor(s.stress);
      cell.dataset.ab = s.ab;
      cell.textContent = s.ab;
      cell.title = s.name;
      cell.addEventListener('click', ()=> select(s.ab));
      miniGrid.appendChild(cell);
    });

    function render(s){
      miniGrid.querySelectorAll('.cell').forEach(c=>c.classList.toggle('active', c.dataset.ab===s.ab));
      sel.value = s.ab;
      const cont = s.cont.map((c,i)=> `<span class="chip">${c}</span>`).join('');
      info.innerHTML = `
        <h3 class="ti-state">${s.name}</h3>
        <p class="ti-region">${s.region}</p>
        <div class="ti-block">
          <div class="k">Main water source</div>
          <div class="v">${s.source}</div>
        </div>
        <div class="ti-block">
          <div class="k">Known contaminants</div>
          <div class="v"><div class="chiprow">${cont}</div></div>
        </div>
        <div class="ti-block">
          <div class="k">Groundwater & supply stress</div>
          <div class="v"><span class="stress-pill" style="background:${stressColor(s.stress)}"><span class="sdot"></span>${stressLabel(s.stress)}</span></div>
        </div>
        <div class="ti-action">
          <b>On the ground &rarr;</b> ${s.note}
        </div>`;
    }
    function select(ab){
      const s = D.STATES.find(x=>x.ab===ab);
      if(s) render(s);
    }
    sel.addEventListener('change', ()=> select(sel.value));

    select('MP'); // open on Madhya Pradesh — the Indore story
  }

  document.addEventListener('DOMContentLoaded', ()=>{ buildCarto(); buildTool(); });
})();

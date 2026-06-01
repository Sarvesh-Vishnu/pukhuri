/* ============================================================
   WATER ON PAPER — data layer
   All figures sourced; see SOURCES[] and the footer.
   Stress scale: 0 safe · 1 semi-critical · 2 critical · 3 over-exploited · 4 severe
   ============================================================ */
window.WOP = (function(){

  /* ---- Earth's water as 100 drops ---- */
  const EARTH = { total: 100, fresh: 3 /* ~2.5% */, accessible: 1 /* <1% liquid surface */ };

  /* ---- Global access bands (WHO/UNICEF JMP) ---- */
  const GLOBAL = [
    { label:"Lack safely managed drinking water", sub:"WHO/UNICEF JMP", val:2.2, unit:"billion people", pct:100, tone:"clay" },
    { label:"No safe water at home — collected elsewhere", sub:"basic or worse", val:703, unit:"million", pct:32, tone:"deep" },
    { label:"Lack safely managed sanitation", sub:"linked to contamination", val:3.5, unit:"billion", pct:100, tone:"water" }
  ];

  /* ---- Top 10 most water-affected countries (WRI Aqueduct + JMP framing).
          A deliberate blend of extreme scarcity (MENA), giant-population
          stress (Asia), and access gaps (Sub-Saharan) so India is in
          company, not isolation. India links down to the deep-dive. ---- */
  const COUNTRIES = [
    { key:"YE", name:"Yemen", region:"Middle East", stress:4,
      stat:"first", statLbl:"Sana'a is projected to be one of the first capital cities on Earth to run out of water.",
      source:"Fossil groundwater & trucked water", challenge:"Aquifers drained faster than they can ever refill — for farming and through years of conflict that shattered the supply network.",
      orgs:[ {name:"UNICEF Yemen — WASH", what:"emergency water & sanitation"}, {name:"Oxfam", what:"clean-water response", url:"https://www.oxfam.org"} ] },
    { key:"IN", name:"India", region:"South Asia", stress:4, deepdive:true,
      stat:"600M", statLbl:"people under high-to-extreme water stress — and the world's single largest user of groundwater.",
      source:"Groundwater, rivers & reservoirs", challenge:"18% of the world's people living on 4% of its fresh water, spending the savings faster than the rain returns them.",
      orgs:[ {name:"WaterAid India", what:"safe water & hygiene, nationwide", url:"https://www.wateraidindia.in"}, {name:"Water.org", what:"water credit & access", url:"https://water.org"} ] },
    { key:"PK", name:"Pakistan", region:"South Asia", stress:4,
      stat:"1 river", statLbl:"A booming population leans almost entirely on the Indus — and is sliding toward absolute scarcity.",
      source:"Indus basin & groundwater", challenge:"Silting reservoirs, leaky canals and little storage leave the country dangerously exposed to a single river system.",
      orgs:[ {name:"WaterAid Pakistan", what:"rural & urban water", url:"https://www.wateraid.org/pk/"}, {name:"Indus Earth Trust", what:"coastal water harvesting"} ] },
    { key:"IR", name:"Iran", region:"Middle East", stress:4,
      stat:"sinking", statLbl:"Plains across Iran are dropping as the aquifers beneath them are pumped dry.",
      source:"Dams & deep groundwater", challenge:"Decades of dam-building and over-extraction have drained reserves; land subsidence and dust storms now follow the falling water table.",
      orgs:[ {name:"Local WASH & NGO efforts", what:"community water programmes"} ] },
    { key:"SA", name:"Saudi Arabia", region:"Gulf", stress:4,
      stat:"~0", statLbl:"Almost no renewable fresh water — among the most water-scarce nations on the planet.",
      source:"Desalination & fossil aquifers", challenge:"Drinking the sea at enormous energy cost while ancient, non-renewable aquifers are spent on agriculture.",
      orgs:[ {name:"Regional water charities", what:"WASH across the Gulf & MENA"} ] },
    { key:"CN", name:"China", region:"East Asia", stress:3,
      stat:"north/south", statLbl:"Most people live in the south; much of the water sits in the north — so China pipes rivers across the country.",
      source:"Rivers, mega-transfers & groundwater", challenge:"The North China Plain aquifer is among the most depleted on Earth, propping up farms and megacities.",
      orgs:[ {name:"charity: water — partners", what:"rural water projects", url:"https://www.charitywater.org"} ] },
    { key:"ZA", name:"South Africa", region:"Southern Africa", stress:3,
      stat:"Day Zero", statLbl:"In 2018, Cape Town counted publicly toward the day its taps would be switched off.",
      source:"Reservoirs & rivers", challenge:"Drought plus rapid growth nearly emptied a major city's dams — a dress rehearsal the whole world watched.",
      orgs:[ {name:"Gift of the Givers", what:"drought & water relief", url:"https://giftofthegivers.org"}, {name:"WaterAid", what:"WASH, Southern Africa", url:"https://www.wateraid.org"} ] },
    { key:"MX", name:"Mexico", region:"Latin America", stress:3,
      stat:"50 cm/yr", statLbl:"Mexico City sinks up to half a metre a year as it pumps the aquifer beneath a drained lakebed.",
      source:"Aquifers & distant reservoirs", challenge:"A megacity loses roughly 40% of its water to leaks while drawing more than the ground can give.",
      orgs:[ {name:"Isla Urbana", what:"rainwater harvesting", url:"https://islaurbana.org"}, {name:"Cántaro Azul", what:"rural safe water"} ] },
    { key:"US", name:"United States", region:"North America", stress:3,
      stat:"Colorado", statLbl:"The over-allocated Colorado River often no longer reaches the sea — and AI data centres are arriving in its driest basins.",
      source:"Rivers, reservoirs & groundwater", challenge:"Southwest mega-drought collides with booming, thirsty computing — wealth is no immunity from scarcity.",
      orgs:[ {name:"DigDeep", what:"water access in the US", url:"https://www.digdeep.org"}, {name:"Water.org", what:"global & US access", url:"https://water.org"} ] },
    { key:"ET", name:"Ethiopia", region:"East Africa", stress:3,
      stat:"distance", statLbl:"For millions, the barrier isn't scarcity but distance — hours walked for water that may not be safe.",
      source:"Rivers, springs & boreholes", challenge:"Real progress meets vast rural distances and swinging rains; the access frontier is the last mile.",
      orgs:[ {name:"charity: water", what:"wells & springs", url:"https://www.charitywater.org"}, {name:"WaterAid", what:"rural WASH", url:"https://www.wateraid.org"} ] }
  ];

  /* ---- Product / activity water footprints (litres). ---- */
  const FOOTPRINTS = [
    { label:"100-word AI prompt", sub:"contested estimate", val:0.5,    disp:"~0.5 L", tone:"deep" },
    { label:"Cup of coffee",      sub:"125 ml brewed",      val:140,    disp:"140 L",  tone:"water" },
    { label:"Cotton t-shirt",     sub:"one garment",        val:2700,   disp:"2,700 L",tone:"water" },
    { label:"Rice",               sub:"per kg",             val:2500,   disp:"2,500 L",tone:"water" },
    { label:"Almonds",            sub:"per kg",             val:8000,   disp:"~8,000 L",tone:"clay" },
    { label:"Beef",               sub:"per kg",             val:15400,  disp:"15,400 L",tone:"clay" }
  ];

  /* ---- AI / data-centre figures ---- */
  const AI = {
    withdraw: 29, consume: 23, potablePct: 80,
    dc100mw: 2, households: 6500,
    globalNow: 560, global2030: 1200,
    evapPct: 80, perPromptMl: 519
  };

  const INDIA = { popShare:18, freshShare:4, stressedMillions:600, diseaseCases:30, annualDeaths:300000, jjmStart:2019 };
  const INDORE = { dead:15, ill:2000, screened:40000, cleanestYears:8 };

  /* ---- India cartogram + the Neer tool ---- */
  const STATES = [
    { ab:"LA", name:"Ladakh",            c:5, r:1, region:"Trans-Himalaya", stress:1,
      source:"Glacial melt & springs", cont:["Sediment","Seasonal scarcity"],
      note:"Springsheds and glacier melt feed most villages — recharge is climate-fragile.",
      orgs:[{name:"Himalayan Institute of Alternatives (Ice Stupa)", what:"artificial glaciers store winter water"}, {name:"SECMOL", what:"community water & education"}] },
    { ab:"JK", name:"Jammu & Kashmir",   c:4, r:1, region:"North",          stress:1,
      source:"Rivers & springs", cont:["Turbidity","Bacterial"],
      note:"Surface-water rich, but treatment gaps drive monsoon contamination spikes.",
      orgs:[{name:"WaterAid India", what:"safe water & hygiene", url:"https://www.wateraidindia.in"}] },
    { ab:"HP", name:"Himachal Pradesh",  c:4, r:2, region:"Hills",          stress:0,
      source:"Himalayan rivers & springs", cont:["Turbidity"],
      note:"Among India's most water-secure states; gravity schemes serve hill hamlets.",
      orgs:[{name:"Himmotthan Society", what:"Himalayan spring revival"}] },
    { ab:"PB", name:"Punjab",            c:3, r:2, region:"North-west",      stress:4,
      source:"Groundwater (tubewells)", cont:["Uranium","Nitrate","Pesticides"],
      note:"Paddy-wheat farming has crashed the water table; uranium and nitrate are now widespread.",
      orgs:[{name:"WaterAid India", what:"water quality & access", url:"https://www.wateraidindia.in"}, {name:"Kheti Virasat Mission", what:"sustainable, low-water farming"}] },
    { ab:"UK", name:"Uttarakhand",       c:5, r:2, region:"Hills",          stress:1,
      source:"Himalayan rivers & springs", cont:["Turbidity","Drying springs"],
      note:"Thousands of springs are drying — the source for most mountain villages.",
      orgs:[{name:"Himmotthan Society", what:"spring-shed restoration"}] },
    { ab:"HR", name:"Haryana",           c:3, r:3, region:"North-west",      stress:4,
      source:"Groundwater & canals", cont:["Nitrate","Salinity","Fluoride"],
      note:"Severely over-exploited blocks ring Delhi; rainwater harvesting is mandated on paper, not enforced.",
      orgs:[{name:"S M Sehgal Foundation", what:"rural water management"}] },
    { ab:"DL", name:"Delhi",             c:4, r:3, region:"Capital",         stress:4,
      source:"Yamuna, Ganga canal, groundwater", cont:["Ammonia","Sewage","Nitrate"],
      note:"Demand far outruns the Yamuna's safe yield; ammonia spikes shut treatment plants.",
      orgs:[{name:"FORCE", what:"water conservation & advocacy"}, {name:"WaterAid India", what:"urban WASH", url:"https://www.wateraidindia.in"}] },
    { ab:"RJ", name:"Rajasthan",         c:3, r:4, region:"West (arid)",     stress:4,
      source:"Groundwater & tankers", cont:["Fluoride","Salinity","Nitrate"],
      note:"India's driest large state; high fluoride causes skeletal fluorosis — test before drinking any new borewell.",
      orgs:[{name:"Tarun Bharat Sangh", what:"reviving traditional johads", url:"https://www.tarunbharatsangh.in"}, {name:"Jal Bhagirathi Foundation", what:"desert water security"}] },
    { ab:"UP", name:"Uttar Pradesh",     c:5, r:3, region:"Gangetic plain",  stress:3,
      source:"Ganga basin & groundwater", cont:["Arsenic","Fluoride","Nitrate"],
      note:"Arsenic belts along the Ganga affect millions; demand piped surface water in mapped blocks.",
      orgs:[{name:"WaterAid India", what:"arsenic-safe water", url:"https://www.wateraidindia.in"}] },
    { ab:"BR", name:"Bihar",             c:6, r:3, region:"Gangetic plain",  stress:3,
      source:"Groundwater & rivers", cont:["Arsenic","Iron","Fluoride"],
      note:"Among the worst arsenic exposure in India; shallow hand-pumps are the risk.",
      orgs:[{name:"Megh Pyne Abhiyan", what:"flood-plain water & sanitation"}, {name:"WaterAid India", what:"safe water", url:"https://www.wateraidindia.in"}] },
    { ab:"AR", name:"Arunachal",         c:9, r:2, region:"North-east",      stress:0,
      source:"Rain-fed rivers & springs", cont:["Turbidity"],
      note:"Abundant rainfall; the challenge is reaching remote hamlets, not supply.",
      orgs:[{name:"WaterAid India", what:"last-mile rural water", url:"https://www.wateraidindia.in"}] },
    { ab:"GJ", name:"Gujarat",           c:2, r:5, region:"West",            stress:3,
      source:"Narmada canal & groundwater", cont:["Salinity","Fluoride","Nitrate"],
      note:"Coastal aquifers are turning saline as the sea intrudes over-pumped wells.",
      orgs:[{name:"Aga Khan Rural Support Programme", what:"watershed & water harvesting"}, {name:"Utthan", what:"coastal & saline-area water"}] },
    { ab:"MP", name:"Madhya Pradesh",    c:4, r:4, region:"Central",         stress:2,
      source:"Rivers, reservoirs & groundwater", cont:["Fluoride","Nitrate","Sewage (urban)"],
      note:"Indore — India's 'cleanest city' — saw sewage seep into a drinking line in Dec 2025, killing at least 15. Clean ≠ safe water.",
      orgs:[{name:"Samerth Charitable Trust", what:"water security in central India"}, {name:"WaterAid India", what:"urban & rural WASH", url:"https://www.wateraidindia.in"}] },
    { ab:"JH", name:"Jharkhand",         c:6, r:4, region:"East",            stress:1,
      source:"Rivers & groundwater", cont:["Iron","Fluoride"],
      note:"Water is available but iron and fluoride are common; source treatment is patchy.",
      orgs:[{name:"WaterAid India", what:"tribal-belt water access", url:"https://www.wateraidindia.in"}] },
    { ab:"WB", name:"West Bengal",       c:7, r:4, region:"East",            stress:3,
      source:"Groundwater & rivers", cont:["Arsenic","Iron","Salinity"],
      note:"The world's most-studied arsenic crisis sits here — mapped for decades, safe piped water still lags.",
      orgs:[{name:"Safe Water Network", what:"arsenic-removal water stations", url:"https://www.safewaternetwork.org"}, {name:"WaterAid India", what:"safe water", url:"https://www.wateraidindia.in"}] },
    { ab:"AS", name:"Assam",             c:8, r:3, region:"North-east",      stress:1,
      source:"Brahmaputra basin & groundwater", cont:["Arsenic","Iron","Fluoride"],
      note:"Water-abundant yet chemically contaminated — arsenic and iron in shallow tubewells.",
      orgs:[{name:"WaterAid India", what:"north-east WASH", url:"https://www.wateraidindia.in"}] },
    { ab:"MH", name:"Maharashtra",       c:3, r:5, region:"West",            stress:3,
      source:"Dams & reservoirs", cont:["Nitrate","Fluoride","Turbidity"],
      note:"Marathwada's recurring drought drives tanker dependence while cane farming drinks the dams.",
      orgs:[{name:"Watershed Organisation Trust (WOTR)", what:"watershed & drought resilience", url:"https://wotr.org"}, {name:"ACWADAM", what:"groundwater science & management"}] },
    { ab:"CG", name:"Chhattisgarh",      c:5, r:4, region:"Central",         stress:1,
      source:"Rivers & groundwater", cont:["Iron","Fluoride"],
      note:"Relatively water-secure; fluoride pockets need point-of-use removal.",
      orgs:[{name:"Samerth Charitable Trust", what:"community water security"}] },
    { ab:"OD", name:"Odisha",            c:5, r:5, region:"East coast",      stress:1,
      source:"Rivers & groundwater", cont:["Iron","Salinity (coastal)","Fluoride"],
      note:"Cyclone surge salts coastal wells; iron is the everyday issue.",
      orgs:[{name:"Gram Vikas", what:"village-wide piped water & sanitation", url:"https://www.gramvikas.org"}] },
    { ab:"TG", name:"Telangana",         c:4, r:5, region:"South (Deccan)",  stress:3,
      source:"Reservoirs & groundwater", cont:["Fluoride","Nitrate"],
      note:"Hard Deccan rock means deep, fast-falling borewells and high fluoride.",
      orgs:[{name:"WASSAN", what:"water & rain-fed farming, Deccan"}, {name:"Safe Water Network", what:"safe-water stations", url:"https://www.safewaternetwork.org"}] },
    { ab:"GA", name:"Goa",               c:3, r:6, region:"West coast",      stress:1,
      source:"Rivers & reservoirs", cont:["Salinity (coastal)","Bacterial"],
      note:"Surface-water rich; tourism load and saline intrusion stress coastal supply in summer.",
      orgs:[{name:"WaterAid India", what:"coastal WASH", url:"https://www.wateraidindia.in"}] },
    { ab:"KA", name:"Karnataka",         c:4, r:6, region:"South",           stress:3,
      source:"Reservoirs & groundwater", cont:["Nitrate","Fluoride","Hardness"],
      note:"Bengaluru's borewells run deep and dry while it pumps Cauvery water uphill.",
      orgs:[{name:"Arghyam", what:"groundwater & water-sanitation funding", url:"https://arghyam.org"}, {name:"Biome Environmental Trust", what:"urban rainwater & open wells"}] },
    { ab:"AP", name:"Andhra Pradesh",    c:5, r:6, region:"South-east coast",stress:2,
      source:"Rivers & groundwater", cont:["Fluoride","Salinity","Nitrate"],
      note:"Fluoride belts (the Nalgonda legacy) and coastal salinity; defluoridation at source is the promise.",
      orgs:[{name:"WASSAN", what:"community water management"}, {name:"Safe Water Network", what:"safe-water stations", url:"https://www.safewaternetwork.org"}] },
    { ab:"KL", name:"Kerala",            c:3, r:7, region:"South-west coast",stress:1,
      source:"Rivers & high rainfall", cont:["Bacterial","Iron","Salinity (coastal)"],
      note:"India's wettest state still faces summer scarcity and bacterial contamination — storage and treatment, not rainfall, are the gap.",
      orgs:[{name:"Mazhapolima", what:"rooftop rainwater well-recharge"}] },
    { ab:"TN", name:"Tamil Nadu",        c:4, r:7, region:"South",           stress:3,
      source:"Reservoirs & groundwater", cont:["Salinity","Fluoride","Nitrate"],
      note:"Chennai hit 'Day Zero' in 2019 when its reservoirs ran dry; rainwater harvesting has been law here since 2003.",
      orgs:[{name:"Gramalaya", what:"rural water & sanitation"}, {name:"Rain Centre, Chennai", what:"rainwater-harvesting know-how"}] }
  ];

  const STRESS = [
    { k:0, label:"Safe / surplus",   color:"var(--s0)" },
    { k:1, label:"Semi-critical",    color:"var(--s1)" },
    { k:2, label:"Critical",         color:"var(--s2)" },
    { k:3, label:"Over-exploited",   color:"var(--s3)" },
    { k:4, label:"Severe stress",    color:"var(--s4)" }
  ];

  const SOURCES = [
    "WHO / UNICEF Joint Monitoring Programme (JMP), Drinking Water 2023.",
    "World Resources Institute, Aqueduct Water Risk Atlas — country-level baseline water stress.",
    "NITI Aayog, Composite Water Management Index (2018) — 600 million Indians under high-to-extreme water stress.",
    "Central Ground Water Board (CGWB), Dynamic Groundwater Resources of India; state contamination atlases.",
    "Ministry of Health & Family Welfare / WHO — ~30 million waterborne-disease cases and ~300,000 deaths a year in India.",
    "2025 Indore drinking-water contamination — municipal sewage ingress, Bhagirathpura; ≥15 deaths, ~2,000 ill (district administration; news reporting, Dec 2025–Jan 2026).",
    "Water Footprint Network; Hoekstra & Mekonnen — product water footprints (beef, rice, cotton, coffee, almonds).",
    "International Energy Agency, Energy & AI (2025) — a 100-MW data centre consumes ~2 million L/day; global DC water ~560 bn L → ~1,200 bn L by 2030.",
    "Li, Yang, Islam & Ren, 'Making AI Less Thirsty' (UC Riverside, 2023/25) — withdrawal vs consumption; one firm's self-owned DCs withdrew 29 bn L, evaporated 23 bn L (≈80% potable) in 2023.",
    "Lawrence Berkeley National Laboratory (2025) — data-centre water intensity varies ~10,000× by site and cooling type; per-query figures carry enormous error margins.",
    "Organisation links are starting points for your own research — please verify each before donating."
  ];

  return { EARTH, GLOBAL, COUNTRIES, FOOTPRINTS, AI, INDIA, INDORE, STATES, STRESS, SOURCES };
})();

// Renders every tool in Node with a minimal fake DOM and checks key behaviour.
// Run after building:  node tests/smoke.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'dist', 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const els = {};
const attrs = () => { const a = {}; return { setAttribute(k, v) { a[k] = String(v); }, removeAttribute(k) { delete a[k]; }, getAttribute(k) { return k in a ? a[k] : null; } }; };
const el = id => els[id] || (els[id] = { id, innerHTML: '', textContent: '', value: '', checked: false, hidden: false, addEventListener() {}, ...attrs() });
global.document = { getElementById: el, documentElement: attrs(), addEventListener() {}, querySelector: () => null, querySelectorAll: () => [] };
global.location = { hash: '' }; global.history = { replaceState() {} };
global.window = global; global.scrollTo = () => {};
new Function(script)();
const N = window.__NETRA;
let fail = 0;
const check = (c, m) => { if (!c) { fail++; console.error('FAIL', m); } else console.log('ok  ', m); };

const D = JSON.parse(script.match(/const PAYLOAD = (\{[\s\S]*?\});\n\(function/)[1]).india;
for (const v of Object.keys(N.PAGES)) {
  let out = '';
  try { out = N.page(v); } catch (e) { check(false, `page "${v}" threw ${e.message}`); continue; }
  check(out.length > 300 && !/[>"(]undefined[<")]/.test(out) && !/>null</.test(out), `page "${v}" renders (${out.length} chars)`);
  // The generated report document has its own section headings; page headings are checked outside it
  const pageOnly = out.replace(/<article class="sheet report"[\s\S]*?<\/article>/, '');
  const bare = (pageOnly.match(/<\/h[23]>(?!\s*<p class="hint")/g) || []).length;
  check(bare === 0, `page "${v}": every heading has a one-line explanation`);
  check(!/[ऀ-ॿ]/.test(out), `page "${v}": no Devanagari outside the title`);
}
const shell = html.slice(html.indexOf('<header'), html.indexOf('<script>'));
check((shell.match(/[ऀ-ॿ]+/g) || []).every(w => w === 'नेत्र'), 'Devanagari appears only as the title नेत्र');
check(!/class="stats"|class="stat"/.test(N.page('home')), 'home has no separate stat boxes');
check(!N.page('home').includes('Explore the cases') && !N.page('home').includes('data-tour="start"'), 'home banner has no buttons repeating the header');
const nRev = D.incidents.filter(i => i.review !== 'unreviewed').length;
check(N.page('home').includes(`data-count="${D.incidents.length}"`) && N.page('home').includes(`${nRev} reviewed by a person · ${D.incidents.length - nRev} unreviewed`) && N.page('home').includes(D.meta.updated), 'home counter is computed from the data, with the update date');
for (const [old, now] of [['navigator','explore-area'],['risks','explore-risks'],['incidents','explore-incidents'],['governance','explore-laws'],['mitigations','explore-measures'],['netra','analysis-dossiers'],['gaps','analysis-gaps'],['evidence','analysis-models'],['about-evidence','analysis-models'],['survey','about-survey'],['about','about-method']])
  check(N.resolve(old) === now, `old link #${old} opens ${now}`);
check(Object.keys(N.PAGES).every(k => /^[A-Za-z0-9._~-]+$/.test(k)), 'every page address is a plain shareable token');
N.state.showFilters = false;
check(/id="filterpanel" hidden/.test(N.page('explore-incidents')), 'filters stay hidden until the Filters button is clicked');
N.state.showFilters = true;
check(!/id="filterpanel" hidden/.test(N.page('explore-incidents')), 'Filters button shows the filters');
N.state.f.incidents = { dom: '4' };
const inc = N.page('explore-incidents');
check(inc.includes('IN-INC-03') && !inc.includes('id="IN-INC-11"'), 'incident filter by risk domain narrows the list');
N.state.f.incidents = { sev: '4' };
check(N.page('explore-incidents').includes('id="IN-INC-11"') && !N.page('explore-incidents').includes('id="IN-INC-03"'), 'severity filter keeps only S4+');
N.state.f.incidents = {}; N.state.q = 'voice';
check(N.page('explore-incidents').includes('id="IN-INC-07"') && !N.page('explore-incidents').includes('id="IN-INC-11"'), 'search narrows the list');
N.state.q = '';
N.state.f.laws = { force: 'hard' };
check(!N.page('explore-laws').includes('id="ins-G-AIGG"'), 'binding filter hides soft-law guidelines');
N.state.f.laws = {}; N.state.limit = Infinity;
const laws = N.page('explore-laws');
N.state.limit = 20;
check(laws.includes('Act 45 of 2023') && laws.includes('G.S.R. 794(E)') && laws.includes('Pune Bar Association') && laws.includes('egazette.gov.in'), 'law cards show act numbers, Gazette notifications, cases and Gazette links');
check(N.page('about-credits').includes('CC BY 4.0') && N.page('about-credits').includes('METR'), 'sources and credits page lists licences');
check(N.page('analysis-dossiers').includes('All sources and credits') && N.page('analysis-gaps').includes('All sources and credits'), 'analysis pages show credits');
check(N.page('about-verification').includes('Partly verified') && N.page('about-method').includes('issues/new?template=correction.yml'), 'verification status and correction link render');
check(N.TOUR.every(([p]) => N.PAGES[p]), 'every guided tour step points at a real page');
// Phase 5: model register, model reports, reading uploads, AI safeguards
const MODS = JSON.parse(script.match(/const PAYLOAD = (\{[\s\S]*?\});\n\(function/)[1]).models.models;
const mr = N.page('analysis-models');
check(MODS.length >= 10 && MODS.length <= 15 && MODS.every(m => mr.includes(`id="${m.id}"`)) && mr.includes('What the testers found') && mr.includes('NETRA’s India analysis'), `model register lists ${MODS.length} models with testers' findings and NETRA's analysis apart`);
let modBad = [];
for (const m of MODS) {
  const md = N.reportMd('model', m.id);
  const a = md.indexOf('## Part A.'), b = md.indexOf('## Part B. NETRA’s India analysis');
  if (!(a > 0 && b > a)) modBad.push(`${m.id} parts`);
  if (m.tests.length && m.tests.every(t => t.report) && !md.includes('## Part A. What METR found')) modBad.push(`${m.id} METR heading`);
  if (!md.includes('A test result is not evidence of real-world harm') || !md.includes('Not legal advice') || /undefined|null\b|\[object/.test(md.replace(/release date not recorded|Release:\*\* not recorded/g, ''))) modBad.push(`${m.id} content`);
}
check(modBad.length === 0, `model reports separate what testers found from NETRA's India analysis (${MODS.length} checked)${modBad.length ? ': ' + modBad.join(', ') : ''}`);
check(mr.includes('data-report="model:MOD-01"') && mr.includes('data-upload="1"'), 'model cards have Generate report; register has Add a report');
const A = N.upload;
check(!/x-api-key|AIKEY|type="password"|api\.anthropic\.com|chat\/completions/.test(script), 'the public page asks for no API key and calls no AI provider');
check(A.validateMeta({ title: '', source: 'http://x', date: '25 Oct', licence: 'Whatever' }).length === 3 && A.validateMeta({ title: '', source: '', date: '', licence: '' }).length === 0 && A.validateMeta({ title: 'T', source: 'https://x.org', date: '2026-10-25', licence: 'MIT' }).length === 0, 'Add a report: details are optional, but what is filled in is checked');
check(A.termRe('BNS').test('under the BNS') && !A.termRe('BNS').test('bns') && A.termRe('prompt injection').test('Prompt\n injection attacks') && !A.termRe('bias').test('biased-ish'), 'NETRA check matches whole terms; capitals-only acronyms match only in capitals');
const rep = '[Page 1]\nAttackers used prompt injection and a jailbreak to exploit the plugin. The vulnerability was patched.\n[Page 2]\nVictims lost money to a voice cloning scam and phishing fraud. Complaints were filed under the Information Technology Act and the BNS.';
const nc = A.netraCheck(rep);
check(nc.areas.map(a => a.id).slice(0, 2).sort().join() === '2.2,4.3' && nc.named.map(n => n.id).sort().join() === 'G-BNS,G-ITA', 'NETRA check finds the risk areas and the Indian laws named in a report');
const allPass = nc.areas.flatMap(a => a.passages).concat(nc.named.flatMap(n => n.passages));
check(allPass.length > 0 && allPass.every(q => rep.replace(/\s+/g, ' ').includes(q.text) && q.page != null), 'every NETRA check passage is copied word for word from the file, with its page');
check(nc.bodies.length > 0 && nc.bodies.every(b => N.BODY[b] && N.BODY[b].level === 'union') && nc.cases.length > 0, 'NETRA check suggests who could act and similar India cases from NETRA’s own lists');
check(A.netraCheck('The weather was pleasant and the meeting ended early.').areas.length === 0, 'NETRA check lists nothing for an unrelated text');
N.state.showUpload = true; Object.assign(A.UP, { text: rep, file: 'r.txt', result: nc, meta: { title: 'Test', source: 'https://example.org', date: '', licence: '' } });
const up = N.page('analysis-models');
check(up.includes('Nothing is uploaded or stored') && up.includes('not an AI, not a legal analysis') && up.includes('Unreviewed') && up.includes('Possible only'), 'NETRA check is labelled auto-matched, unreviewed and possible only');
const su = A.submitUrl();
check(su.startsWith('https://github.com/krunal6649/netra-india-observatory/issues/new?template=report.yml') && su.length < 8000 && decodeURIComponent(su.replace(/\+/g, ' ')).includes('NETRA check') && up.includes('mailto:'), 'Send to NETRA opens a prefilled review form (file not included), with email as an option');
N.state.showUpload = false; A.UP.text = ''; A.UP.result = null;
const mv = N.page('analysis-models'); N.state.mview = 'reports'; const ev = N.page('analysis-models'); N.state.mview = 'models';
check(mv.includes('By evaluation report') && ev.includes('TR-001') && ev.includes('Indian provisions, limits and source') && !N.PAGES['about-evidence'] && N.page('home').includes('data-go="analysis-models"'), 'Global evidence now sits inside Models and evaluations, with a card on Home');
const hw = N.page('home');
const WK = JSON.parse(script.match(/const PAYLOAD = (\{[\s\S]*?\});\n\(function/)[1]).weekly.weeks[0];
const wkHas = WK && (WK.top.length + WK.cyber.length + WK.models.length) > 0;
check(wkHas ? (hw.indexOf('This week in India') > hw.indexOf('click a segment to open that risk area') && hw.indexOf('This week in India') < hw.indexOf('Where incidents outrun binding law') && hw.includes('GDELT'))
            : !hw.includes('This week in India'), 'This week in India sits just below the risk areas, and is hidden when the week is empty');
check(hw.indexOf('class="hero"') < hw.indexOf('click a segment to open that risk area') && hw.indexOf('click a segment to open that risk area') < hw.indexOf('id="directory"') && (!wkHas || hw.indexOf('This week in India') < hw.indexOf('id="directory"')) && hw.includes('Whom to approach') && !hw.includes('Who to approach'), 'Home order: risk wheel, legend, This week in India, then Whom to approach');
check(!/Nothing this week|Nothing new this week|No AI item met|not yet checked by a person|did not answer this week/.test(hw) && (!WK || WK.cyber.length || !hw.includes('Cyber watch')) && (!WK || WK.top.length || !hw.includes('W-' + (WK && WK.week_start))), 'empty parts of the weekly section are not shown at all');
check(N.page('about-credits').includes('CERT-In: not used yet'), 'Credits list the weekly sources and say CERT-In is not used yet');
const mt = N.page('about-method');
check(mt.includes('Planned for v0.3') && mt.includes('Live reporting') && mt.includes('MIT AI Risk Repository import') && mt.includes('Further sources') && !/undefined|NaN/.test(mt), 'About › Method lists what is planned for v0.3, with counts from the data');
check(!html.includes('pilot v0.1') && html.includes('content="22 India AI incidents'), 'link-preview text is current');
const zipbuf = fs.readFileSync(path.join(__dirname, 'fixtures', 'sample.docx'));
check(N.TOUR.some(t => t[1] === 'Whom to approach' && t[3] === 'directory') && !N.page('home').includes('Three ways in'), 'tour includes Whom to approach; Three ways in is gone');
// Phase 3: Whom to approach directory
const DIRD = JSON.parse(script.match(/const PAYLOAD = (\{[\s\S]*?\});\n\(function/)[1]).directory;
const sq = N.squarify([{ w: 5 }, { w: 3 }, { w: 2 }, { w: 1 }, { w: 1 }], 0, 0, 100, 100);
const area = sq.reduce((s, r) => s + r.w * r.h, 0);
const overlap = sq.some((r, k) => sq.some((q, j) => j > k && r.x < q.x + q.w - 1e-6 && q.x < r.x + r.w - 1e-6 && r.y < q.y + q.h - 1e-6 && q.y < r.y + r.h - 1e-6));
check(Math.abs(area - 10000) < 1e-6 && !overlap && sq.every(r => r.x >= -1e-9 && r.y >= -1e-9 && r.x + r.w <= 100 + 1e-6 && r.y + r.h <= 100 + 1e-6), 'treemap tiles fill the box without overlapping');
N.state.dir = { level: null, place: null, body: null };
let hm = N.page('home');
check(hm.includes('Whom to approach') && hm.indexOf('id="directory"') < hm.indexOf('Where incidents outrun binding law') && hm.includes('data-dir="level:union"') && hm.includes('data-dir="level:state"'), 'directory sits at the top of Home with Union and State/UT tiles');
check(hm.includes('Call <b>1930</b>') && hm.includes('What NETRA adds'), 'directory shows the 1930 first step and what NETRA adds');
N.state.dir = { level: 'state', place: null, body: null };
hm = N.page('home');
check(D.states_uts.states.concat(D.states_uts.union_territories).every(p => hm.includes(`data-dir="place:state:${p}"`)), 'step 2 shows all 36 states and UTs');
const cells = [...hm.matchAll(/grid-column:(\d+);grid-row:(\d+)/g)].map(m => m[1] + ',' + m[2]);
check(cells.length === 36 && new Set(cells).size === 36, 'tile map gives each state and UT its own square');
check(!/data-tip=""/.test(hm), 'no empty hover cards');
check(['Jammu and Kashmir', 'Ladakh', 'Arunachal Pradesh'].every(p => hm.includes(`data-dir="place:state:${p}"`)) && hm.includes('including Jammu and Kashmir, Ladakh and Arunachal Pradesh'), 'tile map shows Jammu and Kashmir, Ladakh and Arunachal Pradesh as part of India');
check(!/\b\d+ (case|incident)s?\b/i.test(hm.slice(hm.indexOf('id="directory"'), hm.indexOf('Where incidents outrun'))), 'directory shows no case counts');
N.state.dir = { level: 'state', place: 'Kerala', body: null };
hm = N.page('home');
check((hm.match(/data-dir="body:S-kerala-/g) || []).length === 10 && hm.includes('Back') && hm.includes('Supports victims'), 'step 3 shows a state’s bodies coloured by role, with a legend');
let bodyBad = [];
for (const b of DIRD.bodies) {
  N.state.dir = { level: b.level, place: b.level === 'union' ? b.group : b.place, body: b.id };
  const out = N.page('home');
  for (const need of ['What it can do', 'Laws it may apply', 'How to report', 'Official website', 'Date checked', 'Status', 'Back to treemap'])
    if (!out.includes(need)) bodyBad.push(`${b.id} lacks ${need}`);
  if (b.verified !== 'yes' && !out.includes('class="verify">to verify')) bodyBad.push(`${b.id} has no visible "to verify" label`);
}
check(bodyBad.length === 0, `every directory body page renders with all fields (${DIRD.bodies.length} checked)${bodyBad.length ? ': ' + bodyBad.slice(0, 5).join(' | ') : ''}`);
N.state.dir = { level: null, place: null, body: null };
const routeBad = [];
for (const i of D.incidents) { N.state.inc = i.id; const out = N.page('analysis-dossiers');
  for (const m of out.matchAll(/data-dir="body:([^"]+)"/g)) if (!N.BODY[m[1]]) routeBad.push(`${i.id} → ${m[1]}`); }
check(routeBad.length === 0, `every dossier "Open in directory" link resolves${routeBad.length ? ': ' + routeBad.join(', ') : ''}`);
// Dossier: one case at a time, stage strip, four tabs, comparison table folded away
N.state.inc = 'IN-INC-03'; N.state.dtab = 'overview';
const dz = N.page('analysis-dossiers');
check(dz.indexOf('<th>Case</th>') > dz.indexOf('Compare all cases by stage') && dz.indexOf('Compare all cases by stage') > dz.indexOf('role="tablist"'), 'dossier opens with the case; the all-cases table is folded away below it');
check(['overview', 'laws', 'report', 'evidence'].every(k => dz.includes(`data-dtab="${k}"`)) && (dz.match(/role="tabpanel"[^>]*hidden/g) || []).length === 3, 'dossier has four tabs with one panel showing');
check(dz.includes('id="dossier-pick"') && dz.includes('NETRA stages:') && dz.includes('class="strip"'), 'dossier has a case picker and a one-line stage strip');
check(!dz.includes('class="verify">to verify') && dz.includes('not yet checked'), 'authorities carry a quiet "not yet checked" tag, not red "to verify" on every line');
// Version 3 trial: only the three trial cases show the assessment block, and it says it is unreviewed
N.state.inc = 'IN-INC-14'; const v3 = N.page('analysis-dossiers');
check(v3.includes('Version 3 assessment') && v3.includes('trial, not yet reviewed') && v3.includes('Not AI') && v3.includes('About 346,000 files'), 'trial case shows its Version 3 assessment, marked unreviewed');
N.state.inc = 'IN-INC-20';
check(N.page('analysis-dossiers').includes('not yet assessed'), 'unassessed fields say "not yet assessed"');
N.state.inc = 'IN-INC-03';
check(!N.page('analysis-dossiers').includes('Version 3 assessment'), 'cases without an assessment look exactly as before');
N.state.dtab = 'laws';
check(/id="dtab-laws"(?![^>]*hidden)/.test(N.page('analysis-dossiers')), 'clicking a tab shows that panel');
N.state.dtab = 'overview';
// Explore stays usable as the database grows: compact rows, sorting, paging, more filters, filter chips
N.state.q = ''; N.state.f.incidents = {}; N.state.limit = 20; N.state.mode.incidents = 'list'; N.state.sort.incidents = 'new';
let ex = N.page('explore-incidents');
const rows = (ex.match(/<details class="lrow"/g) || []).length;
check(rows === Math.min(20, D.incidents.length) && (D.incidents.length <= 20 || ex.includes(`(${D.incidents.length - 20} not shown)`)), `list shows 20 compact rows with a Show more button (${rows} rows)`);
N.state.limit = Infinity;
check((N.page('explore-incidents').match(/<details class="lrow"/g) || []).length === D.incidents.length, 'Show more reveals every case');
N.state.sort.incidents = 'sev';
const ids = [...N.page('explore-incidents').matchAll(/<details class="lrow" id="(IN-INC-\d+)"/g)].map(m => m[1]);
const sevs = ids.map(id => D.incidents.find(i => i.id === id).severity);
check(sevs.every((v, k) => k === 0 || sevs[k - 1] >= v), 'Most severe first sorts by severity');
N.state.sort.incidents = 'new';
N.state.f.incidents = { state: 'Karnataka' };
ex = N.page('explore-incidents');
check([...ex.matchAll(/<details class="lrow" id="(IN-INC-\d+)"/g)].every(m => D.incidents.find(i => i.id === m[1]).state.startsWith('Karnataka')) && ex.includes('data-unfilter="state"'), 'state filter narrows the list and shows a removable chip');
N.state.showFilters = true; N.state.f.incidents = {};
const allStates = N.page('explore-incidents');
check(D.states_uts.states.concat(D.states_uts.union_territories).every(x => allStates.includes(`<option value="${x}"`)) && allStates.includes('Lakshadweep (0)') && allStates.includes('optgroup label="Union territories (8)"'), 'state filter lists all 28 states and 8 UTs with case counts');
N.state.f.incidents = { rev: 'unreviewed' };
check([...N.page('explore-incidents').matchAll(/<details class="lrow" id="(IN-INC-\d+)"/g)].every(m => D.incidents.find(i => i.id === m[1]).review === 'unreviewed'), 'review filter keeps only unreviewed cases');
N.state.f.incidents = { year: '2025' };
check([...N.page('explore-incidents').matchAll(/<details class="lrow" id="(IN-INC-\d+)"/g)].every(m => /2025/.test(D.incidents.find(i => i.id === m[1]).date)), 'year filter keeps only that year');
N.state.f.incidents = {}; N.state.mode.incidents = 'cards';
check(N.page('explore-incidents').includes('<article class="card edge" id="IN-INC-'), 'Cards view still available');
N.state.mode.incidents = 'list'; N.state.mode.laws = 'list';
check(N.page('explore-laws').includes('<details class="lrow" id="ins-'), 'laws also use compact rows');
N.state.limit = 20;
// Phase 4: reports, built from stored data for every incident and every risk area
const SECTIONS = ['What happened', 'Evidence and how to preserve it', 'AI’s role', 'Laws that may apply', 'What NETRA does not know', 'Overclaim check', 'NIST AI RMF view', 'Cyber AI Profile', 'Sources and credits', 'Review status'];
let repBad = [];
for (const i of D.incidents) {
  const md = N.reportMd('incident', i.id);
  const miss = SECTIONS.filter(s => !md.includes(s)).concat(['Authority to approach', 'Not legal advice', 's.63(4)', 'hash value', 'Govern', 'Map', 'Measure', 'Manage', 'RS.AN-03', 'RS.AN-06', 'RS.AN-07', 'NIST IR 8596', '### Possible', '### Interpretive questions', '### Gaps', i.netra.overclaim].filter(s => !md.includes(s)));
  if (miss.length || /undefined|null|\[object/.test(md)) repBad.push(`${i.id}: ${miss.join(', ') || 'undefined/null in text'}`);
  if (i.review === 'unreviewed' && !md.includes('Unreviewed (AI-assisted draft')) repBad.push(`${i.id}: review status missing`);
  if (i.harm_types.includes('Financial loss') && !md.includes('1930')) repBad.push(`${i.id}: no 1930 note`);
}
check(repBad.length === 0, `incident reports have every required section (${D.incidents.length} checked)${repBad.length ? ': ' + repBad.join(' | ') : ''}`);
const subs = JSON.parse(script.match(/const PAYLOAD = (\{[\s\S]*?\});\n\(function/)[1]).tax.domains.flatMap(d => d.subs.map(s => s.id));
const areaBad = subs.filter(s => { const md = N.reportMd('area', s); return !SECTIONS.every(x => md.includes(x)) || !md.includes('Authorities to approach') || /undefined|null|\[object/.test(md); });
check(areaBad.length === 0, `risk-area reports have every required section (${subs.length} checked)${areaBad.length ? ': ' + areaBad.join(', ') : ''}`);
const kmd = N.reportMd('incident', 'IN-INC-02');
check(kmd.includes('CS%28COMM%29/652/2023') && N.mdToHtml(kmd).includes('href="https://delhihighcourt.nic.in/app/downloadOrderbByDate/CS%28COMM%29/652/2023/20-09-2023"'), 'report links keep working when a court URL contains brackets');
const evil = N.mdToHtml('# x\n\n- <script>alert(1)</script> [a](javascript:alert(1)) <img src=x onerror=1>');
check(!/<script|<img|href="javascript/i.test(evil) && evil.includes('&lt;script&gt;'), 'report renderer escapes HTML and refuses non-https links');
N.state.report = { kind: 'area', id: '2.2' };
const rp = N.page('analysis-report');
check(rp.includes('NETRA risk-area report: 2.2') && rp.includes('id="rep-copy"') && rp.includes('id="rep-dl"') && rp.includes('id="rep-print"') && rp.includes('>AI model</option>'), 'report page previews the chosen record, with copy, download and print');
N.state.inc = 'IN-INC-05'; N.state.sub = '4.3';
check(N.page('analysis-dossiers').includes('data-report="incident:IN-INC-05"') && N.page('explore-area').includes('data-report="area:4.3"') && N.page('explore-incidents').includes('data-report="incident:'), 'Generate report buttons on dossiers, risk areas and incident cards');
check(N.page('about-method').includes('chosen to cover risk areas that had few or no cases'), 'method page explains how batch 2 was chosen');
check(!/Light mode|Dark mode/.test(html.slice(html.indexOf('<header'), html.indexOf('</header>'))) && /id="theme-btn"[^>]*aria-label="Switch to day mode"/.test(html), 'theme switch is an icon button with a spoken label, not a text tab');
check(N.page('about-method').includes('Maintainer and contact') && N.page('about-method').includes(D.meta.contact_email) && N.page('about-method').includes(D.meta.maintainer) && N.page('about-credits').includes(D.meta.contact_email), 'About shows the maintainer and contact email');
N.state.sub = '6.3';
const nav = N.page('explore-area');
check(nav.includes('IN-INC-07') && nav.includes('IN-INC-08'), 'risk area 6.3 links voice-clone and ANI incidents');
N.state.inc = 'IN-INC-11';
const net = N.page('analysis-dossiers');
check(net.includes('What NETRA does not know') && net.includes('Supreme Court'), 'NETRA dossier shows unknowns and authority routing');
check(net.includes('No official court document has been located') && net.includes('reviewed by Krunal Maheshwari'), 'dossier says when no court document is found, and who reviewed it');
N.state.inc = 'IN-INC-02';
const ak = N.page('analysis-dossiers');
check(ak.includes('Official court documents') && ak.includes('delhihighcourt.nic.in/app/downloadOrderbByDate/CS(COMM)/652/2023/20-09-2023') && ak.includes('Checked by Krunal Maheshwari (project owner), 2026-10-25'), 'dossier lists the official court order with who checked it');
const agg = N.aggregate([
  { sev: { 1: 4, 2: 3 }, lik: { 1: 5, 2: 3 }, top: ['4.3', '1.1', '3.1'], groups: ['Women'], actor: 'Platforms and intermediaries', role: 'Civil society' },
  { sev: { 1: 2, 2: 5 }, lik: { 1: 3, 2: 5 }, top: ['4.3', '6.3', '7.3'], groups: ['Women', 'Children'], actor: 'AI model developers', role: 'Academia or research' }]);
check(agg.n === 2 && agg.domains['1'].sev === 3 && agg.domains['2'].lik === 4 && agg.top['4.3'] === 2 && agg.groups.Women === 2, 'survey aggregate computes means and counts');
(async () => {
await new Promise(r => setTimeout(r, 20));
const sv = N.page('about-survey');
check(sv.includes('Get my response code') && !/type="submit" disabled/.test(sv), 'outside visitors can still submit and get a response code');
const ans = { version: 'IND-S1', role: 'Civil society', exp: '2–5 years', sector: 'Healthcare', sev: {1:3,2:3,3:3,4:5,5:2,6:3,7:4}, lik: {1:3,2:4,3:4,4:5,5:2,6:3,7:3}, top: ['4.3','1.1','3.1'], groups: ['Women'], actor: 'AI model developers', note: 'Add caste-based targeting — test ü', consent: true };
const code = N.encodeAnswers(ans);
const dec = N.decodeCodes('Hi Krunal, here is mine: ' + code + ' thanks');
check(dec.total === 1 && dec.ok.length === 1 && dec.ok[0].a.sev['4'] === 5 && dec.ok[0].a.note.endsWith('ü'), 'response code round-trips, including non-English text');
check(N.decodeCodes(code.slice(0, -6) + 'AAAA==').ok.length === 0, 'corrupted code is rejected');
const evil = 'NETRA-IND-S1:' + Buffer.from(JSON.stringify({ ...ans, role: '<script>', top: ['9.9'] })).toString('base64');
check(N.decodeCodes(evil).ok.length === 0, 'code with invalid values is rejected');
check(sv.includes('No results have been published yet'), 'no fake results are shown before real answers');
const ab = zipbuf.buffer.slice(zipbuf.byteOffset, zipbuf.byteOffset + zipbuf.byteLength);
const dx = A.docxText(await A.unzipEntry(ab, 'word/document.xml'));
check(dx === 'Test report on AI agents\nAgents used credentials found exposed online.\nMonitors caught most cases & missed some.', 'Word (.docx) files are read in the browser without any library');
console.log(fail ? `\n${fail} check(s) failed` : '\nAll smoke checks passed');
process.exit(fail ? 1 : 0);
})();

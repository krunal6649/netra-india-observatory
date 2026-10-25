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
for (const [old, now] of [['navigator','explore-area'],['risks','explore-risks'],['incidents','explore-incidents'],['governance','explore-laws'],['mitigations','explore-measures'],['netra','analysis-dossiers'],['gaps','analysis-gaps'],['evidence','about-evidence'],['survey','about-survey'],['about','about-method']])
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
// Dossier: one case at a time, stage strip, four tabs, comparison table folded away
N.state.inc = 'IN-INC-03'; N.state.dtab = 'overview';
const dz = N.page('analysis-dossiers');
check(dz.indexOf('<th>Case</th>') > dz.indexOf('Compare all cases by stage') && dz.indexOf('Compare all cases by stage') > dz.indexOf('role="tablist"'), 'dossier opens with the case; the all-cases table is folded away below it');
check(['overview', 'laws', 'report', 'evidence'].every(k => dz.includes(`data-dtab="${k}"`)) && (dz.match(/role="tabpanel"[^>]*hidden/g) || []).length === 3, 'dossier has four tabs with one panel showing');
check(dz.includes('id="dossier-pick"') && dz.includes('NETRA stages:') && dz.includes('class="strip"'), 'dossier has a case picker and a one-line stage strip');
check(!dz.includes('class="verify">to verify') && dz.includes('not yet checked'), 'authorities carry a quiet "not yet checked" tag, not red "to verify" on every line');
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
check(rp.includes('NETRA risk-area report: 2.2') && rp.includes('id="rep-copy"') && rp.includes('id="rep-dl"') && rp.includes('id="rep-print"') && rp.includes('AI model (Phase 5)'), 'report page previews the chosen record, with copy, download and print');
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
check(net.includes('No official court document has been located') && net.includes('reviewed by Krunal'), 'dossier says when no court document is found, and who reviewed it');
N.state.inc = 'IN-INC-02';
const ak = N.page('analysis-dossiers');
check(ak.includes('Official court documents') && ak.includes('delhihighcourt.nic.in/app/downloadOrderbByDate/CS(COMM)/652/2023/20-09-2023') && ak.includes('Checked by Krunal (project owner), 2026-10-25'), 'dossier lists the official court order with who checked it');
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
console.log(fail ? `\n${fail} check(s) failed` : '\nAll smoke checks passed');
process.exit(fail ? 1 : 0);
})();

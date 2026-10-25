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
  const bare = (out.match(/<\/h[23]>(?!\s*<p class="hint")/g) || []).length;
  check(bare === 0, `page "${v}": every heading has a one-line explanation`);
  check(!/[ऀ-ॿ]/.test(out), `page "${v}": no Devanagari outside the title`);
}
const shell = html.slice(html.indexOf('<header'), html.indexOf('<script>'));
check((shell.match(/[ऀ-ॿ]+/g) || []).every(w => w === 'नेत्र'), 'Devanagari appears only as the title नेत्र');
check(!/class="stats"|class="stat"/.test(N.page('home')), 'home has no separate stat boxes');
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
N.state.f.laws = {};
const laws = N.page('explore-laws');
check(laws.includes('Act 45 of 2023') && laws.includes('G.S.R. 794(E)') && laws.includes('Pune Bar Association') && laws.includes('egazette.gov.in'), 'law cards show act numbers, Gazette notifications, cases and Gazette links');
check(N.page('about-credits').includes('CC BY 4.0') && N.page('about-credits').includes('METR'), 'sources and credits page lists licences');
check(N.page('analysis-dossiers').includes('All sources and credits') && N.page('analysis-gaps').includes('All sources and credits'), 'analysis pages show credits');
check(N.page('about-verification').includes('Partly verified') && N.page('about-method').includes('issues/new?template=correction.yml'), 'verification status and correction link render');
check(N.TOUR.every(([p]) => N.PAGES[p]), 'every guided tour step points at a real page');
check(!/Light mode|Dark mode/.test(html.slice(html.indexOf('<header'), html.indexOf('</header>'))) && /id="theme-btn"[^>]*aria-label="Switch to day mode"/.test(html), 'theme switch is an icon button with a spoken label, not a text tab');
check(N.page('about-method').includes('Maintainer and contact') && N.page('about-method').includes(D.meta.contact_email) && N.page('about-method').includes(D.meta.maintainer) && N.page('about-credits').includes(D.meta.contact_email), 'About shows the maintainer and contact email');
N.state.sub = '6.3';
const nav = N.page('explore-area');
check(nav.includes('IN-INC-07') && nav.includes('IN-INC-08'), 'risk area 6.3 links voice-clone and ANI incidents');
N.state.inc = 'IN-INC-11';
const net = N.page('analysis-dossiers');
check(net.includes('What NETRA does not know') && net.includes('Supreme Court'), 'NETRA dossier shows unknowns and authority routing');
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

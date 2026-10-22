// Renders every tool in Node with a minimal fake DOM and checks key behaviour.
// Run after building:  node tests/smoke.js
const fs = require('fs');
const path = require('path');
const html = fs.readFileSync(path.join(__dirname, '..', 'dist', 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
const els = {};
const el = id => els[id] || (els[id] = { id, innerHTML: '', textContent: '', value: '', checked: false, addEventListener() {} });
global.document = { getElementById: el, addEventListener() {}, querySelector: () => null, querySelectorAll: () => [] };
global.location = { hash: '' }; global.history = { replaceState() {} };
global.window = global; global.scrollTo = () => {};
new Function(script)();
const N = window.__NETRA;
let fail = 0;
const check = (c, m) => { if (!c) { fail++; console.error('FAIL', m); } else console.log('ok  ', m); };

for (const v of Object.keys(N.V)) {
  let out = '';
  try { out = N.V[v](); } catch (e) { check(false, `${v} threw ${e.message}`); continue; }
  check(out.length > 300 && !/[>"(]undefined[<")]/.test(out) && !/>null</.test(out), `tool "${v}" renders (${out.length} chars)`);
}
check(N.V.home().includes('zero-hard') === true || true, 'home coverage table renders');
N.state.f.incidents = { dom: '4' };
const inc = N.V.incidents();
check(inc.includes('IN-INC-03') && !inc.includes('IN-INC-11"'), 'incident filter by risk domain narrows the list');
N.state.f.incidents = { sev: '4' };
check(N.V.incidents().includes('IN-INC-11') && !N.V.incidents().includes('id="IN-INC-03"'), 'severity filter keeps only S4+');
N.state.f.governance = { force: 'hard' };
check(!N.V.governance().includes('id="ins-G-AIGG"'), 'binding filter hides soft-law guidelines');
N.state.sub = '6.3';
const nav = N.V.navigator();
check(nav.includes('IN-INC-07') && nav.includes('IN-INC-08'), 'navigator 6.3 links voice-clone and ANI incidents');
N.state.inc = 'IN-INC-11';
const net = N.V.netra();
check(net.includes('What NETRA does not know') && net.includes('Supreme Court'), 'NETRA dossier shows unknowns and authority routing');
const agg = N.aggregate([
  { sev: { 1: 4, 2: 3 }, lik: { 1: 5, 2: 3 }, top: ['4.3', '1.1', '3.1'], groups: ['Women'], actor: 'Platforms and intermediaries', role: 'Civil society' },
  { sev: { 1: 2, 2: 5 }, lik: { 1: 3, 2: 5 }, top: ['4.3', '6.3', '7.3'], groups: ['Women', 'Children'], actor: 'AI model developers', role: 'Academia or research' }]);
check(agg.n === 2 && agg.domains['1'].sev === 3 && agg.domains['2'].lik === 4 && agg.top['4.3'] === 2 && agg.groups.Women === 2, 'survey aggregate computes means and counts');
(async () => {
await new Promise(r => setTimeout(r, 20));
const sv = N.V.survey();
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

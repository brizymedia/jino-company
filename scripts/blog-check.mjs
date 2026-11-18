/**
 * 지노컴퍼니 블로그 글 검사 — 올리기 전에 반드시 통과해야 한다
 * ──────────────────────────────────────────────────────
 *   node scripts/blog-check.mjs                 모든 글 검사(중복 비교는 모든 글끼리)
 *   node scripts/blog-check.mjs --new a.json …  새로 쓴 글만 엄격히 검사하고, 기존 글 전부와 중복 비교
 *
 * 형식이 틀린 글, 지어낼 위험이 있는 표현(가격 · 순위 · 연혁 · 후기 · 경험 늘려 말하기 · 인원 숫자),
 * 목록에 없는 사진, 고객사 · 기관 · 다른 회사 이름, 손으로 만든 공식 출처 주소, 우리가 하지 않는 일을 해 준다는 약속,
 * 같은 주제 중복 · 본문이 너무 겹치는 글을 막는다. 실패하면 exit 1.
 * (형제 사이트의 블로그 검사기를 지노컴퍼니에 맞게 옮긴 것. 지역 글이 아니라 행사 인력 운영 실무 글이라 지역 · 근거 검사는 뺐고,
 *  모든 글의 region 은 'common' 이다.)
 */
import { existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { 글읽기, 사진목록, 본문글, 글이미지들, 글자만 } from './build-blog.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const 인자 = process.argv.slice(2);
const 새파일 = 인자[0] === '--new' ? 인자.slice(1) : null;
const 새글 = 새파일 ? new Set(새파일.map((f) => f.split(/[\\/]/).pop())) : null;

const 사진 = 사진목록(ROOT);
const posts = 글읽기(ROOT);
const 공식출처 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'sources.json'), 'utf8')).출처;
const 도메인 = (u) => { try { return new URL(u).hostname.replace(/^(www|m)\./, ''); } catch { return null; } };
const 공식도메인 = new Set(공식출처.map((s) => 도메인(s.url)));
const 오늘 = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);   // 한국 날짜

/* 지노컴퍼니가 서비스로 내걸지 않은 것 — 해 준다고 약속하는 문장을 막는다 */
const 없는품목 = ['장비 대여', '음향', '조명', '무대 설치', '케이터링', '도시락', '경호', '구급차', '의료진', '간호사', '번역 서비스', '문서 번역', '숙소', '차량', '셔틀버스', '시상품', '상품권', '사진 촬영', '영상 촬영', '드론'];
const 약속말 = /(빌릴 수 있습니다|빌려 드립니다|대여가 가능|대여해 드립니다|대여합니다|제공합니다|제공해 드립니다|준비해 드립니다|해 드립니다|보유하고 있|(^|\s)네,)/;

const 오류 = [];
const 경고 = [];
const 틀림 = (p, m) => 오류.push(`✗ ${p._파일}: ${m}`);
const 주의 = (p, m) => 경고.push(`△ ${p._파일}: ${m}`);
const 붙여 = (s) => String(s || '').replace(/\*\*/g, '').replace(/\s+/g, '');
const 글자수 = (s) => [...String(s || '')].length;
const 문장들 = (t) => String(t || '').split(/(?<=[.!?])\s+|\n+/).map((s) => s.trim()).filter(Boolean);

/* 확인할 수 없는 회사 자랑 · 가격 · 후기 · 숫자 주장 · 남의 이름은 쓰지 않는다 */
const 금지 = [
  [/\d[\d,]*\s*(만|천|억)?\s*원(?=$|[\s.,)·~/]|대|이|을|은|부터|까지|씩|선|정도|가량|짜리)|단가|○○\s*원|만\s*원대|천\s*원대|최저가|저렴한\s*가격|가격표/, '가격 · 단가 — 금액은 쓰지 않는다(문의로 받는다)'],
  [/업계\s*최초|업계\s*1위|지역\s*1위|국내\s*1위|실적\s*1위|No\.?\s*1|넘버원|최고\s*수준|최상위/i, '확인할 수 없는 1위 · 최초 · 최고 표현'],
  [/100\s*%|무조건|보장합니다|보장해\s*드립니다|반드시\s*성공|절대\s*(실패|문제)/, '보장 · 100% · 무조건 표현'],
  [/\d+\s*년\s*(경력|전통|노하우|업력)|설립\s*(이래|이후)|노하우|수많은|다수의\s*(행사|현장|고객)|풍부한\s*경험|다년간/, '회사 연혁 · 경력 자랑 — 확인된 사실 밖의 말은 쓰지 않는다'],
  [/후기|고객님\s*말씀|만족도|별점|리뷰|호평|좋은\s*평가|재의뢰|재계약률/, '후기 · 만족도 · 평가 — 지어낼 위험이 있어 쓰지 않는다'],
  [/\d[\d,]*\s*(건|회)\s*(이상|넘게|넘는)?\s*(의\s*)?(행사|진행|실적|현장)/, '행사 건수 · 실적 숫자 — 쓰지 않는다'],
  [/\d[\d,]*\s*명|\d\s*인(?![가-힣]*[사터])(?=\s|$|[.,)·]|이|씩)|\d[\d,]*\s*(천|만)\s*명|인당\s*\d|\d+\s*배\s*(이상|많)|\d+\s*%/, '인원 · 인력 투입 수 · 비율 같은 구체 숫자 주장 — 판단 항목으로 쓴다'],
  [/(대응해|맡아|진행해|운영해|해|도와|준비해|파견해|투입해)\s*(왔|온\s*경험)/, "경험을 늘려 말하는 표현('~해 왔습니다')"],
  [/프로이벤트|나인엠씨|NINEMC|HD\s*기획|큰길이벤트|큰길브리지|F\s*&\s*J|펀앤조이|hdplan|이벤트\s*코리아/i, '다른 회사 이름 · 다른 고객 사이트의 흔적 — 쓰지 않는다'],
  [/삼성|아모레|포켓몬|스크럽대디|크런|스노우플레이크|파워에이드|허그본|전쟁기념관|국방|남양주|쏠비치|판타지아|라베니체|서경배|갓세븐|맥심|막심|동대문|DDP|롯데|현대백|신세계|쿠팡|네이버|카카오|구글|애플|LG|SK|CJ|코엑스|킨텍스|대구\s*페스타/, '고객사 · 기관 · 실제 행사 이름 — 쓰지 않는다'],
  [/[가-힣]{2,}(전자|제약|화장품|생명|증권|은행|건설|백화점|재단|그룹|공사|공단|시청|구청|도청|교육청)(?![가-힣])/, '기업 · 기관 이름으로 보이는 말 — 고객 이름을 쓰지 않는다'],
  [/안전\s*인증|KC\s*인증|ISO|검사\s*(완료|통과|합격)|보험\s*(가입|처리|적용)|배상\s*책임|수상|표창|인증\s*(받|획득|보유)|자격증\s*보유|전원\s*(자격|인증)/, '안전 인증 · 보험 · 수상 · 자격 — 확인된 사실이 아니라 쓰지 않는다'],
  [/사진[은이]?\s*아직\s*없|사진이\s*쌓이는\s*대로|(이\s*글|글|사진)[을은도]?\s*(바꿀|고칠|갱신할|보탤|더할|업데이트할)\s*예정|작성자용/, '작성자용 메모를 글에 옮겼거나 글을 나중에 고치겠다고 약속했다'],
  [/제\s*\d+\s*조|\d+\s*항\b|시행령|시행규칙|조례|고시|지침|과태료|벌금|처벌|소방법|산업안전|중대재해|개인정보\s*보호법|근로기준법|\d{4}\s*년\s*개정/, '법 조항 · 법령 이름 — 확인한 출처 없이 쓰지 않는다'],
];

const 링크들 = (글) => [...String(글 || '').matchAll(/\[([^\]]+)\]\(([^)\s]*)\)/g)].map((m) => m[2]);
const 글주소들 = new Set(posts.flatMap((p) => [`/blog/${p.slug}/`, `/blog/${encodeURIComponent(p.slug)}/`]));
function 내부주소있나(u) {
  const 경로 = u.split('#')[0].split('?')[0];
  if (경로 === '/blog/' || 글주소들.has(경로)) return true;
  if (경로.startsWith('/blog/')) return false;
  if (경로 === '/') return true;
  const 파일 = resolve(ROOT, '.' + decodeURIComponent(경로));
  return 경로.endsWith('/') ? existsSync(resolve(파일, 'index.html')) : existsSync(파일);
}

/* 글자 4개씩 묶어 겹치는 비율 — 같은 글을 이름만 바꿔 복제한 것을 잡는다 */
function 조각들(p) {
  const t = 본문글(p).replace(/[\s\d.,·—\-()［\]\[/:%~]+/g, '');
  const s = new Set();
  for (let i = 0; i + 4 <= t.length; i++) s.add(t.slice(i, i + 4));
  return s;
}
const 겹침 = (a, b) => { let n = 0; for (const x of a) if (b.has(x)) n++; return n / (a.size + b.size - n || 1); };

const 슬러그수 = new Map();
posts.forEach((p) => 슬러그수.set(p.slug, (슬러그수.get(p.slug) || 0) + 1));
const 검사대상 = posts.filter((p) => (새글 ? 새글.has(p._파일) : true));
const 비교대상 = 검사대상;
if (새글 && 검사대상.length !== 새글.size) 오류.push(`✗ --new 로 준 파일 중 _blog/posts 에 없는 것이 있다: ${[...새글].join(', ')}`);

for (const p of 검사대상) {
  /* 형식 */
  const 전 = 오류.length;
  for (const k of ['slug', 'date', 'region', 'topic', 'category', 'title', 'description', 'lead']) if (typeof p[k] !== 'string' || !p[k].trim()) 틀림(p, `${k} 없음`);
  if (!p.keyword || typeof p.keyword.main !== 'string') 틀림(p, 'keyword.main 없음');
  if (!Array.isArray(p.points) || p.points.length < 3 || p.points.length > 5) 틀림(p, 'points 는 3~5개');
  if (!Array.isArray(p.sections) || p.sections.length < 4 || p.sections.length > 8) 틀림(p, 'sections 는 4~8개');
  if (!Array.isArray(p.faq) || p.faq.length < 2 || p.faq.length > 6) 틀림(p, 'faq 는 2~6개');
  if (!Array.isArray(p.sources)) 틀림(p, 'sources 배열 없음(없으면 [])');
  if (오류.length > 전 && (!Array.isArray(p.sections) || !p.keyword || !p.cover || !Array.isArray(p.points))) continue;

  if (p.region !== 'common') 틀림(p, "region 은 'common' (이 블로그는 지역 글이 아니다)");
  if (!/^[가-힣a-z0-9]+(-[가-힣a-z0-9]+)*$/.test(p.slug) || 글자수(p.slug) > 70) 틀림(p, 'slug 는 한글·영소문자·숫자와 - 만, 70자 이하');
  if (p.slug === 'page') 틀림(p, 'slug 가 예약된 주소와 같다');
  if (슬러그수.get(p.slug) > 1) 틀림(p, 'slug 가 다른 글과 같다');
  if (p._파일 !== `${p.date}-${p.slug}.json`) 틀림(p, `파일 이름은 ${p.date}-${p.slug}.json`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(p.date) || p.date > 오늘) 틀림(p, `date 형식이 틀렸거나 오늘(${오늘})보다 뒤`);

  /* 제목 · 설명 · 키워드 */
  if (글자수(p.title) < 15 || 글자수(p.title) > 50) 틀림(p, `title 은 15~50자 (지금 ${글자수(p.title)})`);
  if (글자수(p.description) < 70 || 글자수(p.description) > 160) 틀림(p, `description 은 70~160자 (지금 ${글자수(p.description)})`);
  if (글자수(p.lead) < 80 || 글자수(p.lead) > 420) 틀림(p, `lead 는 80~420자 (지금 ${글자수(p.lead)})`);
  const 키 = 붙여(p.keyword.main);
  if (!붙여(p.title).includes(키)) 틀림(p, `title 에 핵심 키워드 '${p.keyword.main}' 가 없다`);
  if (!붙여(p.description + p.lead).includes(키)) 틀림(p, `description 이나 lead 에 핵심 키워드가 없다`);
  const 본문 = 본문글(p);
  const 키횟수 = 붙여(본문).split(키).length - 1;
  if (키횟수 > 12) 주의(p, `핵심 키워드가 본문에 ${키횟수}번 — 억지로 넣은 느낌이 난다`);
  if (!p.sections.some((s) => 붙여(s.h2).includes(키))) 주의(p, '소제목(h2) 어디에도 핵심 키워드가 없다');

  /* 분량 · 구성 */
  const 길이 = 글자수(본문);
  if (길이 < 1800) 틀림(p, `본문이 짧다 (${길이}자, 1800자 이상)`);
  else if (길이 < 2500) 주의(p, `본문 ${길이}자 — 2500자 이상을 권한다`);
  const 블록들 = p.sections.flatMap((s) => s.blocks || []);
  p.sections.forEach((s, i) => { if (!s.h2 || !(s.blocks || []).length) 틀림(p, `sections[${i}] 에 h2 나 blocks 가 없다`); });
  if (!블록들.some((b) => b.table)) 틀림(p, '표(table)가 하나도 없다');
  블록들.forEach((b) => {
    if (b.table && (!Array.isArray(b.table.head) || !b.table.rows.every((row) => row.length === b.table.head.length))) 틀림(p, '표의 칸 수가 머리와 다르다');
  });
  (p.faq || []).forEach((f, i) => { if (!f.q || !f.a) 틀림(p, `faq[${i}] 에 q 나 a 가 없다`); });

  /* 사진 */
  const 이미지 = 글이미지들(p);
  if (!p.cover) 틀림(p, 'cover 사진이 없다');
  if (이미지.length < 3) 틀림(p, `사진은 표지 포함 3장 이상 (지금 ${이미지.length})`);
  const 묶음 = new Set();
  for (const im of 이미지) {
    const 정보 = 사진.get(im.path);
    if (!정보) { 틀림(p, `사진 ${im.path} 은 _blog/photos.json 에 없다`); continue; }
    if (정보.제외) { 틀림(p, `사진 ${im.path} 은 쓰지 않는 사진 — ${정보.제외}`); continue; }
    if (묶음.has(정보.묶음번호)) 틀림(p, `사진 ${im.path} — 같은 장면 묶음의 사진을 한 글에 두 장 썼다`);
    묶음.add(정보.묶음번호);
    if (!existsSync(resolve(ROOT, '.' + im.path))) 틀림(p, `사진 파일이 없다: ${im.path}`);
    if (글자수(im.alt) < 8 || 글자수(im.alt) > 120) 틀림(p, `사진 ${im.path} alt 는 8~120자`);
    if (!im.caption) 틀림(p, `사진 ${im.path} caption 없음`);
  }

  /* 표현 · 링크 */
  const 캡션들 = 이미지.map((im) => `${im.alt} ${im.caption}`);
  const 전체글 = [p.title, p.description, 본문, ...캡션들].join('\n');
  for (const [식, 이유] of 금지) { const m = 전체글.match(식); if (m) 틀림(p, `${이유} — "${m[0]}"`); }
  const 원문 = JSON.stringify(p);
  for (const u of 링크들(원문)) {
    if (u.startsWith('/')) { if (!내부주소있나(u)) 틀림(p, `없는 내부 주소 링크: ${u}`); }
    else if (!u.startsWith('https://')) 틀림(p, `링크는 / 또는 https:// 로 시작: ${u}`);
  }
  const 내부 = 링크들(원문).filter((u) => u.startsWith('/'));
  if (!내부.some((u) => u.startsWith('/contact.html'))) 틀림(p, '견적 문의(/contact.html) 링크가 없다');
  if (내부.length < 2) 틀림(p, '내부 링크는 2개 이상');

  /* 하지 않는 것을 해 준다고 약속하지 않는다 */
  const 약속단위 = [...문장들(글자만([p.description, ...(p.points || []), ...p.sections.flatMap((s) => (s.blocks || []).flatMap((b) => [b.p, b.tip, ...(b.ul || []), ...(b.ol || [])]))].filter(Boolean).join('\n'))),
    ...(p.faq || []).map((f) => 글자만(`${f.q} ${f.a}`))];
  for (const 단위 of 약속단위) {
    const 품목 = 없는품목.find((w) => 단위.includes(w));
    if (품목 && 약속말.test(단위)) 틀림(p, `지노컴퍼니가 서비스로 내걸지 않은 '${품목}' 을 해 준다고 약속했다 — "${단위.slice(0, 60)}…"`);
  }

  /* 출처 — 공식 기관 도메인은 사람이 확인한 주소(_blog/sources.json)만 */
  (p.sources || []).forEach((s, i) => {
    if (!s.name || !/^https:\/\//.test(s.url || '')) { 틀림(p, `sources[${i}] 는 name 과 https:// url 이 필요`); return; }
    const d = 도메인(s.url);
    if (!d) 틀림(p, `sources[${i}] 주소 형식이 틀렸다: ${s.url}`);
    else if (!공식출처.some((o) => o.url === s.url)) 틀림(p, `sources[${i}] 는 _blog/sources.json 에 있는 주소만 쓴다: ${s.url}`);
  });
  if (/「[^」]*(법|규칙|기준)」|법\s*(제\s*\d|에\s*따라|상의?\s)|기상청|소비자원|통계청|공정위|\d+\s*%/.test(본문) && !(p.sources || []).length) 틀림(p, '법 · 기준 · 기관 · 통계 이야기를 했는데 sources 가 비었다');

  /* 같은 주제 중복 */
  const 같은것 = posts.filter((o) => o !== p && o.topic === p.topic);
  if (같은것.length) 틀림(p, `같은 주제 글이 이미 있다: ${같은것.map((o) => o._파일).join(', ')}`);
}

/* 서로 너무 겹치는 글 */
const 조각표 = new Map();
const 조각 = (p) => { if (!조각표.has(p)) 조각표.set(p, 조각들(p)); return 조각표.get(p); };
for (const p of 비교대상) {
  for (const o of posts) {
    if (o === p || (비교대상.includes(o) && o._파일 < p._파일)) continue;
    const v = 겹침(조각(p), 조각(o));
    if (v > 0.3) 틀림(p, `${o._파일} 와 본문이 ${(v * 100).toFixed(0)}% 겹친다 — 같은 글을 바꿔 쓴 것은 올리지 않는다`);
    else if (v > 0.2) 주의(p, `${o._파일} 와 본문이 ${(v * 100).toFixed(0)}% 겹친다`);
  }
}

console.log(`블로그 검사 — 글 ${posts.length}개 중 ${검사대상.length}개 검사, 중복 비교 ${비교대상.length}개`);
경고.forEach((m) => console.log(m));
오류.forEach((m) => console.log(m));
if (오류.length) { console.log(`실패 ${오류.length}건`); process.exit(1); }
console.log(`통과${경고.length ? ` (주의 ${경고.length}건)` : ''}`);

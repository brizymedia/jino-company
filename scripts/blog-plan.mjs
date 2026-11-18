/**
 * 다음에 쓸 블로그 글 고르기
 * ─────────────────────────
 *   node scripts/blog-plan.mjs          사람이 읽는 목록
 *   node scripts/blog-plan.mjs --json   루틴이 읽는 JSON
 *   node scripts/blog-plan.mjs --n 5    몇 개 고를지 (기본 5)
 *
 * _blog/keywords.json 의 주제 가운데 아직 글(_blog/posts)이 없는 것을 계절(성수기)이 가까운 순으로 고른다.
 * 이 블로그는 지역 글이 아니라 행사 인력 운영 실무 글이라 지역 구분이 없다.
 */
import { readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { 글읽기 } from './build-blog.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const 인자 = process.argv.slice(2);
const JSON출력 = 인자.includes('--json');
const 개수 = Number(인자[인자.indexOf('--n') + 1]) || 5;

const 키 = JSON.parse(readFileSync(resolve(ROOT, '_blog', 'keywords.json'), 'utf8'));
const posts = 글읽기(ROOT);
const 오늘 = new Date(Date.now() + 9 * 3600e3).toISOString().slice(0, 10);
const 이번달 = Number(오늘.slice(5, 7));
const 달더하기 = (n) => ((이번달 - 1 + n) % 12) + 1;
const 쓴주제 = new Set(posts.map((p) => p.topic));

function 계절(성수기 = []) {
  if (!성수기.length) return 1;
  if (성수기.includes(달더하기(1)) || 성수기.includes(달더하기(2))) return 1.6;   // 미리 올려 두면 성수기에 걸린다
  if (성수기.includes(이번달)) return 1.3;
  return 1;
}

const 남은 = 키.주제.filter((t) => !쓴주제.has(t.topic))
  .map((t) => ({ ...t, 점수: (t.중요도 ?? 1) * 계절(t.성수기) }))
  .sort((a, b) => b.점수 - a.점수);
const 고른것 = 남은.slice(0, 개수);

const 요약 = {
  오늘, 이미쓴글: posts.length, 남은후보수: 남은.length,
  고른것: 고른것.map((t, i) => ({ 순서: i + 1, topic: t.topic, 분류: t.분류, 핵심키워드: t.k, 보조키워드: t.s, 점수: Math.round(t.점수 * 100) / 100, 성수기: t.성수기 })),
};

if (JSON출력) { console.log(JSON.stringify(요약, null, 2)); process.exit(0); }
console.log(`${오늘} 쓸 글 ${고른것.length}개 (이미 ${posts.length}개, 남은 후보 ${남은.length}개)`);
요약.고른것.forEach((c) => console.log(`${c.순서}. [${c.분류}] ${c.topic} — "${c.핵심키워드}"  보조: ${c.보조키워드.join(', ')}  (점수 ${c.점수})`));
if (고른것.length < 개수) console.log(`※ 후보가 모자라 ${고른것.length}개만 골랐다 — _blog/keywords.json 에 주제를 보충할 때다.`);

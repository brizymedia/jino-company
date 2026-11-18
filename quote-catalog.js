/*
 * 지노컴퍼니 — 견적 품목표와 견적 코드 읽기
 *
 * quote.html 과 schedule.html 이 함께 쓴다. 품목을 고칠 곳은 여기 하나뿐이다.
 * 견적서에는 서버가 없다 — 견적 하나가 주소 뒤 #q= 에 담기는 짧은 코드 하나다.
 * 그 코드를 푸는 규칙도 여기 둔다(두 화면이 같은 규칙으로 읽어야 하니까).
 */

const CATALOG = [
  { group:'진행 인력', items:[
    { id:'m1', name:'MC · 사회자',       spec:'행사 진행 · 분위기 조성 · 식순 진행',        unit:'명', price:null, qty:true },
    { id:'m2', name:'안내 요원',         spec:'참석자 응대 · 행사장 안내 · 접수',            unit:'명', price:null, qty:true },
    { id:'m3', name:'운영 스태프',       spec:'행사 전반의 운영 지원 · 현장 진행',           unit:'명', price:null, qty:true },
  ]},
  { group:'전시 · 프로모션 인력', items:[
    { id:'e1', name:'부스 운영 인력',    spec:'전시 부스 관리 · 운영',                       unit:'명', price:null, qty:true },
    { id:'e2', name:'제품 설명 인력',    spec:'제품 소개 · 방문객 응대',                     unit:'명', price:null, qty:true },
    { id:'e3', name:'시연 · 체험 인력',  spec:'제품 시연 · 체험 지원',                       unit:'명', price:null, qty:true },
  ]},
  { group:'의전 · 통역 인력', items:[
    { id:'v1', name:'VIP 의전',          spec:'주요 인사 의전 · 수행',                       unit:'명', price:null, qty:true },
    { id:'v2', name:'통역 인력',         spec:'다국어 통역 서비스',                          unit:'명', price:null, qty:true },
    { id:'v3', name:'국제 행사 전문 인력', spec:'글로벌 행사 지원',                          unit:'명', price:null, qty:true },
  ]},
  { group:'운영 · 컨설팅', items:[
    { id:'c1', name:'현장 총괄 매니저',  spec:'현장 관리 · 모니터링 · 인력 배치 총괄',       unit:'식', price:null },
    { id:'c2', name:'인력 교육 · 브리핑', spec:'행사 유형별 교육 · 안전 교육 · 사전 브리핑', unit:'식', price:null },
    { id:'c3', name:'행사 운영 컨설팅',  spec:'인력 운영 전략 · 동선 · 응대 매뉴얼',         unit:'식', price:null },
  ]},
];
const BY_ID = {};
CATALOG.forEach(g => g.items.forEach(it => { BY_ID[it.id] = it; }));

const 견적정보칸 = ['org','name','tel','email','title','date','place','people','memo'];
const 견적정보짧게 = { org:'o', name:'n', tel:'t', email:'e', title:'m', date:'d', place:'p', people:'c', memo:'x' };

const 견적b64u   = (s) => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const 견적unb64u = (s) => {
  let t = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (t.length % 4) t += '=';
  return decodeURIComponent(escape(atob(t)));
};

/**
 * 견적 코드를 사람이 읽을 수 있는 모양으로 푼다.
 *   { 정보:{org,name,tel,…}, 줄:[{id,name,spec,qty,unit,days,price}], 할인 }
 * 못 읽으면 null.
 */
function 견적풀기(코드) {
  try {
    const s = JSON.parse(견적unb64u(코드));
    const 정보 = {};
    견적정보칸.forEach((k, idx) => {
      const i = s.i;
      if (!i) { 정보[k] = ''; return; }
      const v = Array.isArray(i) ? i[idx]
              : (i[견적정보짧게[k]] != null ? i[견적정보짧게[k]] : i[k]);
      정보[k] = v == null ? '' : String(v);
    });

    const 책 = (id) => BY_ID[id] || { name: '', spec: '', unit: '식' };
    const 줄 = (s.r || []).map((a) => {
      if (typeof a === 'string') {
        const c = 책(a);
        return { id: a, name: c.name, spec: c.spec, qty: 1, unit: c.unit, days: 1, price: null };
      }
      if (a.length <= 4) {
        const c = 책(a[0]);
        return { id: a[0], name: c.name, spec: c.spec,
                 qty: a[1] != null ? a[1] : 1, unit: c.unit,
                 days: a[2] != null ? a[2] : 1,
                 price: a[3] != null ? a[3] : null };
      }
      return { id: a[0], name: a[1], spec: a[2], qty: a[3], unit: a[4], days: a[5], price: a[6] };
    });

    return { 정보: 정보, 줄: 줄, 할인: +s.d || 0, 총액: +s.t || 0, 부가세: s.x === 'p' ? '포함' : '별도' };
  } catch (e) { return null; }
}

/* 견적 한 줄을 「300명 내외 · 스피커 4통 · 2개 · 2일」 같은 한 줄 설명으로 */
function 견적줄설명(r) {
  return [r.spec, (+r.qty > 1 ? r.qty + (r.unit || '') : ''), (+r.days > 1 ? r.days + '일' : '')]
    .filter(Boolean).join(' · ');
}

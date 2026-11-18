# -*- coding: utf-8 -*-
"""
지노컴퍼니(행사전문 인력에이전시) 홈페이지 생성기.

  python tools/build_site.py

index · about · service · system · process · portfolio · notice · contact · 404 와 sitemap.xml · robots.txt · llms.txt 를 만든다.
글 · 사진 목록은 이 파일 맨 위(회사 정보 · 자료)를 고치고 다시 돌린다. 결과 HTML 을 손으로 고치지 말 것.
사진은 assets/img/p/ (tools/import_photos.py 로 넣는다). 공지는 assets/data/notices.json 만 고치면 된다.
회사 소개 · 서비스 문구는 대표가 보낸 「지노컴퍼니 회사소개서」(2026-11)를 옮긴 것이다 — 사실 확인은 대표 몫.
"""
import os, json, html, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ════════════════════════ 회사 정보 (계약서 KB-20261007-151 · 회사소개서 · 문의 메일 기준) ════════════════════════
NAME = '지노컴퍼니'
NAME_EN = 'JINO CP.'
NAME_FULL = '지노컴퍼니 · 행사전문 인력에이전시'
CEO = '김진호'
BIZNO = '265-21-01993'
ADDR = '서울 관악구 서원8길 9, 제2층 301호(신림동)'
TEL = '010-6755-5021'
TEL_RAW = TEL.replace('-', '')
EMAIL = 'ghekddud1234@naver.com'
KAKAO = ''            # 카카오톡 채널 주소를 받으면 여기에 (없으면 문자 상담 단추)
REPO = 'brizymedia/jino-company'   # 공지 관리자가 올린 공지(photos 가지)를 읽는 레포
BASE = 'https://brizymedia.github.io/jino-company'   # 계약 도메인 jinocompany.co.kr 연결 뒤 여기만 바꾸고 다시 실행
NOINDEX = True        # 오픈 확정 뒤 False
VER = "3"
EDIT_HASH = 'f32cba32b5153f2d9b0ee9c6fd936e1d446ddb65e5a5449f5778fab23ed9de91'   # 사장님 직접 수정 열쇠의 sha256 (열쇠 자체는 어디에도 적지 않는다 — 큰길브리지 Desktop 메모에만)
FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwHQP2hTixAj4Rvh_Rx4-LBVNGIBcNhzl9-HZgLNFvoSIwrekvU93s3EhxJ7vyxnux2Fw/exec'    # 문의 서버(Apps Script) 배포 뒤 /exec 주소. 비어 있으면 문자 앱으로 연결
MAP = 'https://map.naver.com/p/search/' + '%EC%84%9C%EC%9A%B8%20%EA%B4%80%EC%95%85%EA%B5%AC%20%EC%84%9C%EC%9B%908%EA%B8%B8%209'
OG = BASE + '/assets/img/og.png'
CLIENT_NAMES = True   # 포트폴리오에 고객사 실명(삼성전자 · 아모레퍼시픽 등)을 보일지. 대표 확인 전이라면 False → 일반 이름으로 바뀐다

NAV = [('about.html', '회사 소개'), ('service.html', '인력 서비스'), ('system.html', '관리 시스템'), ('process.html', '이용 안내'),
       ('portfolio.html', '주요 행사'), ('contact.html', '견적 문의')]

# ════════════════════════ 자료 ════════════════════════
# 필요한 인력 9종 (회사소개서 「전문 인력 유형」) — 대문 「골라 담기」 · 견적 문의 양식에 같이 쓴다
ROLES = [
    ('mc', 'MC · 사회자'), ('guide', '안내 요원'), ('ops', '운영 스태프'),
    ('booth', '부스 운영'), ('product', '제품 설명'), ('demo', '시연 · 체험 지원'),
    ('vip', 'VIP 의전'), ('interp', '통역'), ('intl', '국제 행사 전문'),
]
# 대문 출입증이 돌아가며 보여 주는 역할 (p = 아래 PASS_IMGS 번호)
PASS_IMGS = ['xmas1', 'run2', 'scrub1', 'sf1', 'nyj1', 'poke2', 'sk3']
PASS_ROLES = [
    dict(n='안내 요원', p=0, t='ON SITE · 강북 크리스마스 마켓'),
    dict(n='운영 스태프', p=1, t='ON SITE · 마라톤 행사'),
    dict(n='부스 운영', p=2, t='ON SITE · 스크럽대디 팝업'),
    dict(n='제품 설명', p=3, t='ON SITE · 데이터 박람회'),
    dict(n='MC · 사회자', p=4, t='ON SITE · 동부노인복지관 기념행사'),
    dict(n='시연 · 체험', p=5, t='ON SITE · 포켓몬 팝업스토어'),
    dict(n='VIP 의전', p=6, t='ON SITE · 재단 학술 행사'),
]
TICKER = ['행사 진행요원', '안내 요원', 'MC · 사회자', 'VIP 의전', '통역', '부스 운영', '제품 설명', '시연 · 체험', '운영 스태프', '국제 행사 지원', '현장 총괄']

# 역할 3묶음 (service.html)
ROLE_GROUPS = [
    ('진행 인력', 'sk2', [('MC · 사회자', '행사 진행과 분위기 조성'), ('안내 요원', '참석자 응대와 행사장 안내'), ('운영 스태프', '행사 전반의 운영 지원')]),
    ('전시 · 프로모션 인력', 'scrub2', [('부스 운영 인력', '전시 부스 관리와 운영'), ('제품 설명 인력', '전문적인 제품 소개'), ('시연 인력', '제품 시연과 체험 지원')]),
    ('의전 · 통역 인력', 'agm1', [('VIP 의전', '주요 인사 의전과 수행'), ('통역 인력', '다국어 통역 서비스'), ('국제 행사 전문 인력', '글로벌 행사 지원')]),
]
AREAS = [
    ('기업 행사', 'agm1', ['대기업 컨퍼런스', '신제품 발표회', '워크숍 · 세미나', '기업 기념행사', '각종 주주총회']),
    ('전시 · 박람회', 'sf1', ['산업 박람회', '제품 전시회', '국제 전시회', '채용 박람회']),
    ('프로모션', 'scrub2', ['브랜드 홍보', '제품 시연', '로드쇼', '팝업 스토어']),
    ('공연 · 축제', 'lav4', ['문화 축제', '음악 공연', '스포츠 이벤트', '지역 행사', '각종 페스티벌']),
]
WHY = [
    ('현장을 아는 대표', '스태프부터 현장 팀장까지 거친 대표가 직접 현장에서 뜁니다.'),
    ('맞춤형 인력 매칭', '행사 성격 · 규모 · 예산에 맞춰 인력 구성을 제안합니다.'),
    ('체계적인 인력 관리', '인력 DB와 이력 관리, 행사별 브리핑, 행사 뒤 평가와 피드백까지 이어집니다.'),
    ('안전 교육', '화재 · 위급상황 대처와 AED(자동제세동기) 활용법을 교육합니다.'),
]
MATCH = [
    ('행사 특성 분석', '행사 종류 · 규모 · 분위기를 살펴 맞춤형으로 매칭합니다.'),
    ('요구사항 파악', '고객이 원하는 인력의 역할과 조건을 자세히 듣습니다.'),
    ('인력 DB 매칭', '인력 프로필 데이터베이스에서 후보를 추립니다.'),
    ('선발 · 배치', '최적의 인력을 선발해 행사장에 배치합니다.'),
]
FAQ = [
    ('견적은 어떻게 받나요?', '전화나 문자, 아래 문의 양식 어느 쪽이든 괜찮습니다. 행사 규모 · 성격 · 필요한 인력을 알려 주시면 담당 매니저가 요구사항을 확인하고 인력 운영 계획과 견적을 제안합니다.'),
    ('어느 지역까지 가나요?', '전국으로 인력을 보냅니다. 서울 · 경기뿐 아니라 부산 · 대구 같은 지방 행사도 진행한 기록이 있습니다.'),
    ('급하게 필요한데도 가능한가요?', '긴급 지원 계약이 따로 있습니다. 일정과 인원을 먼저 알려 주세요. 가능한지 확인해 바로 답드립니다.'),
    ('비용은 어떻게 정해지나요?', '인력 유형과 전문성에 따라 요금이 다르고, 행사 규모와 기간에 따른 패키지 할인이 있습니다. 인력 교육과 관리 비용이 포함되며 부가세는 별도입니다. 견적과 정산은 투명하게 보여 드립니다.'),
    ('계약은 어떤 방식인가요?', '일회성 행사를 위한 단기 프로젝트 계약부터 연간 계약, 상주 인력 파견 계약, 긴급 지원 계약까지 7가지 방식이 있습니다. 상담 때 맞는 방식을 안내해 드립니다.'),
    ('행사 당일에도 관리해 주시나요?', '네. 행사 전 최종 점검 미팅을 하고, 당일에는 현장 관리와 모니터링을 하며, 행사 뒤에는 평가와 피드백을 모읍니다.'),
]
NOTICES = json.load(open(os.path.join(ROOT, 'assets/data/notices.json'), encoding='utf-8'))
NJ = html.escape(json.dumps(NOTICES, ensure_ascii=False), quote=True).replace("'", '&#39;')

# 주요 행사 22곳 — (코드, 실명, 일반 이름, 분류, 설명, 사진 코드들). 이름은 대표가 보낸 폴더 이름 기준(실명 공개는 대표 확인 필요)
CATS = [('all', '전체'), ('corp', '기업 · 컨퍼런스'), ('promo', '프로모션 · 전시'), ('fest', '축제 · 지역 행사'), ('show', '공연 · 팬 이벤트'), ('sport', '스포츠')]
CATN = dict(CATS)
EVENTS = [
    ('agm', '삼성전자 주주총회', '대기업 정기 주주총회', 'corp', '주주총회 현장 운영 인력 지원', ['agm1', 'agm2', 'agm3', 'agm4']),
    ('sk', '서경배과학재단 행사', '재단 학술 행사', 'corp', '학술 행사 현장 운영 인력 지원', ['sk1', 'sk2', 'sk3', 'sk4']),
    ('a60', '아모레 60주년 행사', '화장품 기업 60주년 행사', 'corp', '기념행사 부스 운영 인력 지원', ['a60a', 'a60b', 'a60c', 'a60d', 'a60e']),
    ('amhq', '아모레퍼시픽 본사 행사', '화장품 기업 본사 행사', 'corp', '대규모 임직원 행사 운영 인력 지원', ['amhq1', 'amhq2', 'amhq3', 'amhq4']),
    ('jin', '진도 쏠비치 아모레퍼시픽 행사', '리조트 기업 행사', 'corp', '리조트 현장 운영 인력 지원', ['jin2', 'jin1', 'jin3']),
    ('war', '전쟁기념관 국방개혁 세미나', '국방 정책 세미나', 'corp', '세미나 현장 운영 인력 지원', ['war1', 'war2']),
    ('sec', '국가안보 행사', '국가안보 행사', 'corp', '행사장 운영 인력 지원', ['sec1', 'sec2', 'sec3']),
    ('sf', '스노우플레이크 데이터 박람회', 'IT 기업 데이터 박람회', 'promo', '박람회 부스 운영 인력 지원', ['sf1', 'sf2', 'sf3']),
    ('poke', '부산 포켓몬 팝업스토어', '캐릭터 팝업스토어', 'promo', '팝업스토어 운영 인력 지원', ['poke1', 'poke2', 'poke3']),
    ('hug', '대구 허그본 팝업', '패션 브랜드 팝업', 'promo', '팝업 매장 운영 인력 지원', ['hug1', 'hug2', 'hug3']),
    ('scrub', '스크럽대디 팝업', '생활용품 브랜드 팝업', 'promo', '팝업 운영 인력 지원', ['scrub1', 'scrub2', 'scrub3']),
    ('crun', '크런틴 팝업', '과자 브랜드 팝업', 'promo', '팝업 운영 인력 지원', ['crun1', 'crun2', 'crun3']),
    ('fan', '판타지아 대구페스타', '판타지아 대구페스타', 'fest', '캐릭터 퍼레이드 운영 인력 지원', ['fan1', 'fan2', 'fan3', 'fan4']),
    ('lav', '김포 라베니체 축제', '김포 라베니체 축제', 'fest', '축제 현장 운영 인력 지원', ['lav3', 'lav4']),
    ('xmas', '강북 크리스마스 마켓 「별빛 보물창고」', '지역 크리스마스 마켓', 'fest', '마켓 안내소 · 부스 운영 인력 지원', ['xmas1', 'xmas2', 'xmas3', 'xmas4']),
    ('snow', '수원 도담뜰 겨울 행사', '겨울 눈썰매 · 체험 행사', 'fest', '겨울 체험 행사 운영 인력 지원', ['snow1', 'snow2', 'snow3', 'snow4']),
    ('ddp', '동대문 그림그리기 대회', '어린이 그림그리기 대회', 'fest', '대회 현장 운영 인력 지원', ['ddp1', 'ddp2', 'ddp3']),
    ('nyj', '남양주시 동부노인복지관 개관 20주년 기념행사', '노인복지관 개관 기념행사', 'fest', '기념식 운영 인력 지원', ['nyj1', 'nyj2', 'nyj3']),
    ('album', '아이돌 싱글앨범 발매 행사', '아티스트 앨범 발매 행사', 'show', '팬 행사 운영 인력 지원', ['album1', 'album2']),
    ('bday', '유명 연예인 생일 팬 이벤트', '연예인 생일 팬 이벤트', 'show', '팬 이벤트 운영 인력 지원', ['bday1', 'bday2', 'bday3', 'bday4']),
    ('run', '마라톤 행사', '마라톤 행사', 'sport', '마라톤 급수 · 안내 운영 인력 지원', ['run1', 'run2', 'run3', 'run4', 'run5']),
    ('sports', '체육대회 행사', '체육대회 행사', 'sport', '체육대회 운영 인력 지원', ['sports1', 'sports2', 'sports3']),
]
def ev_name(e): return e[1] if CLIENT_NAMES else e[2]
CAPN = {}
for _e in EVENTS:
    for _c in _e[5]:
        CAPN[_c] = ev_name(_e)
CAPN.update({'sk3': ev_name(EVENTS[1]), 'scrub2': ev_name(EVENTS[10])})
STRIP = ['run2', 'xmas2', 'poke2', 'agm1', 'fan2', 'a60c', 'snow1', 'crun1']

# ════════════════════════ 조각 ════════════════════════
esc = lambda s: html.escape(str(s), quote=True)
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'
PREV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
NEXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'


def img(code, cls='', alt=None, w=1280, h=None, eager=False):
    ld = '' if eager else ' loading="lazy" decoding="async"'
    sz = f' width="{w}" height="{h}"' if h else ''
    return f'<img class="{cls}" src="assets/img/p/{code}.webp" alt="{esc(alt or CAPN.get(code, NAME))}"{sz}{ld}>'


def btn(href, text, cls='', ext=False):
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f'<a class="btn {cls}" href="{href}"{t}>{text}<span class="ar">{ARROW}</span></a>'


def header(cur):
    items = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV)
    sheet = ''.join(f'<a class="m" href="{h}">{t}<svg viewBox="0 0 24 24" aria-hidden="true" width="22" height="22"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">본문으로 바로가기</a>
<header class="hdr"><div class="bar">
  <a class="logo" href="index.html" aria-label="{NAME} 처음으로"><img src="assets/img/logo-mark.png" alt="" width="38" height="38"><span class="lt"><b>{NAME}</b><small>{NAME_EN}</small></span></a>
  <nav aria-label="주 메뉴">{items}</nav>
  <a class="tel" href="tel:{TEL_RAW}">{PHONE}{TEL}</a>
  <button class="mbtn" aria-label="메뉴 열기" aria-expanded="false" aria-controls="sheet"><i></i><i></i><i></i></button>
</div></header>
<div class="sheet" id="sheet">{sheet}
  <div class="sub"><a href="notice.html">공지사항</a><a href="blog/index.html">블로그</a><a href="quote.html">자동 견적서</a></div>
  <div class="btns" style="margin-top:28px">{btn("tel:" + TEL_RAW, "전화 " + TEL, "acc")}</div>
</div>'''


def footer():
    kk = f'<a href="{KAKAO}" target="_blank" rel="noopener">카카오톡 상담</a>' if KAKAO else f'<a href="sms:{TEL_RAW}">문자 상담</a>'
    return f'''<div class="tape" aria-hidden="true"></div>
<footer class="ft"><div class="wrap">
  <div class="grid">
    <div><a class="logo" href="index.html" aria-label="{NAME} 처음으로"><img src="assets/img/logo-mark.png" alt="" width="38" height="38"><span class="lt"><b>{NAME}</b><small>{NAME_EN}</small></span></a>
      <div class="info"><b style="color:#fff">{NAME_FULL}</b> · 대표 {CEO}<br>사업자등록번호 {BIZNO}<br>{ADDR}<br>전화 <a href="tel:{TEL_RAW}">{TEL}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
    <div><h4>COMPANY</h4><a href="about.html">회사 소개</a><a href="portfolio.html">주요 행사</a><a href="notice.html">공지사항</a><a href="blog/index.html">행사 인력 블로그</a></div>
    <div><h4>SERVICE</h4><a href="service.html">인력 서비스</a><a href="system.html">인력 관리 시스템</a><a href="process.html">이용 안내</a><a href="quote.html">자동 견적서</a></div>
    <div><h4>CONTACT</h4><a href="contact.html">견적 문의</a><a href="tel:{TEL_RAW}">전화 {TEL}</a>{kk}<a href="mailto:{EMAIL}">이메일</a></div>
  </div>
  <div class="copy"><span>© {datetime.date.today().year} {NAME}. All rights reserved.</span><span>현장은 사람이 만듭니다</span></div>
  <div class="admin-entry" style="text-align:center;padding:14px 0 0;font-size:12px"><a href="office.html" rel="nofollow" style="display:inline-flex;gap:5px;align-items:center;opacity:.5;padding:0;color:#fff"><svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>관리자 모드</a></div>
</div></footer>
<div class="dock"><a href="tel:{TEL_RAW}">전화 상담</a>{kk}</div>
<script src="assets/app.js?v={VER}"></script>
<script src="assets/edit.js?v={VER}" defer></script>
<script defer src="https://www.ai-make.co.kr/stats/stats.js" data-site="jino"></script>'''


def jsonld_biz():
    d = {
        '@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': BASE + '/#business', 'name': NAME, 'alternateName': ['JINO CP.', '지노컴퍼니 행사 인력에이전시'],
        'url': BASE + '/', 'image': OG, 'telephone': TEL, 'email': EMAIL,
        'description': '행사 진행요원 · 안내 요원 · MC · VIP 의전 · 통역 · 전시 · 프로모션 인력을 전국으로 파견하는 행사전문 인력에이전시.',
        'address': {'@type': 'PostalAddress', 'addressCountry': 'KR', 'addressRegion': '서울', 'addressLocality': '관악구', 'streetAddress': '서원8길 9, 제2층 301호'},
        'founder': {'@type': 'Person', 'name': CEO}, 'foundingDate': '2024',
        'areaServed': {'@type': 'Country', 'name': '대한민국'},
        'knowsAbout': ['행사 인력 파견', '행사 진행요원', '안내 요원', 'MC 사회자', 'VIP 의전', '통역', '전시 프로모션 인력', '팝업스토어 운영 인력', '주주총회 운영'],
    }
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def jsonld_faq():
    d = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


def page(fn, title, desc, body, cur='', extra_head=''):
    url = BASE + '/' + ('' if fn == 'index.html' else fn)
    robots = '<meta name="robots" content="noindex,nofollow">' if NOINDEX else ''
    EDIT_META = ('<meta name="jino-edit" content="' + EDIT_HASH + '">') if fn not in ('notice-admin.html', '404.html') else ''
    out = f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<meta name="theme-color" content="#0B1226">
{EDIT_META}
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<meta property="og:type" content="website"><meta property="og:locale" content="ko_KR"><meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{OG}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=IBM+Plex+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<link rel="stylesheet" href="assets/style.css?v={VER}">
{extra_head}
</head>
<body>
{header(cur)}
<main id="main">
{body}
</main>
{footer()}
</body>
</html>
'''
    open(os.path.join(ROOT, fn), 'w', encoding='utf-8', newline='\n').write(out)
    print('wrote', fn)


def phead(crumb, eb, h1, lead=''):
    return f'''<section class="phead"><div class="wrap">
  <p class="crumb"><a href="index.html">HOME</a> / {crumb}</p>
  <span class="eb"><i></i>{eb}</span>
  <h1 class="rv">{h1}</h1>
  {f'<p class="lead rv d1">{lead}</p>' if lead else ''}
</div></section>'''


def cta_band(title='필요한 인력, 날짜만 알려 주세요', sub='행사 규모 · 성격 · 필요한 인원만 알려 주시면 인력 운영 계획과 견적을 정리해 드립니다.'):
    kk = btn(KAKAO, '카카오톡 상담', 'white', True) if KAKAO else btn('sms:' + TEL_RAW, '문자로 문의', 'white')
    return f'''<section class="cta"><div class="wrap"><div class="box rv">
  <span class="eb"><i></i>CONTACT</span>
  <h2>{title}</h2>
  <p>{sub}</p>
  <a class="phone" href="tel:{TEL_RAW}">{TEL}</a>
  <div class="btns">{btn("contact.html", "견적 문의하기", "")}{kk}</div>
</div></div></section>'''


# ════════════════════════ 대문 ════════════════════════
def build_index():
    tick = ''.join(f'<span>{esc(t)}</span>' for t in TICKER) * 2
    pass_imgs = ''.join(f'<img src="assets/img/p/{c}.webp" alt=""{" loading=\"lazy\"" if i else ""}>' for i, c in enumerate(PASS_IMGS))
    chips = ''.join(f'<label class="chip"><input type="checkbox" value="{k}" data-n="{esc(n)}"><span>{n}</span></label>' for k, n in ROLES)
    areas = ''.join(
        f'<a class="area rv d{i % 4 + 1}" href="portfolio.html#{["corp","promo","promo","fest"][i]}">{img(c, "", alt=n)}<div class="in"><span class="n">0{i + 1}</span><h3>{n}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div></a>'
        for i, (n, c, L) in enumerate(AREAS))
    strip = ''.join(f'<figure>{img(c, "", w=1280, h=960)}<figcaption><small>{esc(CATN[next(e[3] for e in EVENTS if c in e[5])])}</small>{esc(CAPN[c])}</figcaption></figure>' for c in STRIP)
    steps = ''.join(f'<li class="rv d{i + 1}"><b>{i + 1}</b><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(MATCH))
    why = ''.join(f'<li class="rv d{i % 4 + 1}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(WHY))
    notes = ''.join(f'<li><a href="notice.html#n{i}"><time>{esc(n["d"])}</time><span class="t">{esc(n["t"])}</span></a></li>' for i, n in enumerate(NOTICES[:3]))
    faq = ''.join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ[:5])
    body = f'''
<section class="hero" aria-label="{NAME} 소개">
  <div class="big" aria-hidden="true">STAFF</div>
  <div class="wrap hgrid">
    <div class="htxt">
      <span class="eb"><i></i>JINO CP. · 행사전문 인력에이전시</span>
      <h1>현장은<br><em>사람</em>이<br>만듭니다</h1>
      <p class="sub">행사에 필요한 사람을, 필요한 날, 필요한 자리에. 스태프부터 현장 팀장까지 다 겪어 본 대표가 직접 발로 뜁니다.</p>
      <div class="btns">{btn("contact.html", "인력 견적 문의", "acc")}{btn("portfolio.html", "주요 행사 보기", "line")}</div>
      <ul class="hnum"><li><b>2011</b><span>현장 첫 출근<br>스태프부터 총괄까지</span></li><li><b>2024</b><span>지노컴퍼니 설립</span></li><li><b>전국</b><span>어디든 인력 파견</span></li></ul>
    </div>
    <div class="passbox" aria-hidden="true"><div class="lanyard"></div><div class="clip"></div>
      <div class="pass" id="pass" data-roles='{esc(json.dumps(PASS_ROLES, ensure_ascii=False))}'>
        <div class="slot"></div>
        <div class="ph">{pass_imgs}<span class="tag"></span></div>
        <div class="role"></div>
        <div class="meta"><span><b>{NAME_EN}</b> STAFF</span><span>ID 2024</span></div>
        <div class="code"></div>
        <div class="stamp">CHECK-IN ✓</div>
      </div>
    </div>
  </div>
</section>
<div class="ticker" aria-hidden="true"><div class="tr">{tick}</div></div>

<section class="sec" id="pick"><div class="wrap pickgrid">
  <div><span class="eb"><i></i>BUILD YOUR CREW</span><h2 class="h2 rv">필요한 <span class="hl">사람</span>부터 골라 보세요</h2>
    <p class="lead rv">행사에 필요한 인력을 눌러 담고 견적 문의로 넘기면, 고른 내용이 그대로 채워집니다.</p>
    <div class="chips rv d1" id="picker">{chips}</div></div>
  <aside class="pickside rv d2" aria-live="polite">
    <div class="cnt" id="pickCnt">0<small>개 선택</small></div>
    <p>고른 인력 구성을 담당 매니저에게 바로 전달합니다.</p>
    <ol id="pickList"></ol>
    <a class="btn acc" id="pickGo" href="contact.html#form">이 구성으로 견적 문의<span class="ar">{ARROW}</span></a>
  </aside>
</div></section>

<section class="sec dark" id="area"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>WHERE WE WORK</span><h2 class="h2 rv">이런 <span class="hl">현장</span>에 섭니다</h2></div>
    <p class="lead rv" style="margin:0">기업 행사부터 팝업스토어, 지역 축제까지. 행사가 있는 곳이면 어디든 인력을 보냅니다.</p></div>
  <div class="areas">{areas}</div>
</div></section>

<section class="sec" id="film"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>ON SITE</span><h2 class="h2 rv">현장 <span class="hl">필름</span></h2></div>{btn("portfolio.html", "주요 행사 전체 보기", "ghost sm")}</div>
  <div class="strip" tabindex="0" aria-label="현장 사진 가로 스크롤">{strip}</div>
</div></section>

<section class="sec p2" id="match"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>MATCHING</span><h2 class="h2 rv">인력은 이렇게 <span class="hl">매칭</span>됩니다</h2></div>
    <a class="btn ghost sm" href="process.html">이용 안내 보기<span class="ar">{ARROW}</span></a></div>
  <ol class="steps">{steps}</ol>
</div></section>

<section class="sec"><div class="wrap">
  <ul class="nums">
    <li class="rv d1"><b>2011</b><span>현장 첫 출근 — 스태프에서 총괄 팀장까지</span></li>
    <li class="rv d2"><b>2024</b><span>개인사업자 등록, 지노컴퍼니 설립</span></li>
    <li class="rv d3"><b>{len(EVENTS)}<small>곳</small></b><span>이 홈페이지에 소개한 주요 행사 현장</span></li>
    <li class="rv d4"><b>350<small>여 명</small></b><span>대규모 콘서트 인력 지원 · 총괄 관리</span></li>
  </ul>
</div></section>

<section class="sec dark" id="ceo"><div class="wrap ceo">
  <div class="ph rv">{img("amhq4", "", alt="대규모 행사 현장의 스태프들", w=1280, h=960)}<span class="badge">SINCE 2011</span></div>
  <div><span class="eb"><i></i>FROM THE CEO</span>
    <blockquote class="rv d1">스태프부터 현장 팀장까지, 현장에서 일하다 에이전시를 냈습니다. 그래서 <em>현장에서 발로 뛰는</em> 최고의 파트너가 되겠습니다.</blockquote>
    <cite class="rv d2">대표 <b>{CEO}</b> · 지노컴퍼니</cite>
    <div class="btns rv d3" style="margin-top:28px">{btn("about.html", "회사 소개", "line")}</div></div>
</div></section>

<section class="sec" id="why"><div class="wrap two">
  <div><span class="eb"><i></i>WHY {NAME_EN}</span><h2 class="h2 rv">믿고 맡기실 수 있는 <span class="hl">이유</span></h2>
    <p class="lead rv">인력의 선발부터 교육, 배치, 행사 뒤 평가까지 한 흐름으로 관리합니다.</p></div>
  <ul class="why">{why}</ul>
</div></section>

<section class="sec p2" id="notice"><div class="wrap two">
  <div><span class="eb"><i></i>NOTICE</span><h2 class="h2 rv">공지사항</h2><p class="lead rv">새 소식과 인력 모집 · 행사 안내를 알려 드립니다.</p><div style="margin-top:26px">{btn("notice.html", "공지 전체 보기", "ghost sm")}</div></div>
  <ul class="notes rv d1">{notes}</ul>
</div></section>

<section class="sec" id="faq"><div class="wrap two">
  <div><span class="eb"><i></i>FAQ</span><h2 class="h2 rv">자주 묻는 <span class="hl">질문</span></h2></div>
  <div class="faq">{faq}</div>
</div></section>
{cta_band()}
'''
    page('index.html', f'{NAME} | 행사 인력 파견 · 진행요원 · 안내요원 · MC · 의전 · 통역', '전국 행사 인력 파견 전문 지노컴퍼니. 행사 진행요원, 안내 요원, MC · 사회자, VIP 의전, 통역, 전시 · 프로모션 인력을 행사에 맞게 매칭합니다. 대표가 직접 현장에서 뜁니다.',
         body, 'index.html', extra_head=jsonld_biz() + jsonld_faq())


# ════════════════════════ 회사 소개 ════════════════════════
def build_about():
    info = f'''<div><dt>상호</dt><dd>{NAME_FULL}</dd></div><div><dt>대표</dt><dd>{CEO}</dd></div>
    <div><dt>사업자등록번호</dt><dd>{BIZNO}</dd></div><div><dt>주소</dt><dd>{ADDR}</dd></div>
    <div><dt>전화</dt><dd><a href="tel:{TEL_RAW}">{TEL}</a></dd></div><div><dt>이메일</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>'''
    cards = [
        ('설립 배경 · 비전', ['2024년 설립, 행사 인력 수급 문제 해결이 목표', '전문성과 신뢰성을 바탕으로 한 서비스', '고객과 인력 모두가 만족하는 플랫폼 구축']),
        ('핵심 사업 영역', ['행사 전문 인력 파견 · 관리', '맞춤형 인력 교육 · 훈련 프로그램', '행사 운영 컨설팅 서비스']),
        ('조직 구성 · 전문성', ['전문 교육팀과 인력 관리팀 운영', '분야별 전문가로 구성된 자문단', '현장 경험이 풍부한 운영 인력']),
    ]
    cs = ''.join(f'<div class="card rv d{i + 1}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (t, L) in enumerate(cards))
    fut = [('기술 혁신', ['실시간 모니터링 · 피드백 플랫폼 구축', '온라인 행사 전문 인력 서비스 영역 확대']), ('서비스 확장', ['산업별 특화 인력 서비스 패키지 개발', '행사 규모 · 업종에 맞는 서비스 고도화']), ('전문성 강화', ['전문적인 슈퍼바이저 교육 프로그램 강화', '서비스 품질 향상을 위한 지속적 역량 개발'])]
    fs = ''.join(f'<div class="card d rv d{i + 1}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (t, L) in enumerate(fut))
    body = phead('회사 소개', 'ABOUT', '행사의 마지막 퍼즐,<br><span class="hl">사람</span>을 채웁니다', '행사 인력 수급 문제를 해결하겠다는 목표로 2024년 시작했습니다.') + f'''
<section class="sec"><div class="wrap two">
  <div class="rv"><span class="eb"><i></i>INTRO</span><h2 class="h2">{NAME}<br>행사전문 인력에이전시</h2></div>
  <div class="prose rv d1">
    <p>지노컴퍼니는 행사에 필요한 <strong>전문 인력을 파견하고 관리</strong>하는 행사전문 인력에이전시입니다. 행사 진행요원, 안내 요원, MC · 사회자, VIP 의전, 통역, 전시 · 프로모션 인력까지 행사 성격에 맞는 사람을 전국으로 보냅니다.</p>
    <p>대표는 <strong>2011년 현장에서 스태프로 일을 시작</strong>해 현장 팀장, 총괄 팀장까지 거쳤고, 2024년 개인사업자를 내고 지노컴퍼니를 시작했습니다. 현장에서 무엇이 필요한지 알기 때문에 인력 선발과 교육, 배치, 사후 평가를 한 흐름으로 챙깁니다.</p>
    <blockquote>「그만큼 현장에서 대표인 제가 발로 뛰며 최고의 파트너가 되겠습니다.」<cite>대표 {CEO}</cite></blockquote>
  </div>
</div></section>

<section class="sec p2"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>WHAT WE DO</span><h2 class="h2 rv">지노컴퍼니는 <span class="hl">이런 곳</span>입니다</h2></div></div>
  <div class="cards3">{cs}</div>
</div></section>

<section class="sec dark"><div class="wrap two">
  <div><span class="eb"><i></i>HISTORY</span><h2 class="h2 rv">걸어온 <span class="hl">길</span></h2></div>
  <ul class="tl rv d1">
    <li><time>2011</time><p>행사 현장에서 스태프로 첫 출근. 이후 현장 팀장, 총괄 팀장까지 경험을 쌓았습니다.</p></li>
    <li><time>2024</time><p>개인사업자 등록, 지노컴퍼니 설립. 행사 인력 파견과 교육 · 관리 서비스를 시작했습니다.</p></li>
    <li><time>NOW</time><p>기업 행사, 박람회, 팝업스토어, 지역 축제, 마라톤까지 전국 현장에 인력을 보내고 있습니다.</p></li>
  </ul>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>NEXT</span><h2 class="h2 rv">앞으로의 <span class="hl">방향</span></h2></div></div>
  <div class="cards3">{fs}</div>
</div></section>

<section class="sec p2"><div class="wrap two">
  <div><span class="eb"><i></i>INFO</span><h2 class="h2 rv">회사 정보</h2></div>
  <dl class="info2 rv d1">{info}</dl>
</div></section>
{cta_band()}
'''
    page('about.html', f'회사 소개 | {NAME}', '지노컴퍼니는 2024년 설립된 행사전문 인력에이전시입니다. 2011년부터 스태프, 팀장, 총괄 팀장으로 현장을 겪은 대표가 직접 인력을 매칭합니다.', body, 'about.html')


# ════════════════════════ 인력 서비스 ════════════════════════
def build_service():
    rc = ''.join(f'''<article class="role-c rv d{i + 1}"><div class="im">{img(c, "", alt=t)}</div><div class="tx"><h3>{t}</h3><ul>{"".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in L)}</ul></div></article>'''
                 for i, (t, c, L) in enumerate(ROLE_GROUPS))
    areas = ''.join(f'<div class="card rv d{i % 4 + 1}"><h3>{n}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (n, c, L) in enumerate(AREAS))
    pv = [('인력 파견', ['다양한 행사에 맞춤형 인력 제공', '전문성을 갖춘 인력 즉시 배치', '긴급 상황 대응 인력 지원', '행사 규모별 인력 구성 제안']),
          ('교육 시스템', ['분야별 전문 교육 프로그램', '현장 실습 중심 실무 교육', '정기적인 역량 강화 교육', '서비스 매너 및 응대 교육']),
          ('품질 관리', ['실시간 모니터링 시스템 운영', '행사 뒤 피드백 수집 · 분석', '인력 평가 · 관리 시스템', '지속적인 서비스 품질 개선'])]
    pvs = ''.join(f'<div class="card rv d{i + 1}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (t, L) in enumerate(pv))
    body = phead('인력 서비스', 'SERVICE', '행사에 맞는 사람을<br><span class="hl">맞춤</span>으로 보냅니다', '진행 · 전시 · 의전 · 통역까지, 행사 성격에 최적화된 전문 인력을 제공합니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>CREW TYPES</span><h2 class="h2 rv">전문 인력 <span class="hl">유형</span></h2></div>
    <p class="lead rv" style="margin:0">지노컴퍼니는 다양한 행사에 최적화된 전문 인력을 제공합니다.</p></div>
  <div class="roles">{rc}</div>
  <div class="btns" style="margin-top:34px">{btn("contact.html", "필요한 인력 견적 문의", "acc")}</div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>WHERE WE WORK</span><h2 class="h2 rv">주요 서비스 <span class="hl">영역</span></h2></div></div>
  <div class="cards3" style="grid-template-columns:repeat(auto-fit,minmax(230px,1fr))">{areas.replace('class="card ', 'class="card d ')}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>HOW WE DELIVER</span><h2 class="h2 rv">서비스는 <span class="hl">이렇게</span> 이루어집니다</h2></div></div>
  <div class="cards3">{pvs}</div>
</div></section>
{cta_band()}
'''
    page('service.html', f'인력 서비스 | {NAME}', '행사 진행요원, 안내 요원, MC · 사회자, 운영 스태프, 부스 운영, 제품 설명, 시연, VIP 의전, 통역, 국제 행사 인력까지. 지노컴퍼니의 행사 인력 파견 서비스.', body, 'service.html')


# ════════════════════════ 관리 시스템 ════════════════════════
def build_system():
    cols = [
        ('인재 발굴 · 선발', ['다양한 분야의 전문가 발굴 네트워크 구축', '엄격한 심사 기준과 다단계 면접 과정', '실무 경험 · 전문성 중심 선발', '인재 데이터베이스 지속적 업데이트']),
        ('교육 · 훈련', ['행사 유형별 맞춤형 교육 커리큘럼', '실전 시뮬레이션 · 롤플레이 훈련', '의전, 고객 응대, 위기 대응 교육', '정기적인 보수교육 · 역량 강화 과정']),
        ('안전 교육', ['화재 시 대처 요령 교육', '위급상황 대처 요령 교육', 'AED(자동제세동기) 활용법 교육']),
    ]
    cs = ''.join(f'<div class="card d rv d{i + 1}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (t, L) in enumerate(cols))
    comp = [
        ('전문성과 경험을 갖춘 인력 풀', ['다양한 행사 경험을 보유한 검증된 전문 인력 확보', '분야별 전문가 인증 · 자격증 소지자 우선 배치', '외국어 능력, 의전 경험 등 특화된 역량 보유 인력', '행사 규모와 성격에 맞는 최적의 인력 매칭 능력']),
        ('체계적인 인력 관리 시스템', ['인력 DB 구축과 체계적인 이력 관리', '실시간 인력 배치 · 모니터링 시스템 운영', '행사별 맞춤형 교육 · 브리핑 프로세스', '인력 평가와 피드백을 통한 지속적 품질 관리', '비상 상황 대응을 위한 백업 인력 운영']),
        ('고객 맞춤형 솔루션', ['고객사의 브랜드 이미지와 행사 목적에 부합하는 인력', '행사 기획 단계부터 인력 운영 전략 수립 지원', '예산과 규모에 맞는 최적화된 인력 구성 제안', '긴급 상황 · 돌발 이슈에 대한 신속한 대응 체계', '행사 뒤 결과 분석과 개선점 도출']),
    ]
    cp = ''.join(f'<div class="card rv d{i + 1}"><h3>{t}</h3><ul>{"".join(f"<li>{x}</li>" for x in L)}</ul></div>' for i, (t, L) in enumerate(comp))
    flow = [('선발', '심사 기준과 다단계 면접'), ('교육', '유형별 커리큘럼 · 안전 교육'), ('배치', '행사 특성에 맞춘 매칭'), ('모니터링', '현장 관리와 실시간 확인'), ('평가', '행사 뒤 피드백 수집 · 분석')]
    fl = ''.join(f'<li class="rv d{i % 4 + 1}"><b>{i + 1}</b><h3>{a}</h3><p>{b}</p></li>' for i, (a, b) in enumerate(flow))
    body = phead('관리 시스템', 'SYSTEM', '뽑는 것부터 평가까지,<br><span class="hl">한 흐름</span>으로', '인력의 선발, 교육, 안전, 품질을 체계적으로 관리합니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>CYCLE</span><h2 class="h2 rv">인력 관리 <span class="hl">사이클</span></h2></div></div>
  <ol class="steps" style="grid-template-columns:repeat(auto-fit,minmax(190px,1fr))">{fl}</ol>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>PEOPLE</span><h2 class="h2 rv">선발 · 교육 · <span class="hl">안전</span></h2></div></div>
  <div class="cards3">{cs}</div>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>STRENGTH</span><h2 class="h2 rv">차별화된 <span class="hl">경쟁력</span></h2></div></div>
  <div class="cards3">{cp}</div>
</div></section>
{cta_band()}
'''
    page('system.html', f'인력 관리 시스템 | {NAME}', '행사 인력의 선발, 교육, 안전 교육, 배치, 모니터링, 사후 평가까지. 지노컴퍼니의 체계적인 인력 관리 시스템.', body, 'system.html')


# ════════════════════════ 이용 안내 ════════════════════════
def build_process():
    apply_ = ['전화로 초기 상담 신청', '행사 규모 · 성격 · 필요 인력 기본 정보 제공', '담당 매니저 배정과 상세 요구사항 파악', '맞춤형 인력 운영 계획 · 견적 제안', '계약 체결과 서비스 일정 확정', '행사 전 최종 점검 미팅', '행사 당일 현장 관리 · 모니터링', '행사 뒤 평가와 피드백 수집']
    st = ''.join(f'<li class="rv d{i % 4 + 1}"><b>{i + 1}</b><h3>{t}</h3></li>' for i, t in enumerate(apply_))
    consult = ['행사 목적과 타겟 고객 분석', '행사 규모와 성격에 맞는 인력 구성 제안', '인력별 역할 · 배치 계획 수립', '브랜드 이미지에 부합하는 서비스 매뉴얼 개발', '행사장 동선과 고객 응대 전략 수립', '위기 상황 대응 매뉴얼 제공', '행사 뒤 성과 분석과 개선점 도출']
    cost = ['인력 유형 · 전문성에 따른 차등 요금제', '행사 규모와 기간에 따른 패키지 할인', '인력 교육 · 관리 비용 포함', '장기 계약 시 우대 혜택', '투명한 견적 · 정산 시스템', '행사 변경 · 취소 시 유연한 대응', '부가세 별도 청구']
    ct = [('단기 프로젝트 계약', '일회성 행사 지원'), ('연간 계약', '정기적인 행사 인력 지원'), ('맞춤형 계약', '고객사 요구에 맞춘 계약'), ('인력 파견 계약', '상주 인력 지원'),
          ('성과 연동형 계약', '결과에 따른 인센티브'), ('단계별 계약', '행사 단계별 인력 지원'), ('긴급 지원 계약', '급작스런 인력 수요 대응')]
    cl = ''.join(f'<li class="rv d{i % 4 + 1}"><b>{a}</b><span>{b}</span></li>' for i, (a, b) in enumerate(ct))
    ul = lambda L: '<ul>' + ''.join(f'<li>{x}</li>' for x in L) + '</ul>'
    body = phead('이용 안내', 'PROCESS', '문의에서 행사 뒤까지,<br><span class="hl">이렇게</span> 진행됩니다', '전화 한 통이면 시작합니다. 행사 후 평가까지 함께합니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>STEP BY STEP</span><h2 class="h2 rv">신청 <span class="hl">절차</span></h2></div></div>
  <ol class="steps">{st}</ol>
  <div class="btns" style="margin-top:34px">{btn("contact.html", "지금 상담 신청", "acc")}</div>
</div></section>

<section class="sec p2"><div class="wrap two">
  <div><span class="eb"><i></i>CONSULTING</span><h2 class="h2 rv">맞춤형 <span class="hl">컨설팅</span></h2><p class="lead rv">행사 기획 단계부터 인력 운영 전략을 함께 세웁니다.</p></div>
  <div class="card rv d1">{ul(consult)}</div>
</div></section>

<section class="sec"><div class="wrap two">
  <div><span class="eb"><i></i>COST</span><h2 class="h2 rv">비용 <span class="hl">체계</span></h2><p class="lead rv">정해진 단가표 대신, 행사에 맞춰 견적을 드립니다. 자동 견적서에서 항목을 골라 미리 확인해 볼 수 있습니다.</p>
    <div style="margin-top:22px">{btn("quote.html", "자동 견적서 열기", "ghost sm")}</div></div>
  <div class="card rv d1">{ul(cost)}</div>
</div></section>

<section class="sec dark"><div class="wrap">
  <div class="sechead"><div><span class="eb"><i></i>CONTRACT</span><h2 class="h2 rv">계약 <span class="hl">방식</span></h2></div>
    <p class="lead rv" style="margin:0">행사 성격에 맞는 방식을 고를 수 있습니다.</p></div>
  <ul class="contract">{cl}</ul>
</div></section>
{cta_band()}
'''
    page('process.html', f'이용 안내 | {NAME}', '지노컴퍼니 이용 안내. 상담 신청부터 인력 운영 계획, 견적, 계약, 행사 당일 관리와 사후 평가까지. 비용 체계와 7가지 계약 방식.', body, 'process.html')


# ════════════════════════ 주요 행사 ════════════════════════
def build_portfolio():
    cnt = {k: sum(1 for e in EVENTS if e[3] == k) for k, _ in CATS}
    cnt['all'] = len(EVENTS)
    filt = ''.join(f'<button type="button" data-f="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}<small>{cnt[k]}</small></button>' for k, n in CATS)
    cards = ''.join(
        f'<button type="button" class="pj rv d{i % 3 + 1}" data-c="{e[3]}" data-k="{i}" aria-label="{esc(ev_name(e))} 사진 {len(e[5])}장 보기">'
        f'<div class="im">{img(e[5][0], "", alt=ev_name(e), w=1280, h=960)}<span class="cat">{CATN[e[3]]}</span><span class="cnt">{len(e[5])} PHOTOS</span></div>'
        f'<div class="tx"><h3>{esc(ev_name(e))}</h3><p>{esc(e[4])}</p></div></button>' for i, e in enumerate(EVENTS))
    data = html.escape(json.dumps([{'n': ev_name(e), 'c': CATN[e[3]], 'i': e[5]} for e in EVENTS], ensure_ascii=False), quote=True)
    body = phead('주요 행사', 'PORTFOLIO', '현장에서 <span class="hl">보여드립니다</span>', f'기업 행사, 박람회, 팝업스토어, 지역 축제, 마라톤까지. 지노컴퍼니 인력이 선 {len(EVENTS)}곳의 현장입니다.') + f'''
<section class="sec"><div class="wrap">
  <div class="filters" role="group" aria-label="행사 분류">{filt}</div>
  <div class="pf" id="pf" data-p="{data}">{cards}</div>
  <p class="lead" style="margin-top:34px">카드를 누르면 현장 사진을 크게 볼 수 있어요. 더 많은 행사 자료는 문의 주시면 회사소개서로 보내 드립니다.</p>
</div></section>
<div class="lb" id="lb" role="dialog" aria-modal="true" aria-label="현장 사진 크게 보기">
  <button class="x" type="button" aria-label="닫기">{CLOSE}</button><button class="pv" type="button" aria-label="이전 사진">{PREV}</button><button class="nx" type="button" aria-label="다음 사진">{NEXT}</button>
  <figure><img src="" alt=""><figcaption></figcaption></figure>
</div>
{cta_band('우리 행사에도 같은 인력을', '행사 규모와 성격을 알려 주시면 비슷한 현장 경험이 있는 인력으로 구성안을 드립니다.')}'''
    page('portfolio.html', f'주요 행사 | {NAME}', '지노컴퍼니 인력이 선 주요 행사 현장. 주주총회, 기업 행사, 박람회, 팝업스토어, 지역 축제, 마라톤, 체육대회까지.', body, 'portfolio.html')


# ════════════════════════ 공지 ════════════════════════
def build_notice():
    items = ''.join(f'<article class="nt rv" id="n{i}"><time>{esc(n["d"])}</time><h3>{esc(n["t"])}</h3><p>{esc(n["b"])}</p></article>' for i, n in enumerate(NOTICES))
    live = f'''<script>
(function(){{
  var box=document.getElementById('nlist'); if(!box||location.protocol.indexOf('http')!==0) return;
  function esc(t){{return String(t==null?'':t).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}});}}
  fetch('https://raw.githubusercontent.com/{REPO}/photos/photos/notices.json?t='+Math.floor(Date.now()/120000),{{cache:'no-store'}}).then(function(r){{return r.ok?r.json():null;}}).then(function(j){{
    if(!j||!j.notices||!j.notices.length) return;
    var st=[]; try{{st=JSON.parse(box.getAttribute('data-static')||'[]');}}catch(x){{}}
    box.innerHTML=j.notices.concat(st).map(function(n,i){{return '<article class="nt in" id="n'+i+'"><time>'+esc(n.d)+'</time><h3>'+esc(n.t)+'</h3><p>'+esc(n.b||'')+'</p></article>';}}).join('');
  }}).catch(function(){{}});
}})();
</script>'''
    body = phead('공지사항', 'NOTICE', '공지사항', '새 소식과 인력 모집 · 행사 안내를 알려 드립니다.') + f'<section class="sec"><div class="wrap narrow" id="nlist" data-static=\'{NJ}\'>{items}</div></section>' + live + cta_band()
    page('notice.html', f'공지사항 | {NAME}', '지노컴퍼니 공지사항.', body, '')


def build_notice_admin():
    import re
    pd = open(os.path.join(ROOT, 'tools/port_docs.py'), encoding='utf-8').read()
    m = re.search(r"^GALLERY_URL\s*=\s*'([^']*)'", pd, re.M)
    gurl = m.group(1) if m else ''
    body = f"""<section class="phead" style="padding-bottom:30px"><div class="wrap"><span class="eb"><i></i>ADMIN</span><h1 style="font-size:clamp(30px,5vw,52px)">공지사항 관리</h1>
<p class="lead">공지를 쓰면 홈페이지 공지사항에 올라갑니다(몇 분 안에). 사진 올리기와 같은 비밀번호를 씁니다.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap" style="max-width:900px">
<style>.nadm .nrow{{display:flex;gap:14px;flex-wrap:wrap;align-items:baseline;padding:16px 0;border-bottom:2px dashed var(--line)}}.nadm .nrow time{{color:var(--acc-ink);font-weight:800;font-size:14px;width:96px;flex:none}}.nadm .nrow .t{{font-weight:800;flex:1;min-width:200px}}.nadm .nrow .t small{{display:block;font-weight:500;color:var(--soft)}}.nadm .new{{background:var(--acc);color:var(--ink);border-radius:999px;padding:1px 9px;font-size:11px;margin-left:6px}}.nadm .msg{{color:var(--soft);font-weight:700;margin:8px 0 0}}.nadm .box{{background:#fff;border:2px solid var(--ink);border-radius:20px;padding:22px}}</style>
<div class="nadm">
<div id="setup" class="box" hidden></div>
<form class="form" id="login" style="max-width:420px"><label>비밀번호<input type="password" id="pw" autocomplete="current-password"></label><button class="btn acc" type="submit">들어가기<span class="ar">{ARROW}</span></button><p id="lmsg" class="msg" style="color:#C0210B"></p></form>
<div id="panel" hidden>
  <form class="form box" id="nf"><input type="hidden" id="nid">
    <div class="row2"><label>날짜<input id="nd" placeholder="2026.11.20"></label><label>NEW 표시<select id="nn"><option value="1">표시함</option><option value="0">표시 안 함</option></select></label></div>
    <label>제목 *<input id="nt" maxlength="120"></label>
    <label>내용 (선택)<textarea id="nb" rows="4" maxlength="1500" placeholder="자세한 안내가 있으면 적어 주세요."></textarea></label>
    <div class="btns"><button class="btn acc" type="submit">저장하기<span class="ar">{ARROW}</span></button><button class="btn ghost" type="button" id="nreset">새로 쓰기<span class="ar">{ARROW}</span></button></div>
    <p id="nmsg" class="msg" role="status"></p>
  </form>
  <h2 class="h2" style="font-size:26px;margin:36px 0 6px">올린 공지</h2>
  <div id="nlist"></div>
</div>
</div>
<script>
(function(){{
  var SERVER = '{gurl}', KEY = 'jino-notice-pw';
  var $ = function(i){{ return document.getElementById(i); }};
  var pw = ''; try {{ pw = sessionStorage.getItem(KEY) || ''; }} catch(e) {{}}
  var list = [];
  function esc(t){{ return String(t==null?'':t).replace(/[&<>"]/g,function(c){{return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c];}}); }}
  function call(body){{
    body.pw = pw;
    return fetch(SERVER, {{method:'POST', headers:{{'Content-Type':'text/plain;charset=utf-8'}}, body: JSON.stringify(body)}}).then(function(r){{return r.json();}});
  }}
  function today(){{ var d=new Date(); return d.getFullYear()+'.'+('0'+(d.getMonth()+1)).slice(-2)+'.'+('0'+d.getDate()).slice(-2); }}
  function reset(){{ $('nid').value=''; $('nd').value=today(); $('nt').value=''; $('nb').value=''; $('nn').value='1'; }}
  function draw(){{
    $('nlist').innerHTML = list.length ? list.map(function(n,i){{
      return '<div class="nrow"><time>'+esc(n.d)+'</time><span class="t">'+esc(n.t)+(n.n?'<span class="new">NEW</span>':'')+(n.b?'<small>'+esc(n.b)+'</small>':'')+'</span><span class="btns"><button class="btn sm ghost" data-e="'+i+'">수정</button><button class="btn sm" data-x="'+i+'">삭제</button></span></div>';
    }}).join('') : '<p class="msg">아직 이 화면으로 올린 공지가 없습니다. (처음 열 때 홈페이지에 보이는 기본 공지는 사이트에 들어 있는 것입니다.)</p>';
  }}
  function open(){{
    $('login').hidden = true; $('panel').hidden = false; reset();
    call({{action:'notice-list'}}).then(function(j){{ if(j && j.ok){{ list=j.notices||[]; draw(); }} else {{ $('login').hidden=false; $('panel').hidden=true; $('lmsg').textContent=(j&&j.error)||'열 수 없습니다.'; }} }})
      .catch(function(){{ $('lmsg').textContent='서버에 연결하지 못했습니다.'; $('login').hidden=false; $('panel').hidden=true; }});
  }}
  if(!SERVER){{
    $('login').hidden = true;
    var s = $('setup'); s.hidden = false;
    s.innerHTML = '<b>아직 공지 서버가 연결되지 않았습니다.</b><br>큰길브리지가 사진 업로드 서버(apps-script/gallery)를 배포하고 주소를 넣으면 이 화면이 열립니다. 그 전에는 큰길브리지(1533-7295)에 공지 내용을 알려 주세요.';
  }}
  $('login').addEventListener('submit', function(e){{
    e.preventDefault(); pw = $('pw').value; if(!pw) return;
    try {{ sessionStorage.setItem(KEY, pw); }} catch(x) {{}}
    open();
  }});
  $('nf').addEventListener('submit', function(e){{
    e.preventDefault();
    var t = $('nt').value.trim(); if(!t){{ $('nmsg').textContent='제목을 적어 주세요.'; return; }}
    $('nmsg').textContent='저장하는 중…';
    call({{action:'notice-save', notice:{{id:$('nid').value, d:$('nd').value, t:t, b:$('nb').value, n:$('nn').value==='1'}}}})
      .then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); reset(); $('nmsg').textContent='저장했습니다. 홈페이지에는 몇 분 안에 보입니다.'; }} else $('nmsg').textContent=(j&&j.error)||'저장하지 못했습니다.'; }})
      .catch(function(){{ $('nmsg').textContent='서버에 연결하지 못했습니다.'; }});
  }});
  $('nreset').addEventListener('click', reset);
  $('nlist').addEventListener('click', function(e){{
    var b = e.target.closest('button'); if(!b) return;
    if(b.dataset.e){{ var n=list[+b.dataset.e]; $('nid').value=n.id; $('nd').value=n.d; $('nt').value=n.t; $('nb').value=n.b||''; $('nn').value=n.n?'1':'0'; scrollTo({{top:0,behavior:'smooth'}}); }}
    if(b.dataset.x && confirm('이 공지를 삭제할까요?')){{ var n2=list[+b.dataset.x]; call({{action:'notice-delete', id:n2.id}}).then(function(j){{ if(j&&j.ok){{ list=j.notices; draw(); }} else alert((j&&j.error)||'삭제하지 못했습니다.'); }}); }}
  }});
  if(SERVER && pw) open();
}})();
</script></div></section>"""
    page('notice-admin.html', f'공지사항 관리 | {NAME}', '공지사항 관리 화면', body, '', extra_head='<meta name="robots" content="noindex,nofollow">')


# ════════════════════════ 견적 문의 ════════════════════════
def build_contact():
    chips = ''.join(f'<label class="chip"><input type="checkbox" name="roles" value="{k}" data-n="{esc(n)}"><span>{n}</span></label>' for k, n in ROLES)
    faq = ''.join(f'<details class="rv"><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    kk = f'<a class="cc" href="{KAKAO}" target="_blank" rel="noopener"><b>카카오톡</b><span>채널로 바로 상담</span></a>' if KAKAO else ''
    body = phead('견적 문의', 'CONTACT', '필요한 인력과 날짜만<br><span class="hl">알려 주세요</span>', '전화, 문자, 아래 양식 어느 쪽이든 괜찮습니다.') + f'''
<section class="sec"><div class="wrap cgrid">
  <form class="form rv" id="form" data-endpoint="{FORM_ENDPOINT}" data-tel="{TEL_RAW}" data-email="{EMAIL}" novalidate>
    <h2>인력 견적 문의</h2>
    <label>성함 · 회사명<input name="name" required autocomplete="organization" placeholder="예: ○○ 주식회사 홍길동 팀장"></label>
    <label>연락처<input name="phone" required type="tel" inputmode="tel" autocomplete="tel" placeholder="010-0000-0000"></label>
    <fieldset class="fset"><legend>필요한 인력 (여러 개 선택)</legend><div class="chips">{chips}</div></fieldset>
    <label>행사명<input name="event" placeholder="예: 2026 ○○ 신제품 발표회"></label>
    <div class="row2"><label>행사 날짜<input name="date" placeholder="예: 12월 5일 / 미정"></label><label>필요 인원<input name="people" placeholder="예: 안내 요원 10명"></label></div>
    <label>장소<input name="place" placeholder="예: 서울 코엑스 / 부산 벡스코"></label>
    <label>문의 내용<textarea name="msg" rows="4" placeholder="행사 성격, 근무 시간, 복장 등 알려 주실 내용"></textarea></label>
    <label class="agree"><input type="checkbox" name="agree" required> 문의 답변을 위해 성함 · 연락처를 사용하는 데 동의합니다.</label>
    <input type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px">
    <button class="btn acc" type="submit">문의 보내기<span class="ar">{ARROW}</span></button>
    <p class="fmsg" role="status" aria-live="polite"></p>
  </form>
  <aside class="rv d1">
    <a class="cc big" href="tel:{TEL_RAW}"><b>전화 상담</b><span>{TEL}</span></a>
    <a class="cc" href="sms:{TEL_RAW}"><b>문자 상담</b><span>{TEL}</span></a>
    {kk}
    <a class="cc" href="mailto:{EMAIL}"><b>이메일</b><span>{EMAIL}</span></a>
    <div class="cc plain"><b>주소</b><span>{ADDR}</span><a class="map" href="{MAP}" target="_blank" rel="noopener">네이버 지도에서 보기 →</a></div>
  </aside>
</div></section>
<section class="sec p2"><div class="wrap two">
  <div><span class="eb"><i></i>FAQ</span><h2 class="h2 rv">자주 묻는 <span class="hl">질문</span></h2></div>
  <div class="faq">{faq}</div>
</div></section>'''
    page('contact.html', f'견적 문의 | {NAME}', f'지노컴퍼니 행사 인력 견적 문의. 전화 {TEL}, 문자, 문의 양식. 전국 행사 인력 파견.', body, 'contact.html', extra_head=jsonld_faq())


def build_404():
    body = f'<section class="phead"><div class="wrap"><span class="eb"><i></i>404</span><h1>찾는 페이지가 없어요</h1><p class="lead">주소가 바뀌었거나 잘못 입력되었을 수 있어요.</p><div class="btns" style="margin-top:24px">{btn("index.html", "처음으로", "acc")}</div></div></section>'
    page('404.html', f'페이지를 찾을 수 없어요 | {NAME}', '페이지를 찾을 수 없습니다.', body)


def build_seo():
    pages = ['', 'about.html', 'service.html', 'system.html', 'process.html', 'portfolio.html', 'notice.html', 'contact.html', 'quote.html']
    today = datetime.date.today().isoformat()
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{BASE}/{p}</loc><lastmod>{today}</lastmod></url>\n' for p in pages) + '</urlset>\n'
    open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(sm)
    rb = ('User-agent: *\nDisallow: /\n' if NOINDEX else 'User-agent: *\nAllow: /\nDisallow: /contract.html\nDisallow: /statement.html\nDisallow: /office.html\nDisallow: /schedule.html\nDisallow: /upload.html\nDisallow: /notice-admin.html\n') + f'Sitemap: {BASE}/sitemap.xml\n'
    open(os.path.join(ROOT, 'robots.txt'), 'w', encoding='utf-8', newline='\n').write(rb)
    ll = f'''# {NAME_FULL}
> 전국 행사 인력 파견 전문 행사전문 인력에이전시. 행사 진행요원 · 안내 요원 · MC · 사회자 · VIP 의전 · 통역 · 전시 · 프로모션 인력을 행사 성격에 맞게 매칭한다. 2024년 설립, 대표는 2011년부터 현장 스태프 · 팀장 · 총괄 팀장으로 일했다.

- 대표: {CEO} · 전화 {TEL} · {EMAIL}
- 주소: {ADDR}
- 서비스: 행사 인력 파견 / 맞춤형 인력 교육 · 훈련 / 행사 운영 컨설팅
- 인력 유형: MC · 사회자, 안내 요원, 운영 스태프, 부스 운영, 제품 설명, 시연 · 체험 지원, VIP 의전, 통역, 국제 행사 전문 인력
- 서비스 영역: 기업 행사(컨퍼런스 · 주주총회 · 기념행사), 전시 · 박람회, 프로모션 · 팝업스토어, 공연 · 축제 · 지역 행사 · 마라톤
- 계약 방식: 단기 프로젝트 · 연간 · 맞춤형 · 인력 파견 · 성과 연동형 · 단계별 · 긴급 지원
- 비용: 인력 유형 · 전문성에 따른 차등 요금, 규모 · 기간 패키지 할인, 부가세 별도

## 페이지
- [회사 소개]({BASE}/about.html)
- [인력 서비스]({BASE}/service.html)
- [인력 관리 시스템]({BASE}/system.html)
- [이용 안내]({BASE}/process.html)
- [주요 행사]({BASE}/portfolio.html)
- [견적 문의]({BASE}/contact.html)
'''
    open(os.path.join(ROOT, 'llms.txt'), 'w', encoding='utf-8', newline='\n').write(ll)


if __name__ == '__main__':
    build_index(); build_about(); build_service(); build_system(); build_process(); build_portfolio(); build_notice(); build_notice_admin(); build_contact(); build_404(); build_seo()

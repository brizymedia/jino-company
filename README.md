# 지노컴퍼니 홈페이지 (행사전문 인력에이전시)

큰길브리지 계약 **KB-20261007-151** (회사형 · 부가세 별도 1,000,000원 · 장부 1,100,000원). 2026-11-17 첫 제작.
대표 김진호 · 010-6755-5021 · ghekddud1234@naver.com · 서울 관악구 서원8길 9, 제2층 301호(신림동) · 사업자 265-21-01993.
계약 도메인 `jinocompany.co.kr` (연결 전) · 문의 접수 2026-10-05.

## 보기 / 고치기
```
python -m http.server 8822 --directory C:/Users/gilau/Documents/jino-company
set PYTHONUTF8=1
python tools/build_site.py      # 페이지 · sitemap · robots · llms.txt 를 다시 만든다 (-I 옵션 쓰지 말 것)
```
글 · 연락처 · 메뉴는 `tools/build_site.py` 맨 위에서 고친다. 공지는 `assets/data/notices.json`.
**손으로 `*.html` 을 고치지 말 것** — 다시 빌드하면 덮어써진다.

## 디자인 콘셉트
**현장 출입증(STAFF PASS).** 잉크 네이비 + 현장 오렌지 + 안전띠 노랑. 대문 첫 화면의 목걸이 출입증이 안내 요원 · 운영 스태프 · 부스 운영 · 제품 설명 · MC · 시연 · VIP 의전을 돌아가며 「CHECK-IN」 도장을 찍고(실제 현장 사진 7컷), 마우스를 따라 기울어진다.
대문 「필요한 사람부터 골라 보세요」는 인력 9종을 눌러 담으면 견적 문의 양식에 그대로 채워진다(`contact.html?roles=…`).
글꼴: Black Han Sans(제목) · Pretendard(본문) · IBM Plex Mono(표지). 움직임 줄이기 설정을 지킨다.

## 자료 출처
- `Desktop\큰길브리지\지노컴퍼니\` — `지노컴퍼니 회사소개서(행사 상세표).pptx`(12쪽 + 사진 28쪽), 행사 사진 zip 22개(약 1.2GB, 사진 약 400장).
  글은 회사소개서 문구를 그대로 옮겼다. zip 은 `_raw/` 에 풀어 두었고(레포에 안 올림), `tools/import_photos.py` 가 고른 컷 76장을 `assets/img/p/*.webp`(약 11MB)로 줄여 넣는다.
- 계약서(Drive `NJKA8ARR.json`)와 계약 대장, 문의 메일, 줌 채팅(2026-10-05), 통화 녹음(2026-10-27 「홈페이지 자료 보내 주세요」).

## 납품 전에 확인할 것 (김진호 대표)
1. **계약 서명** — 계약 대장 상태가 「발송」(서명 안 됨)이다. 서명 · 입금 확인.
2. **로고** — 받은 로고가 없다. 지금은 임시 마크(출입증 모양 J, `tools/make_brand.py`). 계약에 「로고 리터치」가 있으니 기존 로고 파일(AI/PNG) 요청.
3. **고객사 실명** — 「주요 행사」에 삼성전자 · 아모레퍼시픽 · 서경배과학재단 등 폴더 이름 그대로 썼다. 대표 확인 전이면 `build_site.py` 의 `CLIENT_NAMES = False` 로 두면 「대기업 정기 주주총회」 같은 일반 이름으로 바뀐다.
4. **숫자** — 2011(현장 첫 출근)은 문의 글 「11년도부터」, 2024(설립)는 회사소개서, 「350여 명」은 회사소개서의 「대규모 콘서트 350여명 인력지원」. 확인.
5. **일부러 안 옮긴 것** — 회사소개서의 「고객 만족도 95% 이상」, 「고객사 후기 3개」, 「2년 이상 연간 계약 사례」는 근거가 없어 사이트에 넣지 않았다. 근거를 받으면 추가.
6. **사진 공개** — 아이들이 나온 컷(수원 도담뜰 눈썰매 · 동대문 그림그리기 · 포켓몬 팝업 · 판타지아 대구페스타), 연예인 팬 이벤트 2곳, 전쟁기념관 · 국가안보 행사(공공 · 국방 행사). 얼굴이 크게 나온 컷은 뺐지만 공개 동의 확인.
7. **카카오톡 채널 · 인스타 · 블로그 · 영업시간** — 받은 것이 없어 안 넣었다(`KAKAO` 에 주소를 넣으면 단추가 생긴다).
8. **대표 직인 PNG** — `assets/img/stamp-jino.png` 로 넣으면 견적서 · 계약서 · 명세서에 찍힌다(없으면 「(인)」).
9. **주소** — 사업자 주소(신림동 2층 301호)를 대표 주소로 썼다. 사무실이 다르면 알려 달라고.

## 계약 항목 점검
| 계약 항목 | 상태 |
|---|---|
| 회사형 홈페이지 10페이지 | 대문 · 회사 소개 · 인력 서비스 · 관리 시스템 · 이용 안내 · 주요 행사 · 공지 · 견적 문의 + 블로그 + 자동 견적서 |
| 브랜드 컨설팅 · 로고 리터치 | 로고 대기(임시 마크) |
| 공지 · 게시판 관리자 | `notice-admin.html` 완료 — **사진·공지 서버 배포 뒤 작동** |
| 직접 수정 CMS + 교육 | 수정 모드(`?edit=열쇠`) 완료 · 매뉴얼 www.ai-make.co.kr/manual/ |
| 갤러리 + 인스타·블로그 자동 연동 | 「사진 올리기 + 글 만들기」(`upload.html`) 이식. 인스타 · 블로그 계정이 없어 연동은 대기 |
| 네이버 · 구글 AI 검색 세팅 | JSON-LD · llms.txt · sitemap · robots 완료 — 서치콘솔 · 네이버 등록은 도메인 연결 뒤 |
| 자동 계약서 작성 · 서명 | `contract.html` 이식 — **계약 서버 배포 뒤 작동** |
| AI 검색 최적화(블로그 10개) | `/blog/` 첫 10편 (아래) |
| 3D 무대시안 | **미착수** — 무대 요구사항 · 로고 필요(큰길이벤트.com/stage3d 방식) |
| 도메인 등록 + 연결 | jinocompany.co.kr 대기(어대리 DNS) |
| 1개월 무상 유지보수 · 월 관리비 5만원 | 특약: 4주 강의 종료 뒤 선택, 직접 관리하면 면제 |
| AI 마케팅 실무 강의 영상 증정 · 매월 블로그 10회 | 별도 |

## 업무 도구 · 사장님 수정 모드
```
python tools/port_docs.py     # 큰길이벤트 원본(~/Documents/클로드코드)에서 업무 도구를 이 회사용으로 다시 옮긴다
```
- 옮긴 것: `quote.html`(+`quote-catalog.js` 인력 9종 + 운영 3종, 가격은 전부 비워 둠) · `contract.html` · `statement.html` · `schedule.html` · `upload.html` · `office.html`(대표 전용 · 바닥글 「관리자 모드」) · `admin-lock.js` · `apps-script/contract` · `apps-script/gallery`(+공지 액션) · `apps-script/inquiry`.
- 회사 설정은 `tools/port_docs.py` 맨 위. **결과 HTML 은 손으로 고치지 말고** 거기서 고친 뒤 다시 실행.
- 사장님 수정 모드: `?edit=열쇠`. 레포에는 열쇠의 sha256(`build_site.py` 의 `EDIT_HASH`)만 있고 열쇠 · 대표 암호는 `Desktop\큰길브리지\지노컴퍼니-수정모드-열쇠.txt` 에만 있다.
- **서버 3개(문의 · 계약 · 사진·공지) 배포 전**이라 `port_docs.py` 의 `CONTRACT_URL` · `GALLERY_URL`, `build_site.py` 의 `FORM_ENDPOINT` 가 비어 있다. 배포(형님 구글 계정) 뒤 `/exec` 주소를 넣고 `port_docs.py` → `build_site.py` 순서로 다시 실행. 계약 서버 스크립트 속성 `BOX_PW` 에 txt 의 대표 암호.
- 문의 폼은 서버 연결 전에는 문자 앱으로 내용이 넘어간다.

## 행사 준비 블로그 (/blog/)
```
python tools/build_site.py          # ① 페이지
python tools/blog_shell.py          # ② 머리 · 꼬리를 _blog/shell.json 으로
node scripts/build-blog.mjs         # ③ /blog/ · rss.xml · sitemap · llms.txt 에 블로그 항목
node scripts/blog-check.mjs         # 글 검사
```
실행 순서는 반드시 ① → ② → ③. 글 규칙 · 쓸 수 있는 사실은 `_blog/GUIDE.md`. `blog/` 는 매번 지우고 다시 만드니 손으로 고치지 않는다.

## 오픈할 때
`build_site.py` 의 `BASE`(도메인) · `NOINDEX = False` → `python tools/port_docs.py`(HOME 도 같이) → `python tools/build_site.py` → `python tools/blog_shell.py` → `node scripts/build-blog.mjs`. `CNAME` 파일, 사이트맵 · 서치콘솔 · 네이버 등록. 유입 현황판(`data-site="jino"`)은 큰길브리지 stats 에 사이트 키 추가가 필요하다.

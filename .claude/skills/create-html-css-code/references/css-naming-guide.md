# CSS Naming Guide

CSS 클래스 네이밍 가이드.

## 네이밍 철칙
- snake_case로 형태_의미 형식(ex. tit_txt, box_desc, area_form). _는 1회 강력히 권장
  - 유니크한 네이밍이 필요한 컴포넌트/섹션 최상위 클래스(단일 셀렉터)와 모듈 앵커(셀렉터 맨 앞에 오는 모듈 클래스)의 경우 **최대 2회**까지 허용(ex. list_museum_news, section_media_news)
- 아래 샘플 네이밍을 최대한 준수하고 없는 부분은 형태_상태(또는 의미) 형식에 맞춰 자유롭게 작성

## 샘플 네이밍

### Prefix — 요소의 형태 표현, 네이밍 앞에 사용
- 레이아웃: wrap·area·group·container·layout·section(영역/레이아웃), main(메인), cont(콘텐츠), page(페이지), inner(컨테이너 안쪽 폭 제한), side(사이드), grid·col·row(그리드/컬럼), box·frame(박스/프레임)
- 헤더/푸터: header, footer
- 내비게이션: menu·nav(메뉴), gnb(global nav), lnb(local nav), snb(side nav), breadcrumb(브레드크럼), paging(페이징), quick(퀵메뉴)
- UI 컴포넌트: btn(버튼), ico(아이콘), img·thumb(이미지), logo, list, tbl(테이블), form·field(폼), inp·select·chk(입력 요소), label, link, visual(비주얼 영역), card(카드형 모듈), noti·alarm(공지/알림), accordion, tooltip, progress, bnr(배너), search(검색), cmt·reply(댓글), tag, toggle
- 모달/팝업: modal·layer(모달/레이어), popup(팝업)
- 미디어/콘텐츠: slide(슬라이드), vod(비디오), aud(오디오), gal(갤러리), txt(텍스트), tit(제목), desc(상세 설명), bg(배경)
- 기타: util·help(유틸), hide(숨김), err·warn(에러), load(로딩), info(정보)

### Suffix — 요소를 꾸며주는 용도, 중간 또는 마지막에 작성
- 크기/레이아웃: xsm·sm·md·lg·xl·xxl(크기), full(전체), half(반), auto(오토), fix·fixed(고정)
- 위치: top·bottom·left·right(상하좌우), center(중앙), start(시작), end(끝), vert(수직), horz(수평)
- 유형/컴포넌트: txt(텍스트), ico(아이콘), item(아이템), tit(제목), desc(설명), label(라벨), media(미디어), thumb(썸네일), info(정보)
- 기타: fst(첫번째), lst(마지막), child(자식 요소), parent(부모 요소), nested(중첩됨), bg(배경), del(삭제)

### Modifier — 요소의 상태 표현, 기본 클래스에 체이닝으로 추가
- on·open·active 는 뜻을 나눠 쓴다 — 섞어 쓰면 상태의 뜻이 흐려진다
  - on(현재) — 현재 페이지·현재 탭처럼 지금 가리키는 항목이 유지되는 상태
  - open(열림) — 아코디언·드롭다운처럼 펼쳐진 상태
  - active(활성화되어 나타남) — 활성 탭 패널처럼 원래 없다가 활성화되어 나타난 요소
- disabled(비활성화), selected(선택됨), err(에러), fix·fixed(고정됨)

가이드에 없는 Prefix/Suffix/Modifier는 각 역할(형태 표현/꾸밈/상태)에 맞춰 자유롭게 작성.

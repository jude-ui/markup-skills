# CSS writing Guide
CSS 작성 가이드(Reset·CSS 모듈 규칙·셀렉터·레이아웃/반응형·속성 선언 순서·값 표기·CSS 변수·포맷).

## Reset
이 스킬이 작동하는 프로젝트가 reset이 있을수도 있고 없을수도 있기 때문에 reset CSS 를 쓰고 있는지 **사용자에게 묻는다.** 별도 파일로 있거나 `common.css`·`layout.css` 같은 파일 안에 들어 있을 수도 있어 코드에서 판단하지 않는다
- 이미 쓰고 있으면 새로 넣지 않는다
- 새로 필요하면 **별도 파일로 만들지, 기존 CSS 파일 안에 넣을지 함께 묻고** `references/css/reset_rw.css`(reset과 global 스타일)를 그 위치에 적용한다

## CSS 모듈 규칙

셀렉터를 어떻게 적을지 정하기 전에 **무엇이 한 단위인지**를 먼저 정한다.
이 단위를 모듈이라 부르고, 셀렉터의 앵커(맨 앞 클래스)는 항상 모듈이다.

- **모듈 = 의미가 하나로 묶이는 영역.** "이건 ○○다" 하고 한 덩이로 부를 수 있으면 모듈이다
- 시안이 아니라 **다 쓴 마크업을 보고 고른다.** 묶음은 대개 이렇게 나와 있다
  - 제목 + 그에 딸린 내용
  - **ul·ol·dl 은 그 자체가 모듈이다.** 안쪽 요소는 목록 클래스를 앵커로 쓴다(ex. .list_notice .date_post)
  - 같은 모양이 반복되는 단위(카드·게시물 행 등)
  - 배경·테두리로 독립한 박스
- 묶음이 아닌 것 — **정렬·간격만 담당하는 래퍼**(제목 줄 `head_*`, 정렬용 묶음 `group_*`, 컨테이너 `inner_*` 계열)
  - **제목을 담고 있어도 그 제목이 바깥 영역 전체를 이름 짓고 있으면, 묶음이 아니라 묶음의 "머리"다.**
    제목과 보조 요소를 한 줄에 놓는 래퍼가 대표적이다 — 제목이 가리키는 건 그 줄이 아니라 바깥 박스다
  - **"모듈이 아니다"가 "마크업에서 지운다"는 뜻은 아니다.** 앵커로 안 쓰는 것과 요소를 없애는 건 별개다.
- **예외 — 앵커가 없으면 모듈로 잡는다.** 의미상 머리 영역이라도 바깥에 쓸 앵커가 섹션 최상위뿐이면
  그 요소를 모듈로 쓴다. 섹션 최상위를 돌려쓰는 것보다 낫다
- **모듈은 모듈을 품을 수 있다.** 내부 요소는 자기를 감싼 **가장 가까운** 모듈에 붙는다
- **앵커 이름은 같은 CSS 파일을 쓰는 페이지 전체에서 한 종류의 모듈만 가리켜야 한다.** 같은 모듈이 여러 번 나오는 건 상관없다
  (ex. 같은 모양의 게시판 영역 둘이 나란히 .area_board 를 쓰는 것). 성격이 다른 모듈에 같은 이름을 쓰면
  스코프가 새므로, 겹치면 이름을 더 구체적으로 짓는다
- **섹션 최상위는 앵커로 돌려쓰지 않는다.** 섹션 안 요소를 전부 section_* 로 묶으면 모듈이 섹션 하나로
  커져서 떼어내 옮길 수 없다. 셀렉터 뎁스가 2로 같아도 의미가 다르다
  ```css
  /* X — 감싼 모듈을 건너뛰고 섹션에 붙였다 */
  .section_news .tit_notice{}
  .section_news .btn_more{}
  .section_news .date_post{}

  /* O — 각자 자기를 감싼 모듈에 붙는다 */
  .area_notice .tit_notice{}
  .area_notice .btn_more{}
  .list_notice .date_post{}
  ```

## 셀렉터 규칙

- 내부 요소는 **자기를 감싼 가장 가까운 모듈을 앵커로 붙여 스코프한다**. 부모를 그대로 반복해 쓰는 flat 형태로 작성하고 중첩 문법은 쓰지 않는다
- 셀렉터 1개는 **최상위 클래스**(ex. .section_news)에만 쓰고 **공통 클래스**(여러 섹션에 걸쳐 쓰는 클래스)는 유효 범위에 맞는 래퍼로 한번 더 스코프한다(사이트 전체 .wrap / 메인 .wrap_main / 서브 콘텐츠 래퍼(ex. .cont_sub) — ex. .wrap_main .tit_main, .wrap .txt_err). 섹션 내부 요소들은 2뎁스가 기본이고, **구조상 반드시 필요한 만큼만** 3~4뎁스까지 늘린다(ex. 항목 상태가 안쪽 요소를 바꾸는 .list_notice li.on .date_post)
- li·dt·dd 처럼 **클래스를 넣지 않는 요소는** 같은 태그가 중첩되어 있는지 확인 후 중첩되어 있다면 반드시 **직접 선택자 `>`** 를 사용한다(ex. .list_news > li.recent). 후손으로 두면 안쪽 목록의 li 까지 잡혀 바깥 항목 스타일이 조용히 샌다
  - 확인은 마크업을 보고 한다 — 그 목록의 li 안에 다른 ul·ol·dl 이 있는지. **공통 컴포넌트를 끼워 넣는 자리도 중첩으로 친다** — 그 컴포넌트가 안에 목록을 품고 있을 수 있다
- 타입/상태 모디파이어 클래스는 기본 클래스에 체이닝(ex. .tag_sort.tag_type1, .tag_approval.on). li 처럼 기본 클래스가 없는 태그는 목록 클래스를 앵커로 잡고 체이닝한다(ex. .list_notice li.on, .list_news > li.recent)
- ID 선택자 금지

## 레이아웃·반응형
- 미디어쿼리는 min-width 사용(모바일 first), 브레이크포인트는 768, 1200, 1400 세 개만 사용.(해당 브레이크포인트를 대체할 scss변수가 프로젝트에 존재한다면 변수로 사용한다)
  - 섹션/컴포넌트 단위로 작성하며, 각 섹션의 일반 셀렉터들 바로 아래에 해당 섹션의 분기만 오름차순으로 작성
  - 여러 섹션의 분기를 파일 하단 하나의 미디어쿼리에 모아 작성하지 않는다(X). - 미디어쿼리 블록 안에도 /* 섹션명 */ 주석을 작성해 가독성을 확보한다.
  - 블록 내부 속성도 1줄 규칙 동일 적용
  ```css
  /* 이용안내 */
  .section_use{padding: 32px 0}
  .section_use .tit_use{font-size: 18px;line-height: 26px}
  @media (min-width: 768px){
    /* 이용안내 */
    .section_use{padding: 44px 0}
  }
  @media (min-width: 1200px){
    /* 이용안내 */
    .section_use .tit_use{font-size: 22px;line-height: 32px}
  }

  /* 미술관소식 */
  .section_news{padding: 48px 0}
  @media (min-width: 1200px){
    /* 미술관소식 */
    .section_news{padding: 72px 0}
  }
  ```
- 콘텐츠 컨테이너는 시안 콘텐츠 너비를 max-width로 고정하고 box-sizing: content-box로 작성해, 좌우 여백은 분기별 padding 오버라이딩으로만 처리한다. 모바일 기본 padding은 시안 기준, 768/1200 분기는 해당 분기 시안의 여백에 맞게 조절, 1400 분기는 스크롤바 폭을 감안해 padding: 0 10px로 오버라이딩. 시안이 없는 분기는 아래 예시 값을 그대로 쓴다(예시에 없는 1200 분기는 따로 두지 않는다)
  ```css
  .wrap .inner_comm{max-width: 1400px;margin: 0 auto;padding: 0 15px;box-sizing: content-box}
  @media (min-width: 768px){
    .wrap .inner_comm{padding: 0 30px}
  }
  @media (min-width: 1400px){
    .wrap .inner_comm{padding: 0 10px}
  }
  ```
- **컨테이너 클래스는 `inner_comm` 하나만 쓴다.** 폭·여백이 다른 섹션이 있어도 `inner_kpi`·`inner_visual` 같은 변형 클래스를 만들지 말고, 그 섹션 클래스로 스코프해 다른 값만 오버라이딩한다(ex. `.section_kpi .inner_comm{max-width: 1640px}`). 변형 클래스를 만들면 분기별 좌우 padding 규칙을 섹션마다 다시 써야 한다
- **grid 트랙은 1단이어도 적는다** — `grid-template-columns: minmax(0, 1fr)` 처럼 쓰고, 유동 트랙도 `minmax(0, …)` 로 쓴다. 트랙을 비우거나 `1fr` 만 쓰면 자식의 한 줄 텍스트(말줄임·nowrap) 폭까지 늘어나 넘친다
- **flex 항목 안에 줄바꿈되지 않는 내용(nowrap·말줄임·고정 폭 자식)이 있으면 `min-width: 0` 을 준다** — 기본값 `min-width: auto` 가 항목을 내용 폭까지 늘려 `flex: 0 0 260px` 같은 고정 폭도 지켜지지 않는다
- **분기에서 display 를 바꾸면(grid → flex 등) 앞 분기의 gap·트랙·정렬 선언이 그대로 남는다** — 새 배치에서 뜻이 달라지는 값은 같은 분기에서 다시 선언한다(ex. 모바일 grid 의 `gap: 20px` → PC flex 에서 `gap: 0`)
- **한글 줄바꿈** — 사이트 공통 CSS 의 `.wrap` 에 `word-break: keep-all;word-wrap: break-word` 를 둔다. 한글은 단어 단위로 줄을 바꾸고, 긴 영문·URL 은 넘치기 전에 끊는다
- **운영 영역 게시물 문구(공지사항 글처럼 운영 중에 입력되는 글)는 `word-break: break-all;word-wrap: break-word`** — 들어올 내용을 미리 알 수 없어 어디서든 끊기게 한다. 한 줄·여러 줄 말줄임으로 보이는 글에도 똑같이 쓴다 — 표시 방식(줄 수·분기)은 바뀌어도 글의 성격은 그대로다

## 속성 선언 순서
flex 축약(flex-grow·flex-shrink·flex-basis 포함)·order → display → flex-direction·flex-wrap·gap·justify-* · align-* → grid-template-*·grid-column·grid-row·grid-area → overflow → float → position·inset·top/right/bottom/left·z-index → width → height → min/max-width → min/max-height → margin → padding → border·border-radius → font(weight → size → line-height → family 순) → color → background → ETC(transform, opacity, visibility, text-overflow, white-space 등 나머지 속성) → content

`·` 로 묶은 속성도 묶음 안에서 적힌 순서대로 쓴다(ex. `display: flex;gap: 8px;justify-content: space-between;align-items: center`)

## 값 표기
- 브라우저 기본값(User Agent Style)과 reset 에서 이미 적용된 속성은 다시 선언하지 않는다. 단 **다른 값으로 되돌리는 오버라이딩**(모디파이어 클래스·미디어쿼리 분기 등)은 필요하므로 선언한다
  - 판단 기준은 **시안이 준 값이 아니라 HTML 에서 고른 태그**다. 시안은 태그를 모른 채 굵기·여백을 주므로, 값을 옮기기 전에 그 클래스가 붙은 태그를 본다
  - 다 쓴 뒤 한 번 대조한다. **reset 이 안 덮는 태그·속성이 UA 기본값과 부딪히는 자리**이므로 거기부터 본다(헤딩 태그의 font-weight 가 대표적)
- !important 금지
- 0 뒤 단위 생략: padding: 0 (예외: flex 축약속성은 단위 유지 → flex: 1 1 0px)
- 소수점 앞 0 생략: opacity: 0.6 (X) → opacity: .6 (O), rgba(0, 0, 0, .6)
- 색상 hex 값은 소문자로 작성하고, 6자리가 모두 같은 문자일 때만 3자리로 축약: #FFFFFF (X) → #fff (O), #ff0000 → #f00으로 축약하지 않고 그대로 사용
- 색상 값이 해당 요소의 글자색과 동일하면 currentColor 사용(ex. color: #121212;border: 1px solid currentColor)
- 크기 단위는 px, % 등 상황에 맞게 판단해 사용
- background 이미지 경로에 따옴표 금지: background: url(https://placehold.co/400x200) 0 0 no-repeat
- font 축약속성 금지, 개별 작성 — ex. font: 700 24px/1.4 Pretendard (X) → font-weight: 700;font-size: 24px;line-height: 34px;font-family: Pretendard (O)
- line-height는 배수 금지, px 값 사용: 1.4 (X) → 34px (O)
- **인라인 요소(a·span)에만 글자 크기·줄 높이를 주지 않는다** — 블록 안에 인라인 하나만 두면 부모 줄 높이가 섞여 줄이 더 높아진다(ex. li 16px/24px 안의 a 19px/23px → 25px). 인라인을 `display: block` 으로 바꾸거나 글자 스타일을 부모에 준다
- **글자 폭에 기대는 여백을 px 로 추정하지 않는다** — 글자로 된 장식(불릿·구분자)은 인라인으로 두면(ex. `::before{content: '• '}`) 폭 계산이 필요 없다. 매달린 들여쓰기처럼 폭이 꼭 필요하면 브라우저에서 잰 값을 쓴다

## CSS 변수
- CSS 변수는 **하나의 값을 바꿀 때 여러 곳이 함께 바뀌어야 하는, 의미로 연결된 값**에만 작성한다(대략 3곳 이상 기준, 함께 바뀌는 값이면 2곳도 허용)
  - 우연히 같은 값이 반복될 뿐인 경우는 변수화하지 않는다
  - **미디어쿼리·테마·모디파이어에서 값이 바뀐다는 이유만으로는 변수화하지 않는다.** 한 곳에서만 쓰는 값은 분기 안에서 속성을 그대로 다시 선언한다(레이아웃·반응형 절 예시처럼)
- CSS 변수는 컴포넌트 최상위 선택자와 동일한 셀렉터를 하나 더 선언하여 변수 전용 블록으로 분리해 작성. 변수 전용 블록은 일반 속성 블록 바로 위에 두고, 변수는 한 줄에 하나씩 개행
  ```css
  .section_visual{
    --visual-gap: 20px;
    --visual-color: #1a1a1a;
  }
  .section_visual{position: relative;padding: 60px 0;background: #f7f8fa}
  ```
- **이미 변수로 만든 값**이 미디어쿼리·테마·모디파이어에서 바뀔 때는 일반 속성을 재선언하지 않고 같은 변수명만 재정의(오버라이딩)한다
  ```css
  @media (min-width: 768px){
    .section_visual{--visual-gap: 32px}
  }
  ```

## 포맷
- 속성은 개행 없이 1줄로 작성: .tit_main{display: flex;align-items: center;padding-bottom: 10px}
- 개행하여 작성된 속성/변수는 값 뒤에 항상 세미콜론을 붙인다
- 쉼표로 셀렉터 그룹핑 시 셀렉터마다 개행
- 섹션/컴포넌트 시작마다 /* 섹션명 */ 주석 작성

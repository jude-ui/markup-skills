# CSS writing Guide
CSS 작성 가이드(Reset·CSS 모듈 규칙·셀렉터·레이아웃/반응형·속성 선언 순서·값 표기·CSS 변수·포맷).

## Reset
reset 은 `reset.css` 같은 별도 파일이 아니라 `common.css`·`layout.css` 등의 안에 섞여 있을 수도 있다. **파일명만 보고 없다고 판단하지 않는다** — 프로젝트가 불러오는 CSS 에서 태그 셀렉터 초기화 선언(ex. `body,ul,li{margin: 0;padding: 0}`·`ul{list-style: none}`·`box-sizing`)을 찾아 판단한다
- 찾았으면 새로 넣지 않는다
- 찾지 못했으면 **사용자에게 묻는다** — 정말 없는지 확인하고, 새로 필요하면 별도 파일로 만들지 기존 CSS 파일 안에 넣을지 함께 묻는다. 정해진 위치에 `references/css/reset_rw.css`(reset과 global 스타일)를 적용한다

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
  - **중첩이 없으면 `>` 를 붙이지 않는다.** 나중에 중첩될지 모른다는 이유의 방어용 `>` 도 쓰지 않는다 — `>` 는 "여기 같은 태그가 중첩돼 있다"는 표시라, 중첩 없이 붙이면 읽는 사람이 없는 구조를 찾게 된다. 마크업에 중첩이 생기면 그때 붙인다. `:has()` 안의 `>` 도 같다
    ```css
    /* X — li 안에 다른 목록이 없는데 붙였다 */
    .list_intro > li{}
    .list_biz:has(> li:hover){}

    /* O */
    .list_intro li{}
    .list_biz:has(li:hover){}
    ```
  - 다 쓴 뒤 `>` 를 쓴 셀렉터마다 마크업에서 중첩을 다시 확인한다
- 타입/상태 모디파이어 클래스는 기본 클래스에 체이닝(ex. .tag_sort.tag_type1, .tag_approval.on). li 처럼 기본 클래스가 없는 태그는 목록 클래스를 앵커로 잡고 체이닝한다(ex. .list_notice li.on, .list_news > li.recent)
- **범위를 좁혀 값을 바꿀 때 원래 규칙의 상태 변화도 유지한다** — `.box_form .txt_desc` 처럼 범위를 붙인 셀렉터는 원래 규칙보다 우선순위가 높아서, 원래 있던 상태·모디파이어 규칙(`.txt_desc.point`, `:disabled`, `[aria-selected="true"]` …)까지 이겨 그 상태 변화가 사라질 수 있다. 시안이 그 상태값을 새로 주면 시안을 따르고, 없으면 아래 순서로 원래 상태 변화를 살린다.
  - 먼저 바꾸려는 속성을 다시 바꾸는 상태 셀렉터를 찾는다 — 상태를 의사 클래스·속성·클래스 중 무엇으로 걸든 같다
    - 같은 요소의 상태 셀렉터면 커스텀 셀렉터와 우선순위를 비교한다. 같으면 나중에 선언된 쪽이 이긴다
    - 상속 속성을 부모의 상태 셀렉터가 바꾸면, 우선순위와 상관없이 자식에 준 값이 이긴다
  - 그 속성이 이미 변수로 되어 있으면 변수만 바꾼다 — 상태 규칙이 다른 변수나 값을 쓰면 손대지 않아도 그대로 작동한다
    - 상태 규칙이 같은 변수를 다시 정하면 바꾼 변수가 그 상태까지 덮을 수 있다. 같은 범위에 상태 셀렉터를 붙여 그 변수의 원래 상태 값을 다시 준다
  - 변수가 아니면 같은 범위에 상태 셀렉터를 붙여 원래 상태 값을 다시 준다. **상태 하나 유지하려고 원래 속성을 변수로 바꾸지 않는다**
  - 다 쓴 뒤 그 상태를 직접 걸어(속성·클래스를 붙여) 원래 상태 모양이 나오는지 확인한다
  ```css
  /* 변수가 아닌 속성 → 같은 범위에서 상태 값을 다시 준다 */
  .txt_desc{color: #000}
  .txt_desc.point{color: #ffcd00}
  .box_form .txt_desc{color: #f00} /* 범위를 좁혀 값을 바꿀 때 */
  .box_form .txt_desc.point{color: #ffcd00}

  /* 이미 변수인 속성 → 변수만 바꾼다 */
  .d_field{background: var(--field-bg)}
  .d_field:disabled{background: var(--field-bg-off)}
  .box_form .d_field{--field-bg: #f6f6f6}

  /* 상태 규칙이 같은 변수를 다시 정할 때 → 같은 범위에서 그 상태의 변수 값도 다시 준다 */
  .btn_more{background: var(--more-bg)}
  .btn_more:hover{--more-bg: #000}
  .box_form .btn_more{--more-bg: #f00}
  .box_form .btn_more:hover{--more-bg: #000}
  ```
- **`:not()`·`:has()` 는 그 요소에 이미 있는 클래스·상태로 표현할 수 있으면 쓰지 않는다** — 기본 셀렉터에 기본 값을, 상태·모디파이어 셀렉터에 바뀌는 값만 주는 방식이 먼저다. `:not()` 은 "아닌 경우"를 뒤집어 읽어야 하고, `:has()` 는 스타일의 근거가 다른 요소에 있어 마크업과 같이 봐야 이해된다. 둘 다 우선순위도 올려서 다음 수정 때 덮어쓰기 어렵다
  - 기본 값은 상태 클래스·속성이 없을 때의 값이다. 마크업에 처음부터 붙어 나가는 상태(ex. 기본 펼침 `.active`)여도 그 값은 상태 셀렉터에 준다
  ```css
  /* X */
  .tab_menu li a{color: #000}
  .tab_menu li:not(.on) a{color: #666}

  /* O */
  .tab_menu li a{color: #666}
  .tab_menu li.on a{color: #000}
  ```
  - 형제 사이 간격·구분선이나 앞뒤 요소에 따른 변화는 `gap`, 결합자(`+`·`~`), 구조 의사 클래스(`:first-child`·`:last-child`), `:focus-within` 으로 먼저 잡는다
    (X `li:not(:last-child){margin-bottom: 10px}` / O `li + li{margin-top: 10px}` 또는 부모에 `gap`)
  - `:not()` 을 쓰는 경우
    - 상태를 긍정형으로 쓰는 셀렉터가 없을 때(ex. 값이 입력됨 `:not(:placeholder-shown)`)
    - 상태가 걸린 쪽 값을 여기서 따로 정하지 않고 공통 규칙·컴포넌트·브라우저 기본값으로 돌아가기만 할 때 — 상태 셀렉터에 되돌리는 값을 쓰면 그 값을 베끼게 되고, 원래 규칙이 바뀌어도 따라가지 못한다(ex. 버튼 묶음에서 마지막이 아닌 버튼의 오른쪽 radius 없애기 — radius 가 버튼 크기마다 다르다 / 접힌 메뉴에만 붙는 타일 모양 — 펼치면 공통 트리 모양으로 돌아간다)
  - `:has()` 를 쓰는 경우 — 바뀌는 근거가 다른 요소에 있을 때. 그 요소의 상태(ex. 자식에 hover·체크·입력하면 부모가 바뀜)든 유무·종류(ex. 삭제 버튼이 있는 칩)든 같다. 부모에 모디파이어를 따로 붙이면 두 곳을 맞춰야 하니 `:has()` 로 읽는다
    - 조건은 그 뜻으로만 쓰이는 클래스로 건다 — 여러 자리에 쓰이는 컴포넌트·태그(`:has(.d_btn)`, `:has(img)`)로 걸면 나중에 다른 이유로 들어온 요소에도 걸린다
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
- **컨테이너 클래스는 페이지 종류마다 하나만 쓴다** — 메인은 `inner_comm`. 서브는 시안의 콘텐츠 최대 너비가 메인과 같으면 `inner_comm` 을 함께 쓰고, 다르면 서브 전용 `inner_sub` 를 따로 만든다. `inner_sub` 의 분기별 padding 도 위 항목과 같은 방식으로 따로 적는다
- **두는 곳** — `inner_comm` 은 사이트 공통 CSS, `inner_sub` 는 서브 페이지 CSS
- **같은 페이지 종류 안에서 폭·여백이 다른 섹션은 변형 클래스를 만들지 않는다** — `inner_kpi`·`inner_visual` 대신 섹션 클래스로 스코프해 다른 값만 덮는다(ex. `.section_kpi .inner_comm{max-width: 1640px}`). 변형 클래스를 만들면 분기별 좌우 padding 을 섹션마다 다시 써야 한다
- **어느 분기에서 다단이 되는 목록은 모바일부터 `display: grid;gap` 과 항목 `min-width: 0` 을 두고, 다단이 되는 분기에서 `grid-template-columns` 를 적는다** — 모바일 1단에는 트랙을 적지 않는다. `min-width: 0` 이 없으면 1단 grid 도 말줄임·nowrap 글 폭까지 늘어나 넘치고, 다단에서는 칸 폭이 어긋난다. block 으로 시작하면 다단 분기에서 display 전환·형제 margin 되돌리기·gap 추가가 따라붙는다
- **끝까지 1단인 목록은 grid·flex 를 걸지 않고 기본 흐름(block)으로 둔다** — 항목 간격은 `li + li{margin-top: …}`
- **flex 는 줄어들어야 하는 항목(글·nowrap·말줄임을 담은 쪽)에만 `min-width: 0` 을 준다** — 기본값 `min-width: auto` 가 항목을 내용 폭까지 늘려 `flex: 0 0 260px` 같은 고정 폭도 지켜지지 않는다. 버튼처럼 라벨 폭을 지켜야 하는 항목에 주면 라벨보다 좁게 찌그러진다
- **분기에서 display 를 바꾸면(grid → flex 등) 앞 분기의 gap·트랙·정렬 선언이 그대로 남는다** — 새 배치에서 뜻이 달라지는 값은 같은 분기에서 다시 선언한다(ex. 모바일 grid 의 `gap: 20px` → PC flex 에서 `gap: 0`)
- **장식(의사 요소·배경 그림) 위로 내용을 올리는 `position`·`z-index` 는 실제로 겹치는 요소에만 준다** — 렌더된 두 요소의 영역이 겹치는지 분기마다 확인하고, 겹칠 것 같다는 추측으로 형제마다 넣지 않는다. 블러·그림자처럼 퍼지는 장식은 눈에 보이는 범위까지를 영역으로 친다. 쌓임 맥락을 새로 만드는 `isolation` 은 쓰지 않는다
- **이미지 자리(img 또는 이미지 틀)는 모든 분기에서 시안 비율의 `aspect-ratio` 나 고정 너비·높이를 준다** — 운영 중 원본 비율이 다른 이미지가 들어와도 자리 크기가 그대로여야 한다. 비율 없이 `height: auto` 로 원본에 맡기거나, 분기에서 `aspect-ratio: auto` 로 풀지 않는다
  - 카드 높이에 맞춰 늘어나야 하는 사진도 틀에 시안 비율을 준다 — flex 의 stretch 가 비율보다 우선이라 글이 길면 늘어나고, 짧으면 비율 높이가 최소로 남는다
  - 분기에서 `height` 를 px 로 고정했으면 `aspect-ratio: auto` 로 덮지 말고 기본 비율 선언을 그대로 둔다
  - 다 쓴 뒤 이미지 src 를 비율이 다른 파일로 바꿔 넣어도 자리 크기가 그대로인지 확인한다
- **한글 줄바꿈** — 사이트 공통 CSS(모든 페이지가 불러오고, 파일 이름도 `common` 처럼 공통을 뜻하는 CSS)의 `.wrap` 에 `word-break: keep-all;word-wrap: break-word` 를 둔다. 한글은 단어 단위로 줄을 바꾸고, 긴 영문·URL 은 넘치기 전에 끊는다
- **운영 영역 게시물 문구(공지사항 글처럼 운영 중에 입력되는 글)는 `word-break: break-all;word-wrap: break-word`** — 들어올 내용을 미리 알 수 없어 어디서든 끊기게 한다. 한 줄·여러 줄 말줄임으로 보이는 글에도 똑같이 쓴다 — 표시 방식(줄 수·분기)은 바뀌어도 글의 성격은 그대로다

## 속성 선언 순서
flex 축약(flex-grow·flex-shrink·flex-basis 포함)·order → display → flex-direction·flex-wrap·gap·justify-* · align-* → grid-template-*·grid-column·grid-row·grid-area → overflow → float → position·inset·top/right/bottom/left·z-index → width → height → min/max-width → min/max-height → margin → padding → border·border-radius → font(weight → size → line-height → family 순) → color → background → ETC(transform, opacity, visibility, text-overflow, white-space 등 나머지 속성) → content

`·` 로 묶은 속성도 묶음 안에서 적힌 순서대로 쓴다(ex. `display: flex;gap: 8px;justify-content: space-between;align-items: center`)

## 값 표기
- 속성을 선언하기 전에 **그 요소에 이미 적용된 값**을 확인하고, 같은 값이면 선언하지 않는다(ex. h2 의 `display: block` 은 UA 값과 같아 선언하지 않고, 시안의 `font-weight: 400` 은 UA 값 bold 와 달라 선언한다)
  - **상속 속성(color·font 계열·line-height·letter-spacing·word-break·text-align 등)은 부모에서 물려받은 값도 이미 적용된 값이다.** 상속되지 않는 속성은 한 곳만 확인하면 되지만, 상속 속성은 부모·부모의 상태 클래스·분기에 따라 물려받는 값이 달라지므로 그 경우들을 모두 본다
  - 부모나 분기에 따라 하나라도 다르면 기본 셀렉터에 선언을 남긴다(ex. PC 분기에서 부모만 18px 로 커져도 `.section_intro .desc{font-size: 16px}`)
  - 부모에 상태 클래스가 붙었을 때만 다르면 기본 셀렉터에는 쓰지 않고, 그 상태 셀렉터에서 되돌린다(ex. 탭이 켜져도 숫자는 회색 → `.tab.on .num{color: #666}`)
- !important 금지
- 0 뒤 단위 생략: padding: 0 (예외: flex 축약속성은 단위 유지 → flex: 1 1 0px)
- 소수점 앞 0 생략: opacity: 0.6 (X) → opacity: .6 (O), rgba(0, 0, 0, .6)
- 색상 hex 값은 소문자로 작성하고, 6자리가 모두 같은 문자일 때만 3자리로 축약: #FFFFFF (X) → #fff (O), #ff0000 → #f00으로 축약하지 않고 그대로 사용
- 색상 값이 해당 요소의 글자색과 동일하면 currentColor 사용(ex. color: #121212;border: 1px solid currentColor)
- 크기 단위는 px, % 등 상황에 맞게 판단해 사용
- background 이미지 경로에 따옴표 금지: background: url(https://placehold.co/400x200) 0 0 no-repeat
- font 축약속성 금지, 개별 작성 — ex. font: 700 24px/1.4 Pretendard (X) → font-weight: 700;font-size: 24px;line-height: 34px;font-family: Pretendard (O)
- line-height는 배수 금지, px 값 사용: 1.4 (X) → 34px (O)
  - **시안이 행간을 정해 주지 않아 직접 고를 때** — 짝수 px 로 쓴다. 범위는 글자 크기 20px 미만 1.4~1.5배, 20px 이상(제목급) 1.2~1.3배이고, 값은 `글자 크기 × 범위 가운데 배수(1.45·1.25)` 에 가장 가까운 짝수다(두 짝수의 한가운데면 큰 쪽). 범위 안에 짝수가 있으면 그중 하나가, 없으면 범위에 가장 가까운 짝수가 나온다(ex. 16px → 24px, 13px → 18px, 20px → 26px, 40px → 50px)
- **인라인 요소(a·span)에만 글자 크기·줄 높이를 주지 않는다** — 블록 안에 인라인 하나만 두면 부모 줄 높이가 섞여 줄이 더 높아진다(ex. li 16px/24px 안의 a 19px/23px → 25px). 인라인을 `display: block` 으로 바꾸거나 글자 스타일을 부모에 준다
- **목록의 불릿은 매달린 들여쓰기로 만든다** — `li{position: relative;padding-left: …}` + `li::before{position: absolute;left: 0}`. 줄이 바뀌어도 둘째 줄이 본문 첫 글자에 맞는다. 지금 한 줄이어도 적용한다(좁은 폭·운영 문구에서 줄이 바뀐다)
  - **시안이 글자 불릿(`• ` 등)이면 글자를 그대로 쓴다** — `content: '•'`;`top: 0`. 본문의 폰트·line-height 를 물려받아 세로 위치는 계산하지 않는다. `padding-left` 는 불릿 글자와 뒤 공백의 폭으로, 피그마 메타데이터로 읽을 수 없으니 브라우저에서 잰 값을 쓴다(px 로 추정하지 않는다)
  - **시안이 도형 불릿이면 CSS 로 그린다** — 크기·모양은 시안 값, 세로 위치는 `top: calc({line-height} / 2);transform: translateY(-50%)`, `padding-left` 는 시안 좌표의 불릿 폭 + 간격
- **목록이 아닌 글자 장식(한 줄 안의 구분자 `|`·`·` 등)은 인라인으로 둔다** — 폭 계산이 필요 없다

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

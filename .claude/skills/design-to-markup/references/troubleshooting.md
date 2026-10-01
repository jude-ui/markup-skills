# 대조에서 자주 나오는 문제와 조치

읽기 스킬의 대조(시안 폭, 좁은 폭·중간 폭)에서 문제를 찾았을 때의 원인과 고치는 법.

## 넘침
- 원인 1순위 — **grid/flex 자식의 `min-width: auto`**. 자식의 min-content(긴 제목 + `padding-right`, `word-break: keep-all` 로 안 쪼개지는 긴 단어)가 트랙보다 크면 트랙을 밀어낸다
- 조치 — `create-html-css-code` css-writing-guide 레이아웃·반응형 절의 grid 트랙·flex `min-width` 규칙대로 고친다. 그래도 넘치면 좁은 분기에서 **min-content 자체**(제목 크기·padding)를 줄인다

## 찌그러짐
- 원인 1순위 — **`left`/`right` 한쪽만 지정한 absolute 요소의 shrink-to-fit** 에, 그 안의 이미지에 걸린 **`max-width: 100%`** 가 겹친 경우. `max-width: 100%` 가 걸린 이미지는 min-content 기여가 0 이라 하한이 사라져 **세로로 늘어난다**
- `img{max-width: 100%}` 는 프로젝트의 리셋·전역 CSS 에 따라 있을 수도 없을 수도 있다 — 원인으로 단정하기 전에 계산 스타일로 실제로 걸려 있는지 확인한다
- 조치 — 그 이미지에 **`max-width: none`**. 컨테이너에 `width` 를 박는 건 원인 제거가 아니다

## 배치 전제가 깨진 값
가로 배치를 전제한 예외값이 세로로 쌓이는 분기까지 따라가 있으면 `translating.md` 의 "배치에 종속된 값" 대로 좁은 분기에서 되돌린다.

## 시안에 없는 폭에서 줄바꿈이 달라짐
`translating.md` 의 "줄바꿈" — `<br>` 대신 텍스트 폭으로 맞춘다.

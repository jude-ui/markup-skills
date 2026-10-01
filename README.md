# markup-skills

HTML/CSS 퍼블리싱 스킬 4개를 담은 저장소입니다. 스킬은 `.claude/skills/` 에 들어 있고, 폴더를 그대로 읽어 씁니다.

## 들어 있는 스킬

| 스킬 | 하는 일 |
|---|---|
| `create-html-css-code` | HTML/CSS 를 쓸 때의 규칙(구조·네이밍·CSS 작성) |
| `design-to-markup` | 시안(피그마·이미지)을 마크업으로 옮기는 흐름. 읽기·쓰기 스킬을 이어 쓴다 |
| `reading-figma` | 피그마 시안의 구조·수치·색·에셋 읽기, 구현 결과 대조 |
| `reading-img` | 이미지 시안(PNG/JPG) 픽셀 실측, 구현 결과 대조 |

`design-to-markup` 이 나머지 세 스킬을 이름으로 불러 쓰므로, 다른 곳에 가져갈 때는 네 폴더를 함께 가져가야 합니다.

## 쓰는 법

- **이 저장소에서 작업할 때** — 저장소를 열면 `.claude/skills/` 의 스킬이 그대로 잡힙니다.
- **다른 프로젝트에서 쓸 때** — `.claude/skills/` 의 네 폴더를 그 프로젝트의 `.claude/skills/` 로 복사합니다.
- **모든 프로젝트에서 쓸 때** — 네 폴더를 `~/.claude/skills/` 로 복사합니다.

스킬 문서를 고친 뒤에는 새 세션을 열면 반영됩니다.

## 구조

```
.claude/skills/
├── create-html-css-code/   SKILL.md · references/(가이드·CSS/HTML 샘플) · scripts/
├── design-to-markup/       SKILL.md · references/
├── reading-figma/          SKILL.md · references/
└── reading-img/            SKILL.md · references/(measure.py 포함)
```

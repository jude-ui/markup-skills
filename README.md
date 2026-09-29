# markup-skills

HTML/CSS 퍼블리싱 스킬을 묶은 Claude 플러그인 `markup` 과 그 마켓입니다. 이 폴더를 로컬 마켓으로 등록해 씁니다.

## 들어 있는 스킬

| 스킬 | 하는 일 |
|---|---|
| `markup:create-html-css-code` | HTML/CSS 를 쓸 때의 규칙(구조·네이밍·CSS 작성) |
| `markup:design-to-markup` | 시안(피그마·이미지)을 마크업으로 옮기는 흐름. 읽기·쓰기 스킬을 이어 쓴다 |
| `markup:reading-figma` | 피그마 시안의 구조·수치·색·에셋 읽기, 구현 결과 대조 |
| `markup:reading-img` | 이미지 시안(PNG/JPG) 픽셀 실측, 구현 결과 대조 |

## 연결하기

Claude Code 세션에서 이 폴더를 로컬 마켓으로 등록하고 플러그인을 설치합니다.

```
/plugin marketplace add <이 폴더의 경로>
/plugin install markup@markup-skills
```

- 로컬 마켓의 플러그인은 이 폴더를 그대로 읽습니다. 스킬 문서를 고친 뒤 새 세션을 열거나 `/reload-plugins` 를 실행하면 바로 반영됩니다.
- 한 프로젝트에서만 쓰려면 그 프로젝트 폴더에서 local 범위로 등록·설치합니다. 셸에서는 두 명령에 `--scope local` 을 붙입니다(`claude plugin marketplace add <경로> --scope local`, `claude plugin install markup@markup-skills --scope local`).
- GitHub 주소(`jude-ui/markup-skills`)로 등록할 수도 있습니다. 이때는 복사본을 받아 쓰므로, 바꾼 내용을 보내려면 `plugins/markup/.claude-plugin/plugin.json` 의 `version` 을 올려 푸시해야 합니다.

## 구조

```
.claude-plugin/marketplace.json             마켓 정보(이름 markup-skills)
plugins/markup/.claude-plugin/plugin.json   플러그인 정보(이름 markup, 버전)
plugins/markup/skills/                      스킬 문서
```

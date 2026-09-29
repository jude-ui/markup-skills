---
name: reading-img
description: "PNG/JPG 이미지 시안만 주어졌을 때 폰트·색·테두리·radius·이미지 배치 값을 픽셀로 실측하고, 구현 결과를 시안과 대조할 때 사용. 시안을 마크업으로 옮기는 작업은 design-to-markup 이 이 스킬을 불러 쓴다. 코드 작성 규칙은 담지 않는다."
---

# reading-img

이미지 시안에 **무엇이 있는지 재서 알아내는 법**만 담는다.

```
읽기   reading-img (이 스킬)        시안에 무엇이 있는지 알아낸다
흐름   design-to-markup            알아낸 것을 코드로 어떻게 바꿀지 정한다
쓰기   create-html-css-code        바꾼 코드를 어떤 스타일로 적을지 정한다
```

## 읽는 순서
1. **실측** — `references/reading-img.md` 의 절차(패스 0~2)·공통 규칙·§0~§7
2. **구현과 대조** — 마크업을 만든 뒤 `references/reading-img.md` §8

측정 도구는 `references/measure.py` 다. 스크래치패드에 복사해 `from measure import *` 로 쓰고, 측정 로직을 새로 타이핑하지 않는다.

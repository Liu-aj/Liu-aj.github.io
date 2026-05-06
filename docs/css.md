---
title: CSS 指南
description: CSS 样式指南
---

# CSS 指南 🎨

> 网页样式设计

---

## 选择器

| 选择器 | 示例 |
|--------|------|
| 元素 | p { } |
| 类 | .class { } |
| ID | #id { } |
| 属性 | [attr] { } |
| 后代 | .parent .child { } |
| 伪类 | :hover { } |

## Flexbox

```css
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
}
```

## Grid

```css
.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
}
```

## 响应式

```css
@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
}
```

---

*CSS 让网页更美观*

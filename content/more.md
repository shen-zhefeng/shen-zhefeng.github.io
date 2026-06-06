+++
title = "More"
[extra]
no_header = true
+++

# Template Reference

Quick reference for all features in this template.
For the **exhaustive** version with every pattern, see `content/test.md` (preview with `zola serve --drafts`).

---

## Markdown Basics

### Text Formatting
**Bold** uses `**double asterisks**`. *Italic* uses `*single asterisks*`. `Inline code` uses `` `backticks` ``.

### Horizontal Rule
Three dashes on a blank line create a horizontal rule:

```
---
```

Looks like this:

---

### Lists

Ordered (numbered):
1. First item
2. Second item
   1. Nested item
   2. Another nested

Unordered (bullets):
- Bullet one
- Bullet two

### Links
- [Internal page link](/about)
- [External link](https://example.com)
- [PDF download](/sample.pdf)

---

## Math (KaTeX)

Write `$...$` for inline, `$$...$$` for display math.  
Escape `_` as `\_` inside math (e.g., `$\GL\_n$`) — Zola's Markdown parser treats bare `_` as italics.

### Inline
$f$ on $\GL\_n(\mathbb{A}\_\mathbb{Q})$

### Display
$$\zeta(s) = \sum_{n=1}^\infty \frac{1}{n^s}$$

### Common Symbols

| You type | Result |
|---|---|
| `\mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}` | $\mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ |
| `\sum, \prod, \int` | $\sum, \prod, \int$ |
| `\leq, \geq, \cong` | $\leq, \geq, \cong$ |
| `\alpha, \beta, \Gamma` | $\alpha, \beta, \Gamma$ |

---

## Expandable Blocks

### Basic (click to show/hide)
{% expandable(trigger="Click for abstract") %}
Hidden content with **Markdown** and [links](https://example.com).
{% end %}

### No underline
{% expandable(trigger="Plain text trigger", underline=false) %}
The trigger link above has no dashed border.
{% end %}

### With header (line above trigger)
{% expandable(trigger="Click for theorem", header="**Theorem.** Your statement here.") %}
Explanation or proof of the theorem.
{% end %}

---

## Toggle & Toggle-Block

Click this toggle — {% toggle(id="ref1", text="Show details") %} — to reveal content.

{% toggle-block(id="ref1") %}
This block appears/disappears. Supports **Markdown**.
{% end %}

---

## Inline Expandable (popover)

Text with an {% inline_expandable(trigger="inline note") %} extra info floating right here. {% end %} in the middle of a sentence.

---

## Syntax Highlighting (`dark-plus` theme)

### Python
```python
def prime_sieve(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for m in range(p * p, n + 1, p):
                is_prime[m] = False
    return [p for p in range(2, n + 1) if is_prime[p]]
```

### LaTeX
```latex
\documentclass{amsart}
\usepackage{amsmath, amssymb}
\newcommand{\GL}{\operatorname{GL}}
```

### Bash
```bash
zola serve           # live preview
zola build           # production build
zola check           # check links
```

### TOML
```toml
[markdown.highlighting]
theme = "dark-plus"
```

---

## Tables

| Header A | Header B |
|---|---|
| Cell 1 | Cell 2 |
| Cell 3 | Cell 4 |

---

## Blockquotes

> Mathematics is the art of giving the same name to different things.
> &mdash; Henri Poincar&eacute;

---

## Native `<details>` (no JavaScript)

<details>
<summary>Click to expand</summary>

This uses the browser's built-in expand/collapse. No JavaScript.
Works everywhere.

</details>

---

## Unicode Symbols (no LaTeX needed)

For simple symbols, you can use HTML entities or paste directly:

`&rarr;` → &rarr; `&le;` → &le; `&infin;` → &infin;  
Subscripts: `GL<sub>n</sub>` → GL<sub>n</sub>

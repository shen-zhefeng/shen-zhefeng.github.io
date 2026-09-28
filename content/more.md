+++
title = "More"
[extra]
no_header = true
+++

This site is a personal website template, built with a modified [zola-sam](https://github.com/janbaudisch/zola-sam) theme
(a Zola port of [hugo-theme-sam](https://github.com/victoriadrake/hugo-theme-sam)).
Source code: [GitHub](https://github.com/shen-zhefeng/shen-zhefeng.github.io).

Developed using [OpenCode](https://opencode.ai/) with [DeepSeek](https://www.deepseek.com/) models and [Codex](https://openai.com/codex/) with [GPT](https://chatgpt.com/) models.

---

# Template Reference

Quick reference for all features in this template.
For the **exhaustive** version with every pattern, see `content/test.md` (preview with `zola serve --drafts`).

---

## Markdown Basics

### Text Formatting
**Bold** uses `**double asterisks**`. *Italic* uses `*single asterisks*`. `Inline code` uses `` `backticks` ``.

Leave a blank line between paragraphs. This also works inside expandable blocks and blockquotes.

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
Inline formulas look like $f$ on $\GL\_n(\mathbb{A}\_\mathbb{Q})$.

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

A blank line starts a separate paragraph, for example to explain the main result after an introduction.
{% end %}

### No underline
{% expandable(trigger="Plain text trigger", underline=false) %}
The trigger link above has no underline.
{% end %}

### With header (line above trigger)
{% expandable(trigger="Click for theorem", header="**Theorem.** Your statement here.") %}
Explanation or proof of the theorem.
{% end %}

---

## `<details>` (native expandable)

Use the browser's built-in `<details>` element — no JavaScript needed.

<details>
<summary>Click to expand</summary>

Hidden content with **Markdown** support.

</details>

---

## Inline Expandable (popover)

Text with an {% inline_expandable(trigger="inline note") %} extra info floating right here. {% end %} in the middle of a sentence.

The note supports Markdown, including links and lists. Click the trigger or the note content to close it, or press Escape. Use a block expandable or native `<details>` when the content should expand in the page layout.

---

## Toggle a Separate Block

{{ toggle(text="Show or hide a separate note", id="quick-reference-note") }}

<div id="quick-reference-note" style="display: none;">

This note uses **Markdown** and is controlled by the trigger above. Press Tab to focus the trigger, then Enter or Space to open or close it.

</div>

The `toggle` shortcode takes `text` for its label and `id` for the target block. Match the target's HTML `id`, and use a different target ID for each independent note. See the README for a complete source example.

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

If a table is wider than the available space, scroll it sideways to see the remaining columns. The surrounding page keeps its normal width.

---

## Blockquotes

> Mathematics is the art of giving the same name to different things.
> &mdash; Henri Poincar&eacute;

---

## Native `<details>` (no JavaScript)

### Plain (no extra class)
<details>
<summary>Click to expand</summary>
This uses the browser's built-in expand/collapse. No JavaScript.
</details>

### Styled (`expand-box` class)
<details class="expand-box">
<summary>Click to expand</summary>
<div class="expand-content">

Add `class="expand-box"` for themed styling (border, +/- icon, themed background).
Works with **Markdown**, tables, lists, etc.

This is a separate paragraph with a [research link](@/research.md). The content and its links adapt to the box's background in both themes.

</div>
</details>

> The `expand-box` class adapts to light/dark mode using CSS custom properties.
> Use `<div class="expand-content">` inside to get the themed content background.
> Leave blank lines around the Markdown body so that formatting is rendered.

---

## Unicode Symbols (no LaTeX needed)

For simple symbols, you can use HTML entities or paste directly:

`&rarr;` → &rarr; `&le;` → &le; `&infin;` → &infin;  
Subscripts: `GL<sub>n</sub>` → GL<sub>n</sub>

+++
title = "Test"
draft = true
[extra]
no_header = true
+++

# Test Page: Feature Reference

This page demonstrates all features available in this Zola template.
Use it as a reference when building your own academic website.

**Live preview**: `zola serve --drafts` → `http://127.0.0.1:1111/test/`

---

## Research: Expandable Abstracts

{% expandable(trigger="On the distribution of prime geodesics (2024)") %}
**Abstract.** We study the equidistribution of prime geodesics on hyperbolic surfaces,
generalizing the Selberg trace formula to the setting of GL<sub>2</sub> over a number field.
[arXiv:xxxx.xxxxx](https://arxiv.org)

This second paragraph should start on its own line with space above it. See the [research page](@/research.md) for related work.
{% end %}

{% expandable(trigger="L-functions and automorphic forms (2023)", underline=false) %}
**Abstract.** We establish new bounds for automorphic L-functions on GL<sub>n</sub>
using the theory of Eisenstein series and spectral methods.
[J. Number Theory](https://example.com)
{% end %}

### Expandable with Header

{% expandable(trigger="Click to see theorem", header="**Theorem** (Prime Number Theorem)") %}
Let &pi;(x) denote the number of primes &le; x. Then
&pi;(x) &sim; x / log x as x &rarr; &infin;.
{% end %}

---

## Math (KaTeX)

### Inline Math

The Riemann zeta function $\zeta(s) = \sum_{n=1}^\infty \frac{1}{n^s}$ for $\Re(s) > 1$.

An automorphic form $f$ on $\GL\_n(\mathbb{A}\_\mathbb{Q})$ satisfies $f(\gamma g k) = f(g)$ for $\gamma \in \GL\_n(\mathbb{Q})$, $k \in K\_\infty$.

### Display Math

$$\zeta(s) = \prod_{p \text{ prime}} \left(1 - \frac{1}{p^s}\right)^{-1}$$

$$\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}$$

$$L(s, \chi) = \sum_{n=1}^\infty \frac{\chi(n)}{n^s}$$

### Number Fields

Let $K/\mathbb{Q}$ be a number field of degree $n = [K:\mathbb{Q}]$.

$$\zeta_K(s) = \sum_{\mathfrak{a} \neq 0} \frac{1}{N(\mathfrak{a})^s}$$

### Modular Forms

$$f(z) = \sum_{n=0}^\infty a_n e^{2\pi i n z}, \qquad \Im(z) > 0$$

### Common Math Symbols

| LaTeX | Rendered |
|---|---|
| `$\mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$` | $\mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ |
| `\mathcal{O}_K, \mathfrak{p}, \mathfrak{m}` | $\mathcal{O}\_K, \mathfrak{p}, \mathfrak{m}$ |
| `\sum, \prod, \int, \partial` | $\sum, \prod, \int, \partial$ |
| `\infty, \to, \mapsto, \hookrightarrow` | $\infty, \to, \mapsto, \hookrightarrow$ |
| `\otimes, \oplus, \cong, \simeq` | $\otimes, \oplus, \cong, \simeq$ |
| `\leq, \geq, \neq, \equiv` | $\leq, \geq, \neq, \equiv$ |
| `\sqrt{2}, \frac{a}{b}, \binom{n}{k}` | $\sqrt{2}, \frac{a}{b}, \binom{n}{k}$ |
| `\alpha, \beta, \gamma, \Gamma` | $\alpha, \beta, \gamma, \Gamma$ |
| `\varepsilon, \varphi, \varnothing` | $\varepsilon, \varphi, \varnothing$ |

### Delimiters

| Syntax | Mode |
|---|---|
| `$\zeta(s)$` | Inline math |
| `$$\sum_{n=1}^\infty$$` | Display math |

---

## Teaching: Tables & Lists

### Course Schedule

| Semester | Course | Role | Notes |
|---|---|---|---|
| 2025 Spring | MATH 101: Calculus I | Teaching Assistant | Section 3 |
| 2025 Spring | MATH 201: Linear Algebra | Teaching Assistant | Section 1 |
| 2024 Autumn | MATH 301: Abstract Algebra | Instructor | — |

### Wide Table on a Narrow Screen

The deliberately long reference below checks horizontal scrolling. Narrow the window: scroll the table to read its final column while the rest of the page stays in place. Also check that the last column remains reachable using the keyboard.

| Topic | Unbroken reference | Notes |
|---|---|---|
| [Research](@/research.md) | `NT2026ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ` | Final column |

### Office Hours

1. Monday 14:00&ndash;16:00
2. Wednesday 10:00&ndash;12:00
3. {% inline_expandable(trigger="by appointment") %}
Email to schedule. Available Friday afternoons.
{% end %}

---

## Talks & Blockquotes

> **"Beyond Endoscopy: New Directions"**  
> Number Theory Seminar, University of Example, March 2025

> **"Prime Geodesic Theorem for Cocompact Lattices"**  
> Joint Mathematics Meetings, January 2025

> Mathematics is the art of giving the same name to different things.
> &mdash; Henri Poincar&eacute;

> **Research note.** This quoted paragraph contains a [research link](@/research.md).
>
> This second paragraph should stay separate. Check that the link above remains readable in light and dark mode, including while hovered or focused with Tab.

---

## Syntax Highlighting (`dark-plus` theme)

### Python

```python
def prime_sieve(n: int) -> list[int]:
    """Return all primes ≤ n using the Sieve of Eratosthenes."""
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
    return [p for p in range(2, n + 1) if is_prime[p]]
```

### Rust

```rust
fn mod_pow(mut a: u64, mut e: u64, m: u64) -> u64 {
    let mut result = 1u64;
    a %= m;
    while e > 0 {
        if e & 1 == 1 {
            result = (result as u128 * a as u128 % m as u128) as u64;
        }
        e >>= 1;
        a = (a as u128 * a as u128 % m as u128) as u64;
    }
    result
}
```

### LaTeX

```latex
\documentclass{amsart}
\usepackage{amsmath, amssymb, amsthm}
\newcommand{\GL}{\operatorname{GL}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\Q}{\mathbb{Q}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
```

### Bash

```bash
zola serve           # live preview
zola serve --drafts  # include draft pages
zola build           # production build to public/
zola check           # check internal and external links (requires network)
./test.sh            # production + isolated draft build, links, navigation checks
```

### TOML (config)

```toml
[markdown.highlighting]
theme = "dark-plus"
style = "inline"
```

---

## Shortcode Reference

### `expandable` (block-toggle)

{% expandable(trigger="Click to show hidden content") %}
Hidden content with **Markdown**, [links](https://example.com), and lists:

- item one
- item two
{% end %}

{% expandable(trigger="No underline variant", underline=false) %}
The trigger link above has no underline.
{% end %}

### `<details>` (native expandable)

Use the browser's built-in element — no JavaScript needed.

<details>
<summary>Click to expand</summary>

This content expands and collapses with **zero** JavaScript.

- Works everywhere
- Accessible by default

</details>

### `inline_expandable` (inline popover)

This sentence has an {% inline_expandable(trigger="inline popover") %}
This floating note supports **Markdown** and [links](https://example.com). Click the note or the trigger to close it, or press Escape.
{% end %} right here.

#### Long note near the end of a line

The text surrounding this trigger should remain in a single flowing paragraph, including on a narrow screen: {% inline_expandable(trigger="read a longer note") %}
**A longer note.** This first paragraph checks that the background and border grow to contain the text. Narrow the browser window, or rotate a phone to landscape, and open the note again.

This second paragraph should remain inside the note too. It includes inline mathematics, $\GL\_n(\mathbb{Q})$, and a [link to the research page](@/research.md).

- A first point with **bold emphasis**.
  1. A nested numbered point.
     - A [third-level research link](@/research.md) keeps its full color.
- A second point with enough text to wrap onto several lines in a narrow window. Every line should stay within the note's background, and scrolling should keep the content reachable.
- A final point with `inline code`.

If the table below is wider than this note, it should scroll sideways within the note. The note itself should still scroll vertically to reach the text after the table.

| Topic | Unbroken reference | Notes |
|---|---|---|
| [Research](@/research.md) | `NOTE2026ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ` | Last column |

Close this note with its trigger, by clicking its content, or with Escape. The words after the trigger should keep their place in the sentence.
{% end %} and then the sentence continues normally.

### `toggle` (a separate block)

{{ toggle(text="Show or hide the shared note", id="test-shared-note") }}

<div id="test-shared-note" style="display: none;">

**One note, two triggers.** Both triggers below and above this block should report the same open or closed state.

- Click either trigger to change visibility.
- Focus either trigger with Tab, then press Enter or Space.
- Space should operate the trigger without scrolling the page.

</div>

{{ toggle(text="A second trigger for the same note", id="test-shared-note") }}

Use the same `id` in both `toggle` shortcodes and the target's HTML `id`. Give each independent target a unique ID.

#### Initially visible target

{{ toggle(text="Hide or show the visible note", id="test-visible-note") }}

<div id="test-visible-note">

This target starts visible. Its trigger should announce an expanded state before the first click, and should close it on the first activation.

</div>

---

## HTML `<details>` (browser-native)

<details>
<summary>Click to expand (native HTML)</summary>

No JavaScript required. Built into all modern browsers.

| Feature | Authoring note |
|---|---|
| No JS dependency | Use blank lines around the Markdown body |
| Native keyboard operation | The browser supplies the default disclosure marker |

</details>

### Styled native details

<details class="expand-box">
<summary>Open the themed Markdown example</summary>
<div class="expand-content">

Add `class="expand-box"` to `<details>` and use an `expand-content` div for the content background. Keep blank lines around this Markdown body.

This text contains **bold**, *italic*, and a [research link](@/research.md).

- Lists should be formatted as lists.
- Hover the summary in both light and dark mode: its text and icon should stay readable.
- The two paragraphs above should remain separate. Check the research link at rest, while hovered, and when focused with Tab in both themes.

| Feature | Expected result |
|---|---|
| Markdown | Formatted text inside the box |
| Narrow screen | Readable content with room to scroll |

</div>
</details>

---

## Nested Lists

1. [Automorphic forms](@/research.md)
   1. [Eisenstein series](@/research.md)
      1. [Spherical](@/research.md)
         1. [Fourth-level example](@/research.md)
      2. Non-spherical
   2. Cusp forms
2. L-functions
   - Riemann $\zeta(s)$
   - Dirichlet L-functions
   - Artin L-functions
   - Hasse&ndash;Weil L-functions

The linked items at all four depths should keep full-strength color, including on hover and keyboard focus. Font size stops shrinking after the third level; adding a fourth level must not make text or links progressively fainter.

## Inline Formatting

**Bold**, *italic*, `inline code`, ~~strikethrough~~.

## Links

- [Internal page link](/research)
- [Internal with anchor](#syntax-highlighting-dark-plus-theme)
- [External link](https://arxiv.org)
- [PDF download](/sample.pdf)

---

## Horizontal Rule

Three dashes on their own line create a horizontal rule:

```
---
```

Result:

---

## Unicode Symbols (no LaTeX needed)

Paste symbols directly, or use HTML entities: `&rarr;` → &rarr;, `&le;` → &le;, `&infin;` → &infin;.
For simple subscripts, `GL<sub>n</sub>` produces GL<sub>n</sub>.

## Multilingual

Add `multilingual = true` to a page's frontmatter to show buttons for its existing translations, excluding the current language:

```toml
+++
title = "About"
[extra]
multilingual = true
+++
```

When all three translations exist and use automatic buttons, `/about/` shows `中文 | 日本語`, and `/cn/about/` shows `English | 日本語`. Missing translations are omitted. Addresses come from the translated pages, so nested directories and custom paths work too.

### Custom lang_links

Choose one assignment. The commented lines are alternatives, not additional settings:

```toml
[extra]
lang_links = [{ code = "cn" }]                    # only CN button, default text
# lang_links = [{ code = "cn", text = "中文版" }]  # custom button text
# lang_links = [{ code = "cn" }, { code = "ja" }] # CN + JA, both defaults
```

An entry without `path` is omitted if that translation is missing. You may add an explicit `path` to link to another address; check that it exists and avoid listing the current language.

Language name defaults are in `config.toml` under `[translations]`, `[languages.cn.translations]`, and `[languages.ja.translations]`. Edit the following keys in each group:
```toml
lang_en = "English"
lang_cn = "中文"
lang_ja = "日本語"
```

Create translated pages as `about.cn.md` and `about.ja.md` beside `about.md`. Add the chosen `[extra]` settings to each version. Menu entries with a `page` filename follow the current language when possible and fall back to English otherwise.

## Menu Labels

In `config.toml`, menu items can use a stable `translation_key` and a default-language content filename:

```toml
[extra]
sam_menu = [
    { text = "Name", translation_key = "menu_name", page = "about.md", link = "/about" },
    { text = "Publications", page = "research.md", link = "/research" }
]
```

Edit the existing `sam_menu` list rather than adding a duplicate setting. The first entry uses the language's `menu_name` translation when present; a missing translation falls back to `text`. The second entry always uses its literal label. PDFs and external websites only need `text` and `link`.

## Light / Dark Mode

These settings belong in `config.toml` under `[extra]`:

```toml
always_dark = false           # dark is the default when true
triple_click = true           # enable the gesture and saved manual choices
light_mode_transition = true  # smooth fade; false makes changes instant
light_mode_style = "grey"     # "grey" or "blue" links in light mode
```

| `always_dark` | `triple_click` | Expected behavior |
|---|---|---|
| `false` | `true` | Follow the OS unless the reader has chosen a manual override. |
| `false` | `false` | Follow the OS and ignore saved overrides; no gesture. |
| `true` | `true` | Default to dark, while allowing saved light/dark overrides. |
| `true` | `false` | Stay dark and ignore saved overrides; no gesture. |

The defaults are `always_dark = false` and `triple_click = true`. With the gesture enabled, triple-click an empty area on the homepage to cycle **default → light → dark → default**. The default follows the OS unless `always_dark` is enabled. Manual choices are saved across pages and visits; returning to the default removes the saved choice. Disabling `triple_click` also ignores a choice saved earlier.

The third click clears any text selection. Nearby menu text may briefly become highlighted during earlier clicks, but should not remain highlighted after the theme changes. Ordinary drag and double-click text selection still work.

`light_mode_transition` controls only the fade. `light_mode_style` chooses light-mode link colors; dark-mode links remain gray.

For a browser check, try all four combinations with both operating-system preferences. When triple-click is enabled, try all three override states and both link-color settings. Save a light override, disable triple-click, and check that the override is ignored. Check the styled `<details>` summary, its research link, and the blockquote link at rest, on hover, and with keyboard focus. Check language links on the English, Chinese, and Japanese About pages as well as the nested-list links above.

On desktop and narrow screens, triple-click the blank space beside a homepage menu label and check that the selection clears through all three theme states. Repeat on translated homepages. Check ordinary drag selection, double-click selection, and menu navigation. With `triple_click = false`, repeated clicks should neither change the theme nor clear the browser's selection. Content pages should retain their normal text-selection behavior.

## Teaching Toggle

```toml
[extra]
hide_teaching = true   # hide Teaching from menu
```

To also exclude teaching pages from the build, set `draft = true` in the frontmatter of `content/teaching.md`, `content/teaching/_index.cn.md`, and every course page in `content/teaching/`. Put the flag before `[extra]`, if that heading is present.

Keep the English `content/teaching/_index.md` non-draft: it groups the courses and has `render = false`. This avoids a Zola 0.22.1 issue when both translated parent sections are drafted together.

To restore teaching, remove the draft flags and set `hide_teaching = false`.

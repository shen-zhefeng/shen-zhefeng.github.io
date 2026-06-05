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

An automorphic form $f$ on $\GL_n(\mathbb{A}_\mathbb{Q})$ satisfies $f(\gamma g k) = f(g)$ for $\gamma \in \GL_n(\mathbb{Q})$, $k \in K_\infty$.

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
| `\mathcal{O}_K, \mathfrak{p}, \mathfrak{m}` | $\mathcal{O}_K, \mathfrak{p}, \mathfrak{m}$ |
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
zola check           # check internal links
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
The trigger link above has no dashed underline.
{% end %}

### `toggle` + `toggle-block` (named pair)

Click this toggle: {% toggle(id="demo", text="Show details") %}

{% toggle-block(id="demo") %}
This block appears/disappears when clicking the toggle above.

- Supports `inline code`, **bold**, *italic*
- Nested content works
{% end %}

### `inline_expandable` (inline popover)

This sentence has an {% inline_expandable(trigger="inline popover") %}
This floating info block appears in the text flow. Click it or the trigger to close.
{% end %} right here.

---

## HTML `<details>` (browser-native)

<details>
<summary>Click to expand (native HTML)</summary>

No JavaScript required. Built into all modern browsers.

| Pros | Cons |
|---|---|
| No JS dependency | No Markdown rendering inside |
| Fast, accessible | Limited styling options |

</details>

---

## Nested Lists

1. Automorphic forms
   1. Eisenstein series
      1. Spherical
      2. Non-spherical
   2. Cusp forms
2. L-functions
   - Riemann $\zeta(s)$
   - Dirichlet L-functions
   - Artin L-functions
   - Hasse&ndash;Weil L-functions

## Inline Formatting

**Bold**, *italic*, `inline code`, ~~strikethrough~~.

## Links

- [Internal page link](/research)
- [Internal with anchor](#syntax-highlighting-dark-plus-theme)
- [External link](https://arxiv.org)
- [PDF download](/sample.pdf)

---

## Horizontal Rule

---

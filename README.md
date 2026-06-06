# zola-sam modified — Academic Personal Website Template

A Zola template for academic personal websites, modified from [zola-sam](https://github.com/janbaudisch/zola-sam) (a Zola port of [hugo-theme-sam](https://github.com/victoriadrake/hugo-theme-sam)).

Developed using [OpenCode](https://opencode.ai) with DeepSeek API (~5.6M tokens).

## Features

- **Dark & light mode** — auto-detects OS preference, manual 3-click override on the splash page
- **KaTeX math rendering** — self-hosted, `$...$` inline + `$$...$$` display
- **Multilingual** — EN, CN, JA with automatic language buttons
- **Expandable blocks** — collapsible content for paper abstracts, course details
- **Syntax highlighting** — VSCode-style `dark-plus` theme (Giallo)
- **Custom shortcodes** — 4 toggle types (expandable, inline_expandable, toggle, toggle-block)
- **Google Analytics** — built-in, disabled by default
- **Responsive** — mobile-friendly with proper spacing

## Quick Start

### Prerequisites

Install [Zola](https://getzola.org) (v0.22+):

```bash
brew install zola      # macOS
```

### Clone and Run

```bash
git clone https://github.com/shen-zhefeng/shen-zhefeng.github.io.git my-site
cd my-site
zola serve             # preview at http://127.0.0.1:1111
zola serve --drafts    # include draft pages
```

### Build

```bash
zola build             # output to public/
```

The `public/` directory is a complete static site. Deploy it to any web server (GitHub Pages, university Apache/Nginx, Netlify, Cloudflare Pages, etc.).

## Configuration

Edit `config.toml`:

### Basic Info

```toml
base_url = "https://yourname.github.io/"
title = "Your Name"
```

### Menu

```toml
[extra]
sam_menu = [
    { text = "Name", link = "/about" },
    { text = "Research", link = "/research" },
    { text = "Teaching", link = "/teaching" },
    { text = "CV", link = "/sample.pdf" },
    { text = "More", link = "/more" }
]
```

### Multilingual

Set `default_language = "en"`. Translate pages by creating `.cn.md` or `.ja.md` versions with the same slug. Add `multilingual = true` to each language version's frontmatter to auto-generate language buttons:

```toml
+++
title = "About"
[extra]
multilingual = true
+++
```

Pages without translations automatically return 404.

For granular control over which languages appear, use `lang_links`:

```toml
[extra]
lang_links = [{ code = "cn" }]                    # Only CN button, default text "中文"
lang_links = [{ code = "cn", text = "中文版" }]    # Custom text override
lang_links = [{ code = "cn" }, { code = "ja" }]   # CN + JA, both defaults
```

Customize language button text in `[translations]`:

```toml
[translations]
lang_en = "English"
lang_cn = "中文"
lang_ja = "日本語"
```

### Teaching Toggle

Set `teaching_draft = true` to hide the Teaching section from navigation. To also hide the pages from build (URL returns 404), add `draft = true` to the frontmatter of each teaching file: `content/teaching.md`, `content/teaching/_index.cn.md`, `content/teaching/course-example-1.md`, and `content/teaching/course-example-2.md`.

### Light Mode

Follows OS preference automatically. Triple-click any empty area to toggle. Preference is saved.

```toml
light_mode_transition = true   # smooth fade. Set false for instant
```

### Google Analytics

```toml
# google_analytics = "G-XXXXXXXXXX"    # Uncomment and set your ID
```

### Footer

```toml
[extra.sam_footer]
update_time = true                 # Show last deployment date
text = ""                          # Optional footer text
```

## Content Pages

Each page is a Markdown file in `content/`:

| File | Purpose |
|---|---|---|
| `_index.md` | Homepage splash (EN) |
| `_index.cn.md` | Homepage splash (CN) |
| `_index.ja.md` | Homepage splash (JA) |
| `about.md` | Bio, contact, social links |
| `research.md` | Publications with expandable abstracts |
| `teaching.md` | Course schedule, office hours |
| `cv.md` | CV page (or link to PDF — see menu config) |
| `more.md` | Template feature reference |

Reference pages:
- `content/test.md` — exhaustive hidden reference (draft). Preview with `zola serve --drafts`
- `content/more.md` — public quick reference. 1-2 examples per feature.

## Shortcodes

### Expandable (block toggle)

```markdown
{% expandable(trigger="Click to show abstract") %}
Hidden content with **Markdown**.
{% end %}
```

Parameters: `trigger` (required), `header` (line above trigger), `underline` (false = no dashed border).

### Toggle & Toggle-Block

```markdown
{% toggle(id="x", text="Click me") %}
{% toggle-block(id="x") %}
Hidden content.
{% end %}
```

### Inline Expandable (popover)

```markdown
Text with {% inline_expandable(trigger="note") %} extra info. {% end %}
```

## Math (KaTeX)

```markdown
$\GL\_n(\mathbb{A}\_\mathbb{Q})$     # inline — escape _ as \_
$$\zeta(s) = \sum 1/n^s$$           # display
```

Custom macros (e.g., `\GL`) defined in `templates/index.html`.

## Development

```bash
git checkout dev     # template branch
zola serve           # live preview (http://127.0.0.1:1111)
zola build           # production build
zola check           # check internal links
./test.sh            # smoke test (build + draft build + link check)
```

The CI workflow (`.github/workflows/actions.yml`) auto-deploys to GitHub Pages on every push to `main` using `shalzz/zola-deploy-action`. PRs to `main` run build + link check only (no deploy).

## Modifications from Original zola-sam

See `AGENTS.md` for the complete inventory. Key changes:

- Dark theme (`#111` background), light mode via CSS custom properties, 3-click toggle on splash page
- Zola 0.22 Giallo syntax highlighting (`dark-plus` theme) with line number CSS
- KaTeX self-hosted with custom macros
- 4 custom expandable/toggle shortcodes
- Multilingual support (EN/CN/JA) with auto language buttons and manual `lang_links` override
- Teaching toggle (`teaching_draft`) to hide the Teaching section
- Footer "Last updated" date with i18n date format
- CI/CD for GitHub Pages deploy with PR link check
- Max-width 800px for readability on large screens
- Google Analytics support (disabled by default)
- Test page (`content/test.md`, draft) — exhaustive reference for all features

## License

**AGPL-3.0** — inherited from [zola-sam](https://github.com/janbaudisch/zola-sam) by Jan Baudisch, a Zola port of [hugo-theme-sam](https://github.com/victoriadrake/hugo-theme-sam) (Apache-2.0) by Victoria Drake.

When redistributing: keep the same license, preserve copyright notices, and document your changes. See `LICENSE` for the full text.

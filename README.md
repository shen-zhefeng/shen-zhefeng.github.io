# zola-sam modified — Academic Personal Website Template

A Zola template for academic personal websites, modified from [zola-sam](https://github.com/janbaudisch/zola-sam) (a Zola port of [hugo-theme-sam](https://github.com/victoriadrake/hugo-theme-sam)).

Developed using [OpenCode](https://opencode.ai) with DeepSeek API.

## Features

- **Dark & light mode** — auto-detects OS preference, manual 3-click override on the splash page
- **KaTeX math rendering** — self-hosted, `$...$` inline + `$$...$$` display
- **Multilingual** — EN, CN, JA with automatic language buttons
- **Expandable blocks** — collapsible content for paper abstracts, course details
- **Syntax highlighting** — VSCode-style `dark-plus` theme (Giallo)
- **Custom shortcodes** — 3 types: expandable, inline_expandable, toggle (plus native `<details>`)
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
```

Open the preview address in your browser. Keep the terminal running while editing; Zola rebuilds the preview when you save a file. Press **Ctrl+C** to stop it. To include the hidden feature-reference page, run `zola serve --drafts` instead and visit `http://127.0.0.1:1111/test/`.

### Build

```bash
zola build             # output to public/
```

The `public/` directory is a complete static site. Deploy it to any web server (GitHub Pages, university Apache/Nginx, Netlify, Cloudflare Pages, etc.).

## Configuration

Edit the existing settings in `config.toml`. TOML groups settings under headings such as `[extra]`; do not add a second copy of an existing heading or assign the same setting twice in one group.

### Basic Info

```toml
base_url = "https://yourname.github.io/"
title = "Your Name"
```

### Menu

```toml
[extra]
sam_menu = [
    { text = "Name", translation_key = "menu_name", page = "about.md", link = "/about" },
    { text = "Research", translation_key = "menu_research", page = "research.md", link = "/research" },
    { text = "Teaching", translation_key = "menu_teaching", page = "teaching.md", link = "/teaching" },
    { text = "CV", translation_key = "menu_cv", link = "/sample.pdf" },
    { text = "More", translation_key = "menu_more", page = "more.md", link = "/more" }
]
```

- `text` is the label to use when no translation is configured.
- `translation_key` is optional. Keep this stable when editing a label, and edit its wording in the English `[translations]`, Chinese `[languages.cn.translations]`, and Japanese `[languages.ja.translations]` groups. A missing key falls back to `text`.
- `page` is an optional path relative to `content/`, using the English filename. It lets the menu follow the reader's language when a translation exists; otherwise the English page is used. Use a section's `_index.md` filename for a section.
- `link` supplies a fallback address and is used for PDFs and external websites. Root-relative site links also work when `base_url` includes a subdirectory.

For a label that stays the same in every language, add an entry such as `{ text = "Publications", page = "research.md", link = "/research" }`. No new translation key is required.

### Multilingual

Set `default_language = "en"`. Translate pages by creating `.cn.md` or `.ja.md` versions beside the English file, such as `about.cn.md` and `about.ja.md`. Add `multilingual = true` to each language version's frontmatter to generate buttons for its available translations:

```toml
+++
title = "About"
[extra]
multilingual = true
+++
```

Only existing translations appear, and the current language is excluded. Links use the generated page addresses, including nested directories, custom paths, and a deployment subdirectory. The translated home and bottom menus stay in the selected language when a destination has a translation; untranslated menu destinations fall back to English.

The Research page includes English, Chinese, and Japanese versions (`research.md`, `research.cn.md`, and `research.ja.md`). Each version links to the other two languages and contains the same publication examples. Edit the translated files alongside the English page when customizing your research content.

For granular control over which languages appear, use `lang_links`. Choose **one** assignment; the commented lines below are alternatives:

```toml
[extra]
lang_links = [{ code = "cn" }]                    # Only CN button, default text "中文"
# lang_links = [{ code = "cn", text = "中文版" }]  # Custom text override
# lang_links = [{ code = "cn" }, { code = "ja" }] # CN + JA, both defaults
```

Without a `path`, an entry links to an existing translation and is omitted if that translation is missing. Add `path = "/custom-address/"` to supply a destination explicitly, and check that the address exists. Custom entries are used in the supplied order, so avoid listing the current language.

Customize language button text in the existing `[translations]`, `[languages.cn.translations]`, and `[languages.ja.translations]` groups:

```toml
[translations]
lang_en = "English"
lang_cn = "中文"
lang_ja = "日本語"
```

### Teaching Toggle

Set `hide_teaching = true` in `[extra]` to hide Teaching from navigation. To also exclude its pages from the build (URLs return 404), add `draft = true` to the frontmatter of `content/teaching.md`, `content/teaching/_index.cn.md`, and each course page in `content/teaching/`. Keep the English `content/teaching/_index.md` non-draft: it only groups the courses and has `render = false`. This avoids a Zola 0.22.1 issue when both translated parent sections are drafted together. Reverse the draft flags and menu setting to restore teaching.

### Light and Dark Mode

By default, the site follows your operating system's light/dark preference. On the homepage, click an empty area three times quickly to cycle **default → light → dark → default**. The saved choice applies across pages and visits. Returning to the default removes the saved override.

The third click also clears any text selection, so nearby menu text does not stay highlighted. A highlight may briefly appear during the earlier clicks. Ordinary drag and double-click text selection still work.

These settings belong in `[extra]`:

```toml
always_dark = false           # true makes dark the default, ignoring the OS preference
triple_click = true           # allow the homepage gesture and saved manual choices
light_mode_transition = true  # smooth fade only; false makes changes instant
light_mode_style = "grey"     # "grey" or "blue" links in light mode
```

| `always_dark` | `triple_click` | Appearance |
|---|---|---|
| `false` | `true` | Follow the OS; allow saved light/dark overrides (the defaults). |
| `false` | `false` | Follow the OS; disable the gesture and ignore saved overrides. |
| `true` | `true` | Start in dark mode; allow saved light/dark overrides. |
| `true` | `false` | Stay in dark mode; disable the gesture and ignore saved overrides. |

`always_dark = true` changes the default appearance; a manual light choice still applies when `triple_click` is enabled. To keep the site dark for everyone, combine `always_dark = true` with `triple_click = false`. The transition setting only controls the fade, not which modes are available.

The favicon follows the site's appearance: `static/faviconwhite.ico` is used in light mode and `static/faviconblack.ico` in dark mode, including saved manual choices. Both are solid-color squares, so a white icon may be hard to see against a light browser tab (and a black icon against a dark tab). The browser controls the tab color independently of the webpage.

### Google Analytics

Tracking is disabled by default. In `[extra]`, uncomment the following setting and replace the example ID to enable it:

```toml
# google_analytics = "G-XXXXXXXXXX"    # Uncomment and set your ID
```

### Footer

```toml
[extra.sam_footer]
update_time = true                 # Show the date the site was built
text = ""                          # Optional footer text
```

## Customizing the Appearance

The files in `sass/` control how the site looks. Zola combines and compiles them into the CSS stylesheets that browsers read. Files whose names begin with `_` are **partials**: they contribute to `style.css` through imports in `style.sass`, rather than producing their own stylesheets. `fonts.scss` produces a separate `fonts.css` for loading the bundled font.

Choose the file for the part of the page you want to change:

| File in `sass/` | What it controls |
|---|---|
| `style.sass` | The list of imports, in the order they are applied |
| `_theme.sass` | Font and spacing settings, plus the dark/light color palettes |
| `_mixins.sass` | Shared style helpers used by several parts of the site |
| `_base.sass` | Browser defaults, the page body, basic text, links, buttons, and horizontal rules |
| `_layout.sass` | Content widths, the homepage, titles, menus, language links, the footer, and alignment helpers |
| `_content.sass` | Markdown content: paragraphs, quotes, tables, code and syntax highlighting, images, galleries, and tags |
| `_disclosures.sass` | Expandable blocks, floating inline notes, toggles, native details, and their spacing in lists |
| `fonts.scss` | The bundled Didact Gothic font file and its loading behavior |

For example, change the content column width in `_layout.sass`, table cell spacing in `_content.sass`, or expandable button styling in `_disclosures.sass`. To choose the existing light/dark options, use `config.toml` as described above; edit `_theme.sass` when you want to change the actual colors or shared font settings.

Page titles use 32px Didact Gothic Regular. Markdown headings step down from `#` to `####` at 28px, 24px, 20px, and 18px, also in regular weight. For example, write `# Main section`, then `## Subsection`, `### Smaller heading`, and `#### Smallest heading` on separate lines. Bulleted and numbered lists use 16px at the first level, 15px at the second, and 14px from the third level onward. Nesting changes their size, not their color or opacity, so links stay readable.

All heading levels have 16px of space above and below, controlled in `_base.sass` and `_content.sass`. Horizontal rules have 8px above and below, set by the `skinny-hr` helper in `_mixins.sass`. These spaces add together when a heading follows a rule. The language links and content area have no extra gap between them beyond line spacing and the rule's top margin.

The `.sass` files use indentation to group rules, so preserve the surrounding indentation when editing. Comments explain which visual element each section affects, and rules for small screens stay beside the feature they adjust. Keep the import order in `style.sass`: shared settings and helpers come first, followed by basic styles, content, layout, and disclosures. Layout follows content so alignment helpers still take precedence when used on a row of tags. Changing this order can change which style takes precedence.

Run `zola serve --drafts` while editing to preview your changes, including the examples at `/test/`. Edit the source files in `sass/`; generated files in `public/` are replaced during a build. Check both themes and a narrow browser window after changing styles.

## Content Pages

Each page is a Markdown file in `content/`:

| File | Purpose |
|---|---|---|
| `_index.md` | Optional English homepage settings; the splash works without this file |
| `_index.cn.md` | Homepage splash (CN) |
| `_index.ja.md` | Homepage splash (JA) |
| `about.md` | Bio, contact, social links |
| `research.md`, `research.cn.md`, `research.ja.md` | Research interests and publications with expandable abstracts in EN/CN/JA |
| `teaching.md` | Course schedule, office hours |
| `teaching/_index.md` | Groups course pages into a section; `render = false` keeps the landing page in `teaching.md` |
| `cv.md` | Optional page you can create; the supplied menu links to `static/sample.pdf` |
| `more.md` | Template feature reference |

Reference pages:

- `content/test.md` — exhaustive hidden reference (draft). Preview with `zola serve --drafts`
- `content/more.md` — public quick reference. 1-2 examples per feature.

To create a page, save a file such as `content/talks.md`:

```markdown
+++
title = "Talks"
+++

## Upcoming talks

Write **bold**, *italic*, or `inline code`.

- [Research page](@/research.md)
- [External website](https://example.com)
- [Download a PDF](/sample.pdf)

---

The three dashes above create a horizontal rule.
```

The `+++` lines enclose the page settings, called *frontmatter*. The remaining text is Markdown. Use `@/` links for other content files so Zola can check the destination; put downloadable files in `static/`. Add the new page to `sam_menu` if you want it in navigation. Use `draft = true` in frontmatter while a page is unfinished.

Leave a blank line between paragraphs, including inside expandable blocks. For multiple paragraphs in a blockquote, put a line containing just `>` between them. Nested lists and language links stay readable without progressively fading; links inside styled details and blockquotes use colors suited to their backgrounds.

### Tables

Write tables using vertical bars between cells and a separator below the header:

```markdown
| Semester | Course |
|---|---|
| Spring | Number Theory |
```

Tables wider than their available space scroll sideways within the page, including inside expandable content and inline notes. Authors do not need to add extra markup. The Test page includes deliberately wide examples for checking small screens.

To scroll with the keyboard, press Tab until the wide table has a visible outline, then use the Left and Right Arrow keys. Tables that already fit do not add an extra Tab stop. Scrolling or clicking inside a table keeps its surrounding expandable box open; links in the table still work normally.

## Shortcodes

### Expandable (block toggle)

```markdown
{% expandable(trigger="Click to show abstract") %}
Hidden content with **Markdown**.
{% end %}
```

Parameters: `trigger` (required), `header` (line above trigger), `underline` (false = no underline).

### Native `<details>`

```markdown
<details>
<summary>Click to expand</summary>

Hidden content with **Markdown**.

</details>
```

Keep blank lines around the Markdown body. For a themed border and content background, add `class="expand-box"` to `<details>` and wrap the body in `<div class="expand-content">`, again with blank lines before and after the Markdown text. Working examples are on the More and Test pages.

### Inline Expandable (popover)

```markdown
Text with {% inline_expandable(trigger="note") %} extra info. {% end %}
```

The note supports Markdown, including emphasis, links, paragraphs, and lists. The trigger stays in the surrounding sentence; the note opens above the page content. Click the trigger or note content to close it, or press Escape. For content that should expand in the page layout, use `expandable` or native `<details>`.

### Toggle an existing block

```markdown
{{ toggle(text="Show or hide the note", id="my-note") }}

<div id="my-note" style="display: none;">

A separate note with **Markdown**.

</div>
```

The `id` must match the target block and be unique on that page. Several triggers can share the same target. Click the trigger, or focus it with Tab and press Enter or Space, to show or hide the content.

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
zola check           # check internal and external links (requires network)
./test.sh            # production/draft builds, regression tests, and links
```

The smoke test requires Zola 0.22.1 and Python 3 (`python3`). It builds the production site in `public/`, compiles drafts in a separate temporary directory, and checks that the hidden `/test/` reference page is absent from production and present in the draft build. Temporary drafts are removed even if a check fails. All Python regression suites named `tests/test_*.py` run automatically, followed by the internal/external link check. Only publish `public/` after the entire script succeeds.

The regression suites check generated navigation and appearance settings, including all four `always_dark`/`triple_click` combinations. They also check that the smoke script rejects missing pages, drafts in production, and failing tests, and cleans up temporary drafts after failures.

For an offline internal-link check, use `zola check --skip-external-links`. This does not replace the full network-enabled check before merging. A connection failure in a restricted environment does not by itself mean the remote page is broken.

The valid Codex destination at `https://openai.com/codex/` returns HTTP 403 to GitHub's automated link checker. Its URL prefix is therefore excluded through `[link_checker].skip_prefixes` in `config.toml`; check this destination manually when editing its links. Other external links still fail validation on errors.

The CI workflow (`.github/workflows/actions.yml`) runs this same script in a **validation job** with read-only repository permission. Zola is installed on the runner at version 0.22.1, with its download verified against a recorded SHA-256 checksum. The validated `public/` directory is saved as an artifact (a downloadable bundle of build output), retained for one day.

A separate **deployment job** runs only after validation succeeds, and only for pushes to `main` or manual workflow runs on `main`. It downloads the validated production artifact and uses `peaceiris/actions-gh-pages` to publish it to `gh-pages`, without rebuilding. Only this job has permission to write repository contents. GitHub Pages should remain configured to **Deploy from a branch → gh-pages → /(root)**. PRs to `main` and manual runs on other branches validate only; pushes to `dev` do not trigger the workflow. New runs cancel older runs for the same branch to avoid overlapping deployments; PR runs are kept separate from `main`.

Every action is pinned to a full commit SHA, with its release version in a nearby comment. When updating an action, verify the new commit against its official repository and update both the SHA and version comment. When updating Zola, update both `ZOLA_VERSION` and the Linux archive's `ZOLA_SHA256` in the workflow, then run the smoke test before publishing.

After changing templates, shortcodes, or styles, also check the browser: mouse and keyboard operation, a narrow or short window, both light and dark mode, and translated pages. The Test page includes long notes and shared toggle targets for these checks. Verify that separate paragraphs remain separate, language and nested-list links remain readable, and links in styled details and blockquotes stay visible at rest, on hover, and with keyboard focus. Scroll the wide tables to their last column using both a pointer and the keyboard; the page should not move sideways, and the long inline note should remain vertically scrollable.

## Modifications from Original zola-sam

Key changes:

- Dark theme (`#111` background), light mode via CSS custom properties, 3-click toggle on splash page
- Zola 0.22 Giallo syntax highlighting (`dark-plus` theme) with line number CSS
- Sass grouped by visual responsibility, with a short import list and comments explaining where to customize each feature
- KaTeX self-hosted with custom macros
- 3 custom shortcodes (expandable, inline_expandable, toggle) plus native `<details>`
- Multilingual support (EN/CN/JA) with auto language buttons and manual `lang_links` override
- Teaching toggle (`hide_teaching`) to hide the Teaching section
- Footer "Last updated" date with i18n date format
- CI/CD for GitHub Pages deploy with PR link check
- Content pages resize smoothly: at the default font size, narrow screens keep 16px side gutters, tablets use a 576px text column when space permits, and windows 1280px or wider retain a 45% column capped at 800px. The homepage keeps its separate layout.
- Google Analytics support (disabled by default)
- Test page (`content/test.md`, draft) — exhaustive reference for all features

## License

**AGPL-3.0** — inherited from [zola-sam](https://github.com/janbaudisch/zola-sam) by Jan Baudisch, a Zola port of [hugo-theme-sam](https://github.com/victoriadrake/hugo-theme-sam) (Apache-2.0) by Victoria Drake.

When redistributing: keep the same license, preserve copyright notices, and document your changes. See `LICENSE` for the full text.

# Zola 0.23.6 authoring and migration

This branch uses Zola **0.23.6** and Tera 2. Check `zola --version` before developing. CI verifies the official Linux download against its SHA-256 checksum; deployment still occurs only from `main`.

## Content components

The old shortcode calls have been converted to named components. Each disclosure needs an ID unique on that page:

```markdown
{% <expandable id="paper-one-abstract" trigger="Abstract" underline={true}> %}
An abstract with **Markdown** and $x^2$.
{% </expandable> %}

A sentence with {% <inline_expandable id="paper-one-note" trigger="note"> %}
Rich note content, including paragraphs and tables.
{% </inline_expandable> %} continues here.

{{ <toggle text="Show or hide" id="existing-note" /> }}

<div id="existing-note" style="display: none;">

Markdown content.

</div>
```

Use quotes for strings and braces for booleans, arrays, or other expressions. Keep citations, links, mathematics, and disclosure bodies in Markdown. `toggle` IDs refer to the supplied target; several toggles may intentionally share it. Other control IDs must be unique. For publication filtering on branches that include it, give the collection its own ID and use `tags={["Number theory", "Geometry"]}` on each `publication` entry.

## Literal examples

Every content page is processed as a template before Markdown. A code fence alone does not protect template syntax. Wrap examples with `{% raw %}` and `{% endraw %}`:

````markdown
{% raw %}
```markdown
{% <expandable id="example" trigger="Abstract"> %}
Example body.
{% </expandable> %}
```
{% endraw %}
````

## Template maintenance

- Shared macros are now globally registered `site.*` components in `templates/helpers.html`; imports are unnecessary.
- Definitions live in `templates/components/`. They declare implicit `@config` and `@lang` only where needed.
- Navigation looks up default-language pages explicitly, then selects real translation permalinks or falls back to the source page.
- HTML attributes and labels are explicitly escaped because content templating does not automatically escape component output.
- Rich inline notes encode generated newlines as HTML entities so Markdown keeps their triggers inside the surrounding paragraph. The browser decodes the newlines when the inert template is mounted.
- Shared disclosure JavaScript is included from `templates/_disclosures.js.html`. Theme styles and interaction semantics are retained.

## Verification and rollback

Run `./test.sh` with Zola 0.23.6 and network access. It verifies production/draft isolation, all discovered regressions, and internal/external links. Also check disclosure and theme behavior in the browser at narrow and desktop widths. Each branch has a checkpoint before conversion and a separate migration commit; revert only the migration commit to restore its previous source without rewriting history.

#!/usr/bin/env python3
"""Build Tera 2 component fixtures: escaping, inline flow, rich bodies, and raw examples."""
from html.parser import HTMLParser
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BODY = r'''
{% <expandable id="block-fixture" trigger='Abstract "A & B" <em>literal</em>'> %}
**Rich block** with $x^2$ and [Research](@/research.md).
{% </expandable> %}

Before {% <inline_expandable id="inline-fixture" trigger='Note "A & B"'> %}
First paragraph.

Second paragraph with **Markdown**.

| Name | Value |
|---|---|
| A | B |

```text
first line
second line
```
{% </inline_expandable> %} after.

{{ <toggle text='Show "A & B"' id="toggle-fixture" /> }}
<div id="toggle-fixture" style="display: none;">Hidden fixture.</div>

{% raw %}
```markdown
{% <expandable id="literal-example" trigger="Literal"> %}
Documentation example.
{% </expandable> %}
```
{% endraw %}
'''


class Markup(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = []
        self.controls = []
        self.parents = []
        self.inline_parent = None
        self.inline_labels = []
        self.pre_text = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if attrs.get("aria-controls"):
            self.controls.append(attrs["aria-controls"])
        if attrs.get("class") == "inline_expandable-container":
            self.inline_parent = self.parents[-1] if self.parents else None
        if attrs.get("id") == "inline-fixture":
            self.inline_labels.append(attrs.get("aria-label"))
        if tag not in {"input", "img", "meta", "link", "br", "hr"}:
            self.parents.append(tag)

    def handle_data(self, data):
        if "pre" in self.parents:
            self.pre_text.append(data)

    def handle_endtag(self, tag):
        if tag in self.parents:
            reverse_index = self.parents[::-1].index(tag)
            del self.parents[len(self.parents) - reverse_index - 1:]


class ComponentTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="zola-components-")
        self.addCleanup(temp.cleanup)
        self.site = Path(temp.name)
        for name in ("content", "templates", "sass", "static"):
            shutil.copytree(ROOT / name, self.site / name)
        shutil.copy2(ROOT / "config.toml", self.site / "config.toml")

    def build(self):
        result = subprocess.run([os.environ.get("ZOLA_BIN", "zola"), "build", "--force",
                                 "--base-url", "https://example.test/subsite/"],
                                cwd=self.site, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_markup_escaping_inline_flow_and_raw_examples(self):
        for suffix in ("", ".cn", ".ja"):
            (self.site / "content" / ("component-fixture" + suffix + ".md")).write_text(
                '+++\ntitle = "Component fixture"\n+++\n' + BODY)
        self.build()
        for language in ("", "cn", "ja"):
            with self.subTest(language=language):
                source = (self.site / "public" / language / "component-fixture/index.html").read_text()
                markup = Markup(source)
                self.assertEqual(markup.inline_parent, "p")
                self.assertEqual(markup.inline_labels, ['Note "A & B"'])
                self.assertTrue(set(markup.controls).issubset(markup.ids))
                self.assertEqual(len(markup.ids), len(set(markup.ids)))
                self.assertNotIn("literal-example", markup.ids)
                self.assertIn("<strong>Rich block</strong>", source)
                self.assertIn("<strong>Markdown</strong>", source)
                self.assertIn("<table>", source)
                self.assertIn("first line\nsecond line", "".join(markup.pre_text))
                self.assertIn("&lt;em&gt;literal&lt;/em&gt;", source)
                self.assertNotIn("<em>literal</em>", source)
                self.assertIn('href="https://example.test/subsite/research/"', source)

    def test_taxonomies_date_and_missing_optional_metadata(self):
        (self.site / "content/taxonomy-fixture.md").write_text(
            '+++\ntitle = "Dated paper"\ndate = 2026-10-14\n'
            '[taxonomies]\ntags = ["Number theory"]\nauthors = ["Example Author"]\n+++\nBody.\n')
        (self.site / "content/plain-fixture.md").write_text('+++\ntitle = "Plain page"\n+++\nBody.\n')
        self.build()
        output = self.site / "public"
        self.assertTrue((output / "plain-fixture/index.html").is_file())
        page = (output / "taxonomy-fixture/index.html").read_text()
        self.assertIn('/tags/number-theory/', page)
        self.assertIn('/authors/example-author/', page)
        for path in ("tags/number-theory", "authors/example-author"):
            source = (output / path / "index.html").read_text()
            self.assertIn("Dated paper", source)
            self.assertIn("2026", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)

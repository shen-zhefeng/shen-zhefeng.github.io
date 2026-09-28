#!/usr/bin/env python3
"""Check theme configuration in built pages without browser dependencies.

Run with: python3 tests/test_theme_config.py
These build checks cover the generated HTML and CSS contracts. Browser checks
are still needed for saved preferences, gesture interaction, and actual colors.
Only Python's standard library and Zola are required; public/ is untouched.
"""

from html.parser import HTMLParser
from itertools import product
from pathlib import Path
import os
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ThemePage(HTMLParser):
    """Read root classes and executable inline scripts from generated HTML."""

    def __init__(self, html):
        super().__init__()
        self.classes = set()
        self.scripts = []
        self.styles = []
        self.collecting = None
        self.parts = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.classes = set(attrs.get("class", "").split())
        if tag == "style" or (tag == "script" and "src" not in attrs):
            self.collecting = tag
            self.parts = []

    def handle_data(self, data):
        if self.collecting:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == self.collecting:
            target = self.scripts if tag == "script" else self.styles
            target.append("".join(self.parts))
            self.collecting = None


def light_media_rules(css):
    """Yield rules inside the compiled automatic-light media block."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for media in re.finditer(r"@media\s*\(\s*prefers-color-scheme\s*:\s*light\s*\)\s*\{", css):
        depth, end = 1, media.end()
        while depth and end < len(css):
            depth += (css[end] == "{") - (css[end] == "}")
            end += 1
        if depth:
            raise AssertionError("Unclosed automatic-light CSS block")
        for rule in re.finditer(r"([^{}]+)\{([^{}]*)\}", css[media.end():end - 1]):
            yield rule.group(1).strip(), rule.group(2)


def root_matches(selector, classes):
    """Match the project's simple root selectors, rejecting unfamiliar syntax.

    Testing which roots match a compiled rule catches an accidental unguarded
    selector without comparing the stylesheet to an exact source snapshot.
    """
    excluded = re.findall(r":not\(\s*\.([\w-]+)\s*\)", selector)
    remaining = re.sub(r":not\(\s*\.[\w-]+\s*\)", "", selector)
    required = re.findall(r"\.([\w-]+)", remaining)
    remaining = re.sub(r"\.[\w-]+", "", remaining).strip()
    if remaining not in ("html", ":root", "html:root"):
        raise AssertionError("Extend the root selector checker for: " + selector)
    return not any(name in classes for name in excluded) and all(name in classes for name in required)


class ThemeConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="zola-theme-config-")
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        for name in ("content", "templates", "sass", "static"):
            shutil.copytree(ROOT / name, self.site / name)
        self.config = (ROOT / "config.toml").read_text()
        self.output = self.site / "build"

    def build(self, always_dark, triple_click, style):
        config = re.sub(r"(?m)^(always_dark|triple_click|light_mode_style)\s*=.*\n?", "", self.config)
        settings = ['light_mode_style = "' + style + '"']
        for name, value in (("always_dark", always_dark), ("triple_click", triple_click)):
            if value is not None:
                settings.append(name + " = " + str(value).lower())
        self.assertIn("[extra]", config)
        (self.site / "config.toml").write_text(config.replace("[extra]", "[extra]\n" + "\n".join(settings), 1))
        result = subprocess.run(
            [os.environ.get("ZOLA_BIN", "zola"), "build", "--force", "--output-dir", str(self.output)],
            cwd=self.site, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def check_pages(self, always_dark, triple_click, style):
        for path in ("", "about", "cn", "cn/about", "ja", "ja/about"):
            with self.subTest(page=path or "home"):
                page = ThemePage((self.output / path / "index.html").read_text())
                self.assertEqual("always-dark" in page.classes, always_dark)
                # Saved preferences are restored by JavaScript, never baked in.
                self.assertFalse(page.classes & {"light-mode", "dark-mode"})
                storage = [script for script in page.scripts if re.search(
                    r"localStorage\.(getItem|setItem|removeItem)\(\s*['\"]color-scheme['\"]", script)]
                restores = [script for script in storage if "getItem" in script]
                gestures = [script for script in storage if re.search(
                    r"addEventListener\(\s*['\"]click['\"]", script)]
                self.assertEqual(len(restores), int(triple_click))
                is_home = path in ("", "cn", "ja")
                self.assertEqual(len(gestures), int(triple_click and is_home))
                if not triple_click:
                    self.assertEqual(storage, [], "Disabled gestures must also ignore stale stored preferences")
                blue_rules = [(selector, body) for selector, body in light_media_rules("\n".join(page.styles))
                              if "--links" in body]
                self.assertEqual(bool(blue_rules), style == "blue")
                self.check_automatic_rules(blue_rules)
        compiled_rules = [(selector, body) for selector, body in
                          light_media_rules((self.output / "style.css").read_text()) if "--bg" in body]
        self.assertTrue(compiled_rules, "The system-light baseline must remain available")
        self.check_automatic_rules(compiled_rules)

    def check_automatic_rules(self, rules):
        for selectors, _ in rules:
            for selector in selectors.split(","):
                self.assertTrue(root_matches(selector, set()))
                self.assertFalse(root_matches(selector, {"always-dark"}), "System light must not override always_dark")
                self.assertFalse(root_matches(selector, {"dark-mode"}), "System light must not override manual dark")

    def test_all_flag_combinations_and_link_styles(self):
        for always_dark, triple_click, style in product((False, True), (False, True), ("grey", "blue")):
            with self.subTest(always_dark=always_dark, triple_click=triple_click, style=style):
                self.build(always_dark, triple_click, style)
                self.check_pages(always_dark, triple_click, style)

    def test_missing_flags_keep_backward_compatible_defaults(self):
        # Check both missing and each independently missing; explicit false
        # must not be mistaken for an absent key by the template's defaults.
        for always_dark, triple_click, style in product((None, True), (None, False), ("grey", "blue")):
            if always_dark is not None and triple_click is not None:
                continue
            with self.subTest(always_dark=always_dark, triple_click=triple_click, style=style):
                self.build(always_dark, triple_click, style)
                self.check_pages(always_dark if always_dark is not None else False,
                                 triple_click if triple_click is not None else True, style)


if __name__ == "__main__":
    unittest.main(verbosity=2)

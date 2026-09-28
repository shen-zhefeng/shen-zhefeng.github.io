#!/usr/bin/env python3
"""Build isolated fixture sites and check the URLs readers actually receive.

Run with: python3 tests/test_navigation.py
Only Python's standard library and the project's Zola executable are required.
Temporary copies keep fixture pages and drafts out of the real public/ folder.
"""

from html.parser import HTMLParser
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://example.test/portfolio/"


class NavigationParser(HTMLParser):
    """Collect visible link labels and destinations from the three menus."""

    def __init__(self):
        super().__init__()
        self.divs = []
        self.links = {"splash": [], "bottom-menu": [], "lang-links": []}
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            self.divs.append(set(attrs.get("class", "").split()) | {attrs.get("id")})
        elif tag == "a":
            regions = [name for name in self.links if any(name in div for div in self.divs)]
            self.anchor = (regions, attrs.get("href"), [])

    def handle_data(self, data):
        if self.anchor:
            self.anchor[2].append(data)

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor:
            regions, href, text = self.anchor
            for region in regions:
                self.links[region].append((" ".join("".join(text).split()), href))
            self.anchor = None
        elif tag == "div" and self.divs:
            self.divs.pop()


class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="zola-navigation-")
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        for name in ("content", "templates", "sass", "static"):
            shutil.copytree(ROOT / name, self.site / name)
        shutil.copy2(ROOT / "config.toml", self.site / "config.toml")
        self.output = self.site / "build"

    def edit_config(self, old, new):
        config = self.site / "config.toml"
        text = config.read_text()
        self.assertIn(old, text, "Configuration fixture no longer matches the project")
        config.write_text(text.replace(old, new, 1))

    def append_menu(self, entries):
        self.edit_config("]\n\nsam_bottom_menu", ",\n" + entries + "\n]\n\nsam_bottom_menu")

    def write_content(self, path, frontmatter, body="Fixture content."):
        target = self.site / "content" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("+++\n" + frontmatter + "\n+++\n" + body + "\n")

    def build(self, drafts=False):
        command = [os.environ.get("ZOLA_BIN", "zola"), "build", "--force",
                   "--base-url", BASE, "--output-dir", str(self.output)]
        if drafts:
            command.append("--drafts")
        result = subprocess.run(command, cwd=self.site, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def links(self, path, region):
        parser = NavigationParser()
        parser.feed((self.output / path / "index.html").read_text())
        return parser.links[region]

    def test_custom_menu_labels_and_external_links(self):
        # A missing key and no key must both fall back to the editable label.
        self.edit_config('text = "Name", translation_key = "menu_name"', 'text = "Biography renamed"')
        self.append_menu('''{ text = "Publications", link = "/research" },
        { text = "Untranslated label", translation_key = "menu_new", link = "/more" },
        { text = "External", link = "https://example.org/papers?q=1#recent" },
        { text = "Protocol-relative", link = "//example.org/papers" }''')
        for drafts in (False, True):
            self.build(drafts=drafts)
            for language in ("", "cn", "ja"):
                for path, region in ((language, "splash"),
                                     (language + "/about" if language else "about", "bottom-menu")):
                    links = self.links(path, region)
                    prefix = language + "/" if language else ""
                    self.assertIn(("Biography renamed", BASE + prefix + "about/"), links)
                    self.assertIn(("Publications", BASE + "research"), links)
                    self.assertIn(("Untranslated label", BASE + "more"), links)
                    self.assertIn(("External", "https://example.org/papers?q=1#recent"), links)
                    self.assertIn(("Protocol-relative", "//example.org/papers"), links)

    def test_localized_home_about_research_and_untranslated_page_fallback(self):
        self.build()
        research_languages = (("", "English"), ("cn", "中文"), ("ja", "日本語"))
        for code, name, home, research, more in (("", "Name", "Start", "Research", "More"),
                                                 ("cn", "姓名", "主页", "研究", "更多"),
                                                 ("ja", "名前", "ホーム", "研究", "もっと")):
            prefix = code + "/" if code else ""
            splash = self.links(code, "splash")
            bottom = self.links(prefix + "about", "bottom-menu")
            research_bottom = self.links(prefix + "research", "bottom-menu")
            for links in (splash, bottom, research_bottom):
                self.assertIn((name, BASE + prefix + "about/"), links)
                self.assertIn((research, BASE + prefix + "research/"), links)
                # More has no translations, so its localized label links to English.
                self.assertIn((more, BASE + "more/"), links)
                self.assertIn(("CV", BASE + "sample.pdf"), links)
            self.assertIn((home, BASE + prefix), bottom)
            self.assertIn((home, BASE + prefix), research_bottom)
            self.assertCountEqual(self.links(prefix + "research", "lang-links"), [
                (label, BASE + (other + "/" if other else "") + "research/")
                for other, label in research_languages if other != code
            ])

    def test_nested_translations_use_actual_custom_permalinks(self):
        self.write_content("courses/_index.md", 'title = "Courses"')
        self.write_content("courses/_index.cn.md", 'title = "课程"')
        self.write_content("courses/topic.md", 'title = "Topic"\n[extra]\nmultilingual = true')
        self.write_content("courses/topic.cn.md", 'title = "主题"\nslug = "topic-cn"\n[extra]\nmultilingual = true')
        self.write_content("courses/topic.ja.md", 'title = "Draft translation"\ndraft = true')
        self.append_menu('{ text = "Topic", page = "courses/topic.md", link = "/courses/topic" },\n'
                         '{ text = "Courses", page = "courses/_index.md", link = "/courses" }')
        self.build()
        self.assertEqual(self.links("courses/topic", "lang-links"),
                         [("中文", BASE + "cn/courses/topic-cn/")])
        self.assertEqual(self.links("cn/courses/topic-cn", "lang-links"),
                         [("English", BASE + "courses/topic/")])
        self.assertIn(("Topic", BASE + "cn/courses/topic-cn/"), self.links("cn", "splash"))
        self.assertIn(("Courses", BASE + "cn/courses/"), self.links("cn", "splash"))
        self.assertIn(("Topic", BASE + "courses/topic/"), self.links("ja", "splash"))

    def test_custom_language_links_use_real_translation_or_explicit_path(self):
        self.write_content("custom.md", '''title = "Custom"
[extra]
lang_links = [{ code = "cn" }, { code = "ja" },
              { code = "de", text = "Deutsch", path = "https://example.org/de/" },
              { code = "xx", path = "/custom-override/" }]''')
        self.write_content("custom.cn.md", 'title = "自定义"\nslug = "custom-cn"')
        self.build()
        self.assertEqual(self.links("custom", "lang-links"), [
            ("中文", BASE + "cn/custom-cn/"),
            ("Deutsch", "https://example.org/de/"),
            ("xx", "/custom-override/"),
        ])

    def test_hidden_teaching_drafts_do_not_trigger_missing_page_lookup(self):
        self.edit_config("hide_teaching = false", "hide_teaching = true")
        self.edit_config('text = "Teaching", translation_key', 'text = "Courses renamed", translation_key')
        # Keep the non-rendered English structural parent. Zola 0.22.1 can
        # remove unrelated translated pages when both parent sections are draft.
        teaching_files = [self.site / "content" / "teaching.md"]
        teaching_files.extend(path for path in (self.site / "content" / "teaching").glob("*.md")
                              if path.name != "_index.md")
        for path in teaching_files:
            path.write_text(path.read_text().replace("+++\n", "+++\ndraft = true\n", 1))
        for drafts in (False, True):
            self.build(drafts=drafts)
            self.assertEqual((self.output / "teaching/index.html").exists(), drafts)
            self.assertEqual((self.output / "cn/teaching/index.html").exists(), drafts)
            for course in ("course-example-1", "course-example-2"):
                self.assertEqual((self.output / "teaching" / course / "index.html").exists(), drafts)
            for code in ("", "cn", "ja"):
                for _, url in self.links(code, "splash"):
                    self.assertNotIn("/teaching", url)
                about = code + "/about" if code else "about"
                for _, url in self.links(about, "bottom-menu"):
                    self.assertNotIn("/teaching", url)

    def test_section_menu_without_custom_entries_stays_in_current_language(self):
        config = self.site / "config.toml"
        text = config.read_text()
        start = text.index("sam_menu = [")
        end = text.index("]\n\nsam_bottom_menu", start) + 1
        config.write_text(text[:start] + text[end:])
        self.write_content("courses/_index.md", 'title = "Courses"')
        self.write_content("courses/_index.cn.md", 'title = "课程"')
        self.build()
        self.assertIn(("课程", BASE + "cn/courses/"), self.links("cn/about", "bottom-menu"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

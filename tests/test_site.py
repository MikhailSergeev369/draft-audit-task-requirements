"""Reading-site regressions: version identity, meaningful diff and local links.
SPDX-License-Identifier: BSD-3-Clause
"""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
spec = importlib.util.spec_from_file_location("audit_site", ROOT / "tools/site.py")
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class ReadingSite(unittest.TestCase):
    def test_print_furniture_is_not_a_text_change(self):
        before = '<table class="ears"><tr><td>Expires Monday [Page]</td></tr></table><p>Same text</p>'
        after = before.replace('Monday', 'Tuesday')
        self.assertEqual(site.reading_blocks(before), ['Same text'])
        self.assertIn('No reading-text changes', site.text_diff(before, after, 'old', 'new'))

    def test_missing_local_resources_fail(self):
        for markup in ('<link rel="stylesheet" href="missing.css">',
                       '<script src="missing.js"></script>', '<img src="missing.png">',
                       '<video poster="missing.png"></video>'):
            with self.subTest(markup=markup), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / 'index.html').write_text(markup)
                with self.assertRaisesRegex(ValueError, 'Broken local link'):
                    site.check_links(root)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<link rel="stylesheet" href="style.css">')
            (root / 'style.css').write_text('/* optional overrides */')
            site.check_links(root)

    def test_diff_ignores_navigation_but_keeps_prose_and_link_targets(self):
        document = ('<html><head><title>ignore</title></head><body>'
                    '<section id="section-toc.1"><p>ignore TOC</p></section>'
                    '<section id="section-boilerplate.1"><p>ignore boilerplate</p></section>'
                    '<h2>4.2. Example</h2><p>not <strong>found</strong>'
                    '<a class="pilcrow" href="#x">¶</a></p>'
                    '<p><a href="https://example.com/a">source</a></p></body></html>')
        blocks = site.reading_blocks(document)
        self.assertEqual(blocks, ['4.2. Example', 'not found', 'source <https://example.com/a>'])
        changes = site.text_diff(document, document.replace('/a"', '/b"'), 'old', 'new')
        self.assertIn('Removed', changes)
        self.assertIn('https://example.com/a', changes)
        self.assertIn('https://example.com/b', changes)

    def test_whitespace_and_preformatted_content(self):
        self.assertEqual(site.reading_blocks('<p> a\n  b<br/>c </p><pre> a\n   b</pre>'), ['a b c', ' a\n   b'])

    def test_nested_lists_and_tables_keep_text(self):
        blocks = site.reading_blocks('<ul><li><p>one</p><ul><li>two</li></ul></li></ul>'
                                    '<table><tr><th>name</th><th>value</th></tr>'
                                    '<tr><td>A</td><td>B</td></tr></table>')
        self.assertEqual(blocks, ['one two', 'name value', 'A B'])

    def test_diff_escapes_text(self):
        result = site.text_diff('<p>before</p>', '<p>&lt;script&gt;bad&lt;/script&gt;</p>', '<old>', '<new>')
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)
        self.assertIn('&lt;old&gt;', result)

    def test_unchanged_text_is_explicit(self):
        self.assertIn('No reading-text changes', site.text_diff('<p>same text</p>', '<p>same\n text</p>', 'old', 'new'))

    def test_pin_configuration_and_invalid_commit(self):
        config = json.loads((ROOT / 'review/candidates.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / 'candidates.json'
            file.write_text(json.dumps(config))
            self.assertEqual(len(site.candidates_config(file)), 1)
            config['candidates'][0]['commit'] = 'main'
            file.write_text(json.dumps(config))
            with self.assertRaises(ValueError):
                site.candidates_config(file)

    def test_local_links_and_missing_fragment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'index.html').write_text('<a href="draft.html#section">read</a>')
            (root / 'draft.html').write_text('<p id="section">text</p>')
            site.check_links(root)
            (root / 'draft.html').write_text('<p id="other">text</p>')
            with self.assertRaisesRegex(ValueError, 'fragment'):
                site.check_links(root)

    def test_links_cannot_escape_site(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'site'
            root.mkdir()
            (Path(tmp) / 'outside.html').write_text('outside')
            (root / 'index.html').write_text('<a href="../outside.html">escape</a>')
            with self.assertRaises(ValueError):
                site.check_links(root)


if __name__ == '__main__':
    unittest.main()

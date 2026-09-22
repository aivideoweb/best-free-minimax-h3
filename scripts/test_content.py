#!/usr/bin/env python3
"""Regression checks that real content drift is rejected, using temporary copies."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ContentGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns('.git', '__pycache__'))

    def tearDown(self):
        self.temp.cleanup()

    def check(self, needle):
        result = subprocess.run([sys.executable, str(self.repo / 'scripts/check_content.py')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(needle, result.stdout + result.stderr)

    def test_recipe_tampering(self):
        p = self.repo / 'prompts/01-brand-advertising.md'
        p.write_text(p.read_text().replace('tall smoked-glass silhouette', 'unrelated plastic bottle'))
        self.check('Source baseline changed')

    def test_image_tampering(self):
        p = self.repo / 'assets/gallery/clay-repair-robot.webp'
        p.write_bytes(p.read_bytes() + b'changed')
        self.check('Source baseline changed')

    def test_translated_spec_drift(self):
        p = self.repo / 'README_ja.md'
        p.write_text(p.read_text().replace('5s / 480p', '15s / 2K', 1))
        self.check('stale output')

    def test_shared_output_drift(self):
        p = self.repo / 'README_zh.md'
        p.write_text(p.read_text().replace('**共同规格：免注册，5 秒 / 480p。**', '**共同规格：免注册，15 秒 / 2K。**'))
        self.check('stale shared output')

    def test_duplicate_html_case_is_rejected(self):
        p = self.repo / 'README.md'
        text = p.read_text()
        import re
        preview = re.search(r'<img src="https://pbs[^>]+>', text).group(0)
        p.write_text(text + '\n' + preview + '\n')
        self.check('expected one inline case preview')

    def test_missing_evidence(self):
        p = self.repo / 'data/tools.json'
        data = json.loads(p.read_text())
        del data['tools'][0]['evidence_method']
        p.write_text(json.dumps(data))
        self.check('missing evidence_method')

    def test_incomplete_evidence_quote(self):
        p = self.repo / 'data/tools.json'
        data = json.loads(p.read_text())
        data['tools'][0]['evidence_quote'] = '480p'
        p.write_text(json.dumps(data))
        self.check('incomplete output evidence')

    def test_affiliate_drift(self):
        p = self.repo / 'README_fr.md'
        p.write_text(p.read_text().replace('20 %', '30 %'))
        self.check('affiliate rate differs')

    def test_missing_relationship_disclosure(self):
        p = self.repo / 'README_zh.md'
        p.write_text(p.read_text().replace('目录中的 13 个工具来自本公司相关品牌', ''))
        self.check('missing verified relationship/status statement')

    def test_workflow_source_connection_is_required(self):
        p = self.repo / 'README_zh.md'
        p.write_text(p.read_text().replace(
            '](./prompts/01-brand-advertising.md#brd-001-midnight-observatory-tea-launch)',
            '](./prompts/01-brand-advertising.md)', 1))
        self.check('missing source-to-practice link')

    def test_duplicate_homepage_gallery_is_rejected(self):
        p = self.repo / 'README.md'
        p.write_text(p.read_text() + '\n![Repeated tea image](./assets/gallery/midnight-observatory-tea.webp)\n')
        self.check('expected one inline reference')

    def test_new_community_practice_is_allowed(self):
        p = self.repo / 'practices/COMM-001.md'
        p.write_text('# COMM-001 One quiet leaf\n\n## Goal\nShow one leaf moving.\n\n## Setup\nText only, 5s, 16:9.\n\n## Prompt\n```text\nA leaf moves gently in a fixed shot; hold the ending.\n```\n\n## Review\nCheck leaf shape.\n\n## Evidence\nStatus: concept\nOriginal test fixture, not generated.\n')
        index = self.repo / 'practices/README.md'
        index.write_text(index.read_text() + '\n[COMM-001](./COMM-001.md)\n')
        result = subprocess.run([sys.executable, str(self.repo / 'scripts/check_content.py')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('1 community practices', result.stdout)


if __name__ == '__main__':
    unittest.main()

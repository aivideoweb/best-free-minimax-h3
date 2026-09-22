#!/usr/bin/env python3
"""Offline checks for reader navigation, catalog parity and evidence boundaries."""
import json
import hashlib
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def anchors(text):
    result = set(re.findall(r'<a\s+id="([^"]+)"', text))
    seen = {}
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, re.M):
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', title).lower()
        slug = ''.join(c for c in title if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        count = seen.get(slug, 0)
        seen[slug] = count + 1
        result.add(slug if not count else f'{slug}-{count}')
    return result


for page in ROOT.rglob('*.md'):
    text = page.read_text()
    for url in re.findall(r'\]\(([^\s)]+)(?:\s+"[^"]*")?\)', text):
        if re.match(r'[a-z]+:', url):
            continue
        path, _, fragment = unquote(url).partition('#')
        target = (page.parent / path).resolve() if path else page
        require(target.exists(), f'{page.relative_to(ROOT)}: missing {url}')
        if target.is_file() and target.suffix == '.md' and fragment:
            require(fragment in anchors(target.read_text()), f'{page.relative_to(ROOT)}: missing anchor {url}')

data = json.loads((ROOT / 'data/tools.json').read_text())
tools = data['tools']
expected = json.loads((ROOT / 'data/upstream-inventory.json').read_text())
urls = {t['url'] for t in tools}
require(len(tools) == len(urls) == 13, 'Expected 13 unique source tools')
require(urls == set(expected['tool_urls']), 'Tool URL set differs from source inventory')
for t in tools:
    require(t['checked_at'] and t['verification'], f'{t["id"]}: missing evidence')
    require(t['verification'] in ['page_read_not_generated', 'indexed_page_only'], f'{t["id"]}: unsupported evidence status')
    require(t['generation_tested'] is False, f'{t["id"]}: generation claim requires a separately reviewed receipt and schema update')
    for field in ['description', 'description_zh', 'caution', 'caution_zh', 'prompt', 'prompt_zh', 'review',
                  'evidence_method', 'evidence_quote', 'access_note', 'aspect_ratios', 'evidence_capture']:
        require(bool(t.get(field)), f'{t["id"]}: missing {field}')
    quote = t.get('evidence_quote', '')
    require('480p' in quote and re.search(r'five[- ]second|5[- ]second|5s', quote), f'{t["id"]}: incomplete output evidence quote')
    require(t.get('aspect_ratios') == ['16:9', '9:16', '1:1'], f'{t["id"]}: unexpected aspect ratios')
    if t.get('evidence_capture') == 'html_hash_recorded':
        require(re.fullmatch(r'[a-f0-9]{64}', t.get('retrieved_html_sha256', '')), f'{t["id"]}: missing HTML hash')
    else:
        require(t.get('evidence_capture') == 'browser_only', f'{t["id"]}: unsupported evidence capture')
    for file in ['docs/tools.md', 'docs/free-tool-prompts.md']:
        require(f'<a id="{t["id"]}"></a>' in (ROOT / file).read_text(), f'{file}: missing {t["id"]}')
    require((ROOT / f'assets/tools/{t["id"]}.svg').exists(), f'{t["id"]}: missing card')
    profile = (ROOT / 'docs/tools.md').read_text().split(f'<a id="{t["id"]}"></a>', 1)[1].split('<a id=', 1)[0]
    require(f'{t["duration_seconds"]}s · {t["resolution"]}' in profile, f'{t["id"]}: profile output differs from tool data')

readmes = [ROOT / 'README.md'] + sorted(ROOT.glob('README_*.md'))
contracts = json.loads((ROOT / 'data/readme-contracts.json').read_text())
affiliate = json.loads((ROOT / 'data/affiliate.json').read_text())
require(len(readmes) == 8, 'Expected eight README entry pages')
for page in readmes:
    text = page.read_text()
    for url in urls:
        require(url in text, f'{page.name}: missing source tool {url}')
    for t in tools:
        rows = [line for line in text.splitlines() if line.startswith('| [') and f']({t["url"]}) |' in line]
        require(len(rows) == 1, f'{page.name}: expected one comparison row for {t["id"]}')
        if rows:
            cells = rows[0].split(' | ')
            expected_output = f'{t["duration_seconds"]} 秒 / {t["resolution"]}' if page.name == 'README_zh.md' else f'{t["duration_seconds"]}s / {t["resolution"]}'
            if page.name in ['README.md', 'README_zh.md']:
                shared = f'**共同规格：免注册，{expected_output}。**' if page.name == 'README_zh.md' else f'**Shared settings: no signup, {expected_output}.**'
                require(shared in text, f'{page.name}: stale shared output for {t["id"]}')
                require(len(cells) == 3, f'{page.name}: expected compact tool row for {t["id"]}')
            else:
                require(cells[2] == expected_output, f'{page.name}: stale output for {t["id"]}')
    for phrase in contracts[page.name]['required_phrases']:
        require(phrase in text, f'{page.name}: missing verified relationship/status statement: {phrase}')
    require('https://videoweb.ai/affiliate-program/' in text, f'{page.name}: missing affiliate link')
    require('https://flaq.ai/affiliate-program/' not in text, f'{page.name}: wrong affiliate brand')
    require('assets/videoweb-free-h3-cinematic.png' in text, f'{page.name}: missing branded hero')
    require('docs/free-tool-prompts.md' in text and 'docs/x-community-showcase.md' in text, f'{page.name}: missing learning routes')
    affiliate_sections = [s for s in text.split('\n## ') if affiliate['program_url'] in s]
    require(len(affiliate_sections) == 1, f'{page.name}: affiliate section missing or duplicated')
    if affiliate_sections:
        section = affiliate_sections[0]
        for rate in [affiliate['first_valid_order_percent'], affiliate['following_valid_order_percent']]:
            require(re.search(rf'(?<!\d){rate}\s*%', section), f'{page.name}: affiliate rate differs from data')
        require(re.search(rf'(?<!\d){affiliate["window_days_after_registration"]}(?!\d)', section), f'{page.name}: affiliate window differs from data')

recipes = []
for page in ROOT.glob('prompts/[0-9]*.md'):
    recipes += re.findall(r'^## ([A-Z]+-\d{3})\b', page.read_text(), re.M)
require(len(recipes) == len(set(recipes)) == 84, 'Expected 84 unique source recipe IDs')
require(set(recipes) == set(expected['recipe_ids']), 'Source recipes were lost or changed')
require(len(list(ROOT.glob('prompts/[0-9]*.md'))) == 24, 'Expected 24 recipe categories')
for path in expected['source_assets']:
    require((ROOT / path).exists(), f'Missing source reference asset: {path}')
for record in expected['inherited_files']:
    path = ROOT / record['path']
    require(path.exists(), f'Missing inherited file: {record["path"]}')
    if path.exists():
        require(hashlib.sha256(path.read_bytes()).hexdigest() == record['accepted_sha256'], f'Source baseline changed: {record["path"]}')

community_ids = set()
practice_index = (ROOT / 'practices/README.md').read_text()
for page in ROOT.glob('practices/COMM-*.md'):
    text = page.read_text()
    match = re.match(r'# (COMM-\d{3})\s+\S', text)
    require(bool(match), f'{page.name}: missing community practice ID and title')
    if match:
        ident = match.group(1)
        require(page.stem == ident and ident not in community_ids, f'{page.name}: duplicate or mismatched practice ID')
        community_ids.add(ident)
    require(f'](./{page.name})' in practice_index, f'{page.name}: missing practice index link')
    for section in ['Goal', 'Setup', 'Prompt', 'Review', 'Evidence']:
        require(f'## {section}\n' in text, f'{page.name}: missing {section} section')
    require('```text\n' in text, f'{page.name}: missing copy-ready prompt block')
    require(re.search(r'Status: (concept|tested)\b', text), f'{page.name}: missing evidence status')
    if 'Status: tested' in text:
        for label in ['Date:', 'Settings:', 'Inputs:', 'Output:', 'Edits:', 'Defects:']:
            require(label in text, f'{page.name}: tested practice missing {label}')

entries = json.loads((ROOT / 'docs/x-community-sources.json').read_text())['entries']
require(len(entries) == 15 and len({e['source_url'] for e in entries}) == 15, 'Expected 15 unique X cases')
gallery = (ROOT / 'docs/x-community-showcase.md').read_text()
for entry in entries:
    for key in ['source_url', 'prompt_url', 'video_url', 'thumbnail_url']:
        require(entry[key] in gallery, f'{entry["id"]}: missing {key} in gallery')
    require('source_text_sha256' in entry and 'inherited_frame_review_source' in entry, f'{entry["id"]}: missing provenance')
    require('no new full playback' in entry['verification'], f'{entry["id"]}: unclear current verification limits')

workflows = json.loads((ROOT / 'data/workflows.json').read_text())
require(workflows['status'] == 'editorial_not_generation_tested', 'Workflow evidence status changed')
known_tools = {t['id'] for t in tools}
require(len(workflows['workflows']) == 6, 'Expected six application workflows')
for workflow in workflows['workflows']:
    require(workflow['primary'] in known_tools, 'Unknown primary workflow tool')
    for role in ['support', 'pickup']:
        require(all(item[0] in known_tools for item in workflow[role]), 'Unknown optional workflow tool')
    for filename in ['README.md', 'README_zh.md']:
        home = (ROOT / filename).read_text()
        require(f'<a id="workflow-{workflow["id"]}"></a>' in home, f'{filename}: missing workflow')
        require('quick-trial' in home, f'{filename}: missing shared trial method')
        section = home.split(f'<a id="workflow-{workflow["id"]}"></a>', 1)[-1].split('<a id="workflow-', 1)[0].split('\n## Explore more prompts', 1)[0].split('\n## 更完整的提示词库', 1)[0]
        require(f'](./assets/gallery/{workflow["image"]})' in section, f'{filename}: workflow reference mismatch')
        require(f'](./prompts/{workflow["recipe"]})' in section, f'{filename}: missing source-to-practice link')
        for case_id in workflow['cases']:
            entry = next(e for e in entries if e['id'] == f'XH3-{case_id:03d}')
            require(entry['thumbnail_url'] in section, f'{filename}: case outside its workflow')
        for category in workflow['categories']:
            require(f'./prompts/{category:02d}-' in section, f'{filename}: category outside its workflow')
        suffix = '_zh' if filename == 'README_zh.md' else ''
        for field in ['name', 'output', 'reason', 'inputs', 'review', 'tags', 'lesson', 'homepage_prompt', 'fix', 'next', 'image_alt']:
            require(workflow[field + suffix] in section, f'{filename}: workflow {workflow["id"]} differs from {field} metadata')
        for role in ['support', 'pickup']:
            for item in workflow[role]:
                require(item[1 if suffix else 2] in section, f'{filename}: workflow role description drift')


# Keep the full visual browse path on both primary homepages.
for filename in ['README.md', 'README_zh.md']:
    home = (ROOT / filename).read_text()
    explicit_ids = re.findall(r'<a id="([^"]+)"></a>', home)
    require(len(explicit_ids) == len(set(explicit_ids)), f'{filename}: duplicate explicit anchor')
    for entry in entries:
        require(len(re.findall(r'(?:\]\(|src=")' + re.escape(entry['thumbnail_url']) + r'(?:\)|")', home)) == 1, f'{filename}: expected one inline case preview {entry["id"]}')
        for field in ['video_url', 'prompt_url']:
            require(entry[field] in home, f'{filename}: missing direct {field} for {entry["id"]}')
    for path in ROOT.glob('prompts/[0-9]*.md'):
        require(f'./prompts/{path.name}' in home, f'{filename}: missing category {path.name}')
    for path in ROOT.glob('assets/gallery/*.webp'):
        require(len(re.findall(r'(?:\]\(|src=")\./assets/gallery/' + re.escape(path.name) + r'(?:\)|")', home)) == 1, f'{filename}: expected one inline reference {path.name}')
    require(home.count('```text\n') >= 4, f'{filename}: missing copy-ready homepage practice')
    require(home.count('.gif)](') >= 3, f'{filename}: missing official motion previews')

for svg in ROOT.rglob('*.svg'):
    try:
        ElementTree.parse(svg)
    except ElementTree.ParseError as exc:
        errors.append(f'Invalid SVG {svg}: {exc}')

require('Flaq AI' in (ROOT / 'LICENSE').read_text(), 'Missing source MIT attribution')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: 13 tools, 8 README entry pages, 84 source recipes, 24 categories, 15 X cases, {len(community_ids)} community practices; local links, anchors, artwork and provenance checked.')

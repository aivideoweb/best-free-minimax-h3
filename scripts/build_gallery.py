"""Build public gallery data from the maintained case and workflow catalogs."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
entries = json.loads((ROOT / 'docs/x-community-sources.json').read_text())['entries']
workflows = json.loads((ROOT / 'data/workflows.json').read_text())['workflows']
fields = ['id', 'title', 'title_zh', 'author', 'source_url', 'prompt_url', 'video_url', 'thumbnail_url', 'lesson', 'lesson_zh']
data = {'entries': [{key: entry[key] for key in fields} for entry in entries], 'workflows': [{key: w[key] for key in ['id', 'name', 'name_zh', 'cases']} for w in workflows]}
(ROOT / 'site/cases.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f'Gallery: {len(entries)} cases, {len(workflows)} workflows')

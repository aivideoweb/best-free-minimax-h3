# Maintaining the free H3 directory

[Home](../README.md) · [Contributing](../CONTRIBUTING.md)

## Tool changes

1. Open the exact free URL. Record the date, access method, any redirect and what the current page says about signup, cost, input images, output duration and resolution.
2. Edit `data/tools.json`. Use null for unknown size or duration; do not infer it from another brand. Keep page claims separate from `generation_tested`.
3. Update the entry in `docs/tools.md` and every translated README. Keep the same URL set across all eight entry pages. Update a localized usage description when it becomes inaccurate.
4. For a generation test, record prompt, input rights, selected settings, queue time, output link and observed defects. Check downloadable output metadata before promoting a page-only record to a tested record.
5. Review differences with `python3 scripts/check_content.py`. Record a dated change in `CHANGELOG.md`.

This directory currently covers the 13 exact source URLs. To add an unrelated service, disclose ownership, explain its relevance and document its actual free route. A free trial, signup credit or paid API is not automatically equivalent to a no-signup free generator.

## X video changes

Find a concrete original X post, not just a search summary. Check author, model statement, complete-prompt location and attached media. If the prompt is in a reply, link the reply separately. Add unique records to `docs/x-community-sources.json` and the bilingual gallery, including a short excerpt, practical lesson, required inputs and verification limits. Link creator media remotely and preserve creator rights. A third-party reader is not a native X authenticated read. Do not carry forward an old frame-review claim as a fresh full playback.

When a direct MP4 fails, check the original post before replacing the URL. If a post is deleted, mark it unavailable and remove the broken preview; retain the source identifier in the history. Do not silently substitute another creator’s clip.

## Routine checks

- Before recommending a tool: recheck access and current free conditions.
- Before a documentation release: check local links, all tool rows, translated entry pages and changed media URLs.
- When changing affiliate language: use the VideoWeb program’s current agreement; do not copy another brand’s conditions.
- After upstream changes: compare the source cookbook, preserve attribution and review whether its longer recipes need a free-tool adaptation.

No automatic generation, recurring task or scheduled network job is enabled by this document. GitHub Actions runs the local content validator on changes.

## Source baseline and synchronized facts

`data/upstream-inventory.json` records the source commit and SHA-256 checksums for 24 recipe files, 12 source visuals and eight supporting guides/templates. The checker compares the accepted local bytes, not just file existence. An intentional edit needs a reviewed baseline update and an explicit adaptation note; keep the original source hash.

The tool manifest is the authority for output rows. The checker compares every README tool row and each detailed profile with its duration/resolution and rejects old indexed-only or unconfirmed status. Keep translated descriptions human-edited. `data/affiliate.json` is the authority for the displayed commission rates and attribution period; all eight README affiliate sections must match. Recheck the live agreement before updating this data.

Run `python3 scripts/test_content.py` after changing the validator. Its regression cases intentionally corrupt source text, images, translated specifications, evidence and affiliate terms in a temporary copy to ensure the checks reject them.


## Application workflow updates

The English and Chinese homepages use six editorial workflows. Update `data/workflows.json` and both README pages together when changing a primary tool, optional support/pickup role, input requirement, review rule or example. A workflow role is not a measured capability advantage. Keep the 5s / 480p page limits and page-only evidence status separate from creative role assignments. Preserve existing section anchors when moving prompts.

The homepage learning route is source reference → one technique → five-second text adaptation → tool entry → review/fix → optional assembly. Keep `image`, `recipe`, `lesson`, `homepage_prompt`, `fix`, `next`, `cases` and `categories` synchronized across the workflow manifest and English/Chinese homepages. Each inherited gallery image appears once per homepage; distribute case cards and category links inside workflows rather than appending a second gallery. The first-form screenshot and original room practice live in `docs/first-clip.md` and `docs/first-clip_zh.md`. Homepage adaptations are untested editorial briefs, separate from the 13 standalone practices and 84 source recipes.

Keep reader-facing prose focused on the task: use “提示词” or “示例” in Chinese and “prompt” or “example” in English. Put adaptation history and source inventory in provenance records, with attribution in the homepage credits. State page-only verification and untested generation clearly once rather than repeating warnings in every tool role. Preserve required credits and meaningful evidence checks when polishing wording.

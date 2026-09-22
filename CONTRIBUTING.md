# Contributing to Best Free MiniMax H3 Tools

VideoWeb AI maintains this directory. Contributions can improve free-tool information, short-shot practice and attributed video examples. The **84 Flaq AI recipes are an inherited reference layer**, not the destination for new VideoWeb prompts. New practice and external creator cases are counted separately.

## Choose a contribution path

| Contribution | Where it belongs | What to include |
|---|---|---|
| Correct one of the 13 tools | `data/tools.json`, its profile and all eight README tables | Exact URL, date, page/FAQ evidence, current limits and relationship disclosure |
| Improve an existing short practice | Prompt fields in `data/tools.json` and `docs/free-tool-prompts.md` | Copy-ready English and Chinese text, one short action, input requirements and review points |
| Add an original short practice | A new `practices/COMM-NNN.md` file and the `practices/README.md` index | Follow the independent format below; do not add a source-category ID |
| Report an X example | Video gallery and its source manifest | Creator, original post, full-prompt link, media, required inputs and evidence limits |
| Correct inherited source material | Open an issue explaining the problem | A maintainer reviews the source and accepted hash baseline before any inherited file changes |

Use the [short-practice proposal form](https://github.com/aivideoweb/best-free-minimax-h3/issues/new?template=prompt-proposal.yml) for ideas and the [tool or video form](https://github.com/aivideoweb/best-free-minimax-h3/issues/new?template=tool-update.yml) for factual corrections. Finished videos are optional for **concept** prompts.

## Independent short-practice format

Create `practices/COMM-001.md` using the next unused number, and link it from [the practice index](./practices/README.md). `COMM` identifies community-authored practice; it is separate from the 84 inherited recipe IDs and the 13 initial tool practices. Use one five-second text-only shot or a clearly explained start/end image pair. State when actual form settings must be rechecked.

The file must have these headings:

````markdown
# COMM-001 Your specific shot title

## Goal
What the viewer should understand in one short shot.

## Setup
Exact free tool URL, target 5 seconds, aspect ratio, text only or both frames.
State which inputs the contributor must supply and their rights.

## Prompt
```text
A complete prompt with opening, action, camera and ending.
```

## Review
What could go wrong and what to inspect in the output.

## Evidence
Status: concept
Author and source/rights statement. No generation has been performed.
````

Write original wording. An English version is sufficient for a new community submission; a Chinese adaptation is welcome and should preserve the same setup. Do not place borrowed X prompt wording in this original-practice section.

For tested practice, replace `Status: concept` with `Status: tested` and include the submitted prompt plus the labels `Date:`, `Settings:`, `Inputs:`, `Output:`, `Edits:` and `Defects:` with actual evidence. Do not identify the backend as verified unless you have evidence beyond a provider label. A tested practice does not automatically promote the directory’s page-level tool record to a tested service rating.

## Source material and media

Do not append new BRD/PRD or other source-category recipes under `prompts/`. Those 24 files, 12 source images and eight reference documents are protected by a reviewed hash baseline. If an inherited example has a factual defect, open an issue; maintainers can make a documented correction while retaining the original source hash and updating the accepted adaptation hash.

For X cases, keep the author credit, link the complete original prompt and mark excerpts as excerpts. External media remain with their creators and outside the repository MIT license. Remote links are preferred; do not mirror media without permission. Official model facts need primary sources.

For original submissions, provide rights-cleared wording and inputs. Do not submit private data, credentials, copied prompts, misleading testimonials or fabricated test results. Existing creator credits in the attributed gallery must remain intact.

## Before a pull request

- Link new practice files from their index and keep IDs unique.
- Record facts in [tool data](./data/tools.json); synchronize all affected language tables and [profiles](./docs/tools.md).
- Run `python3 scripts/check_content.py` and `python3 scripts/test_content.py`.
- Update the [changelog](./CHANGELOG.md), describe the reader benefit, and identify untested claims.

The current public promise is exactly the source’s 13 related-brand tools. Proposals for additional services are welcome as issues; maintainers must review their free route and ownership, then update the directory scope, data, counts, translated disclosures and validation contracts together. Do not simply append an unrelated tool while leaving “all are our company brands” in the README.

Similarly, new X cases require a reviewed gallery-count update and unique source records. See [maintenance instructions](./docs/maintenance.md). Submitting original repository content permits its distribution under the [MIT license](./LICENSE); this does not relicense external linked media.

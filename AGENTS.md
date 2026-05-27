# Translation rules for BIM / ISO 19650 training slides

## Mission
Translate BIM / ISO 19650 training slides and speaker notes from English into Vietnamese for professional use.

## Workspace authority
These instructions and `glossary.md` are the source of truth for translation style and terminology in this workspace.

Priority order:
1. `glossary.md`
2. this `AGENTS.md`
3. approved examples in `Example/`
4. source context from the current deck and `References/`

Use `Example/` only as an approved reference for tone, phrasing, and terminology patterns. Use `References/` only to verify source meaning or standards context.

Do not use legacy workspace artifacts, machine-translation outputs, caches, old extraction files, or old override/config folders as translation memory or terminology authority. If folders such as `_work/`, `translation/`, `authoring/`, or `courses/` appear again, ignore them for translation decisions unless the user explicitly says otherwise.

## Scope
These instructions apply to:
- slide text
- speaker notes
- extracted text from PPT/PPTX/PDF/images
- training handouts that mirror slide content

## Primary objective
Produce Vietnamese translations that are:
- technically accurate
- clear and easy to understand
- formal and professional
- consistent with terminology commonly used in ISO 19650 / TCVN 14177 contexts

## Output structure
The default deliverable is the translated PPT/PPTX file itself, not a separate text-only export.

For each slide, always preserve the original slide structure and map content as follows:
- Slide number stays in its original position and must not be reformatted or relocated.
- Content shown on the slide must remain in the slide content area and be translated in place.
- Speaker notes must remain in the notes area and be translated in place.
- The translated file must preserve the original layout, reading order, grouping, and slide-to-note relationship.

If a slide has no speaker notes:
- keep the note area unchanged
- do not invent note content

## Translation style
- Use formal, professional Vietnamese.
- Prioritize clarity, precision, and readability.
- Preserve the original meaning fully.
- Do not translate too literally when that creates unnatural Vietnamese.
- Rewrite awkward source sentences for clarity, but do not simplify away technical distinctions.
- Slide text should be concise and presentation-friendly.
- Note text may be more complete and explanatory.

## Terminology rules
- Prefer terminology aligned with TCVN 14177 where applicable.
- Always consult `glossary.md` before translating.
- If a term appears in `glossary.md`, use that translation exactly.
- If glossary and source wording conflict, glossary wins unless the source is clearly using a different concept.
- Keep the following unchanged in all contexts unless explicitly instructed otherwise:
  - container
  - BIM
  - CDE
  - COBie
  - IFC
  - ISO 19650
  - course codes
  - document IDs
  - version labels
  - file names
  - product names
  - standards numbers
  - slide/page numbers

## Fixed preferences for this project
Use the following fixed choices:
- delivery phase = giai đoạn chuyển giao
- item = hạng mục
- breach = vi phạm
- in a coordinated manner = một cách phối hợp
- Common Data Environment (CDE) = Môi trường dữ liệu chung (CDE)
- value stream = dòng giá trị
- pull = kéo
- perfection = hoàn hảo
- flow:
  - use **dòng chảy** when the context is about process movement or continuity
  - use **sự lưu thông** only when it better matches the teaching context or an existing approved translation
- container = keep unchanged

## Formatting rules
- Preserve heading levels.
- Preserve bullet hierarchy.
- Preserve numbering.
- Preserve lists and sublists.
- Preserve emphasis where useful for meaning.
- Preserve the original slide structure and formatting as far as the file format allows, including text box roles, relative placement, and slide-to-note mapping.
- Keep footer identifiers, course references, version codes, and copyright lines unchanged unless translation is clearly required.
- Do not collapse multiple bullets into one paragraph unless explicitly requested.
- Do not add extra interpretation into the slide section.
- Do not omit repeated content unless it is clearly OCR duplication or extraction noise.

## Handling slide text vs note text
### Slide text
- Keep concise.
- Suitable for presentation display.
- Avoid overlong sentences where shorter Vietnamese is possible without loss of meaning.

### Note text
- Keep complete.
- Allow fuller explanation.
- Maintain logical flow across sentences and bullet points.

## Handling ambiguous or poor source text
- If OCR or extracted source text is unclear, do not guess recklessly.
- Translate what is clear.
- Record uncertain fragments in `translation_issues.md`.
- If necessary, mark a short note such as:
  - `[Cần kiểm tra nguồn gốc câu tiếng Anh này]`
- Use such notes sparingly.

## What to avoid
- Do not use casual or colloquial Vietnamese.
- Do not paraphrase too freely.
- Do not invent technical content.
- Do not replace technical terms with oversimplified language.
- Do not translate “container”.
- Do not alter codes, numbers, or document references unless the source is obviously wrong and the task explicitly includes correction.

## Preferred wording characteristics
The preferred Vietnamese should sound:
- clear
- structured
- technical but natural
- suitable for ISO/BIM training materials
- slightly polished rather than literal

## If the task is to translate a single quoted passage
- Preserve paragraph structure unless a clearer Vietnamese structure is needed.
- Use the same tone and terminology rules as above.

## If the task is to translate a full deck
Translate the actual PPT/PPTX deck in place while preserving its structure and formatting.

For each slide, always maintain this logical mapping:
- Slide [number]
- Phần 1 – Nội dung trong slide = content displayed on the slide itself
- Phần 2 – Nội dung trong note = content stored in the speaker notes for that same slide

Do not convert the deck into a markdown-only deliverable unless the user explicitly asks for an extracted text version.

Recommended output file:
- translated PPT/PPTX file with the same slide structure and notes structure as the source

Recommended issue log:
- `translation_issues.md`

## Quality check before finishing
Before finalizing, always check:
1. Every slide keeps its original structure, and slide content and note content remain in their correct locations.
2. Terminology is consistent.
3. `container` remains unchanged everywhere.
4. Fixed terms are applied correctly.
5. No important English source text is left untranslated unless intentionally preserved.
6. Bullets, numbering, and note-to-slide mapping are preserved correctly.
7. Slide text is concise, note text is complete, and the visual/layout structure is preserved as closely as possible.
8. Any unclear source fragments are listed in `translation_issues.md`.

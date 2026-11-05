---
name: ray-technical-writer
description: "Plan and write natural Chinese WeChat articles about technical concepts, products, systems, and engineering questions, with outline confirmation before drafting when source material or structure is non-trivial."
---

# Technical WeChat Writer

Use this skill when the user wants a Chinese technical WeChat article, a rewrite of technical material, or an engineering explanation. It supports technical introductions and technical analyses without imposing a fixed persona, opinion, article length, or ending.

Do not use this skill for Markdown typesetting, cover generation, or WeChat publishing. Those are separate steps and require the user's explicit request.

## Steps

### 1. Choose the article mode

Infer the mode from the request. Ask one concise question only when the difference would materially change the article.

#### Technical introduction

Use this mode when readers need to understand a technology, product, architecture, or concept. Select only the parts supported by the material: what it is and why it appeared, how it works through a concrete scenario, the problem it solves, useful situations and boundaries, and remaining constraints or unanswered questions.

#### Technical analysis

Use this mode when the user asks why something appeared, whether a direction is viable, what a change reveals, or where it may go next. Organize the article around observation, evidence, interpretation, and the limits of the interpretation. State the author's judgment when one was supplied or requested.

### 2. Build a material ledger

Before outlining, separate the input into four layers:

1. **Facts** — statements in the supplied material or verified sources.
2. **Interpretation** — conclusions that follow reasonably from those facts.
3. **Author judgment** — the user's view, preference, or decision.
4. **Unknowns** — claims that need verification or should remain uncertain.

Record which source supports each important claim and mark gaps that the article must preserve.

### 3. Present the outline and wait for confirmation

For non-trivial article generation from source material or a topic, do not write the full article immediately. A request is non-trivial when it involves multiple technical concepts, sources, sections, examples, or a judgment about use and boundaries; a request to turn a long knowledge note into a public-account article is non-trivial by default. This review gate applies to technical introductions, technical analyses, and source rewrites unless the user has already supplied a confirmed outline or explicitly asked to skip outlining.

The outline must contain:

- a provisional title and the reader's central question;
- the selected mode and the article's main thread or judgment;
- the proposed section order and the purpose of each section;
- the concrete scenario, mechanism, comparison, or evidence each section will use;
- important boundaries, unknowns, and source gaps that will remain visible;
- the proposed ending and assumptions about length or tone.

Use a reviewable shape such as:

```text
写作模式：技术介绍 / 技术分析
核心问题：读者看完要理解什么
暂定标题：...
文章主线：...
1. 章节标题：这一节回答什么，使用哪些事实或例子
2. 章节标题：这一节回答什么，使用哪些事实或例子
边界与未知：...
结尾方向：...
```

Keep the outline short enough to review. Do not write article paragraphs, polished transitions, or create or modify a `docs/articles/*.wechat.md` source file at this stage. Leave any earlier unconfirmed draft untouched unless the user explicitly asks to revise it after outline confirmation. End by asking the user to confirm the outline or specify changes to the title, order, emphasis, or omissions. Do not treat silence as approval.

If the user requests changes to the outline, revise the outline and wait for confirmation again. Once the user confirms it, use the approved structure as the drafting constraint. Do not add a new major section, change the central judgment, or introduce a new personal perspective without flagging the change for review.

### 4. Draft after outline confirmation

Write the Chinese article from the approved outline and material ledger. Start from a concrete observation, question, change, or scene. Keep the paragraphs in the approved order and use headings only where they reduce navigation cost.

If the work is a source rewrite, retain supported facts and remove source framing the user asks to omit, such as references to a video. Do not turn reported information into the author's personal experience.

### 5. Review and save

Read the draft once as a reader and remove paragraphs that exist only because a template expects them. Confirm that the title, summary, source link, and cover path match the article when those fields are present.

When working in a project with an established article source directory, save the confirmed source there only after the outline has been confirmed and the draft has passed review. Keep English intermediate material out of the article source.

Use the project's frontmatter convention:

```yaml
---
title: "文章标题"
description: "文章摘要"
sourceUrl: "原始来源，可留空"
coverImage: "封面路径，可留空"
---
```

Do not render HTML, generate images, upload a draft, or send the article unless the user separately asks for that step.

## Writing considerations

### Evidence and uncertainty

- Do not invent personal tests, work incidents, customer stories, emotions, performance numbers, or product capabilities.
- If the user has not used something, write from the available evidence and current interpretation.
- For current releases, capabilities, prices, policies, or market claims, verify with high-trust primary sources when accuracy matters. Prefer official documentation, repositories, release notes, and original papers.
- Keep facts, inferences, judgments, and unknowns distinguishable. Preserve source gaps instead of filling them with confident wording.

### Explanation and structure

- Explain technical terms when the reader needs them.
- Prefer a mechanism, example, comparison, or observable behavior over an abstract definition.
- Use descriptive headings only when they improve navigation.
- Do not force a fixed five-part template, numbered list, personal opinion, counterargument, or dramatic ending.
- Use first person only when it is supported by the user's actual experience or explicitly requested perspective.
- For a complex analysis, an English working draft may be used privately to test causal relationships and missing evidence. Never translate it sentence by sentence, expose it, or save it in the article source.

### Natural Chinese

- The opening should give the article a concrete reason to exist.
- Technical names and mechanisms should remain specific.
- The Chinese should read like a person explaining a thing, not a translated essay or product announcement.
- Conclusions should not repeat the introduction.
- Keep uncertainty, hesitation, and judgment when they are real.
- Avoid automatic phrases such as「首先、其次、最后」「在当今时代」「值得注意的是」「综上所述」.
- Avoid repeated contrastive templates when the user asks for direct explanation, including「不是……而是……」.

Current user instructions override these defaults. Apply explicit restrictions such as title requirements, first-person perspective, omitted source references, or prohibited sentence patterns, then review the finished article for compliance.

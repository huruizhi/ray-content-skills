# Ray Content Skills

**A collection of five Codex skills for technical writing, Obsidian Markdown, and publishing to GitHub Pages or WeChat.**

Use the skills individually, or follow the path below. They help structure the article and its evidence; they do not replace the author's judgment or publish without an explicit request.

<p align="center">
  <img src="./assets/readme/content-workflow.svg" width="100%" alt="Ray Content Skills workflow: plan the article, write and polish it, then publish to GitHub Pages or save a WeChat draft">
</p>

## Workflow

| Stage | Skill | What it does |
|---|---|---|
| Plan and draft | [`ray-technical-writer`](skills/ray-technical-writer/SKILL.md) | Interviews the author, builds a reviewable outline, and writes a Chinese technical article from supplied material. |
| Polish | [`ray-tone`](skills/ray-tone/SKILL.md) | Improves clarity and natural flow while preserving supported facts, uncertainty, and author intent. |
| Write Obsidian notes | [`ray-obsidian-markdown`](skills/ray-obsidian-markdown/SKILL.md) | Creates and edits Obsidian Markdown with wikilinks, embeds, callouts, properties, and other vault syntax. |
| Publish to a blog | [`ray-publish-github`](skills/ray-publish-github/SKILL.md) | Adapts the article for a Jekyll GitHub Pages site, pushes only with authorization, and verifies the live post. |
| Save to WeChat | [`ray-post-to-wechat`](skills/ray-post-to-wechat/SKILL.md) | Renders Markdown and saves an article to the Official Account draft box via API or browser. |

The two publishing skills are separate endpoints. GitHub Pages publication does not publish to WeChat, and saving a WeChat draft does not send it to readers. The WeChat skill's browser or API setup depends on the account and local environment.

## Install

Clone the repository, then copy the skills you want into your Codex skills directory:

```bash
git clone https://github.com/huruizhi/ray-content-skills.git
cd ray-content-skills
cp -R skills/ray-technical-writer ~/.codex/skills/
cp -R skills/ray-tone ~/.codex/skills/
cp -R skills/ray-obsidian-markdown ~/.codex/skills/
cp -R skills/ray-publish-github ~/.codex/skills/
cp -R skills/ray-post-to-wechat ~/.codex/skills/
```

Restart or refresh the Codex session if it does not discover the new skills immediately.

## Use

Invoke a skill by name:

```text
$ray-technical-writer 帮我把这个技术主题整理成文章提纲
$ray-tone 润色这篇草稿
$ray-obsidian-markdown 帮我整理这篇 Obsidian 笔记并补齐内部链接
$ray-publish-github 把已确认的文章适配并发布到 GitHub Pages
$ray-post-to-wechat 把文章保存到公众号草稿箱
```

For a substantial article, `ray-technical-writer` presents an outline for review before drafting. The publishing skills keep their own confirmation and verification steps; a draft, a deployed blog post, and a WeChat mass-send are distinct outcomes.

## Contents and attribution

- `skills/ray-technical-writer/` — article planning and drafting.
- `skills/ray-tone/` — editorial guidance and an optional tone lint script.
- `skills/ray-obsidian-markdown/` — Obsidian Flavored Markdown reference and authoring workflow.
- `skills/ray-publish-github/` — Jekyll Pages publishing guidance and a live-site verification script.
- `skills/ray-post-to-wechat/` — WeChat article guidance, scripts, and setup references.

`ray-post-to-wechat` is adapted from [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills). It retains the upstream MIT license in its skill directory and uses upstream dependencies and compatible Baoyu configuration locations.

Credentials, browser profiles, and account-specific configuration belong in local environment variables or ignored configuration files. Do not commit them.

Ray-authored skill content has no blanket license. The MIT license in `skills/ray-post-to-wechat/LICENSE` applies to the upstream material covered by that license.

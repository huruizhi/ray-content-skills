# Ray Content Skills

A small set of Codex skills for planning, writing, polishing, and publishing Chinese technical articles.

## Skills

| Skill | Purpose |
|---|---|
| [`ray-technical-writer`](skills/ray-technical-writer/SKILL.md) | Interview the author, shape an outline, and write Chinese technical articles with evidence boundaries. |
| [`ray-tone`](skills/ray-tone/SKILL.md) | Polish Chinese or English copy for natural flow, clarity, and factual accuracy. |
| [`ray-publish-github`](skills/ray-publish-github/SKILL.md) | Adapt WeChat articles for Jekyll GitHub Pages, publish, and verify the live result. |
| [`ray-post-to-wechat`](skills/ray-post-to-wechat/SKILL.md) | Render and save articles to a WeChat Official Account draft through API or browser. |

## Install

Copy any skill directory into the Codex skills folder:

```bash
cp -R skills/ray-technical-writer ~/.codex/skills/
cp -R skills/ray-tone ~/.codex/skills/
cp -R skills/ray-publish-github ~/.codex/skills/
cp -R skills/ray-post-to-wechat ~/.codex/skills/
```

Then invoke a skill by name, for example:

```text
$ray-technical-writer 帮我把这个技术主题整理成文章提纲
$ray-tone 润色这篇草稿
$ray-publish-github 发布这篇文章到 GitHub Pages
$ray-post-to-wechat 保存到公众号草稿箱
```

## Attribution and configuration

`ray-post-to-wechat` is adapted from [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills), which is licensed under MIT. Its upstream license is included in that skill directory. The implementation retains compatibility with the upstream Baoyu configuration locations and npm dependencies.

The skills contain no account credentials or user-specific configuration. Set service credentials locally with environment variables or ignored configuration files; never commit secrets, browser profiles, tokens, or account data.

## License

No blanket license is granted for the original Ray-authored skill content in this repository. `ray-post-to-wechat` includes upstream material under the license in its own directory.

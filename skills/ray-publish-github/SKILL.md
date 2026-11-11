---
name: ray-publish-github
description: Publish or synchronize WeChat-derived technical articles to an existing Jekyll GitHub Pages blog, including Markdown adaptation, assets, Git push, Pages deployment monitoring, and live readback. Use when the user asks to publish or update Blog posts on GitHub Pages; do not use for WeChat draft publication itself.
---

# Publish GitHub Pages Blog

把公众号技术内容适配为可长期检索的 Jekyll Blog 文章，并以“线上可访问”为发布完成标准。保留文章事实、证据链接、代码、图片与不确定性边界；不要把排版迁移变成无依据的重写。

## 授权边界

- 检查、转换、预览和验证可以先进行；`git push` 是对外发布，只有用户本次明确要求发布、推送或确认发布时才执行。
- 用户只要求准备文章时，新稿写入 Jekyll `_drafts/`，不要提前放进 `_posts/`；现有文章的更新稿放在独立 staging 文件或隔离 worktree。停在本地文件和验证结果，不创建仓库、不推送、不修改 Pages 设置。获得确认后才把新稿移入 `_posts/YYYY-MM-DD-slug.md`，或把已确认的更新覆盖到既有文章。
- 本 Skill 不上传公众号草稿，也不群发微信文章。用户同时要求公众号发布时，另按项目约定使用相应发布 Skill。
- 保留工作区中无关改动；提交前只暂存本次 Blog 发布涉及的文件。

## 发现项目

先读取当前项目的 `AGENTS.md`、Blog `README.md`、站点 `_config.yml` 和目标仓库状态。不要假设所有项目路径相同。

在 `wechat-official-account` 项目中，当前默认结构是：

- 公众号内容源：`docs/articles/*.wechat.md`
- 独立 Blog 仓库：`github-pages/`
- Jekyll 文章：`github-pages/_posts/YYYY-MM-DD-slug.md`
- 静态资源：`github-pages/assets/images/`
- 线上站点：从 Blog README、Git remote 或 Pages 配置确认；不要假设固定域名。

这些是项目默认值，不是跨项目硬编码。路径或仓库变化时，以实际文件和 remote 为准。

## 文章适配

文章需要实质改写时，先读取并使用 [ray-technical-writer](../ray-technical-writer/SKILL.md)：按适用范围确认大纲或既有稿件的修改范围，完成起草、`ray-tone` 整体优化、`lieflat-less-ai-tone` 检测，以及用户接受建议后的局部修改、复测与前后对照。复用已完成的检查和用户对相应建议的授权；适配过程再次实质改写正文时，重新检查改动后的稿件。依赖缺失时明确报告尚未完成的环节，不能宣称文风检查通过。只修 front matter、链接或资源路径时不必启动文风检查流程。

1. 明确本次要同步的文章集合。优先用 Blog front matter 的 `wechat_source` 对照源文件；历史文章没有该字段时，再结合源文件编号、日期、来源 URL、标题和正文证据推断。若“最近一篇”很可能已经上线，先报告对应文章并确认是准备更新稿，还是改选下一篇未同步文章，不得直接生成重复文章。
2. 为 Blog 文章补齐 Jekyll front matter：
   - `layout: post`
   - `title`
   - 带时区的 `date`，当前项目使用 `+0800`
   - `categories`、`tags`
   - 一句可独立理解的 `description`
   - 稳定的源文件标识 `wechat_source: docs/articles/<file>.wechat.md`
   - 源文存在 `sourceUrl` 时映射为 `source_url`，不要在改写时丢失
3. 适配正文而不是机械复制：
   - 标题可改得更适合搜索和网页阅读，但不能夸大结论。
   - 删除只服务公众号编辑器的 front matter，例如空 `coverImage`；保留有用的来源链接。
   - 保留代码、引用、外链和证据限制。来源未自行验证时，继续明确说明。
   - 图片从 `imgs/...` 迁移到站点 `assets/images/...`，正文使用能在 Pages 根路径正确解析的 URL。
   - 不插入“已发布”“扫码关注”等制作说明；公众号入口由站点共享组件负责。
   - 适配前后核对外链、代码块和图片引用清单；数量变化必须能由删除重复内容、合并段落或用户要求解释。
4. 只有首页确实需要最新文章的特定证据组件时，才添加 `evidence_label`、`evidence_caption`、`evidence_steps` 等站点字段。普通文章不为凑版式伪造证据。
5. 不改既有 permalink 规则，不批量重命名已发布文章，除非用户明确接受 URL 变化。

## 发布前验证

在 Blog 仓库中至少完成：

- front matter 可解析；
- 新增图片存在，Markdown 中引用路径正确；
- `git diff --check` 通过；
- 查看 `git diff`，确认没有无关文件、凭据、预览缓存或过程截图进入提交；
- 若本地 Jekyll 已可用，渲染代表性首页和文章；不可用时不要为普通发布擅自安装全局依赖，改用 Pages 的真实构建验证。

Blog 主题或布局只有在用户明确要求设计变更时才使用 `oil-ui`。日常发文复用现有布局，不重复设计首页。

## 推送与 Pages 部署

获得发布授权后：

1. 确认 remote、当前分支和目标 Pages 仓库；不要把公众号主仓库误推到 Pages 仓库。
2. 只暂存本次文章和对应资源，提交信息说明实际发布内容。
3. 推送当前 Pages 分支。若 upstream 未配置，显式指定 remote 与 branch。
4. 记录推送后的 HEAD SHA，并用 `gh run list` 找到该 SHA 对应的 `pages build and deployment`；run 尚未出现时做有界轮询，例如最多等待 2 分钟并逐步拉长间隔。超时就报告本次 run 尚未出现，不要把旧的成功 run 当成本次结果。
5. 用 `gh run watch <run-id> --exit-status` 等待构建和部署结束。构建成功但部署仍排队时继续等待；失败时读取失败步骤，修复后重新发布。

不要绕过 Pages 构建、审批或仓库保护规则。没有成功的 deploy 结果时，不得宣称发布完成。

## 线上回读

部署成功后，从真实站点验证：

- 首页 HTTP 200，且能发现新文章；
- 每篇本次发布文章 HTTP 200；
- 本次新增图片、二维码等关键资源 HTTP 200；
- 文章正文和标题是新版本，不只是 CDN 中的旧页面；必要时加无副作用的查询参数避开缓存；
- 修改了共享布局或样式时，补看桌面和手机代表画面；只发文章时，不要求重新做整站视觉评审。

可运行随 Skill 提供的只读脚本：

```bash
python3 <skill-dir>/scripts/verify_pages.py \
  --base-url https://<owner>.github.io/ \
  --posts-dir _posts \
  --expect-all-posts-on-homepage \
  --post-url /ai/agent/2026/10/27/agent-self-modifying-and-resume/ \
  --post-contains '/ai/agent/2026/10/27/agent-self-modifying-and-resume/::Agent 改了自己的代码' \
  --asset /assets/images/wechat-qrcode.png \
  --cache-bust <commit-sha>
```

脚本会核对首页、从首页提取的文章链接、指定文章正文和静态资源。只有当前首页确实展示全部文章时，才加 `--expect-all-posts-on-homepage` 将首页链接数与 `_posts` 数量做精确比对；站点启用分页后不要使用这个开关。脚本不能替代对新文章正文的人工回读。

## 交付报告

只报告已验证的结果：

- 发布了哪些文章，以及线上地址；
- Pages run 是否 build 与 deploy 均成功；
- 首页、文章和关键资源的线上检查结果；
- commit SHA；
- 未完成或未验证的项目，例如本地未渲染、CDN 尚未刷新或用户未授权推送。

“文件已创建”“已提交”或“已推送”都不等于“已发布”。

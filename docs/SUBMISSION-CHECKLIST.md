# 课程提交对照清单

对照作业缺失清单逐项登记。线上英文入口：https://illusion-error.github.io/tonight-anime-site/en/ ；中文版本：https://illusion-error.github.io/tonight-anime-site/ 。

## 已完成

| 优先级 | 缺失项 | 状态 | 落点与说明 |
| --- | --- | --- | --- |
| 高 | Open Graph 身份信息 | 已完成 | 全站 48 个页面 `<head>` 均含 `og:title`、`og:description`、`og:image`、`og:url`，另含 `og:type`、`og:locale`、`og:site_name`、`twitter:card`。`og:image` 与 `og:url` 为绝对地址。 |
| 高 | 网站图标 | 已完成 | `favicon-32.png`（32×32）、`apple-touch-icon.png`（180×180，兼作 app icon）、`og-cover.jpg`（1200×630），位于 `site/assets/icons/`；页面已用 `<link rel="icon">` 与 `<link rel="apple-touch-icon">` 引用。 |
| 高 | 提交用五张图片 | 已完成 | 见下表，尺寸均按课程规格裁切/生成。 |
| 高 | 英文提交入口 | 已完成 | 提交英文版地址 `/en/`；中文保留为语言版本。README 已注明课程提交以英文版为准。 |
| 中 | 部署结构说明 | 已完成 | README「仓库结构（两个仓库）」一节：`web-course-project` 为课程源码/过程仓（私有，Git 历史以此为准），`tonight-anime-site` 为 Pages 发布仓（公开，仅静态成品副本）。 |
| 低 | 旧 Django 草稿 | 已完成 | 早期 Django 初稿已备份到项目目录外 `../anime-site-django-draft-backup/`，并从课程项目目录移出；未纳入版本库与发布目录。 |

## 提交用五张图片

| 用途 | 文件 | 规格 |
| --- | --- | --- |
| Cover image | `site/assets/icons/og-cover.jpg` | 1200 × 630 JPEG |
| Desktop screenshot | `docs/screenshots/desktop-home.png` | 1920 × 1080 PNG |
| Mobile screenshot | `docs/screenshots/mobile-home.png` | 375 × 812 PNG |
| App icon | `site/assets/icons/apple-touch-icon.png` | 180 × 180 PNG |
| Favicon | `site/assets/icons/favicon-32.png` | 32 × 32 PNG |

## 需人工 / 后续完成（无法由脚本代做）

### 1. 真实手机验收（中优先级）

需在实体手机上分别用**移动数据网络**与**校园 Wi‑Fi**各打开一次英文版 `https://illusion-error.github.io/tonight-anime-site/en/`，逐项确认：

- 导航：Home / Discover / Watchlist / About 可点击，当前页高亮正确。
- 搜索：在 Discover 输入作品名（中文/英文/日文原名）能过滤出对应卡片。
- 筛选：题材、心情下拉可联合筛选；清除条件后回到全部二十部。
- 收藏：卡片或详情页加入想看，清单计数增加，刷新后保留；移除与清空生效。
- 详情直链：从卡片进入详情页，海报、简介、推荐理由、官方来源链接正常；面包屑可返回。
- 布局：无横向滚动条，文字与海报不被裁切，菜单在窄屏可操作。

### 2. Git 持续过程（中优先级）

课程要求“每周逐步发展”的真实历史，**不能补造、不能修改提交时间**。后续每周做一次真实的小改动（文案、样式、修复或新增条目），跑 `python scripts/check_site.py` 与 `node --test scripts/test-watchlist.cjs` 通过后提交，并能向老师解释每次提交改了什么、为什么。

## 检查边界

- 本地回归：`check_site.py` 48 页 / 1186 处内部链接资源全存在；收藏单测 5 项通过。
- 本轮未做实体手机移动网络验收，也未运行独立 HTML 校验器；响应式结论来自浏览器视口检查。

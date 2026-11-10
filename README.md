# 今晚看什么 · Anime Tonight

面向动漫观众的精选指南：按题材与心情浏览二十部作品，阅读无剧透介绍，并把想看的故事保存到本地清单。

## 在线访问

- 英文版本（提交入口）：https://illusion-error.github.io/tonight-anime-site/en/
- 中文版本：https://illusion-error.github.io/tonight-anime-site/

站点为中英双语，页内导航可在两种语言间切换。

## 内容与功能

- 二十部精选动漫，每部含无剧透简介、推荐理由、适合人群与观看前提示。
- 按题材与心情浏览，支持名称搜索与题材、心情联合筛选。
- 想看清单：加入、移除、清空，仅保存在当前浏览器。
- 卡片与详情页使用作品官方海报/主视觉；首页背景为自制的月亮、山峦与星空装饰图形。
- 响应式布局，适配桌面与手机屏幕；采用语义化标记与键盘可达设计。

## 技术方案

原生 HTML / CSS / JavaScript 多页静态站点，无需后端服务或数据库。页面由 `scripts/` 下的生成脚本从中英文案底稿产出，成品位于 `site/` 目录。

## 仓库结构

- **源码仓库** `web-course-project`（私有）：生成脚本、中英文案底稿、文档与站点成品。
- **发布仓库** `tonight-anime-site`（公开）：仅包含 `site/` 内的静态 HTML/CSS/JS、海报与图标，以及 `.nojekyll`；GitHub Pages 从 `main` 根目录部署，是线上成品的发布副本。

改动先在源码仓库完成、测试并提交，再把 `site/` 同步到发布仓库；仅推送源码仓库不会自动更新网页。

## 提交材料（五张图片）

| 用途 | 文件 | 规格 |
| --- | --- | --- |
| Cover image（Open Graph 封面） | `site/assets/icons/og-cover.jpg` | 1200 × 630 JPEG |
| Desktop screenshot（桌面首页） | `docs/screenshots/desktop-home.png` | 1920 × 1080 PNG |
| Mobile screenshot（手机首页） | `docs/screenshots/mobile-home.png` | 375 × 812 PNG |
| App icon（apple-touch-icon） | `site/assets/icons/apple-touch-icon.png` | 180 × 180 PNG，方角由系统裁切 |
| Favicon | `site/assets/icons/favicon-32.png` | 32 × 32 PNG |

每个页面 `<head>` 均包含 `og:title`、`og:description`、`og:image`、`og:url`（另含 `og:type`、`og:locale`、`twitter:card`），并引用上述 favicon 与 apple-touch-icon。

想看清单仅保存在同一浏览器、同一来源，不会跨设备或跨来源同步。

[课程提交对照清单](docs/SUBMISSION-CHECKLIST.md)。

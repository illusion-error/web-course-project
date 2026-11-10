# 今晚看什么 · 网站课程项目

面向动漫观众的精选指南：通过题材与心情寻找作品，阅读无剧透介绍并保存想看清单。

- [正式课程要求](docs/COURSE-REQUIREMENTS.md)
- [详细实施计划与验收任务](docs/IMPLEMENTATION-PLAN.md)
- [二十部作品完整资料（中英双语底稿）](docs/ANIME-COLLECTION-20.md)
- [早期六部作品资料](docs/ANIME-SITE-CONTENT.md)
- [开发记录](docs/DEVLOG.md)
- [课程提交对照清单](docs/SUBMISSION-CHECKLIST.md)

采用原生 HTML/CSS/JavaScript 多页静态方案，无需后端或数据库。发布目录为 site/。目录收录二十部作品，提供中英双语：各 4 个公共页与 20 个详情页；卡片与详情页使用作品官方海报/主视觉，首页背景为自制装饰图形。已完成三种视口的布局检查及键盘基础检查。搜索与联合筛选已完成（批次 C）；收藏、移除、清空和本地保存已完成（批次 D）；已通过 GitHub Pages 正式上线；真实手机及浏览器原生 200% 缩放仍待验收。

本地预览：`python -m http.server 8000 --bind 127.0.0.1 --directory site`，打开 http://127.0.0.1:8000/ 。

- [批次 B 检查记录](docs/BATCH-B-RESULTS.md)
- [桌面首页截图](docs/screenshots/b-home-desktop.png)
- [手机尺寸详情截图](docs/screenshots/b-detail-mobile.png)

《我推的孩子》已从内容目录替换为《夏目友人帐》。早期 Django 初稿不属于静态成品，已备份到项目目录外的 `../anime-site-django-draft-backup/`，未纳入版本库与发布目录。Git 历史保留真实过程。

- [批次 C 实现与验收记录](docs/BATCH-C-RESULTS.md)

- [批次 D 验收记录](docs/BATCH-D-RESULTS.md)

## 公网访问

- 英文提交入口（课程系统提交此地址）：https://illusion-error.github.io/tonight-anime-site/en/
- 中文语言版本：https://illusion-error.github.io/tonight-anime-site/

站点为中英双语，导航可在两种语言间切换。课程提交说明与展示以英文版为准，中文版作为语言版本保留。

## 仓库结构（两个仓库）

- **课程源码 / 过程仓库**：`web-course-project`（私有，origin）。保存生成脚本、中英文案底稿、文档、`site/` 生成结果与完整 Git 历史。课程要求的“每周逐步发展”的真实提交过程以本仓库为准，答辩展示本仓库历史。
- **Pages 发布仓库**：`tonight-anime-site`（公开）。只包含 `site/` 内的静态 HTML/CSS/JS、海报与图标，以及 `.nojekyll`；GitHub Pages 从 `main` 根目录部署。该仓库是线上成品的发布副本，不代表课程开发过程。

修改流程：先在源码仓库完成改动、测试并提交，再把 `site/` 同步到发布仓库；仅推送源码仓库不会自动更新网页。

## 课程提交材料（五张图片）

| 用途 | 文件 | 规格 |
| --- | --- | --- |
| Cover image（Open Graph 封面） | `site/assets/icons/og-cover.jpg` | 1200 × 630 JPEG |
| Desktop screenshot（桌面首页） | `docs/screenshots/desktop-home.png` | 1920 × 1080 PNG |
| Mobile screenshot（手机首页） | `docs/screenshots/mobile-home.png` | 375 × 812 PNG |
| App icon（apple-touch-icon） | `site/assets/icons/apple-touch-icon.png` | 180 × 180 PNG，方角由系统裁切 |
| Favicon | `site/assets/icons/favicon-32.png` | 32 × 32 PNG |

每个页面 `<head>` 均包含 `og:title`、`og:description`、`og:image`、`og:url`（另含 `og:type`、`og:locale`、`twitter:card`），并引用上述 favicon 与 apple-touch-icon。

[上线验收、部署更新方法与检查边界](docs/BATCH-E-RESULTS.md)。收藏仅保存在同一浏览器、同一来源，localhost 收藏不会自动迁移到公网。

# 今晚看什么 · 网站课程项目

面向动漫观众的精选指南：通过题材与心情寻找作品，阅读无剧透介绍并保存想看清单。

- [正式课程要求](docs/COURSE-REQUIREMENTS.md)
- [详细实施计划与验收任务](docs/IMPLEMENTATION-PLAN.md)
- [五页内容与六部作品资料](docs/ANIME-SITE-CONTENT.md)
- [开发记录](docs/DEVLOG.md)

采用原生 HTML/CSS/JavaScript 多页静态方案，无需后端或数据库。发布目录为 site/。已实现十个静态页面与统一视觉，完成三种视口的布局检查及键盘基础检查。搜索与联合筛选已完成（批次 C）；收藏、移除、清空和本地保存已完成（批次 D）；已通过 GitHub Pages 正式上线；真实手机及浏览器原生 200% 缩放仍待验收。

本地预览：`python -m http.server 8000 --bind 127.0.0.1 --directory site`，打开 http://127.0.0.1:8000/ 。

- [批次 B 检查记录](docs/BATCH-B-RESULTS.md)
- [桌面首页截图](docs/screenshots/b-home-desktop.png)
- [手机尺寸详情截图](docs/screenshots/b-detail-mobile.png)

《我推的孩子》已从内容目录替换为《夏目友人帐》。旧 Django 初稿暂留但不继续开发、不进入发布目录。Git 历史保留真实过程。

- [批次 C 实现与验收记录](docs/BATCH-C-RESULTS.md)

- [批次 D 验收记录](docs/BATCH-D-RESULTS.md)

## 公网访问

https://illusion-error.github.io/tonight-anime-site/

仅 site/ 静态内容发布到公开仓库 [tonight-anime-site](https://github.com/illusion-error/tonight-anime-site)。当前开发仓库保持私有，课程 Git 过程以此仓库为准。

[上线验收、部署更新方法与检查边界](docs/BATCH-E-RESULTS.md)。收藏仅保存在同一浏览器、同一来源，localhost 收藏不会自动迁移到公网。

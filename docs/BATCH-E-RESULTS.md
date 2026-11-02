# 批次 E：测试与上线

验收日期：2026-11-02（Asia/Shanghai）。

正式地址：https://illusion-error.github.io/tonight-anime-site/
发布仓库：https://github.com/illusion-error/tonight-anime-site
发布提交：0eff8c367392424b3b78849a37f9cfc090c3b2b5
开发仓库仍为私有 web-course-project，保留原有完整开发历史。

## 发布方式

GitHub 对原私有仓库返回 422：当前套餐不支持 Pages。没有修改原仓库可见性。另建公开发布仓库，只包含 site/ 内的 16 个 HTML/CSS/JS 文件及 .nojekyll。Pages 从 main 根目录部署，https_enforced=true，构建结果 built。

之后修改须先在开发仓库完成，再同步 site/ 到发布仓库；仅推送开发仓库不会自动更新网页。发布仓库不代表课程开发过程，答辩应展示原开发仓库的 Git 历史。

本机发布副本位于 .local-qa/publish（已忽略）。现有文件更新可用 PowerShell：

```powershell
python scripts/build_static.py
python scripts/check_site.py
node --test scripts/test-watchlist.cjs
Copy-Item -Path site/* -Destination .local-qa/publish -Recurse -Force
git -C .local-qa/publish add .
git -C .local-qa/publish commit -m "Update static website"
git -C .local-qa/publish push origin main
```

若删掉网站文件，还需在发布仓库中同步删除对应已废弃文件，以上 Copy-Item 不会自动删除旧文件。勿复制项目根目录、私有文档或环境配置。

## 检查结果

- python scripts/check_site.py：10 页、188 处内部链接/资源/锚点全部存在。
- node --test scripts/test-watchlist.cjs：5 项通过。
- HTTPS 独立请求：根首页、10 个 HTML、6 个 CSS/JS，共 17 个请求全部 HTTP 200。忽略 Git 的 CRLF/LF 转换后，内容全部与本地一致。明细见 LIVE-CHECK.json。
- 无需登录 GitHub 即可读取上述公网地址；请求保留默认 TLS 证书校验。
- 内置浏览器逐页打开全部 10 页，标题与正文正常，采集的控制台 error 日志为空。
- 芙莉莲详情直链打开并刷新正常；其余五个详情直链也分别在浏览器打开并通过 HTTPS 请求检查。
- 线上搜索“夏目”得到 1 部；加入想看后清单显示 1 部，刷新仍保留，移除后为 0 部。测试收藏已清理。
- 公网与 localhost 属于不同来源，收藏不会自动迁移。

## 外部来源与检查边界

官方来源：宇宙更远的地方、摇曳露营返回 200；芙莉莲、排球少年、间谍过家家自动请求返回 403；夏目官网 TLS 握手超时。这些请求未能证明后三类链接失效，因此保留原官方来源，不能声称全部外链通过。

本机系统代理一度造成 TLS EOF；改用直接 HTTPS 请求且保留证书验证后，本站 17 个请求通过。浏览器首次导航超时后，实际完成加载并逐页检查成功。

本次未使用实体手机移动网络，也未完成独立 HTML 校验器验证；此前响应式检查是浏览器视口检查。以上项目不标记为已完成。

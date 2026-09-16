# 网站课程：从 0 到交付的可执行规划

> 执行路线已更新：请优先使用 [个人博客执行清单](BLOG-EXECUTION-CHECKLIST.zh-CN.md)。用户已说明有基础、老师允许 Codex 辅助并需兼顾考研，因此直接构建 Django 博客，不再按本文先学习和先静态后动态的路线推进。本文保留课程证据与概念说明。

本文件是建设规划，不是已完成网站的说明。依据：用户提供的七张课程图片；技术资料见末尾。主题、时间预算与技术路线是建议，不能当成教师硬性规定。

## 1. 先判断课程到底要求什么

| 图片证据 | 能确认的内容 | 对项目的实际影响 |
| --- | --- | --- |
| 图 1：8 次课、9 周 | 1–3 次理解 Web 并手写；第 4 次布局及 AI agent；5–6 次行为与整合；7–8 次运行、提交、答辩 | 按课次逐步构建，保存过程证据 |
| 图 2：评分草案 | Process 20%、Project 40%、Written exam 25%、Defence 15%；明确尚未批准 | 不能把比例视为最终成绩规则；四类准备都要做 |
| 图 2：项目描述 | structure、layout、behaviour、live | 要有结构、布局、可用交互和可访问线上版本 |
| 图 2：过程与答辩 | Git 历史体现逐周成长，五分钟解释自己的决策 | 不能最后一次性上传；要理解自己提交的代码 |
| 图 3、4 与图 5 | 响应式、可访问性、用户体验及浏览器差异 | 必须从使用者角度检查手机、桌面和键盘操作 |
| 图 5 | 部署、DNS/URL、网络、缓存、CDN、安全、版本和迁移等教学议题 | 应理解并选择适用实现；不等于每个项目必须自建 CDN、数据库或翻译系统 |
| 图 6、7 | 缓存、源站、内容更新的课堂转写 | 可帮助理解请求链路；自动转写不作为精确要求 |

没有看到的明确要求：必须 Python、必须 Vue、必须 Django、必须数据库、必须登录注册、必须自建服务器。也没有确切截止日期、最低页面数或最终评分细则。

建议在下一次课向老师核实：

> Does “behaviour” require client-side JavaScript only, or also server-side code and database persistence? Are Django and Vue allowed? What are the final submission, hosting and AI-use requirements?

课程图片中的“手写”和 AI 加入课次是课程信息，而不是对本次助手的直接命令。本次先做规划；学生提交时应核实 AI 使用边界，真实记录本次辅助。

## 2. “动态”不是页面会动

| 类型 | 具体例子 | 数据在哪里 | 是否必须后端 |
| --- | --- | --- | --- |
| 静态展示 | 预先写好的文章 HTML | 服务器上的文件 | 否 |
| 浏览器交互 | 搜索已有文章、切换主题、展开菜单 | 浏览器内存、已下载 JSON | 否 |
| 本地持久化 | 收藏文章，刷新后仍在 | 当前浏览器 localStorage | 否；不能自动跨设备共享 |
| 服务端动态 | 管理员后台发文，所有读者看到新内容 | 服务器数据库 | 是，或使用具有此能力的托管服务 |

静态托管的网站也可以有丰富 JavaScript 交互。使用 Vue 不自动意味着有后端；Python 是语言，Django 是 Python 的 Web 框架，Vue 是界面框架，因此“Python + Vue”和“Django”不是同一层级的二选一。

动态博客的一次请求：浏览器 GET /posts/my-note/ → Django URL 路由 → view 查询已发布文章 → 数据库返回结果 → template 生成 HTML → 浏览器展示。管理员通过表单新增文章时，服务器先验证登录、权限和数据，再写入数据库。

后台发布后，另一台设备刷新能看见新文章，是容易演示的服务端动态证据。动画、随机数字、localStorage 收藏都不能代替这个证据。基础概念参考 [MDN 服务端入门](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Introduction)。

## 3. 技术选择与范围

推荐路线：原生 HTML/CSS/JavaScript 打好课程基础；需要完整动态博客时接入 Django 模板和数据库；第一版不做前后端分离。

| 方案 | 学习成本与适用情况 | 本项目建议 |
| --- | --- | --- |
| 原生 HTML/CSS/JS | 直接练结构、布局、DOM、事件和请求 | 前三次课的主线；若老师只要求前端，可以成为最终方案 |
| Django 模板 + 原生 JS | 一套项目处理页面、表单、数据库、登录后台 | 完整动态版首选 |
| Vue + Django API | 多出接口设计、状态管理、前端构建、鉴权与部署整合 | 有明确 SPA 需求或课后扩展再做 |

Vue 本身支持渐进式使用；此处暂不采用属于项目范围决策，并非 Vue 无法适用。参见 [Vue 官方简介](https://cn.vuejs.org/guide/introduction)。

Django 版本建议选择 5.2 LTS 系列的最新补丁并锁定实际安装版本。当前电脑检测到 Python 3.14.0；Django 5.2 从 5.2.8 开始支持 Python 3.14，因此安装约束可用 `Django>=5.2.8,<5.3`，上线前同时更新 Python 的维护补丁。参见 [Django 5.2 发布说明](https://docs.djangoproject.com/en/dev/releases/5.2/) 和 [官方版本页](https://www.djangoproject.com/download/)。

本地数据库先用 SQLite；上线选择托管 PostgreSQL，或者在明确支持持久化磁盘的单实例环境使用 SQLite。不要把数据库放到每次部署会被清空的临时文件系统。

## 4. 建什么：学习笔记与项目展示站

建议名称：DevNotes。它对应你的已有前端经验，内容可以真实积累，容易解释“谁在用、解决什么问题”。名称和主题以后可以调整。

目标用户：想快速了解你项目的老师、同学；查找特定技术笔记的读者；负责维护内容的你。

三条主要路径：读者从首页找到文章并收藏；老师从项目列表查看实现与复盘；管理员发布笔记且不改页面代码。

| 页面 | 内容和操作 | 可验证结果 |
| --- | --- | --- |
| 首页 `/` | 简介、精选项目、最近文章、明确导航 | 新访客能判断用途并进入内容 |
| 文章 `/posts/` | 标题、摘要、分类、搜索、分页或适量列表 | 关键词和分类共同生效，无结果有提示 |
| 详情 `/posts/<slug>/` | 标题、日期、正文、分类、收藏、返回入口 | 深层链接直接打开，排版适合阅读 |
| 项目 `/projects/` | 2–3 个项目，问题、方案、结果、仓库入口 | 链接有效，能看见真实实现和反思 |
| 关于 `/about/` | 作者介绍、网站目标、技术选择 | 信息真实，避免不必要个人信息 |
| 管理 `/admin/` | 动态版：管理员增改文章、发布草稿 | 匿名不能管理，发布后公开可见 |
| 404 | 不存在页面提示和返回入口 | 返回真正的 404 状态码（动态版） |

内容预算：先准备 6 篇短文、3 个分类、2 个项目案例。不堆占位文本；文章可以写 HTTP、布局、DOM、Git 或本项目排错过程。

首版必做：响应式页面、文章浏览、搜索/筛选、收藏、错误与空状态、真实内容、部署、过程记录。动态扩展必做：后台文章 CRUD、发布状态、数据库读取和权限验证。

暂不做：开放注册、评论、聊天、支付、复杂富文本、多人协作、实时通知。它们会引入额外权限、审核和运维工作，不能替代课程核心质量。

## 5. 前端实现顺序

1. 画五页低保真草图，先定义导航与主要按钮。
2. 手写语义 HTML：header/nav/main/article/footer；输入框配 label，操作用 button，导航用 a。
3. 定义少量 CSS 变量：颜色、字号、间距、边框、内容宽度。用系统字体，减少外部字体依赖。
4. 从窄屏一列开始，再用 Grid/Flex 扩展；正文建议最大宽度约 70ch。
5. 以内容是否拥挤决定断点，检查 360、768、1440px 和 200% 缩放。
6. 先实现菜单与搜索，再实现分类、收藏。每个功能完成后用键盘操作一次。
7. 若用 fetch 读取 articles.json，增加 loading/error/empty 状态；JSON 是静态数据文件，不称为数据库。
8. 收藏只保存文章 ID，捕获存储异常；界面说明“保存在此浏览器”，不承诺跨设备同步。

搜索验收：匹配标题或摘要；前后空格被去除；英文忽略大小写；中文正常；空查询返回全部；无匹配提示可清除筛选。动态版用 URL 查询参数 `?q=css&category=web`，使筛选可以分享和返回。

状态设计：按钮有焦点和禁用态；加载时告知正在加载；失败给重试；没有数据给下一步操作。减少动画，尊重 prefers-reduced-motion。禁用 JS 后动态版基本文章浏览仍应可用。

## 6. Django 版的文件与数据设计

以下为目标结构，现在仓库仅包含文档与忽略规则。

```text
web-course-project/
  README.md
  docs/
  prototype/               # 手写前端阶段，作为真实学习过程保留
  backend/
    manage.py
    config/               # settings、根 urls、wsgi
    blog/
      models.py
      views.py
      urls.py
      admin.py
      migrations/
      tests.py
    templates/
      base.html
      blog/
      404.html
    static/
      css/
      js/
      images/
  requirements.txt
  .env.example             # 只有变量名和占位值
```

| 模型 | 建议字段 | 约束 |
| --- | --- | --- |
| Category | name、slug | slug 唯一 |
| Post | title、slug、excerpt、body、category、status、published_at、created_at、updated_at | slug 唯一；status 仅 draft/published；发布必须有发布时间 |

Category 到 Post 是一对多；先允许文章分类为空，删除分类使用 SET_NULL，避免连带删除文章。公开列表和详情使用同一“已发布且发布时间不晚于当前时间”的过滤规则。不要只在列表隐藏草稿却开放详情直链。

正文首版使用纯文本并由模板自动转义，可保留换行；不把用户输入标为 safe。后续引入 Markdown 时再单独评估 HTML 清洗。项目案例首版可写模板，无需为每一页创建表。

| 路由 | HTTP | 服务端行为 |
| --- | --- | --- |
| `/` | GET | 展示近期已发布文章 |
| `/posts/` | GET | 验证查询参数，ORM 筛选，按发布时间及 ID 稳定排序，分页 |
| `/posts/<slug>/` | GET | 查询公开文章；无结果返回 404 |
| `/projects/`、`/about/` | GET | 渲染对应模板 |
| `/admin/` | GET/POST | Django 内置认证、权限和管理表单 |

第一版无须设计 REST API。收藏仍可由浏览器保存。若将来换成 Vue，才逐步添加文章列表与详情 JSON 接口。

## 7. Windows 上的具体起步命令

这些命令是后续实施步骤，本次没有替你执行 Django 安装或生成作业代码。仅在空的目标位置首次执行创建命令。

前端阶段：在仓库创建 prototype，手写 index.html 和 styles.css 后，在仓库根目录执行：

```powershell
python -m http.server 8000 --bind 127.0.0.1 --directory prototype
```

浏览器打开 `http://127.0.0.1:8000/`；不要把这个开发服务器用作正式部署。

接入后端时，在仓库根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install "Django>=5.2.8,<5.3"
New-Item -ItemType Directory -Path backend
.\.venv\Scripts\python.exe -m django startproject config backend
Set-Location backend
..\.venv\Scripts\python.exe manage.py startapp blog
```

接着手动完成：settings 的 INSTALLED_APPS 加 blog；设置 templates 路径、语言及时区；在 blog/models.py 定义模型；admin.py 注册；blog/urls.py 定义路由并在 config/urls.py 引入；逐步编写 views 和模板。每步先确认自己能解释其作用。

```powershell
..\.venv\Scripts\python.exe manage.py makemigrations blog
..\.venv\Scripts\python.exe manage.py migrate
..\.venv\Scripts\python.exe manage.py createsuperuser
..\.venv\Scripts\python.exe manage.py runserver
```

访问后台创建一篇草稿、一篇已发布文章；连接前台列表与详情。完成后在另一个终端的 backend 目录锁定实际依赖：

```powershell
..\.venv\Scripts\python.exe -m pip freeze | Set-Content -Encoding utf8 ..\requirements.txt
```

迁移文件提交 Git，数据库文件与管理员密码不提交。`.env` 不会被 Django 自动读取：部署可直接使用平台环境变量，代码通过 os.environ 读取；若要加载本地 .env，需明确引入并配置相应库。

官方逐步教程：[Django 入门](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)。

## 8. 九周推进表与完成门槛

这是建议的日历周安排；截图没有给出每次课的日期，实际要根据老师安排对齐。按每周 5–8 小时估计，整体约 45–72 小时，基础薄弱或出现部署问题时需要缓冲。

| 周 | 对应课程阶段 | 具体任务 | 必须留下的成果 |
| --- | --- | --- | --- |
| 1 | 第 1 次课附近 | 核实要求；确定主题；准备文章；手写首页 HTML；了解请求与响应 | 需求记录、页面草图、首页、真实提交 |
| 2 | 第 2 次课附近 | 手写文章列表和详情，正确链接、图片和表单标签 | 无 CSS 也可理解的页面结构 |
| 3 | 第 3 次课附近 | 补齐项目/关于页；学习选择器、盒模型、基础排版；核对 AI 规则 | 完整内容结构；能解释路径与 CSS |
| 4 | 第 4 次课附近 | Grid/Flex、响应式、统一样式、焦点；按规则开始 AI 辅助 | 手机/桌面截图、布局修改记录 |
| 5 | 第 5 次课附近 | 搜索、筛选、收藏、菜单与异常状态；部署可交互前端 | 可运行核心前端；明确是否必须后端 |
| 6 | 第 6 次课附近 | 需要后端则接 Django、模型、后台、列表/详情；否则强化前端测试 | 动态版后台发布闭环或完善前端版 |
| 7 | 运行阶段 | 尽早正式部署；环境变量、数据库持久化、权限、HTTPS | 他人设备可访问；动态版重启不丢数据 |
| 8 | 提交与答辩准备 | 功能冻结；修复缺陷；备份恢复；补 README、测试证据 | 可从干净环境重建；完整交付包 |
| 9 | 缓冲与最终考核 | 依据实际日期提交，练习五分钟答辩与代码诊断 | 最终版本标签、演示与说明 |

每次开发节奏：10 分钟写目标 → 60–90 分钟完成一个小功能 → 20 分钟检查正常与失败路径 → 10 分钟记录与提交。

决策门槛：若最终要求只需前端且第 5 周核心功能还不稳定，暂停后端扩展，把时间投入可访问性、运行可靠性和答辩。若数据库属于必做，应在要求明确后立即给后端留出两周，并削减收藏之外的非核心功能。

## 9. 部署：仓库不等于正在运行的网站

GitHub 保存源码和历史；托管平台运行网站。GitHub Pages 是静态托管，不能直接运行 Django 的 Python 服务。其前端可以请求其他后端，但后端仍需要独立运行环境。参见 [GitHub Pages 官方说明](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)。

纯前端方案：选择课程指定的静态平台；若用 Pages，核实账号与私有仓库的发布资格、子路径资源地址和线上可见性。仓库私有不自动代表网站私有。没有要求时先用平台分配域名，无需先买域名。

动态方案：优先支持 Python Web 服务、环境变量、HTTPS、日志和持久数据库的托管环境，同一域名服务模板和静态资源；部署平台在落实时核实当前套餐、休眠和存储条件，不预设永久免费。

动态部署执行顺序：

1. 根据实际平台选择 Python 运行时，安装 requirements 中的锁定依赖。
2. 配置 SECRET_KEY、DEBUG=False、ALLOWED_HOSTS 与数据库连接；settings 显式读取变量。
3. 若选择 PostgreSQL，安装并锁定驱动，按平台连接参数配置 DATABASES。
4. 配置 STATIC_ROOT 与生产静态文件服务，例如平台静态资源功能或明确配置的中间件。
5. 在受控部署步骤运行 migrate 和 collectstatic；迁移前备份已有数据库。
6. 使用平台支持的生产 WSGI/ASGI 服务启动 config.wsgi 或 config.asgi；不使用 runserver。
7. 开启 HTTPS，按实际代理环境配置安全 Cookie 和可信来源；不盲目复制代理安全头配置。
8. 创建管理员，准备演示文章；管理员凭据不写入仓库或公开 README。
9. 从手机网络访问首页和文章深层链接；在后台发布新文章，再从另一浏览器验证。
10. 重启及重新部署一次，确认数据保留；做一次备份恢复演练。

部署检查命令（使用生产配置与对应环境变量）：`python manage.py check --deploy`。逐项解释和处理警告，检查通过也不代表所有业务权限已经正确。参见 [Django 部署清单](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)。

缓存先保持简单：静态资源版本化；后台、登录和写请求不得由共享缓存公开复用；初版动态页面不额外做复杂缓存。图中转写关于 CDN“全球相同速度”的描述不应当作保证，实际仍受网络和节点影响。

## 10. 安全、测试和排错要落在具体功能上

安全落实：后台权限交给 Django 并验证配置；写入用 POST 和 CSRF；ORM 查询避免拼接 SQL；模板保持转义；服务器验证字段；不上传密钥。Django 提供防护机制，但错误使用模板或权限仍会产生漏洞。参见 [Django 安全说明](https://docs.djangoproject.com/en/5.2/topics/security/)。

| 检查 | 操作 | 预期 |
| --- | --- | --- |
| 发布过滤 | 建立草稿、未来发布和已发布文章，分别访问列表与直链 | 仅已到发布时间的公开文章可见 |
| 搜索 | 中文、空白、无结果、分类组合 | 结果正确，空态明确 |
| 404 | 输入不存在的 slug | 404 页面及状态码 |
| 权限 | 未登录访问后台及写入口 | 要求登录，不能写数据 |
| XSS | 在测试文章中输入脚本字符串 | 显示文本，不执行脚本 |
| CSRF | 测试客户端启用 enforce_csrf_checks，省略令牌提交 | 拒绝不合法写入 |
| 响应式 | 手机、桌面、键盘与缩放测试 | 可读、可操作，无内容遮挡 |
| 网络 | 开发工具模拟慢网或失败 | 若有异步加载，出现正确状态及重试入口 |
| 持久化 | 发布文章后重启并重新部署 | 内容仍在 |

自动测试优先覆盖公开查询、草稿不可访问、筛选和后台权限，不为简单 CSS 写大量形式化测试。动态版执行 `python manage.py test` 和 `python manage.py check`；浏览器检查补足视觉与真实操作。

排错顺序：浏览器 Console 看脚本错误 → Network 看请求 URL、状态码和响应 → 服务日志看异常 → 数据库确认内容状态 → 环境变量和静态路径。例：页面空白不能马上重装依赖；先判断是 JS 崩溃、模板异常还是请求失败。

## 11. Git 过程与交付

每个完成的小目标提交一次，不按代码行数或固定次数凑提交。示例提交名：`feat: add semantic article page`、`style: adapt navigation to mobile`、`fix: exclude draft posts from public detail`。这些是未来示例，不是已发生记录。

建议日常流程：

```powershell
git status
git diff
# 检查后按实际文件添加，不上传环境文件与数据库
git add README.md docs
git commit -m "docs: record actual progress and decisions"
git push
```

代码阶段把示例中的文件列表替换成实际修改文件。提交信息可中文或英文，保持能描述目的。不要为了评分修改提交时间或伪造学习过程。

交付包：仓库地址、可访问网站地址、准确 README、功能与限制说明、依赖与运行步骤、测试记录、真实开发日志、最终版本标签（如 v1.0.0）。如果仓库保持私有，按老师要求邀请访问；公开变更另行决定。

## 12. 五分钟答辩与笔试准备

| 时间 | 内容 |
| --- | --- |
| 0:00–0:40 | 服务谁、解决什么问题 |
| 0:40–1:40 | 演示查找文章、收藏和手机布局 |
| 1:40–2:40 | 动态版演示后台发布、另一个浏览器查看；前端版解释数据来自哪里 |
| 2:40–3:40 | 说明请求链路、技术选择与一个关键实现 |
| 3:40–4:30 | 展示一个真实 bug 的诊断和修复及测试证据 |
| 4:30–5:00 | 说明限制、AI 使用情况和下一步 |

每周选择一段自己写的代码，口头解释输入、输出、执行过程和失败情况。笔试练习：定位错误 HTML 嵌套、CSS 选择器与溢出、JS 事件绑定、fetch 错误处理、URL 相对路径；后端路线再补 GET/POST、模板转义、查询过滤及权限。

最终应能回答：为什么这里用按钮而不是 div？为什么手机布局变化？数据保存在哪？刷新和另一台设备访问有什么差别？为什么没有选择 Vue 分离架构？管理员更新文章如何到达读者？你如何确认修复有效？

## 13. 今天开始的三个动作

1. 把第 1 节英文问题发给老师或当面问清，收到正式要求后更新文档。
2. 在 30 分钟内列出 6 篇真实文章题目、2 个项目和五页导航草图。
3. 按当前课次允许的方式手写第一版首页，浏览器检查，然后提交并记录。先完成一次小而完整的开发闭环。

本规划的“100”指可运行、可验收、可交付并能解释的完整过程，不是承诺课程满分。

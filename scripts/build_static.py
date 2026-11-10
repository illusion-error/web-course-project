"""Regenerate the Chinese static HTML from the twenty-title collection (stdlib only)."""
from pathlib import Path
import re
import json
from english_copy import STORIES
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'
BASE = 'https://illusion-error.github.io/tonight-anime-site'
(OUT / 'anime').mkdir(parents=True, exist_ok=True)
text = (ROOT / 'docs/ANIME-COLLECTION-20.md').read_text(encoding='utf-8')
items = []
for number, title, body in re.findall(r'### (\d{2}) ([^\n]+)\n(.*?)(?=\n### |\n## 后续接入|\Z)', text, re.S):
    d = dict(re.findall(r'^- ([^：\n]+)：([^\n]+)', body, re.M))
    d.update(number=number, title=title.strip())
    items.append(d)
assert len(items) == 20, f'expected 20 titles, got {len(items)}'

GENRES = ['奇幻冒险', '日常户外', '青春成长', '运动竞技', '家庭喜剧', '妖怪人情']
MOODS = ['想放松', '想被鼓励', '想看热血', '想慢慢品味']

(OUT / 'assets/js').mkdir(parents=True, exist_ok=True)
catalog = [dict(id=d['slug'], title=d['title'], original=d['原名'], genre=d['题材'],
                summary=d['卡片推荐'], path='anime/' + d['slug'] + '.html',
                image='assets/images/' + d['slug'] + '.jpg') for d in items]
(OUT / 'assets/js/catalog.js').write_text(
    'window.ANIME_CATALOG = ' + json.dumps(catalog, ensure_ascii=False) + ';\n', encoding='utf-8')


def art_img(slug, alt, prefix=''):
    return f'<img class="art-img" src="{prefix}assets/images/{slug}.jpg" alt="{e(alt)}" loading="lazy">'


def scene(kind=0):
    return f'<div class="scene scene-{kind}" aria-hidden="true"><i class="moon"></i><i class="cloud cloud-a"></i><i class="cloud cloud-b"></i><i class="ridge ridge-a"></i><i class="ridge ridge-b"></i><i class="lake"></i><span class="star s1">✦</span><span class="star s2">✧</span><span class="star s3">·</span></div>'


def page(name, title, body, detail=False):
    pre = '../' if detail else ''
    og_path = '' if name == 'index.html' else name
    og_url = BASE + '/' + og_path
    og_title = f'{title} · 今晚看什么'
    active = 'discover.html' if detail else name
    nav = ''.join(f'<a href="{pre}{file}"' + (' aria-current="page"' if active == file else '') + f'>{label}</a>' for file, label in [('index.html', '首页'), ('discover.html', '发现动漫'), ('watchlist.html', '想看清单'), ('about.html', '关于')])
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="二十部动漫，无剧透介绍。按今天的心情，发现下一段故事。"><link rel="icon" type="image/png" href="{pre}assets/icons/favicon-32.png"><link rel="apple-touch-icon" href="{pre}assets/icons/apple-touch-icon.png"><meta property="og:type" content="website"><meta property="og:site_name" content="今晚看什么"><meta property="og:locale" content="zh_CN"><meta property="og:title" content="{e(og_title)}"><meta property="og:description" content="二十部动漫，无剧透介绍。按今天的心情，发现下一段故事。"><meta property="og:image" content="{BASE}/assets/icons/og-cover.jpg"><meta property="og:url" content="{og_url}"><meta name="twitter:card" content="summary_large_image"><title>{e(title)} · 今晚看什么</title><link rel="stylesheet" href="{pre}assets/css/styles.css"><link rel="stylesheet" href="{pre}assets/css/refinement.css"></head>
<body><a class="skip" href="#main">跳转到正文</a><header class="header"><div class="wrap nav"><a class="brand" href="{pre}index.html"><span aria-hidden="true">☾</span> 今晚看什么<small>AN EVENING, A STORY</small></a><nav aria-label="主导航">{nav}</nav><a class="language" data-language href="{pre}en/{name}" hreflang="en" lang="en">English</a></div></header><main id="main" tabindex="-1">{body}</main><footer class="wrap footer"><a class="brand" href="{pre}index.html">☾ 今晚看什么</a><p>每个平凡的夜晚，都值得一个好故事。</p><a href="{pre}about.html">选片方法与资料说明</a><small>无剧透精选 · 推荐为编辑判断 · 作品资料见详情来源</small></footer><script defer src="{pre}assets/js/language.js"></script><div class="save-feedback" role="status" aria-live="polite" id="save-feedback"></div><script src="{pre}assets/js/catalog.js" defer></script><script src="{pre}assets/js/watchlist-store.js" defer></script><script src="{pre}assets/js/watchlist.js" defer></script></body></html>'''
    (OUT / name).write_text(html, encoding='utf-8')


def save_button(d):
    return f'<button type="button" class="save-button" data-save="{d["slug"]}" aria-pressed="false" hidden>加入想看</button>'


def card(d, prefix=''):
    slug = d['slug']
    en_title = STORIES[slug][0]
    return f'''<article class="card" id="{slug}" data-title="{e(en_title)} {e(d['title'])} {e(d['原名'])}" data-genre="{e(d['题材'])}" data-moods="{e(d['心情'])}"><a class="card-art" tabindex="-1" aria-hidden="true" href="{prefix}anime/{slug}.html">{art_img(slug, e(d['title']) + ' 海报', '')}<span class="art-caption">STORY {d['number']}</span></a><div class="card-body"><p class="eyebrow">{e(d['题材'])} · {e(d['心情'])}</p><h3><a href="{prefix}anime/{slug}.html">{e(d['title'])}</a></h3><p class="original" lang="ja">{e(d['原名'])}</p><p>{e(d['卡片推荐'])}</p><a class="text-link" href="{prefix}anime/{slug}.html">走进这个故事 <span aria-hidden="true">↗</span></a>{save_button(d)}</div></article>'''


cards = ''.join(card(d) for d in items)
page('index.html', '首页', f'''<section class="hero">{scene()}<div class="wrap hero-content"><p class="eyebrow">给今天，留一点幻想</p><h1>下一段故事，<br>从今晚开始。</h1><p>二十部精选动漫，二十种相遇的方式。<br>放下选择的犹豫，找一个适合此刻心情的故事。</p><a class="button" href="discover.html">发现我的下一部 <span aria-hidden="true">↗</span></a><span class="hero-note">NO SPOILERS · JUST STORIES</span></div><span class="vertical" aria-hidden="true">今夜、物語に会いに。</span></section><div class="wrap"><section class="section"><div class="section-title"><div><p class="eyebrow">01 / FIND YOUR MOOD</p><h2>今晚，想要怎样的心情？</h2></div><p>不必追赶热度，跟着自己的节奏。</p></div><div class="moods"><a href="discover.html?mood=想放松"><span>☾</span><h3>让今晚慢一点</h3><p>风景、旅途，和细小的心动。</p></a><a href="discover.html?mood=想被鼓励"><span>✦</span><h3>找一点向前的勇气</h3><p>一次出发，一场全力以赴。</p></a><a href="discover.html?mood=想慢慢品味"><span>❋</span><h3>遇见温柔的陪伴</h3><p>关于家人，也关于奇妙的相遇。</p></a></div></section><section class="section"><div class="section-title"><div><p class="eyebrow">02 / EDITOR’S SELECTION</p><h2>把好故事，留给今晚</h2></div><a class="text-link" href="discover.html">查看全部二十部 ↗</a></div><div class="grid">{''.join(card(d) for d in items[:3])}</div></section><aside class="quote"><p>不以一个分数，定义一次相遇。</p><a href="about.html">了解我们的选片方法 ↗</a></aside></div>''')

chips = ''.join(f'<a href="discover.html?mood={mood}">{title}</a>' for mood, title in
                [('想放松', '让今晚慢一点'), ('想被鼓励', '找一点向前的勇气'), ('想慢慢品味', '遇见温柔的陪伴')])
genre_options = ''.join(f'<option>{e(g)}</option>' for g in GENRES)
mood_options = ''.join(f'<option>{e(m)}</option>' for m in MOODS)
form = '<form id="filters" class="filters" action="discover.html" method="get" hidden><div><label for="search">搜索作品名称</label><input id="search" name="q" type="search" placeholder="中文名或日文原名" maxlength="100"></div><div><label for="genre">题材</label><select id="genre" name="genre"><option value="">全部题材</option>' + genre_options + '</select></div><div><label for="mood">观看心情</label><select id="mood" name="mood"><option value="">全部心情</option>' + mood_options + '</select></div><button class="button" type="submit">查找作品</button><button class="clear" type="button" id="clear-filters">清除条件</button></form>'
body = '<div class="wrap"><section class="page-head"><p class="eyebrow">THE COLLECTION / 二十部精选</p><h1>发现下一部<br><em>想看的动漫。</em></h1><p>从题材与心情出发，先读推荐理由，再决定是否开始。</p><nav class="chips" aria-label="心情专题">' + chips + '</nav></section>'
body += form
body += '<noscript><p>筛选需要启用 JavaScript；下方仍可浏览全部二十部作品。</p></noscript><p id="result-count" role="status" aria-live="polite" aria-atomic="true">共 20 部作品</p><section id="no-results" class="empty" hidden><h2>这次没有找到合适的作品</h2><p>试试减少筛选条件，或换一个作品名称。</p><button type="button" class="button" id="clear-empty">清除筛选</button></section>'
body += f'<section class="section" id="all"><div class="section-title"><h2>全部作品</h2><span>20 部作品</span></div><div class="grid">{cards}</div></section>'
page('discover.html', '发现动漫', body + '</div><script src="assets/js/filter.js" defer></script>')

for d in items:
    source = re.search(r'\[([^]]+)\]\(([^)]+)\)', d['资料来源'])
    body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a><span>/</span><a href="../discover.html">发现动漫</a><span>/</span><span aria-current="page">{e(d['title'])}</span></nav><section class="detail-hero"><div><p class="eyebrow">STORY {d['number']} / {e(d['题材'])}</p><h1>{e(d['title'])}</h1><p lang="ja" class="original">{e(d['原名'])}</p><p class="lead">{e(d['卡片推荐'])}</p><span class="tag">{e(d['心情'])}</span>{save_button(d)}</div><div class="detail-art">{art_img(d['slug'], e(d['title']) + ' 海报', '../')}<span class="art-caption">A STORY FOR TONIGHT</span></div></section><div class="reading-layout"><article class="reading">'''
    for label, key in [('故事，从这里开始', '无剧透简介'), ('为什么推荐', '编辑推荐'), ('适合怎样的你', '适合谁'), ('观看前，知道这些', '观看前知道')]:
        body += f'<section><h2>{label}</h2><p>{e(d[key])}</p></section>'
    body += f'''</article><aside class="reading-aside"><p class="eyebrow">YOUR FIRST EPISODE</p><h2>从哪里开始</h2><p>{e(d['从哪里开始'])}</p><hr><h2>资料来源</h2><a href="{source[2]}">{e(source[1])} ↗</a><p class="fine">基本设定依据官方资料改写。分类与推荐为本站编辑判断，不代表官方评级。</p></aside></div><section class="next"><span>换一种心情，继续寻找。</span><a class="button" href="../discover.html">返回作品列表 ↗</a></section></div>'''
    page(f'anime/{d["slug"]}.html', d['title'], body, True)

page('watchlist.html', '想看清单', '''<div class="wrap"><section class="page-head"><p class="eyebrow">YOUR NEXT STORY</p><h1>把想看的故事，<br><em>留给下一个夜晚。</em></h1><p>仅保存在当前浏览器，不会跨设备同步。清理浏览器数据会删除清单。</p></section><noscript><p>想看清单需要启用 JavaScript。你仍可以<a href="discover.html">浏览全部作品</a>。</p></noscript><section id="watchlist-panel" hidden><div class="list-toolbar"><h2 id="saved-count" tabindex="-1">我的想看清单</h2><button type="button" id="clear-list" class="clear">清空清单</button></div><div id="clear-confirm" class="clear-confirm" hidden><p>确定移除清单中的全部作品？此操作不能撤销。</p><button type="button" id="cancel-clear" class="clear">取消</button><button type="button" id="confirm-clear" class="save-button">确定清空</button></div><div id="saved-grid" class="grid"></div><section id="saved-empty" class="empty" hidden><span aria-hidden="true">☾</span><h2>先找到让你心动的那一部</h2><p>在作品卡片或详情页点击“加入想看”，把故事留在这里。</p><a class="button" href="discover.html">去发现动漫 ↗</a></section></section></div>''')

page('about.html', '关于', '''<div class="wrap"><section class="page-head"><p class="eyebrow">ABOUT / 关于这个小站</p><h1>帮你缩小选择，<br><em>把决定留给你。</em></h1><p>每一次打开动漫，都可以从一个简单的问题开始：<br>今天，我想遇见怎样的故事？</p></section><div class="reading-layout"><article class="reading"><section><h2>为什么做这个网站</h2><p>“今晚看什么”是一个面向动漫观众的精选指南。它从一个简单的问题出发：知道自己想看动漫，却不知道今晚适合哪一部。</p><p>本站用二十部作品组成一个小而明确的入口。先看题材和心情，再读推荐理由与观看提醒，不必面对无穷无尽的排行榜。</p></section><section><h2>我们怎样组织推荐</h2><p>以旅途、成长、竞技、家庭与相遇等主题组织作品，既说明适合谁，也保留观看前需要知道的内容。题材和心情标签是编辑整理，不是官方评级。</p></section><section><h2>关于内容与来源</h2><p>作品基本设定依据官方资料整理，来源链接保留在每个详情页。中文简介经过重新表述，推荐语不冒充观众投票、真实用户评论或站长亲身观看经历。</p><p>内容整理与页面制作使用 AI 辅助。选片、分类和最终编辑判断是课程项目需要作者审阅并解释的部分。</p></section><section><h2>关于作品与素材</h2><p>本站不提供动画播放或下载，与作品官方无隶属关系。卡片与详情页使用的海报、主视觉为各作品官方宣传图，仅作站内展示；首页背景的满月与花枝插画为本站自制装饰图形。</p></section></article><aside class="reading-aside"><p class="eyebrow">SMALL COLLECTION</p><h2>二十部作品<br>不同的观看方向</h2><p>无剧透介绍<br>清晰的推荐理由<br>可追溯的官方资料</p><a class="text-link" href="discover.html">从这里开始 ↗</a></aside></div></div>''')

from build_english import build
build(OUT, items, scene)
print('Generated static pages for', len(items), 'titles.')

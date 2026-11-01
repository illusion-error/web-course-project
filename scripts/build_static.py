"""Regenerate batch-A static HTML from the reviewed content document (stdlib only)."""
from pathlib import Path
import re
from html import escape as e

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'site'
(OUT / 'anime').mkdir(parents=True, exist_ok=True)
text = (ROOT / 'docs/ANIME-SITE-CONTENT.md').read_text(encoding='utf-8')
items = []
for number, title, body in re.findall(r'### (\d{2}) ([^\n]+)\n(.*?)(?=\n### |\n详情页通用按钮)', text, re.S):
    d = dict(re.findall(r'^- ([^：\n]+)：([^\n]+)', body, re.M))
    d.update(number=number, title=title)
    items.append(d)
assert len(items) == 6

def scene(kind=0):
    return f'<div class="scene scene-{kind}" aria-hidden="true"><i class="moon"></i><i class="cloud cloud-a"></i><i class="cloud cloud-b"></i><i class="ridge ridge-a"></i><i class="ridge ridge-b"></i><i class="lake"></i><span class="star s1">✦</span><span class="star s2">✧</span><span class="star s3">·</span></div>'

def page(name, title, body, detail=False):
    pre = '../' if detail else ''
    active = 'discover.html' if detail else name
    nav = ''.join(f'<a href="{pre}{file}"'+(' aria-current="page"' if active == file else '')+f'>{label}</a>' for file,label in [('index.html','首页'),('discover.html','发现动漫'),('watchlist.html','想看清单'),('about.html','关于')])
    html = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="六部动漫，无剧透介绍。按今天的心情，发现下一段故事。"><title>{e(title)} · 今晚看什么</title><link rel="stylesheet" href="{pre}assets/css/styles.css"><link rel="stylesheet" href="{pre}assets/css/refinement.css"></head>
<body><a class="skip" href="#main">跳转到正文</a><header class="header"><div class="wrap nav"><a class="brand" href="{pre}index.html"><span aria-hidden="true">☾</span> 今晚看什么<small>AN EVENING, A STORY</small></a><nav aria-label="主导航">{nav}</nav></div></header><main id="main" tabindex="-1">{body}</main><footer class="wrap footer"><a class="brand" href="{pre}index.html">☾ 今晚看什么</a><p>每个平凡的夜晚，都值得一个好故事。</p><a href="{pre}about.html">选片方法与资料说明</a><small>无剧透精选 · 推荐为编辑判断 · 作品资料见详情来源</small></footer></body></html>'''
    (OUT / name).write_text(html, encoding='utf-8')

def card(d, prefix='', i=0):
    return f'''<article class="card" id="{d['slug']}" data-title="{e(d['title'])} {e(d['原名'])}" data-genre="{e(d['题材'])}" data-moods="{e(d['心情'])}"><a class="card-art" tabindex="-1" aria-hidden="true" href="{prefix}anime/{d['slug']}.html">{scene(i)}<span class="art-caption">STORY {d['number']}</span></a><div class="card-body"><p class="eyebrow">{e(d['题材'])} · {e(d['心情'])}</p><h3><a href="{prefix}anime/{d['slug']}.html">{e(d['title'])}</a></h3><p class="original" lang="ja">{e(d['原名'])}</p><p>{e(d['卡片推荐'])}</p><a class="text-link" href="{prefix}anime/{d['slug']}.html">走进这个故事 <span aria-hidden="true">↗</span></a></div></article>'''

cards = ''.join(card(d,i=i) for i,d in enumerate(items))
page('index.html','首页',f'''<section class="hero">{scene()}<div class="wrap hero-content"><p class="eyebrow">给今天，留一点幻想</p><h1>下一段故事，<br>从今晚开始。</h1><p>六部精选动漫，六种相遇的方式。<br>放下选择的犹豫，找一个适合此刻心情的故事。</p><a class="button" href="discover.html">发现我的下一部 <span aria-hidden="true">↗</span></a><span class="hero-note">NO SPOILERS · JUST STORIES</span></div><span class="vertical" aria-hidden="true">今夜、物語に会いに。</span></section><div class="wrap"><section class="section"><div class="section-title"><div><p class="eyebrow">01 / FIND YOUR MOOD</p><h2>今晚，想要怎样的心情？</h2></div><p>不必追赶热度，跟着自己的节奏。</p></div><div class="moods"><a href="discover.html?mood=想放松"><span>☾</span><h3>让今晚慢一点</h3><p>风景、旅途，和细小的心动。</p></a><a href="discover.html?mood=想被鼓励"><span>✦</span><h3>找一点向前的勇气</h3><p>一次出发，一场全力以赴。</p></a><a href="discover.html?mood=想慢慢品味"><span>❋</span><h3>遇见温柔的陪伴</h3><p>关于家人，也关于奇妙的相遇。</p></a></div></section><section class="section"><div class="section-title"><div><p class="eyebrow">02 / EDITOR’S SELECTION</p><h2>把好故事，留给今晚</h2></div><a class="text-link" href="discover.html">查看全部六部 ↗</a></div><div class="grid">{''.join(card(d,i=i) for i,d in enumerate(items[:3]))}</div></section><aside class="quote"><p>不以一个分数，定义一次相遇。</p><a href="about.html">了解我们的选片方法 ↗</a></aside></div>''')

groups = [('quiet','让今晚慢一点',[items[1],items[0]]),('courage','找一点向前的勇气',[items[2],items[3]]),('company','遇见温柔的陪伴',[items[4],items[5]])]
body = '<div class="wrap"><section class="page-head"><p class="eyebrow">THE COLLECTION / 六部精选</p><h1>发现下一部<br><em>想看的动漫。</em></h1><p>从题材与心情出发，先读推荐理由，再决定是否开始。</p><nav class="chips" aria-label="心情专题">'+''.join(f'<a href="discover.html?mood={mood}">{title}</a>' for (_,title,_),mood in zip(groups,['想放松','想被鼓励','想慢慢品味']))+'</nav></section>'
for id,title,ds in groups:
    body += f'<section class="section" id="{id}"><div class="section-title"><h2>{title}</h2><span>02 STORIES</span></div><div class="grid two">'+''.join(card(d,i=items.index(d)) for d in ds)+'</div></section>'
form = '<form id="filters" class="filters" action="discover.html" method="get" hidden><div><label for="search">搜索作品名称</label><input id="search" name="q" type="search" placeholder="中文名或日文原名" maxlength="100"></div><div><label for="genre">题材</label><select id="genre" name="genre"><option value="">全部题材</option>'+''.join(f'<option>{e(d["题材"])}</option>' for d in items)+'</select></div><div><label for="mood">观看心情</label><select id="mood" name="mood"><option value="">全部心情</option>'+''.join(f'<option>{e(m)}</option>' for m in ['想放松','想被鼓励','想看热血','想慢慢品味'])+'</select></div><button class="button" type="submit">查找作品</button><button class="clear" type="button" id="clear-filters">清除条件</button></form><noscript><p>筛选需要启用 JavaScript；下方仍可浏览全部六部作品。</p></noscript><p id="result-count" role="status" aria-live="polite" aria-atomic="true">共 6 部作品</p><section id="no-results" class="empty" hidden><h2>这次没有找到合适的作品</h2><p>试试减少筛选条件，或换一个作品名称。</p><button type="button" class="button" id="clear-empty">清除筛选</button></section>'
body = body.replace('</section>', '</section>'+form, 1)
page('discover.html','发现动漫',body+'</div><script src="assets/js/filter.js" defer></script>')

for i,d in enumerate(items):
    source = re.search(r'\[([^]]+)\]\(([^)]+)\)',d['资料来源'])
    body = f'''<div class="wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a><span>/</span><a href="../discover.html">发现动漫</a><span>/</span><span aria-current="page">{e(d['title'])}</span></nav><section class="detail-hero"><div><p class="eyebrow">STORY {d['number']} / {e(d['题材'])}</p><h1>{e(d['title'])}</h1><p lang="ja" class="original">{e(d['原名'])}</p><p class="lead">{e(d['卡片推荐'])}</p><span class="tag">{e(d['心情'])}</span></div><div class="detail-art">{scene(i)}<span class="art-caption">A STORY FOR TONIGHT</span></div></section><div class="reading-layout"><article class="reading">'''
    for label,key in [('故事，从这里开始','无剧透简介'),('为什么推荐','编辑推荐'),('适合怎样的你','适合谁'),('观看前，知道这些','观看前知道')]:
        body+=f'<section><h2>{label}</h2><p>{e(d[key])}</p></section>'
    body+=f'''</article><aside class="reading-aside"><p class="eyebrow">YOUR FIRST EPISODE</p><h2>从哪里开始</h2><p>{e(d['从哪里开始'])}</p><hr><h2>资料来源</h2><a href="{source[2]}">{e(source[1])} ↗</a><p class="fine">基本设定依据官方资料改写。分类与推荐为本站编辑判断，不代表官方评级。</p></aside></div><section class="next"><span>换一种心情，继续寻找。</span><a class="button" href="../discover.html">返回作品列表 ↗</a></section></div>'''
    page(f'anime/{d["slug"]}.html',d['title'],body,True)

page('watchlist.html','想看清单','''<div class="wrap"><section class="page-head"><p class="eyebrow">YOUR NEXT STORY</p><h1>把想看的故事，<br><em>留给下一个夜晚。</em></h1></section><section class="empty"><span aria-hidden="true">☾</span><h2>先找到让你心动的那一部</h2><p>浏览六部精选作品，了解故事的题材与观看方向。</p><a class="button" href="discover.html">去发现动漫 ↗</a><p class="fine">此版本提供作品浏览；个人清单的保存与管理尚未开放。</p></section></div>''')
page('about.html','关于','''<div class="wrap"><section class="page-head"><p class="eyebrow">ABOUT / 关于这个小站</p><h1>帮你缩小选择，<br><em>把决定留给你。</em></h1><p>每一次打开动漫，都可以从一个简单的问题开始：<br>今天，我想遇见怎样的故事？</p></section><div class="reading-layout"><article class="reading"><section><h2>为什么做这个网站</h2><p>“今晚看什么”是一个面向动漫观众的精选指南。它从一个简单的问题出发：知道自己想看动漫，却不知道今晚适合哪一部。</p><p>本站用六部作品组成一个小而明确的入口。先看题材和心情，再读推荐理由与观看提醒，不必面对无穷无尽的排行榜。</p></section><section><h2>我们怎样组织推荐</h2><p>以旅途、成长、竞技、家庭与相遇等主题组织作品，既说明适合谁，也保留观看前需要知道的内容。题材和心情标签是编辑整理，不是官方评级。</p></section><section><h2>关于内容与来源</h2><p>作品基本设定依据官方资料整理，来源链接保留在每个详情页。中文简介经过重新表述，推荐语不冒充观众投票、真实用户评论或站长亲身观看经历。</p><p>内容整理与页面制作使用 AI 辅助。选片、分类和最终编辑判断是课程项目需要作者审阅并解释的部分。</p></section><section><h2>关于作品与素材</h2><p>本站不提供动画播放或下载，与作品官方无隶属关系。页面中的月亮、山峦与星空是本站制作的装饰图形，不是作品海报或剧情截图。</p></section></article><aside class="reading-aside"><p class="eyebrow">SMALL COLLECTION</p><h2>六部作品<br>不同的观看方向</h2><p>无剧透介绍<br>清晰的推荐理由<br>可追溯的官方资料</p><a class="text-link" href="discover.html">从这里开始 ↗</a></aside></div></div>''')
print('Generated 10 static pages.')

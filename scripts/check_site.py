from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
class Page(HTMLParser):
 def __init__(self): super().__init__(); self.links=[]; self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src'):
   if k in a:self.links.append(a[k])
root=Path('site').resolve(); pages={}
for f in root.rglob('*.html'):
 p=Page();p.feed(f.read_text(encoding='utf-8'));pages[f]=p
errors=[];count=0
for f,p in pages.items():
 for link in p.links:
  u=urlsplit(link)
  if u.scheme or u.netloc:continue
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  count+=1
  if not target.is_relative_to(root) or not target.is_file(): errors.append(f'{f.name}: missing {link}')
  elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:errors.append(f'{f.name}: missing anchor {link}')
assert not errors,'\n'.join(errors)
print(f'PASS: {len(pages)} pages, {count} internal links/resources/anchors')

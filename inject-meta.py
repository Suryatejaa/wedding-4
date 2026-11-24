#!/usr/bin/env python3
"""Bake <title>, description, Open Graph and Twitter tags from wedding.json into
index.html's <head>. Needed because WhatsApp/Facebook/X/Google link-preview
crawlers do NOT run JavaScript. Re-run after editing the "meta" block:

    python3 inject-meta.py
"""
import json, re, sys
from html import escape
from urllib.parse import urljoin

J = json.load(open('wedding.json', encoding='utf-8'))
M = J['meta']; og = M.get('og', {}); tw = M.get('twitter', {})
base = M.get('siteUrl', '')
if not base:
    print('WARNING: meta.siteUrl is empty — og:image/og:url must be absolute for link previews to work.', file=sys.stderr)
absu = lambda u: urljoin(base, u) if (u and base) else (u or '')

tags = [f'<title>{escape(M["title"])}</title>']
def meta(attr, key, val):
    if val: tags.append(f'<meta {attr}="{key}" content="{escape(val, quote=True)}">')
meta('name','description',M.get('description')); meta('name','keywords',M.get('keywords'))
meta('name','author',M.get('author')); meta('name','theme-color',M.get('themeColor'))
if base:
    tags.append(f'<link rel="canonical" href="{escape(base, quote=True)}">'); meta('property','og:url',base)
for k in ('type','title','description'): meta('property',f'og:{k}',og.get(k))
meta('property','og:image',absu(og.get('image'))); meta('property','og:image:alt',og.get('imageAlt'))
meta('property','og:site_name',og.get('siteName')); meta('property','og:locale',og.get('locale'))
for k in ('card','title','description'): meta('name',f'twitter:{k}',tw.get(k))
meta('name','twitter:image',absu(tw.get('image'))); meta('name','twitter:image:alt',tw.get('imageAlt'))

s = open('index.html', encoding='utf-8').read()
block = '<!-- META:START (generated from wedding.json by inject-meta.py — do not edit by hand) -->\n' \
        + '\n'.join(tags) + '\n<!-- META:END -->'
s, n = re.subn(r'<!-- META:START.*?<!-- META:END -->', lambda _: block, s, flags=re.S)
assert n == 1, 'META markers not found in index.html'
if M.get('lang'):
    s = re.sub(r'<html lang="[^"]*"', f'<html lang="{M["lang"]}"', s, count=1)
open('index.html', 'w', encoding='utf-8').write(s)
print('index.html <head> updated from wedding.json')

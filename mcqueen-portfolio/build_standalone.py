#!/usr/bin/env python3
"""把 index.html + style.css + assets/ 内联成一个自包含的 HTML 文件。

用法： python3 build_standalone.py
输出： mcqueen-portfolio-standalone.html
"""
import base64
import io
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

html = open('index.html', encoding='utf-8').read()
css = open('style.css', encoding='utf-8').read()
fonts_css = open('assets/fonts/fonts.css', encoding='utf-8').read()

_cache = {}


def data_uri(path):
    """图片转 data URI：SVG 原样内嵌，位图转 WebP（保留透明通道，体积约 PNG 的 1/7）。"""
    if path in _cache:
        return _cache[path]
    if path.lower().endswith('.svg'):
        raw = open(path, 'rb').read()
        uri = 'data:image/svg+xml;base64,' + base64.b64encode(raw).decode()
    else:
        buf = io.BytesIO()
        Image.open(path).save(buf, 'WEBP', quality=92, method=6)
        uri = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    _cache[path] = uri
    return uri


html = re.sub(r'src="(assets/[^"]+)"', lambda m: 'src="%s"' % data_uri(m.group(1)), html)
css = re.sub(r'url\((assets/[^)]+)\)', lambda m: 'url(%s)' % data_uri(m.group(1)), css)

for font in re.findall(r'url\(\./([^)]+)\)', fonts_css):
    uri = 'data:font/woff2;base64,' + base64.b64encode(
        open('assets/fonts/' + font, 'rb').read()).decode()
    fonts_css = fonts_css.replace('url(./%s)' % font, 'url(%s)' % uri)

html = html.replace('<link rel="stylesheet" href="assets/fonts/fonts.css">\n', '')
html = html.replace(
    '<link rel="stylesheet" href="style.css">',
    '<style>\n' + fonts_css + '\n</style>\n<style>\n' + css + '\n</style>',
)

out = 'mcqueen-portfolio-standalone.html'
open(out, 'w', encoding='utf-8').write(html)
print('%s  %.2f MB' % (out, os.path.getsize(out) / 1e6))

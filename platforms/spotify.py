import json
import os
import re
import ssl
import tempfile
import urllib.parse
import urllib.request

import yt_dlp

def _get_metadata(url):
    clean = url.split('?')[0].strip()
    m = re.search(r'uri=spotify:(track|album|playlist):([a-zA-Z0-9]+)', url, re.I)
    if m:
        clean = f"https://open.spotify.com/{m.group(1)}/{m.group(2)}"
    oembed_url = f"https://open.spotify.com/oembed?url={urllib.parse.quote(clean)}"
    req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    for ctx in [ssl.create_default_context(), _unverified_ssl_context()]:
        try:
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                data = json.loads(r.read().decode())
                return data.get('title', '') or None
        except Exception:
            continue
    return None

def _unverified_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def download(url):
    query = _get_metadata(url)
    if not query:
        raise Exception('failed to get spotify metadata')
    tmp = tempfile.mkdtemp()
    dl_opts = {
        'outtmpl': os.path.join(tmp, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'flac'}],
    }
    with yt_dlp.YoutubeDL(dl_opts) as ydl:
        ydl.download([f'ytsearch1:{query}'])
    files = [f for f in os.listdir(tmp) if f.endswith('.flac')]
    if not files:
        files = os.listdir(tmp)
    if not files:
        raise Exception('no match found on youtube')
    path = os.path.join(tmp, files[0])
    return path, query

import yt_dlp
from urllib.parse import quote

from misc.utils import detect_platform, is_valid_url

def can_share(url):
    if not is_valid_url(url):
        return False
    return detect_platform(url) is not None

def get_metadata(url):
    opts = {'quiet': True, 'no_warnings': True}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info:
            return None, None
        title = info.get('title') or 'video'
        thumb = info.get('thumbnail')
        return title, thumb

def embed_url(base_url, source_url):
    return f"{base_url.rstrip('/')}/dl?url={quote(source_url, safe='')}"

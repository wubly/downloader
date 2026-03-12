import yt_dlp
from urllib.parse import quote

from misc.utils import detect_platform, is_valid_url

def can_share(url, spotify_enabled=False):
    if not is_valid_url(url):
        return False
    platform = detect_platform(url)
    if not platform:
        return False
    if platform == 'spotify' and not spotify_enabled:
        return False
    return True

def get_metadata(url, spotify_enabled=False):
    if spotify_enabled and detect_platform(url) == 'spotify':
        from platforms.spotify import _get_metadata
        title = _get_metadata(url)
        return title or 'track', None
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

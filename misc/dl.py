import os
import shutil
from starlette.background import BackgroundTask
from fastapi.responses import FileResponse, JSONResponse

from misc.utils import detect_platform, is_valid_url
from platforms import tiktok, reels, youtube, twitter, pinterest, reddit, vimeo, facebook, soundcloud

def get_handlers(spotify_enabled=False):
    h = {
        'tiktok': tiktok, 'reels': reels, 'youtube': youtube, 'twitter': twitter,
        'pinterest': pinterest, 'reddit': reddit, 'vimeo': vimeo, 'facebook': facebook,
        'soundcloud': soundcloud,
    }
    if spotify_enabled:
        from platforms import spotify
        h['spotify'] = spotify
    return h

def cleanup(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except:
        pass

def do_download(url, spotify_enabled=False):
    if not is_valid_url(url):
        return None, 'invalid url'
    platform = detect_platform(url)
    if not platform:
        return None, 'unsupported platform'
    handlers = get_handlers(spotify_enabled)
    if platform not in handlers:
        return None, 'unsupported platform'
    try:
        path, title = handlers[platform].download(url)
    except Exception as e:
        return None, str(e)
    basename = os.path.basename(path)
    ext = os.path.splitext(basename)[1] or '.mp4'
    mime = 'audio/mpeg' if ext == '.mp3' else ('audio/mp4' if ext == '.m4a' else ('audio/flac' if ext == '.flac' else 'video/mp4'))
    safe_title = (title[:50] if title else 'video').replace('<', '').replace('>', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').replace(':', '')
    filename = f"{safe_title}{ext}"
    return (path, filename, mime, os.path.dirname(path)), None

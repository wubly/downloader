import re

def detect_platform(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip().lower()
    if 'tiktok.com' in url or 'vm.tiktok.com' in url:
        return 'tiktok'
    if 'instagram.com' in url or 'instagr.am' in url:
        return 'reels'
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    if 'twitter.com' in url or 'x.com' in url:
        return 'twitter'
    if 'pinterest.com' in url or 'pin.it' in url:
        return 'pinterest'
    if 'reddit.com' in url or 'redd.it' in url:
        return 'reddit'
    if 'vimeo.com' in url:
        return 'vimeo'
    if 'facebook.com' in url or 'fb.com' in url or 'fb.watch' in url or 'fb.reel' in url:
        return 'facebook'
    if 'soundcloud.com' in url:
        return 'soundcloud'
    return None

def is_valid_url(url):
    if not url:
        return False
    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, url.strip()))

import re

def detect_platform(url):
    if not url or not isinstance(url, str):
        return None
    url = url.strip().lower()
    if 'tiktok.com' in url or 'vm.tiktok.com' in url:
        return 'tiktok'
    if 'instagram.com' in url or 'instagr.am' in url:
        return 'reels'
    return None

def is_valid_url(url):
    if not url:
        return False
    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, url.strip()))

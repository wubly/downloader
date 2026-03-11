import yt_dlp
import tempfile
import os

def download(url):
    tmp = tempfile.mkdtemp()
    opts = {
        'outtmpl': os.path.join(tmp, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://www.pinterest.com/',
        },
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise Exception('failed to get video')
        files = os.listdir(tmp)
        if not files:
            raise Exception('no file downloaded')
        path = os.path.join(tmp, files[0])
        return path, info.get('title', 'pinterest') or 'pinterest'

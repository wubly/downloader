import yt_dlp
import tempfile
import os

def download(url):
    tmp = tempfile.mkdtemp()
    opts = {
        'outtmpl': os.path.join(tmp, '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'format': 'best[ext=mp4]/best[ext=webm]/best',
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if not info:
            raise Exception('failed to get video')
        files = os.listdir(tmp)
        if not files:
            raise Exception('no file downloaded')
        path = os.path.join(tmp, files[0])
        return path, info.get('title', 'reddit') or 'reddit'

import os
import shutil
from fastapi import FastAPI, Request, Form
from starlette.background import BackgroundTask
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from misc.utils import detect_platform, is_valid_url
from platforms import tiktok, reels, youtube, twitter

app = FastAPI(title='downloader.wubly.run')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request})

@app.post('/dl')
async def dl(url: str = Form(...)):
    if not is_valid_url(url):
        return JSONResponse(
            status_code=400,
            content={'ok': False, 'error': 'invalid url'}
        )
    platform = detect_platform(url)
    if not platform:
        return JSONResponse(
            status_code=400,
            content={'ok': False, 'error': 'tiktok, instagram, youtube, twitter only'}
        )
    try:
        if platform == 'tiktok':
            path, title = tiktok.download(url)
        elif platform == 'reels':
            path, title = reels.download(url)
        elif platform == 'youtube':
            path, title = youtube.download(url)
        else:
            path, title = twitter.download(url)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'ok': False, 'error': str(e)}
        )
    try:
        basename = os.path.basename(path)
        ext = os.path.splitext(basename)[1] or '.mp4'
        safe_title = (title[:50] if title else 'video').replace('<', '').replace('>', '').replace('"', '').replace('/', '').replace('\\', '').replace('|', '').replace('?', '').replace('*', '').replace(':', '')
        filename = f"{safe_title}{ext}"
        return FileResponse(
            path,
            media_type='video/mp4',
            filename=filename,
            background=BackgroundTask(cleanup, os.path.dirname(path))
        )
    except Exception as e:
        shutil.rmtree(os.path.dirname(path), ignore_errors=True)
        return JSONResponse(
            status_code=500,
            content={'ok': False, 'error': str(e)}
        )

def cleanup(path):
    try:
        shutil.rmtree(path, ignore_errors=True)
    except:
        pass

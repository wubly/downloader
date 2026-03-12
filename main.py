from fastapi import FastAPI, Request, Form
from starlette.background import BackgroundTask
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from misc.dl import do_download, cleanup
from misc.share import can_share, get_metadata, embed_url

SPOTIFY_ENABLED = False

app = FastAPI(title='downloader.wubly.run')
templates = Jinja2Templates(directory='templates')

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/about', response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse('about.html', {'request': request, 'spotify_enabled': SPOTIFY_ENABLED})

@app.get('/api', response_class=HTMLResponse)
async def api_docs(request: Request):
    return templates.TemplateResponse('api.html', {'request': request, 'spotify_enabled': SPOTIFY_ENABLED})

@app.get('/d', response_class=HTMLResponse)
async def share_page(request: Request, url: str = ''):
    if not url or not can_share(url, spotify_enabled=SPOTIFY_ENABLED):
        return templates.TemplateResponse('index.html', {'request': request})
    title, thumbnail = get_metadata(url, spotify_enabled=SPOTIFY_ENABLED)
    if not title:
        title = 'video'
    base = str(request.base_url).rstrip('/')
    video_url = embed_url(base, url)
    is_audio = 'soundcloud.com' in url.lower() or ('spotify.com' in url.lower() and SPOTIFY_ENABLED)
    return templates.TemplateResponse('share.html', {
        'request': request,
        'title': title,
        'thumbnail': thumbnail,
        'video_url': video_url,
        'is_audio': is_audio,
    })

def _dl_response(url):
    result, err = do_download(url, spotify_enabled=SPOTIFY_ENABLED)
    if err:
        code = 400 if err in ('invalid url', 'unsupported platform') else 500
        return JSONResponse(status_code=code, content={'ok': False, 'error': err}), None
    path, filename, mime, tmpdir = result
    try:
        return FileResponse(path, media_type=mime, filename=filename, background=BackgroundTask(cleanup, tmpdir)), None
    except Exception as e:
        cleanup(tmpdir)
        return JSONResponse(status_code=500, content={'ok': False, 'error': str(e)}), None

@app.post('/dl')
async def dl_post(url: str = Form(...)):
    resp, _ = _dl_response(url)
    return resp

@app.get('/dl')
async def dl_get(url: str = ''):
    resp, _ = _dl_response(url)
    return resp

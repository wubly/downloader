# downloader.wubly.run

download videos and audio from tiktok, instagram, youtube, twitter, pinterest, reddit, vimeo, facebook, soundcloud. no login. 

## run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## api

```
POST /dl
body: url (form)
returns: video or audio file

GET /dl?url=...
returns: video or audio file

GET /d?url=...
shareable embed page for discord etc
```

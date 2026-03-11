# downloader.wubly.run

download videos from tiktok, instagram, youtube, twitter, pinterest, reddit, vimeo, facebook. 

## run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

## api

```
POST /dl
body: url (form)
returns: video file
```

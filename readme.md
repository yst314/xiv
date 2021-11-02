
Download the PIXIV bookmarks.

## usage
```shell
pip install -r requirements.txt
```

get access token
```shell
python pixiv_auth.py login > token.txt
```
Download images
```
python main.py ${user_id}
```
The `user_id` is the **numeric** id of the user whose bookmarks you want to download.

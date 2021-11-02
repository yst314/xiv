
Download the pixiv bookmarks.

## usage
Download chromedriver from https://chromedriver.chromium.org/downloads,
and put it in the directory where pixiv_auth.py is located.


Setup python
```shell
pip install -r requirements.txt
```

Get access token
```shell
python pixiv_auth.py login > token.txt
```
Download images
```
python main.py -u ${user_id}
```
The `user_id` is the **numeric** id of the user whose bookmarks you want to download.

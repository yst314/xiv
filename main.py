from pixivpy3 import AppPixivAPI
import argparse
from time import sleep
import json
import os

class PixivToken:
    access_token = ''
    refresh_token = ''

def read_token():
    token = PixivToken
    with open('token.txt', 'r') as f:
        for line in f:
            line = line.rstrip()
            persed = line.split(':')
            if persed[0] == 'access_token':
                token.access_token = persed[1].strip(' ')
            elif persed[0] == 'refresh_token':
                token.refresh_token = persed[1].strip(' ')
        return token

def test_read_token():
    token = read_token()
    assert token.access_token == 'access_token'
    assert token.access_token == 'refresh_token'

def main():
    # 引数
    parser = argparse.ArgumentParser(description='USER_ID')
    parser.add_argument('--userid', '-u', help='ユーザーID', type=str, default='')
    args = parser.parse_args()
    USER_ID = args.userid

    # トークンの読み込み
    token = read_token()
    print('Try to connect Pixiv...')
    aapi = AppPixivAPI()
    aapi.auth(refresh_token=token.refresh_token)
    print('Connection successed')

    # ブックマークした画像のjsonを取得
    users_data = aapi.user_bookmarks_illust(USER_ID, restrict='public')
    bookmarks = users_data['illusts']

    print('')
    while True:
        try:
            next_url = users_data['next_url']
            next_qs = aapi.parse_qs(next_url)
            # users_dataに30以降のjsonデータを再代入
            users_data = aapi.user_bookmarks_illust(**next_qs)
            bookmarks.append(users_data['illusts'])
            #sleep(1)
        except KeyError:
            break
    print(f'[INFO] Found {len(bookmarks)} artworks.')
    # ダウンロード
    for bookmark in bookmarks:
        download_image(bookmark)

def is_manga(work_info):
    if work_info["page_count"] > 1:
        return True
    return False

def download_image(work_info):
    aapi = AppPixivAPI()
    id = work_info.id
    title = work_info.title.replace("/", "-")
    author = work_info.user.name.replace("/", "-")
    author_id = work_info.user.id

    # ダウンロード先のフォルダ作成
    savepath = f"./pixiv_images/{author}({author_id})/{title}({id})"
    if not os.path.exists(savepath):
        os.makedirs(savepath)

        with open(f'{savepath}/info.json', mode='wt', encoding='utf-8') as file:
            json.dump(work_info, file, ensure_ascii=False, indent=2)

        # 漫画のダウンロード
        if is_manga(work_info):
            pages = work_info['meta_pages']
            for i, page in enumerate(pages):
                print(f"[INFO] Downloading {title}({author}) page:{i}")
                aapi.download(page['image_urls']['original'], path = savepath)
                sleep(1)

        # イラストのダウンロード
        else:
            page = work_info['meta_single_page']
            print(f"[INFO] Downloading {title}({author})")
            aapi.download(page["original_image_url"], path = savepath)
            sleep(1)

    else:
        print(f'[INFO] {title}({author}) id:{id} already exists')

if __name__ == '__main__':
    main()
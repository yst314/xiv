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

    # ダウンロード
    #for bookmark in bookmarks:
        #download_image(bookmark)

    next_url = users_data['next_url']
    next_qs = aapi.parse_qs(next_url)
    # users_dataに30以降のjsonデータを再代入
    users_data = aapi.user_bookmarks_illust(**next_qs)
    print(next_qs)

def is_manga(work_info):
    if work_info["page_count"] > 1:
        return True
    return False

def download_image(work_info):
    aapi = AppPixivAPI()
    id = work_info.id
    title = work_info.title.replace("/", "-")
    author = work_info.user.name.replace("/", "-")

    # ダウンロード先のフォルダ作成
    savepath = f"./pixiv_images/{author}/{id}"
    if not os.path.exists(savepath):
        os.makedirs(savepath)

        with open(f'{savepath}/info.json', mode='wt', encoding='utf-8') as file:
            json.dump(work_info, file, ensure_ascii=False, indent=2)

        # 漫画のダウンロード
        if is_manga(work_info):
            pages = work_info['meta_pages']
            for i, page in enumerate(pages):
                print(f"Downloading {title}({author}) page:{i}")
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

# def download_image(users_data, count, allCount):
#     # イラストの数だけ繰り返す
#     ilustNum = len(users_data.illusts)
#     for illust in users_data.illusts[:ilustNum]:
#         author = illust.user.name.replace("/", "-")

#         # ダウンロードフォルダなかったら作る
#         if not os.path.exists("./pixiv_images/" + author):
#             os.makedirs("./pixiv_images/" + author)

#         # 保存先の指定
#         savepath = "./pixiv_images/" + author

#         # 保存
#         aapi.download(illust.image_urls.large, path = savepath)
#         print(str(allCount) + "枚目の画像: " + str(author)+"  " + str(illust.title))
#         count += 1
#         allCount += 1
#         sleep(1)

#         #30回目以降
#         if count > 30:
#             next_url = users_data.next_url
#             next_qs = aapi.parse_qs(next_url)
#             # users_dataに30以降のjsonデータを再代入
#             users_data = aapi.user_bookmarks_illust(**next_qs)
#             count = 1
#             download_image(users_data, count, allCount)

# mkdirExceptExist = lambda path: "" if os.path.exists(path) else os.mkdir(path)

# # 漫画の場合
# if work_info.is_manga:
#     mkdirExceptExist(saving_direcory_path + "manga/" + work_title) # 保存用フォルダがない場合は生成

#     manga_info = api.works(work_info.id)
#     for page_no in range(0, manga_info.response[0].page_count):
#         page_info = manga_info.response[0].metadata.pages[page_no]
#         num = str(page_no) if len(str(page_no)) > 1 else "0" + str(page_no)
#         aapi.download(page_info.image_urls.large, path=saving_direcory_path + "manga/" + work_title, name=num+".jpg")
#         sleep(3)
# # イラストの場合
# else:
#     aapi.download(work_info.image_urls.large, path=saving_direcory_path + "illust", name=work_title+".jpg")
#     sleep(3)

# download_image(users_data, count, all_count)

if __name__ == '__main__':
    main()
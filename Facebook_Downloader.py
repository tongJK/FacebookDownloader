
"""
By SinisterJK : https://github.com/tongjk

If you want to download with HD resolution contact me
or you can develop yourself from this code (keywords : 'url request'.search) :)

Enjoy ur develop :)
"""

from tqdm import tqdm
from re import findall
from bs4 import BeautifulSoup
from urllib.parse import unquote
from requests import get, HTTPError, ConnectionError

symbol = {'right': "\033[92m✔\033[0m", 'cross': "\033[0;91mX\033[0m"}


def fb_download(url):

    if len(findall('www.facebook.com', url)) <= 0:
        print('\n', symbol['cross'], "\033[0;31m", "Facebook url only, Please check your url!!!")
        exit(0)

    print("\033[0;96mDownload video from :", url)
    print("\033[0;96mVideo Channel :", url.split('/')[3])  # work good as url from Facebook channel

    url = url.replace("www", "mbasic")

    try:
        r = get(url, timeout=5, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        title_text = soup.title.string

        if r.status_code != 200:
            raise HTTPError

        if len(findall("/video_redirect/", r.text)) == 0:
            print('\n', symbol['cross'], "\033[0;31m", "Video Not Found or Video has been deleted...")
            exit(0)

        else:
            link, title = unquote(r.text.split("?src=")[1].split('"')[0]), title_text
            print("\033[0;96mVideo Title : ", title.strip())

            download(link, title + '.mp4')
            print('\n', symbol['right'], '\033[0;32m', "Video downloaded")

    except (HTTPError, ConnectionError):

        print('\n', symbol['cross'], "\033[0;31m", "Invalid Facebook url")
        exit(1)


def download(url, path):

    path = str(path).replace('!', '').replace('/', '')  # replace the character that your os not allow with null
    print("\033[0;96mSave To :", path)

    r = get(url, stream=True)
    print("\033[0;96mVideo upload date : ", r.headers.get("Last-Modified"))

    total = int(r.headers.get("content-length"))
    print("\033[0;96mVideo Size : ", round(total / 1024, 2), "kB", end="\n\n")

    with open(path, "wb") as file:
        for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=total / 1024, unit="kB"):
            file.write(data)
        file.close()


if __name__ == '__main__':
    facebook_url = ''  # like : https://www.facebook.com/channel/videos/video_id
    fb_download(facebook_url)

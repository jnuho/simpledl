# EP1: Finding data
from urllib.request import Request, urlopen
from os.path import exists, join
from os import mkdir
from tqdm import tqdm

import argparse


URL = "https://raw.githubusercontent.com/asharov/cute-animal-detector/master/data/kitty-urls.txt"
# URL = "https://raw.githubusercontent.com/iblh/not-cat/master/urls/cat/cat-urls.txt"

def getUrlContent(url):
    requestItem = Request(url)
    response = urlopen(requestItem)
    return response.read()

def getList(url):
    CAT_URL_LIST = [ x for x in getUrlContent(url).decode("utf-8").split('\n') if x != '']
    return CAT_URL_LIST

def getImageItemFromURL(url, folder, idx):
    print(url)
    baseFolder = "data"
    if not exists(baseFolder):
        mkdir(baseFolder)
    folder = join(baseFolder, folder)

    if not exists(folder):
        mkdir(folder)

    try:
        content = getUrlContent(url)
        with open(join(folder, idx + ".jpg"), "wb") as imageFile:
            imageFile.write(content)
        indicator.update()
    except Exception as reason:
        print("reason -> " + str(reason))


# inside simpledl/backend/worker/pytorch, run:
# python download.py -u https://raw.githubusercontent.com/asharov/cute-animal-detector/master/data/kitty-urls.txt  -f cats
if __name__ == '__main__':
    parse = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parse.add_argument('-u', type=str)
    parse.add_argument('-f', type=str)

    args = parse.parse_args()
    urlList = getList(args.u)

    # getImageItemFromURLList(urlList=urlList, folder=args.f)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     executor.map(getImageItemFromURLList, urlList, args.f)
    indicator = tqdm(range(len(urlList)))
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     for url in urlList:
    #         print(url)
    #         executor.map(getImageItemFromURL, url, args.f, str(indicator.n))
    #         indicator.update()

    for url in urlList:
        getImageItemFromURL(url, args.f, str(indicator.n))
        indicator.update()

    print("urlList size: ", len(urlList))
    print("indicator: ", indicator.n)
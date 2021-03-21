import glob
import os


def getsize(url):
    files = glob.glob(url + '/*')
    return len(files)


def make_file(category, text, title=None, url='statics'):
    base_url = f'{url}/{category}'
    os.makedirs(base_url, exist_ok=True)
    if title is None:
        title = f'sample({getsize(base_url)})'
    url = f'{base_url}/{title}.txt'
    with open(url, mode='w', encoding='utf-8') as f:
        f.write(text)

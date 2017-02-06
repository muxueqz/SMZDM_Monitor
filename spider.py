import requests
import time
import json
from marshal import dump, load

cache_file = './sendmail.cache'

keys_file_path = './keys'
# like  'http://sc.ftqq.com/XXX.send'
base_url = ''

try:
    with(open(cache_file, 'rb')) as _fd:
        sended_list = load(_fd)
except IOError:
    sended_list = set()


def get_real_time_data():
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    url = 'http://www.smzdm.com/json_more?timesort=' + str(c_time)
    r = requests.get(url=url, headers=headers)

    data = r.text

    dataa = json.loads(data)

    resultList = []

    for string in dataa:
        title = string['article_title']
        price = ''
        if 'article_price' in string.keys():
            price = string['article_price']
        link = ''
        if 'article_link' in string.keys():
            link = string['article_link']
        page_url = string['article_url']
        result = {
            'title': title,
            'price': price,
            'link': link,
            'page_url': page_url
        }
        resultList.append(result)

    return resultList


def read_local_file_keys():
    with open(keys_file_path, 'rt', encoding='utf-8') as f:
        file_data = f.read()
        return file_data.split(sep=',')


def send_mail(data, key, title):
    subject = 'SMZDM关注关键字;key: %s, title: %s' % (
        key, title)
    url = "%s?text=%s&desp=%s" % (
        base_url, subject, data)
    requests.get(url=url)


def find_keys(result):
    for key in keys:
        if result['title'].find(key) != -1:
            if result['page_url'] not in sended_list:
                print (result)
                send_mail(str(result), key, result['title'])
                sended_list.add(result['page_url'])


if __name__ == '__main__':
    keys = read_local_file_keys()
    resultList = get_real_time_data()
    for result in resultList:
        find_keys(result)
    with(open(cache_file, 'wb')) as _fd:
        dump(sended_list, _fd)

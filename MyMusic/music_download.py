import urllib.request
import urllib.parse
import json
import re


def resemble_data(content, index):
    data = {}
    data['types'] = 'search'
    data['count'] = '30'
    data['source'] = 'netease'
    data['pages'] = index
    data['name'] = content
    data = urllib.parse.urlencode(data).encode('utf-8')
    return data


def request_music(url, content):
    # set proxy agent
    proxy_support = urllib.request.ProxyHandler({'http:': '119.6.144.73:81'})
    opener = urllib.request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36')]
    urllib.request.install_opener(opener)
    # set proxy agent
    total = []
    pattern = re.compile(r'(([sS]*))')
    for i in range(1, 10):
        data = resemble_data(content, str(i))
        response = urllib.request.urlopen(url, data)
        result = response.read().decode('unicode_escape')
        json_result = pattern.findall(result)
        total.append(json_result)
    return total


def save_music_file(id, name):
    save_path = r'F:\666'
    pattern = re.compile('http.*?mp3')
    url = 'http://www.gequdaquan.net/gqss/api.php?callback=jQuery111307210973120745481_1533280033798'
    data = {}
    data['types'] = 'url'
    data['id'] = id
    data['source'] = 'netease'
    data = urllib.parse.urlencode(data).encode('utf-8')
    response = urllib.request.urlopen(url, data)
    music_url_str = response.read().decode('utf-8')
    music_url = pattern.findall(music_url_str)
    result = urllib.request.urlopen(music_url[0])
    file = open(save_path + name + '.mp3', 'wb')
    file.write(result.read())
    file.flush()
    file.close()


def main():
    url = 'https://www.gequdaquan.net/gqss/api.php?callback=jQuery11130967955054499249_1533275477385'
    content = input('please input the artist name:')
    result = request_music(url, content)
    for group in result[0]:
        target = json.loads(group)
        for item in target:
            save_music_file(str(item['id']), str(item['name']))


main()

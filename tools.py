import requests
import urllib.request

def save_html(url, name):
    # r = requests.get(url)  # url - ссылка
    # html = r.text
    # f = open(f'{name}.html', 'w', encoding="utf-8")
    # f.write(html)
    # f.close()

    html = urllib.request.urlopen(url).read()
    f = open('page.html', 'wb')
    f.write(html)

    return html

save_html("https://cabinet.spbu.ru/Lists/1k_EntryLists/list_0aa95bd2-8183-4273-a61f-88fdab9f9d16.html", "a")
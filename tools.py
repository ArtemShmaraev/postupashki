import requests

def save_html(url, name):
    r = requests.get(url)  # url - ссылка
    html = r.text
    f = open(f'vuz/{name}/{name}.html', 'w', encoding="utf-8")
    f.write(html)
    f.close()
    return html
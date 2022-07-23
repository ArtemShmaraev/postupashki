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

save_html("https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-BUDJ-O-010304", "a")
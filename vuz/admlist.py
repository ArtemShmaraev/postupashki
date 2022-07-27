import re
from bs4 import BeautifulSoup
import requests
import urllib.request



def get_admlist(bt):
    url = ["http://admlist.ru/mipt/index.html",
           "http://admlist.ru/bmstu/index.html",
           "http://admlist.ru/mephi/index.html",
           "http://admlist.ru/miet/index.html",
           "http://admlist.ru/mai/index.html",
           "http://admlist.ru/mei/index.html",
           "http://admlist.ru/rudn/index.html",
           "http://admlist.ru/spbstu/index.html"]
    spisok = []

    for i in range(len(url)):
        html = urllib.request.urlopen(url[i]).read().decode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        vuz = soup.find_all("h1")[1].text.split()[-1]

        tab = soup.find_all("table")[1].find_all("tr")
        for j in range(len(tab)):
            nup = tab[j].find("a")
            if nup:
                urls = url[i].replace("index.html", nup.get("href"))
                nup = nup.text
                html = ""
                while html == "":
                    try:
                        html = urllib.request.urlopen(urls).read().decode('utf-8')
                    except Exception:
                        print("повтор")
                s = BeautifulSoup(html, "lxml")
                print(vuz, nup)
                table = s.find_all("table")[1].find_all("tr")
                try:
                    for g in range(len(table)):
                        row = table[g].find_all("td")
                        if row:
                            snils = int("".join(re.findall(r'\d+', row[3].text)))
                            sogl = row[4].text
                            vybor = sogl
                            n = row[5].text
                            ball = int(row[-2].text)
                            if "ОП" in n:
                                forma = "О"
                            elif "Ц" in n:
                                forma = "Ц"
                            elif "К" in n:
                                forma = "К"
                            elif "БВИ" in n:
                                forma = "БВИ"
                                ball = 311
                            else:
                                forma = "Б"

                            if ball > bt:
                                spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
                except Exception:
                    print('1')


    return spisok

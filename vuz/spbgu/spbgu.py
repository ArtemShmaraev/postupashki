import re
from bs4 import BeautifulSoup
import requests
import urllib.request


def get_spbgu():
    vuz = "СПБГУ"
    spisok = []
    url = "https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html"
    req = requests.get(url).text
    soup = BeautifulSoup(req, "lxml")
    pag = soup.findAll("a")[1:]
    for i in range(len(pag)):
        url = "https://cabinet.spbu.ru/Lists/1k_EntryLists/" + pag[i].get("href")
        html = ""
        while html == "":
            try:
                html = urllib.request.urlopen(url).read().decode('utf-8')
            except Exception:
                print("повтор")
        soup = BeautifulSoup(html, "lxml")
        n = soup.find("p").text.lower()
        s = n.find("направление")
        nup = n[s + 13:s + 21].replace(".", "")
        forma = "Б"
        if "особая квота" in n:
            forma = "О"
        if "специальная квота" in n:
            forma = "С"
        if "целевая квота" in n:
            forma = "Ц"
        if "договорная" in n:
            forma = "К"
        print(vuz, nup, forma)
        if nup[:2] == "39":
            break

        table = soup.find_all("tr")[1:]
        for j in range(len(table)):
            try:
                row = table[j].find_all("td")
                snils = int("".join(re.findall(r'\d+', row[1].text)))
                if forma == "К":
                    ball = int(row[3].text[:-3])
                    sogl = row[9].text
                    vybor = sogl  # нет столбца аттестат
                    if ball > 245:
                        spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
                    else:
                        break

                else:
                    if row[2].text == "Без ВИ":
                        ball = 311
                        sogl = row[10].text
                        vybor = sogl  # нет столбца аттестат
                        spisok.append([int(snils), ball, sogl, vybor, nup, vuz, "БВИ"])

                    else:
                        ball = int(row[4].text[:-3])
                        sogl = row[10].text
                        vybor = sogl  # нет столбца аттестат
                        if ball > 245:
                            spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
                        else:
                            break
            except Exception:
                pass
    return spisok

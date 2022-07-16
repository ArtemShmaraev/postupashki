import re
from bs4 import BeautifulSoup
import requests


def get_mtusi():
    vuz = "МТУСИ"
    spisok = []
    url = "https://lk.abitur.mtuci.ru/staticPage.php?page_name=spiski"
    req = requests.get(url).text
    soup = BeautifulSoup(req, "lxml")
    pagе = soup.findAll("a")[6:]
    for i in range(len(pagе)):
        nup = pagе[i].text
        print(vuz, nup)
        url = f"https://lk.abitur.mtuci.ru/ajax.php?function=get_direction_list&direction_id={pagе[i].get('data-direction-id')}&type=neuch"
        req = requests.get(url).text
        soup = BeautifulSoup(req, "lxml")
        table = soup.findAll("tr")[1:]
        for j in range(len(table)):
            row = table[j].find_all("td")
            snils = int("".join(re.findall(r'\d+', row[2].text)))
            ball = int(row[8].text)
            sogl = row[11].text
            vybor = row[10].text
            if ball > 245:
                spisok.append([int(snils), ball, sogl, vybor, nup, vuz, "Б"])
            else:
                break
    return spisok

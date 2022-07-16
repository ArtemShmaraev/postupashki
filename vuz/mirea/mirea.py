import re
from bs4 import BeautifulSoup

import requests



def get_mirea():
    print("Сбор данных МИРЭА")
    spisok = []
    vuz = "МИРЭА"
    html = open("vuz/mirea/mirea.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")
    pag = soup.findAll("a", class_="showListingBtn")

    for j in range(len(pag)):
        url = "https://priem.mirea.ru/accepted-entrants-list/" + pag[j].get("href")
        r = requests.get(url)  # url - ссылка
        html = r.text
        soup = BeautifulSoup(html, "lxml")

        # получаю направление и факультет
        page = soup.find("p", class_='namesListPlan')
        t = str(page.text)
        t = t.replace("Условия поступления:", "")
        t = t.split("/")
        t[0] = t[0].strip().split(" ")
        nup = t[0][0] + t[0][-1]
        nup = nup.replace(".", "").strip()
        f = t[-1].strip()
        if "общий" in f:
            forma = "Б"
        elif "без ви" in f.lower():
            forma = "БВИ"
        elif "особ" in f:
            forma = "О"
        elif "спец" in f:
            forma = "С"
        elif "договор" in f:
            forma = "К"
        else:
            continue
        print(vuz, nup, forma)

        # поиск таблицы, срез для того чтобы убрать первую строку
        table = soup.find("table").findAll("tr")[1:]
        for i in range(len(table)):
            snils = int("".join(re.findall(r'\d+', table[i].find("td", class_="fio").text)))
            if forma == "БВИ":
                ball = 311
            else:
                ball = int(table[i].find("td", class_="sum").text) + int(table[i].find("td", class_="achievments").text)
            sogl = table[i].find("td", class_="accepted").text
            vybor = table[i].find("td", class_="original").text
            if ball > 245:
                spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
            else:
                break

    return spisok

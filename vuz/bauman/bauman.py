import re
from bs4 import BeautifulSoup
import tabula
import urllib.request
import csv


def get_bauman():
    spisok = []
    vuz = "Бауманка"
    html = open(f"vuz/bauman/bauman.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")
    pagе = soup.findAll("a")
    for i in range(len(pagе)):
        nup = pagе[i].text[15:23].replace(".", '')
        url = f'https://priem.bmstu.ru{pagе[i].get("href")}'
        urllib.request.urlretrieve(url, "vuz/bauman/bauman.pdf")
        tabula.convert_into("vuz/bauman/bauman.pdf", "vuz/bauman/bauman.csv", output_format="csv", pages='all')
        print(vuz, nup)
        forma = "Квота"
        sp = []
        with open('vuz/bauman/bauman.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0].isdigit():
                    sp.append(row)
        for j in range(len(sp)):
            row = sp[j]
            if row[0] == "1" and len(sp) - j == int(sp[-1][0]):
                forma = "Б"
            snils = int("".join(re.findall(r'\d+', row[1])))
            if row[3][:3].isdigit():
                ball = int("".join(re.findall(r'\d+', row[3])))
                if forma == "БВИ":
                    forma = "Б"
            else:
                ball = 311
                forma = "БВИ"
            sogl = "Нет"
            vybor = "Нет"
            if "да да" in (" ".join(row)).lower():
                sogl = "Да"
                vybor = "Да"

            if ball > 245 or "Б" not in forma:
                spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
    return spisok


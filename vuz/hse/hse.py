from bs4 import BeautifulSoup
import urllib.request
import openpyxl
import re


def get_hse(name):
    spisok = []
    d = {"hse": "ВШЭ", "hse-spb": "ВШЭ СПБ", "hse_nn": "ВШЭ НН", "hse_p": "ВШЭ П"}
    vuz = d[name]
    html = open(f"vuz/{name}/{name}.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")
    page = soup.findAll("td")[2:]
    for i in range(0, len(page), 2):
        url = page[i + 1].text.strip()
        urllib.request.urlretrieve(url, "hse.xlsx")
        wookbook = openpyxl.load_workbook("hse.xlsx")
        worksheet = wookbook.active
        nup = page[i].text
        print(vuz, nup)
        for y in range(18, worksheet.max_row + 1):
            u = []
            for x in range(1, worksheet.max_column):
                c = worksheet.cell(row=y, column=x).value
                if c is not None:
                    u.append(c)
            if len(u) > 12:
                try:
                    snils = int("".join(re.findall(r'\d+', u[1])))
                    ball = int(u[-7])

                    if u[2] == "Да":
                        forma = "БВИ"
                        ball = 311
                    elif u[3] == "Да":
                        forma = "О"
                    elif u[5] == "Да":
                        forma = "С"
                    else:
                        forma = u[-6]
                    vybor = u[-5]
                    sogl = u[-4]
                    if ball > 245:
                        spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
                except Exception:
                    print("Ошибка")
    return spisok

from bs4 import BeautifulSoup
import urllib.request
import openpyxl
import re



def get_hse():
    spisok = []
    vuz = "ВШЭ"
    html = open("vuz/hse/hse.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")
    page = soup.findAll("a")
    s = []
    for i in range(len(page)):
        s.append(page[i].get("href"))

    for i in range(len(s)):
        url = s[i]
        urllib.request.urlretrieve(url, "hse.xlsx")
        wookbook = openpyxl.load_workbook("hse.xlsx")
        worksheet = wookbook.active
        for y in range(1, 4):
            for x in range(1, worksheet.max_column):
                c = worksheet.cell(row=y, column=x).value
                if c is not None:
                    if "Направление" in c:
                        nup = (''.join(i for i in c if i.isdigit()))
                        break

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

                    spisok.append([snils, ball, sogl, vybor, nup, vuz, forma])
                except Exception:
                    print("Ошибка")

    return spisok

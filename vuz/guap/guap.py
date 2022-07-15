from bs4 import BeautifulSoup
import requests
import re

def get_guap():
    mainurl = "https://priem.guap.ru/_lists/Pred_37"
    req = requests.get(mainurl)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    maintable = soup.find("table", class_="table table-hover")
    nups = maintable.find("tbody").find_all("tr")

    spisok = []
    formadict = {0: "Б", 1: "Ц", 2: "О", 3: "С", 4: "К"}
    vuz = 'ГУАП'

    for i in nups:
        alltd = i.find_all("td")
        nup = alltd[1].text
        alltd = alltd[2:]
        print(vuz, nup)
        for j in alltd:
            if alltd.index(j) == 5:
                break

            a = j.text
            if a != '' and a != '-' and a[0] != '0':
                href = "https://priem.guap.ru" + j.find("a").get("href")

                req1 = requests.get(href)
                src1 = req1.text
                soup1 = BeautifulSoup(src1, "lxml")
                table = soup1.find("table", class_="table table-hover")
                alltr = table.find("tbody").find_all("tr")

                for tr in alltr:
                    tds = tr.find_all("td")
                    snils = int("".join(re.findall(r'\d+', tds[0].text)))
                    #snils = tds[0].text.replace('-', '').replace(' ', '')
                    ball = int(tds[4].text)
                    p = tds[5].text
                    if p == 'Да':
                        forma = 'БВИ'
                        ball = 311
                    else:
                        forma = formadict[alltd.index(j)]
                    sogl = tds[6].text
                    vybor = tds[7].text
                    if ball > 245:
                        spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])

    return spisok
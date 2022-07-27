from bs4 import BeautifulSoup
import requests


def get_guap(bt):
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
                href = "https://priem.guap.ru/_lists/" + j.find("a").get("href")

                req1 = requests.get(href)
                src1 = req1.text
                soup1 = BeautifulSoup(src1, "lxml")
                table = soup1.find("table", class_="table table-hover pk-ratings-table")
                alltr = table.find("tbody").find_all("tr")

                for tr in alltr:
                    tds = tr.find_all("td")
                    snils = tds[0].text.replace('-', '').replace(' ', '')
                    ball = tds[4].text
                    forma = formadict[alltd.index(j)]
                    if ball == 'Без В/И':
                        forma = 'БВИ'
                        ball = '311'
                    sogl = tds[6].text
                    vybor = tds[7].text
                    if int(ball) > bt:
                        spisok.append([snils, int(ball), sogl, vybor, nup, vuz, forma])
    return spisok
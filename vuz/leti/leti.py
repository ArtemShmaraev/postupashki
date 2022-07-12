from bs4 import BeautifulSoup
import requests


def tohtml(src, file):
    with open(f"{file}", "w", encoding="utf-8") as f:
        f.write(src)


def get_leti():
    url = 'https://abit.etu.ru/ru/postupayushhim/bakalavriat-i-specialitet/spiski-podavshih-zayavlenie/'

    req = requests.get(url)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    # all_tr = soup.find_all("div", class_="table-responsive")
    table = soup.find("table").findAll("tr")[2:]

    spisok = []
    vuz = 'ЛЭТИ'
    for item in table:
        href = "https://abit.etu.ru/" + item.find_all("a")[0].get("href")
        nup = item.text.split('\n')[2]
        print(vuz, nup, "Б")
        req1 = requests.get(href)
        src1 = req1.text
        soup1 = BeautifulSoup(src1, "lxml")
        # nazv = soup1.find("h1", class_="page-header").text
        table1 = soup1.find("div", class_="table-responsive").find_all("tr")[2:]

        for i in table1:
            snils = i.find("td", class_="fio").text.replace('-', '').replace(' ', '')
            f1 = i.find("td", class_="group").text
            ball = i.find("td", class_="ball").text
            sogl = i.find("td", class_="is-agree").text
            vybor = i.find("td", class_="is-original").text
            if f1 == 'ОК':
                forma = 'Б'
            if f1 == 'ЦК':
                forma = 'Ц'
            if f1 == 'ОП':
                forma = 'О'
            if f1 == 'СК-1' or f1 == 'СК-2':
                forma = 'С'
            if f1 == 'БВИ':
                forma = 'БВИ'
                ball = 311
            if f1 == "К":
                forma = "К"
            spisok.append([snils, ball, sogl, vybor, nup, vuz, forma])
        try:
            href = "https://abit.etu.ru/" + item.find_all("a")[1].get("href")
            nup = item.text.split('\n')[2]
            print(vuz, nup, "К")
            req1 = requests.get(href)
            src1 = req1.text
            soup1 = BeautifulSoup(src1, "lxml")
            table1 = soup1.find("div", class_="table-responsive").find_all("tr")[2:]
            for i in table1:
                snils = i.find("td", class_="fio").text.replace('-', '').replace(' ', '')
                ball = i.find("td", class_="ball").text
                sogl = i.find("td", class_="is-agree").text
                vybor = i.find("td", class_="is-original").text
                forma = "K"
                spisok.append([snils, ball, sogl, vybor, nup, vuz, forma])
        except Exception:
            print("Ошибка")
    return spisok


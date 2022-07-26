import re
from bs4 import BeautifulSoup
import requests


def get_misis(bt):
    url = ["https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-BUDJ-O-010304",
           "https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-BUDJ-O-090300",
           "https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-CELEV-O-010304",
           "https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-CELEV-O-090301",
           "https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-CELEV-O-090302",
           "https://misis.ru/applicants/admission/progress/baccalaureate-and-specialties/list-of-applicants/list/?id=BAC-CELEV-O-090303"]
    spisok = []
    vuz = "МИСИС"
    for i in range(len(url)):
        nup = "".join(re.findall(r'\d+', url[i]))
        soup = BeautifulSoup(requests.get(url[i]).text, "lxml")
        page = soup.find_all("tr")
        print(vuz, nup)
        for j in range(len(page)):
            t = page[j].find_all("td")
            if t:
                snils = "".join(re.findall(r'\d+', t[2].text))
                if snils:
                    ball = int(t[4].text)
                    if "БВИ" in t[-3].text:
                        forma = "БВИ"
                        ball = 311
                    elif "СК" in t[-3].text:
                        forma = "C"
                    elif "М" in t[-3]:
                        forma = "Б"
                    elif "ОК" in t[-3]:
                        forma = "О"
                    elif "ЦП" in t[-3]:
                        forma = "Ц"
                    else:
                        forma = "Б"
                    sogl = "Нет"
                    vybor = "Нет"
                    if t[-5].text == "+":
                        sogl = "Да"
                    if t[-4].text == "+":
                        vybor = "Да"
                    if ball > bt:
                        spisok.append([int(snils), ball, sogl, vybor, nup, vuz, forma])
    return spisok

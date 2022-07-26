import re
from bs4 import BeautifulSoup
import requests
import json


def get_spisok(s, forma, nup, bt):
    sp = []
    for g in range(len(s)):
        st = s[g]
        snils = st["snils"]
        if snils:
            sogl = st["send_agreement"]
            if sogl:
                sogl = "Да"
            else:
                sogl = "Нет"
            vybor = st["is_send_original"]
            if vybor:
                vybor = "Да"
            else:
                vybor = "Нет"
            ball = st["total_scores"]
            if forma == "БВИ":
                ball = 311
            if ball > bt or "Б" not in forma:
                sp.append([int(snils), ball, sogl, vybor, nup, "ИТМО", forma])
    return sp


def get_itmo(bt):
    spisok = []
    vuz = "ИТМО"
    html = open("vuz/itmo/itmo.html", encoding="utf-8").read()
    soup = BeautifulSoup(html, "lxml")
    page = soup.findAll("a")
    for i in range(len(page)):
        s = page[i].get("href").split("/")[1:]
        url = f"https://abitlk.itmo.ru/api/v1/9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429/rating/bachelor/budget?program_id={s[3]}"
        js = json.loads(requests.get(url).text)
        nup = "".join(re.findall(r'\d+', js["result"]['direction']['direction_title']))
        print(vuz, nup)
        spisok.extend(get_spisok(js["result"]['without_entry_tests'], "БВИ", nup, bt))
        spisok.extend(get_spisok(js["result"]["by_unusual_quota"], "О", nup, bt))
        spisok.extend(get_spisok(js["result"]["by_special_quota"], "С", nup, bt))
        spisok.extend(get_spisok(js["result"]["by_target_quota"], "Ц", nup, bt))
        spisok.extend(get_spisok(js["result"]["general_competition"], "Б", nup, bt))

        url = f"https://abitlk.itmo.ru/api/v1/9e2eee80b266b31c8d65f1dd3992fa26eb8b4c118ca9633550889a8ff2cac429/rating/bachelor/contract?program_id={s[3]}"
        js = json.loads(requests.get(url).text)
        spisok.extend(get_spisok(js["result"]["items"], "K", nup, bt))
    return spisok


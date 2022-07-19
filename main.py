from data import db_session
from data.user import User
import xlsxwriter
from inBD import in_BD
from outBD import out_BD
from datetime import datetime as dt
from flask import Flask, render_template
from data.form import Form
from flask_ngrok import run_with_ngrok
import re

from vuz.mirea.mirea import get_mirea
from vuz.hse.hse import get_hse
from vuz.leti.leti import get_leti
from vuz.itmo.itmo import get_itmo
from vuz.mtusi.mtusi import get_mtusi
from vuz.spbgu.spbgu import get_spbgu
from vuz.guap.guap import get_guap
from vuz.bauman.bauman import get_bauman

# запуск приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
#run_with_ngrok(app)


def main():
    # out_BD("ВШЭ")
    # in_BD(get_mirea())
    in_BD(get_hse("hse"))
    in_BD(get_hse("hse_spb"))
    in_BD(get_hse("hse_nn"))
    in_BD(get_hse("hse_p"))
    # in_BD(get_itmo())
    # in_BD(get_leti())
    # in_BD(get_guap())
    # in_BD(get_mtusi())
    # in_BD(get_bauman())
    # in_BD(get_spbgu())

    print("Все базы загружены, выберите вуз и направление: ")
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        vuz = form.vuz.data
        nupravlen = form.nup.data
        nupravlenie = nupravlen.replace(".", "")
        snils = int("".join(re.findall(r'\d+', form.snils.data)))  # снилс или балл

        db_sess = db_session.create_session()
        name = f"{vuz}_{nupravlenie}_sp{str(dt.now())[20:26]}"
        workbook = xlsxwriter.Workbook(f'static/{name}.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Снилс")
        worksheet.write(0, 1, "Балл")
        worksheet.write(0, 2, "Согласие")
        worksheet.write(0, 3, "Аттестат")
        worksheet.write(0, 4, "Подал")
        row = 1
        top = []
        for user in db_sess.query(User).all():
            if f"{vuz} | {nupravlenie} | Б".lower() in user.podal.lower():
                worksheet.write(row, 0, str(user.snils))

                s = user.podal.split("$")
                ball = 0
                for i in range(len(s)):
                    t = s[i].split("|")
                    if t[0].lower().strip() == vuz.lower().strip() and t[
                        1].lower().strip() == nupravlenie.lower().strip():
                        ball = max(ball, int(t[3]))
                if int(snils) == int(user.snils):
                    snils = ball
                worksheet.write(row, 1, ball)
                worksheet.write(row, 2, "\n".join(user.sogl.split("$")))

                s_vybor = set()
                t_v = user.vybor.split("$")
                for i in range(len(t_v)):
                    s_vybor.add(t_v[i].split("|")[0])
                worksheet.write(row, 3, "\n".join(list(s_vybor)))
                worksheet.write(row, 4, "\n".join(user.podal.split("$")))

                f = 0
                if f"{vuz} | {nupravlenie} | Б".lower() in user.sogl.lower():
                    f = 1
                elif len(user.sogl) > 1:
                    f = 2
                top.append([ball, user.snils, f])
                row += 1
        workbook.close()

        top.sort(reverse=True)
        mesto = 1
        mesto_sogl = 1
        mesto_t = 1
        in_top = False
        bvi = 0
        for i in range(len(top)):
            if top[i][0] == 311:
                bvi += 1
            if top[i][0] <= snils <= 310:
                in_top = True
                break
            if top[i][2] == 1:
                mesto_sogl += 1
                mesto += 1
                mesto_t += 1
            elif top[i][2] == 2:
                mesto += 1
            else:
                mesto += 1
                mesto_t += 1
        if not in_top:
            mesto = 0
            mesto_sogl = 0
            mesto_t = 0

        return render_template(f"post.html", f=f"{name}.xlsx", m1=mesto, m2=mesto_t, m3=mesto_sogl, vuz=vuz,
                               nup=nupravlen, bvi=bvi)

    return render_template("index.html", form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()
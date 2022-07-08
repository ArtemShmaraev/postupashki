from data import db_session
from mirea import get_mirea
from data.user import User
import xlsxwriter
from inBD import in_BD
from datetime import datetime as dt
from flask import Flask, render_template, redirect, make_response, jsonify, request
from random import randint
from data.form import Form
from flask_ngrok import run_with_ngrok


# запуск приложения
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


#run_with_ngrok(app)

def main():
    spisok = []
    spisok.extend(get_mirea())
    in_BD(spisok)
    print("Все базы загружены, выберите вуз и направление: ")
    app.run(port=8080)



@app.route("/", methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        vuz = form.vuz.data
        nupravlenie = form.nup.data
        db_sess = db_session.create_session()
        name = f"{vuz}_{nupravlenie}_sp{str(dt.now())[20:26]}"
        workbook = xlsxwriter.Workbook(f'static/{name}.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "Снилс")
        worksheet.write(0, 1, "Балл")
        worksheet.write(0, 2, "Согласие")
        worksheet.write(0, 3, "Аттестат")
        row = 1
        for user in db_sess.query(User).all():
            if f"{vuz} | {nupravlenie} | Б".lower() in user.podal.lower():
                worksheet.write(row, 0, str(user.snils))
                s = user.podal.split("$")
                for i in range(len(s)):
                    t = s[i].split("|")
                    if t[0].lower().strip() == vuz.lower().strip() and t[1].lower().strip() == nupravlenie.lower().strip():
                        worksheet.write(row, 1, t[3])
                worksheet.write(row, 2, user.sogl)
                worksheet.write(row, 3, user.vybor)
                row += 1
        workbook.close()
        return render_template(f"post.html", f=f"{name}.xlsx")

    return render_template("index.html", form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    main()
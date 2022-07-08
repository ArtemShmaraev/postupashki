from data.user import User
from data import db_session


def in_BD(spisok):
    db_sess = db_session.create_session()
    for i in range(len(spisok)):
        snils = spisok[i][0]
        ball = spisok[i][1]
        sogl = spisok[i][2]
        vybor = spisok[i][3]
        nup = spisok[i][4]
        vuz = spisok[i][5]
        forma = spisok[i][6]

        user = db_sess.query(User).filter(User.snils == snils).first()
        if user:
            if (f"{vuz} | {nup} | {forma}".lower()) not in user.podal.lower():
                user.podal += (f" {vuz} | {nup} | {forma} | {ball}$")

            if vybor == "да" and (f" {vuz} | {nup} | {forma} | {ball}$".lower()) not in user.vybor.lower():
                user.vybor += f" {vuz} | {nup} | {forma} | {ball}$"
            if sogl == "да" and (f" {vuz} | {nup} | {forma} | {ball}$".lower()) not in user.sogl.lower():
                user.sogl += f" {vuz} | {nup} | {forma} | {ball}$"

        else:
            user = User()
            user.snils = snils
            user.podal = f" {vuz} | {nup} | {forma} | {ball}$"
            if vybor == "да":
                user.vybor = f" {vuz} | {nup} | {forma} | {ball}$"
            if sogl == "да":
                user.sogl = f" {vuz} | {nup} | {forma} | {ball}$"
            db_sess.add(user)
        db_sess.commit()
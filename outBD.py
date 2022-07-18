from data.user import User
from data import db_session


def out_BD(vuz):
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if vuz in user.podal:
            podal = user.podal.split("$")
            sogl = user.sogl.split("$")
            vybor = user.vybor.split("$")
            for i in range(len(podal) - 1, -1, -1):
                if vuz in podal[i]:
                    del podal[i]
            for i in range(len(sogl) - 1, -1, -1):
                if vuz in sogl[i]:
                    del sogl[i]
            for i in range(len(vybor) - 1, -1, -1):
                if vuz in vybor[i]:
                    del vybor[i]
            user.podal = "$".join(podal)
            user.sogl = "$".join(sogl)
            user.vybor = "$".join(vybor)
    db_sess.commit()



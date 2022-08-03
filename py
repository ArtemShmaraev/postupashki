import time, json, datetime, vk_api
from random import randint, choice

from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType

from data import db_session
from data.user import User
from function.vk_func import get_but
from function.other_func import top, oshibki, summa, sbros_nedeli


def sender(id, text):
    vk_sess.method('messages.send',
                   {'user_id': id, 'message': text, 'random_id': randint(1, 1000000000), "keyboard": keyboard})


def edit(text, id, event):
    vk_sess.method('messages.edit', {'message_id': id, 'message': text, "peer_id": event.peer_id})


def check(user, n):
    s = user.bad_slova.split()
    s[user.id_slova - 1] = str(max(0, int(s[user.id_slova - 1]) + n))
    user.bad_slova = " ".join(s)


def game(id, tren, db_sess):
    user = db_sess.query(User).filter(User.tg_id == id).first()
    f = open("q.txt", "r", encoding="utf-8").read().split("\n")
    if tren:
        s = []
        sp = user.bad_slova.split()
        for i in range(len(sp)):
            if sp[i] != "0":
                s.append(i + 1)
        if len(s) == 0:
            slovo = randint(1, len(f))
            user.tren = 0
            sender(id, "Ты исправил все ошибки🥳\nНачинаю обычный тест")
        else:
            slovo = choice(s)
    else:
        slovo = randint(1, len(f))
    if user.error == 0:
        user.slovo = f[slovo - 1]
        user.id_slova = slovo
        db_sess.commit()
        vy = user.slovo.lower()
    else:
        vy = user.slovo.lower() + " ❌"

    settings = dict(one_time=False, inline=True)
    keyboard_ = VkKeyboard(**settings)
    g = "уеэоаыяиюё"
    k = 0
    for i in range(len(user.slovo)):
        if user.slovo[i].lower() in g:
            if k == 0:
                k += 1
            else:
                keyboard_.add_line()
            keyboard_.add_button(label=user.slovo[:i].lower() + user.slovo[i].upper() + user.slovo[i + 1:].lower(),
                                 color=VkKeyboardColor.PRIMARY)

    user.msg = vk.messages.send(
        user_id=user.tg_id,
        random_id=randint(1, 1000000000),
        peer_ids=user.tg_id,
        keyboard=keyboard_.get_keyboard(),
        message=vy)
    db_sess.commit()


def rassylka(text, db_sess):
    for user in db_sess.query(User).all():
        time.sleep(0.05)
        try:
            vk.messages.send(
                user_id=user.tg_id,
                random_id=randint(1, 1000000000),
                message=text
            )
        except Exception as e:
            print(e)


def del_user(user):
    user.balance = 0
    user.slovo = ""
    user.good = 0
    user.bad = 0
    user.error = 0
    user.msg = 0
    user.bad_slova = "0 " * 600
    user.id_slova = 0
    user.tren = 0
    user.nedel = 0


vk_sess = vk_api.VkApi(token="8a07dc2550ebf5edbf4446ee1d178c8f9cbf702e81bea8fa672826b957051fe91828bbd0a95deb9e51d62")
vk = vk_sess.get_api()
longpoll = VkLongPoll(vk_sess)
db_session.global_init("db/mars1.db")

keyboard = {
    "one_time": False,
    "buttons": [
        [get_but('Старт📚', 'primary'), get_but('Счёт🎯', 'secondary')],
        [get_but('Ошибки❌', 'secondary'), get_but('Топ🏆', 'positive')],
        [get_but('Розыгрыш 🤩', 'secondary')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
db_sess = db_session.create_session()

for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW:
            user = db_sess.query(User).filter(User.tg_id == event.user_id).first()
            if user is None:
                user_get = vk.users.get(user_ids=(event.user_id))
                user_get = user_get[0]
                first_name = user_get['first_name']
                last_name = user_get['last_name']
                full_name = first_name + " " + last_name
                user = User(name=full_name, tg_id=event.user_id)
                db_sess.add(user)
                db_sess.commit()
            if event.to_me:
                if user.buy == 10:
                    pass
                elif event.text.lower() in user.slovo.lower():
                    if event.text == user.slovo:
                        if not user.error:
                            check(user, -1)
                        user.error = 0
                        user.balance += 1
                        user.nedel += 1
                        user.good += 1
                        vk.messages.delete(
                            peer_id=event.peer_id,
                            message_id=user.msg,
                            delete_for_all=True)
                        sender(event.user_id, user.slovo + " ✅")
                    else:
                        if user.error != 1:
                            user.balance -= 2
                            user.nedel -= 2
                            user.bad += 1
                            check(user, 2)
                        user.error = 1
                        vk.messages.delete(
                            peer_id=event.peer_id,
                            message_id=user.msg,
                            delete_for_all=True)
                    db_sess.commit()
                    game(event.user_id, user.tren, db_sess)

                elif event.text.lower() == "старт" or event.text.lower() == "старт📚":
                    user.tren = 0
                    game(event.user_id, False, db_sess)
                elif event.text.lower() == "исправить ошибки ✅":
                    user.tren = 1
                    game(event.user_id, True, db_sess)

                elif event.text.lower() == "счёт" or event.text.lower() == "счёт🎯":
                    procent = round((user.good * 100) / max(1, (user.good + user.bad)), 3)
                    sender(event.user_id,
                           f"Счёт: {str(user.balance)} 🎯\nПравильно: {str(user.good)} ✅\nНеправильно: {str(user.bad)} "
                           f"❌\nТочность {procent}% 🎲\nЗа неделю: {str(user.nedel)} 🎯")
                elif event.text.lower() == "сброс":
                    del_user(user)
                    db_sess.commit()
                    sender(event.user_id, "Данные удалены")
                elif event.text.lower() == "сброс слова":
                    user.error = 0
                    user.slovo = ""
                    user.msg = 0
                    sender(event.user_id, "Данные слова удалены")
                    game(event.user_id, False, db_sess)
                elif event.text.lower() == "топ" or event.text.lower() == "топ🏆":
                    st = top(event.user_id, 0, db_sess)
                    settings = dict(one_time=False, inline=True)
                    keyboard_ = VkKeyboard(**settings)
                    keyboard_.add_button(label="Точность 🎲", color=VkKeyboardColor.PRIMARY)
                    keyboard_.add_button(label="Топ недели 🌟", color=VkKeyboardColor.PRIMARY)
                    vk.messages.send(
                        user_id=event.user_id,
                        random_id=randint(1, 1000000000),
                        peer_ids=event.user_id,
                        keyboard=keyboard_.get_keyboard(),
                        message=st)
                elif event.text.lower() == "точность 🎲":
                    sender(event.user_id, top(event.user_id, 1, db_sess))
                elif event.text.lower() == "топ недели 🌟":
                    sender(event.user_id, top(event.user_id, 2, db_sess))
                elif event.text.lower() == "ошибки" or event.text.lower() == "ошибки❌":
                    st = oshibki(user)
                    settings = dict(one_time=False, inline=True)
                    keyboard_ = VkKeyboard(**settings)
                    keyboard_.add_button(label="Исправить ошибки ✅", color=VkKeyboardColor.PRIMARY)
                    vk.messages.send(
                        user_id=user.tg_id,
                        random_id=randint(1, 1000000000),
                        peer_ids=user.tg_id,
                        keyboard=keyboard_.get_keyboard(),
                        message=st)
                elif event.text.lower() == "начать":
                    name = user.name.split()[0]
                    sender(event.user_id, f"Привет, {name} 🥳\nЯ помогу тебе выучить все ударения ⭐\n️Для этого просто "
                                          f"нажми 'Старт' 😃\nЗа правильный ответ +1 🎯\nЗа неправильный -2 "
                                          f"🎯\nСоревнуйся с друзьями и учись 🏆 ")
                elif event.text.lower() == "игроки":
                    sender(event.user_id, len(db_sess.query(User).all()))
                elif event.text.lower()[:4] == "блок":
                    name = event.text[5:]
                    print(name)
                    usr = db_sess.query(User).filter(User.name == name).first()
                    usr.buy = 10
                    sender(event.user_id, "Ок")
                elif event.text.lower() == "фича5":
                    a = randint(-800, 350)
                    user.balance += a
                    user.nedel += a
                    procent = round((user.good * 100) / (user.good + user.bad), 3)
                    sender(event.user_id,
                           f"Ты получаешь {a} очков\nСчёт: {str(user.balance)} 🎯\nПравильно: {str(user.good)} ✅\n"
                           f"Неправильно: {str(user.bad)} ❌\nТочность {procent}% 🎲")
                elif "/спам" in event.text.lower():
                    rassylka(event.text[5:], db_sess)
                    sender(event.user_id, "Готово Босс")
                elif event.text.lower() == "сумма":
                    sender(event.user_id, summa(db_sess))
                elif event.text.lower() == "новая неделя":
                    sbros_nedeli(db_sess)
                    sender(event.user_id, "Готово Босс")
                elif event.text.lower() == "розыгрыш 🤩":
                    sender(event.user_id, open("розыгрыш.txt", encoding='utf-8').read())
                elif event.text.lower() == "машина":
                    sender(event.user_id, "Что вы хотели узнать?")
                    sender(365209216, user.name)
                else:
                    sender(365209216, " ⚠️ " + user.name + ":  " + event.text + " " + str(
                        datetime.datetime.now().strftime("%H:%M")))
                db_sess.commit()
    except Exception as e:
        sender(365209216, " ⚠️ " + str(e))
        # sender(event.user_id, "Произошла ошибка, подождите 5 сек. ☹️")
        time.sleep(2)
time.sleep(2)

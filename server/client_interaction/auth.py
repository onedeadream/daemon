import logging
from sqlalchemy.orm import sessionmaker
from model import engine, Users


def check_auth(con, data):
    Session = sessionmaker(bind=engine)
    session = Session(autoflush=True)
    logging.info('% Начало аутентификации %')
    auth_data = data.decode().replace("auth:", "").strip()
    auth_user = auth_data.split(', ')
    user = session.query(Users).filter_by(username=f'{auth_user[0]}').first()
    if user is None or (not user.password == auth_user[1]):
        con.send('disconnect'.encode())
        logging.warning('Пользователь ввел неправильные данные')
    else:
        con.send('accept'.encode())
        logging.info('Пользователь ввел правильные данные')
    session.close()
    con.close()

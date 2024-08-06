import logging
import threading
from datetime import datetime
from sqlalchemy.orm import sessionmaker

from model import engine, List_Hosts, Monitoring_System


def monitoring_system(connected_clients):
    logging.info('% Начало мониторинга систем %')
    threads = []
    for address, client in connected_clients.items():
        thread = threading.Thread(target=thread_monitoring, args=(client, address))
        thread.start()
        threads.append(thread)


def thread_monitoring(client, address):
    Session = sessionmaker(bind=engine)
    session = Session(autoflush=True)
    client.send(b'start monitoring')
    while True:
        try:
            monitoring_data = client.recv(4096)
            print(f'Пакет получен от {address[0]}')
            logging.info(f'Пакет получен от {address[0]}')
        except ConnectionResetError:
            logging.error(f'Соединение с {address[0]} было разорвано')
            break
        list_monitoring_data = monitoring_data.decode().split()
        logging.info(f'Данные от клиента: ' + str(monitoring_data.decode()))
        host = session.query(List_Hosts).filter_by(ip_address=address[0]).first()
        search_dependency = session.query(Monitoring_System).filter_by(host_id=host.id).first()
        current_time = datetime.now().strftime("%H:%M:%S")
        if search_dependency is None:
            # Создание нового объекта Monitoring_System
            new_monitoring_system = Monitoring_System(
                cpu_percent=['0'],
                gpu_percent=['0'],
                used_virtual_memory=['0'],
                temperature_gpu=['0'],
                used_disk=['0'],
                time_monitoring=[f'{current_time}'],
                host_id=host.id
            )
            session.add(new_monitoring_system)
            session.commit()
            logging.info(f'Добавлен новый пустой хост в таблицу Monitoring_System')
        add_search_dependency = session.query(Monitoring_System).filter_by(host_id=host.id).first()
        if host:
            current_time = datetime.now().strftime("%H:%M:%S")
            add_search_dependency.cpu_percent = add_search_dependency.cpu_percent + [list_monitoring_data[0]]
            add_search_dependency.gpu_percent = add_search_dependency.gpu_percent + [list_monitoring_data[1]]
            add_search_dependency.used_virtual_memory = add_search_dependency.used_virtual_memory + [
                list_monitoring_data[4]]
            add_search_dependency.temperature_gpu = add_search_dependency.temperature_gpu + [list_monitoring_data[2]]
            add_search_dependency.used_disk = add_search_dependency.used_disk + [list_monitoring_data[3]]
            add_search_dependency.time_monitoring = add_search_dependency.time_monitoring + [current_time]
            session.commit()
            logging.info(f'Добавлены новые данные о состоянии системы')


def screen_stream(data, connected_clients):
    ip = data.decode().replace("screen: ", "").strip()
    for ip_address, sock in connected_clients.items():
        # Проверка, совпадает ли удаленный IP-адрес с целевым IP-адресом
        if ip_address[0] == ip:
            # Найден сокет для целевого IP-адреса
            sock.send(b'screen')
            sock.close()
            break

import logging

from model import session
from model import List_Hosts, System_Info


def give_system_info(connected_clients):
    # Проверить, чтобы не заносились одинаковые данные
    logging.info('% Получение информации о системе хостов %')
    for address, client in connected_clients.items():
        logging.info('Пакет на получение системной информации был отправлен')
        client.send(b'system info')
        system_info = client.recv(1024)
        logging.info('Пакет на получение системной информации получен')
        data_list = system_info.decode().split(',')
        host = session.query(List_Hosts).filter_by(ip_address=address[0]).first()
        search_dependency = session.query(System_Info).filter_by(hosts_id=host.id).first()
        if host and search_dependency is None:
            new_system_info = System_Info(
                proc_name=data_list[0],
                freq_proc=data_list[1],
                gpu_name=data_list[2],
                gpu_memory=data_list[3],
                total_memory=data_list[4],
                total_virtual_memory=data_list[5]
            )
            new_system_info.host = host
            session.add(new_system_info)
            session.commit()
            logging.info('Полученный пакет и занесен в базу данных: ' + system_info.decode())
        else:
            logging.info(f"Ip адрес не найден: {address[0]} или информации о системе уже имеется")
    logging.info('Конец получения информации о системе')
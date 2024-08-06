import logging
import nmap

from model import List_Hosts, session


def make_scanning(client):
    all_hosts = list_ip_address()
    nm = nmap.PortScanner()
    logging.info('% Начало сканирования сети %')
    result = nm.scan('192.168.0.1/24')
    for ip_address in nm.all_hosts():
        pc_info = result['scan'][f'{ip_address}']
        host_name = nm[f'{ip_address}'].hostname()
        mac_address = pc_info.get('addresses', {}).get('mac')
        if mac_address is None:
            mac_address = ''
        if ip_address not in all_hosts:
            newServer = List_Hosts(host_name=f'{host_name}', ip_address=f'{ip_address}',
                                   mac_address=f'{mac_address}')
            session.add(newServer)
            session.commit()
            logging.info(f'Добавлен новый хост: {ip_address}')
    client.send('end scan'.encode())


def list_ip_address() -> list:
    hosts = session.query(List_Hosts).all()
    list_host = []
    # Формирование списка хостов из бд
    for host in hosts:
        list_host.append(host.ip_address)
    return list_host

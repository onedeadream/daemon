import socket
import psutil
import cpuinfo
import gpustat
import threading
from vidstream import ScreenShareClient


def send_packet():
    while True:
        data = client.recv(1024)
        if data.decode() == 'system info':
            thread_take_info = threading.Thread(target=about_system)
            thread_take_info.start()
        if data.decode() == 'start monitoring':
            thread_make_monitoring = threading.Thread(target=stat_system)
            thread_make_monitoring.start()
        if data.decode() == 'screen':
            thread_screen_stream = threading.Thread(target=screen_stream)
            thread_screen_stream.start()


def screen_stream():
    sender = ScreenShareClient('192.168.0.3', 9999)
    sender.start_stream()
    while input('') != 'STOP':
        continue
    sender.stop_stream()


def about_system():
    virtual_memory = psutil.virtual_memory()
    total_virtual_memory = round(virtual_memory.total / (1024 ** 3), 2)
    cpu_name = cpuinfo.get_cpu_info()['brand_raw']
    total_disk = round(psutil.disk_usage('/').total / (1024 ** 3), 2)
    system_info = f'{cpu_name},{cpuinfo.get_cpu_info()["hz_actual_friendly"]},{gpu_stats.gpus[0].name},{str(gpu_stats.gpus[0].memory_total)},{str(total_disk)},{str(total_virtual_memory)}'
    client.send(system_info.encode())


def stat_system():
    while True:
        new_gpu_stats = gpustat.GPUStatCollection.new_query()
        used_disk = round(psutil.disk_usage('/').used / (1024 ** 3), 2)
        cpu_percent = round(psutil.cpu_percent(interval=1) * 10, 2)
        gpu_percent = new_gpu_stats.gpus[0].utilization
        used_virtual_memory = round(psutil.virtual_memory().percent, 2)
        temperature_gpu = new_gpu_stats.gpus[0].temperature
        monitoring_system = f'{cpu_percent} {gpu_percent} {temperature_gpu} {used_disk} {used_virtual_memory}'
        client.send(monitoring_system.encode())
        monitoring_system = ''


if __name__ == '__main__':
    system_info = None
    gpu_stats = gpustat.GPUStatCollection.new_query()
    server_host = '192.168.0.3'
    server_port = 65325
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_host, server_port))
    client.send(b'connected')
    send_packet()

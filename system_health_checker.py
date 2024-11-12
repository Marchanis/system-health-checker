import psutil
import time 
from datetime import datetime


def get_cpu_usage():
    return psutil.cpu_percent(interval =1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return memory.percent

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent

def get_network_stats():
    net = psutil.net_io_counters()
    return net.bytes_sent, net.bytes_recv #This function provides the number of bytes sent and received by the network


def display_system_info():
    print("System Information and Health Chekcker")
    print("=" * 40)
    while True:
        cpu = get_cpu_usage()
        memory = get_memory_usage()
        disk = get_disk_usage()
        bytes_sent, bytes_recv = get_network_stats() # Get network statistics
        #function retrieves the network statistics (specifically, the amount of data sent and received by the system)

        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"CPU Usage: {cpu}%")
        print(f"Memory Usagr: {memory}%")
        print(f"Disk Usage: {disk}%")
        print(f"Network - Sent: {bytes_sent / (1024 ** 2):.2f} MB, Received: {bytes_recv / (1024 ** 2):.2f} MB") #There are 1024 bytes in a kilobyte (KB) and 1024 kilobytes in a megabyte (MB).
        print("-" * 40)

        check_alerts(cpu, memory, disk)



        time.sleep(5) #pause for 5 sec before updating


def check_alerts(cpu, memory, disk):
    if cpu > 80:
        print("ALERT! CPU Usage is over 80%")
    if memory > 80:
        print("ALERT! Memory Usage is over 80%")
    if disk > 90:
        print("ALERT! Disk Usage is over 90%")


if __name__ == "__main__":
    display_system_info()



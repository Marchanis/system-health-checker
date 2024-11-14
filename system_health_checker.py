import psutil
import time
import csv 
from datetime import datetime
import matplotlib.pyplot as plt



LOG_INTERVAL = 5  #pause for 5 sec before updating
CSV_FILE_PATH = "system_heath_log.csv"
HISTORY_LENGTH = 20 # numbers of intervals to keep in history for plotting


def get_cpu_usage():
    return psutil.cpu_percent(interval =1)

def get_memory_usage():
    memory = psutil.virtual_memory()
    return {
        "memory_percent" : memory.percent,
        "memory_used" : memory.used / (1024 ** 2),
        "memory_available" : memory.available / (1024 ** 2)
    }

def get_disk_usage():
    disk = psutil.disk_usage('/')
    return {
        "disk_percent" : disk.percent,
        "disk_used" : disk.used / (1024 ** 2),
        "disk_free" : disk.free / (1024 ** 2)

    }

def get_network_stats():
    net = psutil.net_io_counters()
    return {
        "bytes_sent": net.bytes_sent / (1024 ** 2),
        "bytes_received": net.bytes_recv / (1024 ** 2)
    }


def check_alerts(cpu, memory, disk):
    if cpu > 80:
        print("ALERT! CPU Usage is over 80%")
    if memory > 80:
        print("ALERT! Memory Usage is over 80%")
    if disk > 90:
        print("ALERT! Disk Usage is over 90%")


def display_system_info():
    print("System Information and Health Chekcker")
    print("=" * 40)

    #let's open CSV file to log data
    with open(CSV_FILE_PATH, "a", newline="") as csvfile:

        # set up CSV with headers 
        fieldnames = ["timestamp", "cpu_percent", "memory_percent","memory_used", "memory_available","disk_percent", "disk_used", "disk_free", "bytes_sent","bytes_received"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #write headers if the file is empty
        if csvfile.tell() ==0:
            writer.writeheader()

        # Initialize lists to store historical data for plotting
        cpu_history = []
        memory_history = []
        disk_history = []
        network_sent_history = []
        network_received_history = []

        plt.ion()  # Turn on interactive mode for live plotting

        # Loop to continuously log data and update plots

        while True:
            timestamp = datetime.now().strftime
            cpu = get_cpu_usage()
            memory = get_memory_usage()
            disk = get_disk_usage()
            network = get_network_stats()
        

            print(f"Time: {timestamp}")
            print(f"CPU Usage: {cpu}%")
            print(f"Memory Usage: {memory['memory_percent']}% (Used: {memory['memory_used']:.2f} MB, Available: {memory['memory_available']:.2f} MB)")
            print(f"Disk Usage: {disk['disk_percent']}% (Used: {disk['disk_used']:.2f} MB, Free: {disk['disk_free']:.2f} MB)")
            print(f"Network - Sent: {network['bytes_sent']:.2f} MB, Received: {network['bytes_received']:.2f} MB")
            print("-" * 40)

            check_alerts(cpu, memory['memory_percent'], disk['disk_percent'])

            #log data to CSV 
            writer.writerow({
                "timestamp": timestamp,
                "cpu_percent": cpu,
                "memory_percent": memory['memory_percent'],
                "memory_used": memory['memory_used'],
                "memory_available": memory['memory_available'],
                "disk_percent": disk['disk_percent'],
                "disk_used": disk['disk_used'],
                "disk_free":disk["disk_free"],
                "bytes_sent": network['bytes_sent'],
                "bytes_received": network['bytes_received']
            })

            # Update history lists
            cpu_history.append(cpu)
            memory_history.append(memory['memory_percent'])
            disk_history.append(disk['disk_percent'])
            network_sent_history.append(network['bytes_sent'])
            network_received_history.append(network['bytes_received'])

            #limit history to the last history length items
            if len(cpu_history) > HISTORY_LENGTH:
                cpu_history.pop(0)
                memory_history.pop(0)
                disk_history.pop(0)
                network_sent_history.pop(0)
                network_received_history.pop(0)
            
            plt.clf()

            plt.subplot(2, 2, 1)
            plt.plot(cpu_history, label="CPU Usage (%)", color="blue")
            plt.title("CPU Usage")
            plt.xlabel("Time")
            plt.ylabel("Usage (%)")
            plt.legend()

            plt.subplot(2, 2, 2)
            plt.plot(memory_history, label="Memory Usage (%)", color="green")
            plt.title("Memory Usage")
            plt.xlabel("Time")
            plt.ylabel("Usage (%)")
            plt.legend()

            plt.subplot(2, 2, 3)
            plt.plot(disk_history, label="Disk Usage (%)", color="red")
            plt.title("Disk Usage")
            plt.xlabel("Time")
            plt.ylabel("Usage (%)")
            plt.legend()

            plt.subplot(2, 2, 4)
            plt.plot(network_sent_history, label="Bytes Sent (MB)", color="orange")
            plt.plot(network_received_history, label="Bytes Received (MB)", color="purple")
            plt.title("Network Usage")
            plt.xlabel("Time")
            plt.ylabel("Data (MB)")
            plt.legend()

            plt.tight_layout()
            plt.pause(0.05) #pause briefly to update the plot

            time.sleep(LOG_INTERVAL)

if __name__ == "__main__":
    display_system_info()


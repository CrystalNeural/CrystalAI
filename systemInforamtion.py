import platform
import socket
import psutil
import os
import datetime
import json

def get_system_info():
    uname = platform.uname()
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())

    return {
        "OS": f"{uname.system} {uname.release}",
        "Kernel Version": uname.version,
        "Architecture": uname.machine,
        "Hostname": uname.node,
        "Boot Time": boot_time.strftime("%Y-%m-%d %H:%M:%S")
    }

def get_cpu_info():
    return {
        "Physical cores": psutil.cpu_count(logical=False),
        "Total cores": psutil.cpu_count(logical=True),
        "Max Frequency (MHz)": psutil.cpu_freq().max,
        "Current Frequency (MHz)": psutil.cpu_freq().current,
        "CPU Usage (%)": psutil.cpu_percent(interval=1)
    }

def get_memory_info():
    svmem = psutil.virtual_memory()
    return {
        "Total (MB)": round(svmem.total / (1024 ** 2), 2),
        "Available (MB)": round(svmem.available / (1024 ** 2), 2),
        "Used (MB)": round(svmem.used / (1024 ** 2), 2),
        "Percentage": svmem.percent
    }

def get_disk_info():
    partitions = psutil.disk_partitions()
    disk_data = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disk_data.append({
                "Device": p.device,
                "Mountpoint": p.mountpoint,
                "File System": p.fstype,
                "Total (GB)": round(usage.total / (1024 ** 3), 2),
                "Used (GB)": round(usage.used / (1024 ** 3), 2),
                "Free (GB)": round(usage.free / (1024 ** 3), 2),
                "Percentage": usage.percent
            })
        except PermissionError:
            continue
    return disk_data

def get_network_info():
    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "N/A"
    interfaces = psutil.net_if_addrs()
    return {
        "Hostname": hostname,
        "IP Address": ip_address,
        "Interfaces": {iface: [addr.address for addr in addrs if addr.family == socket.AF_INET] 
                       for iface, addrs in interfaces.items()}
    }

def get_process_info(limit=10):
    processes = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent']):
        processes.append(p.info)
    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:limit]

def getFullData():
    return {
        "System": get_system_info(),
        "CPU": get_cpu_info(),
        "Memory": get_memory_info(),
        "Disks": get_disk_info(),
        "Network": get_network_info(),
        "Top Processes": get_process_info()
    }
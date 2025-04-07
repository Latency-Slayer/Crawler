from os import cpu_count

import psutil
import platform
import subprocess
import requests
import json


def init():
    print("Iniciando verificação de Hardware... \n")


    motherboard_id = get_motherboard_id()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count()
    ram = {
        "total": psutil.virtual_memory().total,
        "type": "ram",

    }


    teste = json.loads(ram)

    print(teste)


def get_motherboard_id():
    so = platform.system()

    try:
        windows_sh = ["powershell", "-Command", "Get-WmiObject Win32_BaseBoard "
                                                "| Select-Object -ExpandProperty SerialNumber"]

        linux_sh = "sudo dmidecode -s system-uuid"

        sh = windows_sh if so == "Windows" else linux_sh

        motherboard_uuid = subprocess.check_output(sh, shell=True).decode().strip()

    except subprocess.SubprocessError:
        exit("Error collecting uuid from motherboard")

    return motherboard_uuid




init()
# def server_data():
#     print("")
#
# def get_component_data():
#     print("")
#
# def get_system_data():
#     print("")
#
# def get_cpu_data():
#     print("")
#
# def get_ram_data():
#     print("")
#
# def get_disk_data():
#     print("")
#
#
# def parse_json():
#     print("")
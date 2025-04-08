import psutil
import platform
import subprocess
import requests

class Json:
    def __init__(self):
        self.json = {}

    def append(self, key: str, value):
        self.json[key] = value

    def __str__(self):
        import json
        return json.dumps(self.json, ensure_ascii=False, indent=4)


def init():
    print("\033[1;34m💻 Bem-vindo ao Script de Cadastro Automático de Servidores!\033[0m")
    print("📝 Conclua os passos abaixo para continuar...\n")

    server_json = Json()

    auth = get_auth_data()
    server_json.append("auth", auth)

    print("\n🔍 \033[1;33mIniciando verificação de Hardware...\033[0m\n")

    motherboard_id = get_motherboard_id()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_threads = psutil.cpu_count()
    total_ram = psutil.virtual_memory().total

    tag_name = get_tag_name()
    server_type = get_server_type()
    so = platform.system()
    location = get_server_location()
    city = location["countryCode"]
    country = location["city"]

    server_json.append("motherboard_id", motherboard_id)
    server_json.append("tag_name", tag_name)
    server_json.append("type", server_type["type"])
    server_json.append("instance_id", server_type["instance_id"])
    server_json.append("so", so)
    server_json.append("city", city)
    server_json.append("country_code", country)

    print("\n📦 \033[1;32mResumo da Configuração do Servidor:\033[0m")
    print(server_json)


def get_motherboard_id():
    so = platform.system()

    try:
        windows_sh = ["powershell", "-Command", "Get-WmiObject Win32_BaseBoard "
                                                "| Select-Object -ExpandProperty SerialNumber"]
        linux_sh = "sudo dmidecode -s system-uuid"

        sh = windows_sh if so == "Windows" else linux_sh

        motherboard_uuid = subprocess.check_output(sh, shell=True).decode().strip()

    except subprocess.SubprocessError:
        exit("\033[1;31m❌ Erro ao coletar UUID da placa-mãe.\033[0m")

    print(f"📎 UUID da Placa-mãe: \033[1;36m{motherboard_uuid}\033[0m")
    return motherboard_uuid


def get_auth_data():
    print("🔐 \033[1;35mAutenticação do Usuário\033[0m")
    print("ℹ️  Os dados informados serão enviados ao servidor para validação.")
    print("⚠️  A verificação não é feita em tempo real. Caso haja algum erro nas credenciais, você será notificado ao final do processo.\n")
    email = input("📧 Digite seu e-mail: ")
    password = input("🔑 Digite sua senha: ")

    return {
        "email": email,
        "password": password
    }


def get_tag_name():
    print("\n🏷️ \033[1;35mDefina um Apelido (Tag Name)\033[0m")
    tag_name = input("Digite um apelido para o seu servidor. Esse nome será exibido no sistema.\n"
                     "📛 Digite aqui: ")

    return tag_name


def get_server_type():
    print("\n🧩 \033[1;35mSelecione o Tipo de Servidor\033[0m")
    print("1️⃣  - Cloud")
    print("2️⃣  - On-Premise")

    opt = input("Digite uma opção (Default: On-Premise): ")

    if opt == "1":
        return {
            "type": "cloud",
            "instance_id": get_instance_id()
        }

    return {
        "type": "on-premise",
        "instance_id": None
    }


def get_server_location():
    print("\n🌍 \033[1;35mLocalizando o Servidor com base no IP...\033[0m")
    try:
        ip = requests.get('https://api.ipify.org').text
        location = requests.get(f"http://ip-api.com/json/{ip}")
    except subprocess.SubprocessError:
        exit("\033[1;31m❌ Falha ao obter localização.\033[0m")

    print(f"🌐 IP Detectado: \033[1;36m{ip}\033[0m")
    return location.json()


def get_instance_id():
    instance_id = input("☁️ Digite o ID da instância em nuvem (opcional): ")
    return instance_id


def get_disk_data():
    print("\n💾 \033[1;35mInformações dos Discos:\033[0m")
    disks = psutil.disk_partitions()

    for disk in disks:
        device = disk.device
        if device == "F:\\":
            continue

        usage = psutil.disk_usage(device)
        print(f"📁 Disco {device} - Usado: {usage.percent}%")

init()

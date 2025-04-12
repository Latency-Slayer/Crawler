import psutil
import platform
import subprocess
import requests
import re
import json

class Json:
    def __init__(self):
        self.json = {}

    def append(self, key: str, value):
        self.json[key] = value

    def __str__(self):
        return json.dumps(self.json, ensure_ascii=False, indent=4)


def init():
    print("\033[1;34m💻 Bem-vindo ao Script de Cadastro Automático de Servidores!\033[0m")
    print("📝 Conclua os passos abaixo para continuar...\n")

    server_json = Json()

    auth = get_auth_data()
    server_json.append("auth", auth)

    print("\n🔍 \033[1;33mIniciando verificação de Hardware...\033[0m\n")

    motherboard_id = get_motherboard_id()

    tag_name = get_tag_name()
    server_type = get_server_type()
    so = platform.system()
    location = get_server_location()
    city = location["city"]
    country = location["countryCode"]
    components = get_components()

    server_json.append("motherboard_id", motherboard_id)
    server_json.append("tag_name", tag_name)
    server_json.append("type", server_type["type"])
    server_json.append("instance_id", server_type["instance_id"])
    server_json.append("so", so.lower())
    server_json.append("city", city)
    server_json.append("country_code", country)

    server_json.append("components", components)

    try:
        request = requests.post("http://localhost:3333/server/register", json=server_json.json)

        if request.status_code != 201:
            raise ValueError(request.json())

        print("\n📦 \033[1;32mServidor cadastrado com sucesso!:\033[0m")
    except Exception as e:
        print(f"\033[91m[✘ ERRO] Falha ao enviar dados para o servidor: {e}\033[0m")


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

    while True:
        email = input("📧 Digite seu e-mail: ")
        password = input("🔑 Digite sua senha: ")

        if email != "" or password != "":
            break

        print("O e-mail e a senha não podem ser vázios.")

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
    except Exception:
        print("\033[1;31m❌ Falha ao obter localização com baseado no IP do servidor.\033[0m")

        country = input("Digite o código do país onde o servidor está localizado ('BR', 'US', 'UK'...): ")
        city = input("Digite o nome da cidade onde o servidor está localizado ('São Paulo', 'Sidney', 'Lisboa')...")

        location = {}

        location["countryCode"] = country.upper()
        location["city"] = city

        return location

    print(f"🌐 IP Detectado: \033[1;36m{ip}\033[0m")
    print("🌍 Localização")
    print("──────────────")
    print(f"📍 Cidade : {location.json()["city"]}")
    print(f"🏳️ País   : {location.json()["countryCode"]}")
    
    return location.json()


def get_instance_id():
    instance_id = input("☁️ Digite o ID da instância em nuvem (opcional): ")
    return instance_id or None



def get_components ():
    components_json = []

    print("\n \033[1;34mIniciando configuração de componentes, em caso de dúvidas consulte nosso manual...\033[0m")

    components_json.append(get_cpu_data())
    components_json.append(get_ram_data())

    disks = get_disk_data()

    for disk in disks:
        components_json.append(disk)

    return components_json


def get_cpu_data():
    try:
        print("\n💾 \033[1;35m🔍 Coletando Informações do processador...\033[0m\n")

        windows_sh = ["powershell", "-Command", "(Get-ComputerInfo).CsProcessors[0].name"]
        linux_sh = "cat /proc/cpuinfo | grep 'model name' | uniq | cut -d ':' -f2-"

        sh = windows_sh if platform.system() == "Windows" else linux_sh

        cpu_name = subprocess.check_output(sh, shell=True).decode().strip()

        print(f"\033[1;36m🧠 Processador Detectado:\033[0m {cpu_name}")

        while True:
            try:
                max_limit_use = get_number_in_str(input("   📊 Limite MÁXIMO de uso (%): "))
                min_limit_use = get_number_in_str(input("   📉 Limite MÍNIMO de uso (%): "))
                print("\n")

                if max_limit_use != 0 and max_limit_use <= 100 and min_limit_use <= 100:
                    break

                print("❌ Entrada inválida! Tente novamente. O limite máximo não pode ser zero ou nulo e deve estar entre 1% e 100%. \n ")
            except:
                print("❌ Entrada inválida! Tente novamente.\n")


        while True:
            try:
                max_limit_temperature = get_number_in_str(input("   📊 Limite MÁXIMO de uso (C°): "))
                min_limit_temperature = get_number_in_str(input("   📉 Limite MÍNIMO de uso (C°): "))

                if max_limit_temperature > 0:
                    break

                print("❌ Entrada inválida! Tente novamente. O limite máximo não pode ser zero ou nulo e deve estar entre 1% e 100%. \n ")
            except:
                print("❌ Entrada inválida! Tente novamente.\n")


        print(f"\n\033[1;32m✅ Limites configurados com sucesso para {cpu_name}!\033[0m\n")


        return {
            "tag_name": cpu_name,
            "type": "cpu",
            "metrics": [
                {
                    "metric": "%",
                    "max_limit": max_limit_use,
                    "min_limit": min_limit_use or None,
                    "total": 100
                },
                {
                    "metric": "celsius",
                    "max_limit":  max_limit_temperature,
                    "min_limit": min_limit_temperature or None,
                    "total": 0
                }
            ]
        }
    except Exception as e:
        print(f"\n\033[1;31m❗ Erro ao coletar dados do processador:\033[0m {e}")


def get_ram_data():
    try:
        memory_type = subprocess.check_output(["powershell", "-command", """
            switch ((Get-CimInstance -ClassName Win32_PhysicalMemory | Select-Object -First 1).SMBIOSMemoryType) {
                20 { "DDR" }
                21 { "DDR2" }
                22 { "DDR2 FB-DIMM" }
                24 { "DDR3" }
                26 { "DDR4" }
                27 { "DDR5" }
                Default { "Tipo desconhecido" }
            }"""]).decode().strip() or "RAM"
    except:
        print("Erro ao coletar tipo de memória...")


    try:
        print("\n💾 \033[1;35m🔍 Coletando Informações da memória...\033[0m\n")
        ram = psutil.virtual_memory()

        total_gb = ram.total / 1024 ** 3


        print(f"\033[1;36m Memória Detectada:\033[0m {memory_type}")
        print(f"Memória RAM: {total_gb:.2f} GB")

        print(f"\033[1;34m⚙️  Configurando limites para o disco memória RAM:\033[0m")

        while True:
            try:
                max_limit = get_number_in_str(input("   📊 Limite MÁXIMO de uso (%): "))
                min_limit = get_number_in_str(input("   📉 Limite MÍNIMO de uso (%): "))

                if max_limit != 0 and max_limit <= 100 and min_limit <= 100:
                    break

                print("❌ Entrada inválida! Tente novamente. O limite máximo não pode ser zero ou nulo e deve estar entre 1% e 100%. \n ")
            except:
                print("❌ Entrada inválida! Tente novamente.\n")



        memory_json = {
            "tag_name": memory_type,
            "type": "ram",
            "metrics": [
                {
                    "metric": "%",
                    "max_limit": max_limit,
                    "min_limit": min_limit or None,
                    "total": 100
                },
                {
                    "metric": "gb",
                    "max_limit": round(total_gb * (max_limit / 100), 2),
                    "min_limit": round(total_gb * (min_limit / 100), 2) if min_limit else None,
                    "total": round(total_gb, 2)
                }
            ]
        }

        print(f"\n\033[1;32m✅ Limites configurados com sucesso para memória RAM!\033[0m\n")

        return memory_json

    except Exception as e:
        print(f"\n\033[1;31m❗ Erro ao coletar dados dos discos:\033[0m {e}")


def get_disk_data():
    try:
        print("\n💾 \033[1;35m🔍 Coletando Informações dos Discos...\033[0m\n")
        disks = psutil.disk_partitions()

        disks_json = []

        for disk in disks:
            device = disk.device
            print(f"\033[1;36m📁 Partição Detectada:\033[0m {device}")

            try:
                usage = psutil.disk_usage(device)
            except:
                print(f"\033[91m[✘] Erro ao coletar informações da partição: {device}\033[0m")
                continue

            print(f"\033[1;34m⚙️  Configurando limites para o disco {device}:\033[0m")

            while True:
                try:
                    max_limit = get_number_in_str(input("   📊 Limite MÁXIMO de uso (%): "))
                    min_limit = get_number_in_str(input("   📉 Limite MÍNIMO de uso (%): "))

                    if max_limit != 0 and max_limit <= 100 and min_limit <= 100:
                        break

                    print("❌ Entrada inválida! Tente novamente. O limite máximo não pode ser zero ou nulo e deve estar entre 1% e 100%. \n ")
                except:
                    print("❌ Entrada inválida! Tente novamente.\n")

            total_gb = usage.total / 1024 ** 3

            disks_json.append({
                "tag_name": device,
                "type": "storage",
                "metrics": [
                    {
                        "metric": "%",
                        "max_limit": max_limit,
                        "min_limit": min_limit or None,
                        "total": 100
                    },
                    {
                        "metric": "gb",
                        "max_limit": round(total_gb * (max_limit / 100), 0) if max_limit else None,
                        "min_limit": round(total_gb * (min_limit / 100), 0) if min_limit else None,
                        "total": round(total_gb, 0)
                    }
                ]
            })

            print(f"\n\033[1;32m✅ Limites configurados com sucesso para {device}!\033[0m\n")

        return disks_json

    except Exception as e:
        print(f"\n\033[1;31m❗ Erro ao coletar dados dos discos:\033[0m {e}")



def get_number_in_str(str: str):
    if str == "":
        return 0

    str = re.sub(r'[^0-9]', '', str)

    return round(float(str), 2)


init()
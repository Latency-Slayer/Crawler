import mysql.connector  
import time  
import psutil
from mysql.connector import Error, MySQLConnection

def obter_dados():
    cpuPercent = psutil.cpu_percent(interval=1)  # Porcentagem em uso do CPU
    cpuFreq = psutil.cpu_freq().max
    cpuByte = psutil.cpu_freq().current

    diskUsage = psutil.disk_usage('/')
    diskUsageTotal = round(diskUsage.total / (1024**3), 2)  # Total do disco em GB
    diskPercent = psutil.disk_usage('/').percent # Trocar para discol local C: caso o SO seja windows
    diskByte = psutil.disk_usage('/').used


    memory = psutil.virtual_memory()

    memoryTotal = round(memory.total / (1024**3), 2)  # Total de memória RAM
    memoryPercent = psutil.virtual_memory().percent
    memoryByte = psutil.virtual_memory().used

    internet = psutil.net_io_counters()
    redeRecebida = round(internet.bytes_recv/(1024 ** 2), 2)
    redeEnviada = round(internet.bytes_sent/(1024 ** 2), 2)
    return cpuPercent, memoryPercent, diskPercent
try:
    mydb = MySQLConnection(
        host="54.92.165.184",
        user="insert_user",
        password="123",
        database="python"
    )
    mycursor = mydb.cursor()
except Error as erro:
    print(f"Erro ao conectar com o usuário INSERT: {erro}")
    exit()

try:
    mydb2 = MySQLConnection(
        host="54.92.165.184",
        user="select_user",
        password="123",
        database="python"
    )
    mycursor2 = mydb2.cursor()
except Error as erro:
    print(f"Erro ao conectar com o usuário SELECT: {erro}")
    exit()

print(mydb)

usuario = input('Informe o seu email: ')
senha = input('Informe a sua senha: ')


autenticar = "SELECT nome, email, cargo, senha, fkEmpresa from usuarios where email = %s AND senha = %s"
mycursor2.execute(autenticar, (usuario, senha))
resultado = mycursor2.fetchone()

if resultado is None:
    print("Parâmetros incorretos de email ou senha")
else:
    cod_maq = input("Digite o código da sua máquina (caso ja tenha um codigo): ")

    sql3 = "SELECT codigoMaquina FROM maquina_servidor WHERE codigoMaquina = %s"
    mycursor2.execute(sql3, (cod_maq,))
    resultado = mycursor2.fetchone()


    if resultado is None:
        print("A sua máquina ainda nescessita de um registro")


    else:
        tempo = int(input('Informe o tempo em segundos que você deseja coletar seus dados (Somente números por favor): '))
        while True:
            dados = obter_dados()
            
            ramPorcentagem = dados[1]
            cpuPorcentagem = dados[0]
            diskPorcentagem = dados[2]
            
            print(f"""Valores monitorados no momento:
                    [RAM] {ramPorcentagem}%
                    [CPU] {cpuPorcentagem}%
                    [DISCO] {diskPorcentagem}%""")
            
            if ramPorcentagem > 80.00:
                gravidade = 'RAM GRAVE!'
                sql1 = "INSERT alerta (tipo, fkMaquina) VALUES (%s, %s);"
                mycursor.execute(sql1, (gravidade, cod_maq))
                mydb.commit()
            elif cpuPorcentagem > 80.00:
                gravidade = 'CPU GRAVE!'
                sql1 = "INSERT alerta (tipo, fkMaquina) VALUES (%s, %s);"
                mycursor.execute(sql1, (gravidade, cod_maq))
                mydb.commit()
            elif diskPorcentagem > 80.00:
                gravidade = 'DISCO GRAVE!'
                sql1 = "INSERT alerta (tipo, fkMaquina) VALUES (%s, %s);"
                mycursor.execute(sql1, (gravidade, cod_maq))
                mydb.commit()
            time.sleep(tempo)

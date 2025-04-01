import GPUtil
import psutil
import mysql.connector 
import time
import subprocess
import platform

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gui#2020",
    database="captura"
)

if mydb.is_connected() == True:
    print('Conectado ao Banco de Dados')

cursor = mydb.cursor();

def get_mother_board_id():
    try:
        so = platform.system()

        windows_sh = ["powershell", "-Command", "Get-WmiObject Win32_BaseBoard "
                                                "| Select-Object -ExpandProperty SerialNumber"]

        linux_sh = "sudo dmidecode -s system-uuid"

        sh = windows_sh if so == "Windows" else linux_sh

        return subprocess.check_output(sh, shell=True).decode().strip()

    except subprocess.SubprocessError as e:
       exit("Erro ao capturar id da placa mãe... Entre em contato como suporte da InfraWatch")

fkServer = get_mother_board_id()
print(fkServer)

getGpus = GPUtil.getGPUs()


contador = 0

while True:
    cpuPercent = psutil.cpu_percent(interval=1)
    cpuFreq = psutil.cpu_freq().current
    
    memoriaUsadoBytes = int(psutil.virtual_memory().used) # Convertendo Bytes para MegaBytes
    memoriaUsadoPercent = int(psutil.virtual_memory().percent)

    discoUsadoBytes = int(psutil.disk_usage('C:\\').used) # Convertendo Bytes para MegaBytes
    discoUsadoPercent = int(psutil.disk_usage('C:\\').percent) # Convertendo Bytes para MegaBytes

    redeRecebida = round(psutil.net_io_counters().bytes_recv/(1024 ** 2), 2)
    redeEnviada = round(psutil.net_io_counters().bytes_sent/(1024 ** 2), 2)

    sql = "INSERT INTO captura_dados (cpuPercent, cpuFreq, ramPercent, ramBytes, discoPercent, discoBytes, downloadMbps, uploadMbps) VALUES (%s, %s, %s,%s,%s, %s, %s,%s)"
    valores = (cpuPercent,cpuFreq,memoriaUsadoPercent,memoriaUsadoBytes, discoUsadoPercent,discoUsadoBytes,redeRecebida,redeEnviada)


    # if len(getGpus) > 0:
    #     gpu = GPUtil.getGPUs()[0]
    #     gpuUuid = gpu.uuid
    #     gpuMemoryUsed = gpu.memoryUsed
    #     gpuLoad = gpu.load * 100 # Converte o load para porcentagem (inteiro de 0 até 100)
    #     gpuTemperature = gpu.temperature

    #     sql_gpu = "INSERT INTO GPULog (gpuLoad, usedMemory, temperature, fkGPU) VALUES (%s,%s,%s,%s)"
    #     valores_gpu = (gpuLoad, gpuMemoryUsed, gpuTemperature, gpuUuid)

    #     cursor.execute(sql_gpu, valores_gpu)

    cursor.execute(sql, valores)

    mydb.commit()

    contador += 1

    print(f"{contador} - Registros armazenados no banco de dados com sucesso...")    
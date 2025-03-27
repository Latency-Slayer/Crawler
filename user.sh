#!/bin/bash \n
echo "Criação de usuário"

# Nome do usuário/senha/diretório que será movido
read -p "Digite o nome do usuario: " USERNAME

# Verificar se o usuário já existe
if id "$USERNAME" &>/dev/null; then
    echo "O usuário $USERNAME não existe. Prosseguindo com a criação..."
else
    echo "Erro: O usuário $USERNAME já existe."
    exit 1
fi

# Criar o usuário com diretório home e shell Bash 
sudo useradd -m -s /bin/bash -c "Latency Slayer User" "$USERNAME"

# Senha do usuário
read -p "Digite a senha: " PASSWORD

# Definir a senha do usuário \n
echo "$USERNAME:$PASSWORD" | sudo chpasswd; 

# Verifica se a senha foi criada com sucesso
if [ $? -eq 0 ]; then
    echo "Senha para $USERNAME criada com sucesso."
    echo "Usuário $USERNAME criado com sucesso!"  
else
    echo "Erro ao mover o diretório."
    exit 1
fi

read -p "Digite nome do diretório que deseja mover: " DIRETORIO

# Mudar permissões do arquivo criado 
echo "Dando permissões do arquivo para o usuário"
sudo chown -R $USERNAME:$USERNAME /home/ubuntu/$DIRETORIO

# Mover o diretório para a /home do usuário criado
echo "Movendo diretório para /home de $USERNAME"
sudo mv /home/ubuntu/$DIRETORIO /home/$USERNAME/

# Verificar se o diretório foi criado com sucesso
if [ $? -eq 0 ]; then
    echo "Diretório movido para /home/$USERNAME com sucesso."
else
    echo "Erro ao mover o diretório."
    exit 1
fi

echo "Usuário criado e diretório movido para /home de $USERNAME com as devidas permissões"






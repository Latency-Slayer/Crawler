#!/bin/bash

read -p "Digite o nome do usuario do banco: " USER_BANCO
read -p "Digite a senha do usuario do banco: " SENHA_BANCO
read -p "Digite o nome do banco: " BANCO_DE_DADOS

SCRIPT_SQL="CREATE DATABASE $BANCO_DE_DADOS;
USE $BANCO_DE_DADOS;

CREATE TABLE endereco (
    idEndereco INT PRIMARY KEY AUTO_INCREMENT,
    cep CHAR(11),
    numero INT,
    rua VARCHAR(100)
);

CREATE TABLE empresa (
    idEmpresa INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45),
    codigo CHAR(9),
    empresaMatriz INT,
    fkEndereco INT,
    FOREIGN KEY (empresaMatriz) REFERENCES empresa(idEmpresa),
    FOREIGN KEY (fkEndereco) REFERENCES endereco(idEndereco)
);

CREATE TABLE centro_servidores (
    idServidores INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(45),
    fkEmpresa INT,
    fkEndereco INT,
    FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa),
    FOREIGN KEY (fkEndereco) REFERENCES endereco(idEndereco)
);

CREATE TABLE usuarios (
    idUsuarios INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(45),
    senha VARCHAR(45),
    cpf CHAR(11) unique,
    cargo VARCHAR(45),
    nome VARCHAR(45),
    dataRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fkEmpresa INT,
    FOREIGN KEY (fkEmpresa) REFERENCES empresa(idEmpresa)
);

CREATE TABLE maquina_servidor (
    codigoMaquina INT PRIMARY KEY AUTO_INCREMENT,
    fkCentroServidor INT,
    modeloRam VARCHAR(45),
    modeloCpu VARCHAR(45),
    modeloDisk VARCHAR(45),
    dataRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fkCentroServidor) REFERENCES centro_servidores(idServidores)
);

CREATE TABLE componentes (
    idComponentes INT PRIMARY KEY AUTO_INCREMENT,
    componente VARCHAR(45),
    medida VARCHAR(45)
);

CREATE TABLE maquina_componentes (
    idLeitura INT PRIMARY KEY AUTO_INCREMENT,
    fkMaquina INT,
    fkComponentes INT,
    metricaAlerta INT,
    FOREIGN KEY (fkMaquina) REFERENCES maquina_servidor(codigoMaquina),
    FOREIGN KEY (fkComponentes) REFERENCES componentes(idComponentes)
);

CREATE TABLE alerta (
    idAlerta INT PRIMARY KEY AUTO_INCREMENT,
    dataAlerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipo varchar(45),
    fkMaquinaComponente INT,
    fkMaquina INT,
    fkComponente INT,
    FOREIGN KEY (fkMaquinaComponente) REFERENCES maquina_componentes(idLeitura),
    FOREIGN KEY (fkMaquina) REFERENCES maquina_servidor(codigoMaquina),
    FOREIGN KEY (fkComponente) REFERENCES componentes(idComponentes)
);

CREATE USER '$USER_BANCO'@'%' IDENTIFIED BY '$SENHA_BANCO';
GRANT ALL PRIVILEGES ON $BANCO_DE_DADOS.* TO '$USER_BANCO'@'%';
FLUSH PRIVILEGES;

CREATE user 'insert_user'@'%' identified by '123';
GRANT insert on python.* to 'insert_user'@'%';
FLUSH privileges;

CREATE user 'select_user'@'%' identified by '123';
GRANT select on python.* to 'select_user'@'%';
FLUSH privileges;
"

# Rodar o script SQL no MySQL
sudo mysql -u "root" -e "$SCRIPT_SQL"

# Verificar se o comando foi executado com sucesso
if [ $? -eq 0 ]; then
    echo "Script executado com sucesso!"
else
    echo "Erro ao executar o script."
fi

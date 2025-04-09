create database captura;
use captura;
drop table captura_dados;

CREATE TABLE captura_dados(
	id int primary key auto_increment,
    cpuPercent DOUBLE,
    cpuFreq DOUBLE,
    ramPercent DOUBLE,
    ramBytes DOUBLE,
    discoPercent DOUBLE,
    discoBytes DOUBLE,
    downloadMbps DOUBLE,
    uploadMbps DOUBLE,
    dataHora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

truncate table captura_dados;
select * from captura_dados;
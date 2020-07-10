# BDPN synchroniser
The purpose of the project is to increase the speed of mobile number lookups by maintaining a local number-lookup service in an actual condition.
This is a real-world working project, successfully performing its task since 09/2017 under a high load of one of the Russian mobile content providers based in Moscow.

**Disclaimer: The [zniis] account is needed for this software to work, as this is the official [MNP] data provider in Russia**


### Tech
* [Python] 2.6.6 to work.
* [Paramiko] - A Python implementation of SSHv2
* [MySQL] - Open source database

### Installation
mysql-connector-python and paramiko are used in the project:
```sh
$ sudo yum install mysql-connector-python python-paramiko
```
Than, place contents to the desired folder and run:
```sh
$ ./bdpnsync.py initdb    # This will create a new db and a user for it.
```
Settings.cfg will be created in the same folder and should be updated with zniis account data.

### Usage
Daemon:
```sh
$ ./bdpnsync.py start|stop|restart
```
MySQL:
```mysql
SELECT f_get_mnc(79123456789);  # Get Mobile Networc Code(MNC) of the suplied mobile number
```
```mysql
-- Get all available information about the supplied mobile number --
SET @num=79123456789;
CALL p_get_info(@num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date);
SELECT @num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date;
```

#### Tested on:
* Centos 6/python 2.6.6/MySQL 5.1
* Ubuntu 12.04/python 2.7.3/MySQL 5.5

***


# Демон синхронизации базы данных перенесённых номеров (БДПН)
### !!! ВНИМАНИЕ. Для работы требуется sftp аккаунт [института связи](https://www.zniis.ru/bdpn/operators/request) !!!
Демон синхронизации БДПН с MySQL. Поддерживает в актуальном состоянии локальную базу данных проводя её обновления каждый чётный час.
В текущем варианте, база данных показывает принадлежность номера мобильного телефона по версии БДПН.
История миграций не импортируется, но может быть легко добавлена в конфигурацию.
Помимо основных таблиц БДПН, формируются 3 вспомогательных:
* t_info - Служебная. Содержит данные о последней синхронизации таблиц.
* t_mnc - Попытка привести отечественный "зоопарк" MNC к стандарту [MNC](https://en.wikipedia.org/wiki/Mobile_country_code) т.е. к одному коду для всей сети. Это нужно для удобства ответа на вопрос: "Кому из большой 4ки принадлежит номер?". Таблица пополняется новичками, но к сожелению требует ручного распределения по "брэндам".
* t_regions - Содержит список регионов по версии Россвязи. Актуален на момент заливки.

#### Суть всей этой задачи заключается в возможности использовать как минимум одну функцию и одну процедуру:
```mysql
SELECT f_get_mnc(79123456789);  # Актуальный MNC номера из БДПН
```
```mysql
-- Получить всё, что может выдать БДПН по номеру --
SET @num=79123456789;
CALL p_get_info(@num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date);
SELECT @num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date;
```


Протестировано на:
* Centos 6/python 2.6.6/MySQL 5.1
* Ubuntu 12.04/python 2.7.3/MySQL 5.5

   [Paramiko]: <http://www.paramiko.org/index.html>
   [MySQL]: <https://www.mysql.com/>
   [Python]: <https://www.python.org/>
   [zniis]: <https://www.zniis.ru/bdpn/operators/request>
   [MNP]: <https://en.wikipedia.org/wiki/Mobile_number_portability>

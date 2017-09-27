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
SET @num=89123456789;
CALL p_get_info(@num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date);
SELECT @num, @mnc, @brand, @org_code, @org_name, @region_id, @region_name, @region_z, @port_date;
```


Протестировано на:
* Centos 6/python 2.6.6/MySQL 5.1
* Ubuntu 12.04/python 2.7.3/MySQL 5.5
***
# numlex
### !!! WARNING. You should have username and password to access [zniis](https://www.zniis.ru/bdpn/operators/request) sftp server !!!


This daemon works on background and updates data each even hour.
It needs at least python 2.6.6 to work.
Probably you will need to install a couple of additional modules for python:
mysql-connector-python
```sh
$ sudo yum install mysql-connector-python
```
and paramiko
```sh
$ sudo yum install python-paramiko
```
or
```sh
$ pip install paramiko
```
Workability tested on 
* Centos 6/python 2.6.6/MySQL 5.1
* Ubuntu 12.04/python 2.7.3/MySQL 5.5.
***
# Usage:
Firstly, place contents to the desired folder and run:
```sh
$ ./bdpnsync.py initdb    # will create a new db and a user for it
```
Settings.cfg will be created in the same folder.
Secondly, you need to update settings with your zniis account data, than run:
```sh
$ ./bdpnsync.py start   # Start daemon
$ ./bdpnsync.py stop    # Stop daemon
$ ./bdpnsync.py restart   # Restart daemon
```

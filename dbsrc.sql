-- !!! DO NOT CHANGE THIS FILE !!!
-- Make your own copy if you need to change it

CREATE DATABASE IF NOT EXISTS `BDPN` DEFAULT CHARACTER SET utf8;
USE `BDPN`;
--
-- Table structure for table `t_info`
--

DROP TABLE IF EXISTS `t_info`;
CREATE TABLE `t_info` (
  `obj_name` varchar(20) NOT NULL,
  `last_update` bigint(20) unsigned NOT NULL,
  `enable_update` bit(1) NOT NULL DEFAULT b'1',
  `last_file` varchar(50) NOT NULL,
  `last_error_file` varchar(50) NOT NULL,
  PRIMARY KEY (`obj_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_info`
--

LOCK TABLES `t_info` WRITE;
INSERT INTO `t_info` VALUES ('NumberingPlan',0,'','',''),('Operators',0,'','',''),('PortAll',0,'','',''),('PortIncrement',0,'','',''),('ReturnIncrement',0,'','','');
UNLOCK TABLES;

--
-- Table structure for table `t_mnc`
--

DROP TABLE IF EXISTS `t_mnc`;
CREATE TABLE `t_mnc` (
  `MNC` tinyint(3) unsigned NOT NULL,
  `MNC_brand` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'Main brand MNC for ones who own multiple MNC.',
  `name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`MNC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `t_numbering_plan`
--

DROP TABLE IF EXISTS `t_numbering_plan`;
CREATE TABLE `t_numbering_plan` (
  `NumberFrom` bigint(20) unsigned NOT NULL,
  `NumberTo` bigint(20) unsigned NOT NULL,
  `OwnerId` varchar(50) NOT NULL,
  `RegionCode` tinyint(3) unsigned NOT NULL,
  `MNC` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`NumberFrom`,`NumberTo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `t_operators`
--

DROP TABLE IF EXISTS `t_operators`;
CREATE TABLE `t_operators` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `OrgCode` varchar(50) NOT NULL,
  `MNC` tinyint(3) unsigned NOT NULL,
  `dt` datetime NOT NULL COMMENT 'Last activity date.',
  `TIN` varchar(100) DEFAULT NULL,
  `OrgName` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `IX_t_operators` (`OrgCode`,`MNC`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `t_port_all`
--

DROP TABLE IF EXISTS `t_port_all`;
CREATE TABLE `t_port_all` (
  `Number` bigint(20) unsigned NOT NULL,
  `OwnerId` varchar(50) NOT NULL,
  `MNC` tinyint(3) unsigned NOT NULL,
  `Route` varchar(5) NOT NULL,
  `RegionCode` tinyint(3) unsigned NOT NULL,
  `PortDateFET` datetime NOT NULL,
  PRIMARY KEY (`Number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `t_regions`
--

DROP TABLE IF EXISTS `t_regions`;
CREATE TABLE `t_regions` (
  `RegionCode` smallint(6) unsigned NOT NULL,
  `Name` varchar(56) NOT NULL,
  `FETimeModifier` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`RegionCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `t_regions`
--

LOCK TABLES `t_regions` WRITE;
ALTER TABLE `t_regions` DISABLE KEYS;
INSERT INTO `t_regions` VALUES (1,'Республика Адыгея (Адыгея)',0),(2,'Республика Алтай',4),(3,'Республика Башкортостан',2),(4,'Республика Бурятия',5),(5,'Республика Дагестан',0),(6,'Республика Ингушетия',0),(7,'Кабардино-Балкарская Республика',0),(8,'Республика Калмыкия',0),(9,'Карачаево-Черкесская Республика',0),(10,'Республика Карелия',0),(11,'Республика Коми',0),(12,'Республика Марий Эл',0),(13,'Республика Мордовия',0),(14,'Республика Саха (Якутия)',6),(15,'Республика Северная Осетия - Алания',0),(16,'Республика Татарстан (Татарстан)',0),(17,'Республика Тыва',4),(18,'Удмуртская Республика',1),(19,'Республика Хакасия',4),(20,'Чеченская Республика',0),(21,'Чувашская Республика - Чувашия',0),(22,'Алтайский край',3),(23,'Забайкальский край',6),(24,'Камчатский край',9),(25,'Краснодарский край',0),(26,'Красноярский край',4),(27,'Пермский край',2),(28,'Приморский край',7),(29,'Ставропольский край',0),(30,'Хабаровский край',7),(31,'Амурская область',6),(32,'Архангельская область, Ненецкий автономный округ',0),(33,'Астраханская область',1),(34,'Белгородская область',0),(35,'Брянская область',0),(36,'Владимирская область',0),(37,'Волгоградская область',0),(38,'Вологодская область',0),(39,'Воронежская область',0),(40,'Ивановская область',0),(41,'Иркутская область',5),(42,'Калининградская область',-1),(43,'Калужская область',0),(44,'Кемеровская область',4),(45,'Кировская область',0),(46,'Костромская область',0),(47,'Курганская область',2),(48,'Курская область',0),(50,'Липецкая область',0),(51,'Магаданская область',8),(53,'Мурманская область',0),(54,'Нижегородская область',0),(55,'Новгородская область',0),(56,'Новосибирская область',4),(57,'Омская область',3),(58,'Оренбургская область',2),(59,'Орловская область',0),(60,'Пензенская область',0),(61,'Псковская область',0),(62,'Ростовская область',0),(63,'Рязанская область',0),(64,'Самарская область',1),(65,'Саратовская область',1),(66,'Сахалинская область',7),(67,'Свердловская область',2),(68,'Смоленская область',0),(69,'Тамбовская область',0),(70,'Тверская область',0),(71,'Томская область',4),(72,'Тульская область',0),(73,'Тюменская область',2),(74,'Ульяновская область',1),(75,'Челябинская область',2),(76,'Ярославская область',0),(77,'г. Москва, Московская область  ',0),(78,'г. Санкт-Петербург, Ленинградская область',0),(79,'Еврейская автономная область',7),(81,'Ханты-Мансийский автономный округ - Югра',2),(82,'Чукотский автономный округ',9),(83,'Ямало-Ненецкий автономный округ',2),(84,'Республика Крым и г. Севастополь',0);
ALTER TABLE `t_regions` ENABLE KEYS;
UNLOCK TABLES;

--
-- Dumping routines for database 'BDPN'
--
DROP FUNCTION IF EXISTS `f_get_mnc`;
CREATE DEFINER=CURRENT_USER FUNCTION `f_get_mnc`(msisdn BIGINT UNSIGNED) RETURNS TINYINT UNSIGNED
BEGIN
/*** Получение MNC кода абонента ***/
	DECLARE res TINYINT UNSIGNED DEFAULT 0;

	IF (msisdn REGEXP '^(7|8)?9[0-9]{9}$') THEN
		SET msisdn = RIGHT(msisdn,10);
		SET res = (IFNULL((SELECT `MNC` FROM `t_port_all` WHERE `Number` = msisdn), 
							IFNULL((SELECT `MNC` FROM `t_numbering_plan` WHERE msisdn BETWEEN `NumberFrom` AND `NumberTo`),
						  0)
					)
				);
	END IF;
RETURN res;
END;

DROP FUNCTION IF EXISTS `f_get_brand_mnc`;
CREATE DEFINER=CURRENT_USER FUNCTION `f_get_brand_mnc` (msisdn BIGINT UNSIGNED) RETURNS TINYINT UNSIGNED
BEGIN
/*** Получение MNC "Брэнда" абонента, если он не равен 0, иначе возвращается MNC ***/
RETURN (SELECT IF(`MNC_brand` != 0, `MNC_brand`, `MNC`) FROM `t_mnc` WHERE `MNC` = f_get_mnc(msisdn));
END;

DROP FUNCTION IF EXISTS `f_get_owner_id`;
CREATE DEFINER=CURRENT_USER FUNCTION `f_get_owner_id`(msisdn BIGINT UNSIGNED) RETURNS varchar(50) CHARSET utf8
BEGIN
/*** Получение OwnerId кода абонента ***/
	DECLARE res VARCHAR(50) DEFAULT 'Wrong number!';

	IF (msisdn REGEXP '^(7|8)?9[0-9]{9}$') THEN
		SET msisdn = RIGHT(msisdn,10);
		SET res = (IFNULL((SELECT `OwnerId` FROM `t_port_all` WHERE `Number` = msisdn), 
							IFNULL((SELECT `OwnerId` FROM `t_numbering_plan` WHERE msisdn BETWEEN `NumberFrom` AND `NumberTo`),
									'UNKNOWN')
							)
					);
	END IF;
RETURN res;
END;

DROP PROCEDURE IF EXISTS `p_import_operators`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_import_operators`(
IN filename VARCHAR(50),
IN file_time BIGINT)
BEGIN
/*** Производит основную работу по проверке и импорту данных из временной таблицы в рабочую ***/
	DECLARE xrows, xtotal, xerrors INT DEFAULT 0;
	SELECT `RowCount` INTO xrows FROM `tmp_operators` WHERE `RowCount` IS NOT NULL LIMIT 1;
	SELECT count(*) INTO xtotal FROM `tmp_operators`;
	SELECT count(*) INTO xerrors FROM `tmp_operators` WHERE `Errors` !='';
	IF xrows>0 THEN
		IF (xtotal-xerrors)>0 THEN
			UPDATE `t_operators` AS a SET `dt` = NOW()
			WHERE exists
				(SELECT `OrgCode`, `MNC`, `TIN`, `OrgName`
				FROM `tmp_operators` AS b
				WHERE
					b.`Errors` ='' AND
					a.`OrgCode` = b.`OrgCode` AND
					a.`mnc` = b.`mnc` AND
					a.`OrgName` = b.`OrgName`
				);
			INSERT INTO t_operators(`OrgCode`,`MNC`,`dt`,`TIN`,`OrgName`)
				SELECT
					a.`OrgCode`,
					a.`MNC`,
					NOW(),
					a.`TIN`,
					a.`OrgName`
				FROM `tmp_operators` AS a
				WHERE
					a.`Errors` ='' AND
					NOT exists
						(SELECT `OrgCode`, `MNC`, `TIN`, `OrgName`
						FROM `t_operators` AS b
						WHERE
							a.`OrgCode` = b.`OrgCode` AND
							a.`mnc` = b.`mnc` AND
							a.`OrgName` = b.`OrgName`
						)
				ORDER BY a.`OrgCode`, a.`MNC`
			ON DUPLICATE KEY UPDATE `dt`=NOW(), `tin` = a.`tin`, `OrgName` = a.`OrgName`;
			INSERT INTO `t_mnc`(`MNC`,`name`)
				SELECT
					`MNC`,
					SUBSTRING_INDEX(SUBSTRING_INDEX(`OrgName`, '"', 2), '"', -1) AS `name`
				FROM `tmp_operators` AS a
				WHERE
					a.`Errors` ='' AND
					a.`MNC` NOT IN (select b.`MNC` FROM `t_mnc` AS b)
				GROUP BY `MNC`;
		END IF;
		IF xerrors>0 THEN
			SELECT CONCAT('line:',`id`+1,'. Errors in:',`Errors`) AS `ERR`
			FROM `tmp_operators`
			WHERE `Errors` !=''
			LIMIT 15;
		ELSEIF (xrows-xtotal)>0 THEN
			SELECT CONCAT('There are ',xrows-xtotal,' records can not be imported from ',filename);
		END IF;
	END IF;
	UPDATE `t_info` SET
		`last_error_file` = IF(xerrors+(xrows-xtotal) != 0 ,filename ,`last_error_file`),
		`last_file` = filename,
		`last_update` = file_time
	WHERE `obj_name` = 'Operators';
END;

DROP PROCEDURE IF EXISTS `p_import_numplan`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_import_numplan`(
	IN filename VARCHAR(50),
	IN file_time BIGINT)
BEGIN
	DECLARE xrows, xtotal, xerrors INT DEFAULT 0;
	SELECT `RowCount` INTO xrows FROM `tmp_NumPlanImport` WHERE `RowCount` IS NOT NULL LIMIT 1;
	SELECT count(*) INTO xtotal FROM `tmp_NumPlanImport`;
	SELECT count(*) INTO xerrors FROM `tmp_NumPlanImport` WHERE `Errors` !='';
	IF xrows>0 THEN
		IF (xtotal-xerrors)>0 THEN
			IF xerrors=0 THEN
				DELETE FROM `t_numbering_plan`
				WHERE (`NumberFrom`, `NumberTo`) NOT IN
					(SELECT `NumberFrom`, `NumberTo` FROM `tmp_NumPlanImport`);
			END IF;
			INSERT INTO `t_numbering_plan`(`NumberFrom`, `NumberTo`, `OwnerId`, `RegionCode`, `MNC`)
				SELECT
					a.`NumberFrom`,
					a.`NumberTo`,
					a.`OwnerId`,
					a.`RegionCode`,
					a.`MNC`
				FROM `tmp_NumPlanImport` AS a
				WHERE a.`Errors` = ''
			ON DUPLICATE KEY UPDATE
				`OwnerId`=a.`OwnerId`,
				`RegionCode` = a.`RegionCode`,
				`MNC` = a.`MNC`;
		END IF;
		IF xerrors>0 THEN
			SELECT CONCAT('line:',`id`+1,'. Errors in:',`Errors`) AS `ERR`
			FROM `tmp_NumPlanImport`
			WHERE `Errors` !=''
			LIMIT 15;
		ELSEIF (xrows-xtotal)>0 THEN
			SELECT CONCAT('There are ',xrows-xtotal,' records can not be imported from ',filename);
		END IF;
	END IF;
	UPDATE `t_info` SET
		`last_error_file` = IF(xerrors+(xrows-xtotal) != 0 ,filename ,`last_error_file`),
		`last_file` = filename,
		`last_update` = file_time
	WHERE `obj_name` = 'NumberingPlan';
END;

DROP PROCEDURE IF EXISTS `p_import_portall`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_import_portall`(
	IN filename VARCHAR(50),
	IN file_time BIGINT)
BEGIN
	DECLARE xrows, xtotal, xerrors INT DEFAULT 0;
	SELECT `RowCount` INTO xrows FROM `tmp_Port_AllImport` WHERE `RowCount` IS NOT NULL LIMIT 1;
	SELECT count(*) INTO xtotal FROM `tmp_Port_AllImport`;
	SELECT count(*) INTO xerrors FROM `tmp_Port_AllImport` WHERE `Errors` !='';
	IF xrows>0 THEN
		IF (xerrors+(xrows-xtotal))=0 THEN
			TRUNCATE TABLE `t_port_all`;
			INSERT INTO `t_port_all`(`Number`, `OwnerId`, `MNC`, `Route`, `RegionCode`, `PortDateFET`)
				SELECT `Number`, `OwnerId`, `MNC`, `Route`, `RegionCode`, `PortDate`
				FROM `tmp_Port_AllImport`
				WHERE `Errors` = ''
				ORDER BY `Number`;
		END IF;
		IF xerrors>0 THEN
			SELECT CONCAT('line:',`id`+1,'. Errors in:',`Errors`) AS `ERR`
			FROM `tmp_Port_AllImport`
			WHERE `Errors` !=''
			LIMIT 15;
		ELSEIF (xrows-xtotal)>0 THEN
			SELECT CONCAT('There are ',xrows-xtotal,' records can not be imported from ',filename);
		END IF;
	END IF;
	UPDATE `t_info` SET
		`enable_update` = IF(xerrors = 0 AND xrows = xtotal AND `obj_name` = 'PortAll', 0, 1),
		`last_error_file` = IF((xerrors > 0 OR xrows > xtotal) AND `obj_name` = 'PortAll', filename, `last_error_file`),
		`last_file` = filename,
		`last_update` = file_time
	WHERE `obj_name` IN ('PortAll','ReturnIncrement','PortIncrement');
END;

DROP PROCEDURE IF EXISTS `p_import_portinc`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_import_portinc`(
	IN filename VARCHAR(50),
	IN file_time BIGINT)
BEGIN
	DECLARE xrows, xtotal, xerrors INT DEFAULT 0;
	SELECT `RowCount` INTO xrows FROM `tmp_PortIncrement` WHERE `RowCount` IS NOT NULL LIMIT 1;
	SELECT count(*) INTO xtotal FROM `tmp_PortIncrement`;
	SELECT count(*) INTO xerrors FROM `tmp_PortIncrement` WHERE `Errors` !='';
	IF xrows>0 THEN
		IF (xtotal-xerrors)>0 THEN
			DELETE QUICK FROM a USING `t_port_all` AS a
			LEFT JOIN `tmp_PortIncrement` AS b ON a.`Number`=b.`Number`
			WHERE b.`Errors` = '';
			INSERT INTO `t_port_all`(`Number`, `OwnerId`, `MNC`, `Route`, `RegionCode`, `PortDateFET`)
				SELECT
					a.`Number`,
					a.`RecipientId`,
					a.`NewMNC`,
					a.`NewRoute`,
					a.`RegionCode`,
					a.`PortDate`
				FROM `tmp_PortIncrement` AS a
				WHERE a.`Errors` ='' AND a.`RecipientId` != a.`RangeHolderId`
				ORDER BY a.`Number`;
		END IF;
		IF xerrors>0 THEN
			SELECT CONCAT('line:',`id`+1,'. Errors in:',`Errors`) AS `ERR`
			FROM `tmp_PortIncrement`
			WHERE `Errors` !=''
			LIMIT 15;
		ELSEIF (xrows-xtotal)>0 THEN
			SELECT CONCAT('There are ',xrows-xtotal,' records can not be imported from ',filename);
		END IF;
	END IF;
	UPDATE `t_info` SET
		`enable_update` = IF(xerrors+(xrows-xtotal) != 0 AND `obj_name`='PortAll',1,`enable_update`),
		`last_error_file` = IF(xerrors+(xrows-xtotal) != 0 AND `obj_name`='PortIncrement' ,filename ,`last_error_file`),
		`last_file` = IF(`obj_name`='PortIncrement', filename, `last_file`),
		`last_update` = IF(`obj_name`='PortIncrement', file_time, `last_update`)
	WHERE `obj_name` IN ('PortAll','PortIncrement');
END;

DROP PROCEDURE IF EXISTS `p_import_returninc`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_import_returninc`(
	IN filename VARCHAR(50),
	IN file_time BIGINT)
BEGIN
	DECLARE xrows, xtotal, xerrors INT DEFAULT 0;
	SELECT `RowCount` INTO xrows FROM `tmp_ReturnIncrement` WHERE `RowCount` IS NOT NULL LIMIT 1;
	SELECT count(*) INTO xtotal FROM `tmp_ReturnIncrement`;
	SELECT count(*) INTO xerrors FROM `tmp_ReturnIncrement` WHERE `Errors` !='';
	IF xrows>0 THEN
		IF (xtotal-xerrors)>0 THEN
			DELETE QUICK FROM a USING `t_port_all` AS a
			LEFT JOIN `tmp_ReturnIncrement` AS b ON a.`Number`=b.`Number`
			WHERE b.`Errors` = '';
		END IF;
		IF xerrors>0 THEN
			SELECT CONCAT('line:',`id`+1,'. Errors in:',`Errors`) AS `ERR`
			FROM `tmp_ReturnIncrement`
			WHERE `Errors` !=''
			LIMIT 15;
		ELSEIF (xrows-xtotal)>0 THEN
			SELECT CONCAT('There are ',xrows-xtotal,' records can not be imported from ',filename);
		END IF;
	END IF;
	UPDATE `t_info` SET
		`enable_update` = IF(xerrors+(xrows-xtotal) != 0 AND `obj_name`='PortAll', 1, `enable_update`),
		`last_error_file` = IF(xerrors+(xrows-xtotal) != 0 AND `obj_name`='ReturnIncrement' , filename,`last_error_file`),
		`last_file` = IF(`obj_name`='ReturnIncrement', filename, `last_file`),
		`last_update` = IF(`obj_name`='ReturnIncrement', file_time, `last_update`)
	WHERE `obj_name` IN ('PortAll','ReturnIncrement');
END;

DROP PROCEDURE IF EXISTS `p_get_info`;
CREATE DEFINER=CURRENT_USER PROCEDURE `p_get_info`(
/*** Получение всей доступной в БДПН информации по номеру ***/
	INOUT num 	BIGINT UNSIGNED,		-- Номер абонента в е.164.
	OUT	mnc 		TINYINT UNSIGNED,		-- MNC сети оператора.
	OUT	brand		VARCHAR(200),	-- Наименование "Брэнда".
	OUT	org_code 	VARCHAR(50),	-- Буквенный код оператора БДПН.
	OUT	org_name	VARCHAR(100),	-- Наименование оператора.
	OUT	region_id	TINYINT UNSIGNED,		-- Код региона РФ в котором зарегистрирован диапазон в который входит абонент.
	OUT	region_name	VARCHAR(56),	-- Наименование региона РФ.
	OUT	region_z	TINYINT UNSIGNED,		-- Сдвиг времени региона относительно FET(UTC+3) для вычисления времени региона
	OUT	port_date	DATETIME		-- Дата портирования, если актуально.
)
BEGIN
	/*Дополнительно присваиваем переменным дефолтные параметры*/
	SELECT 0, 'UNKNOWN', 'UNKNOWN', 'UNKNOWN', 0, 'UNKNOWN', NULL, NULL
	INTO mnc,brand, org_code, org_name, region_id, region_name, region_z, port_date;
	/********************************/
	IF (num REGEXP '^(7|8)?9[0-9]{9}$') THEN
		SET num=RIGHT(num,10);
		SELECT a.`OwnerId`,a.`MNC`,a.`RegionCode`,a.`PortDateFET` INTO org_code,mnc,region_id,port_date FROM `t_port_all` AS a WHERE a.`Number` = num;
		IF (mnc = 0) THEN
			SELECT a.`OwnerId`,a.`MNC`,a.`RegionCode` INTO org_code,mnc,region_id FROM `t_numbering_plan` AS a WHERE num BETWEEN a.`NumberFrom` AND a.`NumberTo`;
		END IF;
		IF (mnc != 0) THEN
			SELECT IF(a.`MNC_brand` = 0,ifnull(a.`name`,'UNKNOWN'), (SELECT ifnull(b.`name`,'UNKNOWN') FROM `t_mnc` AS b WHERE b.`MNC` = a.`MNC_brand`)) INTO brand FROM `t_mnc` AS a WHERE a.`MNC` = mnc;
			SELECT ifnull(a.`Name`,'UNKNOWN'), a.`FETimeModifier` INTO region_name, region_z FROM `t_regions` AS a WHERE a.`RegionCode` = region_id;
			SELECT ifnull(a.`OrgName`,'UNKNOWN') INTO org_name FROM `t_operators` AS a WHERE a.`OrgCode` = org_code AND a.`MNC` = mnc;
		END IF;
	END IF;
END;

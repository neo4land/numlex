# -*- coding: utf8 -*-
__author__ = "Stinger <neo4land@gmail.com>"
__license__ = "GNU Lesser General Public License (LGPL)"


class BDPNquery:
    def __init__(self):
        self.get_info = "SELECT version() as version"
        self.update = "SELECT CONCAT('update', ' test',' OK') as TEST"


class Operators(BDPNquery):
    get_info = """SELECT `last_update`, `enable_update` FROM `t_info` WHERE `obj_name` = 'Operators'"""

    update = \
"""DROP TABLE IF EXISTS tmp_operators;
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_operators
(`id` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, `OrgCode` VARCHAR(50) NOT NULL, `MNC` TINYINT UNSIGNED NOT NULL, 
`TIN` VARCHAR(100), `OrgName` VARCHAR(200), `Errors` VARCHAR(11) NULL, `RowCount` INT UNSIGNED NULL) 
COLLATE = utf8_bin CHARACTER SET = utf8 
ENGINE=MEMORY; 
LOAD DATA local INFILE '{fst}'
INTO TABLE tmp_operators 
CHARACTER SET 'utf8' 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES 
(@OrgCode,@MNC,TIN,OrgName,@RowCount)
SET 
  OrgCode = @OrgCode,
  MNC = IF(@MNC ='',0,@MNC),
  Errors = CONCAT_WS(',',IF(@MNC REGEXP '^[0-9]{{2}}$' ,NULL,'MNC'),
    IF(@OrgCode REGEXP '^m[A-z0-9]{{1,50}}$',NULL,'OrgCode')),
  RowCount = IF(@RowCount = 0, NULL, @RowCount); 
CALL p_import_operators('{snd}', {frd});
DROP TABLE IF EXISTS tmp_operators;"""


class NumberingPlan(BDPNquery):
    get_info = """SELECT `last_update`, `enable_update` FROM `t_info` WHERE `obj_name` = 'NumberingPlan'"""

    update = \
"""DROP TABLE IF EXISTS tmp_NumPlanImport;
CREATE TABLE tmp_NumPlanImport
(`id` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, `NumberFrom` BIGINT UNSIGNED NOT NULL, 
`NumberTo` BIGINT UNSIGNED NOT NULL, `OwnerId` VARCHAR(50) NOT NULL, `RegionCode` TINYINT UNSIGNED NOT NULL, 
`MNC` TINYINT UNSIGNED NOT NULL, `Errors` VARCHAR(42) NULL, `RowCount` INT UNSIGNED NULL)
COLLATE = utf8_bin CHARACTER SET = utf8 
ENGINE = MEMORY;
LOAD DATA local INFILE '{fst}' 
INTO TABLE tmp_NumPlanImport 
FIELDS TERMINATED BY ',' 
LINES TERMINATED BY '\r\n' 
IGNORE 1 LINES
(@NumberFrom,@NumberTo,@OwnerId,@RegionCode,@MNC,@RowCount)
SET
  NumberFrom = IF(@NumberFrom ='',0,@NumberFrom),
  NumberTo = IF(@NumberTo ='',0,@NumberTo),
  OwnerId = @OwnerId,
  RegionCode = IF(@RegionCode ='',0,@RegionCode),
  MNC = IF(@MNC ='',0,@MNC),
  Errors = CONCAT_WS(',',
    IF(@NumberFrom REGEXP '^9[0-9]{{9}}$', NULL, 'NumberFrom'),
    IF(@NumberTo REGEXP '^9[0-9]{{9}}$', NULL, 'NumberTo'),
    IF(@OwnerId REGEXP '^m[A-z0-9]{{1,50}}$', NULL, 'OwnerId'),
    IF(@RegionCode REGEXP '^[0-9]{{2}}$', NULL, 'RegionCode'),
    IF(@MNC REGEXP '^[0-9]{{2}}$', NULL, 'MNC')),
  RowCount = IF(@RowCount = 0, NULL, @RowCount);
CALL p_import_numplan('{snd}', {frd});
DROP TABLE IF EXISTS tmp_NumPlanImport;"""


class PortIncrement(BDPNquery):
    get_info = """SELECT `last_update`, `enable_update` FROM `t_info` WHERE `obj_name` = 'PortIncrement'"""

    update = \
"""DROP TABLE IF EXISTS tmp_PortIncrement;
CREATE TABLE tmp_PortIncrement
(`id` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, Number BIGINT UNSIGNED NOT NULL, `RecipientId` VARCHAR(50) NOT NULL,
`RangeHolderId` VARCHAR(50), `NewMNC` TINYINT UNSIGNED NOT NULL, `NewRoute` VARCHAR(5),
`RegionCode` TINYINT UNSIGNED NOT NULL, `PortDate` DATETIME, `Errors` VARCHAR(36) NULL, `RowCount` INT UNSIGNED NULL,
INDEX `ix_num` USING BTREE (`Number`))
COLLATE = utf8_bin CHARACTER SET = utf8
ENGINE=MEMORY;
LOAD DATA local INFILE '{fst}'
INTO TABLE tmp_PortIncrement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@dummy,@Number,@RecipientId,@dummy,RangeHolderId,@dummy,
NewRoute,@dummy,@NewMNC,@RegionCode,@PortDate,@RowCount)
SET
  Number = IF(@Number ='',0,@Number),
  RecipientId = @RecipientId,
  NewMNC = IF(@NewMNC ='',0,@NewMNC),
  RegionCode = IF(@RegionCode ='',0,@RegionCode),
  PortDate = IF(@PortDate = '',NOW(),STR_TO_DATE(left(replace(@PortDate,'T',' '),19), '%Y-%m-%d %H:%i:%s')),
  Errors = CONCAT_WS(',',
    IF(@Number REGEXP '^9[0-9]{{9}}$', NULL, 'Number'),
    IF(@RecipientId REGEXP '^m[A-z0-9]{{1,50}}$', NULL, 'RecipientId'),
    IF(@NewMNC REGEXP '^[0-9]{{2}}$', NULL, 'NewMNC'),
    IF(@RegionCode REGEXP '^[0-9]{{2}}$', NULL, 'RegionCode')),
  RowCount = IF(@RowCount = 0, NULL, @RowCount);
CALL p_import_portinc('{snd}', {frd});
DROP TABLE IF EXISTS tmp_PortIncrement;"""


class ReturnIncrement(BDPNquery):
    get_info = """SELECT `last_update`, `enable_update` FROM `t_info` WHERE `obj_name` = 'ReturnIncrement'"""

    update = \
"""DROP TABLE IF EXISTS tmp_ReturnIncrement;
CREATE TABLE tmp_ReturnIncrement
(`id` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, `Number` BIGINT UNSIGNED NOT NULL, `Errors` VARCHAR(6) NULL,
`RowCount` INT UNSIGNED NULL, INDEX `ix_num` USING BTREE (`Number`))
COLLATE = utf8_bin CHARACTER SET = utf8
ENGINE=MEMORY;
LOAD DATA local INFILE '{fst}'
INTO TABLE tmp_ReturnIncrement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@dummy,@Number,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@dummy,@RowCount)
SET
  Number = IF(@Number ='',0,@Number),
  Errors = IF(@Number REGEXP '^9[0-9]{{9}}$', NULL, 'Number'),
  RowCount = IF(@RowCount = 0, NULL, @RowCount);
CALL p_import_returninc('{snd}', {frd});
DROP TABLE IF EXISTS tmp_ReturnIncrement;"""


class PortAll(BDPNquery):
    get_info = """SELECT `last_update`, `enable_update` FROM `t_info` WHERE `obj_name` = 'PortAll'"""

    update = \
"""DROP TABLE IF EXISTS tmp_Port_AllImport;
SET SESSION SQL_BIG_SELECTS=1;
CREATE TEMPORARY TABLE IF NOT EXISTS tmp_Port_AllImport
(`id` INTEGER UNSIGNED AUTO_INCREMENT PRIMARY KEY, `Number` BIGINT UNSIGNED NOT NULL, `OwnerId` VARCHAR(50) NOT NULL,
`MNC` TINYINT UNSIGNED NOT NULL, `Route` VARCHAR(5), `RegionCode` TINYINT UNSIGNED NOT NULL, `PortDate` DATETIME,
`Errors` VARCHAR(29) NULL, `RowCount` INT UNSIGNED NULL, INDEX `ix_num` USING BTREE (`Number`))
COLLATE = utf8_bin CHARACTER SET = utf8;
LOAD DATA local INFILE '{fst}'
INTO TABLE tmp_Port_AllImport
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(@Number,@OwnerId,@MNC,Route,@RegionCode,@PortDate,@RowCount)
SET
  Number = IF(@Number ='',0,@Number),
  OwnerId = @OwnerId,
  MNC = IF(@MNC ='',0,@MNC),
  RegionCode = IF(@RegionCode ='',0,@RegionCode),
  PortDate = IF(@PortDate = '',NOW(),STR_TO_DATE(left(replace(@PortDate,'T',' '),19), '%Y-%m-%d %H:%i:%s')),
  Errors = CONCAT_WS(',',
    IF(@Number REGEXP '^9[0-9]{{9}}$', NULL, 'Number'),
    IF(@OwnerId REGEXP '^m[A-z0-9]{{1,50}}$', NULL, 'OwnerId'),
    IF(@MNC REGEXP '^[0-9]{{2}}$', NULL, 'MNC'),
    IF(@RegionCode REGEXP '^[0-9]{{2}}$', NULL, 'RegionCode')),
  RowCount = IF(@RowCount = 0, NULL, @RowCount); 
CALL p_import_portall('{snd}', {frd});
DROP TABLE IF EXISTS tmp_Port_AllImport;"""

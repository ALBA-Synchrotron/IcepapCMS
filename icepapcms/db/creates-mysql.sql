-- ----------------------------------------------------------------------
-- MySQL GRT Application
-- SQL Script
-- ----------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `icepapcms`
  CHARACTER SET latin1;
-- -------------------------------------
-- Tables

DROP TABLE IF EXISTS `icepapcms`.`cfgparameter`;
CREATE TABLE `icepapcms`.`cfgparameter` (
  `name` VARCHAR(20) NOT NULL DEFAULT '',
  `cfg_id` INT(10) unsigned NOT NULL DEFAULT '0',
  `value` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`name`, `cfg_id`),
  INDEX `CfgParameter_FKIndex1` (`cfg_id`),
  CONSTRAINT `cfgparameter_ibfk_1` FOREIGN KEY `cfgparameter_ibfk_1` (`cfg_id`)
    REFERENCES `icepapcms`.`icepapdrivercfg` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

DROP TABLE IF EXISTS `icepapcms`.`cfgparameterinfo`;
CREATE TABLE `icepapcms`.`cfgparameterinfo` (
  `name` VARCHAR(20) NOT NULL DEFAULT '',
  `info` VARCHAR(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`)
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

DROP TABLE IF EXISTS `icepapcms`.`icepapdriver`;
CREATE TABLE `icepapcms`.`icepapdriver` (
  `icepapsystem_name` VARCHAR(25) NOT NULL DEFAULT '',
  `addr` INT(10) unsigned NOT NULL,
  `name` VARCHAR(32) NULL,
  `mode` VARCHAR(10) NULL,
  PRIMARY KEY (`addr`, `icepapsystem_name`),
  INDEX `IcepapDriver_FKIndex1` (`icepapsystem_name`),
  CONSTRAINT `icepapdriver_ibfk_1` FOREIGN KEY `icepapdriver_ibfk_1` (`icepapsystem_name`)
    REFERENCES `icepapcms`.`icepapsystem` (`name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

DROP TABLE IF EXISTS `icepapcms`.`icepapdrivercfg`;
CREATE TABLE `icepapcms`.`icepapdrivercfg` (
  `id` INT(10) unsigned NOT NULL AUTO_INCREMENT,
  `icepapsystem_name` VARCHAR(25) NULL,
  `driver_addr` INT(10) unsigned NULL,
  `name` VARCHAR(40) NOT NULL,
  `description` VARCHAR(255) NULL,
  `signature` VARCHAR(64) NULL,
  `date` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `IcepapDriverCfg_FKIndex1` (`driver_addr`, `icepapsystem_name`),
  CONSTRAINT `icepapdrivercfg_ibfk_1` FOREIGN KEY `icepapdrivercfg_ibfk_1` (`driver_addr`, `icepapsystem_name`)
    REFERENCES `icepapcms`.`icepapdriver` (`addr`, `icepapsystem_name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

DROP TABLE IF EXISTS `icepapcms`.`icepapsystem`;
CREATE TABLE `icepapcms`.`icepapsystem` (
  `name` VARCHAR(25) NOT NULL DEFAULT '',
  `host` VARCHAR(25) NOT NULL DEFAULT '',
  `port` INT(10) unsigned NOT NULL DEFAULT '5000',
  `description` VARCHAR(250) NULL,
  `version` VARCHAR(10) NULL,
  `location_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`name`),
  INDEX `FKLocation` (`location_name`),
  CONSTRAINT `FKLocation` FOREIGN KEY `FKLocation` (`location_name`)
    REFERENCES `icepapcms`.`location` (`name`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;

DROP TABLE IF EXISTS `icepapcms`.`location`;
CREATE TABLE `icepapcms`.`location` (
  `name` VARCHAR(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`name`)
)
ENGINE = InnoDB
ROW_FORMAT = Compact
CHARACTER SET latin1 COLLATE latin1_swedish_ci;



SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------
-- EOF


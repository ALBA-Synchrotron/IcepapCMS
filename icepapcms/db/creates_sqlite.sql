-- 
-- Created by SQL::Translator::Producer::SQLite
-- Created on Mon Oct  8 14:33:24 2007
-- 


--
-- Table: cfgparameter
--
CREATE TABLE cfgparameter (
  name varchar(20) NOT NULL DEFAULT '',
  cfg_id int(10) NOT NULL DEFAULT '0',
  value varchar(45) NOT NULL DEFAULT '',
  PRIMARY KEY (name, cfg_id)
);

--
-- Table: cfgparameterinfo
--
CREATE TABLE cfgparameterinfo (
  name varchar(20) NOT NULL DEFAULT '',
  info varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (name)
);

--
-- Table: icepapdriver
--
CREATE TABLE icepapdriver (
  icepapsystem_name varchar(25) NOT NULL DEFAULT '',
  addr int(10) NOT NULL DEFAULT '',
  name varchar(32),
  mode varchar(10),
  PRIMARY KEY (icepapsystem_name, addr)
);

--
-- Table: icepapdrivercfg
--
CREATE TABLE icepapdrivercfg (
  id INTEGER PRIMARY KEY NOT NULL,
  icepapsystem_name varchar(25),
  driver_addr int(10),
  name varchar(40) NOT NULL DEFAULT '',
  description varchar(255),
  signature varchar(64),
  date datetime NOT NULL DEFAULT ''
);

--
-- Table: icepapsystem
--
CREATE TABLE icepapsystem (
  name varchar(25) NOT NULL DEFAULT '',
  host varchar(25) NOT NULL DEFAULT '',
  port int(10) NOT NULL DEFAULT '5000',
  description varchar(250),
  version varchar(10),
  location_name varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (name)
);

--
-- Table: location
--
CREATE TABLE location (
  name varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (name)
);

CREATE INDEX CfgParameter_FKIndex1_cfgparam on cfgparameter (cfg_id);
CREATE INDEX IcepapDriver_FKIndex1_icepapdr on icepapdriver (icepapsystem_name);
CREATE INDEX IcepapDriverCfg_FKIndex1_icepa on icepapdrivercfg (driver_addr, icepapsystem_name);
CREATE INDEX FKLocation_icepapsystem on icepapsystem (location_name);


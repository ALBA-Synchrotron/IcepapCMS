/*
 * MySQL Script to increase maximum size of
 * problematic columns @MaxIV
 */

ALTER TABLE `icepapcms`.`icepapsystem`
  MODIFY `name` VARCHAR(100) NOT NULL DEFAULT '',
  MODIFY `host` VARCHAR(100) NOT NULL DEFAULT '';

ALTER TABLE `icepapcms`.`icepapdrivercfg`
  MODIFY `icepapsystem_name` VARCHAR(100) NULL,
  MODIFY `signature` VARCHAR(100) NULL;

ALTER TABLE `icepapcms`.`icepapdriver`
  MODIFY `icepapsystem_name` VARCHAR(100) NOT NULL DEFAULT '';



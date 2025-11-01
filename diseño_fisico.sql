-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `mydb` ;

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`DIM_Fecha`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Fecha` (
  `idDIM_Fecha` INT NOT NULL,
  `Fecha_Completa` DATE NULL,
  `Dia` INT NULL,
  `Mes` INT NULL,
  `Año` INT NULL,
  PRIMARY KEY (`idDIM_Fecha`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DIM_Ubicacion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Ubicacion` (
  `idDIM_Ubicacion` INT NOT NULL,
  `Municipio` VARCHAR(45) NULL,
  `Provincia` VARCHAR(45) NULL,
  `Latitud` INT NULL,
  `Longitud` INT NULL,
  `Tipo_suelo` VARCHAR(45) NULL,
  `Poblacion_total` INT NULL,
  `Poblacion>65` INT NULL,
  PRIMARY KEY (`idDIM_Ubicacion`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DIM_Causa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_Causa` (
  `idDIM_Causa` INT NOT NULL,
  `Cod_Causa` INT NULL,
  `Causa_Detalle` VARCHAR(45) NULL,
  PRIMARY KEY (`idDIM_Causa`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`DIM_CLIMA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`DIM_CLIMA` (
  `idDIM_CLIMA` INT NOT NULL,
  `Temp_Max` INT NULL,
  `Temp_Min` INT NULL,
  `Viento (Km/h)` INT NULL,
  ` Humedad(%)` INT NULL,
  `Dias secos acumulados` INT NULL,
  PRIMARY KEY (`idDIM_CLIMA`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`HECHO_INCENDIO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`HECHO_INCENDIO` (
  `idHECHO_INCENDIO` INT NOT NULL,
  `FK_Fecha` INT NOT NULL,
  `FK_Ubicacion` INT NOT NULL,
  `FK_Clima` INT NOT NULL,
  `FK_Causa` INT NOT NULL,
  `Superficie_total(Ha)` INT NULL,
  `Tiempo_extinción` INT NULL,
  `Num_muertos` INT NULL,
  `Num_heridos` INT NULL,
  `Tiempo_ctrl` INT NULL,
  `Tiempo_ext` INT NULL,
  `Personal` INT NULL,
  `Medios` INT NULL,
  `Gastos` INT NULL,
  `Perdidas_econom` INT NULL,
  PRIMARY KEY (`idHECHO_INCENDIO`),
  INDEX `id_Ubicacion_idx` (`FK_Ubicacion` ASC) VISIBLE,
  INDEX `FK_Fecha_idx` (`FK_Fecha` ASC) VISIBLE,
  INDEX `FK_Causa_idx` (`FK_Causa` ASC) VISIBLE,
  INDEX `FK_Clima_idx` (`FK_Clima` ASC) VISIBLE,
  CONSTRAINT `FK_Fecha`
    FOREIGN KEY (`FK_Fecha`)
    REFERENCES `mydb`.`DIM_Fecha` (`idDIM_Fecha`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Ubicacion`
    FOREIGN KEY (`FK_Ubicacion`)
    REFERENCES `mydb`.`DIM_Ubicacion` (`idDIM_Ubicacion`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Causa`
    FOREIGN KEY (`FK_Causa`)
    REFERENCES `mydb`.`DIM_Causa` (`idDIM_Causa`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Clima`
    FOREIGN KEY (`FK_Clima`)
    REFERENCES `mydb`.`DIM_CLIMA` (`idDIM_CLIMA`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

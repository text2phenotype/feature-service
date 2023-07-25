-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema feature_database
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema feature_database
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `feature_database` DEFAULT CHARACTER SET utf8 ;
USE `feature_database` ;

-- -----------------------------------------------------
-- Table `feature_database`.`FeatureSet`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`FeatureSet` (
  `id` INT NOT NULL,
  `version` VARCHAR(45) NULL,
  `jira` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`Document`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`Document` (
  `id` INT NOT NULL,
  `docId` BINARY(16) NULL,
  `url` TEXT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `docId_UNIQUE` (`docId` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`Corpus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`Corpus` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `url` TEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`DocumentsToCorpus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`DocumentsToCorpus` (
  `id` INT NOT NULL,
  `documentId` INT NULL,
  `corpusId` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fkDocumentId_idx` (`documentId` ASC) VISIBLE,
  INDEX `fkCorpusId_idx` (`corpusId` ASC) VISIBLE,
  CONSTRAINT `fk_DocumentToCorpus_Document`
    FOREIGN KEY (`documentId`)
    REFERENCES `feature_database`.`Document` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_DocumentToCorpus_Corpus`
    FOREIGN KEY (`corpusId`)
    REFERENCES `feature_database`.`Corpus` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`FeatureGroup`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`FeatureGroup` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`Feature`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`Feature` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `featureGroupId` INT NULL,
  `requiresAnnotation` TINYINT NULL,
  `current` TINYINT NULL,
  `version` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fkFeatureGroup_idx` (`featureGroupId` ASC) VISIBLE,
  CONSTRAINT `fk_Feature_FeatureGroup`
    FOREIGN KEY (`featureGroupId`)
    REFERENCES `feature_database`.`FeatureGroup` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`FeatureSetToCorpus`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`FeatureSetToCorpus` (
  `id` INT NOT NULL,
  `featureSetId` INT NULL,
  `corpusId` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fkCorpus_idx` (`corpusId` ASC) VISIBLE,
  INDEX `fkFeatureSet_idx` (`featureSetId` ASC) VISIBLE,
  CONSTRAINT `fk_FeatureSetToCorpus_FeatureSet`
    FOREIGN KEY (`featureSetId`)
    REFERENCES `feature_database`.`FeatureSet` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_FeatureSetToCorpus_Corpus`
    FOREIGN KEY (`corpusId`)
    REFERENCES `feature_database`.`Corpus` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`MachineAnnotation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`MachineAnnotation` (
  `id` INT NOT NULL,
  `featureId` INT NULL,
  `json` JSON NULL,
  `documentId` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fkDocument_idx` (`documentId` ASC) VISIBLE,
  INDEX `fkFeature_idx` (`featureId` ASC) VISIBLE,
  CONSTRAINT `fk_MachineAnnotation_Document`
    FOREIGN KEY (`documentId`)
    REFERENCES `feature_database`.`Document` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_MachineAnnotation_Feature`
    FOREIGN KEY (`featureId`)
    REFERENCES `feature_database`.`Feature` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`FeatureSetToFeatures`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`FeatureSetToFeatures` (
  `id` INT NOT NULL,
  `featureSetId` INT NULL,
  `featureId` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fkFeatureSet_idx` (`featureSetId` ASC) VISIBLE,
  INDEX `fkFeature_idx` (`featureId` ASC) VISIBLE,
  CONSTRAINT `fk_FeatureSetToFeatures_FeatureSet`
    FOREIGN KEY (`featureSetId`)
    REFERENCES `feature_database`.`FeatureSet` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_FeatureSetToFeatures_Feature`
    FOREIGN KEY (`featureId`)
    REFERENCES `feature_database`.`Feature` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`HumanAnnotation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`HumanAnnotation` (
  `id` INT NOT NULL,
  `humanId` VARCHAR(45) NULL,
  `documentId` INT NULL,
  `version` VARCHAR(45) NULL,
  `text` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fkDocument_idx` (`documentId` ASC) VISIBLE,
  CONSTRAINT `fk_HumanAnnotation_Document`
    FOREIGN KEY (`documentId`)
    REFERENCES `feature_database`.`Document` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`Label`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`Label` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `feature_database`.`HumanLabeled`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `feature_database`.`HumanLabeled` (
  `id` INT NOT NULL,
  `humanAnnotationId` INT NULL,
  `json` JSON NULL,
  `labelId` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fkHumanAnnotation_idx` (`humanAnnotationId` ASC) VISIBLE,
  INDEX `fkLabel_idx` (`labelId` ASC) VISIBLE,
  CONSTRAINT `fk_HumanLabeled_HumanAnnotation`
    FOREIGN KEY (`humanAnnotationId`)
    REFERENCES `feature_database`.`HumanAnnotation` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_HumanLabeled_Label`
    FOREIGN KEY (`labelId`)
    REFERENCES `feature_database`.`Label` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema homework_sql_1
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `homework_sql_1` ;

-- -----------------------------------------------------
-- Schema homework_sql_1
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `homework_sql_1` DEFAULT CHARACTER SET utf8 ;
USE `homework_sql_1` ;

-- -----------------------------------------------------
-- Table `homework_sql_1`.`supplier`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `homework_sql_1`.`supplier` ;

CREATE TABLE IF NOT EXISTS `homework_sql_1`.`supplier` (
  `supplier_id` INT NOT NULL AUTO_INCREMENT,
  `supplier_name` VARCHAR(45) NULL,
  `suplier_address` VARCHAR(100) NULL,
  `suplier_phone` VARCHAR(45) NULL,
  PRIMARY KEY (`supplier_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `homework_sql_1`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `homework_sql_1`.`products` ;

CREATE TABLE IF NOT EXISTS `homework_sql_1`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(45) NULL,
  `price` DECIMAL(3) NULL,
  `supplier_id` INT NULL,
  PRIMARY KEY (`product_id`),
  CONSTRAINT `suplier_id`
    FOREIGN KEY (`supplier_id`)
    REFERENCES `homework_sql_1`.`supplier` (`supplier_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE UNIQUE INDEX `item_id_UNIQUE` ON `homework_sql_1`.`products` (`product_id` ASC) VISIBLE;

CREATE INDEX `suplier_id_idx` ON `homework_sql_1`.`products` (`supplier_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `homework_sql_1`.`customer`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `homework_sql_1`.`customer` ;

CREATE TABLE IF NOT EXISTS `homework_sql_1`.`customer` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `customer_name` VARCHAR(45) NULL,
  `customer_surname` VARCHAR(45) NULL,
  `customer_phone` VARCHAR(45) NULL,
  `customer_address` VARCHAR(100) NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;

CREATE UNIQUE INDEX `customer_id_UNIQUE` ON `homework_sql_1`.`customer` (`customer_id` ASC) VISIBLE;


-- -----------------------------------------------------
-- Table `homework_sql_1`.`order`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `homework_sql_1`.`order` ;

CREATE TABLE IF NOT EXISTS `homework_sql_1`.`order` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `product_id` INT NULL,
  `customer_id` INT NULL,
  `product_amount` INT NULL,
  `order_date` DATETIME NULL,
  PRIMARY KEY (`order_id`),
  CONSTRAINT `product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `homework_sql_1`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `customer_id`
    FOREIGN KEY (`customer_id`)
    REFERENCES `homework_sql_1`.`customer` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `customer_id_idx` ON `homework_sql_1`.`order` (`customer_id` ASC) VISIBLE;

CREATE INDEX `product_id_idx` ON `homework_sql_1`.`order` (`product_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

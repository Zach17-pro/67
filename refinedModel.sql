-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema sixseven
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema sixseven
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `sixseven` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `sixseven` ;

-- -----------------------------------------------------
-- Table `sixseven`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `role` ENUM('Admin', 'Csr_Rep', 'PIN_Support', 'Platform_Manager') NOT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `full_name` VARCHAR(100) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `username` (`username` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sixseven`.`service_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`service_category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE INDEX `category_name` (`category_name` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sixseven`.`request`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`request` (
  `request_id` INT NOT NULL AUTO_INCREMENT,
  `pin_user_id` INT NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `description` TEXT NOT NULL,
  `status` ENUM('Open', 'In Progress', 'Completed', 'Cancelled') NULL DEFAULT 'Open',
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `view_count` INT NULL DEFAULT '0',
  `shortlist_count` INT NULL DEFAULT '0',
  `category_id` INT NULL,
  `location` VARCHAR(75) NOT NULL,
  PRIMARY KEY (`request_id`),
  INDEX `idx_pin_requests_pin_user` (`pin_user_id` ASC) VISIBLE,
  INDEX `idx_pin_requests_status` (`status` ASC) VISIBLE,
  INDEX `idx_pin_requests_created` (`created_at` ASC) VISIBLE,
  INDEX `category_id_fk_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `pin_requests_ibfk_1`
    FOREIGN KEY (`pin_user_id`)
    REFERENCES `sixseven`.`user` (`user_id`)
    ON DELETE CASCADE,
  CONSTRAINT `category_id_fk`
    FOREIGN KEY (`category_id`)
    REFERENCES `sixseven`.`service_category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sixseven`.`shortlist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`shortlist` (
  `shortlist_id` INT NOT NULL AUTO_INCREMENT,
  `csr_user_id` INT NOT NULL,
  `request_id` INT NOT NULL,
  `notes` TEXT NULL DEFAULT NULL,
  `added_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`shortlist_id`),
  UNIQUE INDEX `unique_csr_request` (`csr_user_id` ASC, `request_id` ASC) VISIBLE,
  INDEX `request_id` (`request_id` ASC) VISIBLE,
  INDEX `idx_csr_shortlist_csr` (`csr_user_id` ASC) VISIBLE,
  CONSTRAINT `csr_shortlist_ibfk_1`
    FOREIGN KEY (`csr_user_id`)
    REFERENCES `sixseven`.`user` (`user_id`)
    ON DELETE CASCADE,
  CONSTRAINT `csr_shortlist_ibfk_2`
    FOREIGN KEY (`request_id`)
    REFERENCES `sixseven`.`request` (`request_id`)
    ON DELETE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sixseven`.`request_view`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`request_view` (
  `view_id` INT NOT NULL AUTO_INCREMENT,
  `request_id` INT NOT NULL,
  `viewed_by_user_id` INT NULL DEFAULT NULL,
  `viewed_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `user_ip` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`view_id`),
  INDEX `request_id` (`request_id` ASC) VISIBLE,
  INDEX `viewed_by_user_id` (`viewed_by_user_id` ASC) VISIBLE,
  CONSTRAINT `request_views_ibfk_1`
    FOREIGN KEY (`request_id`)
    REFERENCES `sixseven`.`request` (`request_id`)
    ON DELETE CASCADE,
  CONSTRAINT `request_views_ibfk_2`
    FOREIGN KEY (`viewed_by_user_id`)
    REFERENCES `sixseven`.`user` (`user_id`)
    ON DELETE SET NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `sixseven`.`match`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `sixseven`.`match` (
  `match_id` INT NOT NULL AUTO_INCREMENT,
  `request_id` INT NOT NULL,
  `csr_user_id` INT NOT NULL,
  `pin_user_id` INT NOT NULL,
  `service_date` DATE NOT NULL,
  `completion_date` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('Scheduled', 'In Progress', 'Completed', 'Cancelled') NULL DEFAULT 'Scheduled',
  PRIMARY KEY (`match_id`),
  INDEX `request_id` (`request_id` ASC) VISIBLE,
  INDEX `pin_user_id` (`pin_user_id` ASC) VISIBLE,
  INDEX `idx_service_matches_dates` (`service_date` ASC, `completion_date` ASC) VISIBLE,
  INDEX `idx_service_matches_users` (`csr_user_id` ASC, `pin_user_id` ASC) VISIBLE,
  CONSTRAINT `service_matches_ibfk_1`
    FOREIGN KEY (`request_id`)
    REFERENCES `sixseven`.`request` (`request_id`)
    ON DELETE RESTRICT,
  CONSTRAINT `service_matches_ibfk_2`
    FOREIGN KEY (`csr_user_id`)
    REFERENCES `sixseven`.`user` (`user_id`)
    ON DELETE RESTRICT,
  CONSTRAINT `service_matches_ibfk_3`
    FOREIGN KEY (`pin_user_id`)
    REFERENCES `sixseven`.`user` (`user_id`)
    ON DELETE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

--
-- Dumping data for table `users`
--

LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES (1,'SystemAdmin','1','Admin','admin@email.co','System Admin','2025-10-20 04:04:41'),(2,'CSR','11','Platform_Manager','csr@email.com','John CSR','2025-10-20 04:04:41'),(3,'pin01','pin123','PIN_Support','pin@email.com','Mary Person','2025-10-20 04:04:41'),(4,'mgr','2','Platform_Manager','mgr@email.com','David Manager','2025-10-20 04:04:41'),(7,'ganbf','1','Admin',NULL,'ganbf','2025-10-20 11:26:35');
UNLOCK TABLES;

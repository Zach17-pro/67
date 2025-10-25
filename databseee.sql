CREATE DATABASE  IF NOT EXISTS `sixseven` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sixseven`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: sixseven
-- ------------------------------------------------------
-- Server version	9.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `csr_shortlist`
--

DROP TABLE IF EXISTS `csr_shortlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `csr_shortlist` (
  `shortlist_id` int NOT NULL AUTO_INCREMENT,
  `csr_user_id` int NOT NULL,
  `request_id` int NOT NULL,
  `notes` text,
  `added_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`shortlist_id`),
  UNIQUE KEY `unique_csr_request` (`csr_user_id`,`request_id`),
  KEY `request_id` (`request_id`),
  KEY `idx_csr_shortlist_csr` (`csr_user_id`),
  CONSTRAINT `csr_shortlist_ibfk_1` FOREIGN KEY (`csr_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `csr_shortlist_ibfk_2` FOREIGN KEY (`request_id`) REFERENCES `pin_requests` (`request_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `csr_shortlist`
--

LOCK TABLES `csr_shortlist` WRITE;
/*!40000 ALTER TABLE `csr_shortlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `csr_shortlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pin_requests`
--

DROP TABLE IF EXISTS `pin_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pin_requests` (
  `request_id` int NOT NULL AUTO_INCREMENT,
  `pin_user_id` int NOT NULL,
  `title` varchar(200) NOT NULL,
  `description` text NOT NULL,
  `category_id` int NOT NULL,
  `urgency` enum('Low','Medium','High','Critical') DEFAULT 'Medium',
  `status` enum('Open','In Progress','Completed','Cancelled') DEFAULT 'Open',
  `location` varchar(255) DEFAULT NULL,
  `preferred_date` date DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `view_count` int DEFAULT '0',
  `shortlist_count` int DEFAULT '0',
  PRIMARY KEY (`request_id`),
  KEY `idx_pin_requests_pin_user` (`pin_user_id`),
  KEY `idx_pin_requests_category` (`category_id`),
  KEY `idx_pin_requests_status` (`status`),
  KEY `idx_pin_requests_created` (`created_at`),
  CONSTRAINT `pin_requests_ibfk_1` FOREIGN KEY (`pin_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `pin_requests_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`category_id`) ON DELETE RESTRICT,
  CONSTRAINT `pin_requests_ibfk_3` FOREIGN KEY (`category_id`) REFERENCES `service_categories` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pin_requests`
--

LOCK TABLES `pin_requests` WRITE;
/*!40000 ALTER TABLE `pin_requests` DISABLE KEYS */;
/*!40000 ALTER TABLE `pin_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request_views`
--

DROP TABLE IF EXISTS `request_views`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_views` (
  `view_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int NOT NULL,
  `viewed_by_user_id` int DEFAULT NULL,
  `viewed_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `user_ip` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`view_id`),
  KEY `request_id` (`request_id`),
  KEY `viewed_by_user_id` (`viewed_by_user_id`),
  CONSTRAINT `request_views_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `pin_requests` (`request_id`) ON DELETE CASCADE,
  CONSTRAINT `request_views_ibfk_2` FOREIGN KEY (`viewed_by_user_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request_views`
--

LOCK TABLES `request_views` WRITE;
/*!40000 ALTER TABLE `request_views` DISABLE KEYS */;
/*!40000 ALTER TABLE `request_views` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_categories`
--

DROP TABLE IF EXISTS `service_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `category_name` (`category_name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_categories`
--

LOCK TABLES `service_categories` WRITE;
/*!40000 ALTER TABLE `service_categories` DISABLE KEYS */;
INSERT INTO `service_categories` VALUES (7,'ff'),(3,'gang'),(1,'Home'),(2,'Transport');
/*!40000 ALTER TABLE `service_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_matches`
--

DROP TABLE IF EXISTS `service_matches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_matches` (
  `match_id` int NOT NULL AUTO_INCREMENT,
  `request_id` int NOT NULL,
  `csr_user_id` int NOT NULL,
  `pin_user_id` int NOT NULL,
  `service_date` date NOT NULL,
  `completion_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `hours_spent` decimal(4,2) DEFAULT NULL,
  `rating_by_pin` int DEFAULT NULL,
  `rating_by_csr` int DEFAULT NULL,
  `feedback_by_pin` text,
  `feedback_by_csr` text,
  `status` enum('Scheduled','In Progress','Completed','Cancelled') DEFAULT 'Scheduled',
  PRIMARY KEY (`match_id`),
  KEY `request_id` (`request_id`),
  KEY `pin_user_id` (`pin_user_id`),
  KEY `idx_service_matches_dates` (`service_date`,`completion_date`),
  KEY `idx_service_matches_users` (`csr_user_id`,`pin_user_id`),
  CONSTRAINT `service_matches_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `pin_requests` (`request_id`) ON DELETE RESTRICT,
  CONSTRAINT `service_matches_ibfk_2` FOREIGN KEY (`csr_user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT,
  CONSTRAINT `service_matches_ibfk_3` FOREIGN KEY (`pin_user_id`) REFERENCES `users` (`user_id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_matches`
--

LOCK TABLES `service_matches` WRITE;
/*!40000 ALTER TABLE `service_matches` DISABLE KEYS */;
/*!40000 ALTER TABLE `service_matches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `role` enum('Admin','Csr_Rep','PIN_Support','Platform_Manager') NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'1','1','admin@email.c','System Admin','Admin','2025-10-20 04:04:41'),(2,'11','11','csr@email.com','John CSR','Platform_Manager','2025-10-20 04:04:41'),(3,'pin01','pin123','pin@email.com','Mary Person','PIN_Support','2025-10-20 04:04:41'),(4,'2','2','mgr@email.com','David Manager','Platform_Manager','2025-10-20 04:04:41'),(7,'ganbf','1',NULL,'ganbf','Admin','2025-10-20 11:26:35');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-25 22:13:50

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `AdminsFName` varchar(45) NOT NULL,
  `AdminsLName` varchar(45) NOT NULL,
  `AdminsEmail` varchar(100) NOT NULL,
  `AdminsPassword` varchar(128) NOT NULL,
  PRIMARY KEY (`AdminsEmail`),
  UNIQUE KEY `AdminsEmail_UNIQUE` (`AdminsEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES ('Test','Admin','admintest1@email.com','$6$rounds=656000$NqobOQ8d2ApFEeUO$8nml4i2HJ6kXbLa8skc3ydS8FJZ91s5TC0i2GtwTA3U9lwWKEGW3IfxEhe9a8wD3Jo4P0shhIZbLc9/IdR7Yo/'),('Adam','Jackson','AJacobs95@mail.net','$6$rounds=656000$fpgPw2Y4OYNY6Lqd$Phkdz.KPNRk2schpMMeNUYa9VnhJuUDr0lmSyeyyQOck5hf/bvQdwf26nhaWmsW2noQgMLRIc64973s54goh/1');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:24:50

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `CustomersFName` varchar(45) NOT NULL,
  `CustomersLName` varchar(45) NOT NULL,
  `CustomersEmail` varchar(100) NOT NULL,
  `CustomersPassword` varchar(512) NOT NULL,
  `CustomersType` varchar(45) NOT NULL,
  PRIMARY KEY (`CustomersEmail`),
  UNIQUE KEY `CustomersEmail_UNIQUE` (`CustomersEmail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES ('James','Jones','JamesJ@mail.email','$6$rounds=656000$KYU9w2S8u9aEjDdN$gFslygVN.JzGFhiNhFN4h2bgskW5r5/FwcPSKqKXwDRt.m1geZWRMuw32GeP.TH1qU0QcD/Aqrjv8Lgt/V8mL1','Standard'),('Jessica','Adams','JessicaA@inbox.email','$6$rounds=656000$iNrG5kOWYZzvkv.U$G6fjdphDuBB5bO97XCE7KwiDiUzSeBJS4GtT/ibYRqnpxVZihgRR4wnf03lblsIho87CpjvRagU4lVVaedlN1/','Standard'),('Joe','Smith','JoeSmith@email.com','$6$rounds=656000$shrGQIbB1gB86KP3$WzXgfRrsvn0QOESBWjlmAF09ko8tIs8phF1AXJMp/0ipbdz.2KxNtbEXVrV4iab5Kp4j.Pny.b.Dgh7.t9qp7.','Standard'),('Ryan','Jones','RJones@email.com','$6$rounds=656000$rF48xplFun9UOvRz$AV7xoo2zVr8Q6n18Qsll7e7EH3Fn5jyH7n5wTd10AYmDYbWWifNE5kcrmNXoPMZg3h0JQ0xESnuqYsT4SXW.e/','Student');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:24:59

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `venues`
--

DROP TABLE IF EXISTS `venues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venues` (
  `VenueName` varchar(80) NOT NULL,
  `VenueCapacity` smallint NOT NULL,
  `Suitability` longtext,
  PRIMARY KEY (`VenueName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venues`
--

/*!40000 ALTER TABLE `venues` DISABLE KEYS */;
INSERT INTO `venues` VALUES ('Arnolfini',100,NULL),('Ashton Gate Stadium',150,NULL),('Bristol Central Library',50,NULL),('Bristol Old Vic',110,NULL),('Community Centre A',60,NULL),('Creative Space A',30,NULL),('Creative Space B',50,NULL),('Royal West of England Academy',100,NULL),('The Hippodrome',120,NULL),('UWE Exhibition Centre',300,NULL);
/*!40000 ALTER TABLE `venues` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:25:11

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `eventtypes`
--

DROP TABLE IF EXISTS `eventtypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `eventtypes` (
  `EventTypesName` varchar(45) NOT NULL,
  PRIMARY KEY (`EventTypesName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `eventtypes`
--

/*!40000 ALTER TABLE `eventtypes` DISABLE KEYS */;
INSERT INTO `eventtypes` VALUES ('Conference'),('Courses'),('Exhibitions'),('Library Exhibitions'),('Musical'),('Other'),('Sports'),('Theatre'),('Wedding'),('Workshops');
/*!40000 ALTER TABLE `eventtypes` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:25:07

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `idEvents` int unsigned NOT NULL AUTO_INCREMENT,
  `EventsName` varchar(100) NOT NULL,
  `EventsDescription` longtext,
  `EventType` varchar(45) NOT NULL,
  `BasePrice` decimal(6,2) NOT NULL,
  `EventsConditions` longtext,
  `Venue` varchar(80) NOT NULL,
  `EventsDate` date NOT NULL,
  `EventsTime` time NOT NULL,
  PRIMARY KEY (`idEvents`),
  KEY `EventTypesName_idx` (`EventType`),
  KEY `Venue_idx` (`Venue`),
  CONSTRAINT `EventTypesName` FOREIGN KEY (`EventType`) REFERENCES `eventtypes` (`EventTypesName`),
  CONSTRAINT `Venue` FOREIGN KEY (`Venue`) REFERENCES `venues` (`VenueName`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (1,'Bristol Library Tour','A tour around Bristol Library','Library Exhibitions',0.00,NULL,'Bristol Central Library','2026-04-17','15:00:00'),(2,'UWE Open Day','Explore opportunites at UWE','Exhibitions',0.00,NULL,'UWE Exhibition Centre','2026-04-27','13:00:00'),(3,'Musical','Award-winning musical','Musical',50.00,NULL,'The Hippodrome','2026-04-18','18:30:00'),(4,'Football match','Friendly match at the stadium','Sports',70.00,NULL,'Ashton Gate Stadium','2026-04-16','19:00:00'),(5,'Play','A play enjoyable for all ages','Theatre',40.00,NULL,'The Hippodrome','2026-04-19','17:30:00'),(6,'Recycling conference','Have your say in Bristol City Council\'s recycling programme','Conference',0.00,'Only adults can attend','UWE Exhibition Centre','2026-05-26','16:00:00'),(7,'Family wedding',NULL,'Wedding',10.00,'Formal attire','Community Centre A','2026-04-09','15:15:00'),(8,'Arts and crafts workshop for children',NULL,'Workshops',5.00,'Children-oriented workshop, parents are welcome to attend','Creative Space A','2026-06-01','11:00:00'),(9,'Bristol Library Tour','Tour around Bristol Library','Library Exhibitions',0.00,NULL,'Bristol Central Library','2026-06-16','14:00:00'),(10,'Football Match','Bristol Rovers vs Bristol City','Sports',70.00,'Anti-social behaviour will not be tolerated','Ashton Gate Stadium','2026-07-24','19:00:00'),(11,'Musical','Award-winning musical at the Hippodrome','Musical',60.00,'','The Hippodrome','2026-05-08','18:30:00'),(12,'Rugby Match','','Sports',68.00,'Children must be accompanied by an adult','Ashton Gate Stadium','2026-05-22','19:00:00');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:25:03

-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookings` (
  `idBookings` int NOT NULL AUTO_INCREMENT,
  `CustomerEmail` varchar(100) NOT NULL,
  `EventID` int unsigned NOT NULL,
  `Tickets` int NOT NULL DEFAULT '1',
  `PricePaid` decimal(6,2) DEFAULT NULL,
  `DateTimeofBooking` datetime DEFAULT NULL,
  PRIMARY KEY (`idBookings`),
  UNIQUE KEY `idBookings_UNIQUE` (`idBookings`),
  KEY `idEvents_idx` (`EventID`),
  KEY `CustomersEmail_idx` (`CustomerEmail`),
  CONSTRAINT `CustomersEmail` FOREIGN KEY (`CustomerEmail`) REFERENCES `customers` (`CustomersEmail`),
  CONSTRAINT `idEvents` FOREIGN KEY (`EventID`) REFERENCES `events` (`idEvents`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookings`
--

/*!40000 ALTER TABLE `bookings` DISABLE KEYS */;
INSERT INTO `bookings` VALUES (1,'JoeSmith@email.com',1,1,0.00,'2026-03-23 12:15:23'),(2,'JoeSmith@email.com',2,1,0.00,'2026-03-24 10:13:25'),(3,'RJones@email.com',3,1,50.00,'2026-03-31 14:54:54'),(4,'RJones@email.com',5,1,36.00,'2026-04-11 15:56:32'),(8,'JamesJ@mail.email',8,6,30.00,'2026-04-12 10:50:21'),(9,'JessicaA@inbox.email',11,3,180.00,'2026-04-21 09:34:17'),(10,'JessicaA@inbox.email',6,1,0.00,'2026-04-21 14:42:55');
/*!40000 ALTER TABLE `bookings` ENABLE KEYS */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-22 13:24:55

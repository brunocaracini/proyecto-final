-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: sql10.freemysqlhosting.net    Database: sql10404333
-- ------------------------------------------------------
-- Server version	5.5.62-0ubuntu0.14.04.1

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
-- Table structure for table `datosEcoPuntos`
--

DROP TABLE IF EXISTS `datosEcoPuntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datosEcoPuntos` (
  `idValorVenc` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `valor` float DEFAULT NULL,
  `porc_rec_EP` float DEFAULT NULL,
  PRIMARY KEY (`idValorVenc`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datosEcoPuntos`
--

LOCK TABLES `datosEcoPuntos` WRITE;
/*!40000 ALTER TABLE `datosEcoPuntos` DISABLE KEYS */;
INSERT INTO `datosEcoPuntos` VALUES (1,'2017-11-09 00:00:00',3,0.5),(2,'2020-10-09 00:00:00',7,0.3),(3,'2021-04-19 00:17:26',3,0.4),(4,'2021-04-19 00:19:10',5,0.4);
/*!40000 ALTER TABLE `datosEcoPuntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `depositos`
--

DROP TABLE IF EXISTS `depositos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `depositos` (
  `idDeposito` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(100) DEFAULT NULL,
  `cant` float DEFAULT NULL,
  `fechaReg` datetime DEFAULT NULL,
  `fechaDep` datetime DEFAULT NULL,
  `idMaterial` int(11) NOT NULL,
  `idUsuario` int(11) DEFAULT NULL,
  `idPunto` int(11) NOT NULL,
  `idEcoPuntos` int(11) DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  PRIMARY KEY (`idDeposito`),
  KEY `idMaterial_idx` (`idMaterial`),
  KEY `idUsuario_idx` (`idUsuario`),
  KEY `idEcoPuntos_idx` (`idEcoPuntos`),
  KEY `idPunto_idx` (`idPunto`),
  CONSTRAINT `idEcoPuntos` FOREIGN KEY (`idEcoPuntos`) REFERENCES `ecoPuntos` (`idEcoPuntos`) ON DELETE SET NULL ON UPDATE NO ACTION,
  CONSTRAINT `idMaterial` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idPunto` FOREIGN KEY (`idPunto`) REFERENCES `puntosDeposito` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idUsuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `depositos`
--

LOCK TABLES `depositos` WRITE;
/*!40000 ALTER TABLE `depositos` DISABLE KEYS */;
INSERT INTO `depositos` VALUES (22,'66001b25980b0a24',2,'2020-01-19 18:26:14','2020-01-19 17:52:11',26,5,43,72,'acreditado'),(23,'6776d8cf866902e7',5,'2020-01-19 18:28:05','2020-01-19 18:27:54',27,5,33,73,'acreditado'),(24,'fbc48e02dbaf38ea',1800,'2020-01-19 18:38:51','2020-01-19 18:38:41',28,8,37,74,'acreditado'),(25,'c5a6007820f179a1',4,NULL,'2020-01-19 18:39:23',27,NULL,42,75,'no acreditado'),(26,'8c4bacf02dcfbdd7',1900,NULL,'2020-02-19 19:02:23',28,NULL,37,76,'no acreditado'),(27,'2a177509a2f69d2b',3,NULL,'2020-02-19 19:02:23',24,NULL,33,77,'no acreditado'),(28,'6cbda39e97d8d0af',4,'2021-04-20 00:09:41','2020-02-19 19:02:23',26,8,43,78,'acreditado'),(29,'aa6acec24123406e',4,'2020-02-19 19:02:23','2020-02-19 19:02:23',24,5,37,79,'acreditado'),(30,'6bbaf09d5104752b',5,'2020-03-19 19:31:11','2020-03-19 19:31:11',25,5,42,80,'acreditado'),(31,'19c7e70b851165ed',6,'2021-04-20 00:09:12','2020-05-19 21:32:28',26,5,43,81,'acreditado'),(32,'98caff922fa4477a',5,NULL,'2020-05-19 21:32:28',26,NULL,43,82,'no acreditado'),(33,'40588d2a3c590d9b',12,NULL,'2020-05-19 21:32:28',24,NULL,42,83,'no acreditado'),(34,'eaa5beea6a88f799',1200,'2021-04-20 00:09:20','2020-05-19 21:32:28',28,5,37,84,'acreditado'),(35,'f7380143a256be4a',6,NULL,'2020-06-19 21:43:25',24,NULL,37,85,'no acreditado'),(36,'dc053532bee5cdf3',4,NULL,'2020-06-19 21:43:25',27,NULL,33,86,'no acreditado'),(37,'03d1edd11d5448c7',10,'2021-04-20 00:09:34','2020-06-19 21:43:25',25,8,42,87,'acreditado'),(38,'880a50242535f41c',5,'2021-04-20 16:53:32','2020-07-19 23:55:18',26,5,43,88,'acreditado'),(39,'3288eb8df0d53388',2000,NULL,'2020-07-19 23:55:18',28,NULL,37,89,'no acreditado'),(40,'54379c606bf82a7a',2,'2021-04-20 16:53:55','2020-07-19 23:55:18',27,5,33,90,'acreditado'),(41,'35903594cde4b86d',6,'2021-04-20 16:55:20','2020-08-20 00:13:24',24,5,37,91,'acreditado'),(42,'66dcf308975316b6',5,NULL,'2020-09-20 00:29:45',26,NULL,43,92,'no acreditado'),(43,'b1fdc59dda8d822c',3,NULL,'2020-09-20 00:29:45',25,NULL,43,93,'no acreditado'),(44,'7d650e0e7453b38b',4,NULL,'2020-09-20 00:29:45',27,NULL,42,94,'no acreditado'),(45,'d2257321a30334b3',5,'2021-04-20 16:54:48','2020-11-20 01:02:19',24,5,33,95,'acreditado'),(46,'1f2812115f3c8798',4,NULL,'2020-11-20 01:02:19',24,NULL,37,96,'no acreditado'),(47,'67e04d3120bb20ae',2,'2021-04-20 16:53:12','2020-12-20 01:09:42',24,5,42,97,'acreditado'),(48,'3bb01a83a23f6592',4,'2021-04-20 16:54:59','2020-12-20 01:09:42',26,5,33,98,'acreditado'),(49,'fa460067d6d00635',2,'2021-04-20 16:53:20','2021-01-20 01:32:40',26,5,37,99,'acreditado'),(50,'5f41548d450cccd2',500,NULL,'2021-02-20 15:52:19',28,NULL,37,100,'no acreditado'),(51,'a895a50caf45219e',6,NULL,'2021-03-20 16:35:30',24,NULL,37,101,'no acreditado'),(52,'4cb73023c876f436',4,NULL,'2021-04-20 16:50:22',26,NULL,37,102,'no acreditado'),(53,'efc5a39152b559bd',20,'2021-04-26 19:14:12','2021-04-26 19:13:58',26,5,43,103,'acreditado'),(54,'77c7cac3bbab626e',2,NULL,'2021-04-26 19:44:40',26,NULL,37,104,'no acreditado');
/*!40000 ALTER TABLE `depositos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `direcciones`
--

DROP TABLE IF EXISTS `direcciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `direcciones` (
  `idDireccion` int(11) NOT NULL AUTO_INCREMENT,
  `calle` varchar(60) DEFAULT NULL,
  `altura` int(11) DEFAULT NULL,
  `ciudad` varchar(45) DEFAULT NULL,
  `provincia` varchar(45) DEFAULT NULL,
  `pais` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idDireccion`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `direcciones`
--

LOCK TABLES `direcciones` WRITE;
/*!40000 ALTER TABLE `direcciones` DISABLE KEYS */;
INSERT INTO `direcciones` VALUES (33,'San Juan',723,'Rosario','Santa Fe','Argentina'),(37,'Callao',1255,'Rosario','Santa Fe','Argentina'),(42,'Moreno',2047,'Rosario','Santa Fe','Argentina'),(43,'9 de Julio',1000,'Carcarañá','Santa Fe','Argentina'),(44,'Oroño',1300,'Rosario','Santa Fe','Argentina'),(45,'9 de Julio',1000,'Rosario','Santa Fe','Argentina'),(47,'Zeballos',1341,'Rosario','Santa Fe','Argentina'),(48,'Pellegrini',250,'Rosario','Santa Fe','Argentina'),(49,'Cafferata ',729,'Rosario','Santa Fe','Argentina'),(50,'Santa Fe',3100,'Rosario','Santa Fe','Argentina'),(51,'Rondeau',2500,'Rosario','Santa Fe','Argentina');
/*!40000 ALTER TABLE `direcciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecoPuntos`
--

DROP TABLE IF EXISTS `ecoPuntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecoPuntos` (
  `idEcoPuntos` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad` float NOT NULL,
  `cantidadRestante` float NOT NULL,
  PRIMARY KEY (`idEcoPuntos`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecoPuntos`
--

LOCK TABLES `ecoPuntos` WRITE;
/*!40000 ALTER TABLE `ecoPuntos` DISABLE KEYS */;
INSERT INTO `ecoPuntos` VALUES (72,320,0),(73,250,0),(74,1800,0),(75,200,200),(76,1900,1900),(77,600,600),(78,640,337),(79,800,0),(80,1500,0),(81,960,0),(82,800,800),(83,2400,2400),(84,1200,0),(85,1200,1200),(86,200,200),(87,3000,3000),(88,800,0),(89,2000,2000),(90,100,0),(91,1200,0),(92,800,800),(93,900,900),(94,200,200),(95,1000,356),(96,800,800),(97,400,400),(98,640,640),(99,320,0),(100,500,500),(101,1200,1200),(102,640,640),(103,3200,3200),(104,320,320);
/*!40000 ALTER TABLE `ecoPuntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entidadesDestino`
--

DROP TABLE IF EXISTS `entidadesDestino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entidadesDestino` (
  `idEntidad` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `estado` varchar(45) NOT NULL,
  `descripcion` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`idEntidad`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entidadesDestino`
--

LOCK TABLES `entidadesDestino` WRITE;
/*!40000 ALTER TABLE `entidadesDestino` DISABLE KEYS */;
INSERT INTO `entidadesDestino` VALUES (3,'IMACO SRL','disponible','Imaco SRL - Fábrica de tapas plásticas, Rosario.'),(4,'Amoplast','disponible','Amoplast produce bidones, botellas, potes, goteros, frascos de boca ancha,  tapas inviolables y a rosca, en  diversos materiales como ser: PET, PEAD, PEBD y PVC.');
/*!40000 ALTER TABLE `entidadesDestino` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entradasMat`
--

DROP TABLE IF EXISTS `entradasMat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entradasMat` (
  `idEntradaMat` int(11) NOT NULL AUTO_INCREMENT,
  `idMaterial` int(11) NOT NULL,
  `cant` float DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `concepto` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`idEntradaMat`),
  KEY `idMaterial-EM_idx` (`idMaterial`),
  CONSTRAINT `idMaterial-EM` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entradasMat`
--

LOCK TABLES `entradasMat` WRITE;
/*!40000 ALTER TABLE `entradasMat` DISABLE KEYS */;
INSERT INTO `entradasMat` VALUES (1,24,10,'2020-01-19','Entrada de Plástico'),(2,25,22,'2020-01-19','Entrada de vidrio'),(3,26,15,'2020-01-19','Entrada de Madera'),(4,28,2000,'2020-02-19','Entrada de Lana'),(5,26,2,'2020-02-19','Madera'),(6,27,5,'2020-02-19','Entrada de Tela'),(7,24,4,'2020-02-19','Plastico\r\n'),(8,25,1,'2020-03-19','Entrada\r\n'),(9,28,2500,'2020-05-20','Entrada'),(10,26,10,'2020-05-20','Entrada'),(11,24,8,'2020-05-20','Entrada'),(12,27,5,'2020-05-20','Entrada'),(13,25,10,'2020-05-20','Entrada'),(14,26,2,'2020-06-20','Entrada'),(15,28,2000,'2020-06-20','Entrada'),(16,26,20,'2020-08-20','Entrada'),(17,25,5,'2020-08-20','Entrada'),(18,26,3,'2021-01-20','Entrada'),(19,24,20,'2021-02-20','Entrada'),(20,28,2200,'2021-03-20','Entrada');
/*!40000 ALTER TABLE `entradasMat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horariosPD`
--

DROP TABLE IF EXISTS `horariosPD`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horariosPD` (
  `idHorario` int(11) NOT NULL AUTO_INCREMENT,
  `idPunto` int(11) NOT NULL,
  `horaDesde` time DEFAULT NULL,
  `horaHasta` time DEFAULT NULL,
  `dia` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`idHorario`,`idPunto`),
  KEY `idPuntoDeposito_idx` (`idPunto`),
  CONSTRAINT `idPuntoDeposito` FOREIGN KEY (`idPunto`) REFERENCES `puntosDeposito` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=211 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horariosPD`
--

LOCK TABLES `horariosPD` WRITE;
/*!40000 ALTER TABLE `horariosPD` DISABLE KEYS */;
INSERT INTO `horariosPD` VALUES (134,33,'08:00:00','20:00:00','Lunes'),(135,33,NULL,NULL,'Martes'),(136,33,'09:00:00','20:00:00','Miércoles'),(137,33,NULL,NULL,'Jueves'),(138,33,'08:00:00','20:00:00','Viernes'),(139,33,'08:00:00','20:00:00','Sábado'),(140,33,'08:00:00','20:00:00','Domingo'),(162,37,'08:00:00','20:00:00','Lunes'),(163,37,'08:00:00','20:00:00','Martes'),(164,37,'08:00:00','20:00:00','Miércoles'),(165,37,'08:00:00','20:00:00','Jueves'),(166,37,'08:00:00','20:00:00','Viernes'),(167,37,'08:00:00','20:00:00','Sábado'),(168,37,'08:00:00','20:00:00','Domingo'),(197,42,'08:00:00','20:00:00','Lunes'),(198,42,'08:00:00','20:00:00','Martes'),(199,42,'08:00:00','20:00:00','Miércoles'),(200,42,'08:00:00','20:00:00','Jueves'),(201,42,'08:00:00','20:00:00','Viernes'),(202,42,'08:00:00','20:00:00','Sábado'),(203,42,'08:00:00','20:00:00','Domingo'),(204,43,NULL,NULL,'Lunes'),(205,43,'08:00:00','20:00:00','Martes'),(206,43,'08:00:00','20:00:00','Miércoles'),(207,43,'08:00:00','20:00:00','Jueves'),(208,43,'08:00:00','20:00:00','Viernes'),(209,43,NULL,NULL,'Sábado'),(210,43,NULL,NULL,'Domingo');
/*!40000 ALTER TABLE `horariosPD` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horariosPR`
--

DROP TABLE IF EXISTS `horariosPR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horariosPR` (
  `idHorario` int(11) NOT NULL AUTO_INCREMENT,
  `idPunto` int(11) NOT NULL,
  `horaDesde` time DEFAULT NULL,
  `horaHasta` time DEFAULT NULL,
  `dia` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`idHorario`,`idPunto`),
  KEY `idPuntoRetiro_idx` (`idPunto`),
  CONSTRAINT `idPuntoRetiro` FOREIGN KEY (`idPunto`) REFERENCES `puntosRetiro` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horariosPR`
--

LOCK TABLES `horariosPR` WRITE;
/*!40000 ALTER TABLE `horariosPR` DISABLE KEYS */;
INSERT INTO `horariosPR` VALUES (8,6,'08:00:00','20:00:00','Lunes'),(9,6,'08:00:00','20:00:00','Martes'),(10,6,'08:00:00','20:00:00','Miércoles'),(11,6,'08:00:00','20:00:00','Jueves'),(12,6,'08:00:00','20:00:00','Viernes'),(13,6,NULL,NULL,'Sábado'),(14,6,NULL,NULL,'Domingo'),(15,7,'08:00:00','20:00:00','Lunes'),(16,7,'08:00:00','20:00:00','Martes'),(17,7,'08:00:00','20:00:00','Miércoles'),(18,7,'08:00:00','20:00:00','Jueves'),(19,7,'08:00:00','20:00:00','Viernes'),(20,7,'08:00:00','20:00:00','Sábado'),(21,7,'08:00:00','20:00:00','Domingo'),(22,8,'08:00:00','20:00:00','Lunes'),(23,8,'08:00:00','20:00:00','Martes'),(24,8,NULL,NULL,'Miércoles'),(25,8,'08:00:00','20:00:00','Jueves'),(26,8,NULL,NULL,'Viernes'),(27,8,'08:00:00','20:00:00','Sábado'),(28,8,NULL,NULL,'Domingo'),(29,9,'09:00:00','20:00:00','Lunes'),(30,9,NULL,NULL,'Martes'),(31,9,'08:00:00','20:00:00','Miércoles'),(32,9,'09:00:00','20:00:00','Jueves'),(33,9,NULL,NULL,'Viernes'),(34,9,'09:00:00','20:00:00','Sábado'),(35,9,'08:00:00','20:00:00','Domingo');
/*!40000 ALTER TABLE `horariosPR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `idInsumo` int(11) NOT NULL AUTO_INCREMENT,
  `stock` float DEFAULT NULL,
  `unidadMedida` varchar(60) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `cProduccion` float DEFAULT NULL,
  `cMateriales` float DEFAULT NULL,
  `cTotal` float DEFAULT NULL,
  `otrosCostos` float DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  `color` varchar(45) DEFAULT '#444444',
  `descripcion` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES (14,2.4,'Kilogramos','Granzas Plástico',20,100,125,5,'disponible','#b01d4e','Granzas producidas con plástico reciclado'),(15,10.2,'Kilogramos','Vidrio Procesado',25,150,183,8,'disponible','#deaed1',''),(16,23,'Metros Cuadrados','Plancha de Melamina',20,160,181,1,'disponible','#4f13f9',''),(17,56,'Metros Cuadrados','Fibra de Vidrio',23,55,89,11,'disponible','#4bbccd',''),(18,3.5,'Unidad','Ovillo de Lana - 10m',20,427.5,479.5,32,'disponible','#9ff7d2','Ovillo de Lana de 10 metros de largo, hecho a partir de lana reciclada y teñida');
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumosUtilizados`
--

DROP TABLE IF EXISTS `insumosUtilizados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumosUtilizados` (
  `idCompUtil` int(11) NOT NULL AUTO_INCREMENT,
  `idInsumo` int(11) NOT NULL,
  `idProd` int(11) NOT NULL,
  `cantidad` float NOT NULL,
  PRIMARY KEY (`idCompUtil`),
  KEY `insumosUtilizados_FK` (`idInsumo`),
  KEY `insumosUtilizados_FK_1` (`idProd`),
  CONSTRAINT `insumosUtilizados_FK` FOREIGN KEY (`idInsumo`) REFERENCES `insumos` (`idInsumo`),
  CONSTRAINT `insumosUtilizados_FK_1` FOREIGN KEY (`idProd`) REFERENCES `prodTipArt` (`idProdTipArt`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumosUtilizados`
--

LOCK TABLES `insumosUtilizados` WRITE;
/*!40000 ALTER TABLE `insumosUtilizados` DISABLE KEYS */;
INSERT INTO `insumosUtilizados` VALUES (5,18,8,1),(6,15,9,3.6),(7,14,10,3.6),(8,14,11,3),(9,16,11,1),(10,14,12,3),(11,16,12,1),(12,18,13,0.5),(13,15,14,0.4),(14,14,15,0.4),(15,18,16,0.5),(16,14,17,6),(17,16,17,2),(18,18,18,1),(19,14,19,0.8),(20,14,20,3),(21,16,20,1),(22,18,21,0.5),(23,18,22,0.5),(24,15,23,0.6),(25,14,24,0.8),(26,18,25,0.5),(27,15,26,0.8),(28,14,27,6),(29,16,27,2),(30,14,28,1.2),(31,18,29,4.5),(32,15,30,2.8),(33,14,31,0.8),(34,14,32,6),(35,16,32,2),(36,18,33,0.5),(37,15,34,0.4),(38,14,35,0.8),(39,18,36,0.5),(40,14,37,0.4),(41,14,38,18),(42,16,38,6),(43,18,39,3),(44,15,40,20),(45,14,41,2.8),(46,18,42,1),(47,14,43,3),(48,16,43,1),(49,15,44,0.2),(50,18,45,0.5),(51,14,46,4);
/*!40000 ALTER TABLE `insumosUtilizados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mat_ins`
--

DROP TABLE IF EXISTS `mat_ins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mat_ins` (
  `idMaterial` int(11) NOT NULL,
  `idInsumo` int(11) NOT NULL,
  `cantidad` float DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  PRIMARY KEY (`idMaterial`,`idInsumo`),
  KEY `fk_mat_ins_2_idx` (`idInsumo`),
  CONSTRAINT `fk_mat_ins_1` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `fk_mat_ins_2` FOREIGN KEY (`idInsumo`) REFERENCES `insumos` (`idInsumo`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mat_ins`
--

LOCK TABLES `mat_ins` WRITE;
/*!40000 ALTER TABLE `mat_ins` DISABLE KEYS */;
INSERT INTO `mat_ins` VALUES (24,14,1,'disponible'),(24,17,0.1,'disponible'),(25,15,1,'disponible'),(25,17,0.3,'disponible'),(26,16,2,'disponible'),(28,18,855,'disponible');
/*!40000 ALTER TABLE `mat_ins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materiales`
--

DROP TABLE IF EXISTS `materiales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materiales` (
  `idMaterial` int(11) NOT NULL AUTO_INCREMENT,
  `stock` float DEFAULT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  `unidadMedida` varchar(60) DEFAULT NULL,
  `costoRecoleccion` float DEFAULT NULL,
  `color` varchar(45) DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  `descripcion` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`idMaterial`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materiales`
--

LOCK TABLES `materiales` WRITE;
/*!40000 ALTER TABLE `materiales` DISABLE KEYS */;
INSERT INTO `materiales` VALUES (24,18.4,'Plástico','Kilogramos',100,'#ebe15b','habilitado','Plástico obtenido de objetos diarios depositados por usuarios.'),(25,0.2,'Vidrio','Kilogramos',150,'#28cc66','habilitado','Vidrio obtenido de botellas y envases reciclados'),(26,33,'Madera','Metros Cuadrados',80,'#bbdcd9','habilitado',''),(27,29,'Tela','Metros Cuadrados',25,'#bb0659','habilitado',''),(28,710,'Lana','Gramos',0.5,'#9d726e','habilitado','');
/*!40000 ALTER TABLE `materiales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materialesUtilizados`
--

DROP TABLE IF EXISTS `materialesUtilizados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materialesUtilizados` (
  `idCompUtil` int(11) NOT NULL AUTO_INCREMENT,
  `idProd` int(11) NOT NULL,
  `idMaterial` int(11) NOT NULL,
  `cantidad` float NOT NULL,
  PRIMARY KEY (`idCompUtil`),
  KEY `materialesUtilizados_FK` (`idMaterial`),
  KEY `materialesUtilizados_FK_1` (`idProd`),
  CONSTRAINT `materialesUtilizados_FK` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`),
  CONSTRAINT `materialesUtilizados_FK_1` FOREIGN KEY (`idProd`) REFERENCES `prodInsumos` (`idprodInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materialesUtilizados`
--

LOCK TABLES `materialesUtilizados` WRITE;
/*!40000 ALTER TABLE `materialesUtilizados` DISABLE KEYS */;
INSERT INTO `materialesUtilizados` VALUES (9,15,24,5),(10,16,25,10),(11,17,26,12),(12,18,24,1),(13,18,25,3),(14,19,28,1710),(15,20,24,3),(16,21,24,4),(17,22,25,1),(18,23,26,6),(19,24,24,0.6),(20,24,25,1.8),(21,25,28,855),(22,26,24,2),(23,27,28,1710),(24,28,24,3),(25,29,25,6),(26,30,26,4),(27,31,24,0.4),(28,31,25,1.2),(29,32,28,855),(30,33,24,4),(31,34,25,6),(32,35,26,6),(33,36,24,2.1),(34,36,25,6.3),(35,37,28,1710),(36,38,24,8),(37,39,25,8),(38,40,26,8),(39,41,24,1.2),(40,41,25,3.6),(41,42,28,3420),(42,43,24,1),(43,44,26,4),(44,45,26,18),(45,46,25,5),(46,47,28,2565),(47,48,24,2),(48,49,26,4),(49,50,24,18),(50,51,25,3),(51,52,26,14),(52,53,24,0.3),(53,53,25,0.9),(54,54,24,4),(55,55,26,2),(56,56,24,12),(57,57,28,2565);
/*!40000 ALTER TABLE `materialesUtilizados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modulos`
--

DROP TABLE IF EXISTS `modulos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `modulos` (
  `idModulo` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idModulo`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modulos`
--

LOCK TABLES `modulos` WRITE;
/*!40000 ALTER TABLE `modulos` DISABLE KEYS */;
INSERT INTO `modulos` VALUES (1,'Gestión de Insumos'),(2,'Gestión de Artículos'),(3,'Gestión de Niveles'),(4,'Gestión de Usuarios'),(5,'Gestión de Producción'),(6,'Gestión de Entidades'),(7,'Gestión de Puntos de Retiro'),(8,'Gestión de Pedidos - Depósito Central'),(9,'Gestión de Depósitos'),(10,'Gestión de Permisos'),(11,'Gestión de Stock'),(12,'Gestión de Pedidos - Puntos de Retiro'),(13,'Configuración'),(14,'Reportes'),(15,'Gestión de Puntos de Depósito'),(16,'Gestión de Materiales');
/*!40000 ALTER TABLE `modulos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `niveles`
--

DROP TABLE IF EXISTS `niveles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `niveles` (
  `idNivel` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` int(11) DEFAULT NULL,
  `minEcoPuntos` float DEFAULT NULL,
  `maxEcoPuntos` float DEFAULT NULL,
  `descuento` float DEFAULT NULL,
  PRIMARY KEY (`idNivel`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `niveles`
--

LOCK TABLES `niveles` WRITE;
/*!40000 ALTER TABLE `niveles` DISABLE KEYS */;
INSERT INTO `niveles` VALUES (1,1,0,1000,2.5),(11,2,1001,2000,5),(12,3,2001,3000,7.5),(14,4,3001,4000,10),(15,5,4001,5000,12.5);
/*!40000 ALTER TABLE `niveles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `idPedido` int(11) NOT NULL AUTO_INCREMENT,
  `fechaEnc` datetime DEFAULT NULL,
  `fechaRet` datetime DEFAULT NULL,
  `totalEP` float DEFAULT NULL,
  `totalARS` float DEFAULT NULL,
  `estado` varchar(100) DEFAULT 'disponible',
  `idPunto` int(11) DEFAULT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idPedido`),
  KEY `idUsuario_idx` (`idUsuario`),
  KEY `idPuntoPedido_idx` (`idPunto`),
  CONSTRAINT `idPuntoPedido` FOREIGN KEY (`idPunto`) REFERENCES `puntosRetiro` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idUsuarioPedido` FOREIGN KEY (`idUsuario`) REFERENCES `usuarios` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (25,'2020-01-19 18:43:29','2020-01-23 18:43:29',911,341.23,'retirado',9,8),(26,'2020-01-19 18:43:29','2020-01-23 18:43:29',570,104.56,'retirado',8,5),(27,'2020-02-22 19:09:43','2020-02-22 19:09:43',523,0,'retirado',8,5),(28,'2020-02-22 19:09:43','2020-02-22 19:09:43',523,0,'retirado',6,8),(29,'2020-03-19 19:46:33','2020-03-21 19:46:33',1777,283.56,'retirado',9,5),(30,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,437.03,'retirado',9,5),(31,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,209.35,'retirado',6,5),(32,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,848.25,'retirado',9,5),(33,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,596.12,'retirado',7,5),(34,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,218.52,'retirado',8,5),(35,'2020-04-19 20:35:17','2020-04-21 20:35:17',0,209.35,'retirado',7,5),(36,'2020-05-19 21:37:26','2020-05-22 22:37:26',0,848.25,'devuelto',6,5),(37,'2020-05-19 21:37:26','2020-05-22 21:37:26',0,109.26,'retirado',9,5),(38,'2020-06-19 21:44:04','2020-06-21 21:44:04',366,329.55,'retirado',9,8),(39,'2020-08-20 00:12:32','2020-08-21 00:12:32',1414,0,'retirado',6,5),(40,'2020-08-20 00:12:32','2020-08-21 00:12:32',523,0,'retirado',7,5),(41,'2020-09-21 00:12:32','2020-09-21 00:12:32',223,803.65,'retirado',9,5),(42,'2020-09-21 00:12:32','2020-09-21 00:12:32',0,209.35,'listo',9,5),(43,'2020-10-20 00:38:19','2020-10-22 00:38:19',0,2070.2,'retirado',9,5),(44,'2020-11-20 00:38:19','2020-11-24 01:02:05',0,1247.08,'cancelado',7,5),(45,'2020-11-20 00:38:19','2020-11-24 01:02:05',0,104.68,'retirado',7,5),(46,'2020-12-20 01:11:36','2020-12-24 01:02:05',0,213.93,'retirado',6,5),(47,'2021-01-20 01:30:56','2021-01-24 01:30:56',0,848.25,'retirado',7,5),(48,'2021-01-20 01:30:56','2021-01-24 01:30:56',0,327.78,'retirado',7,5),(49,'2021-01-20 01:30:56','2021-01-24 01:30:56',0,314.03,'retirado',8,5),(50,'2021-02-20 15:52:00','2021-02-24 15:52:00',0,104.68,'retirado',7,5),(51,'2021-03-20 16:31:36','2021-03-21 16:31:36',0,1994.56,'preparado',6,5),(52,'2021-03-20 16:32:04','2021-03-23 16:32:04',0,327.78,'retirado',8,5),(53,'2021-04-20 16:50:59','2021-04-22 16:50:59',0,848.25,'preparado',9,5),(54,'2021-04-20 16:51:09','2021-04-24 16:51:09',0,218.52,'retirado',7,5),(55,'2021-04-20 16:51:20','2021-04-21 16:51:20',0,104.68,'preparado',6,5),(56,'2021-04-20 16:55:37','2021-04-21 16:55:37',1166,528.03,'pendiente',6,5),(57,'2021-04-20 16:55:57','2021-04-24 16:55:57',374,200.35,'pendiente',7,5),(58,'2021-04-20 16:56:09','2021-04-24 16:56:09',992,0.2,'listo',7,5),(59,'2021-04-21 01:09:31','2021-04-22 01:09:31',303,40.22,'pendiente',6,8),(60,'2021-04-26 17:01:54','2021-04-30 17:01:54',532,0,'pendiente',7,5);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permisosAcceso`
--

DROP TABLE IF EXISTS `permisosAcceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `permisosAcceso` (
  `idTipoUsuario` int(11) NOT NULL,
  `idModulo` int(11) NOT NULL,
  KEY `idModulo_idx` (`idModulo`),
  KEY `idTipoUsuarioPA_idx` (`idTipoUsuario`),
  CONSTRAINT `idModulo` FOREIGN KEY (`idModulo`) REFERENCES `modulos` (`idModulo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoUsuarioPA` FOREIGN KEY (`idTipoUsuario`) REFERENCES `tiposUsuario` (`idTipoUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permisosAcceso`
--

LOCK TABLES `permisosAcceso` WRITE;
/*!40000 ALTER TABLE `permisosAcceso` DISABLE KEYS */;
INSERT INTO `permisosAcceso` VALUES (2,9),(2,8),(2,5),(2,4),(2,2),(2,10),(2,1),(2,3),(5,9),(5,8),(6,6),(2,6),(2,7),(2,11),(2,13),(2,12),(2,15),(2,14),(2,16),(6,16),(10,5),(10,2);
/*!40000 ALTER TABLE `permisosAcceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prodInsumos`
--

DROP TABLE IF EXISTS `prodInsumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prodInsumos` (
  `idprodInsumo` int(11) NOT NULL AUTO_INCREMENT,
  `idInsumo` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad` float DEFAULT NULL,
  `estado` varchar(50) DEFAULT 'disponible',
  PRIMARY KEY (`idprodInsumo`),
  KEY `idIns_idx` (`idInsumo`),
  CONSTRAINT `prodInsumos_FK` FOREIGN KEY (`idInsumo`) REFERENCES `insumos` (`idInsumo`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prodInsumos`
--

LOCK TABLES `prodInsumos` WRITE;
/*!40000 ALTER TABLE `prodInsumos` DISABLE KEYS */;
INSERT INTO `prodInsumos` VALUES (15,14,'2020-01-19',5,'disponible'),(16,15,'2020-01-19',10,'disponible'),(17,16,'2020-01-19',6,'disponible'),(18,17,'2020-01-19',10,'disponible'),(19,18,'2020-01-19',2,'disponible'),(20,14,'2020-01-19',3,'disponible'),(21,14,'2020-02-19',4,'disponible'),(22,15,'2020-02-19',1,'disponible'),(23,16,'2020-02-19',3,'disponible'),(24,17,'2020-02-19',6,'disponible'),(25,18,'2020-02-19',1,'disponible'),(26,14,'2020-03-19',2,'disponible'),(27,18,'2020-03-19',2,'disponible'),(28,14,'2020-04-19',3,'disponible'),(29,15,'2020-04-19',6,'disponible'),(30,16,'2020-04-19',2,'disponible'),(31,17,'2020-04-19',4,'disponible'),(32,18,'2020-04-19',1,'disponible'),(33,14,'2020-05-19',4,'disponible'),(34,15,'2020-05-19',6,'disponible'),(35,16,'2020-05-19',3,'disponible'),(36,17,'2020-05-19',21,'disponible'),(37,18,'2020-05-19',2,'disponible'),(38,14,'2020-06-19',8,'disponible'),(39,15,'2020-06-19',8,'disponible'),(40,16,'2020-06-19',4,'disponible'),(41,17,'2020-06-19',12,'disponible'),(42,18,'2020-06-19',4,'disponible'),(43,14,'2020-07-20',1,'disponible'),(44,16,'2020-07-20',2,'disponible'),(45,16,'2020-09-20',9,'disponible'),(46,15,'2020-09-20',5,'disponible'),(47,18,'2020-09-20',3,'disponible'),(48,14,'2020-11-20',2,'disponible'),(49,16,'2020-11-20',2,'disponible'),(50,14,'2020-12-20',18,'disponible'),(51,15,'2020-12-20',3,'disponible'),(52,16,'2020-12-20',7,'disponible'),(53,17,'2020-12-20',3,'disponible'),(54,14,'2021-01-20',4,'disponible'),(55,16,'2021-01-20',1,'disponible'),(56,14,'2021-03-20',12,'disponible'),(57,18,'2021-04-20',3,'disponible');
/*!40000 ALTER TABLE `prodInsumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prodTipArt`
--

DROP TABLE IF EXISTS `prodTipArt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prodTipArt` (
  `idProdTipArt` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoArticulo` int(11) NOT NULL,
  `fecha` date DEFAULT NULL,
  `cantidad` float DEFAULT NULL,
  `estado` varchar(50) DEFAULT 'disponible',
  PRIMARY KEY (`idProdTipArt`),
  KEY `idTipArt_idx` (`idTipoArticulo`),
  CONSTRAINT `idTipArt` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prodTipArt`
--

LOCK TABLES `prodTipArt` WRITE;
/*!40000 ALTER TABLE `prodTipArt` DISABLE KEYS */;
INSERT INTO `prodTipArt` VALUES (8,32,'2020-01-19',2,'disponible'),(9,33,'2020-01-19',18,'disponible'),(10,34,'2020-01-19',9,'disponible'),(11,31,'2020-01-19',1,'disponible'),(12,31,'2020-02-19',1,'disponible'),(13,32,'2020-02-19',1,'disponible'),(14,33,'2020-02-19',2,'disponible'),(15,34,'2020-02-19',1,'disponible'),(16,32,'2020-03-19',1,'disponible'),(17,31,'2020-04-19',2,'disponible'),(18,32,'2020-04-19',2,'disponible'),(19,34,'2020-04-19',2,'disponible'),(20,31,'2020-05-19',1,'disponible'),(21,32,'2020-05-19',1,'disponible'),(22,32,'2020-05-19',1,'disponible'),(23,33,'2020-05-19',3,'disponible'),(24,34,'2020-05-19',2,'disponible'),(25,32,'2020-06-19',1,'disponible'),(26,33,'2020-06-19',4,'disponible'),(27,31,'2020-07-19',2,'disponible'),(28,34,'2020-07-19',3,'disponible'),(29,32,'2020-10-20',9,'disponible'),(30,33,'2020-10-20',14,'disponible'),(31,34,'2020-10-20',2,'disponible'),(32,31,'2020-12-20',2,'disponible'),(33,32,'2020-12-20',1,'disponible'),(34,33,'2020-12-20',2,'disponible'),(35,34,'2020-12-20',2,'disponible'),(36,32,'2021-01-20',1,'disponible'),(37,34,'2021-01-20',1,'disponible'),(38,31,'2021-02-20',6,'disponible'),(39,32,'2021-02-20',6,'disponible'),(40,33,'2021-02-20',100,'disponible'),(41,34,'2021-03-20',7,'disponible'),(42,32,'2021-04-20',2,'disponible'),(43,31,'2021-04-21',1,'disponible'),(44,33,'2021-04-21',1,'disponible'),(45,32,'2021-04-21',1,'disponible'),(46,35,'2021-04-21',2,'disponible');
/*!40000 ALTER TABLE `prodTipArt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntosDep_mat`
--

DROP TABLE IF EXISTS `puntosDep_mat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntosDep_mat` (
  `idDepMat` int(11) NOT NULL AUTO_INCREMENT,
  `idMaterial` int(11) NOT NULL,
  `idPunto` int(11) NOT NULL,
  `estado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idDepMat`,`idMaterial`,`idPunto`),
  KEY `idPuntoDM_idx` (`idPunto`),
  KEY `idMaterialDM` (`idMaterial`),
  CONSTRAINT `idMaterialDM` FOREIGN KEY (`idMaterial`) REFERENCES `materiales` (`idMaterial`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idPuntoDM` FOREIGN KEY (`idPunto`) REFERENCES `puntosDeposito` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntosDep_mat`
--

LOCK TABLES `puntosDep_mat` WRITE;
/*!40000 ALTER TABLE `puntosDep_mat` DISABLE KEYS */;
INSERT INTO `puntosDep_mat` VALUES (89,24,37,'disponible'),(90,26,37,'disponible'),(91,28,37,'disponible'),(92,24,42,'disponible'),(93,25,42,'disponible'),(94,27,42,'disponible'),(95,24,33,'disponible'),(96,26,33,'disponible'),(97,27,33,'disponible'),(98,26,43,'disponible'),(99,25,43,'disponible');
/*!40000 ALTER TABLE `puntosDep_mat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntosDeposito`
--

DROP TABLE IF EXISTS `puntosDeposito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntosDeposito` (
  `idPunto` int(11) NOT NULL AUTO_INCREMENT,
  `estado` tinyint(4) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `estadoEliminacion` varchar(45) DEFAULT NULL,
  `idDireccion` int(11) DEFAULT NULL,
  PRIMARY KEY (`idPunto`),
  KEY `idDireccionPD_idx` (`idDireccion`),
  CONSTRAINT `idDireccionPD` FOREIGN KEY (`idDireccion`) REFERENCES `direcciones` (`idDireccion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntosDeposito`
--

LOCK TABLES `puntosDeposito` WRITE;
/*!40000 ALTER TABLE `puntosDeposito` DISABLE KEYS */;
INSERT INTO `puntosDeposito` VALUES (33,1,'Zona Sur','disponible',33),(37,1,'Barrio Lourdes','disponible',37),(42,1,'Barrio Parque','disponible',43),(43,1,'Alberdi','disponible',51);
/*!40000 ALTER TABLE `puntosDeposito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `puntosRetiro`
--

DROP TABLE IF EXISTS `puntosRetiro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `puntosRetiro` (
  `idPunto` int(11) NOT NULL AUTO_INCREMENT,
  `estado` varchar(100) DEFAULT NULL,
  `demoraFija` int(11) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `idDireccion` int(11) DEFAULT NULL,
  `estadoEliminacion` varchar(45) DEFAULT '0',
  PRIMARY KEY (`idPunto`),
  KEY `idDireccionPR_idx` (`idDireccion`),
  CONSTRAINT `idDireccionPR` FOREIGN KEY (`idDireccion`) REFERENCES `direcciones` (`idDireccion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `puntosRetiro`
--

LOCK TABLES `puntosRetiro` WRITE;
/*!40000 ALTER TABLE `puntosRetiro` DISABLE KEYS */;
INSERT INTO `puntosRetiro` VALUES (6,'1',1,'UTN - FRRo',47,'disponible'),(7,'1',4,'UNR - FCEIA',48,'disponible'),(8,'1',3,'Mercado del Patio',49,'disponible'),(9,'1',2,'UNR - FCM',50,'disponible');
/*!40000 ALTER TABLE `puntosRetiro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salidasMun`
--

DROP TABLE IF EXISTS `salidasMun`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salidasMun` (
  `idSalidaMun` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoArticulo` int(11) NOT NULL,
  `cantSalida` float DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `concepto` varchar(200) DEFAULT NULL,
  `costo` float DEFAULT NULL,
  `costoObtencionAlt` float DEFAULT NULL,
  PRIMARY KEY (`idSalidaMun`),
  KEY `idTipoArt-SM_idx` (`idTipoArticulo`),
  CONSTRAINT `idTipoArt-SM` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salidasMun`
--

LOCK TABLES `salidasMun` WRITE;
/*!40000 ALTER TABLE `salidasMun` DISABLE KEYS */;
INSERT INTO `salidasMun` VALUES (2,34,1,'2020-02-19','Salida',88,150),(3,33,6,'2020-04-20','Salida floreros',579.6,1200),(4,33,2,'2020-06-19','Salida',193.2,400),(5,31,1,'2020-08-20','Salida',696,1200),(6,31,1,'2020-09-20','Salida',696,1200),(7,32,1,'2020-07-20','Salida',254.75,650),(8,32,2,'2020-10-20','Salida',509.5,1300),(9,34,1,'2021-01-20','Salida',88,150),(10,33,100,'2021-02-20','Salida',9660,20000),(11,32,6,'2021-02-20','Salida',1528.5,3900),(12,33,2,'2021-03-20','Salida',193.2,400);
/*!40000 ALTER TABLE `salidasMun` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `salidasStock`
--

DROP TABLE IF EXISTS `salidasStock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salidasStock` (
  `idSalida` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoArticulo` int(11) NOT NULL,
  `idEntidad` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `cantidadSalida` float NOT NULL,
  `valorTotal` float NOT NULL,
  `concepto` varchar(200) DEFAULT NULL,
  `costo` float DEFAULT NULL,
  PRIMARY KEY (`idSalida`,`idTipoArticulo`,`idEntidad`),
  KEY `idEntidadST_idx` (`idEntidad`),
  KEY `idTipoArticuloST_idx` (`idTipoArticulo`),
  CONSTRAINT `idTipoArticuloST` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `salidasStock`
--

LOCK TABLES `salidasStock` WRITE;
/*!40000 ALTER TABLE `salidasStock` DISABLE KEYS */;
INSERT INTO `salidasStock` VALUES (3,34,4,'2020-01-19',2,214.72,'Salida de comederos a Amoplast',176),(4,33,3,'2020-02-19',3,336.18,'Salida',289.8),(5,33,4,'2020-08-20',2,224.12,'Salida',193.2),(6,33,3,'2020-11-20',4,448.24,'Salida',386.4),(7,32,3,'2020-12-20',2,611.4,'Salida',509.5),(8,33,4,'2021-01-20',2,224.12,'Salida',193.2),(9,31,3,'2021-02-20',4,3878,'Salida',2784),(10,32,3,'2021-03-20',3,917.4,'Salida',764.25),(11,34,4,'2021-04-20',2,300.72,'Salida',176);
/*!40000 ALTER TABLE `salidasStock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stockPuntosRetiro`
--

DROP TABLE IF EXISTS `stockPuntosRetiro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stockPuntosRetiro` (
  `idPunto` int(11) NOT NULL,
  `idTipoArticulo` int(11) NOT NULL,
  `stock` float NOT NULL,
  KEY `idPuntoSPR_idx` (`idPunto`),
  KEY `idTipoArticuloSPR_idx` (`idTipoArticulo`),
  CONSTRAINT `idPuntoSPR` FOREIGN KEY (`idPunto`) REFERENCES `puntosRetiro` (`idPunto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoArticuloSPR` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stockPuntosRetiro`
--

LOCK TABLES `stockPuntosRetiro` WRITE;
/*!40000 ALTER TABLE `stockPuntosRetiro` DISABLE KEYS */;
/*!40000 ALTER TABLE `stockPuntosRetiro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposArt_ins`
--

DROP TABLE IF EXISTS `tiposArt_ins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposArt_ins` (
  `idTipoArticulo` int(11) NOT NULL,
  `idInsumo` int(11) NOT NULL,
  `cantidad` float DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  PRIMARY KEY (`idTipoArticulo`,`idInsumo`),
  KEY `idInsumo_idx` (`idInsumo`),
  CONSTRAINT `idInsumo` FOREIGN KEY (`idInsumo`) REFERENCES `insumos` (`idInsumo`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoArt` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposArt_ins`
--

LOCK TABLES `tiposArt_ins` WRITE;
/*!40000 ALTER TABLE `tiposArt_ins` DISABLE KEYS */;
INSERT INTO `tiposArt_ins` VALUES (31,14,3,'disponible'),(31,16,1,'disponible'),(32,18,0.5,'disponible'),(33,15,0.2,'disponible'),(34,14,0.4,'disponible'),(35,14,2,'disponible'),(36,14,1,'disponible'),(36,15,1,'disponible'),(36,17,1,'disponible'),(37,14,1,'disponible'),(37,15,1,'disponible'),(37,16,1,'disponible'),(38,14,1,'disponible'),(38,15,1,'disponible');
/*!40000 ALTER TABLE `tiposArt_ins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposArt_pedidos`
--

DROP TABLE IF EXISTS `tiposArt_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposArt_pedidos` (
  `idTipoArticulo` int(11) NOT NULL,
  `idPedido` int(11) NOT NULL,
  `cantidad` float DEFAULT NULL,
  `margenGanancia` float NOT NULL,
  PRIMARY KEY (`idTipoArticulo`,`idPedido`),
  KEY `idPedidoPed_idx` (`idPedido`),
  CONSTRAINT `idPedidoPed` FOREIGN KEY (`idPedido`) REFERENCES `pedidos` (`idPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoArtPed` FOREIGN KEY (`idTipoArticulo`) REFERENCES `tiposArticulo` (`idTipoArticulo`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposArt_pedidos`
--

LOCK TABLES `tiposArt_pedidos` WRITE;
/*!40000 ALTER TABLE `tiposArt_pedidos` DISABLE KEYS */;
INSERT INTO `tiposArt_pedidos` VALUES (31,32,1,0.25),(31,36,1,0.25),(31,41,1,0.25),(31,43,1,0.25),(31,47,1,0.25),(31,51,2,0.25),(31,53,1,0.25),(31,56,1,0.25),(32,25,1,0.32),(32,29,2,0.32),(32,33,2,0.2),(32,38,1,0.2),(32,39,1,0.2),(32,43,3,0.2),(32,44,2,0.2),(32,51,1,0.2),(32,57,1,0.2),(33,26,2,0.16),(33,30,4,0.16),(33,34,2,0.16),(33,37,1,0.16),(33,43,3,0.16),(33,44,5,0.16),(33,46,1,0.16),(33,48,3,0.16),(33,52,3,0.16),(33,54,2,0.16),(33,59,1,0.16),(33,60,1,0.16),(34,25,2,0.22),(34,27,1,0.22),(34,28,1,0.22),(34,31,2,0.22),(34,35,2,0.22),(34,38,1,0.22),(34,40,1,0.22),(34,42,2,0.22),(34,44,1,0.22),(34,45,1,0.22),(34,46,1,0.22),(34,49,3,0.22),(34,50,1,0.22),(34,55,1,0.22),(34,58,2,0.22);
/*!40000 ALTER TABLE `tiposArt_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposArticulo`
--

DROP TABLE IF EXISTS `tiposArticulo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposArticulo` (
  `idTipoArticulo` int(11) NOT NULL AUTO_INCREMENT,
  `stock` float DEFAULT NULL,
  `margenGanancia` float DEFAULT NULL,
  `unidadMedida` varchar(60) CHARACTER SET latin1 DEFAULT NULL,
  `nombre` varchar(50) CHARACTER SET latin1 DEFAULT NULL,
  `cProduccion` float DEFAULT NULL,
  `cInsumos` float DEFAULT NULL,
  `cTotal` float DEFAULT NULL,
  `cObtencionAlt` float DEFAULT NULL,
  `otrosCostos` float DEFAULT NULL,
  `img` varchar(1000) DEFAULT NULL,
  `vUsuario` tinyint(4) DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  `descripcion` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`idTipoArticulo`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=latin2;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposArticulo`
--

LOCK TABLES `tiposArticulo` WRITE;
/*!40000 ALTER TABLE `tiposArticulo` DISABLE KEYS */;
INSERT INTO `tiposArticulo` VALUES (31,2,0.25,'Unidades','Árbol de Navidad',120,556,696,1200,20,'/static/img/articulos/31/christmas.jpg',1,'disponible',''),(32,3,0.2,'Unidad','Gorro de Lana',10,239.75,254.75,650,5,'/static/img/articulos/32/lana.jpg',1,'disponible',''),(33,0,0.16,'Unidad','Florero de Vidrio',50,36.6,96.6,200,10,'/static/img/articulos/33/florero.jpg',1,'disponible',''),(34,2,0.22,'Unidad','Comedero de Perro',20,50,88,150,18,'/static/img/articulos/34/comedero.jpg',1,'disponible',''),(35,2,0.02,'Unidad','Ladrillo de Plástico',50,250,310,400,10,'/static/img/articulos/35/images.jpg',1,'disponible','Ladrillos hechos de PET'),(36,0,0.02,'test','Test',1222,397,1741,122,122,'/staticimgarticulos36Wallpaper_77.jpg',1,'eliminado',''),(37,0,0.02,'ass','ass',12,489,623,122,122,'',1,'eliminado','asss'),(38,0,0.22,'1222','122',122,308,552,1222,122,'',1,'eliminado','1222');
/*!40000 ALTER TABLE `tiposArticulo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposDocumento`
--

DROP TABLE IF EXISTS `tiposDocumento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposDocumento` (
  `idTipoDoc` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idTipoDoc`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposDocumento`
--

LOCK TABLES `tiposDocumento` WRITE;
/*!40000 ALTER TABLE `tiposDocumento` DISABLE KEYS */;
INSERT INTO `tiposDocumento` VALUES (1,'DNI','habilitado'),(2,'LC','habilitado'),(3,'LE','habilitado'),(4,'CI','habilitado');
/*!40000 ALTER TABLE `tiposDocumento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposUsuario`
--

DROP TABLE IF EXISTS `tiposUsuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tiposUsuario` (
  `idTipoUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `estado` varchar(45) DEFAULT 'disponible',
  PRIMARY KEY (`idTipoUsuario`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COMMENT='	';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposUsuario`
--

LOCK TABLES `tiposUsuario` WRITE;
/*!40000 ALTER TABLE `tiposUsuario` DISABLE KEYS */;
INSERT INTO `tiposUsuario` VALUES (1,'Ciudadano','disponible'),(2,'Administrador Total','disponible'),(3,'Empleado Punto de Retiro','disponible'),(4,'Empleado Punto de Depósito','disponible'),(5,'Empleado Contable','disponible'),(6,'Supervisor','disponible'),(7,'Coordinador','disponible'),(8,'ssss','eliminado'),(9,'Ayudante del Ayudante','eliminado'),(10,'Encargado de Produccion','disponible');
/*!40000 ALTER TABLE `tiposUsuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `nroDoc` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `password` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `nombre` varchar(150) CHARACTER SET latin1 DEFAULT NULL,
  `apellido` varchar(150) CHARACTER SET latin1 DEFAULT NULL,
  `email` varchar(100) CHARACTER SET latin1 DEFAULT NULL,
  `idTipoUsuario` int(11) DEFAULT '1',
  `idTipoDoc` int(11) DEFAULT NULL,
  `idDireccion` int(11) DEFAULT NULL,
  `idNivel` int(11) DEFAULT NULL,
  `img` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `estado` varchar(45) CHARACTER SET latin1 DEFAULT 'habilitado',
  `codigo_registro` varchar(45) DEFAULT NULL,
  `fechaReg` date DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `idTipoDoc_idx` (`idTipoDoc`),
  KEY `idTipoUsuario_idx` (`idTipoUsuario`),
  KEY `idDireccion_idx` (`idDireccion`),
  KEY `idNivelUsuario_idx` (`idNivel`),
  CONSTRAINT `idDireccion` FOREIGN KEY (`idDireccion`) REFERENCES `direcciones` (`idDireccion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idNivelUsuario` FOREIGN KEY (`idNivel`) REFERENCES `niveles` (`idNivel`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoDoc` FOREIGN KEY (`idTipoDoc`) REFERENCES `tiposDocumento` (`idTipoDoc`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `idTipoUsuario` FOREIGN KEY (`idTipoUsuario`) REFERENCES `tiposUsuario` (`idTipoUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin5;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (5,'40346879','proyectoFinal1','Santiago','Garcia','proyecto@final.com',2,1,44,15,'/static/img/users/5/profile/santi-test.jpg','habilitado','5b417a954055fe63','2019-02-16'),(8,'41028971','holaChau1','Bruno Tomás','Caracini','bruno98980@gmail.com',1,1,45,14,'/static/img/users/8/profile/39558094.jpg','habilitado','9b417a957055fe63','2021-01-02'),(9,NULL,'holaChau1',NULL,NULL,'agus@gmail.com',1,NULL,NULL,NULL,NULL,'no-activo','17605bd432ba1de2','2021-03-16'),(10,NULL,'holaChau1',NULL,NULL,'andy@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','334ae6e4f88b4c80','2021-02-16'),(11,NULL,'holaChau1',NULL,NULL,'nacha@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','6f0942a35d98bad0','2021-01-16'),(12,NULL,'holaChau1',NULL,NULL,'joaco@gmail.com',1,NULL,NULL,NULL,NULL,'eliminado','d6ded5856fc625cb','2019-02-16'),(13,NULL,'holaChau1',NULL,NULL,'dai@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','75e1490f277960cb','2020-04-16'),(14,NULL,'holaChau1',NULL,NULL,'seba@gmail.com',1,NULL,NULL,NULL,NULL,'eliminado','60a3579fe5787d8c','2020-08-16'),(15,NULL,'holaChau1',NULL,NULL,'juli@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','17b547283f33eb03','2020-07-16'),(16,NULL,'holaChau1',NULL,NULL,'melo@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','d62e19f3d5da3af8','2021-02-16'),(17,NULL,'holaChau1',NULL,NULL,'ro@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','702d9f7614f1c7ff','2020-12-16'),(19,NULL,'Hola12345',NULL,NULL,'joaquincardonaruiz@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','66e8a107e00d811b','2021-04-22'),(20,NULL,'holaChau1',NULL,NULL,'brunocinvestments@gmail.com',1,NULL,NULL,NULL,NULL,'no-activo','77f6529a54f9491a','2021-04-22'),(21,NULL,'holaChau1',NULL,NULL,'joaco.swii@gmail.com',1,NULL,NULL,NULL,NULL,'no-verificado','7d6b404d9d1540a7','2021-04-22');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valoresTipArt`
--

DROP TABLE IF EXISTS `valoresTipArt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valoresTipArt` (
  `idValor` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoArticulo` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `valor` float DEFAULT NULL,
  PRIMARY KEY (`idValor`,`idTipoArticulo`),
  KEY `idTipoArticulo_idx` (`idTipoArticulo`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valoresTipArt`
--

LOCK TABLES `valoresTipArt` WRITE;
/*!40000 ALTER TABLE `valoresTipArt` DISABLE KEYS */;
INSERT INTO `valoresTipArt` VALUES (37,31,'2018-04-19 17:36:25',744.72),(38,32,'2018-04-19 17:41:53',280.23),(39,33,'2018-04-19 17:46:22',100.46),(40,31,'2018-04-19 17:46:42',870),(41,32,'2018-04-19 17:46:48',336.27),(42,33,'2018-04-19 17:46:55',112.06),(43,34,'2018-04-19 17:48:20',107.36),(44,32,'2021-04-19 20:50:20',305.7),(45,35,'2021-04-21 02:47:11',316.2),(46,36,'2021-04-23 22:54:23',1775.82),(47,37,'2021-04-23 22:56:10',635.46),(48,38,'2021-04-23 22:58:04',673.44);
/*!40000 ALTER TABLE `valoresTipArt` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-26 19:45:56

-- MariaDB dump 10.19  Distrib 10.5.13-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: spotifree
-- ------------------------------------------------------
-- Server version	10.5.13-MariaDB-0ubuntu0.21.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `friends`
--

DROP TABLE IF EXISTS `friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `friends` (
  `id_user1` int(11) DEFAULT NULL,
  `id_user2` int(11) DEFAULT NULL,
  KEY `id_user1` (`id_user1`),
  KEY `id_user2` (`id_user2`),
  CONSTRAINT `friends_ibfk_1` FOREIGN KEY (`id_user1`) REFERENCES `user` (`id_user`),
  CONSTRAINT `friends_ibfk_2` FOREIGN KEY (`id_user2`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friends`
--

LOCK TABLES `friends` WRITE;
/*!40000 ALTER TABLE `friends` DISABLE KEYS */;
INSERT INTO `friends` VALUES (2,1),(1,5);
/*!40000 ALTER TABLE `friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `musique`
--

DROP TABLE IF EXISTS `musique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `musique` (
  `id_musique` int(11) NOT NULL AUTO_INCREMENT,
  `nom` text DEFAULT NULL,
  `artiste` text DEFAULT NULL,
  `album` text DEFAULT NULL,
  `lien` text DEFAULT NULL,
  PRIMARY KEY (`id_musique`),
  UNIQUE KEY `nom` (`nom`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `musique`
--

LOCK TABLES `musique` WRITE;
/*!40000 ALTER TABLE `musique` DISABLE KEYS */;
INSERT INTO `musique` VALUES (10,'Fireflies','Owl City','Ocean Eyes','Fireflies'),(11,'Sainted by the Storm','Powerwolf','Sainted by the Storm','Sainted by the Storm'),(12,'Le Lac Du Connemara - Live In Chasse Theater, Breda / 1996','BZN','A Symphonic Night','Le Lac Du Connemara - Live In Chasse Theater, Breda  1996'),(13,'Sunday Bloody Sunday','Rockabye Baby!','Lullaby Renditions of U2','Sunday Bloody Sunday'),(14,'Sunday Bloody Sunday - Live at Wembley Stadium, 13th July 1985','U2','U2 at Live Aid (Live at Wembley Stadium, 13th July 1985)','Sunday Bloody Sunday - Live at Wembley Stadium, 13th July 1985'),(15,'Thunderstruck','AC/DC','The Razors Edge','Thunderstruck'),(16,'Rock N Roll Train','AC/DC','Black Ice','Rock N Roll Train'),(17,'T.N.T.','AC/DC','High Voltage','T.N.T.');
/*!40000 ALTER TABLE `musique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `musique_playlist`
--

DROP TABLE IF EXISTS `musique_playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `musique_playlist` (
  `id_playlist` int(11) DEFAULT NULL,
  `id_musique` int(11) DEFAULT NULL,
  KEY `id_playlist` (`id_playlist`),
  KEY `id_musique` (`id_musique`),
  CONSTRAINT `musique_playlist_ibfk_1` FOREIGN KEY (`id_playlist`) REFERENCES `playlist` (`id_playlist`),
  CONSTRAINT `musique_playlist_ibfk_2` FOREIGN KEY (`id_musique`) REFERENCES `musique` (`id_musique`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `musique_playlist`
--

LOCK TABLES `musique_playlist` WRITE;
/*!40000 ALTER TABLE `musique_playlist` DISABLE KEYS */;
INSERT INTO `musique_playlist` VALUES (2,13),(2,17),(2,16),(3,11),(3,12),(3,17),(3,13),(2,17),(2,11);
/*!40000 ALTER TABLE `musique_playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playlist`
--

DROP TABLE IF EXISTS `playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playlist` (
  `id_playlist` int(11) NOT NULL AUTO_INCREMENT,
  `id_user` int(11) DEFAULT NULL,
  `nom_playlist` text DEFAULT NULL,
  `prive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id_playlist`),
  UNIQUE KEY `nom_playlist` (`nom_playlist`) USING HASH,
  KEY `id_user` (`id_user`),
  CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playlist`
--

LOCK TABLES `playlist` WRITE;
/*!40000 ALTER TABLE `playlist` DISABLE KEYS */;
INSERT INTO `playlist` VALUES (2,1,'premiere_play',0),(3,1,'best_playlist',0);
/*!40000 ALTER TABLE `playlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nom_user` text DEFAULT NULL,
  `mdp` text DEFAULT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `nom_user` (`nom_user`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'CyrilC','cyril'),(2,'Rania','rania'),(3,'Bastien','bastien'),(5,'CyrilM','cyril'),(6,'Baptiste','baptiste');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_playlist`
--

DROP TABLE IF EXISTS `user_playlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_playlist` (
  `id_playlist` int(11) DEFAULT NULL,
  `id_user` int(11) DEFAULT NULL,
  KEY `id_playlist` (`id_playlist`),
  KEY `id_user` (`id_user`),
  CONSTRAINT `user_playlist_ibfk_1` FOREIGN KEY (`id_playlist`) REFERENCES `playlist` (`id_playlist`),
  CONSTRAINT `user_playlist_ibfk_2` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_playlist`
--

LOCK TABLES `user_playlist` WRITE;
/*!40000 ALTER TABLE `user_playlist` DISABLE KEYS */;
INSERT INTO `user_playlist` VALUES (2,3);
/*!40000 ALTER TABLE `user_playlist` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-17  9:17:23

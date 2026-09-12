-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: my_pos_db
-- ------------------------------------------------------
-- Server version	8.0.46

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add category',7,'add_category'),(26,'Can change category',7,'change_category'),(27,'Can delete category',7,'delete_category'),(28,'Can view category',7,'view_category'),(29,'Can add product',8,'add_product'),(30,'Can change product',8,'change_product'),(31,'Can delete product',8,'delete_product'),(32,'Can view product',8,'view_product'),(33,'Can add order',9,'add_order'),(34,'Can change order',9,'change_order'),(35,'Can delete order',9,'delete_order'),(36,'Can view order',9,'view_order'),(37,'Can add order item',10,'add_orderitem'),(38,'Can change order item',10,'change_orderitem'),(39,'Can delete order item',10,'delete_orderitem'),(40,'Can view order item',10,'view_orderitem'),(41,'Can add supplier',11,'add_supplier'),(42,'Can change supplier',11,'change_supplier'),(43,'Can delete supplier',11,'delete_supplier'),(44,'Can view supplier',11,'view_supplier'),(45,'Can add sale',12,'add_sale'),(46,'Can change sale',12,'change_sale'),(47,'Can delete sale',12,'delete_sale'),(48,'Can view sale',12,'view_sale'),(49,'Can add sale item',13,'add_saleitem'),(50,'Can change sale item',13,'change_saleitem'),(51,'Can delete sale item',13,'delete_saleitem'),(52,'Can view sale item',13,'view_saleitem'),(53,'Can add product size',14,'add_productsize'),(54,'Can change product size',14,'change_productsize'),(55,'Can delete product size',14,'delete_productsize'),(56,'Can view product size',14,'view_productsize'),(57,'Can add cashier profile',15,'add_cashierprofile'),(58,'Can change cashier profile',15,'change_cashierprofile'),(59,'Can delete cashier profile',15,'delete_cashierprofile'),(60,'Can view cashier profile',15,'view_cashierprofile'),(61,'Can add product variant',16,'add_productvariant'),(62,'Can change product variant',16,'change_productvariant'),(63,'Can delete product variant',16,'delete_productvariant'),(64,'Can view product variant',16,'view_productvariant'),(65,'Can add subcategory',17,'add_subcategory'),(66,'Can change subcategory',17,'change_subcategory'),(67,'Can delete subcategory',17,'delete_subcategory'),(68,'Can view subcategory',17,'view_subcategory'),(69,'Can add supplier',18,'add_supplier'),(70,'Can change supplier',18,'change_supplier'),(71,'Can delete supplier',18,'delete_supplier'),(72,'Can view supplier',18,'view_supplier'),(73,'Can add purchase',19,'add_purchase'),(74,'Can change purchase',19,'change_purchase'),(75,'Can delete purchase',19,'delete_purchase'),(76,'Can view purchase',19,'view_purchase'),(77,'Can add managed product',20,'add_managedproduct'),(78,'Can change managed product',20,'change_managedproduct'),(79,'Can delete managed product',20,'delete_managedproduct'),(80,'Can view managed product',20,'view_managedproduct');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$ZG5X7cO4qFz56LTRwQ2vpm$GHXOFVlQdYXdLNUjE1zPcOrIXbf87rT8cjUj3pnELhM=','2026-08-13 15:03:26.100135',1,'zin','','','',1,1,'2026-06-09 12:54:00.418671'),(2,'pbkdf2_sha256$1000000$uvHPvJxkN6VJfaLf4PHKJG$jr8vhvebNsuHuj8V20cHl7Li8z655lT9AUuC/h7WCc0=','2026-08-13 15:03:03.006609',0,'su myat noe','','','su@gmail.com',0,1,'2026-06-09 12:55:35.429543'),(4,'pbkdf2_sha256$1000000$UCHliAQtfeTv56zrDNAXf5$3pWHjZT7b4nGpHFe4tKfDH2Qro0wdHEsDv0lnFPvvLc=',NULL,0,'Shein Wai Khant','','','shein@gmail.com',1,1,'2026-06-15 14:28:13.411965');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(15,'products','cashierprofile'),(7,'products','category'),(20,'products','managedproduct'),(8,'products','product'),(14,'products','productsize'),(16,'products','productvariant'),(19,'products','purchase'),(17,'products','subcategory'),(11,'products','supplier'),(9,'sales','order'),(10,'sales','orderitem'),(12,'sales','sale'),(13,'sales','saleitem'),(6,'sessions','session'),(18,'suppliers','supplier');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-06-09 12:53:06.201134'),(2,'auth','0001_initial','2026-06-09 12:53:07.578680'),(3,'admin','0001_initial','2026-06-09 12:53:07.837829'),(4,'admin','0002_logentry_remove_auto_add','2026-06-09 12:53:07.859681'),(5,'admin','0003_logentry_add_action_flag_choices','2026-06-09 12:53:07.878346'),(6,'contenttypes','0002_remove_content_type_name','2026-06-09 12:53:08.054693'),(7,'auth','0002_alter_permission_name_max_length','2026-06-09 12:53:08.183478'),(8,'auth','0003_alter_user_email_max_length','2026-06-09 12:53:08.228940'),(9,'auth','0004_alter_user_username_opts','2026-06-09 12:53:08.238840'),(10,'auth','0005_alter_user_last_login_null','2026-06-09 12:53:08.336868'),(11,'auth','0006_require_contenttypes_0002','2026-06-09 12:53:08.347386'),(12,'auth','0007_alter_validators_add_error_messages','2026-06-09 12:53:08.360721'),(13,'auth','0008_alter_user_username_max_length','2026-06-09 12:53:08.479283'),(14,'auth','0009_alter_user_last_name_max_length','2026-06-09 12:53:08.608736'),(15,'auth','0010_alter_group_name_max_length','2026-06-09 12:53:08.637983'),(16,'auth','0011_update_proxy_permissions','2026-06-09 12:53:08.650311'),(17,'auth','0012_alter_user_first_name_max_length','2026-06-09 12:53:08.780994'),(18,'products','0001_initial','2026-06-09 12:53:08.989646'),(19,'products','0002_alter_product_barcode_id','2026-06-09 12:53:08.998096'),(20,'sales','0001_initial','2026-06-09 12:53:09.432214'),(21,'sales','0002_order_pdf_file_order_subtotal_order_tax_amount','2026-06-09 12:53:09.818580'),(22,'sessions','0001_initial','2026-06-09 12:53:09.907361'),(23,'products','0003_supplier_rename_barcode_id_product_product_code_and_more','2026-06-09 15:18:09.216124'),(24,'products','0004_remove_supplier_address_alter_product_category_and_more','2026-06-09 15:23:58.313359'),(25,'sales','0003_remove_order_invoice_number_remove_order_pdf_file_and_more','2026-06-15 16:49:50.558128'),(26,'products','0005_productsize_cashierprofile_productvariant','2026-07-18 17:28:44.728440'),(27,'products','0006_subcategory','2026-07-18 17:48:36.271608'),(29,'products','0007_supplier_email','2026-07-19 17:03:51.941240'),(30,'products','0008_purchase','2026-07-19 17:36:25.127445'),(31,'products','0009_product_subcategory','2026-07-20 15:15:48.709765'),(32,'products','0010_purchase_product_name_alter_purchase_product','2026-07-21 14:29:26.613342'),(33,'products','0010_managedproduct','2026-07-21 15:09:14.437571'),(34,'products','0011_remove_purchase_product_purchase_product_name','2026-07-21 15:42:28.535647'),(35,'products','0012_productvariant_barcode_productvariant_buying_price_and_more','2026-07-21 15:54:33.428087'),(36,'sales','0004_order_invoice_number_order_pdf_file_order_subtotal_and_more','2026-07-23 17:19:18.393918'),(37,'sales','0005_sale_image_file','2026-07-25 15:09:35.030105');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1lw91snlri5pppgy2q33kfa1w0q0zfoy','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq1At:YqS3WOtuZp8RWJD6J19zKdl6LVr7JC5DEka0BxPHQJo','2026-08-15 04:18:15.258255'),('2b2x97lftgqgmf7b0uuhji790xygpqxq','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wuWxq:d9noq27B0rPeF3sEcSBFx7-OHb2ZiRTjRCUbzRpgRdw','2026-08-27 15:03:26.110903'),('53918ago7t3ut3ygwyugbuxwftbxvb26','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wlTDW:f0n5RDnrwC7BTsdEN5FciuZkAPJJWGhFIJdhdVUzaPQ','2026-08-02 15:14:10.597106'),('96xlsc1hnw6hb4d1vfh4kbx6q5a6luuj','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FX:V4LZLg6bgR56jCg4IpsRlyWJPS3gsQ8_cdAtsXGqq7g','2026-06-29 14:25:15.225268'),('9p9txj6qh6nuoayfzduh1ezpvkz732jb','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wXMSh:t1WEkZN6JDcPN1CIyV81HbjRL47IW9yMnxXycG48K2s','2026-06-24 17:11:31.584556'),('a52h9dbj9vg54objjm0kq7exv6egdoho','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq1ED:a6T2hPTnLv8PbNxyN0V0jeXDAW9tmUilQF-sf0aBF8Y','2026-08-15 04:21:41.044980'),('a8zofvybgclohkuuavlpssw3jo9agw62','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FW:epePcr_aQ9fz7QuVu5V3qkz30TVpKFt3wY75sa8JoS8','2026-06-29 14:25:14.292769'),('atjiiw5q4ugl023o0fsho1wl3tgyrn8s','.eJxVjLsOAiEQAP-F2hD2RBcs7f0GsrsscmoguUdl_HdzyRXazkzmbRKtS03rrFMas7kYMIdfxiRPbZvID2r3bqW3ZRrZbond7WxvPevrurd_g0pz3baanQf25xNg9qjimDSScwJHgBDK4CkHQnQDl1JYGJE4qETxgCGazxfoBzhW:1wpr6e:jU8lWCXsoa2csFWSKlyhPX4GgDZ1UhdVT9LSXhtbo-k','2026-08-14 17:33:12.908744'),('ccseqb3b0svh6lzqadh4ajiekft9fdk8','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FX:V4LZLg6bgR56jCg4IpsRlyWJPS3gsQ8_cdAtsXGqq7g','2026-06-29 14:25:15.065112'),('ejs6ds5qkkqmel8q1461814w2se4h49w','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq1Eg:v-qxaqNMqVsoG5lzgKDYXajATOcYBlpPt47wbOSAyL8','2026-08-15 04:22:10.202669'),('f2u5j5x9uabpkam83zp1l8rritom41lk','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq16i:JMBrRxTNRX2F1u-j1TrYMJoqQHHtZcbzNdvl5-VPQgQ','2026-08-15 04:13:56.438491'),('fvd2vtx8gyr6ppe3hociuf00eqo1mu8l','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wlTKJ:k9LUmTT7vcsMBHb3UjSJ0fKBMb4OD8wDK2t-FbnYrDo','2026-08-02 15:21:11.939558'),('fzd4dlw28vg3p8ywze9er8lkgjz85a7d','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wpqaN:1uSEYg-jEkOQKPuXcoVikqP_06ewQ5aTHRfEWlHoIpo','2026-08-14 16:59:51.245897'),('h0bk5pwnv240ys2clpb4utu63wqrg0gz','e30:1wnpc3:Mwz3r9LVik8Ia2ZKzwhhns9axhLI-iy1fkqd9-JjXs4','2026-08-09 03:33:15.798322'),('hskm9sc11dqeu8hyirxgqmyilqf4k91j','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wpql0:kpw7CbCWr9WS8-UT41mYf4M3tej5LuP2bKqf5Zb4G0o','2026-08-14 17:10:50.172155'),('hzleers9i47kf31r8tt7b7ktzdm5vjp9','e30:1wnf7T:NBSLLFjx6HGCWhC-TCl8YrARPXjiHLT91aBf2bWC5O8','2026-08-08 16:20:59.466665'),('jowjm9hnjpmk0x3xrondcot4mqluqysp','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wXDdU:qlAIfMf3JfxWDNxN6g-azdmC57vw_F38NMBlOT3KvcU','2026-06-24 07:46:04.874397'),('kxuano2rhkf1pu5k5z214j99sl5xz7gg','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wmuRn:9BFZbQo4FWLrMgaxulIp2I5-1HXzofcDZa34vnzh-bM','2026-08-06 14:30:51.185978'),('kytmxogdi5v6yqycs6gb1u15w1ht9yfd','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FU:p4WziXHS-OSPxe7Bm6NpDxjtQDrb7AsaCQirjk33mHA','2026-06-29 14:25:12.927491'),('lv3cs5oc1dfwk6us0f224fi8reqeplg9','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq17s:pSw30mrnYXOt8y-1lYoc8LhVNzTDAgNsaNnYHK2cG-Q','2026-08-15 04:15:08.948260'),('mdmpgivmqcyviwd3szy4sjy85wodnv2c','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq1aI:wITMxU2wUn_Bu--a0VaKB8p5V0RpKXzVU33pmmIPQTU','2026-08-15 04:44:30.120962'),('nev044vjsygvrr8rssk0unasnpt1v2gd','e30:1wXFpH:gYE63WppQihp_4cfBDp5d6DooWVIthclMDRwWDTV8R4','2026-06-24 10:06:23.692476'),('qkvt3vhgmqq19vp7ub44ufsnct3hejmt','.eJxVjLsOAiEQAP-F2hD2RBcs7f0GsrsscmoguUdl_HdzyRXazkzmbRKtS03rrFMas7kYMIdfxiRPbZvID2r3bqW3ZRrZbond7WxvPevrurd_g0pz3baanQf25xNg9qjimDSScwJHgBDK4CkHQnQDl1JYGJE4qETxgCGazxfoBzhW:1wpqta:Q6rgEq2mZV85B5L7uYYpZcCwrtAZbe_AP6hOLVGGVmE','2026-08-14 17:19:42.980614'),('sjyuqtwwq6l4u6wdrjimcltwyejvyk0j','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FX:V4LZLg6bgR56jCg4IpsRlyWJPS3gsQ8_cdAtsXGqq7g','2026-06-29 14:25:15.232839'),('tvad310o2bkmc9qyszf9y97ic79z13sv','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wZ8FQ:_noTroWKxuCsC6euQ_kE-PVz4QZED1koX8fDpm_GHKs','2026-06-29 14:25:08.670415'),('vq3wu5ouqcu6js2y27vx3vv1doycdt7p','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq1bp:dn35AZ2QULaAWFrD_Pxhw1iHgbPFZyoaHJj_fTqO3Do','2026-08-15 04:46:05.561395'),('wymxhfhdyk2m2x2utjz1x3d1uwgb7un7','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq131:rv9Guie7BYv8xZe5MoY2zXvs6ohuN22ES9z0saJ0H-Y','2026-08-15 04:10:07.915255'),('wz49vv88gchgd6zal86dbuvv74p2u5c9','.eJxVjMEOwiAQRP-FsyHAIhSP3v0GsrCLVA1NSnsy_rtt0oOeJpn3Zt4i4rrUuHae40jiIrQ4_XYJ85PbDuiB7T7JPLVlHpPcFXnQLm8T8et6uH8HFXvd1hZCyYWLDXgmpYIxwNalAQBIq-Ap4BYarVfsQGXymmEgA8aRSUDi8wXROTc3:1wq17C:dHSkOKPmS5e7MUS-8r27BnoNX6YFC0XA3qbWhmnujJ0','2026-08-15 04:14:26.471460'),('ydxmg49dwdoc6hv3bti9ee1b3rvczfi4','.eJxVjDsOwyAQBe9CHSHA5qOU6XMGtLsswUkEkrErK3ePLblI2jczbxMR1qXEtfMcpySuQovL74ZAL64HSE-ojyap1WWeUB6KPGmX95b4fTvdv4MCvew1cwIMeXTBuoEzwsgGWaEmAvba-ECDIqOs0tY7j4yIFnaFTcqALD5fGX85kw:1wpqaj:auYy3Za6Al0agbmlpG9puqAUT-sJLuMhXe13mWf-LAM','2026-08-14 17:00:13.572763');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_cashierprofile`
--

DROP TABLE IF EXISTS `products_cashierprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_cashierprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `products_cashierprofile_user_id_8d67fc8d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_cashierprofile`
--

LOCK TABLES `products_cashierprofile` WRITE;
/*!40000 ALTER TABLE `products_cashierprofile` DISABLE KEYS */;
INSERT INTO `products_cashierprofile` VALUES (1,'097654333354',2),(2,'09765477753',4);
/*!40000 ALTER TABLE `products_cashierprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_category`
--

DROP TABLE IF EXISTS `products_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_category` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_category`
--

LOCK TABLES `products_category` WRITE;
/*!40000 ALTER TABLE `products_category` DISABLE KEYS */;
INSERT INTO `products_category` VALUES (5,'Cosmetics'),(3,'Drinks'),(7,'Food'),(10,'Uncategorized');
/*!40000 ALTER TABLE `products_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_managedproduct`
--

DROP TABLE IF EXISTS `products_managedproduct`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_managedproduct` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `category_id` bigint NOT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  `supplier_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_managedprod_category_id_290acd99_fk_products_` (`category_id`),
  KEY `products_managedprod_subcategory_id_0ccac10f_fk_products_` (`subcategory_id`),
  KEY `products_managedprod_supplier_id_1d3050b0_fk_products_` (`supplier_id`),
  CONSTRAINT `products_managedprod_category_id_290acd99_fk_products_` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`),
  CONSTRAINT `products_managedprod_subcategory_id_0ccac10f_fk_products_` FOREIGN KEY (`subcategory_id`) REFERENCES `products_subcategory` (`id`),
  CONSTRAINT `products_managedprod_supplier_id_1d3050b0_fk_products_` FOREIGN KEY (`supplier_id`) REFERENCES `products_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_managedproduct`
--

LOCK TABLES `products_managedproduct` WRITE;
/*!40000 ALTER TABLE `products_managedproduct` DISABLE KEYS */;
INSERT INTO `products_managedproduct` VALUES (1,'Yan Yan','2026-07-21 15:37:52.115603',7,1,1),(5,'Romand','2026-08-02 04:25:14.991675',5,5,2),(6,'JM Solution B5 HYA','2026-08-02 04:25:51.127885',5,2,2),(8,'KIYOI','2026-08-02 04:36:51.178405',5,10,2);
/*!40000 ALTER TABLE `products_managedproduct` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_product`
--

DROP TABLE IF EXISTS `products_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_product` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `product_code` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int NOT NULL,
  `qr_code` varchar(100) DEFAULT NULL,
  `category_id` bigint NOT NULL,
  `supplier_id` bigint DEFAULT NULL,
  `subcategory_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode_id` (`product_code`),
  KEY `products_product_category_id_9b594869_fk_products_category_id` (`category_id`),
  KEY `products_product_supplier_id_b9ff64a9_fk_products_supplier_id` (`supplier_id`),
  KEY `products_product_subcategory_id_b28a1e3b_fk_products_` (`subcategory_id`),
  CONSTRAINT `products_product_category_id_9b594869_fk_products_category_id` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`),
  CONSTRAINT `products_product_subcategory_id_b28a1e3b_fk_products_` FOREIGN KEY (`subcategory_id`) REFERENCES `products_subcategory` (`id`),
  CONSTRAINT `products_product_supplier_id_b9ff64a9_fk_products_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `products_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_product`
--

LOCK TABLES `products_product` WRITE;
/*!40000 ALTER TABLE `products_product` DISABLE KEYS */;
INSERT INTO `products_product` VALUES (22,'KIYOI','PUR_15196',0.00,0,'qr_codes/qr_PUR_15196.png',10,NULL,NULL),(23,'Romand','PUR_86765',0.00,0,'qr_codes/qr_PUR_86765.png',10,NULL,NULL);
/*!40000 ALTER TABLE `products_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productsize`
--

DROP TABLE IF EXISTS `products_productsize`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_productsize` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productsize`
--

LOCK TABLES `products_productsize` WRITE;
/*!40000 ALTER TABLE `products_productsize` DISABLE KEYS */;
INSERT INTO `products_productsize` VALUES (7,'1ပါကင်'),(4,'200g'),(2,'20g'),(1,'20ml'),(3,'50ml'),(8,'ကော်ဘူး'),(5,'ဘူး'),(9,'သံဘူး'),(6,'အထုပ်');
/*!40000 ALTER TABLE `products_productsize` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_productvariant`
--

DROP TABLE IF EXISTS `products_productvariant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_productvariant` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `product_id` bigint NOT NULL,
  `barcode` varchar(100) DEFAULT NULL,
  `buying_price` decimal(10,2) NOT NULL,
  `exp` varchar(50) DEFAULT NULL,
  `qr_code` varchar(100) DEFAULT NULL,
  `qty` int NOT NULL,
  `selling_price` decimal(10,2) NOT NULL,
  `size_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`),
  KEY `products_productvari_product_id_d9c22902_fk_products_` (`product_id`),
  KEY `products_productvari_size_id_b307fc69_fk_products_` (`size_id`),
  CONSTRAINT `products_productvari_product_id_d9c22902_fk_products_` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  CONSTRAINT `products_productvari_size_id_b307fc69_fk_products_` FOREIGN KEY (`size_id`) REFERENCES `products_productsize` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_productvariant`
--

LOCK TABLES `products_productvariant` WRITE;
/*!40000 ALTER TABLE `products_productvariant` DISABLE KEYS */;
INSERT INTO `products_productvariant` VALUES (11,'KIYOI001',22,'KIYOI001',8500.00,'2029-8-9','variant_qr_codes/qr_KIYOI001.png',20,9000.00,6),(12,'ROMAND01',23,'ROMAND01',29000.00,'2030-8-9','variant_qr_codes/qr_ROMAND01.png',20,30000.00,5);
/*!40000 ALTER TABLE `products_productvariant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_purchase`
--

DROP TABLE IF EXISTS `products_purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_purchase` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `cashier_id` int DEFAULT NULL,
  `supplier_id` bigint DEFAULT NULL,
  `product_name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `products_purchase_cashier_id_4abd49d4_fk_auth_user_id` (`cashier_id`),
  KEY `products_purchase_supplier_id_74c65336_fk_products_supplier_id` (`supplier_id`),
  CONSTRAINT `products_purchase_cashier_id_4abd49d4_fk_auth_user_id` FOREIGN KEY (`cashier_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `products_purchase_supplier_id_74c65336_fk_products_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `products_supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_purchase`
--

LOCK TABLES `products_purchase` WRITE;
/*!40000 ALTER TABLE `products_purchase` DISABLE KEYS */;
INSERT INTO `products_purchase` VALUES (9,15,1500.00,22500.00,'2026-07-21 15:47:49.069159',2,1,'Yan Yan'),(12,20,25000.00,500000.00,'2026-08-02 04:31:29.159418',2,2,'JM Solution B5 HYA'),(13,20,29000.00,580000.00,'2026-08-02 04:32:29.889199',2,2,'Romand'),(14,20,8500.00,170000.00,'2026-08-02 04:33:50.640461',2,2,'KIYOI');
/*!40000 ALTER TABLE `products_purchase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_subcategory`
--

DROP TABLE IF EXISTS `products_subcategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_subcategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `category_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `products_subcategory_name_category_id_2ce9ad32_uniq` (`name`,`category_id`),
  KEY `products_subcategory_category_id_44d297b7_fk_products_` (`category_id`),
  CONSTRAINT `products_subcategory_category_id_44d297b7_fk_products_` FOREIGN KEY (`category_id`) REFERENCES `products_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_subcategory`
--

LOCK TABLES `products_subcategory` WRITE;
/*!40000 ALTER TABLE `products_subcategory` DISABLE KEYS */;
INSERT INTO `products_subcategory` VALUES (11,'Coca Cola',3),(7,'Eye brow',5),(4,'Foundation',5),(5,'Lipstic',5),(8,'Mask',5),(1,'Noodle',7),(6,'Powder',5),(9,'Scrub',5),(3,'Sunscreen',5),(2,'Toner',5),(10,'Toner Pad',5),(13,'Uncategorized',7);
/*!40000 ALTER TABLE `products_subcategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_supplier`
--

DROP TABLE IF EXISTS `products_supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_supplier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_supplier`
--

LOCK TABLES `products_supplier` WRITE;
/*!40000 ALTER TABLE `products_supplier` DISABLE KEYS */;
INSERT INTO `products_supplier` VALUES (1,'Aye Myat Khaing','09683848046','aye@gmail.com'),(2,'Hein Khant Aung','09663436987','hein@gmial.com');
/*!40000 ALTER TABLE `products_supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_order`
--

DROP TABLE IF EXISTS `sales_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `cashier_id` int DEFAULT NULL,
  `invoice_number` varchar(100) DEFAULT NULL,
  `pdf_file` varchar(100) DEFAULT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `tax_amount` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_number` (`invoice_number`),
  KEY `sales_order_cashier_id_77af2abb_fk_auth_user_id` (`cashier_id`),
  CONSTRAINT `sales_order_cashier_id_77af2abb_fk_auth_user_id` FOREIGN KEY (`cashier_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_order`
--

LOCK TABLES `sales_order` WRITE;
/*!40000 ALTER TABLE `sales_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_orderitem`
--

DROP TABLE IF EXISTS `sales_orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_orderitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `order_id` bigint NOT NULL,
  `product_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_orderitem_order_id_7845449c_fk_sales_order_id` (`order_id`),
  KEY `sales_orderitem_product_id_12b2cc4b_fk_products_product_id` (`product_id`),
  CONSTRAINT `sales_orderitem_order_id_7845449c_fk_sales_order_id` FOREIGN KEY (`order_id`) REFERENCES `sales_order` (`id`),
  CONSTRAINT `sales_orderitem_product_id_12b2cc4b_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_orderitem`
--

LOCK TABLES `sales_orderitem` WRITE;
/*!40000 ALTER TABLE `sales_orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales_orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_sale`
--

DROP TABLE IF EXISTS `sales_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_sale` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `total_amount` decimal(10,2) NOT NULL,
  `tax` decimal(10,2) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `cashier_id` int NOT NULL,
  `image_file` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_sale_cashier_id_ff324bab_fk_auth_user_id` (`cashier_id`),
  CONSTRAINT `sales_sale_cashier_id_ff324bab_fk_auth_user_id` FOREIGN KEY (`cashier_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_sale`
--

LOCK TABLES `sales_sale` WRITE;
/*!40000 ALTER TABLE `sales_sale` DISABLE KEYS */;
INSERT INTO `sales_sale` VALUES (1,5880.00,280.00,'2026-06-15 16:53:02.923258',2,NULL),(2,2100.00,100.00,'2026-06-15 17:02:01.941651',2,NULL),(3,1890.00,90.00,'2026-06-15 17:05:21.606297',2,NULL),(4,3990.00,190.00,'2026-06-15 17:18:21.102028',2,NULL),(5,1050.00,50.00,'2026-06-15 17:19:54.451932',2,NULL),(6,17325.00,825.00,'2026-07-23 16:38:11.561208',2,NULL),(7,17325.00,825.00,'2026-07-23 16:50:58.795058',2,NULL),(8,15750.00,750.00,'2026-07-23 17:21:36.955367',2,NULL),(9,15750.00,750.00,'2026-07-25 14:47:57.277075',2,NULL),(10,15750.00,750.00,'2026-07-25 15:17:02.010393',2,'invoices_images/SALE-10.png'),(11,15750.00,750.00,'2026-07-25 15:19:06.802776',2,'invoices_images/SALE-11.png'),(12,15750.00,750.00,'2026-07-25 15:41:12.370859',2,'invoices_images/SALE-12.png'),(13,1575.00,75.00,'2026-07-25 15:51:49.654358',2,'invoices_images/SALE-13.png'),(14,7875.00,375.00,'2026-08-01 04:37:40.512115',2,'invoices_images/SALE-14.png'),(15,7875.00,375.00,'2026-08-01 04:38:30.559379',2,'invoices_images/SALE-15.png'),(17,1575.00,75.00,'2026-08-01 04:47:29.388707',2,'invoices_images/SALE-17.png'),(18,1575.00,75.00,'2026-08-01 05:36:23.445949',2,'invoices_images/SALE-18.png'),(19,1575.00,75.00,'2026-08-01 05:36:44.645315',2,'invoices_images/SALE-19.png'),(20,40950.00,1950.00,'2026-08-06 07:45:31.547939',2,'invoices_images/SALE-20.png'),(21,192150.00,9150.00,'2026-08-06 07:46:00.651732',2,'invoices_images/SALE-21.png'),(22,31500.00,1500.00,'2026-08-06 08:50:39.185775',2,'invoices_images/SALE-22.png'),(23,31500.00,1500.00,'2026-08-06 08:52:50.678063',2,'invoices_images/SALE-23.png'),(24,9450.00,450.00,'2026-08-13 15:03:13.189390',2,'invoices_images/SALE-24.png');
/*!40000 ALTER TABLE `sales_sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales_saleitem`
--

DROP TABLE IF EXISTS `sales_saleitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales_saleitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_name` varchar(200) NOT NULL,
  `quantity` int NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `sale_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sales_saleitem_sale_id_56e67045_fk_sales_sale_id` (`sale_id`),
  CONSTRAINT `sales_saleitem_sale_id_56e67045_fk_sales_sale_id` FOREIGN KEY (`sale_id`) REFERENCES `sales_sale` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales_saleitem`
--

LOCK TABLES `sales_saleitem` WRITE;
/*!40000 ALTER TABLE `sales_saleitem` DISABLE KEYS */;
INSERT INTO `sales_saleitem` VALUES (1,'Coca Cola',2,1800.00,1),(2,'Max +',1,2000.00,1),(3,'Max +',1,2000.00,2),(4,'Coca Cola',1,1800.00,3),(5,'Max +',1,2000.00,4),(6,'Coca Cola',1,1800.00,4),(7,'Egg',1,1000.00,5),(8,'Ultra (M000001)',1,1500.00,6),(9,'Yan Yan (Y000001)',1,15000.00,6),(10,'Yan Yan',1,15000.00,7),(11,'Ultra',1,1500.00,7),(12,'Yan Yan',1,15000.00,8),(13,'Yan Yan',1,15000.00,9),(14,'Yan Yan',1,15000.00,10),(15,'Yan Yan',1,15000.00,11),(16,'Yan Yan',1,15000.00,12),(17,'Ultra',1,1500.00,13),(18,'Ultra',5,1500.00,14),(19,'Ultra',5,1500.00,15),(21,'Ultra',1,1500.00,17),(22,'Ultra',1,1500.00,18),(23,'Ultra',1,1500.00,19),(24,'KIYOI',1,9000.00,20),(25,'Romand',1,30000.00,20),(26,'Romand',4,30000.00,21),(27,'KIYOI',7,9000.00,21),(28,'Romand',1,30000.00,22),(29,'Romand',1,30000.00,23),(30,'KIYOI',1,9000.00,24);
/*!40000 ALTER TABLE `sales_saleitem` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-13 21:37:56

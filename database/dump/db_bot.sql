-- MySQL dump 10.13  Distrib 8.0.27, for Win64 (x86_64)
--
-- Host: localhost    Database: bot_db
-- ------------------------------------------------------
-- Server version	8.0.27

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
-- Table structure for table `request_info`
--

DROP TABLE IF EXISTS `request_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `request_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `command` varchar(45) DEFAULT NULL,
  `request_params` varchar(90) DEFAULT NULL,
  `request_result` longtext,
  `data` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request_info`
--

LOCK TABLES `request_info` WRITE;
/*!40000 ALTER TABLE `request_info` DISABLE KEYS */;
INSERT INTO `request_info` VALUES (1,222,'lowprice','some text in params','some text in results','2020-01-01'),(2,222,'lowprice','some text in params1','some text in results1','2020-01-02'),(3,222,'lowprice','some text in params','some text in results','2020-01-01'),(8,224,'lowprice','some text in params2','some text in results2','2020-04-01'),(9,224,'lowprice','some text in params2','some text in results2','2020-04-01'),(10,232,'lowprice','some text in params333','some text in results33','2020-03-01'),(11,232,'lowprice','some text in params31','some text in results133','2020-01-05'),(12,224,'highprice','some text in params2','some text in results2','2020-04-01'),(13,224,'highprice','some text in params2','some text in results2','2020-04-01'),(14,459415065,'lowprice','Вы искали отели в городе Тбилиси на период с 2022-11-23 по 2022-11-28.','Отель Ваш дом в Тбилиси 2.5 звезды.\nАдрес:тупик Гурджаани, 7.\nЦена за ночь 864 RUB\nПолная стоимость 4320\nСсылка: https://www.hotels.com/ho1267055840\nОтель Хостел Moosica 2.0 звезды.\nАдрес:ул. Александра Грибоедова, 13.\nЦена за ночь 1,056 RUB\nПолная стоимость 5280\nСсылка: https://www.hotels.com/ho1055980384\nОтель Hostel Portal 2.0 звезды.\nАдрес:ул. Вахтанга Горгасали, 4А.\nЦена за ночь 1,067 RUB\nПолная стоимость 5335\nСсылка: https://www.hotels.com/ho729652960\nОтель Гостевой дом «36» 3.0 звезды.\nАдрес:пр-т Шота Руставели, 36.\nЦена за ночь 1,153 RUB\nПолная стоимость 5765\nСсылка: https://www.hotels.com/ho863514688\nОтель Отель «Бон Вояж»  2.5 звезды.\nАдрес:пр-т Шота Руставели, 38.\nЦена за ночь 1,174 RUB\nПолная стоимость 5870\nСсылка: https://www.hotels.com/ho1215180960\n','2022-09-15'),(15,459415065,'highprice','Вы искали отели в городе Лондон на период с 2022-12-29 по 2023-01-04.','Отель Grandeur IV Executive Apartment Central London 0.0 звезды.\nАдрес: .\nЦена за ночь 212,950 RUB\nПолная стоимость 1277700\nСсылка: https://www.hotels.com/ho1223784480\nОтель Stylish Studios Students Only Kentish Town 2.5 звезды.\nАдрес: .\nЦена за ночь 121,437 RUB\nПолная стоимость 728622\nСсылка: https://www.hotels.com/ho1968677568\n','2022-09-15'),(16,459415065,'highprice','Вы искали отели в городе Тбилиси на период с 2022-12-30 по 2023-01-01.','Отель Санаторно-курортное объединение Bioli Medical Wellness Resort 5.0 звезды.\nАдрес:ул. Биоли, 1.\nЦена за ночь 23,552 RUB\nПолная стоимость 47104\nСсылка: https://www.hotels.com/ho1099108896\nОтель Отель Stamba 5.0 звезды.\nАдрес:ул. М. Костава, 14.\nЦена за ночь 14,240 RUB\nПолная стоимость 28480\nСсылка: https://www.hotels.com/ho770139808\n','2022-09-18'),(17,459415065,'beastdeal','Вы искали отели в городе Тбилиси на период с 2022-11-23 по 2022-11-25.','Отель Отель Your Comfort 2.5 звезд(ы).\nАдрес:ул. Узнадзе, 72, Чугурети.\nРастоянее от центра: 0,0 км\nЦена за ночь 1,280 RUB \nПолная стоимость 2560\nСсылка: https://www.hotels.com/ho1130216640\nОтель Отель «Арта» 3.0 звезд(ы).\nАдрес:Ул. Вахтанга Орбелиани, 24.\nРастоянее от центра: 0,0 км\nЦена за ночь 2,346 RUB \nПолная стоимость 4692\nСсылка: https://www.hotels.com/ho1145001408\nОтель Апартаменты Duplex200 3.0 звезд(ы).\nАдрес:ул. Мирзы Везирови, 16.\nРастоянее от центра: 0,0 км\nЦена за ночь 3,324 RUB \nПолная стоимость 6648\nСсылка: https://www.hotels.com/ho1265058880\nОтель Jazz Hotel 3.0 звезд(ы).\nАдрес:Махатский подъем, 23.\nРастоянее от центра: 1,4 км\nЦена за ночь 2,763 RUB \nПолная стоимость 5526\nСсылка: https://www.hotels.com/ho1232848064\nОтель Отель Sisno 0.0 звезд(ы).\nАдрес:ул. Зураба Квливидзе, 49.\nРастоянее от центра: 1,9 км\nЦена за ночь 4,235 RUB \nПолная стоимость 8470\nСсылка: https://www.hotels.com/ho1442894048\n','2022-09-18'),(18,459415065,'lowprice','Вы искали отели в городе Тбилиси на период с 2022-11-21 по 2022-11-26.','Отель Ваш дом в Тбилиси 2.5 звезды.\nАдрес:тупик Гурджаани, 7.\nЦена за ночь 864 RUB\nПолная стоимость 4320\nСсылка: https://www.hotels.com/ho1267055840\nОтель Хостел Moosica 2.0 звезды.\nАдрес:ул. Александра Грибоедова, 13.\nЦена за ночь 1,056 RUB\nПолная стоимость 5280\nСсылка: https://www.hotels.com/ho1055980384\nОтель Hostel Portal 2.0 звезды.\nАдрес:ул. Вахтанга Горгасали, 4А.\nЦена за ночь 1,066 RUB\nПолная стоимость 5330\nСсылка: https://www.hotels.com/ho729652960\nОтель Гостевой дом «36» 3.0 звезды.\nАдрес:пр-т Шота Руставели, 36.\nЦена за ночь 1,152 RUB\nПолная стоимость 5760\nСсылка: https://www.hotels.com/ho863514688\nОтель Отель «Бон Вояж»  2.5 звезды.\nАдрес:пр-т Шота Руставели, 38.\nЦена за ночь 1,174 RUB\nПолная стоимость 5870\nСсылка: https://www.hotels.com/ho1215180960\n','2022-09-18'),(19,459415065,'lowprice','Вы искали отели в городе Тбилиси на период с 2022-09-25 по 2022-09-29.','Отель Ваш дом в Тбилиси 2.5 звезды.\nАдрес:тупик Гурджаани, 7.\nЦена за ночь 864 RUB\nПолная стоимость 3456\nСсылка: https://www.hotels.com/ho1267055840\nОтель Хостел Moosica 2.0 звезды.\nАдрес:ул. Александра Грибоедова, 13.\nЦена за ночь 1,056 RUB\nПолная стоимость 4224\nСсылка: https://www.hotels.com/ho1055980384\nОтель Hostel Portal 2.0 звезды.\nАдрес:ул. Вахтанга Горгасали, 4А.\nЦена за ночь 1,066 RUB\nПолная стоимость 4264\nСсылка: https://www.hotels.com/ho729652960\nОтель Гостевой дом «36» 3.0 звезды.\nАдрес:пр-т Шота Руставели, 36.\nЦена за ночь 1,152 RUB\nПолная стоимость 4608\nСсылка: https://www.hotels.com/ho863514688\nОтель Отель «Бон Вояж»  2.5 звезды.\nАдрес:пр-т Шота Руставели, 38.\nЦена за ночь 1,174 RUB\nПолная стоимость 4696\nСсылка: https://www.hotels.com/ho1215180960\n','2022-09-18');
/*!40000 ALTER TABLE `request_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-23 13:01:55

/*
SQLyog Community v13.1.5  (64 bit)
MySQL - 5.6.12-log : Database - scrap_net
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`scrap_net` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `scrap_net`;

/*Table structure for table `car_details` */

DROP TABLE IF EXISTS `car_details`;

CREATE TABLE `car_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `car_model` varchar(30) DEFAULT NULL,
  `engineno` varchar(20) DEFAULT NULL,
  `chasesno` varchar(30) DEFAULT NULL,
  `seater` varchar(23) DEFAULT NULL,
  `regno` varchar(45) DEFAULT NULL,
  `fuel_type` varchar(20) DEFAULT NULL,
  `veh_condition` varchar(50) DEFAULT NULL,
  `reg_year` varchar(50) DEFAULT NULL,
  `wheel_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `car_details` */

insert  into `car_details`(`id`,`lid`,`car_model`,`engineno`,`chasesno`,`seater`,`regno`,`fuel_type`,`veh_condition`,`reg_year`,`wheel_type`) values 
(1,3,'zen','AFLK654FG5Fh','JGHJFGVH478G5','4','KL 32 N 3826','petrol','Running','2000','steel'),
(2,3,'k10','ASF46FGH5FF','G3GFDGH45','5','KL 22 F 5435','petrol','Running','1999','steel');

/*Table structure for table `carstatus` */

DROP TABLE IF EXISTS `carstatus`;

CREATE TABLE `carstatus` (
  `cid` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `carstatus` */

insert  into `carstatus`(`cid`) values 
(1);

/*Table structure for table `certificate` */

DROP TABLE IF EXISTS `certificate`;

CREATE TABLE `certificate` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reqid` int(11) DEFAULT NULL,
  `slid` int(11) DEFAULT NULL,
  `certificate` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `certificate` */

insert  into `certificate`(`id`,`reqid`,`slid`,`certificate`,`date`) values 
(1,1,2,'1.png','2023-05-09');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `complaint` varchar(20) DEFAULT NULL,
  `reply` varchar(30) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`id`,`lid`,`complaint`,`reply`,`date`) values 
(1,3,'not well services','ok','2023-05-08');

/*Table structure for table `location` */

DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `not_id` int(11) NOT NULL AUTO_INCREMENT,
  `scrap_id` int(11) DEFAULT NULL,
  `latitude` varchar(25) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`not_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `location` */

insert  into `location`(`not_id`,`scrap_id`,`latitude`,`longitude`) values 
(1,2,'11.25','75.25');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `password` varchar(30) NOT NULL,
  `type` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`id`,`username`,`password`,`type`) values 
(1,'admin','admin','admin'),
(2,'s','s','scraper'),
(3,'u','u','user');

/*Table structure for table `price_info` */

DROP TABLE IF EXISTS `price_info`;

CREATE TABLE `price_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reqid` int(11) DEFAULT NULL,
  `price` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `price_info` */

insert  into `price_info`(`id`,`reqid`,`price`) values 
(1,1,30000);

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ulid` int(11) DEFAULT NULL,
  `slid` int(11) DEFAULT NULL,
  `rating` varchar(40) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`id`,`ulid`,`slid`,`rating`,`date`) values 
(1,3,2,'5','2023-05-08');

/*Table structure for table `scrap` */

DROP TABLE IF EXISTS `scrap`;

CREATE TABLE `scrap` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `fname` varchar(30) DEFAULT NULL,
  `lname` varchar(30) DEFAULT NULL,
  `place` varchar(20) DEFAULT NULL,
  `post` varchar(34) DEFAULT NULL,
  `pin` bigint(20) DEFAULT NULL,
  `email` varchar(40) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `scrap` */

insert  into `scrap`(`id`,`lid`,`fname`,`lname`,`place`,`post`,`pin`,`email`,`phone`) values 
(1,2,'PKB','scrap','kannur','kannur',674523,'pk@gmail.com',9854126357);

/*Table structure for table `scraprequest` */

DROP TABLE IF EXISTS `scraprequest`;

CREATE TABLE `scraprequest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lid` int(11) DEFAULT NULL,
  `carid` int(11) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  `date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `scraprequest` */

insert  into `scraprequest`(`id`,`lid`,`carid`,`status`,`date`) values 
(1,2,1,'Certified','2023-05-08'),
(2,2,2,'verified by Scraper','2023-05-09');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

-- CREATE TABLE `user` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `lid` int(11) DEFAULT NULL,
--   `fname` varchar(30) DEFAULT NULL,
--   `lname` varchar(30) DEFAULT NULL,
--   `gender` varchar(30) DEFAULT NULL,
--   `place` varchar(30) DEFAULT NULL,
--   `post` varchar(30) DEFAULT NULL,
--   `pin` bigint(20) DEFAULT NULL,
--   `email` varchar(30) DEFAULT NULL,
--   `phone` bigint(20) DEFAULT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`id`,`lid`,`fname`,`lname`,`gender`,`place`,`post`,`pin`,`email`,`phone`) values 
(1,3,'jinoj','p','male','palakkad','palakkad',635478,'jinoj@gmail.com',9758621453);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

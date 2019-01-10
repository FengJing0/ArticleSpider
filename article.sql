/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 100130
Source Host           : localhost:3306
Source Database       : article_spider

Target Server Type    : MYSQL
Target Server Version : 100130
File Encoding         : 65001

Date: 2019-01-09 17:11:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `jobble_article`;
CREATE TABLE `jobble_article` (
  `title` varchar(255) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(255) DEFAULT NULL,
  `praise_nums` int(11) NOT NULL DEFAULT '0',
  `fav_nums` int(11) NOT NULL DEFAULT '0',
  `comment_nums` int(11) NOT NULL DEFAULT '0',
  `tags` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

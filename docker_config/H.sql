/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80021
 Source Host           : localhost:3306
 Source Schema         : H

 Target Server Type    : MySQL
 Target Server Version : 80021
 File Encoding         : 65001

 Date: 11/10/2021 10:53:54
*/
SET GLOBAL sort_buffer_size = 1024*1024;

USE mysql;
UPDATE user SET plugin='mysql_native_password' WHERE User='root';
update mysql.user set authentication_string=password('root') where user='root' and Host = 'localhost';
flush privileges;

CREATE DATABASE IF NOT EXISTS H;
USE H;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for Blacklist
-- ----------------------------
DROP TABLE IF EXISTS `Blacklist`;
CREATE TABLE `Blacklist` (
  `id` int NOT NULL AUTO_INCREMENT,
  `black_name` varchar(128) DEFAULT NULL,
  `black_time` varchar(128) DEFAULT NULL,
  `black_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `black_name` (`black_name`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Cronjob
-- ----------------------------
DROP TABLE IF EXISTS `Cronjob`;
CREATE TABLE `Cronjob` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cornjob_name` varchar(128) DEFAULT NULL,
  `cornjob_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Dirb
-- ----------------------------
DROP TABLE IF EXISTS `Dirb`;
CREATE TABLE `Dirb` (
  `id` int NOT NULL AUTO_INCREMENT,
  `dir_base` varchar(128) DEFAULT NULL,
  `dir_path` varchar(128) DEFAULT NULL,
  `dir_status` varchar(128) DEFAULT NULL,
  `dir_length` varchar(128) DEFAULT NULL,
  `dir_title` varchar(128) DEFAULT NULL,
  `dir_time` varchar(128) DEFAULT NULL,
  `dir_http` int DEFAULT NULL,
  `dir_tool` varchar(128) DEFAULT NULL,
  `dir_user` varchar(128) DEFAULT NULL,
  `dir_new` int DEFAULT NULL,
  `dir_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dir_base` (`dir_base`)
) ENGINE=InnoDB AUTO_INCREMENT=521 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Domain
-- ----------------------------
DROP TABLE IF EXISTS `Domain`;
CREATE TABLE `Domain` (
  `id` int NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(128) DEFAULT NULL,
  `domain_user` varchar(128) DEFAULT NULL,
  `domain_time` varchar(128) DEFAULT NULL,
  `domain_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Http
-- ----------------------------
DROP TABLE IF EXISTS `Http`;
CREATE TABLE `Http` (
  `id` int NOT NULL AUTO_INCREMENT,
  `http_schema` varchar(128) DEFAULT NULL,
  `http_name` varchar(128) DEFAULT NULL,
  `http_title` varchar(128) DEFAULT NULL,
  `http_status` varchar(128) DEFAULT NULL,
  `http_length` varchar(128) DEFAULT NULL,
  `http_screen` longtext,
  `http_finger` varchar(128) DEFAULT NULL,
  `http_see` tinyint(1) DEFAULT NULL,
  `http_new` int DEFAULT NULL,
  `http_time` varchar(128) DEFAULT NULL,
  `http_user` varchar(128) DEFAULT NULL,
  `http_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `http_name` (`http_name`),
  CONSTRAINT `http_chk_1` CHECK ((`http_see` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Port
-- ----------------------------
DROP TABLE IF EXISTS `Port`;
CREATE TABLE `Port` (
  `id` int NOT NULL AUTO_INCREMENT,
  `port_domain` varchar(128) DEFAULT NULL,
  `port_ip` varchar(128) DEFAULT NULL,
  `port_port` varchar(128) DEFAULT NULL,
  `port_server` varchar(128) DEFAULT NULL,
  `port_http_status` tinyint(1) DEFAULT NULL,
  `port_time` varchar(128) DEFAULT NULL,
  `port_user` varchar(128) DEFAULT NULL,
  `port_new` int DEFAULT NULL,
  `port_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `port_chk_1` CHECK ((`port_http_status` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=126 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Scancron
-- ----------------------------
DROP TABLE IF EXISTS `Scancron`;
CREATE TABLE `Scancron` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scancron_name` varchar(20) DEFAULT NULL,
  `scancron_month` varchar(20) DEFAULT NULL,
  `scancron_week` varchar(20) DEFAULT NULL,
  `scancron_day` varchar(20) DEFAULT NULL,
  `scancron_hour` varchar(20) DEFAULT NULL,
  `scancron_min` varchar(20) DEFAULT NULL,
  `scancron_time` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Scanmethod
-- ----------------------------
DROP TABLE IF EXISTS `Scanmethod`;
CREATE TABLE `Scanmethod` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scanmethod_name` varchar(128) DEFAULT NULL,
  `scanmethod_subfinder` tinyint(1) DEFAULT NULL,
  `scanmethod_amass` tinyint(1) DEFAULT NULL,
  `scanmethod_shuffledns` tinyint(1) DEFAULT NULL,
  `scanmethod_second` tinyint(1) DEFAULT NULL,
  `scanmethod_port` tinyint(1) DEFAULT NULL,
  `scanmethod_port_portlist` varchar(128) DEFAULT NULL,
  `scanmethod_port_dfportlist` varchar(255) DEFAULT NULL,
  `scanmethod_httpx` tinyint(1) DEFAULT NULL,
  `scanmethod_ehole` tinyint(1) DEFAULT NULL,
  `scanmethod_screenshot` tinyint(1) DEFAULT NULL,
  `scanmethod_jsfinder` tinyint(1) DEFAULT NULL,
  `scanmethod_dirb` tinyint(1) DEFAULT NULL,
  `scanmethod_dirb_wordlist` varchar(128) DEFAULT NULL,
  `scanmethod_xray` tinyint(1) DEFAULT NULL,
  `scanmethod_nuclei` tinyint(1) DEFAULT NULL,
  `scanmethod_nuclei_my` tinyint(1) DEFAULT NULL,
  `scanmethod_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `scanmethod_chk_1` CHECK ((`scanmethod_subfinder` in (0,1))),
  CONSTRAINT `scanmethod_chk_11` CHECK ((`scanmethod_dirb` in (0,1))),
  CONSTRAINT `scanmethod_chk_12` CHECK ((`scanmethod_xray` in (0,1))),
  CONSTRAINT `scanmethod_chk_13` CHECK ((`scanmethod_nuclei` in (0,1))),
  CONSTRAINT `scanmethod_chk_14` CHECK ((`scanmethod_nuclei_my` in (0,1))),
  CONSTRAINT `scanmethod_chk_2` CHECK ((`scanmethod_amass` in (0,1))),
  CONSTRAINT `scanmethod_chk_3` CHECK ((`scanmethod_shuffledns` in (0,1))),
  CONSTRAINT `scanmethod_chk_5` CHECK ((`scanmethod_port` in (0,1))),
  CONSTRAINT `scanmethod_chk_6` CHECK ((`scanmethod_httpx` in (0,1))),
  CONSTRAINT `scanmethod_chk_7` CHECK ((`scanmethod_ehole` in (0,1))),
  CONSTRAINT `scanmethod_chk_8` CHECK ((`scanmethod_screenshot` in (0,1))),
  CONSTRAINT `scanmethod_chk_9` CHECK ((`scanmethod_jsfinder` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Subdomain
-- ----------------------------
DROP TABLE IF EXISTS `Subdomain`;
CREATE TABLE `Subdomain` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subdomain_name` varchar(128) DEFAULT NULL,
  `subdomain_ip` varchar(128) DEFAULT NULL,
  `subdomain_info` varchar(128) DEFAULT NULL,
  `subdomain_tool` varchar(128) DEFAULT NULL,
  `subdomain_user` varchar(128) DEFAULT NULL,
  `subdomain_new` int DEFAULT NULL,
  `subdomain_time` varchar(128) DEFAULT NULL,
  `subdomain_target` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `subdomain_name` (`subdomain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=451 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Sysconfig
-- ----------------------------
DROP TABLE IF EXISTS `Sysconfig`;
CREATE TABLE `Sysconfig` (
  `id` int NOT NULL AUTO_INCREMENT,
  `config_email_username` varchar(128) DEFAULT NULL,
  `config_email_password` varchar(128) DEFAULT NULL,
  `config_email_server` varchar(128) DEFAULT NULL,
  `config_email_get` longtext,
  `config_subdomain` tinyint(1) DEFAULT NULL,
  `config_port` tinyint(1) DEFAULT NULL,
  `config_http` tinyint(1) DEFAULT NULL,
  `config_vuln` tinyint(1) DEFAULT NULL,
  `config_vuln_github` varchar(128) DEFAULT NULL,
  `config_count` int DEFAULT NULL,
  `config_push_hour` varchar(128) DEFAULT NULL,
  `config_xray` tinyint(1) DEFAULT NULL,
  `config_vuln_my` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sysconfig_chk_1` CHECK ((`config_subdomain` in (0,1))),
  CONSTRAINT `sysconfig_chk_2` CHECK ((`config_port` in (0,1))),
  CONSTRAINT `sysconfig_chk_3` CHECK ((`config_http` in (0,1))),
  CONSTRAINT `sysconfig_chk_4` CHECK ((`config_vuln` in (0,1))),
  CONSTRAINT `sysconfig_chk_5` CHECK ((`config_xray` in (0,1))),
  CONSTRAINT `sysconfig_chk_6` CHECK ((`config_vuln_my` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Target
-- ----------------------------
DROP TABLE IF EXISTS `Target`;
CREATE TABLE `Target` (
  `id` int NOT NULL AUTO_INCREMENT,
  `target_name` varchar(128) DEFAULT NULL,
  `target_description` varchar(128) DEFAULT NULL,
  `target_method` varchar(128) DEFAULT NULL,
  `target_cron` tinyint(1) DEFAULT NULL,
  `target_cron_id` varchar(128) DEFAULT NULL,
  `target_status` int DEFAULT NULL,
  `target_user` varchar(128) DEFAULT NULL,
  `target_pid` int DEFAULT NULL,
  `target_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `target_chk_1` CHECK ((`target_cron` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for User
-- ----------------------------
DROP TABLE IF EXISTS `User`;
CREATE TABLE `User` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(128) DEFAULT NULL,
  `password` binary(255) DEFAULT NULL,
  `isadmin` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 ;

-- ----------------------------
-- Table structure for Vuln
-- ----------------------------
DROP TABLE IF EXISTS `Vuln`;
CREATE TABLE `Vuln` (
  `id` int NOT NULL AUTO_INCREMENT,
  `vuln_mainkey` varchar(128) DEFAULT NULL,
  `vuln_name` varchar(128) DEFAULT NULL,
  `vuln_info` varchar(128) DEFAULT NULL,
  `vuln_level` varchar(128) DEFAULT NULL,
  `vuln_poc` longtext CHARACTER SET utf8mb4,
  `vuln_http` varchar(128) DEFAULT NULL,
  `vuln_target` int DEFAULT NULL,
  `vuln_user` varchar(128) DEFAULT NULL,
  `vuln_new` int DEFAULT NULL,
  `vuln_tool` varchar(128) DEFAULT NULL,
  `vuln_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vuln_mainkey` (`vuln_mainkey`)
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=utf8mb4 ;

SET FOREIGN_KEY_CHECKS = 1;

insert into User value('1','admin','5e59601e941c93866169e1d23d876b7afc741cf69e60de3becb065d8253d5ec490d0811d8b94769a8aa1e6c0fddde853620b63d02b7bfe2eb9cf05e6304149da78288db52267c11d43fcfe9c80b6f6eb90b51172ca150a3bca52b788d11e0bd1','1');

insert into Sysconfig value('1','admin','admin','stmp.qq.com','123@qq.com','1','1','1','1','https://username:password@gitee.com/xxxx/xxx.git','2','18','0','0');
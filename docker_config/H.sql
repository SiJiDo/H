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

 Date: 29/10/2021 15:41:43
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for Cronjob
-- ----------------------------
DROP TABLE IF EXISTS `Cronjob`;
CREATE TABLE `Cronjob` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cronjob_pid` varchar(128) CHARACTER SET utf8mb4 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=521 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for Indexnote
-- ----------------------------
DROP TABLE IF EXISTS `Indexnote`;
CREATE TABLE `Indexnote` (
  `id` int NOT NULL AUTO_INCREMENT,
  `index_note` longtext,
  `index_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for plugins_Hostcrack
-- ----------------------------
DROP TABLE IF EXISTS `plugins_Hostcrack`;
CREATE TABLE `plugins_Hostcrack` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hostcrack_domain` longtext,
  `hostcrack_ip` longtext,
  `hostcrack_result` longtext,
  `hostcrack_pid` varchar(128) DEFAULT NULL,
  `hostcrack_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for plugins_Icp
-- ----------------------------
DROP TABLE IF EXISTS `plugins_Icp`;
CREATE TABLE `plugins_Icp` (
  `id` int NOT NULL AUTO_INCREMENT,
  `icp_cookie` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for Runlog
-- ----------------------------
DROP TABLE IF EXISTS `Runlog`;
CREATE TABLE `Runlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `log_info` longtext,
  `log_time` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Table structure for Celerytask
-- ----------------------------
DROP TABLE IF EXISTS `Celerytask`;
CREATE TABLE `Celerytask` (
  `id` int NOT NULL AUTO_INCREMENT,
  `celery_target` int DEFAULT NULL,
  `celery_id` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=460 DEFAULT CHARSET=utf8mb4;

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
  `config_info` tinyint(1) DEFAULT NULL,
  `config_vuln` tinyint(1) DEFAULT NULL,
  `config_vuln_github` varchar(128) DEFAULT NULL,
  `config_count` int DEFAULT NULL,
  `config_push_hour` varchar(128) DEFAULT NULL,
  `config_xray` tinyint(1) DEFAULT NULL,
  `config_vuln_my` tinyint(1) DEFAULT NULL,
  `config_nuclei_day` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `sysconfig_chk_1` CHECK ((`config_info` in (0,1))),
  CONSTRAINT `sysconfig_chk_2` CHECK ((`config_vuln` in (0,1))),
  CONSTRAINT `sysconfig_chk_3` CHECK ((`config_xray` in (0,1))),
  CONSTRAINT `sysconfig_chk_4` CHECK ((`config_vuln_my` in (0,1))),
  CONSTRAINT `sysconfig_chk_5` CHECK ((`config_nuclei_day` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB AUTO_INCREMENT=213 DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

insert into User value('1','admin','5e59601e941c93866169e1d23d876b7afc741cf69e60de3becb065d8253d5ec490d0811d8b94769a8aa1e6c0fddde853620b63d02b7bfe2eb9cf05e6304149da78288db52267c11d43fcfe9c80b6f6eb90b51172ca150a3bca52b788d11e0bd1','1');

insert into Sysconfig value('1','admin','admin','smtp.qq.com','123@qq.com','1','1','https://username:password@gitee.com/xxxx/xxx.git','2','18','0','0','0');

insert into Cronjob value('1','0');

insert into plugins_Icp value('1', '');

INSERT INTO `H`.`Indexnote`(`id`, `index_note`, `index_time`) VALUES (1, '漏洞多多,奖励多多,天天sql注入,月月rce\r\n详细项目地址可见:https://github.com/SiJiDo/H\r\n\r\n搜索语法介绍:\r\n我们可以在站点识别模块使用 target=电信&&title=四川 来获取电信项目中是标题带有四川的资产 \r\n\r\n具体的搜索字段如下，对于所有模块均有\r\ntarget = 项目名\r\nnew = true (新增资产)\r\nstart_time = 资产添加起始时间\r\nend_time = 资产添加终止时间\r\n\r\n子域名模块独有搜索语法\r\nsubdomain = 子域名\r\nip = ip地址\r\n\r\n端口收集模块独有搜索语法\r\nsubdomain = 域名\r\nip = ip地址\r\nport = 端口\r\nserver = 服务\r\n\r\n站点识别模块独有搜索语法\r\nurl = url路径\r\ntitle = 标题\r\nstatus = 响应码\r\finger = 指纹\r\n\r\n目录扫描模块独有搜索语法\r\nurl = url路径\r\ntitle = 标题\r\nstatus = 响应码\r\ntool = 收集工具\r\n\r\n漏洞扫描模块独有搜索语法\r\nurl = url路径\r\nlevel = 漏洞危害等级\r\ninfo = 漏洞信息\r\ntool = 收集工具\r\n', '2021-11-08  15:42:17');
INSERT INTO `H`.`Scancron`(`id`, `scancron_name`, `scancron_month`, `scancron_week`, `scancron_day`, `scancron_hour`, `scancron_min`, `scancron_time`) VALUES (1, 'example', '*', '*', '1', '0', '0', '0');
INSERT INTO `H`.`Scanmethod`(`id`, `scanmethod_name`, `scanmethod_subfinder`, `scanmethod_amass`, `scanmethod_shuffledns`, `scanmethod_second`, `scanmethod_port`, `scanmethod_port_portlist`, `scanmethod_port_dfportlist`, `scanmethod_httpx`, `scanmethod_ehole`, `scanmethod_screenshot`, `scanmethod_jsfinder`, `scanmethod_dirb`, `scanmethod_dirb_wordlist`, `scanmethod_xray`, `scanmethod_nuclei`, `scanmethod_nuclei_my`, `scanmethod_time`) VALUES (1, 'full', 1, 1, 1, 1, 1, 'all', '', 1, 1, 1, 1, 1, 'top1000', 1, 1, 1, '2021-11-08  15:43:50');
INSERT INTO `H`.`Scanmethod`(`id`, `scanmethod_name`, `scanmethod_subfinder`, `scanmethod_amass`, `scanmethod_shuffledns`, `scanmethod_second`, `scanmethod_port`, `scanmethod_port_portlist`, `scanmethod_port_dfportlist`, `scanmethod_httpx`, `scanmethod_ehole`, `scanmethod_screenshot`, `scanmethod_jsfinder`, `scanmethod_dirb`, `scanmethod_dirb_wordlist`, `scanmethod_xray`, `scanmethod_nuclei`, `scanmethod_nuclei_my`, `scanmethod_time`) VALUES (2, 'normal', 1, 0, 1, 0, 1, 'top100', '', 1, 1, 1, 1, 1, 'top100', 0, 0, 0, '2021-11-08  15:47:53');

insert into Runlog value('1', '欢迎使用H资产收集器', '1998-03-31 0:00:00');

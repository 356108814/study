/*
Navicat MySQL Data Transfer

Source Server         : 本机
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : aimei_data

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2016-08-19 17:05:30
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for t_data_aimei_consum_total
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_consum_total`;
CREATE TABLE `t_data_aimei_consum_total` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `time_span` varchar(10) NOT NULL,
  `p_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`time_span`,`p_type`,`m_type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=80121 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_mid_consum_detail
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_mid_consum_detail`;
CREATE TABLE `t_data_aimei_mid_consum_detail` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(11) unsigned NOT NULL,
  `p_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `action_time` int(11) unsigned NOT NULL,
  `coin_price` int(11) unsigned NOT NULL,
  `coin_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  `auto_idx` bigint(20) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89376 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_mid_consum_total_201606
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_mid_consum_total_201606`;
CREATE TABLE `t_data_aimei_mid_consum_total_201606` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(11) unsigned NOT NULL,
  `p_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `time_span` smallint(6) NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`mid`,`p_type`,`c_type`,`m_type`,`time_span`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_mid_consum_total_201607
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_mid_consum_total_201607`;
CREATE TABLE `t_data_aimei_mid_consum_total_201607` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(11) unsigned NOT NULL,
  `p_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `time_span` smallint(6) NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`mid`,`p_type`,`c_type`,`m_type`,`time_span`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=405190 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_mid_consum_total_201608
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_mid_consum_total_201608`;
CREATE TABLE `t_data_aimei_mid_consum_total_201608` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `mid` int(11) unsigned NOT NULL,
  `p_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `time_span` smallint(6) NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`mid`,`p_type`,`c_type`,`m_type`,`time_span`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_user_action_201608
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_user_action_201608`;
CREATE TABLE `t_data_aimei_user_action_201608` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) DEFAULT NULL,
  `p_type` char(1) DEFAULT NULL,
  `t_type` char(1) DEFAULT NULL,
  `a_type` char(1) DEFAULT NULL,
  `action_time` bigint(20) DEFAULT NULL,
  `location` int(11) DEFAULT NULL,
  `aimei_object` varchar(64) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=284244 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_user_action_mob_201608
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_user_action_mob_201608`;
CREATE TABLE `t_data_aimei_user_action_mob_201608` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `p_type` char(1) DEFAULT NULL,
  `a_type` char(1) DEFAULT NULL,
  `provinceid` smallint(6) DEFAULT NULL,
  `isp` smallint(255) DEFAULT NULL,
  `time_span` smallint(6) DEFAULT NULL COMMENT 'ddhh，一小时一条记录， 15号16点的记录， 1516',
  `aimei_object` varchar(64) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `t_type` (`p_type`,`a_type`,`provinceid`,`isp`,`time_span`,`aimei_object`)
) ENGINE=MyISAM AUTO_INCREMENT=67178 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_user_consum_201606
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_user_consum_201606`;
CREATE TABLE `t_data_aimei_user_consum_201606` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `jobid` varchar(64) NOT NULL DEFAULT '',
  `p_type` varchar(1) DEFAULT '0',
  `t_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `action_time` int(11) unsigned NOT NULL,
  `auto_idx` int(11) unsigned NOT NULL,
  `location` int(11) unsigned NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`p_type`,`t_type`,`c_type`,`m_type`,`action_time`,`auto_idx`,`location`) USING BTREE,
  KEY `key_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_user_consum_201607
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_user_consum_201607`;
CREATE TABLE `t_data_aimei_user_consum_201607` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `jobid` varchar(64) NOT NULL DEFAULT '',
  `p_type` varchar(1) DEFAULT '0',
  `t_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `action_time` int(11) unsigned NOT NULL,
  `auto_idx` int(11) unsigned NOT NULL,
  `location` int(11) unsigned NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`p_type`,`t_type`,`c_type`,`m_type`,`action_time`,`auto_idx`,`location`) USING BTREE,
  KEY `key_uid` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=406991 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for t_data_aimei_user_consum_201608
-- ----------------------------
DROP TABLE IF EXISTS `t_data_aimei_user_consum_201608`;
CREATE TABLE `t_data_aimei_user_consum_201608` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `uid` int(11) unsigned NOT NULL,
  `jobid` varchar(64) NOT NULL DEFAULT '',
  `p_type` varchar(1) DEFAULT '0',
  `t_type` varchar(1) DEFAULT '0',
  `c_type` varchar(1) DEFAULT '0',
  `m_type` varchar(1) DEFAULT '0',
  `action_time` int(11) unsigned NOT NULL,
  `auto_idx` int(11) unsigned NOT NULL,
  `location` int(11) unsigned NOT NULL,
  `money_count` int(11) unsigned NOT NULL,
  `update_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_id` (`p_type`,`t_type`,`c_type`,`m_type`,`action_time`,`auto_idx`,`location`) USING BTREE,
  KEY `key_uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_data_aimei_user_consum_201608` (
	  `id` int(11) unsigned NOT NULL AUTO_INCREMENT, 
	  `uid` int(11) unsigned NOT NULL,
	  `jobid` varchar(64) NOT NULL DEFAULT '',
	  `p_type` varchar(1) default '0',
	  `t_type` varchar(1) default '0',
	  `c_type` varchar(1) default '0',
	  `m_type` varchar(1) default '0',
	  `action_time` int(11) unsigned NOT NULL,
	  `auto_idx` int(11) unsigned NOT NULL,
	  `location` int(11) unsigned NOT NULL,
	  `money_count` int(11) unsigned NOT NULL,
	  `update_time` datetime not null,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `uniq_id` (p_type, t_type, c_type, m_type, action_time, auto_idx, location) USING BTREE,
	  KEY `key_uid` (uid)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `t_data_aimei_mid_consum_detail` (
	  `id` int(11) unsigned NOT NULL AUTO_INCREMENT, 
	  `mid` int(11) unsigned NOT NULL,
	  `p_type` varchar(1) default '0',
	  `m_type` varchar(1) default '0',
	  `action_time` int(11) unsigned NOT NULL,
	  `coin_price` int(11) unsigned NOT NULL,
	  `coin_count` int(11) unsigned NOT NULL,
	  `update_time` datetime not null,
	  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `t_data_aimei_mid_consum_total_201608` (
	  `id` int(11) unsigned NOT NULL AUTO_INCREMENT, 
	  `mid` int(11) unsigned NOT NULL,
	  `p_type` varchar(1) default '0',
	  `c_type` varchar(1) default '0',
	  `m_type` varchar(1) default '0',
	  `time_span` smallint NOT NULL,
	  `money_count` int(11) unsigned NOT NULL,
	  `update_time` datetime not null,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `uniq_id` (mid, p_type, c_type, m_type, time_span) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `t_data_aimei_consum_total` (
	  `id` int(11) unsigned NOT NULL AUTO_INCREMENT, 
	  `time_span` varchar(10) NOT NULL,
	  `p_type` varchar(1) default '0',
	  `m_type` varchar(1) default '0',
	  `money_count` int(11) unsigned NOT NULL,
	  `update_time` datetime not null,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `uniq_id` (time_span, p_type, m_type) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

extern int mylogfd;

int connector_entryHandler_macPlayingModeGameOverV2(time_t cur, int mid, cJSON *req)
{
	return 0;
}

typedef struct {
	uint32_t uid;
	int mid;
	int coin_count;
	int coin_price;
	int idx;
	time_t t;
	uint8_t c_type;
	uint8_t m_type;
} t_aimei_data_account_base;

static int connector_entryHandler_accountRecordInfo_sub(t_aimei_data_account_base *m)
{
	char sql[512] = {0x0};
	char date[32] = { 0 };
	get_strtime_by_format_and_time("%Y%m%d%H%M%S", &(m->t), date, sizeof(date));

	int mcount = m->coin_count * m->coin_price;
	snprintf(sql, sizeof(sql), "insert into t_data_aimei_user_consum_%.*s(id, uid, jobid, p_type, t_type, c_type, m_type, action_time, auto_idx, location, money_count, update_time) values(NULL, %u, '', %d, %d, %d, %d, %ld, %d, %u, %d, now()) ", 6, date, m->uid, AIMEI_PRODUCT_TYPE_MINIK, AIMEI_TERMINAL_TYPE_MACHINE, m->c_type, m->m_type, m->t, m->idx, m->mid, mcount);
	if (mysql_query(mysql, sql)) 
	{
		LOG(mylogfd, LOG_ERROR, "mysql_query error:%s:[%s]\n", mysql_error(mysql), sql);
		mysql_ping(mysql);
		return -1;
	}

	if (m->m_type == MONEY_ID_FREE_TICKET)
	{
		LOG(mylogfd, LOG_TRACE, "%s %d %d %d\n", __func__, __LINE__, m->c_type, m->m_type);
		return 0;
	}

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "insert into t_data_aimei_mid_consum_total_%.*s(id, mid, p_type, c_type, time_span, m_type, money_count, update_time) values(NULL, %d, %u, %u, %.*s, '%u', %d, now()) on duplicate key update money_count = money_count + %d, update_time = now()", 6, date, m->mid, AIMEI_PRODUCT_TYPE_MINIK, m->c_type, 4, date + 6, m->m_type, mcount, mcount);
	if (mysql_query(mysql, sql)) 
	{
		LOG(mylogfd, LOG_ERROR, "mysql_query error:%s:[%s]\n", mysql_error(mysql), sql);
		mysql_ping(mysql);
		return -1;
	}

	if (m->c_type != MONEY_BE_USED)
	{
		LOG(mylogfd, LOG_TRACE, "%s %d %d %d\n", __func__, __LINE__, m->c_type, m->m_type);
		return 0;
	}

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "insert into t_data_aimei_consum_total(id, time_span, p_type, m_type, money_count, update_time) values(NULL, %.*s, '%u', '%u', %d, now()) on duplicate key update money_count = money_count + %d, update_time = now()", 10, date, AIMEI_PRODUCT_TYPE_MINIK, m->m_type, mcount, mcount);
	if (mysql_query(mysql, sql)) 
	{
		LOG(mylogfd, LOG_ERROR, "mysql_query error:%s:[%s]\n", mysql_error(mysql), sql);
		mysql_ping(mysql);
		return -1;
	}

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "insert into t_data_aimei_mid_consum_detail(id, mid, p_type, action_time, coin_price, m_type, coin_count, update_time) values(NULL, %d, %d, %ld, %d, '%u', %d, now()) ", m->mid, AIMEI_PRODUCT_TYPE_MINIK, m->t, m->coin_price, m->m_type, m->coin_count);
	if (mysql_query(mysql, sql)) 
	{
		LOG(mylogfd, LOG_ERROR, "mysql_query error:%s:[%s]\n", mysql_error(mysql), sql);
		mysql_ping(mysql);
		return -1;
	}

	return 0;
}

int connector_entryHandler_accountRecordInfo(time_t cur, int mid, cJSON *req)
{
	cJSON *timestamp = cJSON_GetObjectItem(req, "timestamp");
	cJSON *type = cJSON_GetObjectItem(req, "type");
	cJSON *coin_price = cJSON_GetObjectItem(req, "coin_price");
	cJSON *coin = cJSON_GetObjectItem(req, "coin");
	cJSON *free_ticket = cJSON_GetObjectItem(req, "free_ticket");
	cJSON *mobile_pay = cJSON_GetObjectItem(req, "mobile_pay");
	cJSON *suid = cJSON_GetObjectItem(req, "uid");
	cJSON *auto_idx = cJSON_GetObjectItem(req, "auto_idx");

	if (!timestamp || !type || !coin_price || !coin || !free_ticket || !mobile_pay || !auto_idx
			|| timestamp->type != cJSON_Number
			|| type->type != cJSON_Number || coin_price->type != cJSON_Number || auto_idx->type != cJSON_Number
			|| coin->type != cJSON_Number || mobile_pay->type != cJSON_Number || free_ticket->type != cJSON_Number) 
	{
		LOG(mylogfd, LOG_ERROR, "%s %d error\n", __func__, __LINE__);
		return -1;
	}

	if (coin_price->valueint == 0)
	{
		LOG(mylogfd, LOG_ERROR, "%s %d mid = %d error\n", __func__, __LINE__, mid);
		return -1;
	}

	char date[32] = { 0 };
	time_t t = timestamp->valueint;
	get_strtime_by_format_and_time("%Y%m%d", &t, date, sizeof(date));

	uint32_t uid = 0;
	if (suid && suid->type == cJSON_String && suid->valuestring)
		uid = atol(suid->valuestring);
	uint8_t oper_type = type->valueint + 1;

	if (oper_type > MONEY_WRITE_OFF || oper_type < MONEY_PRE_SUB)
	{
		LOG(mylogfd, LOG_ERROR, "%s %d error %u\n", __func__, __LINE__, oper_type);
		return -1;
	}

	t_aimei_data_account_base m;
	m.uid = uid;
	m.mid = mid;
	m.idx = auto_idx->valueint;
	m.t = t;
	m.c_type = oper_type;
	m.coin_price = coin_price->valueint;

	if(coin->valueint)
	{
		m.coin_count = coin->valueint;
		m.m_type = MONEY_ID_CASH;
		if (connector_entryHandler_accountRecordInfo_sub(&m))
		{
			LOG(mylogfd, LOG_ERROR, "%s %d error %u\n", __func__, __LINE__, oper_type);
			return -1;
		}
	}

	if(free_ticket->valueint)
	{
		m.coin_count = free_ticket->valueint;
		m.m_type = MONEY_ID_FREE_TICKET;
		if (connector_entryHandler_accountRecordInfo_sub(&m))
		{
			LOG(mylogfd, LOG_ERROR, "%s %d error %u\n", __func__, __LINE__, oper_type);
			return -1;
		}
	}

	if(mobile_pay->valueint)
	{
		m.coin_count = mobile_pay->valueint;
		m.m_type = MONEY_ID_WEIXIN_PAY;
		if (connector_entryHandler_accountRecordInfo_sub(&m))
		{
			LOG(mylogfd, LOG_ERROR, "%s %d error %u\n", __func__, __LINE__, oper_type);
			return -1;
		}
	}

	return 0;
}

t_minik_logic_log_db_cb_s minik_log_cball[MINIK_LOGIC_LOG_COUNT] = 
{
	{"connector.entryHandler.macPlayingModeGameOverV2", sizeof("connector.entryHandler.macPlayingModeGameOverV2") - 1, connector_entryHandler_macPlayingModeGameOverV2},
	{"connector.entryHandler.accountRecordInfo", sizeof("connector.entryHandler.accountRecordInfo") - 1, connector_entryHandler_accountRecordInfo}
};

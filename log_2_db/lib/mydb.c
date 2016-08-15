#include <stdlib.h>
#include "mydb.h"

int lib_connect_db(t_db_info *db, MYSQL * mysql)
{
    mysql_init(mysql);
	mysql_options(mysql, MYSQL_SET_CHARSET_NAME, "gbk");
	mysql_options(mysql, MYSQL_SET_CHARSET_NAME, "utf8");

	int reconnect = 1;
	mysql_options(mysql, MYSQL_OPT_RECONNECT, (my_bool *)&reconnect);
    if (NULL == mysql_real_connect(mysql, db->host, db->username, db->passwd, db->db, db->port, NULL, 0))
		return -1;

	char sql[128] = {0x0};
	snprintf(sql, sizeof(sql), "set SESSION wait_timeout=86400");
	if (mysql_query(mysql, sql))
		return -1;

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "set autocommit=1");
	if (mysql_query(mysql, sql))
		return -1;
	return 0;
}

void close_db(MYSQL* mysql)
{
    mysql_close(mysql);
}

uint32_t get_sel_count(MYSQL* mysql, char *sql)
{
	uint32_t ret = 0;
	if (mysql_query(mysql, sql))
		return 0;
	MYSQL_RES* result = mysql_store_result(mysql);
	if (result) 
	{
		MYSQL_ROW row = NULL;
		if (NULL != (row = mysql_fetch_row(result)))
		{
			if (row[0])
				ret = atol(row[0]);
		}
		mysql_free_result(result);
	}
    return ret;
}

int get_sel_count_by_default(MYSQL* mysql, char *sql, int predef)
{
	int ret = predef;
	if (mysql_query(mysql, sql))
		return ret;
	MYSQL_RES* result = mysql_store_result(mysql);
	if (result) 
	{
		MYSQL_ROW row = NULL;
		if (NULL != (row = mysql_fetch_row(result)))
		{
			if (row[0])
				ret = atol(row[0]);
		}
		mysql_free_result(result);
	}
    return ret;
}

int get_sel_mul_count(MYSQL* mysql, char *sql, long *ret, int n)
{
	if (mysql_query(mysql, sql))
		return -1;
	MYSQL_RES* result = mysql_store_result(mysql);
	if (result) 
	{
		MYSQL_ROW row = NULL;
		if (NULL != (row = mysql_fetch_row(result)))
		{
			int i = 0;
			for (; i < n; i++, ret++)
			{
				*ret = atol(row[i]);
			}
		}
		mysql_free_result(result);
	}
    return 0;
}

int get_sel_string(MYSQL* mysql, char *sql, char *buf, int buflen)
{
	int ret = -1;
	if (mysql_query(mysql, sql))
		return -1;
	MYSQL_RES* result = mysql_store_result(mysql);
	if (result) 
	{
		MYSQL_ROW row = NULL;
		if (NULL != (row = mysql_fetch_row(result)))
		{
			ret = 0;
			snprintf(buf, buflen, "%s", row[0]);
		}
		mysql_free_result(result);
	}
    return ret;
}

int mydb_begin(MYSQL* mysql)
{
	char sql[1024] = {0x0};
	snprintf(sql, sizeof(sql), "begin;");
    if (mysql_query(mysql, sql))
		return -1;
	return 0;
}

int mydb_commit(MYSQL* mysql)
{
	char sql[1024] = {0x0};
	snprintf(sql, sizeof(sql), "commit;");
    if (mysql_query(mysql, sql))
		return -1;
	return 0;
}

int mydb_rollback(MYSQL* mysql)
{
	char sql[1024] = {0x0};
	snprintf(sql, sizeof(sql), "rollback;");
    if (mysql_query(mysql, sql))
		return -1;
	return 0;
}

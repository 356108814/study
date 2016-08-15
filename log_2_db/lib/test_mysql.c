#include "mysqld_error.h"
#include <mysql.h>
#include <stdio.h>
#include <string.h>

MYSQL mysql0;
MYSQL * mysql = &mysql0;

int get_sel_count(char *sql)
{

	int ret = 0;
	if (mysql_query(mysql, sql))
		return -1;
	MYSQL_RES* result = mysql_store_result(mysql);
	if (result) 
	{
		MYSQL_ROW row = NULL;
		if (NULL != (row = mysql_fetch_row(result)))
		{
			ret = atoi(row[0]);
		}

		mysql_free_result(result);
	}
    
    return ret;
}

int main()
{
    mysql_init(mysql);
	mysql_options(mysql, MYSQL_SET_CHARSET_NAME, "gbk");

	int reconnect = 1;
	mysql_options(mysql, MYSQL_OPT_RECONNECT, (my_bool *)&reconnect);
    if (NULL == mysql_real_connect(mysql, "203.195.154.19", "kshow", "123456", "kshow", 3306, NULL, 0))
	{
		fprintf(stderr, "connect mysql error %s\n", mysql_error(mysql));
		return -1;
	}

	char sql[256] = {0x0};
	snprintf(sql, sizeof(sql), "call get_increment_id('user_id', @a, @b);");
	int a = get_sel_count(sql);
	if (a < 0)
	{
		fprintf(stderr, "connect mysql error %s\n", mysql_error(mysql));
		return -1;
	}
	fprintf(stdout, "%d\n", a);

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "select @b");
	a = get_sel_count(sql);
	if (a < 0)
	{
		fprintf(stderr, "connect mysql error %s\n", mysql_error(mysql));
		return -1;
	}
	fprintf(stdout, "%d\n", a);

	return 0;
}

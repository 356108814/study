#include "minik_logic_log.h"
#include "plugins.h"
#include "log.h"

static int mylogfd = -1;
#define SO_NAME "minik_logic_log"
static MYSQL *mysql;

int so_init(int logfd, MYSQL *h_mysql)
{
	mylogfd = logfd;
	mysql = h_mysql;
	return 0;
}

#include "minik_logic_log_sub.c"

int so_proc(char *buf)
{
	char *s = buf;
	char *t = strchr(s, '&');
	if (t == NULL)
	{
		LOG(mylogfd, LOG_ERROR, "%s %s %d %s\n", ID, FUNC, LN, s);
		return -1;
	}
	time_t cur = strtoul(s, NULL, 10);

	s = t + 1;
	t = strchr(s, '&');
	if (t == NULL)
	{
		LOG(mylogfd, LOG_ERROR, "%s %s %d %s\n", ID, FUNC, LN, s);
		return -1;
	}

	int mid = atoi(s);

	s = t + 1;
	t = strchr(s, '&');
	if (t == NULL)
	{
		LOG(mylogfd, LOG_ERROR, "%s %s %d %s\n", ID, FUNC, LN, s);
		return -1;
	}
	*t = 0x0;

	int ret = 0;
	int i = 0;
	for ( ; i < sizeof(minik_log_cball)/sizeof(t_minik_logic_log_db_cb_s); i++)
	{
		if (strncasecmp(s, minik_log_cball[i].router, minik_log_cball[i].len) == 0)
		{
			t++;
			char *v = strchr(t, '&');
			if(v != NULL)
				v = 0x0;

			cJSON *req = cJSON_Parse(t);
			if (req == NULL)
			{
				LOG(mylogfd, LOG_ERROR, "%s %s %d %m err \n", ID, FUNC, LN);
				return -1;
			}

			ret = minik_log_cball[i].cb(cur, mid, req);
			cJSON_Delete(req);
		}
	}

	return ret;
}

int so_fini()
{
	return 0;
}


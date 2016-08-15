#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <signal.h>
#include <errno.h>
#include "common.h"
#include "myconfig.h"
#include "log.h"
#include "c_api.h"
#include "plugins.h"
#include "aimei_data_config.h"

int log_2_db_log = -1;

volatile int g_stop = 0;

char *logfile_indir = NULL;
char *logfile_bkdir = NULL;
char *logfile_errdir = NULL;
int dir_recursive = 0;

static MYSQL mysql0;
static MYSQL *mysql = &mysql0;

static int connect_db(t_db_info *db)
{
    mysql_init(mysql);
	mysql_options(mysql, MYSQL_SET_CHARSET_NAME, "utf8");
	int reconnect = 1;
	mysql_options(mysql, MYSQL_OPT_RECONNECT, (my_bool *)&reconnect);
    if (NULL == mysql_real_connect(mysql, db->host, db->username, db->passwd, db->db, db->port, NULL, 0))
	{
		LOG(log_2_db_log, LOG_ERROR, "mysql_real_connect err %m\n");
		return -1;
	}
	LOG(log_2_db_log, LOG_NORMAL, "connect db ok %x\n", mysql);
	char sql[1024] = {0x0};
	snprintf(sql, sizeof(sql), "set SESSION wait_timeout=86400");
	if (mysql_query(mysql, sql))
	{
		LOG(log_2_db_log, LOG_ERROR, "mysql_query error:%s:[%s]\n", mysql_error(mysql), sql);
		return -1;
	}

	memset(sql, 0, sizeof(sql));
	snprintf(sql, sizeof(sql), "set autocommit=0");
	if (mysql_query(mysql, sql))
	{
		LOG(log_2_db_log, LOG_ERROR, "set autocommit=0 %s %d %s %s\n", __func__, __LINE__, mysql_error(mysql), sql);
		return -1;
	}
	return 0;
}

int init_db()
{
	t_db_info db;
	memset(&db, 0, sizeof(db));
	char *v = myconfig_get_value("db_host");
	if (v == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "no db_host\n");
		return -1;
	}
	snprintf(db.host, sizeof(db.host), "%s", v);

	v = myconfig_get_value("db_username");
	if (v == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "no db_username\n");
		return -1;
	}
	snprintf(db.username, sizeof(db.username), "%s", v);

	v = myconfig_get_value("db_password");
	if (v == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "no db_password\n");
		return -1;
	}
	snprintf(db.passwd, sizeof(db.passwd), "%s", v);

	v = myconfig_get_value("db_db");
	if (v == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "no db_db\n");
		return -1;
	}
	snprintf(db.db, sizeof(db.db), "%s", v);

	db.port = myconfig_get_intval("db_port", 3306);
	return connect_db(&db);
}


static void sigterm_handler(int signo) 
{
	LOG(log_2_db_log, LOG_ERROR, "%s %d %d\n", __func__, __LINE__, signo);
	g_stop = 1;
}

static int init_log_2_db()
{
	char *logname = myconfig_get_value("log_logname");
	if (logname == NULL)
	{
		fprintf(stderr, "config have not logname!\n");
		return -1;
	}
	int loglevel = getloglevel(myconfig_get_value("log_loglevel"));
	int logsize = myconfig_get_intval("log_logsize", 100);
	int logtime = myconfig_get_intval("log_logtime", 3600);
	int logcount = myconfig_get_intval("log_logcount", 10);

	if (init_log())
	{
		fprintf(stderr, "init log error %m\n");
		return -1;
	}

	log_2_db_log = registerlog(logname, loglevel, logsize, logtime, logcount);
	if (log_2_db_log < 0)
	{
		fprintf(stderr, "open %s error %m\n", logname);
		return -1;
	}

	dir_recursive = myconfig_get_intval("recursive", 0);
	logfile_indir = myconfig_get_value("path_indir");
	if (logfile_indir == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "logfile_indir is null %s %d\n", __func__, __LINE__);
		return -1;
	}
	logfile_bkdir = myconfig_get_value("path_bkdir");
	if (logfile_bkdir == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "logfile_bkdir is null %s %d\n", __func__, __LINE__);
		return -1;
	}
	logfile_errdir = myconfig_get_value("path_errdir");
	if (logfile_errdir == NULL)
	{
		LOG(log_2_db_log, LOG_ERROR, "logfile_errdir is null %s %d\n", __func__, __LINE__);
		return -1;
	}
	struct sigaction sa;
	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = sigterm_handler;
	sigaction(SIGUSR1, &sa, NULL);
	return init_db();
}

#include "p.c"

#define log_2_db_version "0.9"

int main(int argc, char **argv)
{
	if (argc > 1)
	{
		if (strcasecmp(argv[1], "-v") == 0)
		{
			fprintf(stdout, "version [%s]\n", log_2_db_version);
			fprintf(stdout, "compile time [%s %s]\n", __DATE__, __TIME__);
			return -1;
		}
	}
	daemon(1, 1);

	if (myconfig_init(argc, argv))
	{
		fprintf(stderr, "myconfig_init error [%s]\n", strerror(errno));
		exit(-1);
	}

	if (init_log_2_db())
		exit(-1);

	LOG(log_2_db_log, LOG_NORMAL, "init_log_2_db ok.\n"); 

	if (init_libs(mysql))
	{
		LOG(log_2_db_log, LOG_ERROR, "init_libs %s %d error %m\n", __func__, __LINE__);
		exit(-1);
	}
	LOG(log_2_db_log, LOG_NORMAL, "init_libs %s %d ok.\n", __func__, __LINE__); 

	if (init_aimei_data_config())
	{
		LOG(log_2_db_log, LOG_ERROR, "init_aimei_data_config %s %d error %m\n", __func__, __LINE__);
		exit(-1);
	}

	LOG(log_2_db_log, LOG_NORMAL, "init_aimei_data_config %s %d ok.\n", __func__, __LINE__); 

	t_aimei_data_config c;
	memset(&c, 0, sizeof(c));
	c.prefix = logfile_indir;

	get_soname_by_config(&c, AIMEI_DATA_DIR_PREFIX);
	while (g_stop)
	{
		do_subdir(logfile_indir, &c);
		sleep(5);
	}
	fini_libs();
	return 0;
}

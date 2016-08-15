#include "myconfig.h"
#include "log.h"
#include "aimei_data_config.h"
#include "plugins.h"

extern int log_2_db_log;
#define MAX_CONFIG_COUNT 128

static t_aimei_data_config  aimei_data_config[AIMEI_DATA_MAX_PREFIX][MAX_CONFIG_COUNT];

static int qsort_config(const void *v1, const void *v2)
{
	t_aimei_data_config *c1 = (t_aimei_data_config *) v1;
	t_aimei_data_config *c2 = (t_aimei_data_config *) v2;

	return c1->prelen < c2->prelen;
}

int init_aimei_data_config_sub(char *father, t_aimei_data_config *conf)
{
	LOG(log_2_db_log, LOG_NORMAL, "%s %d %s\n", __func__, __LINE__, father);
	t_aimei_data_config *c = conf;
	char k[64] = {0x0};
	snprintf(k, sizeof(k), "%s_prefix", father);
	char* pval = NULL; int i = 0;
	for( i = 0; (pval = myconfig_get_multivalue(k, i)) != NULL && i < MAX_CONFIG_COUNT; i++ )
	{
		LOG(log_2_db_log, LOG_NORMAL, "%s %d %s=%s\n", __func__, __LINE__, k, pval);
		char *t = strchr(pval, ':');
		if (t == NULL)
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %s=%s\n", __func__, __LINE__, k, pval);
			return -1;
		}
		*t = 0x0;
		t++;
		if (check_libs_exist(t))
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %s %s:%s\n", __func__, __LINE__, k, pval, t);
			return -1;
		}
		conf->prefix = pval;
		conf->prelen = strlen(conf->prefix);
		conf->soname = t;
		conf++;
	}
	if (i == MAX_CONFIG_COUNT)
	{
		LOG(log_2_db_log, LOG_ERROR, "%s %d too many\n", __func__, __LINE__, i);
		return -1;
	}
	qsort(c, MAX_CONFIG_COUNT, sizeof(t_aimei_data_config), qsort_config);
	return 0;
}

int init_aimei_data_config()
{
	memset(aimei_data_config, 0, sizeof(aimei_data_config));
	return init_aimei_data_config_sub("file", aimei_data_config[AIMEI_DATA_FILE_PREFIX]) || init_aimei_data_config_sub("dir", aimei_data_config[AIMEI_DATA_DIR_PREFIX]);
}

int get_soname_by_config(t_aimei_data_config *conf, uint8_t type)
{
	t_aimei_data_config *c = aimei_data_config[type%AIMEI_DATA_MAX_PREFIX];
	int i = 0;
	for(; i < MAX_CONFIG_COUNT; i++)
	{
		if (c->prefix == NULL || c->soname == NULL)
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %s %d\n", __func__, __LINE__, conf->prefix, type);
			return -1;
		}
		if (strncmp(c->prefix, conf->prefix, c->prelen) == 0)
		{
			conf->soname = c->soname;
			return 0;
		}
		c++;
	}
	LOG(log_2_db_log, LOG_ERROR, "%s %d %s %d\n", __func__, __LINE__, conf->prefix, type);
	return -1;
}


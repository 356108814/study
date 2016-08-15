#include <dlfcn.h>
#include "plugins.h"
#include "myconfig.h"
#include "log.h"

extern int log_2_db_log;
static list_head_t plist;

int check_libs_exist(char *soname)
{
	t_aimei_data_lib *lib = NULL;
	list_head_t *l;
	list_for_each_entry_safe_l(lib, l, &(plist), list)
	{
		LOG(log_2_db_log, LOG_NORMAL, "%s %d %s %s\n", __func__, __LINE__, soname, lib->soname);
		if (strcmp(soname, lib->soname) == 0)
			return 0;
	}
	return -1;
}

int call_libs(char *soname, char *buf)
{
	t_aimei_data_lib *lib = NULL;
	list_head_t *l;
	list_for_each_entry_safe_l(lib, l, &(plist), list)
	{
		if (strcmp(soname, lib->soname) == 0)
			return lib->so_proc(buf);
	}
	return -1;
}

int init_libs(MYSQL *mysql)
{
	INIT_LIST_HEAD(&plist);
	char* pval = NULL; int i = 0;
	for( i = 0; ( pval = myconfig_get_multivalue( "plugin_so", i ) ) != NULL; i++ )
	{
		t_aimei_data_lib * lpplugin = (t_aimei_data_lib*)malloc( sizeof(t_aimei_data_lib) );
		if( lpplugin == NULL ) 
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %m\n", __func__, __LINE__);
			return -1;
		}
		lpplugin->handle = dlopen( pval, RTLD_NOW);
		if( lpplugin->handle == NULL )
		{
			LOG(log_2_db_log, LOG_ERROR, "%s %d %m [%s] %s\n", __func__, __LINE__, pval, dlerror());
			return -1;
		}
		lpplugin->so_init = (so_method)dlsym( lpplugin->handle, "so_init" );
		lpplugin->so_proc = (so_method)dlsym( lpplugin->handle, "so_proc" );
		if (lpplugin->so_proc == NULL)
		{
			LOG(log_2_db_log, LOG_ERROR, "Plugin %s no so_proc.", pval );
			return -1;
		}
		lpplugin->so_fini = (so_method)dlsym( lpplugin->handle, "so_fini" );
		if( lpplugin->so_init != NULL )
		{
			if( lpplugin->so_init(log_2_db_log, mysql) != 0 )
			{
				LOG(log_2_db_log, LOG_ERROR, "Plugin %s so_init fail.", pval );
				return -1;
			}
		}
		lpplugin->soname = pval;
		INIT_LIST_HEAD(&(lpplugin->list));
		list_add_tail(&(lpplugin->list), &plist);
	}
	return 0;
}

void fini_libs()
{
	t_aimei_data_lib *lib = NULL;
	list_head_t *l;
	list_for_each_entry_safe_l(lib, l, &(plist), list)
	{
		if (lib->so_fini)
			lib->so_fini();
		list_del_init(&(lib->list));
		free(lib);
	}
}


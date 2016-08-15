#ifndef __56NM_PLUGINS_H__
#define __56NM_PLUGINS_H__

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <unistd.h>
#include "list.h"
#include "mydb.h"

#ifdef __cplusplus
extern "C"
{
#endif

typedef int (*so_init_func) (int fd, MYSQL * mysql);
typedef int (*so_method) ();
typedef int (*so_call) (char *buf);

typedef struct {
	void *handle;
	char *soname;
	so_init_func	so_init;
	so_call		so_proc;
	so_method   so_fini;
	list_head_t list;
} t_aimei_data_lib;

int init_libs(MYSQL *mysql);
void fini_libs();
int call_libs(char *soname, char *buf);

int check_libs_exist(char *soname);

#ifdef __cplusplus
}
#endif
#endif

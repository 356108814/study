#ifndef __56NM_DB_H_
#define __56NM_DB_H_
#include "common.h"
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <dirent.h>
#include <string.h>
#include <mysql.h>

#ifdef __cplusplus
extern "C"
{
#endif

int lib_connect_db(t_db_info *db_info, MYSQL* mysql);

void close_db(MYSQL * mysql);

uint32_t get_sel_count(MYSQL * mysql, char *sql);

int mydb_begin(MYSQL* mysql);

int mydb_commit(MYSQL* mysql);

int mydb_rollback(MYSQL* mysql);

int get_sel_string(MYSQL* mysql, char *sql, char *buf, int buflen);

int get_sel_mul_count(MYSQL* mysql, char *sql, long *ret, int n);

int get_sel_count_by_default(MYSQL* mysql, char *sql, int predef);

#ifdef __cplusplus
}
#endif
#endif

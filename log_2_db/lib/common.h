/*
* Copyright (C) 2012-2014 www.56.com email: jingchun.zhang AT renren-inc.com; jczhang AT 126.com ; danezhang77 AT gmail.com
* 
* 56VFS may be copied only under the terms of the GNU General Public License V3
*/

#ifndef _NM_COMMON_H_
#define _NM_COMMON_H_
#include "nm.h"
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <stdarg.h>
#include <stddef.h>
#include <time.h>
#include <pthread.h>
#include <errno.h>
#include <stdint.h>
#include <ctype.h>

#define MIN_ITEMS 3
#define MAX_ITEMS 32
#define MAX_SIZE_ITEM 256

#define ID __FILE__
#define FUNC __FUNCTION__
#define LN __LINE__

#define vfs_abs(value)       (((value) >= 0) ? (value) : - (value))
#define vfs_max(val1, val2)  (((val1) < (val2)) ? (val2) : (val1))
#define vfs_min(val1, val2)  (((val1) > (val2)) ? (val2) : (val1))

#define MAX_IP_GROUP 16

#define get_int(x) (x==NULL ? -1 : atoi(x))
#define get_lint(x) (x==NULL ? -1 : atol(x))
#define get_str(x) (x==NULL ? "" : x)

typedef struct {
	char indir[256];
	char bkdir[256];
	char workdir[256];
	char outdir[256];
	char fulldir[256];
	char tmpdir[256];
}t_path_info;

typedef struct {
	char host[512];
	char username[32];
	char passwd[32];
	char db[32];
	int port;
}t_db_info;

typedef unsigned char u_char;

typedef struct {
	size_t      len;
	u_char     *data;
} ngx_str_t;

#ifdef __cplusplus
extern "C"
{
#endif
int get_ip_by_domain(char *serverip, char *domain);

void trim_in(char *s, char *d);

uint32_t r5hash(const char *p); 

int get_strtime(char *buf);

int get_strtime_by_t(char *buf, time_t now);

char* get_strtime_by_format_and_time(char* format, time_t* tNow, char* buf, int buf_size);

uint32_t get_uint32_ip(char *sip, char *s_ip);

time_t get_time_t (char *p);

void base64_encode(const char *buf, int len, char *out, int pad);

void ngx_encode_base64(ngx_str_t *dst, ngx_str_t *src);

int ngx_decode_base64(ngx_str_t *dst, ngx_str_t *src);

void urlencode(unsigned char * src, int src_len, unsigned char * dest, int dest_len);
unsigned char* urldecode(unsigned char* encd,unsigned char* decd);

int get_http_head(char *d, char *k, char *v, int vl);

#ifdef __cplusplus
}
#endif
#endif

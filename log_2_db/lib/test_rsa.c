/*
* Copyright (C) 2012-2014 www.56.com email: jingchun.zhang AT renren-inc.com; jczhang AT 126.com ; danezhang77 AT gmail.com
* 
* 56VFS may be copied only under the terms of the GNU General Public License V3
*/

#include <stdio.h>
#include <libgen.h>
#include "ssllib.h"
#include "common.h"

int main(int c, char **v)
{
	if (c != 3)
	{
		fprintf(stderr, "testrsa pem instr!\n");
		return -1;
	}
	if (load_pri_key(v[1])) 
	{
		fprintf(stderr, "load_key error! %m\n");
		return -1;
	}

	unsigned char decode[128] = {0x0};
	ngx_str_t dst;
	dst.data = decode;
	dst.len = sizeof(decode);

	ngx_str_t src;
	src.data = (u_char *)v[2];
	src.len = strlen((char*)v[2]);

	if (ngx_decode_base64(&dst, &src))
	{
		fprintf(stderr, "%s %d %s %m\n", __func__, __LINE__, v[2]);
		return -1;
	}

	fprintf(stdout, "len = %ld\n", dst.len);
	int i = 0;
	for(; i < dst.len; i++)
	{
		fprintf(stdout, "%02x ", decode[i]);
	}
	fprintf(stdout, "\n\n\n");

	char outbuf[64] = {0x0};
	int len = 0;
	if (ssl_decrypt_by_pri((char *)decode, dst.len, outbuf, &len, NULL))
	{
		fprintf(stderr, "%s %d %s %m\n", __func__, __LINE__, v[2]);
		return -1;
	}

	i = 0;
	for(; i < len; i++)
	{
		fprintf(stdout, "%02x ", (unsigned char)outbuf[i]);
	}
	fprintf(stdout, "\n");

	fprintf(stdout, "ssl_decrypt [%s][%d]!\n", outbuf, len);
	return 0;
}

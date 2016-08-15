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
		fprintf(stderr, "testrsa pub pem!\n");
		return -1;
	}
	if (load_pub_key(v[1]))
	{
		fprintf(stderr, "load_pub_key error!\n");
		return -1;
	}
	if (load_pri_key(v[2]))
	{
		fprintf(stderr, "load_pri_key error!\n");
		return -1;
	}

	char buf[] = "23456xxxxxxxxxxxxxxxxxxyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
	char out[1024] = {0x0};
	int outlen = 0;
	if (ssl_encrypt_by_pri(buf, strlen(buf), out, &outlen, NULL))
	{
		fprintf(stderr, "ssl_encrypt error!\n");
		return -1;
	}
	fprintf(stdout, "len %d\n", outlen);
	ngx_str_t src;
	src.data = (u_char *)out;
	src.len = outlen;

	char base64out[2048] = {0x0};
	ngx_str_t dst;
	dst.data = (u_char *)base64out;
	ngx_encode_base64(&dst, &src);
	fprintf(stdout, "ssl_encrypt [%s]!\n", base64out);

	char debase64out[2048] = {0x0};
	ngx_str_t de_dst;
	de_dst.data = (u_char *)debase64out;

	if (ngx_decode_base64(&de_dst, &dst))
	{
		fprintf(stderr, "ngx_decode_base64 error %m\n");
		return -1;
	}

	char outbuf[2048] = {0x0};
	int len = 0;
	if (ssl_decrypt_by_pub((char *)de_dst.data, de_dst.len, outbuf, &len, NULL))
	{
		fprintf(stderr, "ssl_decrypt error!\n");
		return -1;
	}

	fprintf(stdout, "ssl_decrypt [%s]!\n", outbuf);
	return 0;
}

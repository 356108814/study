/*
* Copyright (C) 2012-2014 www.56.com email: jingchun.zhang AT renren-inc.com; jczhang AT 126.com ; danezhang77 AT gmail.com
* 
* 56VFS may be copied only under the terms of the GNU General Public License V3
*/

#include <stdio.h>
#include <libgen.h>
#include "ssllib.h"
#include "common.h"

static int get_input(char *encoded, char *input)
{
	int i = 0;
	char *s = encoded;
	while (*s)
	{
		i++;
		char sbuf[4] = {0x0};
		snprintf(sbuf, sizeof(sbuf), "%.*s", 2, s);
		s += 2;
		int c = strtol(sbuf, NULL, 16);
		*input = c;
		input++;
	}
	return i;
}

int main(int c, char **v)
{
	if (c != 3)
	{
		fprintf(stderr, "testrsa pem pub!\n");
		return -1;
	}
	if (load_pri_key(v[1]) || load_pub_key(v[2]))
	{
		fprintf(stderr, "load_key error! %m\n");
		return -1;
	}

	char buf[128] = {0x0};
	int sl = snprintf(buf, sizeof(buf), "04B50001245E000120160203");

	fprintf(stdout, "%s %d %s %d\n", __func__, __LINE__, buf, sl);
	char out[128] = {0x0};
	int outlen = 0;
	if (ssl_encrypt_by_pub(buf, sl, out, &outlen, NULL))
	{
		fprintf(stderr, "ssl_encrypt_by_pub %d %m\n", __LINE__);
		return -1;
	}
	char shard_id[256] = {0x0};
	int i = 0;
	unsigned char *o = (unsigned char *)out;
	char *oh = shard_id;
	while (i < outlen)
	{
		fprintf(stdout, "[%d:%u]\n", i, *o);
		sprintf(oh, "%02X", *o);
		oh += 2;
		o++;
		i++;
	}
	*oh = 0x0;
	char *mbuf = shard_id;

	char input[128] = {0x0};
	int ilen = get_input(mbuf, input);
	int ret = memcmp(input, out, ilen);
	fprintf(stdout, "ilen = %d outlen = %d %d [%s]\n", ilen, outlen, ret, mbuf);
	i = 0;
	o = (unsigned char *)input;
	while (i < ilen)
	{
		fprintf(stdout, "[%d:%u]\n", i, *o);
		i++;
		o++;
	}


	char outbuf[2048] = {0x0};
	int len = 0;
	if (ssl_decrypt_by_pri(input, ilen, outbuf, &len, NULL))
	{
		fprintf(stderr, "ssl_decrypt error!\n");
		return -1;
	}

	char *s = outbuf;
	i = 0;
	for ( ; i < len; i++)
	{
		if (*s != 0x0)
			break;
		s++;
	}

	len = strlen(s);
	len -=8;
	char hard_id[64] = {0x0};
	char *s1 = s;
	char *d = hard_id;
	for (i = 0; i < len; i++)
	{
		sprintf(d, "%02X", *s1);
		d += 2;
		s1++;
	}
	fprintf(stdout, "ssl_decrypt [%s] [%s]!\n", s, hard_id);
	return 0;
}

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "valid_check.h"
#include "parsepara.h"
#include "sha1sum.h"

int sortstr(const void *p1, const void *p2)
{   
	return strcmp((char *)p1, (char *)p2);
} 

static void get_sha1sum_for_kshow(char *nonce, char *timestamp, char *token, char *sha1sum)
{
	char str[4][64];
	memset(str, 0, sizeof(str));
	snprintf(str[0], sizeof(str[0]), "%s", nonce);
	snprintf(str[1], sizeof(str[1]), "%s", timestamp);
	snprintf(str[2], sizeof(str[2]), "%s", token);

	qsort(str, 3, 64, sortstr);
	char buf[256] = {0x0};
	int l = snprintf(buf, sizeof(buf), "%s%s%s", str[0], str[1], str[2]);
	GetStringSHA1_Hex(buf, l, sha1sum);
}

int check_valid_by_sha1(char *nonce, char *timestamp, char *signature, char *token)
{
	char crypt_msg[64] = {0x0};
	get_sha1sum_for_kshow(nonce, timestamp, token, crypt_msg);
	return strcmp(crypt_msg, signature);
}

int check_wx_valid(char *data, char *token)
{
	data = strchr(data, '?');
	if (data == NULL)
		return -1;
	data++;
	char *e = strchr(data, ' ');
	if (e == NULL)
		return -1;
	*e = 0x0;

	int datalen = strlen(data);
	StringPairList *pairlist = CreateStringPairList(20);
	if (!pairlist)
		return -1;

	if(DecodePara(data, datalen, pairlist) != 0)
	{
		DestroyStringPairList(pairlist);
		return -1;
	}

	char signature[64] = {0x0};
	if (!GetParaValue(pairlist, "signature", signature, sizeof(signature)))
	{
		DestroyStringPairList(pairlist);
		return -1;
	}

	char timestamp[64] = {0x0};
	if (!GetParaValue(pairlist, "timestamp", timestamp, sizeof(timestamp)))
	{
		DestroyStringPairList(pairlist);
		return -1;
	}

	char nonce[64] = {0x0};
	if (!GetParaValue(pairlist, "nonce", nonce, sizeof(nonce)))
	{
		DestroyStringPairList(pairlist);
		return -1;
	}

	if (check_valid_by_sha1(nonce, timestamp, signature, token))
	{
		DestroyStringPairList(pairlist);
		return -1;
	}
	DestroyStringPairList(pairlist);

	return 0;
}



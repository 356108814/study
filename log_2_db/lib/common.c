/*
* Copyright (C) 2012-2014 www.56.com email: jingchun.zhang AT renren-inc.com; jczhang AT 126.com ; danezhang77 AT gmail.com
* 
* 56VFS may be copied only under the terms of the GNU General Public License V3
*/

#include "common.h"
#include "util.h"
#include <sys/mman.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/un.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <netdb.h>
#include <sys/socket.h> 
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int get_ip_by_domain(char *serverip, char *domain)
{
	char **pptr;
	char                    str[128] = {0x0};
	struct hostent  *hptr;
	if ( (hptr = gethostbyname(domain)) == NULL) 
		return -1;

	switch (hptr->h_addrtype) {
		case AF_INET:
#ifdef  AF_INET6
		case AF_INET6:
#endif
			pptr = hptr->h_addr_list;
			for ( ; *pptr != NULL; pptr++)
			{
				inet_ntop(hptr->h_addrtype, *pptr, str, sizeof(str));
				strcpy(serverip, str);
				return 0;
			}
			break;

		default:
			return -1;
			break;
	}
	return -1;
}

void trim_in(char *s, char *d)
{
	/*skip head blank */

	while (s)
	{
		if (*s != ' ')
			break;
		s++;
	}

	int c = 0;
	while (*s)
	{
		if (*s == ' ')
		{
			c++;
			if (c == 1)
			{
				*d = *s;
				d++;
				s++;
				continue;
			}
			s++;
		}
		else
		{
			c = 0;
			*d = *s;
			d++;
			s++;
		}
	}
	return;
}

uint32_t r5hash(const char *p) 
{
	uint32_t h = 0;
	while(*p) {
		h = h * 11 + (*p<<4) + (*p>>4);
		p++;
	}
	return h;
}

char* get_strtime_by_format_and_time(char* format, time_t* tNow, char* buf, int buf_size)
{
	struct tm ptm;

	localtime_r(tNow, &ptm);
	strftime(buf, buf_size, format, &ptm);

	return buf;
}

int get_strtime(char *buf)
{
    struct tm tmm; 
	time_t now = time(NULL);
	localtime_r(&now, &tmm);  
	sprintf(buf, "%04d%02d%02d%02d%02d%02d", tmm.tm_year + 1900, tmm.tm_mon + 1, tmm.tm_mday, tmm.tm_hour, tmm.tm_min, tmm.tm_sec);
	return 0;
}

int get_strtime_by_t(char *buf, time_t now)
{
    struct tm tmm; 
	localtime_r(&now, &tmm);  
	sprintf(buf, "%04d%02d%02d%02d%02d%02d", tmm.tm_year + 1900, tmm.tm_mon + 1, tmm.tm_mday, tmm.tm_hour, tmm.tm_min, tmm.tm_sec);
	return 0;
}

uint32_t get_uint32_ip(char *sip, char *s_ip)
{
	uint32_t ip = str2ip(sip);
	if (ip == INADDR_NONE)
	{
		char tmpip[16] = {0x0};
		if (get_ip_by_domain(tmpip, sip))
			return INADDR_NONE;
		ip = str2ip(tmpip);
		snprintf(s_ip, 16, "%s", tmpip);
	}
	else
		snprintf(s_ip, 16, "%s", sip); 
	return ip;
}

time_t get_time_t (char *p)
{
	if (strlen(p) != 14)
		return 0;
	struct tm t;
	memset(&t, 0, sizeof(t));
	char b[8] = {0x0};
	snprintf(b, sizeof(b), "%.4s", p);
	t.tm_year = atoi(b) - 1900;
	memset(b, 0, sizeof(b));

	snprintf(b, sizeof(b), "%.2s", p+4);
	t.tm_mon = atoi(b) - 1;
	memset(b, 0, sizeof(b));

	snprintf(b, sizeof(b), "%.2s", p+6);
	t.tm_mday = atoi(b);
	memset(b, 0, sizeof(b));

	snprintf(b, sizeof(b), "%.2s", p+8);
	t.tm_hour = atoi(b);
	memset(b, 0, sizeof(b));

	snprintf(b, sizeof(b), "%.2s", p+10);
	t.tm_min = atoi(b);
	memset(b, 0, sizeof(b));

	snprintf(b, sizeof(b), "%.2s", p+12);
	t.tm_sec = atoi(b);
	memset(b, 0, sizeof(b));

	return mktime(&t);
}

#ifdef uchar
#undef uchar
#endif
#define uchar unsigned char

void base64_encode(const char *buf, int len, char *out, int pad)
{
	char *b64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	int bit_offset, byte_offset, idx, i;
	const uchar *d = (const uchar *)buf;
	int bytes = (len*8 + 5)/6;

	for (i = 0; i < bytes; i++) {
		byte_offset = (i*6)/8;
		bit_offset = (i*6)%8;
		if (bit_offset < 3) {
			idx = (d[byte_offset] >> (2-bit_offset)) & 0x3F;
		} else {
			idx = (d[byte_offset] << (bit_offset-2)) & 0x3F;
			if (byte_offset+1 < len) {
				idx |= (d[byte_offset+1] >> (8-(bit_offset-2)));
			}
		}
		out[i] = b64[idx];
	}

	while (pad && (i % 4))
		out[i++] = '=';

	out[i] = '\0';
}

static void ngx_encode_base64_internal(ngx_str_t *dst, ngx_str_t *src, const u_char *basis, uint8_t padding)
{
    u_char         *d, *s;
    size_t          len;

    len = src->len;
    s = src->data;
    d = dst->data;

    while (len > 2) {
        *d++ = basis[(s[0] >> 2) & 0x3f];
        *d++ = basis[((s[0] & 3) << 4) | (s[1] >> 4)];
        *d++ = basis[((s[1] & 0x0f) << 2) | (s[2] >> 6)];
        *d++ = basis[s[2] & 0x3f];

        s += 3;
        len -= 3;
    }

    if (len) {
        *d++ = basis[(s[0] >> 2) & 0x3f];

        if (len == 1) {
            *d++ = basis[(s[0] & 3) << 4];
            if (padding) {
                *d++ = '=';
            }

        } else {
            *d++ = basis[((s[0] & 3) << 4) | (s[1] >> 4)];
            *d++ = basis[(s[1] & 0x0f) << 2];
        }

        if (padding) {
            *d++ = '=';
        }
    }

    dst->len = d - dst->data;
}

void ngx_encode_base64(ngx_str_t *dst, ngx_str_t *src)
{
    static u_char   basis64[] =
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

    ngx_encode_base64_internal(dst, src, basis64, 1);
}

static int ngx_decode_base64_internal(ngx_str_t *dst, ngx_str_t *src, const u_char *basis)
{
    size_t          len;
    u_char         *d, *s;

    for (len = 0; len < src->len; len++) {
        if (src->data[len] == '=') {
            break;
        }

        if (basis[src->data[len]] == 77) {
            return -1;
        }
    }

    if (len % 4 == 1) {
        return -1;
    }

    s = src->data;
    d = dst->data;

    while (len > 3) {
        *d++ = (u_char) (basis[s[0]] << 2 | basis[s[1]] >> 4);
        *d++ = (u_char) (basis[s[1]] << 4 | basis[s[2]] >> 2);
        *d++ = (u_char) (basis[s[2]] << 6 | basis[s[3]]);

        s += 4;
        len -= 4;
    }

    if (len > 1) {
        *d++ = (u_char) (basis[s[0]] << 2 | basis[s[1]] >> 4);
    }

    if (len > 2) {
        *d++ = (u_char) (basis[s[1]] << 4 | basis[s[2]] >> 2);
    }

    dst->len = d - dst->data;

    return 0;
}

int ngx_decode_base64(ngx_str_t *dst, ngx_str_t *src)
{
    static u_char   basis64[] = {
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 62, 77, 77, 77, 63,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 77, 77, 77, 77, 77, 77,
        77,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 77, 77, 77, 77, 77,
        77, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 77, 77, 77, 77, 77,

        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77,
        77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77, 77
    };

    return ngx_decode_base64_internal(dst, src, basis64);
}

static unsigned char char_to_hex(unsigned char x) {
	return (unsigned char) (x > 9 ? x + 55 : x + 48);
}

static int is_alpha_number_char(unsigned char c) {
	if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
			|| (c >= '0' && c <= '9'))
		return 1;
	return 0;
}

void urlencode(unsigned char * src, int src_len, unsigned char * dest,
		int dest_len) {
	unsigned char ch;
	int len = 0;

	while (len < (dest_len - 4) && *src) {
		ch = (unsigned char) *src;
		if (*src == ' ') {
			*dest++ = '+';
		} else if (is_alpha_number_char(ch) || strchr("-_.!~*'()", ch)) {
			*dest++ = *src;
		} else {
			*dest++ = '%';
			*dest++ = char_to_hex((unsigned char) (ch >> 4));
			*dest++ = char_to_hex((unsigned char) (ch % 16));
		}
		++src;
		++len;
	}
	*dest = 0;
	return;
}

unsigned char* urldecode(unsigned char* encd, unsigned char* decd) {
	int j, i;
	unsigned char *cd = encd;
	char p[2];
	unsigned int num = strlen((char*)cd);
	j = 0;

	for (i = 0; i < num; i++) {
		memset(p, 0, 2);

		if (cd[i] == '+') {
			decd[j++] = ' ';
			continue;
		}

		if (cd[i] != '%') {
			decd[j++] = cd[i];
			continue;
		}

		p[0] = cd[++i];
		p[1] = cd[++i];

		p[0] = p[0] - 48 - ((p[0] >= 'A') ? 7 : 0) - ((p[0] >= 'a') ? 32 : 0);
		p[1] = p[1] - 48 - ((p[1] >= 'A') ? 7 : 0) - ((p[1] >= 'a') ? 32 : 0);
		decd[j++] = (unsigned char) (p[0] * 16 + p[1]);

	}
	decd[j] = '\0';

	return decd;
}

int get_http_head(char *d, char *k, char *v, int vl)
{
	char *t = strcasestr(d, k);
	if (t == NULL)
		return -1;

	char *e = strstr(t, "\r\n");
	if (e == NULL)
		return -1;
	*e = 0x0;

	memset(v, 0, vl);
	snprintf(v, vl, "%s", t + strlen(k));
	*e = '\r';
	return 0;
}


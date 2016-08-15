#ifndef __KSHOW_VALID_CHECK_H__
#define __KSHOW_VALID_CHECK_H__
int sortstr(const void *p1, const void *p2);
int check_valid_by_sha1(char *nonce, char *timestamp, char *signature, char *token);
int check_wx_valid(char *data, char *token);
#endif

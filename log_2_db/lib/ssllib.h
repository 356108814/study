#ifndef __SSL_LIB_H_
#define __SSL_LIB_H_
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<openssl/rsa.h>
#include<openssl/pem.h>
#include<openssl/err.h>

#ifdef __cplusplus

extern "C"
{
#endif
int load_pub_key(char *pubkey);

int load_pri_key(char *prikey);

int ssl_encrypt_by_pri(char *in, int inlen, char *out, int *outlen, FILE *logfile);

int ssl_encrypt_by_pub(char *in, int inlen, char *out, int *outlen, FILE *logfile);

int ssl_decrypt_by_pri(char *in, int inlen, char *out, int *outlen, FILE *logfile);

int ssl_decrypt_by_pub(char *in, int inlen, char *out, int *outlen, FILE *logfile);

int release_rsa();

#ifdef __cplusplus
}
#endif
#endif

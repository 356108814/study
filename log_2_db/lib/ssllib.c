#include "ssllib.h"

static RSA *pub_rsa = NULL;
static RSA *pri_rsa = NULL;

int load_pub_key(char *pubkey)
{
	FILE *fp;
	if((fp = fopen(pubkey, "r")) == NULL)
	{
		perror("open key file error");
		return -1;
	}

	if((pub_rsa = PEM_read_RSA_PUBKEY(fp, NULL, NULL, NULL)) == NULL)
	{
		ERR_print_errors_fp(stdout);
		fclose(fp);
		return -1;
	}
	fclose(fp);
	return 0;
}

int load_pri_key(char *prikey)
{
	FILE *fp;
	if((fp = fopen(prikey, "r")) == NULL)
	{
		perror("open key file error");
		return -1;
	}

	if((pri_rsa = PEM_read_RSAPrivateKey(fp, NULL, NULL, NULL)) == NULL)
	{
		ERR_print_errors_fp(stdout);
		fclose(fp);
		return -1;
	}
	fclose(fp);
	return 0;
}

int ssl_encrypt_by_pub(char *in, int inlen, char *out, int *outlen, FILE *logfile)
{
	if (inlen == 0)
	{
		*outlen = 0x0;
		return 0;
	}

	char *o = out;
	char *i = in;
	int rsa_len = RSA_size(pub_rsa);
	int blocks = inlen/rsa_len;

	int div = inlen%rsa_len;
	if (div)
		blocks++;

	int l = 0;
	int curlen = 0;
	for(l = 0; l < blocks; l++)
	{
		if (inlen > rsa_len)
			curlen = rsa_len;
		else
			curlen = inlen;
		int retlen=RSA_public_encrypt(rsa_len, (unsigned char *)i, (unsigned char *)o, pub_rsa, RSA_NO_PADDING);
		if (retlen < 0)
		{
			if (logfile == NULL)
				logfile = stderr;
			ERR_print_errors_fp(logfile);
			return -1;
		}

		*outlen += retlen;
		o += retlen;
		i += curlen ;
		inlen -= curlen;
	}

	return 0;
}

int ssl_encrypt_by_pri(char *in, int inlen, char *out, int *outlen, FILE *logfile)
{
	if (inlen == 0)
	{
		*outlen = 0x0;
		return 0;
	}

	char *o = out;
	char *i = in;
	int rsa_len = RSA_size(pri_rsa);
	int blocks = inlen/rsa_len;

	int div = inlen%rsa_len;
	if (div)
		blocks++;

	int l = 0;
	int curlen = 0;
	for(l = 0; l < blocks; l++)
	{
		if (inlen > rsa_len)
			curlen = rsa_len;
		else
			curlen = inlen;
		int retlen=RSA_private_encrypt(rsa_len, (unsigned char *)i, (unsigned char *)o, pri_rsa, RSA_NO_PADDING);
		if (retlen < 0)
		{
			if (logfile == NULL)
				logfile = stderr;
			ERR_print_errors_fp(logfile);
			return -1;
		}

		*outlen += retlen;
		o += retlen;
		i += curlen ;
		inlen -= curlen;
	}

	return 0;
}

int ssl_decrypt_by_pri(char *in, int inlen, char *out, int *outlen, FILE *logfile)
{
	if (inlen == 0)
	{
		*outlen = 0x0;
		return 0;
	}

	char *o = out;
	char *i = in;
	int rsa_len = RSA_size(pri_rsa);
	int blocks = inlen/rsa_len;

	int div = inlen%rsa_len;
	if (div)
		blocks++;

	int l = 0;
	int curlen = 0;
	for(l = 0; l < blocks; l++)
	{
		if (inlen > rsa_len)
			curlen = rsa_len;
		else
			curlen = inlen;
		int retlen = RSA_private_decrypt(curlen, (const unsigned char *)i, (unsigned char *)o, pri_rsa, RSA_NO_PADDING);
		if (retlen < 0)
		{
			if (logfile == NULL)
				logfile = stderr;
			ERR_print_errors_fp(logfile);
			return -1;
		}

		*outlen += retlen;
		o += retlen;
		i += curlen;
		inlen -= curlen;
	}

	return 0;
}

int ssl_decrypt_by_pub(char *in, int inlen, char *out, int *outlen, FILE *logfile)
{
	if (inlen == 0)
	{
		*outlen = 0x0;
		return 0;
	}

	char *o = out;
	char *i = in;
	int rsa_len = RSA_size(pub_rsa);
	int blocks = inlen/rsa_len;

	int div = inlen%rsa_len;
	if (div)
		blocks++;

	int l = 0;
	int curlen = 0;
	for(l = 0; l < blocks; l++)
	{
		if (inlen > rsa_len)
			curlen = rsa_len;
		else
			curlen = inlen;
		int retlen = RSA_public_decrypt(curlen, (const unsigned char *)i, (unsigned char *)o, pub_rsa, RSA_NO_PADDING);
		if (retlen < 0)
		{
			if (logfile == NULL)
				logfile = stderr;
			ERR_print_errors_fp(logfile);
			return -1;
		}

		*outlen += retlen;
		o += retlen;
		i += curlen;
		inlen -= curlen;
	}

	return 0;
}

int release_rsa()
{
	RSA_free(pub_rsa);
	RSA_free(pri_rsa);
    return 0;
}


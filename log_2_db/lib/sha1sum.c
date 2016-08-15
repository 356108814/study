#include "sha1sum.h"

/*
int main()
{
    char out[41];
    GetStringSHA1_Hex("1444894366201709124756monitor_weixin", sizeof("1444894366201709124756monitor_weixin")-1, out);
    printf("%s\n", out);

    return 0;
}
*/
void toHexString(SHA1Context sha1, char output[41])
{
	int i = 0;
    for(; i < 5 ; i++)
    {
        char str[9] = {0x0};;
        sprintf(str, "%08x", sha1.Message_Digest[i]);
        strcat(output, str);
    }
}

void GetStringSHA1_Hex(char *input, unsigned long length, char output[41])
{
    if (NULL == input || NULL == output)
        return;

    SHA1Context sha1;

    SHA1Reset(&sha1);
    SHA1Input(&sha1, (const unsigned char *)input, length);
    SHA1Result(&sha1);

    toHexString(sha1, output);
}

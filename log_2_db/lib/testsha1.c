#include "sha1sum.h"

int main()
{
    char out[41] = {0x0};
    GetStringSHA1_Hex("1444894366201709124756aammusic", strlen("1444894366201709124756aammusic"), out);
    printf("%s\n", out);

    return 0;
}


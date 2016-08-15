#include <stdio.h>
#include <libgen.h>
#include "common.h"

int main(int c, char **v)
{
	if (c != 2)
	{
		fprintf(stderr, "%s domain!\n", basename(v[0]));
		return -1;
	}

	while (1)
	{
		char ip[16] = {0x0};

		if(get_ip_by_domain(ip, v[1]))
		{
			fprintf(stderr, "get_ip_by_domain %s!\n", v[1]);
			return -1;
		}

		fprintf(stdout, "%s A %s\n", v[1], ip);
		sleep(5);
	}
	return 0;
}

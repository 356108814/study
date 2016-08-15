#include "common.h"
#include <stdio.h>
#include <stdlib.h>

int main(int c, char **v)
{
	int t = 0;
	if (c == 2)
		t = atoi(v[1]);
	char day[16] = {0x0};

	time_t now = time(NULL) + t * 86400;
	get_strtime_by_t(day, now);

	memset(day + 8, '0', 6);
	time_t s = get_time_t (day);
	strcpy(day + 8, "235959");
	time_t e = get_time_t (day);

	fprintf(stdout, "%d %ld %ld\n", t, s, e);
	return 0;
}

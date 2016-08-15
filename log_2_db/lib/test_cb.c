#include <stdio.h>

typedef int (*cb)(int a);

int abc(int a)
{
	fprintf (stdout, "abc %d\n", a);
	return 0;
}

int bcd(int a)
{
	fprintf (stdout, "bcd %d\n", a);
	return 0;
}

const cb cball[] = {abc, bcd};

int main(int c, char **v)
{
	if (c != 3)
		return -1;
	if (strcmp(v[1], "abc") == 0)
		cball[0](atoi(v[2]));
	return 0;
}

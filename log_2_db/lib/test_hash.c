#include <stdio.h>
#include <stdint.h>

uint32_t r5hash(const char *p) 
{
	uint32_t h = 0;
	while(*p) {
		h = h * 11 + (*p<<4) + (*p>>4);
		p++;
	}
	return h;
}

int main(int c, char **v)
{
	if (c != 2)
	{
		fprintf(stdout, "test_hash songid!\n");
		return -1;
	}

	fprintf(stdout, "t_data_rank_song_%03d\n", r5hash(v[1]) & 0xFF);
	return 0;
}



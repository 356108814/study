#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

int main()
{
	int fd = open("xxx", O_CREAT | O_RDWR | O_APPEND , 0755);
	if (fd < 0)
	{
		fprintf(stderr, "open error %m\n");
		return -1;
	}

	FILE *fp = fdopen(fd, "a+");

	if (fp == NULL)
	{
		fprintf(stderr, "fdopen error %m\n");
		close(fd);
		return -1;
	}

	fprintf(stdout, "fdopen ok!\n");
	sleep (10);

	fclose(fp);
	fprintf(stdout, "fclose ok!\n");
	sleep (10);
	close(fd);
	return 0;
}

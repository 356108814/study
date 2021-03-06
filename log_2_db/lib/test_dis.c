#include <libgen.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#define EARTH_RADIUS  6378.137
#define PI 3.1415926
double rad(double d)
{
	return d * PI / 180.0;
}

double dis(double lat1, double lng1, double lat2, double lng2)
{
	double radLat1 = rad(lat1);
	double radLat2 = rad(lat2);
	double a = radLat1 - radLat2;
	double b = rad(lng1) - rad(lng2);
	double s = 2 * asin(sqrt(pow(sin(a/2),2) + cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)));
	s = s * EARTH_RADIUS * 1000;
	return s;
}

int main(int c, char **v)
{
	if (c != 5)
	{
		fprintf(stdout, "%s la1 ln1 la2 ln2\n", basename(v[0]));
		return -1;
	}
	fprintf(stdout, "%f\n", dis(atof(v[1]), atof(v[2]), atof(v[3]), atof(v[4])));
	return 0;
}

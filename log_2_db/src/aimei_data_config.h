#ifndef AIMEI_DATA_CONFIG_H
#define AIMEI_DATA_CONFIG_H

#include <stdint.h>
#include "list.h"

enum {
	AIMEI_DATA_FILE_PREFIX = 0,
	AIMEI_DATA_DIR_PREFIX,
	AIMEI_DATA_MAX_PREFIX
};

typedef struct {
	uint8_t prelen;
	char *prefix;
	char *soname;
} t_aimei_data_config;

int init_aimei_data_config();

int get_soname_by_config(t_aimei_data_config *conf, uint8_t type);

#endif

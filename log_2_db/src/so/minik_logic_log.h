#ifndef __DATA_AIMEI_MINIK_LOGIC_LOG_H_
#define __DATA_AIMEI_MINIK_LOGIC_LOG_H_

#include <time.h>
#include <stdio.h>
#include "cJSON.h"
#include "def.h"

#define MINIK_LOGIC_LOG_COUNT 2

typedef int (*minik_logic_log_db_cb) (time_t cur, int mid, cJSON *req);

typedef struct {
	char *router;
	int  len;
	minik_logic_log_db_cb cb;
} t_minik_logic_log_db_cb_s;

extern t_minik_logic_log_db_cb_s minik_log_cball[MINIK_LOGIC_LOG_COUNT];

#endif

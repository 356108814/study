/*
 * vfs_pay_file.h
 *
 *  Created on: 2015-12-21
 *      Author: laojiancong
 */

#ifndef VFS_PAY_FILE_H_
#define VFS_PAY_FILE_H_

#include "list.h"
#include "vfs_task.h"
#include "nm_app_vfs.h"
#include <stdint.h>
#include <time.h>
#include <pthread.h>


enum{
	TASK_PAY_2_ACCESS_QR,
	TASK_PAY_2_ACCESS_QR_MAX = 31,
	TASK_PAY_2_ACCESS_RESULT,
	TASK_PAY_2_ACCESS_RESULT_MAX = 63,
	TASK_ACCESS_2_PAY_QR,
	TASK_ACCESS_2_PAY_CONFIRM,
	TASK_PAY_MISS,
	TASK_PAY_HOME,
	TASK_PAY_UNKNOWN
};

enum {
	GET_TASK_PAY_ERR = -1, GET_TASK_PAY_OK, GET_TASK_PAY_NOTHING
};

enum {
	PAY_SYNC_YES = 0,
	PAY_SYNC_NO
};

typedef struct {
	uint32_t mid;
	uint32_t price;
	uint32_t uid;
	uint8_t type;
	char sequeid[32];
	char title[32];
}t_vfs_pay_request;

typedef struct {
	uint32_t msgcode;
	uint32_t mid;
	char sequeid[32];
	char title[32];
	char pay_url[256];
}t_vfs_pay_qr;

typedef struct {
	uint32_t msgcode;
	uint32_t mid;
	uint32_t price;
	char orderid[64];
	char sequeid[32];
}t_vfs_pay_result;

typedef struct {
	uint32_t mid;
	uint8_t result;
	uint8_t type;
	char orderid[64];
	char sequeid[32];
	char comment[256];
}t_vfs_pay_confirm;

typedef struct {
	union 
	{
		t_vfs_pay_request request;
		t_vfs_pay_qr  qr;
		t_vfs_pay_result result;
		t_vfs_pay_confirm confirm;
	};
	uint8_t sync_flag;
	uint8_t req_type;
}t_vfs_pay_info;

typedef struct {
	t_vfs_pay_info info;
	list_head_t llist;
	uint8_t status;
	uint8_t s_stat;
	time_t endtime;
}t_vfs_pay_file_list;

int vfs_get_pay_file(t_vfs_pay_file_list **task, int status);

int vfs_set_pay_file(t_vfs_pay_file_list *task, int status);

int init_pay_file_info();

int add_pay_to_alltask(t_vfs_pay_file_list *task);

int check_pay_from_alltask(t_vfs_pay_file_list **task, char *jobid, int flag);

#endif /* VFS_PAY_FILE_H_ */

#ifndef __AMPAY__PROTOCOL_H__
#define __AMPAY__PROTOCOL_H__

#include <stdint.h>

enum {
	PAY_RESPONE_QR = 0,
	PAY_RESPONE_CONFIRM
};

enum {
	PAY_CON_STATUS_DISCONNECT,
	PAY_CON_STATUS_CONNECTED
};

enum {
	AMPAY_CLIENT_GET_QRCODE_OF_PAYMENT,
	AMPAY_SERVER_PUSH_SUCCESS_OF_PAYMENT,
	AMPAY_CLIENT_PUSH_RESULT_OF_CONSUMPTION,
};

#pragma pack(1)

typedef struct {
	uint8_t channel;//M
	uint32_t cmd;  //M  rsp = req + 0x80000000
	uint32_t seq;  //M  rsp = req
	uint32_t timeStamp;  //M  rsp = req
	uint32_t mid;  //M
	uint32_t len;  //M  body length
} t_ampay_protocol_head;

typedef struct {
	uint16_t retcode;
	char sequeid[32];
	char title[128];
	char qrcode[256];
	char sign[64];
} t_ampay_protocol_qrcode_rsp;

typedef struct {
	uint8_t payType;
	char orderid[64];
	char sequeid[32];
	char nonce[64];
	char sign[64];
	uint16_t price;
} t_ampay_protocol_pay_success_req;

#pragma pack()
#endif

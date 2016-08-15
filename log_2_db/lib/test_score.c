#include <stdio.h>
#include <stdint.h>
#include <libgen.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>

#pragma pack(1)
enum NoteRecordItemType  
{
	NoteRecordItemType_Judgment=0xd1,
	NoteRecordItemType_combo,
	NoteRecordItemType_life,
	NoteRecordItemType_score,
	NoteRecordItemType_SummyCombo, 
	NoteRecordItemType_Unknow
};

const char *type_msg[5] = {
	"NoteRecordItemType_Judgment",
	"NoteRecordItemType_combo",
	"NoteRecordItemType_life",
	"NoteRecordItemType_score",
	"NoteRecordItemType_SummyCombo" 
};

typedef struct 
{
	unsigned char datalen;
	unsigned char type;
#ifdef __linux__
	uint8_t data[0];
#endif
} PkItemData;

typedef struct
{
	unsigned int row;
	uint8_t item_count;
#ifdef __linux__
	PkItemData data[0];
#endif
} GameItemData;

#pragma pack()
void p_data(uint8_t t, int l, char *v)
{
	int v0 = 0;
	switch(t)
	{
		case NoteRecordItemType_Judgment:
			fprintf(stdout, "%s %u\n", type_msg[t - NoteRecordItemType_Judgment], (uint8_t)*v);
			break;
		case NoteRecordItemType_combo:
			fprintf(stdout, "%s %u\n", type_msg[t - NoteRecordItemType_Judgment], (uint32_t)*v);
			break;
		case NoteRecordItemType_life:
			fprintf(stdout, "%s %u\n", type_msg[t - NoteRecordItemType_Judgment], (uint8_t)*v);
			break;
		case NoteRecordItemType_score:
			memcpy(&v0, v, 4); 
			fprintf(stdout, "%s %d\n", type_msg[t - NoteRecordItemType_Judgment], v0);
			break;
		case NoteRecordItemType_SummyCombo:
			memcpy(&v0, v, 4); 
			fprintf(stdout, "%s %d\n", type_msg[t - NoteRecordItemType_Judgment], v0);
			break;
		default:
			break;
	}
}

int main(int c, char **v)
{
	if (c != 2)
	{
		fprintf(stderr, "%s scorefile\n", basename(v[0]));
		return -1;
	}
	int fd = open(v[1], O_RDONLY);
	if (fd < 0)
	{
		fprintf(stderr, "open %s error %m\n", v[1]);
		return -1;
	}
	char head[128] = {0x0};
	char subhead[128] = {0x0};
	while (1)
	{
		int n = read(fd, head, sizeof(GameItemData));
		if (n != sizeof(GameItemData))
		{
			fprintf(stderr, "read error %d %d\n", n, sizeof(GameItemData));
			break;
		}
		GameItemData *gamedata = (GameItemData *)head;
		fprintf(stdout, "head %u %u\n", gamedata->row, gamedata->item_count);

		int i = 0;
		for(; i < gamedata->item_count; i++)
		{
			n = read(fd, subhead, sizeof(PkItemData));
			if (n != sizeof(PkItemData))
			{
				fprintf(stderr, "read error %d %d\n", n, sizeof(PkItemData));
				return -1;
			}
			PkItemData *pkdata = (PkItemData *)subhead;
			if (pkdata->type > NoteRecordItemType_SummyCombo)
			{
				fprintf(stderr, "n= %d %u %x\n", n, pkdata->datalen, pkdata->type);
				return -1;
			}
			//fprintf(stdout, "sub head %u %s\n", pkdata->datalen, type_msg[pkdata->type - NoteRecordItemType_Judgment]);

			if (pkdata->datalen <= sizeof(PkItemData))
			{
				fprintf(stderr, "error %d %d\n", pkdata->datalen, sizeof(PkItemData));
				return -1;
			}

			char body[128] = {0x0};
			int rn = pkdata->datalen - sizeof(PkItemData);
			n = read(fd, body, rn);
			if (n != rn)
			{
				fprintf(stderr, "error %d %d\n", n, rn);
				return -1;
			}
			p_data(pkdata->type, n, body);
		}
		fprintf(stdout, "\n\n");
	}
	close(fd);
	return 0;
}

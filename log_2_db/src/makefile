CC=gcc
CXX=g++
INC+= -I./  -I../lib -I/usr/include/mysql -I../3rdlib
LIB+= -lpthread -ldl -lrt -rdynamic 
LIB+=-L../lib -lvfs -L/usr/lib64/mysql/ -lmysqlclient 

CFLAGS+= -g -O2 -pipe -Wall -fno-strict-aliasing -D_GNU_SOURCE -D_REENTRANT -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE=1 -D_LARGE_FILES=1 -D_XOPEN_SOURCE=600
TARGET= log_2_db
ALL:$(TARGET)

OBJS = main.o plugins.o aimei_data_config.o

log_2_db:$(OBJS)
	$(CXX)	$(CFLAGS) -o $@ $^ $(LIB)

%.o: %.cpp
	$(CXX)  $(CFLAGS) $(INC) -c -o $@ $< 	 
%.o: %.c
	$(CC)  $(CFLAGS) $(INC) -c -o $@ $< 	 
clean:
	rm -f *.o
	rm -f $(TARGET) 	

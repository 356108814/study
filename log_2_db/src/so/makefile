CC=gcc
CXX=g++
INC+= -I../ -I../../lib  -I../../3rdlib -I/usr/include/mysql 
LIB+=-lpthread  -L../../lib -lvfs  -L/usr/lib64/mysql/ -lmysqlclient
CFLAGS+= -g -O2 -pipe -Wall -fno-strict-aliasing -D_GNU_SOURCE -D_REENTRANT -D_FILE_OFFSET_BITS=64 -fPIC -shared #-z defs
TARGET=minik_logic_log.so
ALL:$(TARGET)
minik_logic_log_OBJ=minik_logic_log.o

minik_logic_log.so: $(minik_logic_log_OBJ)
	$(CC)	$(CFLAGS) -o $@ $^ $(LIB)
%.o: %.cpp
	$(CXX)  $(CFLAGS) $(INC) -c -o $@ $< 	 
%.o: %.c
	$(CC)  $(CFLAGS) $(INC) -c -o $@ $< 	 
clean:
	rm -f *.o *.so
	rm -f $(TARGET) 	

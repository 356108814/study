OBJ=log.o  util_ip.o myconfig.o md5.o util_hex.o util_misc.o util_str.o myepoll.o protocol.o acl.o common.o pro_voss.o GeneralHashFunctions.o cJSON.o parsepara.o sha1.o sha1sum.o ssllib.o mydb.o valid_check.o dis.o
LIBNAME=libvfs
CXX=g++

# Fallback to gcc when $CC is not in $PATH.
CC:=$(shell sh -c 'type $(CC) >/dev/null 2>/dev/null && echo $(CC) || echo gcc')
OPTIMIZATION?=-O3
WARNINGS=-Wall -W -Wstrict-prototypes -Wwrite-strings
DEBUG?= -g -ggdb
REAL_CFLAGS=$(OPTIMIZATION) -fPIC $(CFLAGS) $(WARNINGS) $(DEBUG)
REAL_LDFLAGS=$(LDFLAGS)
LIB+= -lpthread -ldl -lrt -rdynamic -lz -lstdc++ -L./ -lmnm -lssl -lcrypto  -L/usr/lib64/mysql/ -lmysqlclient -lm
MLIB=$(LIB) libmnm.a
CFLAGS+= -g -O2 -pipe -Wall -fno-strict-aliasing -D_GNU_SOURCE -D_REENTRANT -Wl,-Bdynamic -fPIC -Wno-sizeof-pointer-memaccess -lssl -lcrypto -I/usr/include/mysql -I../3rdlib
#INCLUDE = -I/home/jingchun.zhang/st/mysql/include/mysql
CFLAGS+= $(INCLUDE)
TARGET = testjson testrsa testsha1 test_rsa testdns test_rsa_all test_time test_dis test_hash

STLIBSUFFIX=a
STLIBNAME=$(LIBNAME).$(STLIBSUFFIX)
STLIB_MAKE_CMD=ar rcs $(STLIBNAME)
ALL: $(STLIBNAME) $(TARGET)

$(STLIBNAME): $(OBJ)
	$(STLIB_MAKE_CMD) $(OBJ)

testdns: testdns.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

testjson: testjson.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

testrsa: testrsa.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

test_rsa_all: test_rsa_all.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

test_rsa: test_rsa.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

test_hash: test_hash.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

test_dis: test_dis.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

testsha1: testsha1.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

test_time: test_time.o
	$(CXX)	$(CFLAGS) -o $@ $^ -L./ -lvfs

%.o: %.cpp
	$(CC) -std=c99 -pedantic -c $(REAL_CFLAGS) $<

clean:
	rm -rf $(STLIBNAME) *.o $(TARGET)

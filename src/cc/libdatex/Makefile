CC = g++
CCFLAGS = -std=c++17 -Wall -Wextra -Wfatal-errors -flto -O3
INCLUDES =
LIBS = -flto


all: libdatex.so

libdatex.so: cc_version04.cc
	$(CC) $(CCFLAGS) $(INCLUDES) -fPIC -shared $^ $(LIBS) -o $@

clean:
	rm -f *.o
	rm -f *.so



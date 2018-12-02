CC = g++
CCFLAGS = -std=c++14 -Wall -O2 -static
INCLUDES = -I./ -I/usr/local/include/python3.5m
LIBS = -lpython3.5m -lpthread


all: test_1

test_1: test_1.o cc4py_1.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

test_2: test_2.o cc4py_2.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

%.o: %.cc
	$(CC) -c $(CCFLAGS) $(INCLUDES) $< -o $@

clean:
	rm -f *.o test_1 test_2


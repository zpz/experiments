CC = g++
CCFLAGS = -std=c++14 -Wall -O3 -static
INCLUDES = -I./ -I/usr/local/include/python3.5m
LIBS = -lpython3.5m
LLFLAGS =


all: test_basic test_cast test_copy test_ref test_kwargs


test_basic: test_basic.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

test_cast: test_cast.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

test_copy: test_copy.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

test_ref: test_ref.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

test_kwargs: test_kwargs.o
	$(CC) $(LLFLAGS) $^ $(LIBS) -o $@

%.o: %.cc
	$(CC) -c $(CCFLAGS) $(INCLUDES) $< -o $@

clean:
	rm -f *.o core test_basic test_cast test_copy test_ref test_kwargs



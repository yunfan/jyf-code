all: test

test: test.o core_engine.o
	gcc test.o core_engine.o -o test

test.o: test.c
	gcc -c test.c -o test.o

core_engine.o: core_engine.c
	gcc -c core_engine.c -o core_engine.o

clean:
	@rm -rf *.o
	@rm test

LDFLAGS = `sdl-config --libs`
CFLAGS = `sdl-config --cflags`
all: test

test: core_engine.o render_engine.o

clean:
	@rm -rf *.o
	@rm test

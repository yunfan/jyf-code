cc= tcc
mix:libchain.so mix.c
	$(cc) -I./ -L./ -lchain mix.c -o mix
libchain.so:chain.c chain.h
	$(cc) -shared -fPIC chain.c -o libchain.so
clean:
	rm *.so
	rm mix

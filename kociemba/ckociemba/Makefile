CKOCIEMBA_SRC = coordcube.c cubiecube.c facecube.c search.c
CKOCIEMBA_INCLUDE = include
CFLAGS = -std=c99 -O3 -D_XOPEN_SOURCE=700
BINDIR = bin
CACHEDIR = cache
BIN = kociemba

all solve: solve.c $(CKOCIEMBA_SRC)
	mkdir -p $(BINDIR)
	gcc $(CFLAGS) $(CKOCIEMBA_SRC) -I$(CKOCIEMBA_INCLUDE) solve.c -o $(BINDIR)/$(BIN)

clean:
	rm -rf $(BINDIR) $(CACHEDIR)

install:
	cp bin/kociemba /usr/local/bin/

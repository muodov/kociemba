CKOCIEMBA_SRC = ckociemba/coordcube.c ckociemba/cubiecube.c ckociemba/facecube.c ckociemba/search.c
CKOCIEMBA_INCLUDE = ckociemba/include
CFLAGS = -std=c99

solve: solve.c $(CKOCIEMBA_SRC)
	gcc $(CFLAGS) $(CKOCIEMBA_SRC) -I$(CKOCIEMBA_INCLUDE) solve.c -o solve


import cffi

ffi = cffi.FFI()
ffi.set_source(
    "kociemba.ckociembawrapper",
    """
    #include <stdio.h>
    #include <stdlib.h>
    #include <search.h>

    char* solve(char *cubestring, char *patternstring, char *cache_dir)
    {
        char patternized[64];
        if (patternstring) {
            patternize(cubestring, patternstring, patternized);
            cubestring = patternized;
        }

        char *sol = solution(
            cubestring,
            24,
            1000,
            0,
            cache_dir
        );
        return sol;
    }
    """,
    include_dirs=['kociemba/ckociemba/include'],
    sources=[
        'kociemba/ckociemba/coordcube.c',
        'kociemba/ckociemba/cubiecube.c',
        'kociemba/ckociemba/facecube.c',
        'kociemba/ckociemba/search.c'],
    extra_compile_args=['-std=c99', '-O3', '-D_XOPEN_SOURCE=700'])

ffi.cdef("char* solve(char *cubestring, char *patternstring, char *cache_dir);")

if __name__ == "__main__":
    ffi.compile(verbose=True)

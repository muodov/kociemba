#include <stdio.h>
#include <stdlib.h>
#include "search.h"

int main(int argc, char **argv)
{
    if (argc > 1) {
        char *sol = solution(
            argv[1],
            24,
            1000,
            0
        );
        puts(sol);
        free(sol);
        return 0;
    } else {
        return 1;
    }
}

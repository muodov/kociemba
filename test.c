#include <stdio.h>
#include <stdlib.h>
#include "search.h"

int main(int argc, char **argv)
{
    char *sol = solution(
        "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF",
        24,
        1000,
        0
    );
    printf("%s\n", sol);
    //free(sol);
}

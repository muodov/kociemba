#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/stat.h>
#include <string.h>
#include "prunetable_helpers.h"

char * join_path(const char *dir, const char *filename)
{
    size_t path_len = strnlen(dir, 500);
    char *fpath = calloc(path_len + 32, 1);
    if (path_len == 500) {
        return NULL;
    }
    strcpy(fpath, dir);
    strcat(fpath, "/");
    strncat(fpath, filename, 30);
    return fpath;
}

int check_cached_table(const char* name, void* ptr, int len, const char *cache_dir)
{
    int res = 0;
    char *fname = join_path(cache_dir, name);
    if (fname == NULL) {
        fprintf(stderr, "Path to cache tables is too long\n");
        return -1;
    }

    if (access(fname, F_OK | R_OK) != -1) {
        // fprintf(stderr, "Found cache for %s. Loading...", name);
        read_from_file(ptr, len, fname);
        // fprintf(stderr, "done.\n");
        res = 0;
    } else {
        fprintf(stderr, "Cache table %s was not found. Recalculating.\n", fname);
        res = 1;
    }
    free(fname);
    return res;
}

void read_from_file(void* ptr, int len, const char* name)
{
    FILE* f = fopen(name, "rb");
    if (!fread(ptr, len, 1, f))
        ((void)0); // suppress -Wunused-result warning
    fclose(f);
}

int make_dir(const char *cache_dir)
{
#if defined(_WIN32)
    return _mkdir(cache_dir);
#else
    return mkdir(cache_dir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
#endif
}

void dump_to_file(void* ptr, int len, const char* name, const char *cache_dir)
{
    int status;
    status = make_dir(cache_dir);
    if (status == 0 || errno == EEXIST) {
        char *fname = join_path(cache_dir, name);
        if (fname == NULL) {
            fprintf(stderr, "Path to cache tables is too long\n");
        } else {
            FILE* f = fopen(fname, "wb");
            fwrite(ptr, len, 1, f);
            free(fname);
            fclose(f);
        }
    } else {
        fprintf(stderr, "cannot create cache tables directory\n");
    }
}

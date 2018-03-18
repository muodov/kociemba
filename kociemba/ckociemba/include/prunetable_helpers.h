#ifndef PRUNETABLE_HELPERS_H
#define PRUNETABLE_HELPERS_H

#if defined(_WIN32)
#include <io.h>
#include "direct.h"
#define R_OK 4 /* Test for read permission. */
#define W_OK 2 /* Test for write permission. */
#define X_OK 1 /* Test for execute permission. */
#define F_OK 0 /* Test for existence. */
#define access _access
#else
#include <unistd.h>
#endif

int make_dir(const char *cache_dir);
int check_cached_table(const char* name, void* ptr, int len, const char *cache_dir);
void dump_to_file(void* ptr, int len, const char* name, const char *cache_dir);
void read_from_file(void* ptr, int len, const char* name);

#endif

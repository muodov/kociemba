/** This file is part of the Mingw32 package.
*  unistd.h maps     (roughly) to io.h
*/
#ifndef _UNISTD_H  
#define _UNISTD_H  
#include <io.h>  
#include <process.h>  
#define R_OK 4 /* Test for read permission. */
#define W_OK 2 /* Test for write permission. */
#define X_OK 1 /* Test for execute permission. */
#define F_OK 0 /* Test for existence. */
#endif /* _UNISTD_H */ #pragma once

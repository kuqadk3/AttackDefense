#define _GNU_SOURCE 1
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <dlfcn.h>

ssize_t (*orig_read)(int, void*, int);
char *(*orig_fgets)(char*, int, FILE*);
int (*orig_getc)(FILE*);

char *gets(char *str) {
    if (orig_read == 0)
        *(void **)(&orig_read) = dlsym(RTLD_NEXT, "read");

    int max_size = 0x20, read_size;
    if ((read_size = (*orig_read)(0, str, max_size)) == -1)
        return NULL;
    str[read_size - 1] = 0;

    char log[128];
    snprintf(log, 128, "[+] gets(%p = '%s')\n", str, str);
    write(3, log, strlen(log));

    return str;
}

ssize_t read (int fd, void *buf, size_t nbytes) {
    if (orig_read == 0)
        *(void **)(&orig_read) = dlsym(RTLD_NEXT, "read");

    int read_size = (*orig_read)(fd, buf, nbytes);
    if (read_size < 0)
        return -1;

    char log[128];
    snprintf(log, 128, "[+] read(%i, %p = '%s', %li)\n", fd, buf, (char *)&buf, nbytes);
    write(3, log, strlen(log));
    return read_size;
}

char *fgets(char *str, int n, FILE *stream){
    if (orig_fgets == 0)
        *(void **)(&orig_fgets) = dlsym(RTLD_NEXT, "fgets");

    (*orig_fgets)(str, n, stream);
    
    char log[128];
    snprintf(log, 128, "[+] fgets(%p = '%s', %i, %p)\n", str, str, n, stream);
    write(3, log, strlen(log));

    return str;
}

int getc(FILE *stream) {
    if (orig_getc == 0)
        *(void **)(&orig_getc) = dlsym(RTLD_NEXT, "getc");

    int res = (*orig_getc)(stream);

    char log[128];
    snprintf(log, 128, "[+] getc(%p) = %c\n", stream, res);
    write(3, log, strlen(log));

    return res;
}

void free(void *ptr) {
}

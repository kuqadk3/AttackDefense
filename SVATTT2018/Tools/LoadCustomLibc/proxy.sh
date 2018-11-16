#! /bin/sh

# gcc -shared -fPIC -o lib.so lib.c -ldl
LD_PRELOAD='./lib.so' ./matrix_patched

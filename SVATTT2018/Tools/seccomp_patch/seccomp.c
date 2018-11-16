// gcc -masm=intel -nostdlib -nodefaultlibs -fPIC -Wl,-shared seccomp.c -o seccomp

#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>

#include <sys/types.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/socket.h>

#include <linux/filter.h>
#include <linux/seccomp.h>
#include <linux/audit.h>

#define ArchField offsetof(struct seccomp_data, arch)

#define Allow(syscall) \
    BPF_JUMP(BPF_JMP+BPF_JEQ+BPF_K, SYS_##syscall, 0, 1), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW)

#define Disallow(syscall) \
    BPF_JUMP(BPF_JMP+BPF_JEQ, SYS_##syscall, 0, 1), \
    BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL)

void init_seccomp(int argc, char *argv[], char *envp[]) {
    int _argc = argc;
    char **_argv = argv;
    char **_envp = envp;
    long long main_addr;

    asm volatile(
        "lea rax, [rip - 0x1111];"
        "mov %0, rax;"
        :"=r" (main_addr)
        :
        :"rax"
    );


    struct sock_filter filter[] = {
        /* validate arch */
        BPF_STMT(BPF_LD+BPF_W+BPF_ABS, ArchField),
        BPF_JUMP( BPF_JMP+BPF_JEQ+BPF_K, AUDIT_ARCH_X86_64, 1, 0),
        BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL),
    
        /* load syscall */
        BPF_STMT(BPF_LD+BPF_W+BPF_ABS, offsetof(struct seccomp_data, nr)),
    
        /* list of syscalls */
        Disallow(execve),
        Disallow(execveat),
        Disallow(fork),
        Disallow(vfork),
        Disallow(clone),
        Disallow(creat),
        Disallow(mprotect),
        Disallow(socket),
        Disallow(dup2),
        Disallow(name_to_handle_at),
        Disallow(open_by_handle_at),
        Disallow(open),
        Disallow(openat),
    
        /* and if we don't match above, die */
        BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_ALLOW),
        /* BPF_STMT(BPF_RET+BPF_K, SECCOMP_RET_KILL), */
    };

    struct sock_fprog filterprog = {
        .len = sizeof(filter)/sizeof(filter[0]),
        .filter = filter
    };

    asm volatile(
        "mov rax, 0x9d;"
        "mov rdi, 0x26;"
        "mov rsi, 0x1;"
        "xor rdx, rdx;"
        "xor r10, r10;"
        "xor r8, r8;"
        "xor r9, r9;"
        "syscall;"
        :
        :
        :"rax", "rdi", "rsi", "rdx", "r10", "r8", "r9"
    );

    asm volatile(
        "mov rax, 0x9d;"
        "mov rdi, 0x16;"
        "mov rsi, 0x2;"
        "mov rdx, %0;"
        "syscall;"
        :
        :"r" (&filterprog)
        :"rax", "rdi", "rsi", "rdx"
    );

    asm volatile(
        "xor rdi, rdi;"
        "mov edi, %0;"
        "mov rsi, %1;"
        "mov rdx, %2;"
        "mov rax, %3;"
        "call rax;"
        :
        :"r" (_argc), "r" (_argv), "r" (_envp), "r" (main_addr)
        :"rdi", "rsi", "rdx", "rax"
    );
}

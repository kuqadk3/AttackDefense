#! /usr/bin/python2

import lief, sys, os, subprocess
from pwn import *

def main():
    binary = lief.parse(sys.argv[1])
    
    main_addr = binary.get_content_from_virtual_address(binary.header.entrypoint + 0x20, 4)
    main_addr = (main_addr[3] << 24) | (main_addr[2] << 16) | (main_addr[1] << 8) | main_addr[0]
    
    subprocess.call(["gcc", "-masm=intel", "-nostdlib", "-nodefaultlibs", "-fPIC", "-Wl,-shared", "seccomp.c", "-o", "seccomp"])
    seccomp = lief.parse("seccomp")
    seccomp_seg = seccomp.segments[0]
    seccomp_seg = binary.add(seccomp_seg)
    
    init_seccomp_addr = seccomp_seg.virtual_address + seccomp.get_symbol("init_seccomp").value
    init_seccomp_offset = init_seccomp_addr - (binary.entrypoint + 0x24)
    code = asm('lea rdi, [rip + %s]' % hex(init_seccomp_offset), arch='amd64')
    code = unpack(code, 'all')
    binary.patch_address(binary.header.entrypoint + 0x1d, code, 7)
    
    if binary.is_pie:
        main_addr += binary.entrypoint + 0x24
    main_offset = init_seccomp_addr + 0x45 - main_addr
    main_offset = (-main_offset) & (2**32-1)
    binary.patch_address(init_seccomp_addr + 0x41, main_offset, 4)
    
    binary.write(sys.argv[1] + "_patched")


if __name__ == '__main__':
    main()

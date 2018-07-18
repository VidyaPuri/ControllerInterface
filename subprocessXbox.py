#!/usr/bin/env/ python

import subprocess

password = subprocess.Popen(["echo", "waka"], stdout=subprocess.PIPE)

with subprocess.Popen(["sudo", "-S", "xboxdrv", "--detach-kernel-driver"], stdin=password.stdout, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as nigga:
    for line in nigga.stdout:
        print(line, end='')

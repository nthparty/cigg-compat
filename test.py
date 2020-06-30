"""Load and confirm compatibility of CIGG for current environment."""

import sys
import platform
import canaries

print("sys.maxsize: ", sys.maxsize)
print("platform.system(): ", platform.system())

lib = canaries.load({
    'Linux': ['./cigg.linux.so'],
    'Darwin': ['./cigg.macos.so'],
    'Windows': ['./cigg.dll']
})

assert(lib is not None)

"""Load and confirm compatibility of CIGG for current environment."""

# Check that the object file can be loaded and invoked.
import canaries

lib = canaries.load({
    'Linux': ['./cigg.linux.so'],
    'Darwin': ['./cigg.macos.so'],
    'Windows': ['./cigg.dll']
})

assert(lib is not None)

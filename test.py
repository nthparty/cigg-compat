"""Load and confirm compatibility of CIGG for current environment."""

# Check that the object file can be loaded and invoked.
import canaries

lib = canaries.load({
    'Linux': ['./cigg.linux.so'],
    'Darwin': ['./cigg.macos.so'],
    'Windows': ['./cigg.dll']
})

assert(lib is not None)

# Check some of the cryptographic primitives it exports.
import ctypes

key = bytes(list(range(32)))
data = bytes(list(range(32)))

ciphertext_ = ctypes.create_string_buffer(len(data)+200)
key_ = ctypes.create_string_buffer(key)
message_ = ctypes.create_string_buffer(bytes(data))
try:
    length_ = ctypes.create_string_buffer(len(data).to_bytes(4, 'little'))
except:
    length_ = ctypes.create_string_buffer(bytes([32, 0, 0, 0]))
lib.server_encrypt_to_self(ciphertext_, key_, message_, length_)
print(ciphertext_.raw)
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
data = bytes(list(range(32))*100)

ciphertext_ = ctypes.create_string_buffer(len(data)+16)
key_ = ctypes.create_string_buffer(key)
message_ = ctypes.create_string_buffer(bytes(data))
try:
    length_ = ctypes.create_string_buffer(len(data).to_bytes(4, 'little'))
except:
    length_ = ctypes.create_string_buffer(bytes([128, 12, 0, 0]))
lib.server_encrypt_to_self(ciphertext_, key_, message_, length_)
ciphertext = bytes(ciphertext_.raw)

message_ = ctypes.create_string_buffer(len(ciphertext)-16)
ciphertext_ = ctypes.create_string_buffer(bytes(ciphertext))
try:
    length_ = ctypes.create_string_buffer(len(ciphertext).to_bytes(4, 'little'))
except:
    length_ = ctypes.create_string_buffer(bytes([144, 12, 0, 0]))
lib.server_decrypt_from_self(message_, key_, ciphertext_, length_)
data_ = bytes(message_.raw)

assert(data == data_)

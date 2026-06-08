import ctypes
import os

# error codes
ERR_OK = 0

# type definitions
c_uint8_p = ctypes.POINTER(ctypes.c_uint8)
c_size_t = ctypes.c_size_t

def set_func_defs(func_name, restype, argtypes):
        try:
            func = getattr(tzi_lib, func_name)
            func.restype = restype
            func.argtypes = argtypes
            return func
        except AttributeError:
            print(f"Warning: Function '{func_name}' not found in library.")
            return None

tzi_lib = None
try:
    # crypto/ -> app/ -> project root -> tzi/libs
    lib_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "tzi", "libs", "TZICrypt.dll")
    )
    tzi_lib = ctypes.CDLL(lib_path)
except (OSError, AttributeError) as e:
    print(f"Could not load the library from {lib_path}. Error: {e}")

if tzi_lib:    
    # Compute hash using the belt-hash algorithm
    # Parameters:
    #   x: const uint8_t* - pointer to the message to be hashed
    #   x_size: size_t - size of the message in bytes
    #   y: uint8_t* - pointer to the buffer for the resulting hash value (32 bytes)
    # Returns: err_type (int) - error code (0 = success)
    tzi_belt_hash = set_func_defs('tzi_belt_hash', ctypes.c_int, [c_uint8_p, c_size_t, c_uint8_p])

    # Compute MAC using the belt-mac algorithm
    # Parameters:
    #   k: const uint8_t* - pointer to the key (32 bytes)
    #   x: const uint8_t* - pointer to the message
    #   x_size: size_t - size of the message in bytes
    #   t: uint8_t* - pointer to the buffer for the resulting MAC value (8 bytes)
    # Returns: err_type (int) - error code (0 = success)
    tzi_belt_mac = set_func_defs('tzi_belt_mac', ctypes.c_int, [c_uint8_p, c_uint8_p, c_size_t, c_uint8_p])

    # Key derivation function bake-kdf
    # Parameters:
    #   x: const uint8_t* - pointer to the secret word
    #   x_size: size_t - size of the secret word
    #   s: const uint8_t* - pointer to the extra word
    #   s_size: size_t - size of the extra word
    #   c: size_t - key number
    #   y: uint8_t* - pointer to the buffer for the resulting key (32 bytes)
    # Returns: err_type (int) - error code (0 = success)
    tzi_bake_kdf = set_func_defs('tzi_bake_kdf', ctypes.c_int, [c_uint8_p, c_size_t, c_uint8_p, c_size_t, c_size_t, c_uint8_p])

def belt_hash(data: bytes) -> bytes:
    if tzi_lib is None:
        raise RuntimeError("TZICrypt.dll is not loaded; belt_hash is unavailable")

    # using ctypes array
    data_array = (ctypes.c_ubyte * len(data))(*data)
    buf = (ctypes.c_ubyte * 32)()

    err = tzi_belt_hash(data_array, len(data), buf)
    if err != ERR_OK:
        raise ValueError(f"Hashing error with code {err}")

    return bytes(buf)

def belt_mac(key: bytes, data: bytes) -> bytes:
    if tzi_lib is None:
        raise RuntimeError("TZICrypt.dll is not loaded; belt_mac is unavailable")
    if len(key) != 32:
        raise ValueError("Key must be 32 bytes long")

    key_array = (ctypes.c_ubyte * 32)(*key)
    data_array = (ctypes.c_ubyte * len(data))(*data)
    buf = (ctypes.c_ubyte * 8)()

    err = tzi_belt_mac(key_array, data_array, len(data), buf)
    if err != ERR_OK:
        raise ValueError(f"MAC error with code {err}")

    return bytes(buf)

def bake_kdf(secret: bytes, extra: bytes, key_num: int) -> bytes:
    if tzi_lib is None:
        raise RuntimeError("TZICrypt.dll is not loaded; bake_kdf is unavailable")

    secret_array = (ctypes.c_ubyte * len(secret))(*secret)
    extra_array = (ctypes.c_ubyte * len(extra))(*extra)
    buf = (ctypes.c_ubyte * 32)()

    err = tzi_bake_kdf(secret_array, len(secret), extra_array, len(extra), key_num, buf)
    if err != ERR_OK:
        raise ValueError(f"KDF error with code {err}")

    return bytes(buf)

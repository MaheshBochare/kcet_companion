import os
import sys
import ctypes

torch_path = os.path.join(sys.prefix, "Lib", "site-packages", "torch", "lib")

os.add_dll_directory(torch_path)
ctypes.CDLL(os.path.join(torch_path, "c10.dll"))

import torch
print("Torch loaded successfully")

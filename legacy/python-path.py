import os

from pathlib import Path

print(f"{Path.cwd()}\data")
print(Path.home())

path_lib = f"{Path.cwd()}\data"
print(os.getcwd())
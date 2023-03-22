from common import *
import sys
import subprocess

export_env_var()

print(sys.argv)
print(os.getcwd())
subprocess.run(sys.argv[1:])

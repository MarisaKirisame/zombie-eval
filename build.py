import os
import subprocess

subprocess.run("ls", shell=True, check=True)
subprocess.run("git clone git@github.com:MarisaKirisame/zombie.git", shell=True, check=False)
os.chdir("zombie")
subprocess.run("mkdir build", shell=True, check=False)
os.chdir("build")
subprocess.run("ls", shell=True, check=True)
subprocess.run("cmake ../..", shell=True, check=True)
subprocess.run("make", shell=True, check=True)

print("hello world")

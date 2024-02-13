import os
import subprocess

subprocess.run("ls", shell=True, check=True)
subprocess.run("git clone git@github.com:MarisaKirisame/zombie.git", shell=True, check=False)
os.chdir("zombie")
subprocess.run("git pull", shell=True, check=False)
subprocess.run("mkdir build", shell=True, check=False)
os.chdir("build")
subprocess.run("cmake ..", shell=True, check=True)
subprocess.run("make", shell=True, check=True)

os.chdir("../..")
subprocess.run("git clone git@github.com:MarisaKirisame/TVirus.git", shell=True, check=False)
os.chdir("TVirus")
subprocess.run("git pull", shell=True, check=False)

print("hello world")

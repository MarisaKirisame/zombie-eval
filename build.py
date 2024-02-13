import subprocess

subprocess.run("git clone git@github.com:MarisaKirisame/zombie.git", shell=True, check=False)
subprocess.run("cd zombie", shell=True, check=True)
subprocess.run("mkdir build", shell=True, check=False)
subprocess.run("cmake ../..", shell=True, check=True)
subprocess.run("make", shell=True, check=True)

print("hello world")

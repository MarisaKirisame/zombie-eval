import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def run_ok(cmd):
    return subprocess.run(cmd, shell=True).returncode == 0

if not run_ok("mill -v"):
    run("""curl -fL "https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz" | gzip -d > cs""")
    run("chmod +x cs")
    run("yes | ./cs setup")

run("git clone git@github.com:MarisaKirisame/zombie.git || true")
os.chdir("zombie")
run("git pull")
run("mkdir build || true")
os.chdir("build")
run("cmake ..")
run("make")

os.chdir("../..")
run("git clone git@github.com:MarisaKirisame/TVirus.git || true")
os.chdir("TVirus")
run("git pull")

raise

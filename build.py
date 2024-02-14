import os
import subprocess

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def run_ok(cmd):
    return subprocess.run(cmd, shell=True).returncode == 0

def append_envvar(name, val):
    if name in os.environ:
        os.environ[name] = val + ":" + os.environ[name]
    else:
        os.environ[name] = val

project_cwd = os.getcwd()

append_envvar("PATH", os.environ["HOME"] + "/.local/share/coursier/bin")
append_envvar("PATH", os.environ["HOME"] + "/.cache/coursier/arc/https/github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.22%252B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz/jdk-11.0.22+7/bin")
append_envvar("JAVA_HOME", os.environ["HOME"] + "/.cache/coursier/arc/https/github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.22%252B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.22_7.tar.gz/jdk-11.0.22+7")
append_envvar("CPLUS_INCLUDE_PATH", project_cwd + "/json/single_include")
append_envvar("CPLUS_INCLUDE_PATH", project_cwd + "/local/include")

if not run_ok("mill -v"):
    run("""curl -fL "https://github.com/coursier/launchers/raw/master/cs-x86_64-pc-linux.gz" | gzip -d > cs""")
    run("chmod +x cs")
    run("yes | ./cs setup")
    run("./cs install mill")

run("git clone git@github.com:nlohmann/json.git || true")

run("git clone git@github.com:MarisaKirisame/zombie.git || true")
os.chdir("zombie")
run("git pull")
run("mkdir build || true")
os.chdir("build")
run(f"cmake -DCMAKE_INSTALL_PREFIX={project_cwd}/local ..")
run("make install")
run("ls local")

os.chdir("../..")
run("git clone git@github.com:MarisaKirisame/TVirus.git || true")
os.chdir("TVirus")
run("git pull")

run("python3 drive.py")
run("python3 anal.py")

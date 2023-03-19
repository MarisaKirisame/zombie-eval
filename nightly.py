from pathlib import Path
import os
import subprocess

zombie_eval_dir = Path.cwd()
assert zombie_eval_dir.name == "Zombie-Eval"
third_party_dir = Path("third_party").resolve()
third_party_dir.mkdir(exist_ok=True)
install_dir = Path("_build").resolve()
install_dir.mkdir(exist_ok=True)

def query(script):
    return subprocess.check_output(script, shell=True, text=True)

def run(script):
    subprocess.run(script, shell=True, check=True)

def export_env_var():
    arch = query("dpkg-architecture -qDEB_HOST_MULTIARCH 2> /dev/null").split()[0]
    
    os.environ['PATH'] += f":{install_dir}/bin"
    PKG_CONFIG_PATH = "PKG_CONFIG_PATH"
    os.environ.setdefault(PKG_CONFIG_PATH, "")
    os.environ[PKG_CONFIG_PATH] += f":{install_dir}/share/pkgconfig"
    os.environ[PKG_CONFIG_PATH] += f":{install_dir}/lib/pkgconfig"
    os.environ[PKG_CONFIG_PATH] += f":{install_dir}/lib64/pkgconfig"
    os.environ[PKG_CONFIG_PATH] += f":{install_dir}/lib/{arch}/pkgconfig"

    XDG_DATA_DIRS = "XDG_DATA_DIRS"
    os.environ.setdefault(XDG_DATA_DIRS, "")
    os.environ[XDG_DATA_DIRS] += f":{install_dir}/share:/usr/local/share:/usr/share"

    LD_LIBRARY_PATH = "LD_LIBRARY_PATH"
    os.environ.setdefault(LD_LIBRARY_PATH, "")
    os.environ[LD_LIBRARY_PATH] += f":{install_dir}/lib"
    os.environ[LD_LIBRARY_PATH] += f":{install_dir}/lib/{arch}"

    ACLOCAL_FLAGS = "ACLOCAL_FLAGS"
    os.environ.setdefault(ACLOCAL_FLAGS, "")
    os.environ[ACLOCAL_FLAGS] += f"-I {install_dir}/share/aclocal"

def update_repo(repo_name):
    os.chdir(third_party_dir)
    repo_path = Path(repo_name).resolve()
    if not repo_path.exists():
        run(f"git clone 'git@github.com:MarisaKirisame/{repo_name}.git'")
    os.chdir(repo_path)
    run("git commit -am 'save' || true")
    print(query("git status --porcelain"))
    if query("git status --porcelain") != "":
        print("Git repo dirty. Quit.")
        raise
    run("git pull")
    build_ok = Path("_build/ok")
    if build_ok.exists() and query("git rev-parse HEAD") != query("cat '_build/ok'"):
        run("rm '_build/ok'")

def babl():
    update_repo("babl")
    if not Path("_build").exists():
        run(f"meson _build --prefix={install_dir} --buildtype=release -Db_lto=true")
        run("meson configure _build -Denable-gir=true")
    if not Path("_build/ok").exists():
        run("ninja -C _build install")
        run("git rev-parse HEAD > '_build/ok'")

def gegl():
    update_repo("gegl")
    if not Path("_build").exists():
        run(f"meson _build --prefix={install_dir} --buildtype=release -Db_lto=true")
    if not Path("_build/ok").exists():
        run("ninja -C _build install")
        run("git rev-parse HEAD > '_build/ok'")

def gimp():
    update_repo("gimp")
    if not Path("_build").exists():
        run(f"meson _build --prefix={install_dir} --buildtype=release -Db_lto=true")
    if not Path("_build/ok").exists():
        run("ninja -C _build install")
        run("git rev-parse HEAD > '_build/ok'")

export_env_var()
babl()
gegl()
gimp()

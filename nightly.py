from pathlib import Path
import os
import subprocess
from common import *

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

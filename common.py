from pathlib import Path
import os
import subprocess

zombie_eval_dir = Path.cwd()
assert zombie_eval_dir.name == "zombie-eval"
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

    GI_TYPELIB_PATH = "GI_TYPELIB_PATH"
    os.environ.setdefault(GI_TYPELIB_PATH, "")
    os.environ[GI_TYPELIB_PATH] += f":{install_dir}/lib/{arch}/girepository-1.0"

from pathlib import Path
import os
import subprocess
from common import *

USE_GIT = True

class Module:
    def __init__(self, name, dependency):
        self.name = name
        os.chdir(third_party_dir)
        self.path = Path(self.name).resolve()
        self.build_path = Path(self.name + "/_build").resolve()
        self.build_ok_path = Path(self.name + "/_build/ok").resolve()
        self.dependency = dependency

        self.done = False
        self.dependent = []

        for m in self.dependency:
            m.dependent.append(self)

    def update(self):
        os.chdir(third_party_dir)
        if not self.path.exists():
            run(f"git clone 'git@github.com:MarisaKirisame/{self.name}.git'")
        os.chdir(self.path)
        if USE_GIT:
            run("git pull")
            run("git commit -am 'save' || true")
            run("git push || true")
            if query("git status --porcelain") != "":
                print(query("git status --porcelain"))
                print("Git repo dirty. Quit.")
                raise

    def build_impl(self):
        raise NotImplementedError

    def is_dirty(self):
        os.chdir(self.path)
        return not (self.build_ok_path.exists() and query("git rev-parse HEAD") == query("cat '_build/ok'"))

    def dirty(self):
        assert not self.done
        os.chdir(self.path)
        build_ok = Path("_build/ok")
        if build_ok.exists():
            run("rm '_build/ok'")
        assert self.is_dirty()

    def clean(self):
        assert self.is_dirty()
        os.chdir(self.path)
        run("git rev-parse HEAD > '_build/ok'")
        self.done = True
        assert not self.is_dirty()

    # cycle should not exist because dependency is a constructor parameter
    def build(self):
        if not self.done:
            print(f"building {self.name}...")
            self.update()
            for m in self.dependency:
                m.build()
            if self.is_dirty():
                print(f"working on {self.name}...")
                os.chdir(self.path)
                self.build_impl()
                print(f"{self.name} work ok!")
                for m in self.dependent:
                    m.dirty()
                self.clean()
            print(f"{self.name} build ok!")

class Zombie(Module):
    def __init__(self):
        super().__init__("zombie", [])

    def build_impl(self):
        if not Path("_build").exists():
            run("mkdir _build")
            os.chdir("_build")
            run(f"cmake -DCMAKE_INSTALL_PREFIX={install_dir} ../")
        os.chdir(self.build_path)
        run(f"make install")

zombie = Zombie()

class Babl(Module):
    def __init__(self):
        super().__init__("babl", [])

    def build_impl(self):
        if not Path("_build").exists():
            run(f"meson _build --prefix={install_dir} --buildtype=release -Db_lto=true")
            run("meson configure _build -Denable-gir=true")
        run("ninja -C _build install")


babl = Babl()

class Gegl(Module):
    def __init__(self):
        super().__init__("gegl", [babl, zombie])

    def build_impl(self):
        if not Path("_build").exists():
            run(f"meson _build --prefix={install_dir} --buildtype=release -Db_lto=true")
        run("ninja -C _build install")

gegl = Gegl()

class Gimp(Module):
    def __init__(self):
        super().__init__("gimp", [gegl])

    def build_impl(self):
        if not Path("_build").exists():
            run("mkdir _build")
            os.chdir("_build")
            run(f"../autogen.sh --prefix={install_dir} --disable-python")
        os.chdir(self.build_path)
        run("make install")
        os.chdir(zombie_eval_dir)
        run("cp scripts/* _build/share/gimp/2.0/scripts")

gimp = Gimp()

export_env_var()

gimp.build()

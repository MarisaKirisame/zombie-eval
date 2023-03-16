#!/bin/bash

set -e
set -x

zombie_eval_dir=$PWD

mkdir -p "third_party"
cd "third_party"
third_party_dir=$PWD

install_dir=${zombie_eval_dir}/build

export PATH="${install_dir}/bin:$PATH"
export PKG_CONFIG_PATH="${install_dir}/share/pkgconfig:${install_dir}/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export PKG_CONFIG_PATH="${install_dir}/lib64/pkgconfig:$PKG_CONFIG_PATH"
export XDG_DATA_DIRS="${XDG_DATA_DIRS:+$XDG_DATA_DIRS:}${install_dir}/share:/usr/local/share:/usr/share"
export LD_LIBRARY_PATH="${install_dir}/lib:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export ACLOCAL_FLAGS="-I $INSTALL_PREFIX/share/aclocal $ACLOCAL_FLAGS"

arch="$(dpkg-architecture -qDEB_HOST_MULTIARCH 2> /dev/null)"
export PKG_CONFIG_PATH="${install_dir}/lib/${arch}/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="${install_dir}/lib/${arch}:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

[ ! -d "babl" ] && git clone git@github.com:MarisaKirisame/babl.git
cd "babl"
git pull
meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
meson configure build -Denable-gir=true
ninja -C build install

cd $third_party_dir

[ ! -d "gegl" ] && git clone git@github.com:MarisaKirisame/gegl.git
cd "gegl"
git pull
meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
ninja -C build install

cd $third_party_dir

[ ! -d "gimp" ] && git clone git@github.com:MarisaKirisame/gimp.git
cd "gimp"
git pull
meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
ninja -C build install

cd $third_party_dir

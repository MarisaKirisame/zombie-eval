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

babl () {
    cd $third_party_dir
    if [ ! -d "babl" ] ; then
	git clone git@github.com:MarisaKirisame/babl.git
    fi
    cd "babl"
    git pull
    if [ ! -d "build" ] ; then
	meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
	meson configure build -Denable-gir=true
    fi
    if [ ! -f "build/ok" ] ; then
	ninja -C build install
	touch "build/ok"
    fi
}

gegl() {
    cd $third_party_dir
    [ ! -d "gegl" ] && git clone git@github.com:MarisaKirisame/gegl.git
    cd "gegl"
    git pull
    if [ ! -d "build" ] ; then
	meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
    fi
    if [ ! -f "build/ok" ] ; then
	ninja -C build install
	touch "build/ok"
    fi
}

gimp() {
    cd $third_party_dir
    [ ! -d "gimp" ] && git clone git@github.com:MarisaKirisame/gimp.git
    cd "gimp"
    git pull
    if [ ! -d "build" ] ; then
	meson build --prefix=${install_dir} --buildtype=release -Db_lto=true
    fi
    if [ ! -f "build/ok" ] ; then
	ninja -C build install
	touch "build/ok"
    fi
}

babl
gegl
gimp

#!/bin/bash

set -e
set -x

zombie_eval_dir=$PWD

mkdir -p "third_party"
cd "third_party"
third_party_dir=$PWD

install_dir=${zombie_eval_dir}/_build

export PATH="${install_dir}/bin:$PATH"
export PKG_CONFIG_PATH="${install_dir}/share/pkgconfig:${install_dir}/lib/pkgconfig${PKG_CONFIG_PATH:+:$PKG_CONFIG_PATH}"
export PKG_CONFIG_PATH="${install_dir}/lib64/pkgconfig:$PKG_CONFIG_PATH"
export XDG_DATA_DIRS="${XDG_DATA_DIRS:+$XDG_DATA_DIRS:}${install_dir}/share:/usr/local/share:/usr/share"
export LD_LIBRARY_PATH="${install_dir}/lib:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export ACLOCAL_FLAGS="-I $INSTALL_PREFIX/share/aclocal $ACLOCAL_FLAGS"

arch="$(dpkg-architecture -qDEB_HOST_MULTIARCH 2> /dev/null)"
export PKG_CONFIG_PATH="${install_dir}/lib/${arch}/pkgconfig:$PKG_CONFIG_PATH"
export LD_LIBRARY_PATH="${install_dir}/lib/${arch}:${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

update_repo () {
    cd $third_party_dir
    if [ ! -d "${1:?}" ] ; then
	git clone "git@github.com:MarisaKirisame/${1:?}.git"
    fi
    cd "${1:?}"
    git commit -am "save" || true
    if [ $(git status --porcelain | wc -l) != "0" ]; then
	echo "Git repo dirty. Quit."
	exit 1
    fi
    git pull
    if [ -e "_build/ok" ] && [ $(git rev-parse HEAD) != $(cat "_build/ok") ] ; then
	rm "_build/ok"
    fi
}

babl () {
    update_repo "babl"
    if [ ! -d "_build" ] ; then
	meson _build --prefix=${install_dir} --buildtype=release -Db_lto=true
	meson configure _build -Denable-gir=true
    fi
    if [ ! -f "_build/ok" ] ; then
	ninja -C _build install
	git rev-parse HEAD > "_build/ok"
    fi
}

gegl() {
    update_repo "gegl"
    if [ ! -d "_build" ] ; then
	meson _build --prefix=${install_dir} --buildtype=release -Db_lto=true
    fi
    if [ ! -f "_build/ok" ] ; then
	ninja -C _build install
	git rev-parse HEAD > "_build/ok"
    fi
}

gimp() {
    update_repo "gimp"
    if [ ! -d "_build" ] ; then
	meson _build --prefix=${install_dir} --buildtype=release -Db_lto=true
    fi
    if [ ! -f "_build/ok" ] ; then
	ninja -C _build install
	git rev-parse HEAD > "_build/ok"
    fi
}

babl
gegl
gimp

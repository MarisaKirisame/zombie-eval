#!/bin/bash

set -e
set -x

zombie_eval_dir=$PWD

cd "../"
[ ! -d "gegl" ] && git clone git@github.com:MarisaKirisame/gegl.git

cd gegl
git pull
meson _build
ninja -C _build

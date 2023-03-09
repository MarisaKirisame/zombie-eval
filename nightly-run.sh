#!/bin/bash

set -e
set -x

zombie_eval_dir=$PWD

cd "../"
[ ! -d "gegl" ] && git clone git@github.com:MarisaKirisame/gegl.git

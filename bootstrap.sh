#!/bin/bash

cd "$(dirname $0)"
git submodule init && git submodule update
./data/extras/enhance.py data/TextAsset/enUS.txt fireplace/cards/enUS.xml

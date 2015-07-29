#!/bin/bash

# check python version
PY_MAJOR=$(python -c 'import sys; print(sys.version_info[0])')
PY_MINOR=$(python -c 'import sys; print(sys.version_info[1])')

if [[ "$PY_MAJOR" -lt 3 ]]; then
	>&2 echo "ERROR: Python 3.4 is required to run Fireplace."
	exit 1
fi

if [[ "$PY_MINOR" -lt 4 ]]; then
	>&2 echo "WARNING: Python versions older than 3.4 are known to have issues."
fi

cd "$(dirname $0)"
git submodule init && git submodule update
./data/extras/enhance.py data/TextAsset/enUS.txt fireplace/cards/enUS.xml

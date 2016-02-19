#!/bin/bash

BASEDIR="$(dirname $0)"
HSDATA_URL="https://github.com/HearthSim/hs-data.git"
HSDATA_DIR="$BASEDIR/hs-data"
CARDDEFS_OUT="$BASEDIR/../fireplace/CardDefs.xml"

# check python version
PY_MAJOR=$(python -c 'import sys; print(sys.version_info[0])')
PY_MINOR=$(python -c 'import sys; print(sys.version_info[1])')

if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MINOR" -lt 5 ]]; then
	>&2 echo "ERROR: Python 3.5 is required to run Fireplace."
	exit 1
fi

command -v git &>/dev/null || {
	>&2 echo "ERROR: git is required to bootstrap Fireplace."
	exit 1
}

python -c "import hearthstone" &>/dev/null || {
	pip install -r "$BASEDIR/../requirements.txt"
}

echo "Fetching data files from $HSDATA_URL"
if [[ ! -e "$HSDATA_DIR" ]]; then
	git clone --depth=1 "$HSDATA_URL" "$HSDATA_DIR"
else
	git -C "$HSDATA_DIR" fetch &&
	git -C "$HSDATA_DIR" reset --hard origin/master
fi

python "$BASEDIR/bootstrap.py" "$HSDATA_DIR" "$CARDDEFS_OUT"

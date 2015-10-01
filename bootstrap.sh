#!/bin/bash
set -e

BASEDIR="$(readlink -f $(dirname $0))"
DATADIR="$BASEDIR/fireplace/cards/data"
HSDATA_DIR="$DATADIR/hs-data"
HSDATA_URL="https://github.com/HearthSim/hs-data.git"

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

echo "Fetching data files from $HSDATA_URL"
if [ ! -e "$HSDATA_DIR" ]; then
	git clone --depth=1 "$HSDATA_URL" "$HSDATA_DIR"
else
	git -C "$HSDATA_DIR" fetch &&
	git -C "$HSDATA_DIR" reset --hard origin/master
fi

"$DATADIR/__init__.py" "$HSDATA_DIR" "$DATADIR/CardDefs.xml"

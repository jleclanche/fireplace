#!PowerShell

$BASEDIR=Split-Path $script:MyInvocation.MyCommand.Path
$HSDATA_URL="https://github.com/HearthSim/hs-data.git"
$HSDATA_DIR="$BASEDIR/hs-data"
$CARDDEFS_OUT="$BASEDIR/../fireplace/CardDefs.xml"

# check python version
$PY_MAJOR=$(python -c 'import sys; print(sys.version_info[0])')
$PY_MINOR=$(python -c 'import sys; print(sys.version_info[1])')

if ($PY_MAJOR -lt 3 -Or $PY_MINOR -lt 5) {
	Write-Error "ERROR: Python 3.5 is required to run Fireplace."
	exit 1
}

if ((Get-Command "git.exe" -ErrorAction SilentlyContinue) -eq $null) {
	Write-Error "ERROR: git is required to bootstrap Fireplace."
	exit 1
}

Write-Output "Fetching data files from $HSDATA_URL"
if (!(Test-Path $HSDATA_DIR)) {
	git clone --depth=1 $HSDATA_URL $HSDATA_DIR
} else {
	git -C $HSDATA_DIR fetch | Write-Output
	if ($?) {
		git -C $HSDATA_DIR reset --hard origin/master | Write-Output
	}
}

python "$BASEDIR/bootstrap.py" $HSDATA_DIR $CARDDEFS_OUT

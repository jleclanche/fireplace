$ScriptDir = Split-Path $script:MyInvocation.MyCommand.Path
$DataDir = "$ScriptDir/fireplace/cards/data"
$HsdataDir = "$DataDir/hs-data"
$HsdataUrl = "https://github.com/HearthSim/hs-data.git"

# check python version
$PyMajor = $(python -c 'import sys; print(sys.version_info[0])')
$PyMinor = $(python -c 'import sys; print(sys.version_info[1])')

if ($PyMajor -lt 3) {
	Throw "ERROR: Python 3 and above is required to run Fireplace."
}

if ($PyMinor -lt 4) {
	Write-Error "WARNING: Python versions older than 3.4 are known to have issues."
}

Write-Output "Fetching data files from $HsdataUrl"
if (!(Test-Path $HsdataDir)) {
	git clone --depth=1 $HsdataUrl $HsdataDir
} else {
	git -C $HsdataDir fetch | Write-Output
	if ($?) {
		git -C $HsdataDir reset --hard origin/master | Write-Output
	}
}

python "$DataDir/__init__.py" $HsdataDir "$DataDir/CardDefs.xml"

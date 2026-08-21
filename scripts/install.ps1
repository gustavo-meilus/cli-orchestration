$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) {
    & py "$ScriptDir\install.py" @args
    exit $LASTEXITCODE
}
& python "$ScriptDir\install.py" @args
exit $LASTEXITCODE

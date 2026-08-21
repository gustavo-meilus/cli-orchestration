$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) {
    & py "$ScriptDir\verify_install.py" @args
    exit $LASTEXITCODE
}
& python "$ScriptDir\verify_install.py" @args
exit $LASTEXITCODE

param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [string]$DraftPath,

    [string]$ConfigPath,

    [string]$OverridePath,

    [string]$CachePath,

    [string]$WorkDir,

    [string]$PythonExe = "python",

    [switch]$DraftOnly
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
if (-not $ConfigPath) {
    $ConfigPath = Join-Path $root "translation\config\base_vi.json"
}
if (-not $CachePath) {
    $CachePath = Join-Path $root "_work\cache\google_vi_cache.json"
}
if (-not $WorkDir) {
    $WorkDir = Join-Path $root "_work"
}

if (-not (Test-Path -LiteralPath $WorkDir)) {
    New-Item -ItemType Directory -Force -Path $WorkDir | Out-Null
}

$cacheDirectory = Split-Path -Parent $CachePath
if ($cacheDirectory -and -not (Test-Path -LiteralPath $cacheDirectory)) {
    New-Item -ItemType Directory -Force -Path $cacheDirectory | Out-Null
}

$resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
$resolvedConfig = (Resolve-Path -LiteralPath $ConfigPath).Path
$resolvedOverride = if ($OverridePath) { (Resolve-Path -LiteralPath $OverridePath).Path } else { $null }
$resolvedDraft = if ($DraftPath) { (Resolve-Path -LiteralPath $DraftPath).Path } else { $null }

$stem = [IO.Path]::GetFileNameWithoutExtension($resolvedInput)
$sourceJson = Join-Path $WorkDir ("{0}.source.json" -f $stem)
$draftJson = Join-Path $WorkDir ("{0}.draft.json" -f $stem)
$updatesJson = Join-Path $WorkDir ("{0}.translations.json" -f $stem)

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "ppt-extract.ps1") `
    -InputPath $resolvedInput `
    -OutputPath $sourceJson

if ($resolvedDraft) {
    & powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "ppt-extract.ps1") `
        -InputPath $resolvedDraft `
        -OutputPath $draftJson
}

$pythonArgs = @(
    (Join-Path $PSScriptRoot "build-ppt-translation-json.py"),
    "--source-json", $sourceJson,
    "--config", $resolvedConfig,
    "--cache", $CachePath,
    "--output", $updatesJson
)

if ($resolvedDraft) {
    $pythonArgs += @("--current-json", $draftJson)
}
if ($resolvedOverride) {
    $pythonArgs += @("--override", $resolvedOverride)
}
if ($DraftOnly) {
    $pythonArgs += @("--draft-only")
}

& $PythonExe @pythonArgs

$basePresentation = if ($resolvedDraft) { $resolvedDraft } else { $resolvedInput }

& powershell -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "ppt-apply-translations.ps1") `
    -InputPath $basePresentation `
    -TranslationsPath $updatesJson `
    -OutputPath $OutputPath

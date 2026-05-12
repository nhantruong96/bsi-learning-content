param(
    [Parameter(Mandatory = $true)]
    [string]$CourseCode,

    [Parameter(Mandatory = $true)]
    [string]$CourseTitle,

    [string]$RootPath
)

$ErrorActionPreference = "Stop"

$workspaceRoot = if ($RootPath) {
    (Resolve-Path -LiteralPath $RootPath).Path
} else {
    Split-Path -Parent $PSScriptRoot
}

$courseRoot = Join-Path $workspaceRoot ("courses\{0}" -f $CourseCode)
$folders = @(
    "01_brief",
    "02_source",
    "03_authoring",
    "04_translation",
    "05_review",
    "06_delivery"
)

$sourcePackageFolders = @(
    "Certificate Sample",
    "Delegate Workbook",
    "Tutor Guide",
    "Version Control"
)

foreach ($folder in $folders) {
    $path = Join-Path $courseRoot $folder
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

foreach ($folder in $sourcePackageFolders) {
    $path = Join-Path $courseRoot ("02_source\{0}" -f $folder)
    if (-not (Test-Path -LiteralPath $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
    }
}

$readmePath = Join-Path $courseRoot "README.md"
if (-not (Test-Path -LiteralPath $readmePath)) {
    $readmeContent = @(
        "# $CourseCode - $CourseTitle",
        "",
        "## Status",
        "",
        "- Course code: $CourseCode",
        "- Course title: $CourseTitle",
        "- Workspace status: initialized",
        "",
        "## Folder Guide",
        "",
        "- 01_brief/: course brief, scope, learning outcomes",
        "- 02_source/: original source package and admin documents",
        "- 02_source/Delegate Workbook/: learner-facing source files",
        "- 02_source/Tutor Guide/: trainer-facing source files",
        "- 02_source/Certificate Sample/: certificate assets",
        "- 02_source/Version Control/: review history and change records",
        "- 03_authoring/: newly authored content",
        "- 04_translation/: localized assets and overrides",
        "- 05_review/: SME review and language review",
        "- 06_delivery/: final release files"
    ) -join "`r`n"
    Set-Content -LiteralPath $readmePath -Encoding UTF8 -Value $readmeContent
}

$sourceReadmePath = Join-Path $courseRoot "02_source\README.md"
if (-not (Test-Path -LiteralPath $sourceReadmePath)) {
    $sourceReadmeContent = @(
        "# Source Package Guide",
        "",
        "This folder stores the source course package using the standard BSI package structure.",
        "",
        "Recommended contents:",
        "",
        "- Build List_$CourseCode...",
        "- Important Course Info_$CourseCode... or Important Course Information_$CourseCode...",
        "- Delegate Workbook/",
        "- Tutor Guide/",
        "- Certificate Sample/",
        "- Version Control/"
    ) -join "`r`n"
    Set-Content -LiteralPath $sourceReadmePath -Encoding UTF8 -Value $sourceReadmeContent
}

$briefTemplate = Join-Path $workspaceRoot "authoring\templates\course-brief.md"
$outlineTemplate = Join-Path $workspaceRoot "authoring\templates\module-outline.md"
$sessionTemplate = Join-Path $workspaceRoot "authoring\templates\session-plan.md"
$activityTemplate = Join-Path $workspaceRoot "authoring\templates\activity-sheet.md"
$assessmentTemplate = Join-Path $workspaceRoot "authoring\templates\assessment-blueprint.md"

$templateCopies = @(
    @{ Source = $briefTemplate; Destination = Join-Path $courseRoot "01_brief\course-brief.md" },
    @{ Source = $outlineTemplate; Destination = Join-Path $courseRoot "03_authoring\module-outline.md" },
    @{ Source = $sessionTemplate; Destination = Join-Path $courseRoot "03_authoring\session-plan.md" },
    @{ Source = $activityTemplate; Destination = Join-Path $courseRoot "03_authoring\activity-sheet.md" },
    @{ Source = $assessmentTemplate; Destination = Join-Path $courseRoot "05_review\assessment-blueprint.md" }
)

foreach ($item in $templateCopies) {
    if ((Test-Path -LiteralPath $item.Source) -and -not (Test-Path -LiteralPath $item.Destination)) {
        Copy-Item -LiteralPath $item.Source -Destination $item.Destination
    }
}

Write-Output $courseRoot

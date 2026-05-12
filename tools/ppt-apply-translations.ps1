param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$TranslationsPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

function Get-ShapeByPath {
    param(
        [object]$Slide,
        [string]$Path
    )

    $shapePart = $Path.Split('|')[0]
    $isNotesPath = $shapePart.StartsWith('notes:')
    $normalizedShapePart = if ($isNotesPath) { $shapePart.Substring(6) } else { $shapePart }
    $shapeCollection = if ($isNotesPath) { $Slide.NotesPage.Shapes } else { $Slide.Shapes }

    $target = $shapeCollection | Where-Object { "$($_.Id)" -eq ($normalizedShapePart.Split('/')[0]) } | Select-Object -First 1
    if (-not $target) {
        throw "Shape path not found: $Path"
    }

    $ids = $normalizedShapePart.Split('/')
    $current = $target
    for ($i = 1; $i -lt $ids.Count; $i++) {
        $childId = $ids[$i]
        $next = $current.GroupItems | Where-Object { "$($_.Id)" -eq $childId } | Select-Object -First 1
        if (-not $next) {
            throw "Group shape path not found: $Path"
        }
        $current = $next
    }

    return $current
}

$resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
$resolvedTranslations = (Resolve-Path -LiteralPath $TranslationsPath).Path
Copy-Item -LiteralPath $resolvedInput -Destination $OutputPath -Force
$resolvedOutput = (Resolve-Path -LiteralPath $OutputPath).Path

$translationData = Get-Content -LiteralPath $resolvedTranslations -Raw -Encoding UTF8 | ConvertFrom-Json
$lookup = @{}
foreach ($entry in $translationData) {
    $lookup["$($entry.slide)|$($entry.path)"] = $entry.text
}

$pp = $null
$presentation = $null

try {
    $pp = New-Object -ComObject PowerPoint.Application
    $presentation = $pp.Presentations.Open($resolvedOutput, $false, $false, $false)

    foreach ($slide in $presentation.Slides) {
        foreach ($key in $lookup.Keys | Where-Object { $_ -like "$($slide.SlideNumber)|*" }) {
            $path = $key.Split('|', 2)[1]
            $translated = [string]$lookup[$key]
            $shape = Get-ShapeByPath -Slide $slide -Path $path

            if ($path -like '*|cell:*') {
                $cellPart = $path.Split('|')[1].Replace('cell:', '')
                $row, $col = $cellPart.Split(',')
                $shape.Table.Cell([int]$row, [int]$col).Shape.TextFrame.TextRange.Text = $translated
                continue
            }

            if ($shape.HasTextFrame -eq -1) {
                $shape.TextFrame.TextRange.Text = $translated
            }
        }
    }

    $presentation.Save()
}
finally {
    if ($presentation) { $presentation.Close() }
    if ($pp) { $pp.Quit() }
}

param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [string]$OutputPath
)

$ErrorActionPreference = 'Stop'

function Get-ShapeEntries {
    param(
        [object]$Shape,
        [int]$SlideNumber,
        [string]$PathPrefix,
        [string]$PathRoot = ''
    )

    $entries = New-Object System.Collections.Generic.List[object]
    $shapePath = if ([string]::IsNullOrEmpty($PathPrefix)) { "$($Shape.Id)" } else { "$PathPrefix/$($Shape.Id)" }
    $entryPath = if ([string]::IsNullOrEmpty($PathRoot)) { $shapePath } else { "$PathRoot`:$shapePath" }

    if ($Shape.Type -eq 6) {
        foreach ($child in $Shape.GroupItems) {
            foreach ($entry in Get-ShapeEntries -Shape $child -SlideNumber $SlideNumber -PathPrefix $shapePath -PathRoot $PathRoot) {
                [void]$entries.Add($entry)
            }
        }
        return $entries
    }

    if ($Shape.HasTable -eq -1) {
        $table = $Shape.Table
        for ($row = 1; $row -le $table.Rows.Count; $row++) {
            for ($col = 1; $col -le $table.Columns.Count; $col++) {
                $cellShape = $table.Cell($row, $col).Shape
                if ($cellShape.HasTextFrame -eq -1 -and $cellShape.TextFrame.HasText -eq -1) {
                    [void]$entries.Add([pscustomobject]@{
                        slide = $SlideNumber
                        path = "$entryPath|cell:$row,$col"
                        kind = 'table_cell'
                        shapeName = $Shape.Name
                        text = $cellShape.TextFrame.TextRange.Text
                    })
                }
            }
        }
        return $entries
    }

    if ($Shape.HasTextFrame -eq -1 -and $Shape.TextFrame.HasText -eq -1) {
        [void]$entries.Add([pscustomobject]@{
            slide = $SlideNumber
            path = $entryPath
            kind = 'text'
            shapeName = $Shape.Name
            text = $Shape.TextFrame.TextRange.Text
        })
    }

    return $entries
}

$resolvedInput = (Resolve-Path -LiteralPath $InputPath).Path
$resolvedOutput = if ($OutputPath) {
    $OutputPath
} else {
    Join-Path -Path (Split-Path -Parent $resolvedInput) -ChildPath ("{0}.json" -f [IO.Path]::GetFileNameWithoutExtension($resolvedInput))
}

$pp = $null
$presentation = $null

try {
    $pp = New-Object -ComObject PowerPoint.Application
    $presentation = $pp.Presentations.Open($resolvedInput, $false, $true, $false)

    $slides = New-Object System.Collections.Generic.List[object]
    foreach ($slide in $presentation.Slides) {
        $slideEntries = New-Object System.Collections.Generic.List[object]
        foreach ($shape in $slide.Shapes) {
            foreach ($entry in Get-ShapeEntries -Shape $shape -SlideNumber $slide.SlideNumber -PathPrefix '' -PathRoot '') {
                [void]$slideEntries.Add($entry)
            }
        }

        foreach ($shape in $slide.NotesPage.Shapes) {
            foreach ($entry in Get-ShapeEntries -Shape $shape -SlideNumber $slide.SlideNumber -PathPrefix '' -PathRoot 'notes') {
                [void]$slideEntries.Add($entry)
            }
        }

        [void]$slides.Add([pscustomobject]@{
            slide = $slide.SlideNumber
            entries = $slideEntries
        })
    }

    $payload = [pscustomobject]@{
        source = $resolvedInput
        slideCount = $presentation.Slides.Count
        slides = $slides
    }

    $json = $payload | ConvertTo-Json -Depth 8
    $outputDir = Split-Path -Parent $resolvedOutput
    if ($outputDir -and -not (Test-Path -LiteralPath $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir | Out-Null
    }
    [IO.File]::WriteAllText($resolvedOutput, $json, [Text.UTF8Encoding]::new($false))
}
finally {
    if ($presentation) { $presentation.Close() }
    if ($pp) { $pp.Quit() }
}

param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [string]$ConfigPath,

    [string]$CachePath,

    [string]$WorkDir,

    [string]$PythonExe = "python"
)

$ErrorActionPreference = 'Stop'

function Split-WordText {
    param(
        [string]$Text
    )

    $match = [regex]::Match($Text, '[\x07\x0b\x0c\r\n]+$')
    if ($match.Success) {
        return [pscustomobject]@{
            Body   = $Text.Substring(0, $Text.Length - $match.Length)
            Suffix = $match.Value
        }
    }

    return [pscustomobject]@{
        Body   = $Text
        Suffix = ''
    }
}

function Normalize-Compare {
    param(
        [string]$Text
    )

    if ($null -eq $Text) {
        return ''
    }

    return (($Text -replace '\s+', ' ').Trim())
}

function Get-StoryParagraphEntries {
    param(
        [object]$Document
    )

    $entries = New-Object System.Collections.Generic.List[object]
    $seen = @{}
    $storyOrdinal = 0

    foreach ($rootRange in $Document.StoryRanges) {
        $range = $rootRange

        while ($null -ne $range) {
            $rangeKey = "$($range.StoryType)|$($range.Start)|$($range.End)"
            if ($seen.ContainsKey($rangeKey)) {
                break
            }
            $seen[$rangeKey] = $true
            $storyOrdinal++

            $paragraphOrdinal = 0
            foreach ($paragraph in $range.Paragraphs) {
                $paragraphOrdinal++
                $split = Split-WordText -Text ([string]$paragraph.Range.Text)
                if ([string]::IsNullOrWhiteSpace($split.Body)) {
                    continue
                }

                [void]$entries.Add([pscustomobject]@{
                    slide = 1
                    path  = "story:$storyOrdinal|paragraph:$paragraphOrdinal"
                    text  = $split.Body
                })
            }

            try {
                $range = $range.NextStoryRange
            }
            catch {
                $range = $null
            }
        }
    }

    return $entries
}

function Get-ShapeEntriesFromShape {
    param(
        [object]$Shape,
        [string]$Path
    )

    $entries = New-Object System.Collections.Generic.List[object]

    if ($Shape.Type -eq 6) {
        for ($childIndex = 1; $childIndex -le $Shape.GroupItems.Count; $childIndex++) {
            $child = $Shape.GroupItems.Item($childIndex)
            foreach ($entry in Get-ShapeEntriesFromShape -Shape $child -Path "$Path/$childIndex") {
                [void]$entries.Add($entry)
            }
        }
        return $entries
    }

    try {
        if ($Shape.TextFrame.HasText -eq -1) {
            $text = [string]$Shape.TextFrame.TextRange.Text
            if (-not [string]::IsNullOrWhiteSpace($text)) {
                [void]$entries.Add([pscustomobject]@{
                    slide = 1
                    path  = $Path
                    text  = $text
                })
            }
        }
    }
    catch {
    }

    return $entries
}

function Get-DocumentShapeEntries {
    param(
        [object]$Document
    )

    $entries = New-Object System.Collections.Generic.List[object]
    for ($shapeIndex = 1; $shapeIndex -le $Document.Shapes.Count; $shapeIndex++) {
        $shape = $Document.Shapes.Item($shapeIndex)
        foreach ($entry in Get-ShapeEntriesFromShape -Shape $shape -Path "shape:$shapeIndex") {
            [void]$entries.Add($entry)
        }
    }

    return $entries
}

function Resolve-ShapeByPath {
    param(
        [object]$Document,
        [string]$Path
    )

    $segments = $Path.Substring(6).Split('/')
    $current = $Document.Shapes.Item([int]$segments[0])
    if ($null -eq $current) {
        return $null
    }

    for ($index = 1; $index -lt $segments.Count; $index++) {
        if ($null -eq $current -or $current.Type -ne 6) {
            return $null
        }
        $current = $current.GroupItems.Item([int]$segments[$index])
        if ($null -eq $current) {
            return $null
        }
    }

    return $current
}

function Apply-TranslationsToDocument {
    param(
        [object]$Document,
        [hashtable]$Lookup
    )

    $seen = @{}
    $storyOrdinal = 0
    $updated = 0

    foreach ($rootRange in $Document.StoryRanges) {
        $range = $rootRange

        while ($null -ne $range) {
            $rangeKey = "$($range.StoryType)|$($range.Start)|$($range.End)"
            if ($seen.ContainsKey($rangeKey)) {
                break
            }
            $seen[$rangeKey] = $true
            $storyOrdinal++

            $paragraphOrdinal = 0
            foreach ($paragraph in $range.Paragraphs) {
                $paragraphOrdinal++
                $split = Split-WordText -Text ([string]$paragraph.Range.Text)
                if ([string]::IsNullOrWhiteSpace($split.Body)) {
                    continue
                }

                $lookupKey = "1|story:$storyOrdinal|paragraph:$paragraphOrdinal"
                if (-not $Lookup.ContainsKey($lookupKey)) {
                    continue
                }

                $translated = [string]$Lookup[$lookupKey]
                if ((Normalize-Compare -Text $translated) -eq (Normalize-Compare -Text $split.Body)) {
                    continue
                }

                $paragraph.Range.Text = $translated + $split.Suffix
                $updated++
            }

            try {
                $range = $range.NextStoryRange
            }
            catch {
                $range = $null
            }
        }
    }

    return $updated
}

function Apply-TranslationsToShapes {
    param(
        [object]$Document,
        [hashtable]$Lookup
    )

    $updated = 0

    foreach ($lookupKey in $Lookup.Keys | Where-Object { $_ -like '1|shape:*' }) {
        try {
            $path = $lookupKey.Split('|', 2)[1]
            $shape = Resolve-ShapeByPath -Document $Document -Path $path
            if ($null -eq $shape) {
                continue
            }

            $translated = [string]$Lookup[$lookupKey]
            if ($Shape.TextFrame.HasText -eq -1) {
                $currentText = [string]$Shape.TextFrame.TextRange.Text
                if ((Normalize-Compare -Text $translated) -ne (Normalize-Compare -Text $currentText)) {
                    $Shape.TextFrame.TextRange.Text = $translated
                    $updated++
                }
            }
        }
        catch {
        }
    }

    return $updated
}

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
$stem = [IO.Path]::GetFileNameWithoutExtension($resolvedInput)
$sourceJson = Join-Path $WorkDir ("{0}.docx.source.json" -f $stem)
$updatesJson = Join-Path $WorkDir ("{0}.docx.translations.json" -f $stem)

$word = $null
$sourceDocument = $null
$outputDocument = $null

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $sourceDocument = $word.Documents.Open($resolvedInput, $false, $true)
    $entries = New-Object System.Collections.Generic.List[object]
    foreach ($entry in Get-StoryParagraphEntries -Document $sourceDocument) {
        [void]$entries.Add($entry)
    }
    foreach ($entry in Get-DocumentShapeEntries -Document $sourceDocument) {
        [void]$entries.Add($entry)
    }
    $payload = [pscustomobject]@{
        source = $resolvedInput
        slideCount = 1
        slides = @(
            [pscustomobject]@{
                slide = 1
                entries = $entries
            }
        )
    }
    [IO.File]::WriteAllText($sourceJson, ($payload | ConvertTo-Json -Depth 8), [Text.UTF8Encoding]::new($false))
    $sourceDocument.Close($false)
    $sourceDocument = $null

    $pythonArgs = @(
        (Join-Path $PSScriptRoot "build-ppt-translation-json.py"),
        "--source-json", $sourceJson,
        "--config", $resolvedConfig,
        "--cache", $CachePath,
        "--output", $updatesJson
    )
    & $PythonExe @pythonArgs

    Copy-Item -LiteralPath $resolvedInput -Destination $OutputPath -Force
    $resolvedOutput = (Resolve-Path -LiteralPath $OutputPath).Path

    $translationData = Get-Content -LiteralPath $updatesJson -Raw -Encoding UTF8 | ConvertFrom-Json
    $lookup = @{}
    foreach ($entry in $translationData) {
        $lookup["$($entry.slide)|$($entry.path)"] = $entry.text
    }

    $outputDocument = $word.Documents.Open($resolvedOutput, $false, $false)
    $updated = Apply-TranslationsToDocument -Document $outputDocument -Lookup $lookup
    $updated += Apply-TranslationsToShapes -Document $outputDocument -Lookup $lookup
    $outputDocument.Save()
    Write-Output ("Translated DOCX saved to: {0}" -f $resolvedOutput)
    Write-Output ("Updated paragraphs: {0}" -f $updated)
}
finally {
    if ($sourceDocument) { $sourceDocument.Close($false) }
    if ($outputDocument) { $outputDocument.Close($false) }
    if ($word) { $word.Quit() }
}

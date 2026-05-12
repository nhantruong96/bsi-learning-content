param(
    [Parameter(Mandatory = $true)]
    [string]$SourceJson,

    [Parameter(Mandatory = $true)]
    [string]$ProposalJson,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Normalize-CellText {
    param([AllowNull()][string]$Text)

    if ($null -eq $Text) {
        return ""
    }

    return ($Text -replace "`r`n?", "`n")
}

function Get-EntryKey {
    param(
        [int]$Slide,
        [string]$Path
    )

    return "$Slide|$Path"
}

function Get-ReviewBucket {
    param([string]$EnglishText)

    $trimmed = $EnglishText.Trim()
    $lineCount = ($trimmed -split "\n").Count

    if ([string]::IsNullOrWhiteSpace($trimmed)) {
        return "keep"
    }

    if ($trimmed -match '^[0-9]+$') {
        return "keep"
    }

    if ($trimmed -notmatch '[A-Za-z]') {
        return "keep"
    }

    if ($trimmed -eq "© 2025 BSI. All rights reserved.") {
        return "keep"
    }

    if ($trimmed -match '^[A-Z0-9]+ v[0-9]+(?:\.[0-9]+)? [A-Za-z]{3,9} [0-9]{4}$') {
        return "keep"
    }

    if ($trimmed -cmatch '^[A-Z0-9© ._\-/:()]+$' -and $trimmed.Length -lt 40) {
        return "keep"
    }

    if ($trimmed.Length -gt 140 -or $lineCount -ge 5) {
        return "long"
    }

    return "term"
}

function Add-UniqueValue {
    param(
        [System.Collections.ArrayList]$List,
        [AllowNull()]$Value
    )

    if ($null -eq $Value) {
        return
    }

    if (-not $List.Contains($Value)) {
        [void]$List.Add($Value)
    }
}

function Add-HeaderRow {
    param(
        $Sheet,
        [string[]]$Headers
    )

    for ($column = 0; $column -lt $Headers.Count; $column++) {
        $Sheet.Cells.Item(1, $column + 1) = $Headers[$column]
    }

    $headerRange = $Sheet.Range("A1", "M1")
    $headerRange.Font.Bold = $true
    $headerRange.WrapText = $true
    $headerRange.Interior.ColorIndex = 15
}

function Apply-SheetFormatting {
    param(
        $Sheet,
        [int]$LastRow
    )

    $Sheet.Rows.Item("1:1").RowHeight = 30
    $Sheet.Columns.Item("A").ColumnWidth = 12
    $Sheet.Columns.Item("B").ColumnWidth = 18
    $Sheet.Columns.Item("C").ColumnWidth = 16
    $Sheet.Columns.Item("D").ColumnWidth = 14
    $Sheet.Columns.Item("E").ColumnWidth = 12
    $Sheet.Columns.Item("F").ColumnWidth = 18
    $Sheet.Columns.Item("G").ColumnWidth = 16
    $Sheet.Columns.Item("H").ColumnWidth = 20
    $Sheet.Columns.Item("I").ColumnWidth = 50
    $Sheet.Columns.Item("J").ColumnWidth = 50
    $Sheet.Columns.Item("K").ColumnWidth = 14
    $Sheet.Columns.Item("L").ColumnWidth = 28
    $Sheet.Columns.Item("M").ColumnWidth = 24

    $Sheet.Columns.Item("F:M").WrapText = $true
    $Sheet.Columns.Item("A:M").VerticalAlignment = -4160
    $Sheet.Columns.Item("A:M").EntireRow.AutoFit() | Out-Null

    if ($LastRow -ge 2) {
        $filterRange = $Sheet.Range("A1", "M$LastRow")
        $filterRange.AutoFilter() | Out-Null

        $approvalRange = $Sheet.Range("K2", "K$LastRow")
        $approvalRange.Validation.Delete()
        $approvalRange.Validation.Add(3, 1, 1, "Duyệt,Sửa,Giữ EN,Bỏ")

        $flagRange = $Sheet.Range("M2", "M$LastRow")
        $flagRange.FormatConditions.Delete() | Out-Null
    }

    $Sheet.Activate() | Out-Null
    $Sheet.Application.ActiveWindow.SplitRow = 1
    $Sheet.Application.ActiveWindow.FreezePanes = $true
}

function Write-ReviewSheet {
    param(
        $Sheet,
        [System.Collections.IEnumerable]$Rows
    )

    $headers = @(
        "ID",
        "Nhóm",
        "Hành động đề xuất",
        "Số lần xuất hiện",
        "Slide đầu tiên",
        "Các slide",
        "Vị trí mẫu",
        "Shape mẫu",
        "English",
        "Tiếng Việt đề xuất",
        "Phê duyệt",
        "Ghi chú",
        "Cờ kiểm tra"
    )

    Add-HeaderRow -Sheet $Sheet -Headers $headers

    $rowIndex = 2
    foreach ($row in $Rows) {
        $Sheet.Cells.Item($rowIndex, 1) = $row.ID
        $Sheet.Cells.Item($rowIndex, 2) = $row.Group
        $Sheet.Cells.Item($rowIndex, 3) = $row.ProposedAction
        $Sheet.Cells.Item($rowIndex, 4) = $row.Occurrences
        $Sheet.Cells.Item($rowIndex, 5) = $row.FirstSlide
        $Sheet.Cells.Item($rowIndex, 6) = $row.Slides
        $Sheet.Cells.Item($rowIndex, 7) = $row.SamplePath
        $Sheet.Cells.Item($rowIndex, 8) = $row.ShapeName
        $Sheet.Cells.Item($rowIndex, 9) = $row.English
        $Sheet.Cells.Item($rowIndex, 10) = $row.VietnameseProposal
        $Sheet.Cells.Item($rowIndex, 11) = ""
        $Sheet.Cells.Item($rowIndex, 12) = ""
        $Sheet.Cells.Item($rowIndex, 13) = $row.ReviewFlag
        $rowIndex++
    }

    Apply-SheetFormatting -Sheet $Sheet -LastRow ($rowIndex - 1)
}

function Build-RecordList {
    param(
        [System.Collections.IEnumerable]$SourceSlides,
        [hashtable]$ProposalMap
    )

    $records = [ordered]@{}

    foreach ($slideBlock in $SourceSlides) {
        foreach ($entry in $slideBlock.entries) {
            $english = Normalize-CellText -Text $entry.text
            $entryKey = Get-EntryKey -Slide ([int]$entry.slide) -Path ([string]$entry.path)
            $proposal = ""

            if ($ProposalMap.ContainsKey($entryKey)) {
                $proposal = $ProposalMap[$entryKey]
            }

            if (-not $records.Contains($english)) {
                $records[$english] = [pscustomobject]@{
                    English         = $english
                    Occurrences     = 0
                    FirstSlide      = [int]$entry.slide
                    SamplePath      = [string]$entry.path
                    ShapeName       = [string]$entry.shapeName
                    SlideValues     = [System.Collections.ArrayList]::new()
                    ProposalValues  = [System.Collections.ArrayList]::new()
                }
            }

            $record = $records[$english]
            $record.Occurrences++
            Add-UniqueValue -List $record.SlideValues -Value ([int]$entry.slide)
            Add-UniqueValue -List $record.ProposalValues -Value $proposal
        }
    }

    return $records.Values
}

function Convert-ToReviewRows {
    param([System.Collections.IEnumerable]$RawRecords)

    $rows = foreach ($record in $RawRecords) {
        $bucket = Get-ReviewBucket -EnglishText $record.English
        $proposalText = [string]::Join(" || ", @($record.ProposalValues))
        $reviewFlagValues = [System.Collections.ArrayList]::new()

        if ($record.ProposalValues.Count -gt 1) {
            [void]$reviewFlagValues.Add("Có nhiều đề xuất VN theo ngữ cảnh")
        }

        if ($bucket -ne "keep" -and $proposalText -eq $record.English) {
            [void]$reviewFlagValues.Add("Đề xuất hiện vẫn giữ nguyên EN")
        }

        $group = switch ($bucket) {
            "term" { "Thuật ngữ / cụm ngắn" }
            "long" { "Đoạn dài / notes" }
            default { "Giữ nguyên / mã / số" }
        }

        $proposedAction = if ($bucket -eq "keep") { "Giữ nguyên" } else { "Dịch" }

        [pscustomobject]@{
            Bucket            = $bucket
            FirstSlide        = $record.FirstSlide
            SamplePath        = $record.SamplePath
            ShapeName         = $record.ShapeName
            Occurrences       = $record.Occurrences
            Slides            = [string]::Join(", ", @($record.SlideValues | Sort-Object))
            English           = $record.English
            VietnameseProposal = $proposalText
            Group             = $group
            ProposedAction    = $proposedAction
            ReviewFlag        = [string]::Join(" | ", $reviewFlagValues)
        }
    }

    $index = 1
    foreach ($row in ($rows | Sort-Object FirstSlide, SamplePath, English)) {
        $row | Add-Member -NotePropertyName ID -NotePropertyValue ("P5-{0:D4}" -f $index)
        $index++
    }

    return $rows | Sort-Object FirstSlide, SamplePath, English
}

$resolvedSourceJson = (Resolve-Path -LiteralPath $SourceJson).Path
$resolvedProposalJson = (Resolve-Path -LiteralPath $ProposalJson).Path
$resolvedOutputPath = [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutputPath))

$outputDirectory = Split-Path -Parent $resolvedOutputPath
if (-not (Test-Path -LiteralPath $outputDirectory)) {
    New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
}

$sourceDeck = Get-Content -Raw -LiteralPath $resolvedSourceJson | ConvertFrom-Json
$proposalData = Get-Content -Raw -LiteralPath $resolvedProposalJson | ConvertFrom-Json

if ($proposalData -is [System.Array]) {
    $proposalEntries = $proposalData
}
elseif ($proposalData.PSObject.Properties.Name -contains "slides") {
    $proposalEntries = foreach ($slide in $proposalData.slides) {
        foreach ($entry in $slide.entries) {
            $entry
        }
    }
}
else {
    throw "Unsupported proposal JSON shape: $resolvedProposalJson"
}

$proposalMap = @{}
foreach ($entry in $proposalEntries) {
    $proposalMap[(Get-EntryKey -Slide ([int]$entry.slide) -Path ([string]$entry.path))] = (Normalize-CellText -Text $entry.text)
}

$rawRecords = Build-RecordList -SourceSlides $sourceDeck.slides -ProposalMap $proposalMap
$reviewRows = Convert-ToReviewRows -RawRecords $rawRecords

$termRows = $reviewRows | Where-Object { $_.Bucket -eq "term" }
$longRows = $reviewRows | Where-Object { $_.Bucket -eq "long" }
$keepRows = $reviewRows | Where-Object { $_.Bucket -eq "keep" }

$excel = $null
$workbook = $null
$summarySheet = $null
$termsSheet = $null
$longSheet = $null
$keepSheet = $null

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    $workbook = $excel.Workbooks.Add()

    while ($workbook.Worksheets.Count -lt 4) {
        [void]$workbook.Worksheets.Add()
    }

    while ($workbook.Worksheets.Count -gt 4) {
        $workbook.Worksheets.Item($workbook.Worksheets.Count).Delete()
    }

    $summarySheet = $workbook.Worksheets.Item(1)
    $termsSheet = $workbook.Worksheets.Item(2)
    $longSheet = $workbook.Worksheets.Item(3)
    $keepSheet = $workbook.Worksheets.Item(4)

    $summarySheet.Name = "Summary"
    $termsSheet.Name = "Terms_Phrases"
    $longSheet.Name = "Long_Texts"
    $keepSheet.Name = "Keep_Unchanged"

    $summarySheet.Cells.Item(1, 1) = "Part 5 vocabulary review workbook"
    $summarySheet.Cells.Item(1, 1).Font.Bold = $true
    $summarySheet.Cells.Item(3, 1) = "Source JSON"
    $summarySheet.Cells.Item(3, 2) = $resolvedSourceJson
    $summarySheet.Cells.Item(4, 1) = "Proposal JSON"
    $summarySheet.Cells.Item(4, 2) = $resolvedProposalJson
    $summarySheet.Cells.Item(5, 1) = "Generated"
    $summarySheet.Cells.Item(5, 2) = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $summarySheet.Cells.Item(7, 1) = "Unique text items"
    $summarySheet.Cells.Item(7, 2) = $reviewRows.Count
    $summarySheet.Cells.Item(8, 1) = "Terms / phrases to review"
    $summarySheet.Cells.Item(8, 2) = $termRows.Count
    $summarySheet.Cells.Item(9, 1) = "Long texts to review"
    $summarySheet.Cells.Item(9, 2) = $longRows.Count
    $summarySheet.Cells.Item(10, 1) = "Keep unchanged"
    $summarySheet.Cells.Item(10, 2) = $keepRows.Count
    $summarySheet.Cells.Item(12, 1) = "How to review"
    $summarySheet.Cells.Item(13, 1) = "1. Review sheet Terms_Phrases first, then Long_Texts."
    $summarySheet.Cells.Item(14, 1) = "2. If the proposal is acceptable, set 'Phê duyệt' = 'Duyệt'."
    $summarySheet.Cells.Item(15, 1) = "3. If you want to change wording, edit 'Tiếng Việt đề xuất' and set 'Phê duyệt' = 'Sửa'."
    $summarySheet.Cells.Item(16, 1) = "4. Use 'Ghi chú' to record style, context, or keep-English rules."
    $summarySheet.Columns.Item("A").ColumnWidth = 38
    $summarySheet.Columns.Item("B").ColumnWidth = 100
    $summarySheet.Columns.Item("A:B").WrapText = $true
    $summarySheet.Columns.Item("A:B").EntireRow.AutoFit() | Out-Null

    Write-ReviewSheet -Sheet $termsSheet -Rows $termRows
    Write-ReviewSheet -Sheet $longSheet -Rows $longRows
    Write-ReviewSheet -Sheet $keepSheet -Rows $keepRows

    $workbook.SaveAs($resolvedOutputPath, 51)
}
finally {
    if ($workbook) {
        $workbook.Close($true)
    }

    if ($excel) {
        $excel.Quit()
    }

    foreach ($comObject in @($keepSheet, $longSheet, $termsSheet, $summarySheet, $workbook, $excel)) {
        if ($null -ne $comObject) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($comObject)
        }
    }

    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

Write-Output "Workbook created: $resolvedOutputPath"

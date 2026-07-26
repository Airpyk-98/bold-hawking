$word = New-Object -ComObject Word.Application
$word.Visible = $false
$htmlPath = Resolve-Path "index_corrected.html"
$doc = $word.Documents.Open($htmlPath.Path)
$docxPath = [string](Join-Path (Get-Location).Path "Corrected_Pilot_Fixed_Updated.docx")
$doc.SaveAs([ref]$docxPath, [ref]16) # 16 = wdFormatDocumentDefault (.docx)
$doc.Close()
$word.Quit()
Write-Host "Converted to Original_Reference.docx successfully."

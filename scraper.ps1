$baseUrl = "https://indigenousmedicinescayoosecreek.pressbooks.tru.ca/"
Write-Host "Fetching main page..."
$mainPage = Invoke-WebRequest -Uri $baseUrl -UseBasicParsing
$html = $mainPage.Content

$pattern = '(?s)<p class="toc__title">\s*<a href="([^"]+)">'
$matches = [regex]::Matches($html, $pattern)

$links = @()
foreach ($m in $matches) {
    $links += $m.Groups[1].Value
}

$links = $links | Select-Object -Unique

Write-Host "Found $($links.Length) unique links."

$finalHtml = @"
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</title>
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 20px; color: #333; }
  img { max-width: 100%; height: auto; display: block; margin: 20px auto; }
  .stitched-page { margin-bottom: 60px; padding-bottom: 40px; border-bottom: 2px solid #ccc; }
  h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 0.5em; }
  h1.chapter-title { border-bottom: 1px solid #eee; padding-bottom: 10px; }
  h2 { color: #34495e; }
  .wp-caption { background: #f9f9f9; padding: 10px; border: 1px solid #ddd; text-align: center; margin-bottom: 20px; max-width: 100%; }
  .wp-caption-text { font-style: italic; color: #666; margin: 5px 0 0 0; }
  .chapter-nav { display: none !important; }
</style>
</head>
<body>
<div style="text-align:center; padding: 40px 0; border-bottom: 4px solid #2c3e50; margin-bottom: 40px;">
  <h1>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</h1>
  <p><em>Complete word-for-word single page compilation</em></p>
</div>
"@

$count = 1
foreach ($link in $links) {
    Write-Host "Fetching [$count/$($links.Length)]: $link"
    try {
        $page = Invoke-WebRequest -Uri $link -UseBasicParsing
        $pageHtml = $page.Content
        
        if ($pageHtml -match '(?si)<main id="main"[^>]*>(.*?)</main>') {
            $mainContent = $matches[1]
            $finalHtml += "`n<div class=`"stitched-page`">`n$mainContent`n</div>`n"
        } else {
            Write-Host "No main content found for $link"
        }
    } catch {
        Write-Host "Error fetching $link : $_"
    }
    $count++
}

$finalHtml += "`n</body>`n</html>"

Set-Content -Path "index.html" -Value $finalHtml -Encoding UTF8
Write-Host "Done! File saved to index.html"

$content = Get-Content 'index.html' -Raw
$matches = [regex]::Matches($content, '(?si)<div class="stitched-page">(.*?)</div>')

for ($i=0; $i -lt 3; $i++) {
    $m = $matches[$i].Groups[1].Value
    if ($m -match '(?si)<h1[^>]*>(.*?)</h1>') {
        $title = $matches[1] -replace '<[^>]+>', ''
        Write-Host "Chapter $i: $title"
    }
}

$html = Get-Content -Raw index.html

# 1. Elders citation
$html = $html.Replace("Elders and Community members of the Cayoose Creek Band of Sekw’el’was", "(Elders of Cayoose Creek Band, traditional knowledge, 2025)")

# 2. WNPS n.d.
$html = $html.Replace("Washington Native Plant Society. (n.d.).", "Washington Native Plant Society. (n.d.). Retrieved from ")

# 3. Kuhnlein 1989 in-text
$html = $html.Replace("and 3.33 milligrams ascorbic acid</p>", "and 3.33 milligrams ascorbic acid (Kuhnlein, 1989)</p>")

# 4. Nabavi et al 2015 in-text
$html = $html.Replace("↑ Cardiac contractility</p>", "↑ Cardiac contractility (Nabavi et al., 2015)</p>")

# 5. Dahmer and Scott URL
$html = $html.Replace("American Family Physician, 81</em>(4), 465–468.</li>", "American Family Physician, 81</em>(4), 465–468. Retrieved from https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html</li>")

# 6. Journal italics (Black Gooseberry)
$html = $html.Replace("Journal of Ethnopharmacology, 276", "<em>Journal of Ethnopharmacology</em>, <em>276</em>")
$html = $html.Replace("Journal of Agricultural and Food Chemistry, 50", "<em>Journal of Agricultural and Food Chemistry</em>, <em>50</em>")
$html = $html.Replace("Foods, 10", "<em>Foods</em>, <em>10</em>")
$html = $html.Replace("International Journal of Molecular Sciences, 20", "<em>International Journal of Molecular Sciences</em>, <em>20</em>")
$html = $html.Replace("Nutrition and Cancer, 54", "<em>Nutrition and Cancer</em>, <em>54</em>")
$html = $html.Replace("Journal of Food Composition and Analysis, 2", "<em>Journal of Food Composition and Analysis</em>, <em>2</em>")

Set-Content -Path index.html -Value $html -Encoding UTF8
Write-Host "Replacements completed on index.html"

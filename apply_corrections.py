import io

filepath = 'vercel_deploy/index.html'

with io.open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Elders citation
content = content.replace('Elders and Community members of the Cayoose Creek Band of Sekw’el’was', '(Elders of Cayoose Creek Band, traditional knowledge, 2025)')

# 2. WNPS n.d.
content = content.replace('Washington Native Plant Society. (n.d.).', 'Washington Native Plant Society. (n.d.). Retrieved from ')

# 3. Kuhnlein 1989 in-text
content = content.replace('and 3.33 milligrams ascorbic acid</p>', 'and 3.33 milligrams ascorbic acid (Kuhnlein, 1989)</p>')

# 4. Nabavi et al 2015 in-text
content = content.replace('↑ Cardiac contractility</p>', '↑ Cardiac contractility (Nabavi et al., 2015)</p>')

# 5. Dahmer and Scott URL (handling possible HTML entities or en-dashes)
content = content.replace('American Family Physician, 81</em>(4), 465–468.</li>', 'American Family Physician, 81</em>(4), 465–468. Retrieved from https://www.aafp.org/pubs/afp/issues/2010/0215/p465.html</li>')

# 6. Journal italics (Black Gooseberry)
content = content.replace('Journal of Ethnopharmacology, 276', '<em>Journal of Ethnopharmacology</em>, <em>276</em>')
content = content.replace('Journal of Agricultural and Food Chemistry, 50', '<em>Journal of Agricultural and Food Chemistry</em>, <em>50</em>')
content = content.replace('Foods, 10', '<em>Foods</em>, <em>10</em>')
content = content.replace('International Journal of Molecular Sciences, 20', '<em>International Journal of Molecular Sciences</em>, <em>20</em>')
content = content.replace('Nutrition and Cancer, 54', '<em>Nutrition and Cancer</em>, <em>54</em>')
content = content.replace('Journal of Food Composition and Analysis, 2', '<em>Journal of Food Composition and Analysis</em>, <em>2</em>')

with io.open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Corrections applied successfully.")

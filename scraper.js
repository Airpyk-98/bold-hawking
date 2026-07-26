const cheerio = require('cheerio');
const fs = require('fs');

const BASE_URL = 'https://indigenousmedicinescayoosecreek.pressbooks.tru.ca/';

const headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'en-US,en;q=0.5'
};

async function fetchHtml(url) {
  const response = await fetch(url, { headers });
  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status}`);
  }
  return await response.text();
}

async function scrape() {
  try {
    console.log('Fetching main page...');
    const mainHtml = await fetchHtml(BASE_URL);
    let $ = cheerio.load(mainHtml);
    
    const links = [];
    $('.toc__title a').each((i, el) => {
      const href = $(el).attr('href');
      if (href && href.startsWith(BASE_URL)) {
        links.push(href);
      }
    });
    
    const uniqueLinks = [...new Set(links)];
    console.log(`Found ${uniqueLinks.length} unique links in TOC.`);

    let finalHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</title>
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    color: #333;
  }
  img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
  }
  .stitched-page {
    margin-bottom: 60px;
    padding-bottom: 40px;
    border-bottom: 2px solid #ccc;
  }
  h1 { color: #2c3e50; font-size: 2.5em; margin-bottom: 0.5em; }
  h1.chapter-title { border-bottom: 1px solid #eee; padding-bottom: 10px; }
  h2 { color: #34495e; }
  .wp-caption {
    background: #f9f9f9;
    padding: 10px;
    border: 1px solid #ddd;
    text-align: center;
    margin-bottom: 20px;
    max-width: 100%;
  }
  .wp-caption-text {
    font-style: italic;
    color: #666;
    margin: 5px 0 0 0;
  }
  .chapter-nav { display: none !important; }
</style>
</head>
<body>
<div style="text-align:center; padding: 40px 0; border-bottom: 4px solid #2c3e50; margin-bottom: 40px;">
  <h1>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</h1>
  <p><em>Complete word-for-word single page compilation</em></p>
</div>
`;

    for (let i = 0; i < uniqueLinks.length; i++) {
      const link = uniqueLinks[i];
      console.log(`Fetching [${i + 1}/${uniqueLinks.length}]: ${link}`);
      try {
        const html = await fetchHtml(link);
        const $page = cheerio.load(html);
        
        let mainContent = $page('main#main').html();
        
        if (mainContent) {
           finalHtml += `\n<div class="stitched-page">\n${mainContent}\n</div>\n`;
        } else {
           console.log('No main content found for', link);
        }
      } catch (err) {
        console.error(`Error fetching ${link}:`, err.message);
      }
      
      await new Promise(r => setTimeout(r, 200));
    }
    
    finalHtml += `\n</body>\n</html>`;

    console.log('Writing to index.html...');
    fs.writeFileSync('index.html', finalHtml);
    console.log('Done! File saved to index.html');
  } catch (error) {
    console.error('An error occurred:', error);
  }
}

scrape();

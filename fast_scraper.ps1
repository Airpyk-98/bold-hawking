$source = @"
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;

public class Scraper {
    public static async Task Run() {
        var handler = new HttpClientHandler() { UseProxy = true };
        var client = new HttpClient(handler);
        client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");
        
        string baseUrl = "https://indigenousmedicinescayoosecreek.pressbooks.tru.ca/";
        Console.WriteLine("Fetching main page...");
        string mainHtml = await client.GetStringAsync(baseUrl);
        
        var pattern = @"<p class=""toc__title"">\s*<a href=""([^""]+)""";
        var matches = Regex.Matches(mainHtml, pattern, RegexOptions.Singleline);
        
        var links = new HashSet<string>();
        var orderedLinks = new List<string>();
        foreach (Match m in matches) {
            string link = m.Groups[1].Value;
            if (links.Add(link)) {
                orderedLinks.Add(link);
            }
        }
        
        Console.WriteLine(string.Format("Found {0} unique links.", orderedLinks.Count));
        
        var results = new ConcurrentDictionary<string, string>();
        
        var tasks = orderedLinks.Select(async link => {
            try {
                string html = await client.GetStringAsync(link);
                var m = Regex.Match(html, @"<main id=""main""[^>]*>(.*?)</main>", RegexOptions.Singleline | RegexOptions.IgnoreCase);
                if (m.Success) {
                    results[link] = m.Groups[1].Value;
                } else {
                    results[link] = "";
                }
            } catch (Exception ex) {
                Console.WriteLine(string.Format("Error on {0}: {1}", link, ex.Message));
                results[link] = "";
            }
        });
        
        await Task.WhenAll(tasks);
        
        Console.WriteLine("Stitching...");
        string finalHtml = @"<!DOCTYPE html>
<html lang=""en"">
<head>
<meta charset=""UTF-8"">
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
<div style=""text-align:center; padding: 40px 0; border-bottom: 4px solid #2c3e50; margin-bottom: 40px;"">
  <h1>Indigenous Medicinal and Food Plants of the Cayoose Creek Band of Sekw’el’was</h1>
</div>";
        
        foreach (var link in orderedLinks) {
            string content;
            if (results.TryGetValue(link, out content) && !string.IsNullOrEmpty(content)) {
                finalHtml += string.Format("\n<div class=\"stitched-page\">\n{0}\n</div>\n", content);
            }
        }
        finalHtml += "\n</body></html>";
        System.IO.File.WriteAllText("index.html", finalHtml);
        Console.WriteLine("Done! Saved to index.html");
    }
}
"@
Add-Type -TypeDefinition $source -Language CSharp -ReferencedAssemblies System.Net.Http
[Scraper]::Run().GetAwaiter().GetResult()

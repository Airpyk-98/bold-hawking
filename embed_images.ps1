$source = @"
using System;
using System.Net.Http;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.Linq;

public class ImageEmbedder {
    public static async Task Run() {
        var handler = new HttpClientHandler() { UseProxy = true };
        var client = new HttpClient(handler);
        client.Timeout = TimeSpan.FromMinutes(10);
        client.DefaultRequestHeaders.Add("User-Agent", "Mozilla/5.0");
        
        string html = System.IO.File.ReadAllText("temp.html");
        
        var pattern = @"<img[^>]+src=""([^""]+)""";
        var matches = Regex.Matches(html, pattern, RegexOptions.IgnoreCase);
        
        var uniqueUrls = new HashSet<string>();
        foreach (Match m in matches) {
            uniqueUrls.Add(m.Groups[1].Value);
        }
        
        Console.WriteLine(string.Format("Found {0} unique images.", uniqueUrls.Count));
        
        var imageCache = new ConcurrentDictionary<string, string>();
        
        var tasks = uniqueUrls.Select(async url => {
            if (url.StartsWith("data:")) return;
            try {
                byte[] imageBytes = await client.GetByteArrayAsync(url);
                string base64 = Convert.ToBase64String(imageBytes);
                string ext = "png";
                if (url.ToLower().EndsWith(".jpg") || url.ToLower().EndsWith(".jpeg")) ext = "jpeg";
                string dataUri = string.Format("data:image/{0};base64,{1}", ext, base64);
                imageCache[url] = dataUri;
            } catch (Exception ex) {
                Console.WriteLine(string.Format("Error downloading {0}: {1}", url, ex.Message));
            }
        });
        
        await Task.WhenAll(tasks);
        
        foreach (var kvp in imageCache) {
            html = html.Replace("src=\"" + kvp.Key + "\"", "src=\"" + kvp.Value + "\"");
        }
        
        System.IO.File.WriteAllText("Corrected_Pilot_Fixed.doc", html);
        System.IO.File.WriteAllText("Original_Reference_Fixed.doc", html);
        Console.WriteLine("Done! Saved self-contained files.");
    }
}
"@
Add-Type -TypeDefinition $source -Language CSharp -ReferencedAssemblies System.Net.Http
[ImageEmbedder]::Run().GetAwaiter().GetResult()

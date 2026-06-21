import xml.etree.ElementTree as ET

# Define the namespace dictionary
ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
   <url>
      <loc>https://example.com</loc>
      <lastmod>2026-06-21</lastmod>
   </url>
</urlset>
"""

# Parse the XML data
root = ET.fromstring(xml_data)

# Use the 'ns' prefix in your XPath queries
for url in root.findall("ns:url", ns):
    loc = url.find("ns:loc", ns).text
    print(loc)
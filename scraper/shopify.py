from curl_cffi import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json
import csv
import time
import sys
from datetime import datetime
# ---------Configuration---------
# STORE_URL="https://www.allbirds.com"
STORE_URL_LIST=["https://www.tentree.com", "https://maguireshoes.com", "https://www.adoredvintage.com", "https://skims.com"]

def is_shopify_store(url):
  try:
    response = requests.get(
      f"{url}/products.json?limit=1",
      impersonate="chrome120",
      timeout=10
    )
    if response.status_code == 200:
      data = response.json()
      return 'products' in data
    
  except Exception as e:
    return e
  return False

def diagnose_shopify_store(store_url):
  """Run a full diagnosis of a shopify store"""
  report = {"store": store_url}
  ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

  # 1. products.json availability + get a sample handle
  sample_handle = None
  try:
    resp = requests.get(
      f"{store_url}/products.json?limit=1",
      impersonate="chrome120",
      timeout=10
    )
    report["products_json"] = resp.status_code
    if resp.status_code == 200:
      data = resp.json()
      report["is_shopify"] = "products" in data
      if data.get("products"):
        sample_handle = data["products"][0]["handle"]
    else: 
      report["is_shopify"] = False
  except Exception:
    report["products_json"] = "Error"
    report["is_shopify"] = False
  
  # 2. Catalog size from sitemap (checks all product sub-sitemaps)
  try:
    resp = requests.get(
      f"{store_url}/sitemap.xml",
      impersonate="chrome120",
      timeout=10
    )
    root = ET.fromstring(resp.content)
    total = 0
    for sm in root.findall("ns:sitemap", ns):
      loc = sm.find("ns:loc", ns).text
      if "products" in loc:
        req2 = requests.get(loc, impersonate="chrome120", timeout=15)
        req2_root = ET.fromstring(req2.content)
        total += sum(
          1 for u in req2_root.findall("ns:url", ns)
          if "/products" in u.find("ns:loc", ns).text
        )
      report["catalog_size"] = total if total else None
  except:
    report["catalog_size"] = None

  # 3. /products/{handle}.js endpoint
  if sample_handle:
    try:
      r = requests.get(
        f"{store_url}/products/{sample_handle}.js",
        impersonate="chrome120", timeout=10
      )
      report["js_endpoint"] = r.status_code == 200
    except:
      report["js_endpoint"] = False

  # 4. /collections.json endpoint
  try:
    r = requests.get(
      f"{store_url}/collections.json?limit=1",
      impersonate="chrome120", timeout=10
    )
    report["collections_json"] = (
      r.status_code == 200 and "collections" in r.json()
    )
  except:
    report["collections_json"] = False

  return report

for store_url in STORE_URL_LIST:
  report = diagnose_shopify_store(store_url)
  for key, value in report.items():
    print(f"{key}:  {value}")
  print("-"*30)



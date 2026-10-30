import csv
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

url = "https://www.musashino-u.ac.jp/"
parsed_base = urlparse(url)
domain = parsed_base.netloc  

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}


visited_urls = set()
queue = [url]


sitemap_data = {}

print("武蔵野大学のサイトマップのクロールを開始します...")


max_pages = 30

while queue and len(visited_urls) < max_pages:
  current_url = queue.pop(0)

  if current_url in visited_urls:
    continue

  print(f"クロール中: {current_url}")
  visited_urls.add(current_url)

  try:
    
    res = requests.get(current_url, headers=headers, timeout=10)

    
    time.sleep(1)

    
    if res.status_code != 200:
      print(f"スキップ：ステータスコード {res.status_code}")
      continue

    res.encoding = res.apparent_encoding

    
    soup = BeautifulSoup(res.text, 'html.parser')

    
    title_tag = soup.find('title')
    title_text = title_tag.text.strip() if title_tag else "No Title"

    
    sitemap_data[current_url] = title_text

    
    for a_tag in soup.find_all('a', href=True):
      href = a_tag['href']

      
      absolute_url = urljoin(current_url, href)

      
      parsed_url = urlparse(absolute_url)
      clean_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

      
      if (
          parsed_url.netloc == domain
          and clean_url not in visited_urls
          and clean_url not in queue
      ):
        queue.append(clean_url)

  except Exception as e:
    print(f"エラー発生 {current_url}: {e}")


csv_filename = "musashino_sitemap.csv"
with open(csv_filename, mode="w", encoding="utf-8-sig", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["URL", "Title"])
  for url, title in sitemap_data.items():
    writer.writerow([url, title])

print(
    f"クロール完了しました。合計 {len(sitemap_data)} ページのデータを収集し、"
    f"{csv_filename} に保存しました。"
)
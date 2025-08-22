import requests
from bs4 import BeautifulSoup
import random
def get_free_proxies():
    url = "https://free-proxy-list.net/"
    headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://e-hentai.org/",
    "Accept": "text/html",
    "Accept-Language": "zh-TW"
    }
    response = requests.get(url, headers=headers,timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    proxies = []
    #class有可能要改
    table=soup.find("table", class_="table table-striped table-bordered")
    if not table or not table.find("tbody"):                              
        return proxies
    for row in table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        ip = cols[0].get_text(strip=True)
        port = cols[1].get_text(strip=True)
        https = cols[6].get_text(strip=True).lower()
        if https == "yes":
            proxies.append(f"https://{ip}:{port}")
        else:
            proxies.append(f"http://{ip}:{port}")
    return proxies

def main():
    proxies = get_free_proxies()
    if proxies:
        print("獲取到的免費代理列表:")
        for proxy in proxies:
            print(proxy)
    else:
        print("未能獲取到免費代理。")
if __name__ == "__main__":
    main()
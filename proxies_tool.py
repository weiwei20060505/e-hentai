import requests
from bs4 import BeautifulSoup
import random
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://e-hentai.org/",
    "Accept": "text/html",
    "Accept-Language": "zh-TW"
    }
def get_free_proxies(https_only: bool = True) -> list[str]:
    url = "https://free-proxy-list.net/"
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
        elif not https_only:
            proxies.append(f"http://{ip}:{port}")
    return proxies
def test_proxy(proxy: str, test_url: str = "https://httpbin.org/ip", timeout: int = 5) -> bool:
    try:
        response = requests.get(test_url, proxies={"http": proxy, "https": proxy}, headers=headers ,timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False
def get_working_proxy(max_test: int = 30) -> str | None:
    proxies = get_free_proxies()
    print(f"抓到 {len(proxies)} 個代理")
    random.shuffle(proxies)
    tested = 0
    for proxy in proxies:
        if tested >= max_test:                               
            break
        tested += 1
        if test_proxy(proxy):
            return proxy                                           
    return None 
def main():
    print(get_working_proxy())
if __name__ == "__main__":
    main()
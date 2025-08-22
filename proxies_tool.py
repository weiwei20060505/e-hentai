import requests
from bs4 import BeautifulSoup
import random
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html",
    "Accept-Language": "zh-TW"
    }
def get_free_proxies(https_only: bool =True) -> list[str]:
    url = "https://free-proxy-list.net/zh-tw/ssl-proxy.html"
    response = requests.get(url, headers=headers, timeout=10)
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
def test_proxy(proxy: str, test_url: str = "https://httpbin.org/ip") -> bool:
    try:
        if proxy.startswith("https"):
            proxies={"https": proxy}
        else:
            proxies={"http": proxy}
        response = requests.get(test_url, proxies=proxies, headers=headers, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
def get_working_proxy(max_test: int = 100) -> str | None:
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
        else:
            print(f"第{tested}個代理不可用：{proxy}")                                          
    return None 
def main():
    print(get_working_proxy())
if __name__ == "__main__":
    main()
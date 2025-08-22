import os
import requests
from bs4 import BeautifulSoup

url = "https://e-hentai.org/g/3426863/b3fb69ce86/"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://e-hentai.org/",
    "Accept": "text/html",
    "Accept-Language": "zh-TW"
}


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


save_folder = soup.find('head').find('title').get_text()
path=f"e-hentai-images//{save_folder}"
os.makedirs(path, exist_ok=True)

a_href=soup.find('div',id="gdt").find_all('a')

link_set=[]
for link in a_href:
    img_url = link.get('href')
    response2 = requests.get(img_url, headers=headers)
    soup2 = BeautifulSoup(response2.text, "html.parser")
    src=soup2.find('img', id='img')
    if src:
        img_url2 = src.get('src')
        link_set.append(img_url2)
        try:
            image_response = requests.get(img_url2, headers=headers)
            if image_response.status_code == 200:
                    # 用圖片網址的最後一段當檔名
                    filename = os.path.basename(img_url2)
                    filepath = os.path.join(path, filename)

                    with open(filepath, "wb") as f:
                        f.write(image_response.content)
                    print(f"已儲存：{filename}")
            else:
                print(f"圖片下載失敗：{img_url2}")                          
        except Exception as e:
                print(f"錯誤：{e}")
    else:
        print(f'{img_url}沒找到原圖:error')
print(f"\n✅ 共抓到 {len(link_set)} 張原圖")
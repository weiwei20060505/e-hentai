import os
import requests
from bs4 import BeautifulSoup
import time
import random
import asyncio
import aiohttp
import re

def safe_folder_name(name):
    """移除不允許的字元"""
    return re.sub(r'[\\/:*?"<>|]', "_", name)

def get_total_pages(url):
    """取得總頁數"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lastpage = soup.select("table.ptt td")[-2].text  # 倒數第二格是最後頁碼
    return int(lastpage)
def find_makedirs(url,save_folder_path):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://e-hentai.org/",
        "Accept": "text/html",
        "Accept-Language": "zh-TW"
    }
    os.makedirs(save_folder_path, exist_ok=True)

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    folder_name = soup.find('head').find('title').get_text()
    folder_name = safe_folder_name(folder_name)
    
    path=os.path.join(save_folder_path,folder_name)
    os.makedirs(path, exist_ok=True)
    return path
async def get_image_urls_from_page(session, page_url):
    headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://e-hentai.org/",
            "Accept": "text/html",
            "Accept-Language": "zh-TW"
        }
    page=int(page_url.split('=')[-1])+1
    try:
        async with session.get(page_url, headers=headers) as response:
            if response.status != 200:
                print(f"頁面 {page} 請求失敗，狀態碼：{response.status}")
                return []
            
            html_content = await response.text()
            soup = BeautifulSoup(html_content, "html.parser")
            a_href=soup.find('div',id="gdt").find_all('a')
            if not a_href:
                print(f"頁面 {page} 沒有找到圖片連結")
                return []
            page_img_urls_list = []
            for link in a_href:
                img_url = link.get('href')
                page_img_urls_list.append(img_url)
            print(f"第 {page} 頁已完成解析")
            return page_img_urls_list
    except Exception as e:
        print(f"解析頁面 {page} 時發生錯誤：{e}")
        return []
async def download_image(session, img_url, path):
    headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://e-hentai.org/",
            "Accept": "text/html",
            "Accept-Language": "zh-TW"
        }
    img_name=f"第{img_url.split('-')[-1]}頁.jpg"
    try:
        async with session.get(img_url, headers=headers) as response:
            if response.status != 200:
                print(f"圖片 {img_name} 請求失敗，狀態碼：{response.status}")
                return
            html_content = await response.text()
            soup= BeautifulSoup(html_content, "html.parser")
            src=soup.find('img', id='img')
            if not src:
                print(f"圖片 {img_name} 沒有找到原圖")
                return
            org_img_link= src.get('src')
            try:
                image_response = requests.get(org_img_link, headers=headers)
                if image_response.status_code == 200:
                    filepath = os.path.join(path, img_name)
                    with open(filepath, "wb") as f:
                        f.write(image_response.content)
                        print(f"已儲存：圖片 {img_name}")
                else:
                    print(f"圖片 {img_name} 下載失敗，狀態碼：{response.status}")    
            except Exception as e:
                print(f"圖片 {img_name}錯誤：{e}")                      
    except Exception as e:
        print(f"圖片 {img_name}錯誤：{e}")
    return


async def download_gallery(url, start_page=1, end_page=1, auto_all=False, save_folder_path="C:\Users\weiwe\Desktop\e-hentai-images"):
    path=find_makedirs(url,save_folder_path)
    if auto_all:
        end_page = get_total_pages(url)
        start_page = 0
        print(f"📖 偵測到總頁數：{end_page}，將下載整本")
    else:
        start_page -= 1
        end_page -= 1
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for page in range(start_page, end_page + 1):
            page_url = f"{url}?p={page}"
            tasks.append(get_image_urls_from_page(session, page_url))
        
        all_image_urls_list = await asyncio.gather(*tasks)
        all_image_urls = [item for sublist in all_image_urls_list for item in sublist]
        
        print(f"\n✅ 共找到 {len(all_image_urls)} 張圖片網址")
        
        download_tasks = [download_image(session, img_url, path) for img_url in all_image_urls]
        await asyncio.gather(*download_tasks)
        print("\n🎉 所有圖片下載完成！")
    return
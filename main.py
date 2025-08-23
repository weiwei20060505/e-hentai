from ehentai_downloader import download_gallery
import asyncio
if __name__ == "__main__":
    url = input("請輸入畫廊網址：").strip()
    mode = input("要下載整本嗎？(y/n)：").strip().lower()

    if mode == "y":
        download_gallery(url, auto_all=True)
    else:
        start_page = int(input("請輸入起始頁數（例如 1）：").strip())
        end_page = int(input("請輸入結束頁數（例如 5）：").strip())
        asyncio.run(download_gallery(url, start_page, end_page))




import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

logo = r'''
███╗   ███╗██╗    ██╗██╗  ██╗
████╗ ████║██║    ██║██║  ██║
██╔████╔██║██║ █╗ ██║███████║
██║╚██╔╝██║██║███╗██║██╔══██║
██║ ╚═╝ ██║╚███╔███╔╝██║  ██║
╚═╝     ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝

By: @alisster00         v.1.0
'''
class MediaWebHunter:
    def __init__(self, url, max_workers=5):
        self.url = url.strip()
        self.img_dir = "IMAGES"
        self.vid_dir = "VIDEOS"
        os.makedirs(self.img_dir, exist_ok=True)
        os.makedirs(self.vid_dir, exist_ok=True)
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.max_workers = max_workers

    def fetch_content(self):
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            print(f"\033[1;33m[\033[0m!\033[1;33m]\033[1;31m Error fetching URL {self.url}: {e}\033[0m\n")
            return None

    def _get_extension(self, response, fallback):
        content_type = response.headers.get("Content-Type", "")
        if "png" in content_type:
            return ".png"

        elif "jpeg" in content_type or "jpg" in content_type:
            return ".jpg"

        elif "gif" in content_type:
            return ".gif"

        elif "mp4" in content_type:
            return ".mp4"

        elif "webm" in content_type:
            return ".webm"

        else:
            return fallback
                
    def _download_file(self, url, files_dir, prefix, index, fallback_ext):
        try:
            with requests.get(url, headers=self.headers, timeout=20, stream=True) as r:
                r.raise_for_status()
                extension = os.path.splitext(url)[1]
                if not extension:
                    extension = self._get_extension(r, fallback_ext)

                file_name = os.path.join(files_dir, f"{prefix}_{index}{extension}")
                if os.path.exists(file_name):
                    print(f"\033[1;33m[\033[0m!\033[1;33m]\033[1;35m This file already exist: {file_name}\033[0m")
                    return

                with open(file_name, "wb") as file:
                    for chunk in r.iter_content(chunk_size=8192):
                        file.write(chunk)

                print(f"\033[1;33m[\033[0m+\033[1;33m]\033[1;32m Saved: {file_name}\033[0m")
        except requests.RequestException as e:
            print(f"\033[1;33m[\033[0m!\033[1;33m]\033[1;31m Error downloading {url}: {e}\033[0m\n")
        except OSError as e:
            print(f"\033[1;33m[\033[0m!\033[1;33m]\033[1;31m Error saving {url}: {e}\033[0m\n")
    
    def _get_best_img(self, img_tag):
        if img_tag.get("srcset"):
            options = [s.split()[0] for s in img_tag["srcset"].split(",")]
            return options[-1].strip()

        elif img_tag.get("data-src"):
            return img_tag("data-src")

        elif img_tag.get("data-original"):
            return img_tag("data-original")

        else:
            return img_tag("src")

    def download_images(self, soup):
        images = soup.find_all("img")
        tasks = []
    
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for i, img in enumerate(images):
                #src = img.get("src")
                src = self._get_best_img(img)
                if not src or src.startswith(("data:", "blob:")):
                    continue
                img_url = urljoin(self.url, src)
                tasks.append(executor.submit(self._download_file, img_url, self.img_dir, "IMG", i, ".jpg"))

            for future in as_completed(tasks):
                future.result()

    def download_videos(self, soup):
        videos = []
        for video in soup.find_all("video"):
            if video.get("src"):
                videos.append(video.get("src"))
            for source in video.find_all("source"):
                if source.get("src"):
                    video.append(source.get("src"))

        videos = list(set(videos))

        tasks = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for i, vid_src in enumerate(videos):
                if vid_src.startswith(("data:", "blob:")):
                    continue
                vid_url = urljoin(self.url, vid_src)
                tasks.append(executor.submit(self._download_file, vid_url, self.vid_dir, "VID", i, ".mp4"))

            for future in as_completed(tasks):
                future.result()

    def run(self):
        soup = self.fetch_content()
        if soup:
            self.download_images(soup)
            self.download_videos(soup)
        else:
            print(f"\033[1;33m[\033[0m!\033[1:33m]\033[1;31m The content couldn't be fetched.\033[0m\n")

def clean_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

if __name__ == '__main__':
    clean_screen()
    print(f"\033[1;34m{logo}")
    url = input("\033[1;33m[\033[0m*\033[1;33m]\033[1;32m Enter your URL:\033[0m ")
    hunter = MediaWebHunter(url, max_workers=10)
    hunter.run()

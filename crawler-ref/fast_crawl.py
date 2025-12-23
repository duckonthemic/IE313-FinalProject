"""
Fast crawl - save URLs to file then batch download
Target: 3000+ jobs from CareerViet (has 4970 URLs available)
"""
import os
import json
import time
import random
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Thread-local storage for drivers
local = threading.local()

def get_driver():
    if not hasattr(local, 'driver'):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        local.driver = webdriver.Chrome(options=options)
        local.driver.set_page_load_timeout(15)
    return local.driver

def get_careerviet_urls(max_pages=80):
    """Get job URLs from CareerViet listing pages - target 4000 jobs"""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(20)
    
    job_urls = set()
    base_url = "https://careerviet.vn/viec-lam/tat-ca-viec-lam-trang-{page}-vi.html"
    
    print("Getting job URLs from CareerViet...")
    for page in tqdm(range(1, max_pages + 1), desc="Listing pages"):
        url = base_url.format(page=page)
        
        try:
            driver.get(url)
            time.sleep(1)
            
            links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/vi/tim-viec-lam/']")
            for link in links:
                href = link.get_attribute("href")
                if href and '.html' in href and 'tim-viec-lam' in href:
                    job_urls.add(href)
                    
        except Exception as e:
            continue
    
    driver.quit()
    return list(job_urls)

def download_page(args):
    """Download a single page"""
    url, output_dir = args
    try:
        driver = get_driver()
        
        url_hash = str(abs(hash(url)))[-12:]
        filename = f"job_{url_hash}.html"
        filepath = os.path.join(output_dir, filename)
        
        if os.path.exists(filepath):
            return None
        
        driver.get(url)
        time.sleep(0.5)
        
        html = driver.page_source
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return filepath
        
    except Exception as e:
        return None

def main():
    print("="*60)
    print("FAST CRAWL - TARGET 3000+ JOBS")
    print("="*60)
    
    output_dir = "./data/html_content/careerviet"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get URLs (80 pages × ~50 = ~4000 unique URLs)
    job_urls = get_careerviet_urls(max_pages=80)
    print(f"\nTotal unique URLs: {len(job_urls)}")
    
    # Save URLs for reference
    with open('./data/careerviet_urls.json', 'w') as f:
        json.dump(job_urls, f)
    
    # Get existing files
    existing = set(os.listdir(output_dir))
    to_download = []
    for url in job_urls:
        url_hash = str(abs(hash(url)))[-12:]
        filename = f"job_{url_hash}.html"
        if filename not in existing:
            to_download.append((url, output_dir))
    
    print(f"Existing: {len(existing)}, To download: {len(to_download)}")
    
    if len(to_download) == 0:
        print("All files already downloaded!")
        return
    
    # Download with single driver (more reliable)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(15)
    
    downloaded = 0
    for url, out_dir in tqdm(to_download, desc="Downloading"):
        try:
            url_hash = str(abs(hash(url)))[-12:]
            filename = f"job_{url_hash}.html"
            filepath = os.path.join(out_dir, filename)
            
            driver.get(url)
            time.sleep(0.3)
            
            html = driver.page_source
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            downloaded += 1
            
        except:
            continue
    
    driver.quit()
    
    total = len([f for f in os.listdir(output_dir) if f.endswith('.html')])
    print(f"\n{'='*60}")
    print(f"COMPLETE: {downloaded} new, {total} total HTML files")
    print("="*60)

if __name__ == "__main__":
    main()

import re, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import cloudscraper

scraper = cloudscraper.create_scraper()

def safe_get(url):
    try:
        return scraper.get(url, timeout=20)
    except:
        return None

def seo_analyze(url):
    start = time.time()
    res = safe_get(url)
    if not res:
        return {"Error": "Blocked by Cloudflare / Bot Firewall"}

    load_time = round(time.time() - start, 2)
    soup = BeautifulSoup(res.text, "html.parser")

    title = soup.title.text.strip() if soup.title else "Missing"
    meta = soup.find("meta", attrs={"name":"description"})
    meta_desc = meta["content"].strip() if meta else "Missing"

    headings = {f"H{i}": len(soup.find_all(f"h{i}")) for i in range(1,7)}

    imgs = soup.find_all("img")
    missing_alt = len([i for i in imgs if not i.get("alt")])

    domain = urlparse(url).netloc
    internal = external = 0
    for a in soup.find_all("a"):
        href = a.get("href","")
        if domain in href:
            internal += 1
        elif href.startswith("http"):
            external += 1

    text = soup.get_text().lower()
    words = re.findall(r'\w+', text)
    word_count = len(words)

    freq = {}
    for w in words:
        if len(w) > 3:
            freq[w] = freq.get(w,0) + 1
    top_keywords = sorted(freq.items(), key=lambda x:x[1], reverse=True)[:10]

    robots = safe_get(url.rstrip("/") + "/robots.txt")
    sitemap = safe_get(url.rstrip("/") + "/sitemap.xml")

    return {
        "Website": url,
        "Title": title,
        "Meta Description": meta_desc,
        "Load Time (sec)": load_time,
        "HTTPS Enabled": url.startswith("https"),
        "Robots.txt Exists": True if robots and robots.status_code==200 else False,
        "Sitemap.xml Exists": True if sitemap and sitemap.status_code==200 else False,
        "Word Count": word_count,
        "Top Keywords": top_keywords,
        "Internal Links": internal,
        "External Links": external,
        "Images Without ALT": missing_alt,
        "Headings": headings
    }

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import xml.etree.ElementTree as ET
import tldextract
import time

class FullSitemapGenerator:
    def __init__(self, start_url):
        self.start_url = start_url.rstrip('/')
        self.domain = self.get_domain(start_url)
        self.visited = set()
        self.to_visit = set([self.start_url])

        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_domain(self, url):
        extracted = tldextract.extract(url)
        return f"{extracted.domain}.{extracted.suffix}"

    def is_internal_link(self, url):
        parsed = urlparse(urljoin(self.start_url, url))
        return self.get_domain(parsed.netloc) == self.domain

    def is_clean_url(self, url):
        parsed = urlparse(url)
        return parsed.query == ''

    def crawl(self):
        print(f"[+] Crawling: {self.start_url}")
        while self.to_visit:
            current_url = self.to_visit.pop()
            if current_url in self.visited:
                continue

            print(f"[*] Visiting: {current_url}")
            try:
                self.driver.get(current_url)
                time.sleep(1)

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                self.visited.add(current_url)

                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href).split('#')[0].rstrip('/')
                    if self.is_internal_link(full_url) and full_url not in self.visited and self.is_clean_url(full_url):
                        self.to_visit.add(full_url)

            except Exception as e:
                print(f"[!] Failed: {e}")
                continue

    def generate_sitemap(self, output_file="sitemap.xml"):
        print("[+] Writing sitemap.xml")
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

        for url in sorted(self.visited):
            if not self.is_clean_url(url):
                continue

            url_elem = ET.SubElement(urlset, "url")

            loc = ET.SubElement(url_elem, "loc")
            loc.text = url

            lastmod = ET.SubElement(url_elem, "lastmod")
            lastmod.text = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")

            changefreq = ET.SubElement(url_elem, "changefreq")
            if url == self.start_url:
                changefreq.text = "daily"
            elif "/blog" in url or "/service" in url or "/portfolio" in url:
                changefreq.text = "weekly"
            else:
                changefreq.text = "monthly"

            priority = ET.SubElement(url_elem, "priority")
            if url == self.start_url:
                priority.text = "1.0"
            elif "/blog" in url or "/portfolio" in url:
                priority.text = "0.7"
            elif "/service" in url:
                priority.text = "0.8"
            else:
                priority.text = "0.8"

        self._indent(urlset)
        tree = ET.ElementTree(urlset)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"[✓] Sitemap saved to {output_file}")

    def _indent(self, elem, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            for child in elem:
                self._indent(child, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i

    def close(self):
        self.driver.quit()


# --- Usage ---
if __name__ == "__main__":
    start_url = input("Enter website URL (e.g., https://example.com): ").strip()
    bot = FullSitemapGenerator(start_url)
    bot.crawl()
    bot.generate_sitemap()
    bot.close()

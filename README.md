````markdown
# 🕸️ Full Website Sitemap Generator

A Python-powered bot that automatically crawls and generates a fully formatted `sitemap.xml` for any website — perfect for SEO submissions and Google indexing.

---

## 🚀 Features

- ✅ Crawls all internal links (JS-rendered and static)
- ✅ Uses **headless Chrome (Selenium)** for dynamic websites
- ✅ Skips query-string URLs like `?filter[...]`
- ✅ Generates a **Google-compatible, pretty-printed `sitemap.xml`**
- ✅ Sets `lastmod`, `changefreq`, and `priority` automatically

---

## 🧰 Requirements

### Python 3.8+
Install dependencies:

```bash
pip install selenium beautifulsoup4 tldextract
````

### ChromeDriver

* Download ChromeDriver: [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
* Make sure the version matches your installed Chrome browser
* Place the `chromedriver` binary in your PATH or next to your script

---

## 📦 How to Run

```bash
python sitemap.py
```

You'll be prompted to enter your website URL, for example:

```
Enter website URL (e.g., https://example.com): https://ryven.co
```

After crawling, a `sitemap.xml` file will be created in the current directory.

---

## 🗂 Output Example

```xml
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com</loc>
    <lastmod>2025-05-23T10:00:00+00:00</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  ...
</urlset>
```

---

## ⚠️ Notes

* This tool **respects JavaScript rendering** using Selenium
* It ignores URLs with query strings to keep sitemap clean
* Be respectful when crawling third-party websites
* Set crawl delay if you plan to crawl large sites frequently

---

## 👨‍💻 Author

**Sifat Kazi**
Founder, [Ryven.co](https://ryven.co)

---

## 📄 License

MIT License – free to use, modify, and distribute.

```
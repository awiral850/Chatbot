In this class, we dive into the world of the web: understanding how the internet works, what HTTP is, and how to build a simple web scraper in Python.

## 1. What is HTTP?

HTTP (HyperText Transfer Protocol) is the way your browser and websites talk to each other. Think of it as a set of rules for sending messages between your computer and a web server.

### Visual: HTTP Request/Response

```text
Browser (You)  |----------------------->|   Server
		 |   (HTTP Request)       |
		 |                        |
		 |<-----------------------|   (HTTP Response)
```

HTTP messages are just text. The server knows a message is done when it sees a blank line (two newlines `\n\n`).

**Example HTTP Request:**

```text
GET / HTTP/1.1
Host: example.com
User-Agent: Chrome

```

The server starts processing as soon as it sees the blank line at the end.

#### Understanding HTTP as a Protocol (See it in Action with nc)

You can use the `nc` (netcat) command to connect to a web server and send an HTTP request by hand. This helps you see how HTTP works under the hood.

**Example:**

```bash
nc example.com 80
```

Then type (press Enter after each line, and press Enter twice at the end):

```text
GET / HTTP/1.1
Host: example.com


```

The server will only respond after you send the blank line (two Enters, which is `\n\n`).

**Visual:**

```text
You:   GET / HTTP/1.1   --->|
	Host: example.com --->|  (wait...)
	[blank line]      --->|  (now server responds!)
```

**Key Concepts:**

- **Request:** Your browser asks for a web page or data.
- **Response:** The server sends back the page or data.
- **Headers:** Extra info sent with requests/responses (like what browser you use).
- **Status Codes:** Numbers that tell you what happened (e.g., 200 = OK, 404 = Not Found).

**Common HTTP Status Codes:**
| Code | Meaning |
|------|----------------|
| 200 | OK |
| 301 | Moved Permanently |
| 404 | Not Found |
| 500 | Server Error |

---

## 1.1 HTTP Methods: GET, POST, PUT, PATCH

HTTP supports different types of requests, called **methods**. The most common are:

- **GET**: Ask for data (like a web page). Example: visiting a website.
- **POST**: Send new data to the server (like submitting a form).
- **PUT**: Replace existing data on the server.
- **PATCH**: Update part of existing data.

**Visual:**

```text
GET    [You] ---> [Server]  ("Give me this page!")
POST   [You] ---> [Server]  ("Here is some new data!")
PUT    [You] ---> [Server]  ("Replace this data!")
PATCH  [You] ---> [Server]  ("Update this part!")
```

**Example:**

```text
GET /profile HTTP/1.1
POST /profile HTTP/1.1
PUT /profile HTTP/1.1
PATCH /profile HTTP/1.1
```

Most web scraping uses GET (to fetch pages), but sometimes POST is needed for forms.

---

## 2. What is a Web Scraper?

A **web scraper** is a program that automatically downloads web pages and extracts useful information from them.

**How it works:**

1. Send an HTTP request to a web page.
2. Receive the HTML response.
3. Parse the HTML to find the data you want.
4. Save the data (e.g., to a file).

---

## 3. Ethics of Web Scraping

Web scraping is powerful, but it comes with responsibilities:

- **Respect robots.txt:** 
	- `robots.txt` is a special file placed at the root of a website (e.g., `https://example.com/robots.txt`). 
	- It tells web crawlers (like Google or your scraper) which parts of the site can or cannot be accessed. 
	- **Example robots.txt:**
	
			User-agent: *
			Disallow: /private/
			Allow: /public/
	
	- **Key-Value Pairs:** 
		- `User-agent`: Which bots the rule applies to (`*` means all bots). 
		- `Disallow`: Paths bots should NOT visit. - `Allow`: Paths bots CAN visit. 
		- **What if both Disallow and Allow are none?** - If neither `Disallow` nor `Allow` is specified for a user-agent, it means the bot is allowed to crawl everything on the site (no restrictions).

- **Don’t overload servers:** Make requests slowly, don’t hammer the site.
- **Don’t scrape private or sensitive data.**
- **Give credit:** If you use scraped data, cite the source.
- **Check Terms of Service:** Some sites forbid scraping.

---

## 4. The DOM (Document Object Model)

The **DOM** is a tree-like structure representing the elements of a web page (headings, paragraphs, links, etc.).

**Visual:**

```html
<html>
	<body>
		<h1>Hello</h1>
		<a href="page1.html">Page 1</a>
		<a href="page2.html">Page 2</a>
	</body>
</html>
```

Looks like this as a tree:

```text
html
└── body
		├── h1 (Hello)
		├── a (Page 1)
		└── a (Page 2)
```

- When you scrape, you’re really navigating the DOM to find the data you need.
- Example: To get all the links on a page, you find all `<a>` tags in the DOM.

**Learn more:** [MDN Web Docs: Introduction to the DOM](https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model/Introduction)

---

## 5. Depth of a Web Crawler

A **web crawler** is a program that visits a web page, finds links on that page, and can follow those links to visit more pages. The **depth** is how many steps (or "hops") away from the starting page you go.

**Visual Example:**

```text
Start: index.html
  |
  |-- page1.html
  |-- page2.html
		 |
		 |-- page3.html
```

- **Depth 1:** Only `index.html` is scraped.
- **Depth 2:** Scrape `index.html`, then also `page1.html` and `page2.html`.
- **Depth 3:** Scrape `index.html`, `page1.html`, `page2.html`, and `page3.html`.

**HTML Example:**

```html
<!-- index.html -->
<a href="page1.html">Page 1</a>
<a href="page2.html">Page 2</a>
```

**Python Example:**

```python
def crawl(url, depth):
	if depth == 0:
		return
	print(f"Scraping {url}")
	# fetch page, extract links (not shown for brevity)
	for link in find_links(url):
		crawl(link, depth-1)
```

**Be careful:** Deeper crawls can quickly become huge and may overload servers. Always limit your depth!

### 5.1 Crawl Limit: Why It Matters

When building a web crawler, it's important to set a **crawl limit**—the maximum number of pages your crawler will visit. Without a limit, your crawler could:

- Accidentally visit thousands (or millions) of pages, using up bandwidth and resources.
- Overload the target website, which is unethical and could get your IP blocked.
- Take a very long time to finish or even crash your computer.

**Best Practices:**

- Always set a reasonable crawl limit (e.g., 10, 100, or 1000 pages).
- Start with a small limit while testing your code.
- Increase the limit only if you’re sure it’s safe and allowed.

---

## 6. Python Libraries for Web Scraping

### a. `requests`

Lets you send HTTP requests easily.

**Common methods:**

```python
import requests
response = requests.get('https://example.com')
print(response.status_code)  # HTTP status code
print(response.headers)      # Response headers
print(response.text)         # HTML content
```

**Docs:** [requests documentation](https://docs.python-requests.org/en/latest/)

### b. `beautifulsoup4`

Lets you parse and search HTML documents easily.

**Common usage:**

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.text)  # Get the page title
for link in soup.find_all('a'):
	print(link.get('href'))  # Print all links
```

**Docs:** [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

---

## 7. Building a Simple Web Scraper (Project Overview)

**Goal:** Download a web page, extract data, and save it to a file.

**Steps:**

1. Use `requests` to fetch the page.
2. Use `BeautifulSoup` to parse the HTML.
3. Extract the data you want (e.g., all headlines, links, etc.).
4. Save the data to a file (e.g., CSV or TXT).

---

## 8. Example: Scraping All Links from a Page

```python
import requests
from bs4 import BeautifulSoup

url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

links = []
for link in soup.find_all('a'):
	href = link.get('href')
	if href:
		links.append(href)

with open('links.txt', 'w') as f:
	for l in links:
		f.write(l + '\n')
```

---

## 9. Further Reading & Resources

- [What is HTTP? (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview)
- [requests documentation](https://docs.python-requests.org/en/latest/)
- [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [robots.txt info](https://www.robotstxt.org/)
- [Ethics of Web Scraping (Real Python)](https://realpython.com/python-web-scraping-practical-introduction/#is-web-scraping-legal)

---

## 10. Summary

- HTTP is how browsers and servers talk.
- Web scraping lets you extract data from websites.
- Always scrape ethically and legally.
- Use `requests` to fetch pages, `BeautifulSoup` to parse them.
- Understand the DOM and crawler depth.
- Save your data for later use!

## 11. Learning by example code

A simple code to scrape trending topics from kathmandu post

```python
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Target URL
url = 'https://kathmandupost.com/'

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

# Inside ul having class trending-topics-list, all li elements having a tags, extract their url
trending_topics_section = soup.find('ul', class_='trending-topics-list')
trending_topics = trending_topics_section.find_all('li')

trending_paths = []
for each_topic in trending_topics:
    a_tag = each_topic.find('a')
    if a_tag:
        trending_paths.append(a_tag['href'])

trending_articles_urls = []
for each_path in trending_paths:
    full_url = 'https://kathmandupost.com' + each_path
    trending_articles_urls.append(full_url)


# print("Trending Articles URLs:", trending_articles_urls)
# Visit trending articles and extract title, author, date and content
articles_data = []
for article_url in trending_articles_urls:
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.text, features='html.parser')

    tag_mark = article_soup.find('h4', class_='title--line__red')
    tag = None
    if tag_mark:
        tag = tag_mark.find('a').get_text(strip=True)
    
    title = tag_mark.find_next('h1').get_text(strip=True)
    content_paragraphs = article_soup.find('section', class_='story-section').find_all('p')
    content = '\n'.join(p.get_text(strip=True) for p in content_paragraphs)
    
    articles_data.append({
        'title': title,
        'tag': tag,
        'content': content,
        'url': article_url,
        'scraped_at': datetime.now().isoformat()
    })

print(articles_data)
```
import datetime
import io
import json
import logging
import os
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import tempfile
import img2pdf
import tldextract
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

LOG = logging.getLogger(__name__)

combined_xpath = """
    //button[
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see more') or
        contains(@class, 'more') or
        contains(@id, 'more') or 
        contains(@class, 'load') or
        contains(@class, 'expand')
    ] |
    //div[
        (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load more')) and
        not(.//button) and not(.//a)
    ] |
    //span[
        (contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load more')) and
        not(.//button) and not(.//a)
    ]
"""


def is_same_domain_or_subdomain(url, base_domain):
    extracted = tldextract.extract(url)
    link_domain = f"{extracted.domain}.{extracted.suffix}"
    return link_domain == base_domain


def extract_domain_name(url):
    parsed_url = urlparse(url)
    netloc = parsed_url.netloc
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    domain_parts = netloc.split('.')
    domain_name = domain_parts[0]

    return domain_name


def url2canonical_form(url: str):
    parsed = urlparse(url)
    netloc = parsed.netloc.replace('www.', '')

    # Set fragment to empty string to remove it
    fragment = ''

    path = parsed.path

    # Remove trailing slash in all these cases:
    # 1. When path is just "/" (with or without fragments/queries)
    # 2. When path ends with "/" and is longer than 1 character
    if path == '/' or (path.endswith('/') and len(path) > 1):
        path = path[:-1] if path != '/' else ''

    canonical = urlunparse((
        parsed.scheme,
        netloc,
        path,
        parsed.params,
        parsed.query,
        fragment
    ))

    return canonical


def generate_uuid():
    return uuid.uuid4().hex


class WebAgent:
    def __init__(self, driver, output_file="discovered_links.txt"):

        self.driver = driver
        self.visited_urls = set()
        self.output_file = output_file
        self.all_links = []
        self.edges = []

        window_size = driver.get_window_size()

        self.start_width = window_size['width']
        self.start_height = window_size['height']

        self.start_url = None

    def parse_page(self) -> BeautifulSoup:
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def extract_all_links(self) -> list[str]:
        elements = self.driver.find_elements(By.XPATH, "//a[@href]")
        links = []

        for element in elements:
            href = element.get_attribute("href")
            if href and href.startswith("http"):
                links.append(href)

        return links

    def _scroll_to_bottom(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break

            last_height = new_height

    def _unwrap_content(self, max_attempts=100):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        attempts = 0

        while attempts < max_attempts:
            attempts += 1
            found_element = False

            try:
                elements = self.driver.find_elements(By.XPATH, combined_xpath)
                processed_elements = set()
                for element in elements:
                    element_id = element.id

                    if element_id in processed_elements:
                        continue

                    processed_elements.add(element_id)

                    if element.is_displayed() and element.is_enabled():
                        try:
                            LOG.info(f"Clicking {element.tag_name} element with text: {element.text.strip()}")
                            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(0.5)
                            element.click()
                            time.sleep(0.5)
                            found_element = True
                            break
                        except Exception as e:
                            LOG.warning(f"Failed to click element: {str(e)}")
                            continue

            except Exception as e:
                LOG.error(f"Error in _unwrap_content: {str(e)}")

            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height and not found_element:
                LOG.info("No height change and no clickable elements found. Stopping expansion.")
                break

            last_height = new_height

    def expand_page(self):
        LOG.info("Expanding page...")
        self._scroll_to_bottom()
        self._unwrap_content()
        LOG.info("Page expanded...")

    def get_content_type(self):
        content_type = self.driver.execute_script("return document.contentType")

        if content_type == "text/html":
            return "HTML"
        elif content_type.startswith("image/"):
            return "Image"
        elif content_type.startswith("audio/"):
            return "Audio"
        elif content_type == "application/pdf":
            return "PDF"
        elif content_type.startswith("video/"):
            return "Video"
        else:
            return f"Other: {content_type}"

    def capture_webpage_as_pdf(self, output_pdf_path="webpage.pdf"):
        try:
            time.sleep(3)

            total_width = self.driver.execute_script("return document.body.scrollWidth")
            total_height = self.driver.execute_script("return document.body.scrollHeight")

            self.driver.set_window_size(total_width, min(20000, total_height + 100))
            time.sleep(1)

            screenshot = driver.get_screenshot_as_png()

            img = Image.open(io.BytesIO(screenshot))

            temp_image_paths = []
            with tempfile.TemporaryDirectory() as temp_dir:
                IMG_HEIGHT = 2 * self.start_height
                for i, cur_top in enumerate(range(0, img.height, IMG_HEIGHT)):
                    cropped_img = img.crop((0, cur_top, img.width, min(cur_top + IMG_HEIGHT, img.height)))

                    temp_path = os.path.join(temp_dir, f"slice_{i}.png")
                    cropped_img.save(temp_path)
                    temp_image_paths.append(temp_path)

                # Convert all image slices to a single PDF
                with open(output_pdf_path, "wb") as f:
                    f.write(img2pdf.convert(temp_image_paths))

            return output_pdf_path

        except Exception as e:
            print(f"An error occurred: {e}")
            import traceback
            traceback.print_exc()
            return None

    def crawl_website(self, start_url, folder, filename):

        dir_path = Path(folder)
        dir_path.mkdir(parents=True, exist_ok=True)

        output_path = dir_path / Path(filename)

        self.start_url = start_url
        urls_to_visit = [{
            'link': url2canonical_form(start_url),
            'from': 'ROOT'
        }]

        start_domain = tldextract.extract(start_url)
        base_domain = f"{start_domain.domain}.{start_domain.suffix}"

        while urls_to_visit:
            current_entry = urls_to_visit.pop(0)

            current_url = current_entry['link']

            if current_url in self.visited_urls:
                continue

            LOG.info(f"Handling {current_url}")

            self.visited_urls.add(current_url)

            try:
                self.driver.get(current_url)
                time.sleep(0.1)

                status_code = self.driver.execute_script(
                    "return window.performance.getEntries()[0].responseStatus"
                )

                if status_code != 200:
                    continue

                self.expand_page()
                if not os.path.exists('./content'):
                    os.mkdir('./content')

                filename = f"{hash(current_url)}.pdf"
                self.capture_webpage_as_pdf(f'content/{filename}')
                time.sleep(0.1)

                self.all_links.append({
                    'link': current_entry['link'],
                    'id': hash(current_entry['link']),
                    'content_type': self.get_content_type(),
                    'filename': filename,
                })

                current_page_links = set(self.extract_all_links())

                LOG.info(f"Link from this page: {current_page_links}")

                for link in current_page_links:
                    if is_same_domain_or_subdomain(link, base_domain):
                        link = url2canonical_form(link)
                        if current_url != link:
                            urls_to_visit.append({
                                'link': link,
                                'from': current_url
                            })
                            self.edges.append((current_url, link))

            except Exception as e:
                raise e

            self.save_result(output_path)

    def save_result(self, filename):
        used = set()
        final_links = []
        for entry in self.all_links:
            if entry['link'] not in used:
                used.add(entry['link'])

                children = []
                for edge in self.edges:
                    if edge[0] == entry['link']:
                        children.append(edge[1])

                final_links.append({
                    'id': entry['id'],
                    'content_type': entry['content_type'],
                    'filename': entry['filename'],
                    'link': entry['link'],
                    'children': list(set(children))
                })

        result = {'dt': datetime.datetime.now().isoformat(), 'start_url': self.start_url,
                  'links': list(sorted(final_links, key=lambda x: x['link']))}

        with open(filename, "w") as f:
            f.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    headless = True
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # critical to have headless for capture_webpage_as_pdf
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10)

    companies = open('companies.txt').readlines()

    for company_url in companies:
    # for company_url in ['https://cbkone.com']:
        agent = WebAgent(driver)

        agent.crawl_website(company_url, './website_links', extract_domain_name(company_url) + '.json')

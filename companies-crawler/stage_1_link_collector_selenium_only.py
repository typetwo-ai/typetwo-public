import datetime
import json
import logging
import time
import uuid
from urllib.parse import urlparse, urlunparse
from pathlib import Path
import tldextract
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

    def save_page_as_pdf(self, output_path):
        LOG.info(f"Saving page as PDF to {output_path}")

        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_options = {
            'printBackground': True,
            'paperHeight': 8.27,
            'paperWidth': 11.69,
            'marginTop': 0,
            'marginBottom': 0,
            'marginLeft': 0,
            'marginRight': 0,
            'scale': 1.0
        }

        result = self.driver.execute_cdp_cmd('Page.printToPDF', pdf_options)

        with open(output_path, 'wb') as pdf_file:
            import base64
            pdf_data = base64.b64decode(result['data'])
            pdf_file.write(pdf_data)

        LOG.info(f"PDF saved successfully to {output_path}")

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

            self.all_links.append(current_entry)

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
                self.save_page_as_pdf(f'content/{hash(current_url)}.pdf')
                time.sleep(0.1)
                current_page_links = set(self.extract_all_links())

                LOG.info(f"Link from this page: {current_page_links}")

                for link in current_page_links:
                    # TODO: check that it is not a file (.pdf for example).
                    if is_same_domain_or_subdomain(link, base_domain):
                        link = url2canonical_form(link)
                        if current_url != link:
                            urls_to_visit.append({
                                'id': hash(link),
                                'link': link,
                                'from': current_url
                            })

            except Exception as e:
                raise e

            self.save_result(output_path)

    def save_result(self, filename):
        used = set()
        final_links = []
        for entry in self.all_links:
            if entry['link'] not in used:
                froms = []
                for inner_entry in self.all_links:
                    if entry['link'] == inner_entry['link']:
                        froms.append(inner_entry['from'])
                used.add(entry['link'])
                final_links.append({
                    'link': entry['link'],
                    'from': froms
                })

        result = {'dt': datetime.datetime.now().isoformat(), 'start_url': self.start_url,
                  'links': list(sorted(final_links, key=lambda x: x['link']))}

        with open(filename, "w") as f:
            f.write(json.dumps(result, indent=4))


if __name__ == "__main__":
    headless = False
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
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

    # companies = open('companies.txt').readlines()

    for company_url in ['https://cbkone.com']:
        agent = WebAgent(driver)

        agent.crawl_website(company_url, './website_links', extract_domain_name(company_url) + '.json')

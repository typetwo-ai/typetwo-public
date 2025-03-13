import datetime
import json
import logging
import time
from urllib.parse import urlparse
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
    //a[
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'show more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'load more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view more') or
        contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'see more') or
        contains(@class, 'more') or
        contains(@id, 'more') or
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
    if url.endswith('/') and len(url) > 1:
        url = url[:-1]

    url = url.replace('www.', '')

    return url


class WebAgent:
    def __init__(self, driver, output_file="discovered_links.txt"):

        self.driver = driver
        self.visited_urls = set()
        self.output_file = output_file
        self.all_links = set()

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
                            time.sleep(2)
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

    def crawl_website(self, start_url, folder, filename):
        dir_path = Path(folder)
        dir_path.mkdir(parents=True, exist_ok=True)

        output_path = dir_path / Path(filename)

        self.start_url = start_url
        urls_to_visit = [url2canonical_form(start_url)]
        start_domain = tldextract.extract(start_url)
        base_domain = f"{start_domain.domain}.{start_domain.suffix}"

        while urls_to_visit:
            current_url = urls_to_visit.pop(0)

            if current_url in self.visited_urls:
                continue

            LOG.info(f"Handling {current_url}")

            self.visited_urls.add(current_url)

            try:
                self.driver.get(current_url)
                time.sleep(5)
                self.expand_page()
                time.sleep(3)
                current_page_links = set(self.extract_all_links())

                self.all_links |= current_page_links

                for link in current_page_links:
                    # TODO: check that it is not a file (.pdf for example).
                    # TODO: cut / as the end, because we can have dups like "https://thinkbioscience.com/contact", "https://thinkbioscience.com/contact/",
                    if is_same_domain_or_subdomain(link, base_domain):
                        urls_to_visit.append(url2canonical_form(link))

            except Exception as e:
                raise e

            self.save_result(output_path)

    def save_result(self, filename):
        result = {'dt': datetime.datetime.now().isoformat(), 'start_url': self.start_url,
                  'links': list(sorted(self.all_links))}

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

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10)

    for company_url in ['https://thinkbioscience.com']:
        agent = WebAgent(driver)

        agent.crawl_website(company_url, './website_links', extract_domain_name(company_url) + '.json')

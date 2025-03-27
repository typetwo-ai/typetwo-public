import glob
import json
import time
import urllib
from pathlib import Path

import requests
from tqdm.auto import tqdm

HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/39.0.2171.95 Safari/537.36'}
OUTPUT_DIR = Path("./website_links_filtered")
SKIP_EXTENSIONS = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.jpg', '.jpeg', '.png', '.gif']
FILTERED_DOMAINS = [
    'instagram.com',
    'linkedin.com',
    'x.com',
    'twitter.com',
    'facebook.com',
    'threads.net'
]
OUTPUT_DIR.mkdir(exist_ok=True)

failed_companies = []

for path in tqdm(glob.glob("./website_links/*")):
    path = Path(path)

    data = json.load(open(path))

    data['filtered_links'] = []

    failed = False

    for link in data['links']:

        link = link.replace('www.', '')

        parsed_url = urllib.parse.urlparse(link)
        domain = parsed_url.netloc.lower()
        path_part = parsed_url.path.lower()

        if any(filtered_domain == domain for filtered_domain in FILTERED_DOMAINS):
            continue

        if any(path_part.endswith(ext) for ext in SKIP_EXTENSIONS):
            continue

        data['filtered_links'].append(link)
        # try:
        #     result = requests.get(link)
        # except Exception as e:
        #     failed = True
        #     print("Exception, ", e.__repr__())
        #     break
        # time.sleep(1)
        # if result.headers['Content-Type'] == 'text/html':
        #     data['html_links'].append(link)

    if failed:
        failed_companies.append(path.name)

    with open(OUTPUT_DIR / path.name, 'w') as f:
        json.dump(data, f, indent=4)

if failed_companies:
    print("Done, failed with these companies: ", ','.join(failed_companies))

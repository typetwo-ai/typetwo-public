import glob
import json
import mimetypes
import os
import re
import time
import torch
from urllib.parse import urlparse, urljoin
from docling.document_converter import DocumentConverter

import requests
from bs4 import BeautifulSoup
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

from stage_3_utils import transcribe_audio, extract_audio_from_video

ROOT_FOLDER = './website_links_with_content/content/'

CATEGORIES = {
    # HTML
    'html': 'html', 'htm': 'html',
    # Documents
    'pdf': 'pdfs', 'doc': 'pdfs', 'docx': 'pdfs', 'txt': 'pdfs',
    'xls': 'pdfs', 'xlsx': 'pdfs', 'ppt': 'pdfs', 'pptx': 'pdfs',
    # Images
    'jpg': 'images', 'jpeg': 'images', 'png': 'images',
    'gif': 'images', 'svg': 'images', 'webp': 'images',
    # Audio
    'mp3': 'audio', 'wav': 'audio', 'ogg': 'audio', 'flac': 'audio',
    # Video
    'mp4': 'video', 'webm': 'video', 'avi': 'video', 'mov': 'video'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_domain(url_string):
    try:
        parsed_url = urlparse(url_string)
        return parsed_url.netloc
    except Exception as e:
        print("Exception, ", e.__repr__())
        return None


def extract_file_links(page_url, page_content):
    file_links = []
    base_url = page_url
    soup = BeautifulSoup(page_content, 'html.parser')

    file_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt',
                       '.mp3', '.wav', '.ogg', '.mp4', '.avi', '.mov', '.zip', '.rar']

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href:
            full_url = urljoin(base_url, href)
            path = urlparse(full_url).path.lower()
            if any(path.endswith(ext) for ext in file_extensions):
                file_links.append(full_url)

    for img in soup.find_all('img', src=True):
        src = img['src']
        if src:
            full_url = urljoin(base_url, src)
            file_links.append(full_url)

    for tag in soup.find_all(['audio', 'video']):
        if tag.has_attr('src'):
            full_url = urljoin(base_url, tag['src'])
            file_links.append(full_url)

        for source in tag.find_all('source', src=True):
            full_url = urljoin(base_url, source['src'])
            file_links.append(full_url)

    return list(set(file_links))


def get_extension(url_string, content_type=None):
    path = urlparse(url_string).path
    ext = os.path.splitext(path)[1].lower()

    if ext and len(ext) > 1:
        return ext[1:]

    if content_type:
        ext = mimetypes.guess_extension(content_type.split(';')[0].strip())
        if ext:
            return ext[1:]

        mapping = {
            'text/html': 'html',
            'application/pdf': 'pdf',
            'image/jpeg': 'jpg',
            'image/png': 'png',
            'image/gif': 'gif',
            'image/svg+xml': 'svg',
            'audio/mpeg': 'mp3',
            'audio/wav': 'wav',
            'video/mp4': 'mp4',
            'video/webm': 'webm'
        }

        for mime, extension in mapping.items():
            if mime in content_type:
                return extension

    return 'bin'


def save_file(file_path, data, is_binary=False):
    mode = 'wb' if is_binary else 'w'
    encoding = None if is_binary else 'utf-8'

    try:
        with open(file_path, mode, encoding=encoding) as f:
            f.write(data)
    except Exception as e:
        pass


def download_file(file_url, company_name, root_folder):
    try:
        response = requests.get(file_url, headers=HEADERS, stream=True, timeout=30)
        response.raise_for_status()

        content_type = response.headers.get('content-type', '')
        extension = get_extension(file_url, content_type)
        category = CATEGORIES.get(extension, 'other')

        url_obj = urlparse(file_url)
        file_name = os.path.basename(url_obj.path)
        _id = hash(file_url) % 1000000

        if not file_name or file_name == '/' or not os.path.splitext(file_name)[1]:
            file_name = f"file_{company_name}_{int(time.time())}_{_id}.{extension}"

        output_path = os.path.join(root_folder, category, file_name)

        output_path = re.sub(r'[\\/*?:"<>|]', "_", output_path)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        save_file(output_path, response.content, is_binary=True)

        return {
            'id': _id,
            'path': output_path,
            'category': category,
        }
    except Exception as e:
        return None


def load_json_files(links_dir: str):
    all_data = {}
    for file_path in glob.glob(os.path.join(links_dir, "*.json")):
        filename = os.path.basename(file_path).replace('.json', '')
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                all_data[filename] = data
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    return all_data





def handle_file(path, category, company_name, root_folder):
    content_to_save = None
    extension = None
    result = None
    converter = DocumentConverter()

    if category == 'audio':
        full_text, detailed_output = transcribe_audio(path)
        extension = 'txt'
        result = {
            'annotation': detailed_output
        }
    if category == 'html' or category == 'pdfs':
        result = converter.convert(path)
        content_to_save = result.document.export_to_markdown()
        extension = 'md'
        result = {}

    if category == 'video':
        audio_path = extract_audio_from_video(path)
        full_text, detailed_output = transcribe_audio(path)
        extension = 'txt'
        result = {
            'annotation': detailed_output
        }
        os.remove(audio_path)


    _id = hash(path) % 1000000
    file_name = f"file_{company_name}_{int(time.time())}_{_id}.{extension}"
    output_path = os.path.join(root_folder, category, file_name)
    output_path = re.sub(r'[\\/*?:"<>|]', "_", output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    save_file(output_path, content_to_save, is_binary=False)

    return result


def process_company(company, data, metadata: list):
    start_url = data['start_url'].trim()
    links = [item['link'] for item in data['cls_links'] if item['cls'] == 'useful']

    start_domain = get_domain(start_url)

    for link in links:
        link_domain = get_domain(link)

        if link_domain == start_domain:
            response = requests.get(link, headers=HEADERS, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type', '')

            if 'text/html' in content_type:
                file_links = extract_file_links(link, response.text)
                for file_link in file_links:
                    result = download_file(file_link, company, ROOT_FOLDER + '/' + 'original')
                    category = result['category']
                    path = result['path']

                    cur_meta = {
                        'original_path': path,
                        'category': category,
                    }

                    handle_file(path, category, company, ROOT_FOLDER + '/' + 'parsed')

                    metadata.append(cur_meta)
            else:
                print(f"WARNING! Page is not html - {link}")


def main():
    mimetypes.init()
    company2data = load_json_files('classified_links')

    metadata = []

    for company, data in company2data.items():
        print(company)


if __name__ == "__main__":
    main()

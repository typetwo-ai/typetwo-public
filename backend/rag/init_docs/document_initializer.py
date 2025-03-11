import os
from pathlib import Path
from typing import List, Dict, Union

import pickle
import faiss
import numpy as np
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import ImageRefMode
from langchain_text_splitters import MarkdownTextSplitter
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from backend.gc_utils import download_folder

pipeline_options = PdfPipelineOptions()
pipeline_options.images_scale = 2.0
pipeline_options.generate_page_images = True
pipeline_options.generate_picture_images = True

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

os.environ["GOOGLE_CLOUD_PROJECT"] = "project-1-450712"


def _save_faiss_index(index_data: Dict, output_path: Union[str, Path]):
    output_path = Path(output_path)

    faiss.write_index(index_data['index'], str(output_path.with_suffix('.index')))

    data_to_save = {
        'chunks': index_data['chunks'],
        'metadata': index_data['metadata'],
        'dimension': index_data['dimension']
    }

    with open(output_path.with_suffix('.pkl'), 'wb') as f:
        pickle.dump(data_to_save, f)


def _chunk_markdown(text: str,):
    markdown_splitter = MarkdownTextSplitter()
    chunks = markdown_splitter.split_text(text)
    return chunks


class DocumentsInitializer:
    def __init__(self, data_folder, model_name='microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract'):
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(parents=True, exist_ok=True)
        self.embedder = SentenceTransformer(model_name)

    def _download_pdfs(self, pdf_folder):
        download_folder('literature-resources-bucket', 'Journal of Medicinal Chemistry', self.data_folder / pdf_folder)

    def _convert_to_md(self, pdf_folder, md_folder):
        md_output_path = self.data_folder / md_folder
        md_output_path.mkdir(parents=True, exist_ok=True)

        pdf_path = self.data_folder / pdf_folder
        pdf_files = list(pdf_path.glob('**/*.pdf'))

        for pdf_file in tqdm(pdf_files, desc='Converting PDFs'):
            rel_path = pdf_file.relative_to(pdf_path)
            output_dir = md_output_path / rel_path.parent
            output_dir.mkdir(parents=True, exist_ok=True)

            base_name = pdf_file.stem
            md_file_path = output_dir / f"{base_name}.md"

            result = converter.convert(pdf_file)
            result.document.save_as_markdown(
                md_file_path,
                image_mode=ImageRefMode.REFERENCED
            )

    def _create_faiss_index(self,
                            chunks: List[str],
                            metadata: List[Dict[str, str]]) -> Dict:
        embeddings = self.embedder.encode(chunks, show_progress_bar=True)
        embeddings = np.array(embeddings).astype('float32')

        embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)

        return {
            'index': index,
            'chunks': chunks,
            'metadata': metadata,
            'dimension': dimension
        }

    def _create_vector_db(self, md_folder, db_path):
        md_path = self.data_folder / md_folder
        all_chunks = []
        all_metadata = []

        md_files = list(md_path.glob('**/*.md'))
        print(f"Found {len(md_files)} markdown files")

        for md_file in tqdm(md_files, desc='Processing markdown files'):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            file_chunks = _chunk_markdown(content)

            rel_path = md_file.relative_to(md_path)
            for i, chunk in enumerate(file_chunks):
                metadata = {
                    'text': chunk,
                    'source': str(rel_path),
                    'chunk_index': i,
                    'total_chunks': len(file_chunks)
                }
                all_metadata.append(metadata)

            all_chunks.extend(file_chunks)

        index_data = self._create_faiss_index(all_chunks, all_metadata)

        db_output_path = self.data_folder / db_path
        _save_faiss_index(index_data, db_output_path)

    def init_db(self, pdf_folder, md_folder, db_path):
        self._download_pdfs(pdf_folder)
        self._convert_to_md(pdf_folder, md_folder)
        self._create_vector_db(md_folder, db_path)

    def test_db(self, query: str, index_name, k: int = 5):
        """
        Sanity check for implementation and embedder - just put some query from the dataset to check if it will be on the first place.
        """

        index_path = self.data_folder / f'{index_name}.index'
        metadata_path = self.data_folder / f'{index_name}.pkl'

        if not index_path.exists():
            raise FileNotFoundError(f"FAISS index not found at {index_path}")

        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found at {metadata_path}")

        index = faiss.read_index(str(index_path))

        with open(metadata_path, 'rb') as f:
            data = pickle.load(f)

        chunks = data.get('chunks', [])
        metadata = data.get('metadata', [])

        query_embedding = self.embedder.encode([query])[0].reshape(1, -1).astype('float32')

        distances, indices = index.search(query_embedding, k)

        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(chunks):
                results.append((
                    chunks[idx],
                    metadata[idx],
                    float(distances[0][i])
                ))

        print(f"\nTop {len(results)} results:")
        for i, (chunk, meta, distance) in enumerate(results):
            print(f"\n[{i + 1}] Distance: {distance:.4f}")
            print(f"Source: {meta['source']} (Chunk {meta['chunk_index'] + 1}/{meta['total_chunks']})")
            print(f"Text snippet: {chunk[:150]}...")


document_initializer = DocumentsInitializer('./../data')
document_initializer.init_db(Path('./pdfs'), Path('./parsed'), Path('./preprocessed_data'))
# document_initializer.test_db("According to the SAR analysis, when the aromatic ring at the para position was substituted by fluorine, methoxy, bromine, or a benzene ring, a smaller substituent size led to stronger antiproliferative activity against MCF-7 and HepG2 cells. The substituents at the N atoms seemed to play a large role in the anticancer activities because the Rh complexes with an N1-aliphatic chain exhibited equivalent or higher antiproliferation than those with an N1-aromatic chain.", 'preprocessed_data', k=5)

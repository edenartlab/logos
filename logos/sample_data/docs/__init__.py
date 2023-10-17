import glob
from pathlib import Path

dir_path = Path(__file__).parent

def get_sample_docs():
    doc_files = glob.glob(str(dir_path / 'eden/*.md'))
    docs = []

    for doc_file in doc_files:
        with open(doc_file, 'r') as file:
            docs.append(file.read())

    return docs

from setuptools import setup, find_packages
from glob import glob

md_files = [f.split('/', 1)[1] for f in glob('logos/**/*.md', recursive=True)]
txt_files = [f.split('/', 1)[1] for f in glob('logos/**/*.txt', recursive=True)]

setup(
    name='eden-logos',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "python-dotenv", 
        "pytest",
        "pydantic>=2.0",
        "fire>=0.3.0",
        "httpx>=0.24.1",
        "python-dotenv>=1.0.0",
        "orjson>=3.9.0",
        "rich>=13.4.1",
        "python-dateutil>=2.8.2",
    ],
    package_data={'logos': md_files + txt_files}
)

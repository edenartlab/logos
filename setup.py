from setuptools import setup, find_packages
from glob import glob

md_files = [f.split('/', 1)[1] for f in glob('logos/**/*.md', recursive=True)]
txt_files = [f.split('/', 1)[1] for f in glob('logos/**/*.txt', recursive=True)]

setup(
    name='eden-logos',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['simpleaichat', 'python-dotenv', 'pytest'],
    package_data={'logos': md_files + txt_files}
)

from string import Template
from pathlib import Path

dir_path = Path(__file__).parent

with open(dir_path / 'chat.txt', 'r') as file:
    chat_template = Template(file.read())

with open(dir_path / 'creator.txt', 'r') as file:
    creator_template = Template(file.read())

with open(dir_path / 'qa.txt', 'r') as file:
    qa_template = Template(file.read())

with open(dir_path / 'router.txt', 'r') as file:
    router_template = Template(file.read())

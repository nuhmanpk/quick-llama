import pathlib
from setuptools import setup, find_packages

file = pathlib.Path(__file__).parent

README = (file / "README.md").read_text()

setup(
    name='quick-llama',
    version='0.0.8',
    description='Run Ollama models easily, anywhere – including online platforms like Google Colab',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nuhman PK',
    url='https://github.com/nuhmanpk/quick-llama',
    packages=find_packages(include=['quick_llama']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'ollama'
    ],
    project_urls={
        'Documentation': 'https://github.com/nuhmanpk/quick-llama/blob/main/README.md',
        'Funding': 'https://github.com/sponsors/nuhmanpk',
        'Source': 'https://github.com/nuhmanpk/quick-llama/',
        'Tracker': 'https://github.com/nuhmanpk/quick-llama/issues',
    },
)

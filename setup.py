from setuptools import setup, find_packages

setup(
    name='quick-llama',
    version='0.0.1',
    description='Run Ollama models on Colab easily',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nuhman PK',
    url='https://github.com/nuhmanpk/quick-llama',
    packages=find_packages(include=['quick-llama']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=[
        'ollama',
        'threading',
    ],
    project_urls={
        'Documentation': 'https://github.com/nuhmanpk/pytrycatch/blob/main/README.md',
        'Funding': 'https://github.com/sponsors/nuhmanpk',
        'Source': 'https://github.com/nuhmanpk/pytrycatch/',
        'Tracker': 'https://github.com/nuhmanpk/pytrycatch/issues',
    },
)

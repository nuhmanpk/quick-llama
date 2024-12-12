from setuptools import setup, find_packages

setup(
    name='quickllama',
    version='0.0.1',
    description='A simple and efficient way to run LLM models with multithreading support',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nuhman PK',
    url='https://github.com/nuhmanpk/quickllama',
    packages=find_packages(include=['quickllama']),
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
)

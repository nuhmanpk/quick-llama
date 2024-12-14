from setuptools import setup, find_packages

setup(
    name='ollama-manager',
    version='0.0.1',
    description='Run Ollama models on Colab easily',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Nuhman PK',
    url='https://github.com/nuhmanpk/ollama-manager',
    packages=find_packages(include=['ollama-manager']),
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

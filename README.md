# Quick Llama

[![PyPI version](https://badge.fury.io/py/quick-llama.svg)](https://badge.fury.io/py/quick-llama)
[![Downloads](https://pepy.tech/badge/quick-llama)](https://pepy.tech/project/quick-llama)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python wrapper for Ollama that simplifies managing and interacting with language models. QuickLlama automates server setup, model management, and model interaction for a seamless developer experience.

## Installtion

```py
pip install quick-llama
```

```py
from quick-llama import QuickLlama

from ollama import chat
from ollama import ChatResponse

# Defaults to mistral
quick_llama = QuickLlama(model_name="llama3.2:1b")

quick_llama.init()

response: ChatResponse = chat(model='llama3.2:1b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

quick_llama.stop_server()

```

## Use custom Models

```py
quick_llama = QuickLlama()  # Defaults to mistral
quick_llama.init()

# Custom Model
quick_llama = QuickLlama(model_name="custom-model-name")
quick_llama.init()
```
## List Models

```py
quick_llama.list_models()
```

## Stop Model
```py
quick_llama.stop_model("llama3.2:1b")
```
## Stop Server

```py
quick_llama.stop_server()
```






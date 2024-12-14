# Quick Llama

[![PyPI version](https://badge.fury.io/py/quick-llama.svg?icon=si%3Apython)](https://badge.fury.io/py/quick-llama)
[![Downloads](https://pepy.tech/badge/quick-llama)](https://pepy.tech/project/quick-llama)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python wrapper for Ollama that simplifies managing and interacting with LLMs.

<p align="center">
  <img src="https://raw.githubusercontent.com/nuhmanpk/quick-llama/main/images/llama-image.webp" width="300" height="300" />
</p>

QuickLlama automates server setup, model management, and seamless interaction with LLMs, providing an effortless developer experience.

🚀 Colab-Ready: Easily run and experiment with QuickLlama on Google Colab for hassle-free, cloud-based development!

> **Note**: Don’t forget to use a GPU if you actually want it to perform well!

## Installtion

```py
pip install quick-llama
```

```py
from quick_llama import QuickLlama

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

```py
from quick_llama import QuickLlama


from ollama import chat
from ollama import ChatResponse

# Defaults to mistral
quick_llama = QuickLlama(model_name="llama3.2:1b")

quick_llama.init()

response: ChatResponse = chat(model='llama3.2:1b', messages=[
  {
    'role': 'user',
    'content': 'what is 6 times 5?',
  },
])
print(response['message']['content'])

print(response.message.content)
```

## Use with Langchain 

```py
from quick_llama import QuickLlama
from langchain_ollama import OllamaLLM

model_name = "llama3.2:1b"

quick_llama = QuickLlama(model_name=model_name)

model = OllamaLLM(model=model_name)
model.invoke("Come up with 10 names for a song about parrots")
```

## Use custom Models

```py
quick_llama = QuickLlama()  # Defaults to mistral
quick_llama.init()

# Custom Model
# Supports all models from https://ollama.com/search
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


Made with ❤️ by [Nuhman](https://github.com/nuhmanpk). Happy Coding 🚀

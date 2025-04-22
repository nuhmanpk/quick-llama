# Quick Llama

[![PyPI version](https://badge.fury.io/py/quick-llama.svg?icon=si%3Apython)](https://badge.fury.io/py/quick-llama)
[![Downloads](https://pepy.tech/badge/quick-llama)](https://pepy.tech/project/quick-llama)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A Python wrapper for Ollama that simplifies managing and interacting with LLMs on colab with multi model and reasoning model support.

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

### Serve a model
```py
from quick_llama import QuickLlama
model = 'gemma3'
quick_llama = QuickLlama(model_name=model,verbose=True)

quick_llama.init()
```

```py
from quick_llama import QuickLlama

from ollama import chat
from ollama import ChatResponse

# Defaults to gemma3
model = 'gemma3'
quick_llama = QuickLlama(model_name=model,verbose=True)

quick_llama.init()

response: ChatResponse = chat(model=model, messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

quick_llama.stop()

```

## MultiModels
```py
import requests
import os
from ollama import chat
from quick_llama import QuickLlama

model = 'gemma3'
quick_llama = QuickLlama(model_name=model,verbose=True)

quick_llama.init()

# Step 1: Download the image
img_url = "https://raw.githubusercontent.com/nuhmanpk/quick-llama/main/images/llama-image.webp" # quick llama cover photo
img_path = "temp_llama_image.webp"

with open(img_path, "wb") as f:
    f.write(requests.get(img_url).content)

# Step 2: Send the image to the model
response = chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": "Describe what you see in this photo.",
            "images": [img_path],
        }
    ]
)

# Step 3: Print the result
print(response['message']['content'])

# Step 4: Clean up the image file
os.remove(img_path)

```


```py
from quick_llama import QuickLlama


from ollama import chat
from ollama import ChatResponse

# Defaults to gemma3
quick_llama = QuickLlama(model_name="gemma3")

quick_llama.init()

response: ChatResponse = chat(model='gemma3', messages=[
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

model_name = "gemma3"

quick_llama = QuickLlama(model_name=model_name,verbose=True)

quick_llama.init()

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
quick_llama.stop_model("gemma3")
```
## Stop Server

```py
quick_llama.stop()
```


Made with ❤️ by [Nuhman](https://github.com/nuhmanpk). Happy Coding 🚀

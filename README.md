# Ollama Manager

A Python wrapper for Ollama that simplifies managing and interacting with language models. OllamaManager automates server setup, model management, and model interaction for a seamless developer experience.

## Installtion

```py
pip install ollama-manager
```

```py
from ollama-manager import OllamaManager

from ollama import chat
from ollama import ChatResponse

# Defaults to mistral
manager = OllamaManager(model_name="llama3.2:1b")

manager.init()

response: ChatResponse = chat(model='llama3.2:1b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

manager.stop_server()

```

## Use custom Models

```py
manager = OllamaManager()  # Defaults to mistral
manager.init()

# Custom Model
manager = OllamaManager(model_name="custom-model-name")
manager.init()
```


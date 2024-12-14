# quickllama

```py

from ollama-manager import OllamaManager

manager = OllamaManager()

manager.init()
manager.pull_model("mistral")
manager.run_model("mistral")
manager.list_models()
manager.list_running_models()
manager.stop_model("mistral")
manager.remove_model("mistral")
manager.stop_server()
```

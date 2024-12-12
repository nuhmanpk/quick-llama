# quickllama

```py
manager.queue_command("start")  # Start the server

manager.queue_command("pull", "mistral")  # Pull the mistral model

manager.queue_command("run", "mistral")  # Run the mistral model

manager.queue_command("list")  # List all models

manager.queue_command("ps")  # List running models

manager.queue_command("stop_model", "mistral")  # Stop the mistral model

manager.queue_command("rm", "mistral")  # Remove the mistral model

manager.queue_command("stop")
```

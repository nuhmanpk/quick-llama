import subprocess
import platform
import threading
import queue
import os
import signal
import time


class OllamaManager:
    def __init__(self):
        self.server_process = None
        self.command_queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self.process_commands, daemon=True)
        self.worker_thread.start()

    def check_and_install_ollama(self):
        """Check if ollama is installed; if not, install it."""
        try:
            result = subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Ollama is already installed. Version: {result.stdout.decode().strip()}")
        except FileNotFoundError:
            print("Ollama is not installed. Attempting installation...")
            system_type = platform.system()
            if system_type == "Linux":
                try:
                    subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", check=True, shell=True)
                    print("Ollama installation completed successfully.")
                except subprocess.CalledProcessError as e:
                    print(f"Installation failed with error: {e}")
            else:
                print(f"Unsupported operating system: {system_type}")

    def start_server(self):
        """Start the Ollama server."""
        if self.server_process:
            print("Server is already running.")
            return
        print("Starting Ollama server...")
        self.server_process = subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Ollama server started.")

    def stop_server(self):
        """Stop the Ollama server."""
        if self.server_process:
            print("Stopping Ollama server...")
            os.kill(self.server_process.pid, signal.SIGTERM)
            self.server_process.wait()
            self.server_process = None
            print("Ollama server stopped.")

    def run_model(self, model_name):
        """Run a specified model."""
        print(f"Running model: {model_name}")
        try:
            subprocess.run(["ollama", "run", model_name], check=True)
            print(f"Model '{model_name}' executed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error running model '{model_name}': {e}")

    def pull_model(self, model_name):
        """Pull a model from the registry."""
        print(f"Pulling model: {model_name}")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"Model '{model_name}' pulled successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error pulling model '{model_name}': {e}")

    def list_models(self):
        """List all available models."""
        print("Listing available models:")
        try:
            result = subprocess.run(["ollama", "list"], check=True, stdout=subprocess.PIPE)
            print(result.stdout.decode().strip())
        except subprocess.CalledProcessError as e:
            print(f"Error listing models: {e}")

    def list_running_models(self):
        """List all running models."""
        print("Listing running models:")
        try:
            result = subprocess.run(["ollama", "ps"], check=True, stdout=subprocess.PIPE)
            print(result.stdout.decode().strip())
        except subprocess.CalledProcessError as e:
            print(f"Error listing running models: {e}")

    def stop_model(self, model_name):
        """Stop a specific running model."""
        print(f"Stopping model: {model_name}")
        try:
            subprocess.run(["ollama", "stop", model_name], check=True)
            print(f"Model '{model_name}' stopped successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping model '{model_name}': {e}")

    def remove_model(self, model_name):
        """Remove a model."""
        print(f"Removing model: {model_name}")
        try:
            subprocess.run(["ollama", "rm", model_name], check=True)
            print(f"Model '{model_name}' removed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error removing model '{model_name}': {e}")

    def process_commands(self):
        """Process queued commands sequentially."""
        while True:
            command, args = self.command_queue.get()
            if command == "start":
                self.start_server()
            elif command == "stop":
                self.stop_server()
            elif command == "run":
                self.run_model(args)
            elif command == "pull":
                self.pull_model(args)
            elif command == "list":
                self.list_models()
            elif command == "ps":
                self.list_running_models()
            elif command == "stop_model":
                self.stop_model(args)
            elif command == "rm":
                self.remove_model(args)
            else:
                print(f"Unknown command: {command}")
            self.command_queue.task_done()

    def queue_command(self, command, args=None):
        """Queue a command for execution."""
        print(f"Queuing command: {command} {args if args else ''}")
        self.command_queue.put((command, args))

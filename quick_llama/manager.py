import subprocess
import platform
import os
import signal
import threading

class QuickLlama:
    def __init__(self, model_name="mistral"):
        self.server_process = None
        self.model_name = model_name

    def init(self):
        """Initialize Ollama, start the server, pull the model, and run it."""
        print(f"🌟 Initializing QuickLlama with model '{self.model_name}'...")
        
        if not self.is_ollama_installed():
            self.install_ollama()
        
        # Start the server in a separate thread
        server_thread = threading.Thread(target=self.start_server, daemon=True)
        server_thread.start()
        
        # Wait for the server to start (this is a simple way to wait for the server to be ready)
        print("⚡ Waiting for the server to be ready...")
        server_thread.join()  # Wait for the server to be fully up
        
        # Pull and run the model in a separate thread
        model_thread = threading.Thread(target=self.run_model, args=(self.model_name,), daemon=True)
        model_thread.start()
        model_thread.join()  # Wait for the model to finish running

    def is_ollama_installed(self):
        """Check if Ollama is installed."""
        print("🔍 Checking if Ollama is installed...")
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Ollama is installed.")
            return True
        except FileNotFoundError:
            print("❌ Ollama is not installed.")
            return False

    def install_ollama(self):
        """Install Ollama."""
        print("🚀 Installing Ollama...")
        system_type = platform.system()
        if system_type == "Linux":
            try:
                subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", check=True, shell=True)
                print("✅ Ollama installation completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Installation failed: {e}")
                raise RuntimeError("Ollama installation failed.")
        else:
            raise RuntimeError(f"Unsupported operating system: {system_type}")

    def start_server(self):
        """Start the Ollama server."""
        if self.server_process:
            print("⚠️ Server is already running.")
            return
        print("🚀 Starting Ollama server...")
        self.server_process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        threading.Thread(target=self.stream_output, args=(self.server_process,), daemon=True).start()
        print("✅ Ollama server started and running.")

    def stop_server(self):
        """Stop the Ollama server."""
        if self.server_process:
            print("🛑 Stopping Ollama server...")
            os.kill(self.server_process.pid, signal.SIGTERM)
            self.server_process.wait()
            self.server_process = None
            print("✅ Ollama server stopped.")
        else:
            print("⚠️ No server is running.")

    def run_command(self, command):
        """Run an Ollama command with real-time output."""
        print(f"🔧 Executing command: {' '.join(command)}")
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.stream_output(process)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing command '{' '.join(command)}': {e}")

    def pull_model(self, model_name):
        """Pull a model."""
        print(f"📥 Pulling model: {model_name}...")
        self.run_command(["ollama", "pull", model_name])
        print(f"✅ Model '{model_name}' pulled successfully.")

    def run_model(self, model_name):
        """Run a model."""
        print(f"🏃 Running model: {model_name}...")
        self.pull_model(model_name)
        self.run_command(["ollama", "run", model_name])
        print(f"✅ Model '{model_name}' is running.")

    def list_models(self):
        """List all available models."""
        print("📋 Listing available models...")
        self.run_command(["ollama", "list"])

    def list_running_models(self):
        """List all running models."""
        print("📋 Listing running models...")
        self.run_command(["ollama", "ps"])

    def stop_model(self, model_name):
        """Stop a running model."""
        print(f"🛑 Stopping model: {model_name}...")
        self.run_command(["ollama", "stop", model_name])
        print(f"✅ Model '{model_name}' stopped.")

    def remove_model(self, model_name):
        """Remove a model."""
        print(f"🗑️ Removing model: {model_name}...")
        self.run_command(["ollama", "rm", model_name])
        print(f"✅ Model '{model_name}' removed successfully.")

    @staticmethod
    def stream_output(process):
        """Stream the output of a subprocess in real-time."""
        for line in process.stdout:
            print(line.strip())
        for line in process.stderr:
            print(f"⚠️ {line.strip()}")


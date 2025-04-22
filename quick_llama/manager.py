import subprocess
import threading
import time
import requests
from queue import Queue

class QuickLlama:
    def __init__(self, model_name="mistral", verbose=True):
        self.model_name = model_name
        self.verbose = verbose
        self.server_proc = None

    def init(self):
        if self.verbose:
            print(f"🌟 Initializing QuickLlama with model '{self.model_name}'...")
        if not self._ollama_installed():
            self._install_ollama()
        self._start_server()
        self._wait_for_server()
        self._pull_model(self.model_name)
        if self.verbose:
            print("✅ QuickLlama is ready!")

    def _ollama_installed(self):
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def _install_ollama(self):
        if self.verbose:
            print("🚀 Installing Ollama...")
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)

    def _start_server(self):
        if self.verbose:
            print("🚀 Starting Ollama server in background...")
        # Launch without wait
        self.server_proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1
        )
        threading.Thread(target=self._stream_logs, daemon=True).start()

    def _wait_for_server(self, timeout=60):
        if self.verbose:
            print("⚡ Waiting for Ollama server to be ready...")
        start = time.time()
        url = "http://localhost:11434/api/generate"
        while time.time() - start < timeout:
            try:
                r = requests.get(url)
                if r.status_code in (200, 405):
                    if self.verbose:
                        print("✅ Ollama server is ready!")
                    return
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
        raise RuntimeError("Ollama server did not become ready in time")

    def _pull_model(self, model_name):
        if self.verbose:
            print(f"📥 Pulling model '{model_name}'...")
        subprocess.run(["ollama", "pull", model_name], check=True)
        if self.verbose:
            print(f"✅ Model '{model_name}' pulled.")

    def _stream_logs(self):
        q = Queue()
        def _enqueue(pipe):
            for line in iter(pipe.readline, ""):
                q.put(line)
            pipe.close()
        threading.Thread(target=_enqueue, args=(self.server_proc.stdout,), daemon=True).start()
        threading.Thread(target=_enqueue, args=(self.server_proc.stderr,), daemon=True).start()
        while True:
            try:
                line = q.get(timeout=0.1)
                print(line, end="")
            except:
                if self.server_proc.poll() is not None:
                    break

    def stop(self):
        if self.server_proc:
            if self.verbose:
                print("🛑 Stopping Ollama server...")
            self.server_proc.terminate()
            self.server_proc.wait()
            if self.verbose:
                print("✅ Ollama server stopped.")

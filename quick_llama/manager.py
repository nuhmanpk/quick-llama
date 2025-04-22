import subprocess
import threading
import time
import requests
from queue import Queue


class QuickLlama:
    """
    QuickLlama manages an Ollama server running locally (e.g., in Colab),
    streams its logs, waits for it to become healthy, and pulls the specified model.
    """

    def __init__(self, model_name: str = "gemma3", verbose: bool = True):
        self.model_name = model_name
        self.verbose = verbose
        self.server_proc = None

    def init(self):
        """Install Ollama (if needed), start the server, wait for readiness, and pull the model."""
        if self.verbose:
            print(f"🌟 Initializing QuickLlama with model '{self.model_name}'...")

        if not self._ollama_installed():
            self._install_ollama()

        self._start_server()
        self._wait_for_server(timeout=60)
        self._pull_model(self.model_name)

        if self.verbose:
            print("✅ QuickLlama is ready!")

    def stop(self):
        """Terminate the Ollama server."""
        if self.server_proc:
            if self.verbose:
                print("🛑 Stopping Ollama server...")
            self.server_proc.terminate()
            self.server_proc.wait()
            if self.verbose:
                print("✅ Ollama server stopped.")
            self.server_proc = None
        elif self.verbose:
            print("⚠️ No Ollama server running to stop.")

    # ─── Internal Helpers ────────────────────────────────────────────────────────

    def _ollama_installed(self) -> bool:
        """Returns True if the `ollama` CLI is on PATH."""
        try:
            subprocess.run(
                ["ollama", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            if self.verbose:
                print("🔍 Ollama CLI found.")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            if self.verbose:
                print("🔍 Ollama CLI not found.")
            return False

    def _install_ollama(self):
        """Installs Ollama via the official install script."""
        if self.verbose:
            print("🚀 Installing Ollama CLI...")
        subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            check=True,
        )
        if self.verbose:
            print("✅ Ollama CLI installed.")

    def _start_server(self):
        """Launches `ollama serve` in the background and starts log streaming."""
        if self.verbose:
            print("🚀 Starting Ollama server in background...")
        self.server_proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        threading.Thread(target=self._stream_logs, daemon=True).start()

    def _wait_for_server(self, timeout: int = 60):
        """
        Polls GET /api/version until it returns 200, or raises RuntimeError on timeout.
        """
        if self.verbose:
            print("⚡ Waiting for Ollama server to be ready...")
        url = "http://127.0.0.1:11434/api/version"
        start = time.time()

        while time.time() - start < timeout:
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    version = resp.json().get("version", "<unknown>")
                    if self.verbose:
                        print(f"✅ Ollama server ready (version {version})")
                    return
            except requests.RequestException:
                pass

            time.sleep(1)

        raise RuntimeError("Ollama server did not become ready in time")

    def _pull_model(self, model_name: str):
        """Pulls the requested model so it's available for inference."""
        if self.verbose:
            print(f"📥 Pulling model '{model_name}'...")
        subprocess.run(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        if self.verbose:
            print(f"✅ Model '{model_name}' pulled.")

    def _stream_logs(self):
        """Reads both stdout and stderr from the server process and prints lines live."""
        q: Queue = Queue()

        def enqueue(pipe):
            for line in iter(pipe.readline, ""):
                q.put(line)
            pipe.close()

        # Start reader threads for stdout and stderr
        threading.Thread(target=enqueue, args=(self.server_proc.stdout,), daemon=True).start()
        threading.Thread(target=enqueue, args=(self.server_proc.stderr,), daemon=True).start()

        # Drain the queue until the process exits
        while True:
            try:
                line = q.get(timeout=0.1)
                print(line, end="")
            except Exception:
                if self.server_proc.poll() is not None:
                    break

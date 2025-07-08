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
        if self.verbose:
            print("🌟 Starting initialization of QuickLlama...")
        if not self._ollama_installed():
            if self.verbose:
                print("ℹ️  Need to install Ollama — kicking off installer now.")
            self._install_ollama()
        else:
            if self.verbose:
                print("✅ Ollama CLI is already installed; skipping installer.")

        if self.verbose:
            print("🚀 Launching Ollama server...")
        self._start_server()

        if self.verbose:
            print("⌛ Waiting for Ollama server to respond to health checks...")
        self._wait_for_server(timeout=60)

        if self.verbose:
            print(f"📥 Ensuring model '{self.model_name}' is present locally...")
        self._pull_model(self.model_name)

        if self.verbose:
            print("🎉 QuickLlama setup complete and ready to use!")

    def stop(self):
        if self.server_proc:
            if self.verbose:
                print("🛑 Sending shutdown signal to Ollama server...")
            self.server_proc.terminate()
            self.server_proc.wait()
            if self.verbose:
                print("✅ Ollama server has shut down cleanly.")
            self.server_proc = None
        elif self.verbose:
            print("⚠️  No running Ollama server found; nothing to stop.")

    def _ollama_installed(self) -> bool:
        try:
            subprocess.run(
                ["ollama", "--version"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            if self.verbose:
                print("🔍 Ollama CLI check passed.")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            if self.verbose:
                print("🔍 Ollama CLI check failed.")
            return False

    def _install_ollama(self):
        if self.verbose:
            print("🚧 Installing Ollama CLI (this may take a minute)...")
        subprocess.run(
            "curl -fsSL https://ollama.com/install.sh | sh",
            shell=True,
            check=True,
        )
        if self.verbose:
            print("✅ Installation of Ollama CLI finished.")

    def _start_server(self):
        if self.verbose:
            print("🔄 Starting `ollama serve` in the background now.")
        self.server_proc = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        threading.Thread(target=self._stream_logs, daemon=True).start()
        if self.verbose:
            print("🔍 Log streaming thread launched.")

    def _wait_for_server(self, timeout: int = 60):
        url = "http://127.0.0.1:11434/api/version"
        start = time.time()
        while time.time() - start < timeout:
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    version = resp.json().get("version", "<unknown>")
                    if self.verbose:
                        print(f"✅ Ollama server healthy (version {version}).")
                    return
            except requests.RequestException:
                pass
            if self.verbose:
                print("…still waiting for server to become healthy…")
            time.sleep(1)
        raise RuntimeError("Ollama server did not become ready in time")

    def _pull_model(self, model_name: str):
        if self.verbose:
            print(f"🔄 Pulling model '{model_name}'—this may take a while if not yet cached.")
        subprocess.run(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        if self.verbose:
            print(f"✅ Model '{model_name}' is now available locally.")

    def _stream_logs(self):
        q: Queue = Queue()

        def enqueue(pipe):
            for line in iter(pipe.readline, ""):
                q.put(line)
            pipe.close()

        threading.Thread(target=enqueue, args=(self.server_proc.stdout,), daemon=True).start()
        threading.Thread(target=enqueue, args=(self.server_proc.stderr,), daemon=True).start()

        while True:
            try:
                line = q.get(timeout=0.1)
                print(f"[ollama] {line}", end="")
            except Exception:
                if self.server_proc.poll() is not None:
                    break

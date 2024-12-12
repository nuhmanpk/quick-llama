import subprocess
import platform

def install_ollama():
    system_type = platform.system()

    if system_type == "Linux":  # Linux
        subprocess.run(["curl", "https://ollama.ai/install.sh", "|", "sh"])
    else:
        raise Exception(f"Unsupported operating system: {system_type}")
    print("Ollama installation completed.")

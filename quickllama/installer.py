import subprocess
import platform

def install_ollama():
    system_type = platform.system()

    if system_type == "Darwin":  # macOS
        subprocess.run(["curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"])
    elif system_type == "Linux":  # Linux
        subprocess.run(["curl", "https://ollama.ai/install.sh", "|", "sh"])
    elif system_type == "Windows":  # Windows
        subprocess.run(["Invoke-WebRequest", "-Uri", "https://ollama.ai/windows-installer", "-OutFile", "ollama-installer.exe"])
        subprocess.run(["./ollama-installer.exe", "/silent"])
    else:
        raise Exception(f"Unsupported operating system: {system_type}")
    print("Ollama installation completed.")

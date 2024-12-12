import subprocess
import threading
import time


def start_ollama_service():
    print("Starting Ollama service...")
    subprocess.run(["ollama", "start"])
    print("Ollama service started.")


def stop_ollama_service():
    print("Stopping Ollama service...")
    subprocess.run(["ollama", "stop"])
    print("Ollama service stopped.")


def query_model(prompt):
    response = subprocess.run(
        ["ollama", "run", "llama3", "--prompt", prompt], 
        capture_output=True, text=True
    )
    print(f"Response: {response.stdout}")

# Function to run queries in parallel
def run_queries_parallel(prompts):
    threads = []
    for prompt in prompts:
        thread = threading.Thread(target=query_model, args=(prompt,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# Start the service and run queries in parallel
def run():
    start_ollama_service()
    
    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity.",
        "Who won the World Series in 2023?"
    ]
    run_queries_parallel(prompts)

    stop_ollama_service()

# Entry point
if __name__ == "__main__":
    run()

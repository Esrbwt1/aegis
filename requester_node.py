import requests
import json

LEDGER_URL = "http://127.0.0.1:9000"

def main():
    print("--- Aegis Requester Node (Multi-Task Aware) ---")
    
    # Define the task we want to run
    task_type_needed = "python_script_runner"
    task_payload = {
        "script_name": "data_analyzer.py"
    }
    
    print(f"\nAttempting to find a provider for task type: '{task_type_needed}'")

    # 1. Discover a suitable provider from the Ledger
    try:
        response = requests.get(f"{LEDGER_URL}/list-providers")
        response.raise_for_status()
        all_providers = response.json()
        
        if not all_providers:
            print("!!! No active providers found on the network. Exiting.")
            return

        print(f"Found {len(all_providers)} total provider(s). Searching for one that supports our task...")
        
        suitable_providers = [
            p for p in all_providers if task_type_needed in p.get("supported_tasks", [])
        ]

        if not suitable_providers:
            print(f"!!! No provider found that can handle the task '{task_type_needed}'. Exiting.")
            return

        # For now, select the first suitable provider
        provider_to_use = suitable_providers[0]
        provider_address = provider_to_use['address']
        print(f"\nFound suitable provider at {provider_address}")

    except requests.exceptions.RequestException as e:
        print(f"\nError connecting to Ledger Server: {e}")
        return

    # 2. Structure the request for the generic endpoint and send it
    request_payload = {
        "task_type": task_type_needed,
        "payload": task_payload
    }
    
    print(f"Sending task to provider...")
    print(json.dumps(request_payload, indent=2))
    
    try:
        task_response = requests.post(f"{provider_address}/execute-task", json=request_payload)
        task_response.raise_for_status()
        print("\nTask sent successfully. Provider responded:")
        print(json.dumps(task_response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"\nError sending task to provider: {e}")
        if e.response:
            print(f"Server response: {e.response.text}")

if __name__ == "__main__":
    main()
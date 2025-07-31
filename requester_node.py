import requests
import json

PROVIDER_URL = "http://127.0.0.1:8000"

def main():
    print("--- Aegis Requester Node (Render Task) ---")
    print(f"Connecting to Provider at {PROVIDER_URL}")

    # 1. Check Provider Status
    try:
        response = requests.get(PROVIDER_URL)
        response.raise_for_status()
        print("Connection successful. Provider status:")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"\nError connecting: {e}")
        return

    # 2. Define and Send a Render Task
    render_task_payload = {
        "blend_file": "scene.blend",
        "output_image": "render_output.png"
    }
    
    print(f"\nSending render task for '{render_task_payload['blend_file']}'...")
    
    try:
        task_response = requests.post(f"{PROVIDER_URL}/execute-render", json=render_task_payload)
        task_response.raise_for_status()
        print("Task sent. Provider responded:")
        print(json.dumps(task_response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"\nError sending task: {e}")
        # If the response has content, print it for more detail
        if e.response:
            print(f"Server response: {e.response.text}")

if __name__ == "__main__":
    main()
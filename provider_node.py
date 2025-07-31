# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import os
import requests
import atexit
import sys # <-- IMPORT SYS TO FIND THE CORRECT PYTHON
from typing import Dict, Any, Callable

# --- Configuration ---
LEDGER_URL = "http://127.0.0.1:9000"
MY_ADDRESS = "http://127.0.0.1:8000"
# Get the absolute path to the python executable in our current venv
PYTHON_EXECUTABLE = sys.executable

# --- Task-Specific Logic ---
def execute_blender_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    # (This function remains unchanged)
    print("Executing Blender task...")
    blend_file = payload.get("blend_file")
    output_image = payload.get("output_image")
    frame_number = payload.get("frame_number", 1)
    if not all([blend_file, output_image]):
        raise ValueError("Missing 'blend_file' or 'output_image' in payload.")
    blend_file_path = os.path.abspath(blend_file)
    output_prefix = os.path.abspath(os.path.splitext(output_image)[0])
    final_output_filename = os.path.abspath(output_image)
    command = ["blender", "-b", blend_file_path, "-o", f"{output_prefix}####.png", "-f", str(frame_number)]
    process = subprocess.run(command, check=True, capture_output=True, text=True)
    blender_output_filename = f"{output_prefix}{str(frame_number).zfill(4)}.png"
    if os.path.exists(blender_output_filename):
        if os.path.exists(final_output_filename):
            os.remove(final_output_filename)
        os.rename(blender_output_filename, final_output_filename)
        return {"status": "Success", "detail": f"Render complete. Output saved to {output_image}"}
    else:
        raise FileNotFoundError(f"Blender process finished but expected output file was not found: {blender_output_filename}")

def execute_python_task(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a specific, whitelisted Python script using the project's venv Python interpreter.
    """
    print("Executing Python script task...")
    script_name = payload.get("script_name")
    if not script_name:
        raise ValueError("Missing 'script_name' in payload.")
    if script_name != "data_analyzer.py":
        raise ValueError(f"Script '{script_name}' is not in the approved whitelist.")
    
    # --- HARDENED COMMAND ---
    # Use the specific Python executable from our virtual environment
    command = [PYTHON_EXECUTABLE, script_name]
    print(f"Executing command: {' '.join(command)}")
    
    try:
        # Execute the script
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        output_file = "analysis_results.txt" 
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                results_content = f.read()
            return {"status": "Success", "detail": f"Script '{script_name}' executed successfully.", "results": results_content}
        else:
            raise FileNotFoundError(f"Script finished but expected output '{output_file}' was not found.")
    
    # --- HARDENED ERROR REPORTING ---
    except subprocess.CalledProcessError as e:
        # If the script fails, capture its error output (stderr) for detailed debugging
        error_message = f"Script '{script_name}' failed with exit code {e.returncode}."
        error_log = e.stderr.strip()
        print(f"!!! SUBPROCESS ERROR: {error_log}")
        raise RuntimeError(f"{error_message} Log: {error_log}")
    
# --- Task Catalog ---
TASK_CATALOG: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "blender_render": execute_blender_task,
    "python_script_runner": execute_python_task
}

# (The rest of the file remains exactly the same)
# --- Data Models, App instance, Network Registration, Endpoints etc. ---
class TaskRequest(BaseModel):
    task_type: str
    payload: Dict[str, Any]
app = FastAPI()
def register_with_ledger():
    print(f"Registering with Ledger at {LEDGER_URL}...")
    try:
        payload = {"address": MY_ADDRESS, "supported_tasks": list(TASK_CATALOG.keys())}
        response = requests.post(f"{LEDGER_URL}/register", json=payload)
        response.raise_for_status()
        print(f"Registration successful. Advertising tasks: {list(TASK_CATALOG.keys())}")
    except requests.exceptions.RequestException as e:
        print(f"!!! CRITICAL: Could not register with Ledger: {e}")
def deregister_from_ledger():
    print(f"\nDeregistering from Ledger...")
    try:
        payload = {"address": MY_ADDRESS, "supported_tasks": []}
        requests.post(f"{LEDGER_URL}/deregister", json=payload)
        print("Deregistration successful.")
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not deregister from Ledger: {e}")
@app.on_event("startup")
def on_startup():
    register_with_ledger()
atexit.register(deregister_from_ledger)
@app.post("/execute-task")
def execute_task(task_request: TaskRequest):
    task_type = task_request.task_type
    print(f"Received request for task of type: '{task_type}'")
    if task_type not in TASK_CATALOG:
        raise HTTPException(status_code=400, detail=f"Task type '{task_type}' not supported by this provider.")
    executor_function = TASK_CATALOG[task_type]
    try:
        result = executor_function(task_request.payload)
        return result
    except Exception as e:
        print(f"!!! ERROR executing task '{task_type}': {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/")
def get_status():
    return {"status": "Aegis Provider Node: Online and Multi-Task Ready", "address": MY_ADDRESS, "supported_tasks": list(TASK_CATALOG.keys())}
# Import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess # To execute external commands (like Blender)
import os         # To interact with the operating system
import re         # To perform regular expression searches

# --- Data Model Definition ---
class RenderTask(BaseModel):
    blend_file: str
    output_image: str
    frame_number: int = 1 # Add frame number to our task definition

# --- Aegis Provider Node Application ---
app = FastAPI()

# --- API Endpoints ---
@app.get("/")
def get_status():
    """Root endpoint to check if the Provider Node is online."""
    return {"status": "Aegis Provider Node: Online and Render-Ready", "version": "0.0.3-alpha"}

@app.post("/execute-render")
def execute_render(task: RenderTask):
    """
    Receives a render task, executes it, finds the output file,
    renames it to the requested name, and returns the status.
    """
    print(f"Received render task for file: {task.blend_file} at frame {task.frame_number}")
    
    if "/" in task.blend_file or "\\" in task.blend_file or ".." in task.blend_file:
        return {"status": "Error", "detail": "Invalid file path."}

    blend_file_path = os.path.abspath(task.blend_file)
    # We define the output prefix, not the full name, for the blender command
    output_prefix = os.path.abspath(os.path.splitext(task.output_image)[0])

    if not os.path.exists(blend_file_path):
        return {"status": "Error", "detail": f"Blend file '{task.blend_file}' not found."}
        
    command = [
        "blender",
        "-b",
        blend_file_path,
        "-o",
        f"{output_prefix}####.png", # Use Blender's frame padding placeholder
        "-f",
        str(task.frame_number)
    ]

    print(f"Executing command: {' '.join(command)}")

    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Blender process finished successfully.")
        
        # --- NEW CALIBRATED VERIFICATION LOGIC ---
        # Construct the filename Blender would have created (e.g., "render_output0001.png")
        blender_output_filename = f"{output_prefix}{str(task.frame_number).zfill(4)}.png"
        final_output_filename = os.path.abspath(task.output_image)

        if os.path.exists(blender_output_filename):
            print(f"Verified Blender output file found: {blender_output_filename}")
            # Rename the file to the user-requested simple name
            os.rename(blender_output_filename, final_output_filename)
            print(f"Renamed file to: {final_output_filename}")
            return {
                "status": "Success",
                "detail": f"Render complete. Output saved to {task.output_image}"
            }
        else:
             print(f"Error: Could not find expected output file: {blender_output_filename}")
             return {
                "status": "Error",
                "detail": "Blender process finished but expected output file was not found."
            }

    except FileNotFoundError:
        return {"status": "Error", "detail": "Blender is not installed or not in the system's PATH."}
    except subprocess.CalledProcessError as e:
        return {"status": "Error", "detail": "Blender process failed.", "log": e.stderr}
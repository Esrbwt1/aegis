# Import necessary libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# --- Data Model Definitions ---
class ProviderInfo(BaseModel):
    # The network address of the provider (e.g., http://127.0.0.1:8000)
    address: str 
    # A list of task types this provider can execute (e.g., ["blender_render", "protein_folding"])
    supported_tasks: List[str]

# --- In-Memory Database ---
# The key is the provider's address, the value is the ProviderInfo object.
active_providers: Dict[str, ProviderInfo] = {}

# --- Aegis Ledger Server Application ---
app = FastAPI()

# --- API Endpoints ---
@app.get("/")
def get_ledger_status():
    """Root endpoint to check if the Ledger Server is online."""
    return {"status": "Aegis Ledger Server: Online", "version": "0.1.0-alpha", "active_providers_count": len(active_providers)}

@app.post("/register")
def register_provider(provider_info: ProviderInfo):
    """A Provider Node calls this endpoint to register itself as online."""
    addr = provider_info.address
    if addr in active_providers:
        print(f"Provider at {addr} re-registered. Updating supported tasks to {provider_info.supported_tasks}.")
    else:
        print(f"New Provider registered: {addr} with tasks {provider_info.supported_tasks}.")
    
    active_providers[addr] = provider_info
    return {"status": "Registration Successful", "registered_provider": addr}

@app.get("/list-providers", response_model=List[ProviderInfo])
def list_providers():
    """A Requester Node calls this endpoint to get a list of all active providers."""
    print(f"Requester asked for provider list. Returning {len(active_providers)} providers.")
    return list(active_providers.values())

@app.post("/deregister")
def deregister_provider(provider_info: ProviderInfo):
    """A Provider Node can call this to gracefully remove itself from the list."""
    # This endpoint now only needs the address, but we keep the model for consistency.
    addr = provider_info.address
    if addr in active_providers:
        print(f"Deregistering provider: {addr}")
        del active_providers[addr]
        return {"status": "Deregistration Successful"}
    else:
        return {"status": "Provider was not registered"}
# Aegis Protocol - Alpha v0.1.0

**A decentralized, extensible trust layer for the future of AI and Scientific Compute.**

[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://shields.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

Aegis is an open-source protocol building a secure, transparent, and globally accessible marketplace for computation. Our **Alpha Protocol** demonstrates a working, multi-task network capable of discovering and executing distinct computational jobs on a decentralized network of providers.

This repository contains the official Python implementation, featuring a **Ledger Server** for discovery, a multi-task **Provider Node**, and a task-aware **Requester Node**.

For a full overview of the project's vision, architecture, and roadmap, please read our **[Aegis Whitepaper](./docs/Aegis_Whitepaper_v0.1.md)**.

## Current Capabilities: Multi-Task Alpha

The current implementation supports a catalog of distinct computational tasks. A provider can advertise which tasks it can perform, and a requester can find a suitable provider for its specific needs.

**Currently Supported Tasks:**
*   `blender_render`: Renders a 3D scene using Blender's command-line interface.
*   `python_script_runner`: Executes a whitelisted Python script for data analysis (e.g., using `numpy`).

### How to Run the Full Stack

1.  **Prerequisites:** Python 3.8+, Blender, Git.
2.  **Clone the repository:** `git clone https://github.com/Esrbwt1/aegis.git`
3.  **Set up the environment:**
    ```bash
    cd aegis
    python3 -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt 
    ```
4.  **In Terminal 1, run the Ledger Server:**
    ```bash
    uvicorn ledger_server:app --port 9000
    ```
5.  **In Terminal 2, run the Provider Node:**
    ```bash
    uvicorn provider_node:app --reload
    ```
6.  **In Terminal 3, run the Requester Node:**
    *   *(To run the Python analysis, no changes are needed in `requester_node.py`)*
    *   *(To run the Blender render, edit `requester_node.py` to request the `blender_render` task type)*
    ```bash
    python requester_node.py
    ```

## Roadmap

-   [x] **Phase 0: Toy Protocol & Whitepaper** (Complete)
-   [x] **Phase 1a: Alpha Protocol Development** (Complete)
-   [ ] **Phase 1b: Scientific Computing Beachhead:** Onboard first test users from university labs.
-   [ ] **Phase 2: Developer SDK & XAI Protocol.**
-   [ ] **Phase 3: Full Decentralization & DAO Launch.**

## Contributing

Aegis is in active alpha development. We are seeking collaborators, scientific partners, and community feedback. If you have a computational workload and are interested in testing the network, or are a developer passionate about building the future of decentralized compute, please open an issue or reach out.
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

### How to Run the Demonstration

We have created simple scripts to automate the launch of the entire network stack.

1.  **Prerequisites:** Python 3.8+, Blender, Git.
2.  **Clone the repository:** `git clone https://github.com/Esrbwt1/aegis.git`
3.  **Set up the environment (only needs to be done once):**
    ```bash
    cd aegis
    python3 -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt 
    ```
4.  **Launch the Network:**
    *   Navigate to the `scripts` folder.
    *   On Windows, double-click `run_aegis_windows.bat`.
    *   *(On macOS/Linux, run `chmod +x run_aegis_linux_macos.sh` then `./run_aegis_linux_macos.sh`)*
5.  **Observe:** Three terminal windows will open, launching the Ledger, Provider, and Requester in sequence.
6.  **Shut Down:**
    *   Simply double-click `stop_aegis_windows.bat` to terminate all server processes.

## Roadmap

-   [x] **Phase 0: Toy Protocol & Whitepaper** (Complete)
-   [x] **Phase 1a: Alpha Protocol Development** (Complete)
-   [ ] **Phase 1b: Scientific Computing Beachhead:** Onboard first test users from university labs.
-   [ ] **Phase 2: Developer SDK & XAI Protocol.**
-   [ ] **Phase 3: Full Decentralization & DAO Launch.**

## Contributing

Aegis is in active alpha development. We are seeking collaborators, scientific partners, and community feedback. If you have a computational workload and are interested in testing the network, or are a developer passionate about building the future of decentralized compute, please open an issue or reach out.
# Aegis Protocol - v0.0.3-alpha

**A decentralized trust layer for the future of AI compute.**

[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://shields.io/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

---

Aegis is an open-source protocol designed to solve the centralization crisis in Artificial Intelligence. We are building a secure, transparent, and globally accessible marketplace for AI computation and data, built upon a foundational **Trust Protocol** that mandates verifiable compute and explainable AI (XAI).

This repository contains the official Python implementation of the Aegis "Toy Protocol," a functional proof-of-concept demonstrating the core principles of the network.

## The Vision

Our mission is to democratize access to AI compute. We envision a world where any researcher, startup, or innovator can access vast computational resources without being locked into the opaque, expensive "walled gardens" of centralized providers.

For a full overview of the project's vision, architecture, and roadmap, please read our **[Aegis Whitepaper](./docs/Aegis_Whitepaper_v0.1.md)**.

## Current Status: "Toy Protocol" v0.0.3-alpha

This repository contains a working prototype demonstrating the fundamental transaction loop of the Aegis network:

1.  `provider_node.py`: A server that offers its computational power. It is currently configured to execute 3D rendering tasks using Blender's command-line interface as a proof-of-work.
2.  `requester_node.py`: A client script that delegates a rendering task to the provider and awaits confirmation of the result.

### How to Run the Prototype

1.  **Prerequisites:** Python 3.8+, Blender, Git.
2.  **Clone the repository:** `git clone https://github.com/Esrbwt1/aegis.git`
3.  **Set up the environment:**
    ```bash
    cd aegis
    python3 -m venv venv
    source venv/bin/activate  # or .\venv\Scripts\activate on Windows
    pip install -r requirements.txt 
    ```
4.  **Run the Provider Node:**
    ```bash
    uvicorn provider_node:app --reload
    ```
5.  **In a new terminal, run the Requester Node:**
    ```bash
    python requester_node.py
    ```
6.  **Verify:** Check for the `render_output.png` file in the root directory.

## Roadmap

-   [x] **Phase 0: Toy Protocol & Whitepaper** (Complete)
-   [ ] **Phase 1: Scientific Computing Beachhead:** Target university labs and researchers as first users.
-   [ ] **Phase 2: Developer SDK & XAI Protocol:** Release tools for building trusted AI "Skills".
-   [ ] **Phase 3: Full Decentralization & DAO Launch.**

## Contributing

Aegis is in its infancy. We are actively seeking collaborators, co-founders, and community feedback. If you are passionate about building a more open and trustworthy future for AI, please open an issue or reach out.

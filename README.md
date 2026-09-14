# Full-Stack Data Structure Visualizer

An interactive, event-driven visualization platform for fundamental computer science data structures and algorithms. Built with a **FastAPI** backend that acts as an execution engine—generating granular step-by-step trace events—and an **Angular (Signals)** frontend that renders state-driven animations side-by-side (tree diagrams, array memory bars, and execution logs).

---

## 🌟 Architecture Overview

The system uses an **Event-Driven Trace Architecture**. Instead of animating state mutations directly in the client, the client sends arbitrary datasets to the Python engine. The backend executes the algorithm, logs each micro-step (`COMPARE`, `SWAP`, `BALANCED`, `INSERT`, `DELETE`) with exact state snapshots, and returns an event payload. The frontend playback engine then steps and scrubs through these events deterministically.

```text
┌─────────────────────────────────┐        HTTP POST        ┌──────────────────────────────────┐
│  Angular Frontend (Port 4200)   │ ──────────────────────> │   FastAPI Backend (Port 8000)    │
│  - Signal-based PlaybackEngine  │                         │  - Algorithmic Trace Generators  │
│  - SVG Tree & Memory Bar Graphs │ <────────────────────── │  - Pure In-Memory State Engines  │
└─────────────────────────────────┘      Trace Event JSON   └──────────────────────────────────┘
== Project Structure
data-structure-visualizer/
├── backend/
│   ├── algorithms/          # Pure data structures with event-logging mechanisms
│   │   ├── heap.py          # Max-Heap implementation (Build-Heap, Insert, Delete)
│   │   └── ...              # (Future: avl_tree.py, graph.py, trie.py)
│   ├── models.py            # Pydantic request & response schemas
│   ├── main.py              # FastAPI endpoints & CORS configuration
│   └── requirements.txt     # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── components/  # Modular visualizer views (HeapTree, ArrayBar, Controls)
    │   │   ├── models/      # TypeScript interfaces matching backend payloads
    │   │   ├── services/    # PlaybackEngine (Signals) & Visualizer HTTP API client
    │   │   ├── app.component.ts
    │   │   └── app.component.html
    │   └── main.ts          # Application bootstrap & HttpClient configuration
    ├── angular.json
    └── package.json
== Supported & Planned Data Structures
[x] Max-Heap (Structural Build-Max-Heap, Insert, Delete Root / Extract-Max)

[ ] Min-Heap / Priority Queue

[ ] AVL Tree (Self-balancing binary search tree with rotations)

[ ] Red-Black Tree

[ ] Graph Algorithms (BFS, DFS, Dijkstra’s, A* Pathfinding)

== Getting Started
Prerequisites
Python: 3.10+

Node.js: 18+

Angular CLI: 17+

1. Backend Setup (FastAPI)
Open a terminal and navigate to the backend directory:

Bash
cd backend
Create and activate a virtual environment:

Bash
python3 -m venv .venv
source .venv/bin/activate
Install dependencies:

Bash
pip install fastapi uvicorn pydantic
Launch the development server:

Bash
python -m uvicorn main:app --reload --port 8000
The API documentation will be available at http://localhost:8000/docs.

2. Frontend Setup (Angular)
Open a second terminal tab and navigate to the frontend directory:

Bash
cd frontend
Install dependencies:

Bash
npm install
Start the Angular development server:

Bash
npm start
Access the web interface at http://localhost:4200.

== Example
To test the Build-Max-Heap structural transformation:

Launch both backend and frontend servers.

Enter a comma-separated array into the input field:
42, -87, 15, -3, 99, 64, -51, 0, 78, -22, 33, 85, -94, 11, -40, 56, -72, 91, 5, -18
Click Build Max-Heap.

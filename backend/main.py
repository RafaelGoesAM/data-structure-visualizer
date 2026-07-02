import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 1. Import your custom data structures
from backend.structures.linked_list import LinkedList
from backend.structures.queue import Queue
from backend.structures.heap import MaxHeap
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("VisualizerLogger")

app = FastAPI()

# 2. Setup your centralized data structure states
states = {
    "LINKED_LIST": LinkedList(),
    "QUEUE": Queue(),
    "HEAP": MaxHeap()
}

current_structure = "LINKED_LIST"  # Tracks which view is actively selected

# 3. Static Files Mounting (References to your index.html and assets)
# This calculates the absolute path to your 'frontend' folder relative to this script
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# Mount your subfolders so the browser can read index.html's href paths
app.mount("/css", StaticFiles(directory=os.path.join(FRONTEND_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(FRONTEND_DIR, "js")), name="js")

@app.get("/")
async def serve_frontend():
    """Serves the main index.html file when visiting http://localhost:8000"""
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


# 4. Core WebSocket Engine
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("New WebSocket connection established from frontend client.")
    global current_structure
    print("Frontend client successfully connected via WebSocket.")
    
    # Send the current active structure state instantly upon connection
    await websocket.send_json({
        "type": "UPDATE_VISUAL",
        "structure_type": current_structure,
        "payload": states[current_structure].to_dict()
    })

    try:
        while True:
            # Wait for any incoming payload from app.js
            data = await websocket.receive_json()
            print(f"Command received from frontend: {data}")

            action = data.get("action")

            # Route 1: Handle layout changes
            if action == "SWITCH_STRUCTURE":
                new_structure = data.get("structure")
                if new_structure in states:
                    current_structure = new_structure

            # Route 2: Handle data additions
            elif action == "INSERT":
                value = data.get("value")
                if value is not None:
                    if current_structure == "LINKED_LIST":
                        states["LINKED_LIST"].insert(value)
                    elif current_structure == "QUEUE":
                        states["QUEUE"].enqueue(value)
                    elif current_structure == "HEAP":
                        states["HEAP"].insert(value)

            # Route 3: Clear the canvas memory
            elif action == "RESET":
                states[current_structure].clear()

            # Broadcast the freshly mutated data state back down the pipe
            await websocket.send_json({
                "type": "UPDATE_VISUAL",
                "structure_type": current_structure,
                "payload": states[current_structure].to_dict()
            })

    except WebSocketDisconnect:
        print("Frontend client disconnected safely.")
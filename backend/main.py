from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from algorithms.heap import HeapVisualizer
from models import ArrayInputRequest, InsertNodeRequest, HeapResponse

app = FastAPI(
    title="Max-Heap Visualizer API",
    description="Backend service producing trace logs for heap operations",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# CORS Configuration
# ------------------------------------------------------------------------------
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# Global Visualizer Instance
# ------------------------------------------------------------------------------
visualizer = HeapVisualizer()

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------
@app.post("/api/heap/build", response_model=HeapResponse)
def build_heap_endpoint(payload: ArrayInputRequest):
    events, final_state = visualizer.build_heap(payload.data)
    return {"events": events, "final_state": final_state}

@app.post("/api/heap/insert", response_model=HeapResponse)
def insert_node(payload: InsertNodeRequest):
    visualizer.data = payload.current_tree[:]
    events, final_state = visualizer.insert(payload.value)
    return {"events": events, "final_state": final_state}

@app.post("/api/heap/delete", response_model=HeapResponse)
def delete_root(payload: ArrayInputRequest):
    visualizer.data = payload.data[:]
    events, final_state = visualizer.delete_root()
    return {"events": events, "final_state": final_state}
# backend/main.py

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import the HeapVisualizer class from backend/algorithms/heap.py
from algorithms.heap import HeapVisualizer

app = FastAPI(
    title="Data Structure Visualizer API",
    description="API that generates event traces for data structure operations to power step-by-step frontend playback.",
    version="1.0.0"
)

# Enable CORS for Angular frontend running on port 4200
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# -----------------------------------------------------------------------------

class EventSchema(BaseModel):
    type: str = Field(..., description="Type of mutation: INSERT, DELETE, COMPARE, SWAP, BALANCED, MARK_SORTED, INFO")
    indices: List[int] = Field(..., description="Array/tree indices involved in the operation")
    current_state: List[int] = Field(..., description="Full snapshot of the array after this step")
    description: str = Field(..., description="Human-readable step description for UI logs")


class HeapResponse(BaseModel):
    events: List[EventSchema]
    final_state: List[int]


class ArrayInputRequest(BaseModel):
    data: List[int] = Field(..., description="List of integers representing the current heap array")


class InsertNodeRequest(BaseModel):
    current_tree: List[int] = Field(..., description="Current heap array state")
    value: int = Field(..., description="Integer value to insert into the heap")


# -----------------------------------------------------------------------------
# API ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"status": "online", "message": "Data Structure Visualizer API active"}


@app.post("/api/heap/heapsort", response_model=HeapResponse)
def execute_heapsort(payload: ArrayInputRequest):
    """
    Takes an unstructured or semi-structured list of numbers,
    builds a Max-Heap, and executes Heapsort with event tracing.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Input array cannot be empty.")
    
    visualizer = HeapVisualizer(payload.data)
    events, final_state = visualizer.heapsort()
    
    return HeapResponse(events=events, final_state=final_state)


@app.post("/api/heap/insert", response_model=HeapResponse)
def insert_node(payload: InsertNodeRequest):
    """
    Inserts a new value into an existing heap array and performs Sift-Up
    to maintain the Max-Heap property.
    """
    visualizer = HeapVisualizer(payload.current_tree)
    events, final_state = visualizer.insert(payload.value)
    
    return HeapResponse(events=events, final_state=final_state)


@app.post("/api/heap/delete", response_model=HeapResponse)
def delete_root_node(payload: ArrayInputRequest):
    """
    Removes the root (max element) from the current heap array and performs Sift-Down
    to restore the Max-Heap property.
    """
    if not payload.data:
        raise HTTPException(status_code=400, detail="Cannot delete root from an empty heap.")
        
    visualizer = HeapVisualizer(payload.data)
    events, final_state = visualizer.delete_root()
    
    return HeapResponse(events=events, final_state=final_state)
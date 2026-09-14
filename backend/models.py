from pydantic import BaseModel
from typing import List, Dict, Any


class ArrayInputRequest(BaseModel):
    """Payload for Build-Max-Heap and Delete operations."""
    data: List[int]


class InsertNodeRequest(BaseModel):
    """Payload for inserting a new node into an existing tree."""
    current_tree: List[int]
    value: int


class HeapResponse(BaseModel):
    """Standardized response returning trace events and the resulting state."""
    events: List[Dict[str, Any]]
    final_state: List[int]
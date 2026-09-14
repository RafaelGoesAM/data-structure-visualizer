export type EventType =
  | 'INSERT'
  | 'DELETE'
  | 'COMPARE'
  | 'SWAP'
  | 'BALANCED'
  | 'MARK_SORTED'
  | 'INFO';

export interface TraceEvent {
  type: EventType;
  indices: number[];
  current_state: number[];
  description: string;
}

export interface HeapResponse {
  events: TraceEvent[];
  final_state: number[];
}

export interface ArrayInputRequest {
  data: number[];
}

export interface InsertNodeRequest {
  current_tree: number[];
  value: number;
}
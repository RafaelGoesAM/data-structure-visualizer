import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  HeapResponse,
  ArrayInputRequest,
  InsertNodeRequest,
} from '../models/trace-event.model';

@Injectable({
  providedIn: 'root',
})
export class VisualizerService {
  private http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/api/heap';

  /**
   * Sends an unorganized or semi-organized array to perform Heapsort with event logging.
   */
  executeHeapsort(data: number[]): Observable<HeapResponse> {
    const payload: ArrayInputRequest = { data };
    return this.http.post<HeapResponse>(`${this.apiUrl}/heapsort`, payload);
  }

  /**
   * Inserts a value into the current heap array and executes Sift-Up rebalancing.
   */
  insertNode(currentTree: number[], value: number): Observable<HeapResponse> {
    const payload: InsertNodeRequest = { current_tree: currentTree, value };
    return this.http.post<HeapResponse>(`${this.apiUrl}/insert`, payload);
  }

  /**
   * Deletes the root node (max element) and executes Sift-Down rebalancing.
   */
  deleteRoot(currentTree: number[]): Observable<HeapResponse> {
    const payload: ArrayInputRequest = { data: currentTree };
    return this.http.post<HeapResponse>(`${this.apiUrl}/delete`, payload);
  }
}
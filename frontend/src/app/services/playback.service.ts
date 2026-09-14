import { Injectable, signal, computed } from '@angular/core';
import { TraceEvent, HeapResponse } from '../models/trace-event.model';

@Injectable({
  providedIn: 'root'
})
export class PlaybackService {
  // Canonical tree state and event logs
  readonly currentTree = signal<number[]>([90, 40, 50, 10, 20]);
  readonly events = signal<TraceEvent[]>([]);
  readonly currentStep = signal<number>(0);
  readonly isPlaying = signal<boolean>(false);
  readonly speed = signal<number>(600); // ms per step

  private timerId: any = null;

  // Active snapshot at current playback step
  readonly activeState = computed(() => {
    const list = this.events();
    const step = this.currentStep();
    return list.length > 0 ? list[step].current_state : this.currentTree();
  });

  readonly activeEvent = computed(() => {
    const list = this.events();
    const step = this.currentStep();
    return list.length > 0 ? list[step] : null;
  });

  loadTrace(response: HeapResponse) {
    this.pause();
    this.events.set(response.events);
    this.currentStep.set(0);
    this.currentTree.set(response.final_state);
    this.play();
  }

  play() {
    if (this.events().length === 0 || this.currentStep() >= this.events().length - 1) return;
    this.isPlaying.set(true);
    this.timerId = setInterval(() => this.stepNext(), this.speed());
  }

  pause() {
    this.isPlaying.set(false);
    if (this.timerId) {
      clearInterval(this.timerId);
      this.timerId = null;
    }
  }

  stepNext() {
    if (this.currentStep() < this.events().length - 1) {
      this.currentStep.update((s: number) => s + 1);
    } else {
      this.pause();
    }
  }
  
  stepPrev() {
    if (this.currentStep() > 0) {
      this.currentStep.update((s: number) => s - 1);
    }
  }
}
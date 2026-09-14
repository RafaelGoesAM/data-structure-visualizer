import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { PlaybackService } from '../../services/playback.service';
import { VisualizerService } from '../../services/visualizer.service';

@Component({
  selector: 'app-controls',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './controls.component.html',
  styleUrls: ['./controls.component.css']
})
export class ControlsComponent {
  readonly playback = inject(PlaybackService);
  private visualizer = inject(VisualizerService);

  insertValue: number | null = null;
  rawArrayInput: string = '45, 20, 75, 12, 90, 30';
  isLoading: boolean = false;

  // --- API OPERATIONS ---

  onInsert() {
    if (this.insertValue === null) return;
    const val = Number(this.insertValue);
    this.isLoading = true;
  
    this.visualizer.insertNode(this.playback.currentTree(), val).subscribe({
      next: (response: any) => {
        this.playback.loadTrace(response);
        this.insertValue = null;
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Insert error:', err);
        this.isLoading = false;
      }
    });
  }
  
  onDeleteRoot() {
    if (this.playback.currentTree().length === 0) return;
    this.isLoading = true;
  
    this.visualizer.deleteRoot(this.playback.currentTree()).subscribe({
      next: (response: any) => {
        this.playback.loadTrace(response);
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Delete root error:', err);
        this.isLoading = false;
      }
    });
  }
  
  onBuildHeap() {
    const parsed = this.rawArrayInput
      .split(',')
      .map((v: string) => parseInt(v.trim(), 10))
      .filter((v: number) => !isNaN(v));
  
    if (parsed.length === 0) return;
    this.isLoading = true;
  
    this.visualizer.buildHeap(parsed).subscribe({
      next: (response: any) => {
        this.playback.loadTrace(response);
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Build heap error:', err);
        this.isLoading = false;
      }
    });
  }

  // --- SPEED SLIDER CONTROL ---

  onSpeedChange(event: Event) {
    const input = event.target as HTMLInputElement;
    this.playback.speed.set(Number(input.value));
  }
}
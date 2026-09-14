import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlaybackService } from '../../services/playback.service';

interface ArrayItem {
  value: number;
  index: number;
  heightPercentage: number;
  isHighlighted: boolean;
}

@Component({
  selector: 'app-array-bar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './array-bar.component.html',
  styleUrls: ['./array-bar.component.css']
})
export class ArrayBarComponent {
  private playback = inject(PlaybackService);

  readonly items = computed<ArrayItem[]>(() => {
    const arr = this.playback.activeState();
    const activeEvt = this.playback.activeEvent();
    const highlightedIndices = activeEvt ? activeEvt.indices : [];
  
    const maxVal = arr.length > 0 ? Math.max(...arr, 1) : 1;
  
    return arr.map((value: number, index: number) => ({
      value,
      index,
      heightPercentage: Math.max(20, Math.round((value / maxVal) * 100)),
      isHighlighted: highlightedIndices.includes(index)
    }));
  });
}
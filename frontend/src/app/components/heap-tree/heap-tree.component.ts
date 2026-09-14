import { Component, inject, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlaybackService } from '../../services/playback.service';

interface TreeNode {
  value: number;
  index: number;
  x: number;
  y: number;
  parentX?: number;
  parentY?: number;
  isHighlighted: boolean;
}

@Component({
  selector: 'app-heap-tree',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="tree-container">
      <svg width="600" height="320">
        <!-- Render Edge Lines -->
        <g stroke="#94a3b8" stroke-width="2">
          <line 
            *ngFor="let node of nodes()" 
            [attr.x1]="node.parentX" 
            [attr.y1]="node.parentY" 
            [attr.x2]="node.x" 
            [attr.y2]="node.y"
            [attr.display]="node.index === 0 ? 'none' : 'block'" />
        </g>

        <!-- Render Nodes -->
        <g *ngFor="let node of nodes()">
          <circle 
            [attr.cx]="node.x" 
            [attr.cy]="node.y" 
            r="20" 
            [attr.fill]="node.isHighlighted ? '#ef4444' : '#3b82f6'"
            stroke="#1e3a8a" 
            stroke-width="2" />
          <text 
            [attr.x]="node.x" 
            [attr.y]="node.y + 5" 
            text-anchor="middle" 
            fill="white" 
            font-weight="bold" 
            font-size="14">
            {{ node.value }}
          </text>
        </g>
      </svg>
    </div>
  `,
  styles: [`
    .tree-container { display: flex; justify-content: center; padding: 20px; }
    circle { transition: all 0.3s ease; }
  `]
})
export class HeapTreeComponent {
  private playback = inject(PlaybackService);

  readonly nodes = computed(() => {
    const arr = this.playback.activeState();
    const activeEvt = this.playback.activeEvent();
    const highlightedIndices = activeEvt ? activeEvt.indices : [];

    const result: TreeNode[] = [];
    const width = 600;

    arr.forEach((value: number, index: number) => {
      const level = Math.floor(Math.log2(index + 1));
      const posInLevel = index - (Math.pow(2, level) - 1);
      const totalInLevel = Math.pow(2, level);
      
      const x = (width / (totalInLevel + 1)) * (posInLevel + 1);
      const y = 50 + level * 65;

      let parentX: number | undefined;
      let parentY: number | undefined;

      if (index > 0) {
        const parentIdx = Math.floor((index - 1) / 2);
        const parentNode = result[parentIdx];
        parentX = parentNode.x;
        parentY = parentNode.y;
      }

      result.push({
        value,
        index,
        x,
        y,
        parentX,
        parentY,
        isHighlighted: highlightedIndices.includes(index)
      });
    });

    return result;
  });
}
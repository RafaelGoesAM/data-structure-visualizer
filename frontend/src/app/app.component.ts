import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlsComponent } from './components/controls/controls.component';
import { HeapTreeComponent } from './components/heap-tree/heap-tree.component';
import { ArrayBarComponent } from './components/array-bar/array-bar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule, 
    ControlsComponent, 
    HeapTreeComponent, 
    ArrayBarComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Max-Heap Visualizer';
}
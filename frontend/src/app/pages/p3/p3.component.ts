import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { BrgbService } from '../../services/brgb.service';
import { GrafanaEmbedComponent } from '../grafana-embed/grafana-embed.component';
@Component({
  selector: 'app-pi3-page',
  standalone: true,
  imports: [CommonModule, FormsModule, GrafanaEmbedComponent],
  templateUrl: './p3.component.html',
  styleUrl: './p3.component.css',
})
export class P3Component {
  selectedColor = '#ff0000';

  constructor(private brgbService: BrgbService, private toastr: ToastrService) {}

  setColor() {
    const { red, green, blue } = this.hexToNormalizedRgb(this.selectedColor);

    this.brgbService.setBrgbColor({ red, green, blue }).subscribe({
      next: () => this.toastr.success('BRGB color updated'),
      error: () => this.toastr.error('Failed to update BRGB color'),
    });
  }

  private hexToNormalizedRgb(hex: string): { red: number; green: number; blue: number } {
    const cleanHex = hex.replace('#', '');
    const r = parseInt(cleanHex.substring(0, 2), 16);
    const g = parseInt(cleanHex.substring(2, 4), 16);
    const b = parseInt(cleanHex.substring(4, 6), 16);
    return { red: r / 255, green: g / 255, blue: b / 255 };
  }
}
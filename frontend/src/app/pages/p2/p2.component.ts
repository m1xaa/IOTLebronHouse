import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { Sd4Service } from '../../services/sd4.service';
import { GrafanaEmbedComponent } from '../grafana-embed/grafana-embed.component';

@Component({
  selector: 'app-pi2-page',
  standalone: true,
  imports: [CommonModule, FormsModule, GrafanaEmbedComponent],
  templateUrl: './p2.component.html',
  styleUrl: './p2.component.css',
})
export class P2Component implements OnInit {
  displayValue = 0;
  secondsIncrement = 10;

  constructor(private sd4Service: Sd4Service, private toastr: ToastrService) {}

  ngOnInit(): void {
    this.sd4Service.getSecondsIncrement().subscribe({
      next: s => (this.secondsIncrement = s),
    });
  }

  setDisplay() {
    const rounded = Math.round(this.displayValue);
    this.sd4Service.setTimer({ seconds: rounded }).subscribe({
      next: () => this.toastr.success('SD4 timer set'),
      error: () => this.toastr.error('Failed to set SD4 timer'),
    });
  }

  setSecondsIncrement() {
    const rounded = Math.round(this.secondsIncrement);
    this.sd4Service.setSecondsIncrement({ seconds: rounded }).subscribe({
      next: () => this.toastr.success('Set seconds increment'),
      error: () => this.toastr.error('Failed to set seconds increment'),
    });
  }
}
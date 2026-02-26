import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';

import { AlarmState } from '../../models/alarm/alarm-state';
import { AlarmService } from '../../services/alarm.service';
import { Sd4Service } from '../../services/sd4.service';
import { GrafanaEmbedComponent } from '../grafana-embed/grafana-embed.component';


@Component({
  selector: 'app-pi1-page',
  standalone: true,
  imports: [CommonModule, FormsModule, GrafanaEmbedComponent],
  templateUrl: './p1.component.html',
  styleUrl: './p1.component.css',
})
export class P1Component implements OnInit {
  states = Object.values(AlarmState);
  currentState: AlarmState | null = null;

  currentPersonCount: number | null = null;

  pi1CameraUrl = 'http://<raspberry_pi_ip>:8080/?action=stream';
  showCamera = true;
  toggleCamera() { this.showCamera = !this.showCamera; }

  constructor(
    private alarmService: AlarmService,
    private sd4Service: Sd4Service,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.alarmService.init();

    this.alarmService.state$.subscribe(state => this.currentState = state);
    this.alarmService.personCountState$.subscribe(pc => this.currentPersonCount = pc);
  }

  onSelect(state: AlarmState) {
    if (state === AlarmState.ARMING) return;
    this.alarmService.changeState(state);
  }

  isActive(state: AlarmState) { return this.currentState === state; }
  isDisabled(state: AlarmState) { return state === AlarmState.ARMING; }

  resetPersonCount() {
    this.alarmService.resetPersonCount().subscribe({
      next: () => { this.currentPersonCount = 0; this.toastr.success('Person count reset'); },
      error: () => this.toastr.error('Failed to reset person count')
    });
  }
}
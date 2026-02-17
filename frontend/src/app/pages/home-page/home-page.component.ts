import { Component, OnInit } from '@angular/core';
import { AlarmState } from '../../models/alarm/alarm-state';
import { CommonModule } from '@angular/common';
import { AlarmService } from '../../services/alarm.service';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements OnInit {

  states = Object.values(AlarmState);
  currentState: AlarmState | null = null;

  constructor(private alarmService: AlarmService) {}

  ngOnInit(): void {
    this.alarmService.init();

    this.alarmService.state$.subscribe(state => {
      this.currentState = state;
    });
  }

  onSelect(state: AlarmState) {
    if (state === AlarmState.ARMING) return;

    this.alarmService.changeState(state);
  }

  isActive(state: AlarmState) {
    return this.currentState === state;
  }

  isDisabled(state: AlarmState) {
    return state === AlarmState.ARMING;
  }
}

import { Component, OnInit } from '@angular/core';
import { AlarmState } from '../../models/alarm/alarm-state';
import { CommonModule } from '@angular/common';
import { AlarmService } from '../../services/alarm.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.css'
})
export class HomePageComponent implements OnInit {

  displayValue: number = 0;
  selectedColor: string = '#ff0000';
  secondsIncrement: number = 5;

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

  setDisplay() {
    console.log("Set display:", this.displayValue);
  }

  setSecondsIncrement() {
    console.log("Set seconds increment:", this.secondsIncrement);
  }

  setColor() {
    console.log("Set color:", this.selectedColor);
  }
}

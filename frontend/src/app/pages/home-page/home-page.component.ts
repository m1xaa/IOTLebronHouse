import { Component, OnInit } from '@angular/core';
import { AlarmState } from '../../models/alarm/alarm-state';
import { CommonModule } from '@angular/common';
import { AlarmService } from '../../services/alarm.service';
import { FormsModule } from '@angular/forms';
import { BrgbService } from '../../services/brgb.service';
import { ToastrService } from 'ngx-toastr';

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

  constructor(
    private alarmService: AlarmService,
    private brgbService: BrgbService,
    private toastr: ToastrService
  ) {}

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
    const { red, green, blue } = this.hexToNormalizedRgb(this.selectedColor);

    this.brgbService.setBrgbColor({ red, green, blue })
      .subscribe({
      next: () => this.toastr.success('BRGB color updated'),
      error: () => this.toastr.error('Failed to update BRGB color')
      });
  }

  private hexToNormalizedRgb(hex: string): { red: number; green: number; blue: number } {
  const cleanHex = hex.replace('#', '');

  const r = parseInt(cleanHex.substring(0, 2), 16);
  const g = parseInt(cleanHex.substring(2, 4), 16);
  const b = parseInt(cleanHex.substring(4, 6), 16);

  return {
    red: r / 255,
    green: g / 255,
    blue: b / 255
  };
}

}



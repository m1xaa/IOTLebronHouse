import { Component, OnInit } from '@angular/core';
import { AlarmState } from '../../models/alarm/alarm-state';
import { CommonModule } from '@angular/common';
import { AlarmService } from '../../services/alarm.service';
import { FormsModule } from '@angular/forms';
import { BrgbService } from '../../services/brgb.service';
import { ToastrService } from 'ngx-toastr';
import { Sd4Service } from '../../services/sd4.service';

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

  currentPersonCount: number | null = null;
  pi1CameraUrl = 'http://192.168.107.146:8080/?action=stream';

  showCamera = true;
  toggleCamera() { this.showCamera = !this.showCamera; }
  constructor(
    private alarmService: AlarmService,
    private brgbService: BrgbService,
    private sd4Service: Sd4Service,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.alarmService.init();

    this.sd4Service.getSecondsIncrement().subscribe({
      next: seconds => {
        this.secondsIncrement = seconds;
      }
    });

    this.alarmService.state$.subscribe(state => {
      this.currentState = state;
    });

    this.alarmService.personCountState$.subscribe(personCount => {
      this.currentPersonCount = personCount;
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
    const rounded = Math.round(this.displayValue);
    this.sd4Service.setTimer({seconds: rounded}).subscribe({
      next: () => this.toastr.success('SD4 timer set'),
      error: () => this.toastr.error('Failed to set SD4 timer')
    });
  }

  setSecondsIncrement() {
    const rounded = Math.round(this.secondsIncrement);
    this.sd4Service.setSecondsIncrement({seconds: rounded}).subscribe({
      next: () => this.toastr.success('Set seconds increment'),
      error: () => this.toastr.error('Failed to set seconds increment')
    });
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

  resetPersonCount() {
    this.alarmService.resetPersonCount().subscribe({
      next: () => {
        this.currentPersonCount = 0;
        this.toastr.success('Person count reset');
      },
      error: () => this.toastr.error('Failed to reset person count')
    });
  }

}



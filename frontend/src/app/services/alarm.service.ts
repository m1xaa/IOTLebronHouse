import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { environment } from '../environments/environvment';
import { AlarmState } from '../models/alarm/alarm-state';
import { WebSocketService } from './web-scoket.service';

@Injectable({
  providedIn: 'root'
})
export class AlarmService {

  private baseUrl = environment.apiUrl;
  private stateSubject = new BehaviorSubject<AlarmState | null>(null);
  state$ = this.stateSubject.asObservable();

  constructor(
    private http: HttpClient,
    private ws: WebSocketService
  ) {}

  init() {
    this.http.get<AlarmState>(`${this.baseUrl}/api/alarm/state`)
      .subscribe(state => {
        this.stateSubject.next(state);
      });

    this.ws.connect();

    this.ws.subscribe('/topic/alarm', (message: AlarmState) => {
      console.log(message);
      this.stateSubject.next(message);
    });
  }

  changeState(state: AlarmState) {
    this.http.post(`${this.baseUrl}/api/alarm/state/${state}`, {})
      .subscribe();
  }
}

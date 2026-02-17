import { APP_ID, Injectable } from '@angular/core';
import { environment } from '../environments/environvment';
import { HttpClient } from '@angular/common/http';
import { SetTimerRequest } from '../models/sd4/set-timer-request';
import { Observable } from 'rxjs';
import { SetSecondsIncrementRequest } from '../models/sd4/set-seconds-increment-request';

@Injectable({
  providedIn: 'root'
})
export class Sd4Service {

  baseUrl: string = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }

  setTimer(request: SetTimerRequest): Observable<void> {
    return this.http.put<void>(`${this.baseUrl}/api/sd4/timer`, request);
  }

  setSecondsIncrement(request: SetSecondsIncrementRequest): Observable<void> {
    return this.http.put<void>(`${this.baseUrl}/api/sd4/seconds`, request);
  }
}

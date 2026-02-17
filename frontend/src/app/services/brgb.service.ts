import { Injectable } from '@angular/core';
import { environment } from '../environments/environvment';
import { HttpClient } from '@angular/common/http';
import { SetBrgbColorRequest } from '../models/brgb/set-brgb-color-request';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BrgbService {

  baseUrl: string = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }

  setBrgbColor(request: SetBrgbColorRequest): Observable<void> {
    return this.http.put<void>(`${this.baseUrl}/api/brgb`, request);
  }
}

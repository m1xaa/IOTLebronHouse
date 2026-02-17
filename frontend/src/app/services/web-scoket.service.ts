import { Injectable } from '@angular/core';
import { Client, IMessage } from '@stomp/stompjs';
import { environment } from '../environments/environvment';
import SockJS from 'sockjs-client';

@Injectable({
  providedIn: 'root'
})
export class WebSocketService {

  private baseUrl: string = environment.apiUrl;
  private client!: Client;
  private connected = false;
  private pendingSubscriptions: Array<() => void> = [];

  connect(): void {

    if (this.client?.active) return;

    this.client = new Client({
      webSocketFactory: () => new SockJS(`${this.baseUrl}/ws`),
      reconnectDelay: 5000
    });

    this.client.onConnect = () => {
      console.log('WS connected');
      this.connected = true;

      // izvrši sve subscribe-ove koji su čekali
      this.pendingSubscriptions.forEach(fn => fn());
      this.pendingSubscriptions = [];
    };

    this.client.onDisconnect = () => {
      this.connected = false;
    };

    this.client.activate();
  }

  subscribe(destination: string, callback: (body: any) => void): void {

    const subscribeLogic = () => {
      this.client.subscribe(destination, (message: IMessage) => {
        try {
          callback(JSON.parse(message.body));
        } catch {
          callback(message.body);
        }
      });
    };

    if (this.connected) {
      subscribeLogic();
    } else {
      this.pendingSubscriptions.push(subscribeLogic);
    }
  }

  publish(destination: string, body: any): void {

    if (!this.connected) {
      console.error('WebSocket not connected');
      return;
    }

    this.client.publish({
      destination,
      body: typeof body === 'string' ? body : JSON.stringify(body)
    });
  }

  disconnect(): void {
    if (this.client) {
      this.client.deactivate();
      this.connected = false;
    }
  }
}

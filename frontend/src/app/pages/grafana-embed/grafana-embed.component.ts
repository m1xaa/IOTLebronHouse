import { Component, Input, OnChanges } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grafana-embed',
  standalone: true,
  imports: [CommonModule],
  template: `
    <iframe class="grafana-frame" [src]="safeUrl" frameborder="0"></iframe>
  `,
  styles: [`
    .grafana-frame {
      width: 100%;
      height: 900px;
      border: 1px solid #334155;
      border-radius: 14px;
      background: #0b1220;
    }
  `]
})
export class GrafanaEmbedComponent implements OnChanges {
  @Input() dashboardUid!: string; // e.g. lebronhouse-pi3
  @Input() piId!: string;         // e.g. PI3
  @Input() grafanaBase = 'http://localhost:3000';

  safeUrl!: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) {}

  ngOnChanges(): void {
    const url =
      `${this.grafanaBase}/d/${this.dashboardUid}/${this.dashboardUid}` +
      `?orgId=1&var-pi_id=${encodeURIComponent(this.piId)}` +
      `&var-simulated=.*&kiosk`;

    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
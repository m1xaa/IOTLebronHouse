import { Component, Input, OnChanges } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grafana-embed',
  standalone: true,
  imports: [CommonModule],
  template: `
    <iframe
      class="grafana-frame"
      [src]="safeUrl"
      [style.height.px]="smaller ? 390 : 1100"
      frameborder="0">
    </iframe>
  `,
  styles: [`
    .grafana-frame {
      width: 100%;
      border: 1px solid #334155;
      border-radius: 14px;
      background: #0b1220;
    }
  `]
})
export class GrafanaEmbedComponent implements OnChanges {

  @Input() dashboardUid!: string;
  @Input() piId?: string;
  @Input() grafanaBase = 'http://localhost:3000';
  @Input() smaller: boolean = false;

  safeUrl!: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) {}

  ngOnChanges(): void {
    let url =
      `${this.grafanaBase}/d/${this.dashboardUid}/${this.dashboardUid}` +
      `?orgId=1&kiosk`;

    if (this.piId) {
      url += `&var-pi_id=${encodeURIComponent(this.piId)}`;
    }

    this.safeUrl = this.sanitizer.bypassSecurityTrustResourceUrl(url);
  }
}
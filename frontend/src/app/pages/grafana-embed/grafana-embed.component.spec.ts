import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GrafanaEmbedComponent } from './grafana-embed.component';

describe('GrafanaEmbedComponent', () => {
  let component: GrafanaEmbedComponent;
  let fixture: ComponentFixture<GrafanaEmbedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GrafanaEmbedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GrafanaEmbedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

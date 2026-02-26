import { Routes } from '@angular/router';
import { P1Component } from './pages/p1/p1.component';
import { P2Component } from './pages/p2/p2.component';
import { P3Component } from './pages/p3/p3.component';

export const routes: Routes = [
  { path: '', redirectTo: 'pi1', pathMatch: 'full' },

  { path: 'pi1', component: P1Component },
  { path: 'pi2', component: P2Component },
  { path: 'pi3', component: P3Component },

  { path: '**', redirectTo: 'pi1' }
];
import { Component } from '@angular/core';
import { faBars } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  faBars = faBars;

  sideNavbarActive: boolean = true;

  toggleSideNavbar() {
    this.sideNavbarActive = !this.sideNavbarActive;
  }
}

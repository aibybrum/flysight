import { Component } from '@angular/core';
import { faBug, faSignOut, faCompass } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-side-navbar',
  templateUrl: './side-navbar.component.html',
  styleUrl: './side-navbar.component.scss'
})
export class SideNavbarComponent {
  faBug = faBug;
  faSignOut = faSignOut;
  faCompass = faCompass;
}

import { Component, EventEmitter, Output } from '@angular/core';
import { faBars, faBell, faSearch } from '@fortawesome/free-solid-svg-icons';


@Component({
  selector: 'app-top-navbar',
  templateUrl: './top-navbar.component.html',
  styleUrl: './top-navbar.component.scss'
})
export class TopNavbarComponent {
  faBars = faBars;
  faBell = faBell;
  faSearch = faSearch;
  // @Output() toggleSideNavbar = new EventEmitter<void>();
}

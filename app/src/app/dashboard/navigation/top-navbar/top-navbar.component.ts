import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-top-navbar',
  templateUrl: './top-navbar.component.html',
  styleUrl: './top-navbar.component.scss',
})
export class TopNavbarComponent {
  // public iconOnlyToggled = false;
  // public sidebarToggled = false;
  
  // constructor(config: NgbDropdownConfig) {
  //   config.placement = 'bottom-right';
  // }

  ngOnInit() {
  }

  // toggle sidebar in small devices
  toggleOffcanvas() {
    // document.querySelector('.sidebar-offcanvas').classList.toggle('active');
  }

  // toggle sidebar
  toggleSidebar() {
    // let body = document.querySelector('body');
    // if((!body.classList.contains('sidebar-toggle-display')) && (!body.classList.contains('sidebar-absolute'))) {
    //   this.iconOnlyToggled = !this.iconOnlyToggled;
    //   if(this.iconOnlyToggled) {
    //     body.classList.add('sidebar-icon-only');
    //   } else {
    //     body.classList.remove('sidebar-icon-only');
    //   }
    // } else {
    //   this.sidebarToggled = !this.sidebarToggled;
    //   if(this.sidebarToggled) {
    //     body.classList.add('sidebar-hidden');
    //   } else {
    //     body.classList.remove('sidebar-hidden');
    //   }
    }
}

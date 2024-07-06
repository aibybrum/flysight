import { Component, OnInit} from '@angular/core';
import { NgbDropdownConfig } from "@ng-bootstrap/ng-bootstrap";

@Component({
  selector: 'app-top-navbar',
  templateUrl: './top-navbar.component.html',
  styleUrl: './top-navbar.component.scss',
  providers: [NgbDropdownConfig]
})
export class TopNavbarComponent implements OnInit {
  public iconOnlyToggled = false;
  public sidebarToggled = false;

  toggleRightSidebar() {
    const sidebarOffcanvas = document.querySelector('.sidebar-offcanvas');
    if (sidebarOffcanvas) {
      sidebarOffcanvas.classList.toggle('active');
    } else {
      console.warn("No element with class 'sidebar-offcanvas' found.");
    }
  }

  toggleIconOnlySidebar() {
    this.iconOnlyToggled =!this.iconOnlyToggled;
    (document.querySelector("body")?? document.body).classList.toggle("sidebar-icon-only", this.iconOnlyToggled);
  }

  constructor(config: NgbDropdownConfig) {
    config.placement = "bottom-right";
  }
  ngOnInit() {}
}

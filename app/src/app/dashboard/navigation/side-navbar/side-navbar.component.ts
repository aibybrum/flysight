import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-side-navbar',
  templateUrl: './side-navbar.component.html',
  styleUrl: './side-navbar.component.scss'
})
export class SideNavbarComponent implements OnInit {
  constructor() {}

  ngOnInit() {
    const body = document.querySelector("body");
    if (body) {
      document.querySelectorAll(".sidebar .nav-item").forEach(function(el) {
        el.addEventListener("mouseover", function() {
          if (body.classList.contains("sidebar-icon-only")) {
            el.classList.add("hover-open");
          }
        });
        el.addEventListener("mouseout", function() {
          if (body.classList.contains("sidebar-icon-only")) {
            el.classList.remove("hover-open");
          }
        });
      });
    }
  }

  public parentId = "";
  clickedMenu(event: MouseEvent) {
    var target = event.currentTarget as HTMLElement;
    let parentId = target.id;
    if (parentId == this.parentId) {
      console.log('same');
      this.parentId = "";
    } else {
      console.log('not same');
      this.parentId = target.id;
    }
  }
}

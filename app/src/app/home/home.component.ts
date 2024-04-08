import { Component } from '@angular/core';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  ngOnInit(): void {
    const title = "\"Unleash the power in your swooping journey with SG3K\"";
    const text = "The advanced GPS tool designed to fuel continuous improvement for all skill levels and transform every jump into an opportunity for growth.";
    const titleElement = document.getElementById('title-element');
    const textElement = document.getElementById('text-element');
    const typingDelay = 130;

    if (titleElement && textElement) {
      this.typeText(title, titleElement, typingDelay);
      this.typeText(text, textElement, typingDelay, title.split(' ').length * typingDelay);
    }
  }

  typeText(text: string, typingElement: HTMLElement, delay: number, initialDelay: number = 0) {
    if (typingElement) {
      const words = text.split(' ');
      let currentWord = '';
  
      for (let i = 0; i < words.length; i++) {
        setTimeout(() => {
          currentWord = words[i];
          if (currentWord === 'SG3K\"') {
            typingElement.innerHTML += `SG<span class="text-primary">${3}</span>K\"`;
          } else {
            typingElement.textContent += currentWord + ' ';
          }
        }, delay * i + initialDelay);
      }
    }
  }
}

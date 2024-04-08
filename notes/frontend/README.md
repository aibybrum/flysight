# Angular commands to remember

## Installation

// node.js version
node -v

// angular version
ng version

// install
npm install -g @angular/cli

// update
npm install -g @angular/cli@latest

// creating new app
ng new app
or
ng new app --no-standalone

// install plotly packages
npm install angular-plotly.js plotly.js-dist-min --save
npm install @types/plotly.js-dist-min --save-dev

//adding bootstrap
npm install bootstrap
https://www.hvdig.us/angular-agency/angular-bootstrap-adding-bootstrap-to-an-angular-application

// adding fontawesome
npm i @fortawesome/angular-fontawesome

// start app
ng serve / npm start

## Creating stuff

ng generate component <component-name>
ng generate service <service-name>
ng generate module <module-name>

## Component Overview

/my-app
|-- node_modules
|-- src
| |-- app
| | |-- core
| | | |-- base
| | | | |-- base.component.ts
| | | | |-- base.module.ts
| | | |-- services
| | | | |-- authentication.service.ts
| | | | |-- jump-data.service.ts
| | | | |-- api.service.ts
| | |-- dashboard
| | | |-- dashboard.component.ts
| | | |-- dashboard.module.ts
| | | |-- dashboard-routing.module.ts
| | | |-- components
| | | | |-- header
| | | | | |-- header.component.ts
| | | | |-- jump-data-table
| | | | | |-- jump-data-table.component.ts
| | | | |-- chart
| | | | | |-- chart.component.ts
| | | | |-- upload-file
| | | | | |-- upload-file.component.ts
| | | | |-- filters
| | | | | |-- filters.component.ts
| | | | |-- metrics
| | | | | |-- metrics.component.ts
| | | | |-- side-view-flight-path
| | | | | |-- side-view-flight-path.component.ts
| | | | |-- map
| | | | | |-- map.component.ts
| | | | |-- overhead-view-flight-path
| | | | | |-- overhead-view-flight-path.component.ts
| | |-- login
| | | |-- login.component.ts
| | | |-- login.module.ts
| | |-- signup
| | | |-- signup.component.ts
| | | |-- signup.module.ts
| | |-- home
| | | |-- home.component.ts
| | | |-- home.module.ts
| | |-- app.component.ts
| | |-- app.module.ts
| |-- assets
| |-- environments
| |-- app-routing.module.ts
| |-- index.html
| |-- main.ts
| |-- styles.css
|-- package.json

# Customising Bootstrap

https://medium.com/@kathar.rahul/scss-integration-with-bootstrap-5-in-angular-8e12ddf9b471

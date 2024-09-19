# Angular

### Check node.js version

```
node -v
```

### Check angular version

```
ng version
```

### Install angular

```
npm install -g @angular/cli
```

### Update angular

```
npm install -g @angular/cli@latest
```

### Check and fix vulnerabilities

```
npm audit
npm audit fix
```

### Creating new app

```
ng new app
or
ng new app --no-standalone
```

### Install plotly packages

```
npm install angular-plotly.js plotly.js-dist-min --save
npm install @types/plotly.js-dist-min --save-dev
```

### Adding bootstrap

```
npm install bootstrap
ng add @ng-bootstrap/ng-bootstrap
```

https://www.hvdig.us/angular-agency/angular-bootstrap-adding-bootstrap-to-an-angular-application

### Icons

```
@mdi/font
```

### Start app

```
ng serve / npm start
```

## Creating stuff

```
ng generate component <component-name>
ng generate service <service-name>
ng generate module <module-name>
ng generate interface models/<interface-name>
```

## Component Overview

```
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
```

# Customising Bootstrap

https://medium.com/swlh/how-to-structure-scss-in-an-angular-app-a1b8a759a028
https://sass-guidelin.es/#architecture

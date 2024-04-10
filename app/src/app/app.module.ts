import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';

import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { BaseComponent } from './core/base/base.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { SignupComponent } from './signup/signup.component';
import { HeaderComponent } from './dashboard/header/header.component';
import { JumpDataTableComponent } from './dashboard/jump-data-table/jump-data-table.component';
import { ChartComponent } from './dashboard/chart/chart.component';
import { UploadFileComponent } from './dashboard/upload-file/upload-file.component';
import { FiltersComponent } from './dashboard/filters/filters.component';
import { MetricsComponent } from './dashboard/metrics/metrics.component';
import { SideViewFlightPathComponent } from './dashboard/side-view-flight-path/side-view-flight-path.component';
import { MapComponent } from './dashboard/map/map.component';
import { OverheadViewFlightPathComponent } from './dashboard/overhead-view-flight-path/overhead-view-flight-path.component';
import { SideNavComponent } from './dashboard/side-nav/side-nav.component';

PlotlyModule.plotlyjs = PlotlyJS;

const appRoutes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'auth/login', component: LoginComponent },
  { path: 'auth/signup', component: SignupComponent },
  { path: 'dashboard', component: DashboardComponent },
];

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    BaseComponent,
    DashboardComponent,
    LoginComponent,
    SignupComponent,
    HeaderComponent,
    JumpDataTableComponent,
    ChartComponent,
    UploadFileComponent,
    FiltersComponent,
    MetricsComponent,
    SideViewFlightPathComponent,
    MapComponent,
    OverheadViewFlightPathComponent,
    SideNavComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    PlotlyModule,
    FontAwesomeModule,
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

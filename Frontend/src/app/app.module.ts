//import per far funzionare il tutto (non toccare), create già con la creazione del progetto
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

//import per i vari componenti usati nei file html
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatDividerModule } from '@angular/material/divider';
import { MatListModule } from '@angular/material/list';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatCardModule } from '@angular/material/card';

//import per il funzionamento dei grafici
import { HighchartsChartModule } from 'highcharts-angular';

//import per le pagine create da noi
import { AppComponent } from './app.component'; //creata già con la creazione del progetto
import { DashboardComponent } from './dashboard/dashboard.component';
import { LoginComponent } from './login/login.component';
import { TableComponent } from './table/table.component';
import { StoricoComponent } from './storico/storico.component';
import { CookieService } from "ngx-cookie-service";

@NgModule({
  declarations: [ //dichiarazione delle pagine create da noi
    AppComponent,
    DashboardComponent,
    LoginComponent,
    TableComponent,
    StoricoComponent
  ],
  imports: [ //import per i vari componenti usati nei file html
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatIconModule,
    MatToolbarModule,
    MatMenuModule,
    MatSidenavModule,
    MatDividerModule,
    MatListModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatCardModule,
    HighchartsChartModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
//@ts-ignore
export class AppModule { }
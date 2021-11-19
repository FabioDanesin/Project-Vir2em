import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

//import per le pagine create da noi
import { LoginComponent } from './login/login.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { TableComponent } from './table/table.component';
import { StoricoComponent } from './storico/storico.component';

const routes: Routes = [ 
  { path: '', redirectTo: '/login', pathMatch: 'full' }, //per dichiarare che come pagina prinicipale voglio quella di login
  { path: 'login', component: LoginComponent }, 
  { path: 'dashboard', component: DashboardComponent, children: [
    { path: 'table', component: TableComponent },
    { path: 'storico', component: StoricoComponent }
  ] } //per dichiarare la pagina dashboard in cui all'interno si può accedere alla pagina table
];

@NgModule ({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }

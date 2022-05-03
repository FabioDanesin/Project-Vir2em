import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

//import per le pagine create da noi
import { LoginComponent } from './login/login.component';
import { TableComponent } from './table/table.component';
import { StoricoComponent } from './storico/storico.component';
import { DashboardComponent } from './dashboard/dashboard.component';

const routes: Routes = [ 
  { path: '', redirectTo: '/login', pathMatch: 'full' }, //per dichiarare che come pagina prinicipale voglio quella di login
  { path: 'login', component: LoginComponent }, 
  { path: 'dashboard', component: DashboardComponent, children: [
    { path: 'table', component: TableComponent },
    { path: 'storico', component: StoricoComponent }
  ] } //per dichiarare la pagina dashboard in cui all'interno si può accedere alla pagina table e storico
];

@NgModule ({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }

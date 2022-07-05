import { Component, NgModule, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Globals } from 'src/globals';
import { AppRoutingModule } from '../app-routing.module';
import { AppComponent } from '../app.component';
const crypto  = require('crypto-js');
/*
@NgModule({
	declarations: [
		LoginComponent
	],
	imports: [
		BrowserModule,
		AppRoutingModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
*/


@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.css']
})
//@ts-ignore
export class LoginComponent implements OnInit {

	//DA SISTEMARE
	errorMessage = "";
	hide = true;
	url: string;
	debug = true;

	constructor(private router: Router) {
		//Ottengo i parametri URL dal file .ts
		const ip = Globals.VIR2EMAPI_IP;
		const port = Globals.VIR2EMAPI_PORT;
		const protocol = Globals.VIR2EMAPI_PROTOCOL;

		//Costruisco l'url
		this.url = `${protocol}://${ip}:${port}`;

		//Router per il rerouting della pagina.
		this.router = router;
	}

	ngOnInit(): void { }

	onClick(): void {
		//console.log("Parsing\n");

		function hash(p: string) {
			return crypto.SHA256(p);
		}
		const username = ((document.getElementById("username"))as HTMLInputElement)?.value;
		const password = ((document.getElementById("password"))as HTMLInputElement)?.value;

		if (!username || !password) {
			this.setErrorMessage("No data found");
		}
		else {

			//Creo il payload
			const body = {
				username: hash(username),
				password: hash(password)
			}

			//Body e header della richiesta
			let request_options: RequestInit = {
				method: "POST",
				body: JSON.stringify(body),
				redirect: "follow"
			};

			//Esecuzione e passaggio della callback per salvare il body
			const token_response = fetch(this.url + '/login', request_options);
			token_response
				.then(
					//Richiesta ritorna 200, ritorno il token e lo mantengo.
					(success: Response) => {
						success
							.text() // Brutto da morire ma TS mi costringe
							.then(
								(token) => {
									if(token != undefined)
									{	
										console.log(token);
										localStorage.setItem("access-token", token); //Storing del token
									}
									this.router.navigate(["/dashboard/table"]);
								}
							);
					},
					(failure: Response) => {
						//Ritornato errore. Invio messaggio di errore al frontend.
						//Setto errtxt per side effect. 
						let errtxt : string = "";
						failure.text().then(function(error){
							errtxt = error;
						})
						this.setErrorMessage(errtxt);
					}
				)
				.catch(
					(onerror) => {
						console.error(onerror);
					}
				);
		}
	}

	/**
	 * Funzione per mettere a schermo il messaggio di errore e ripulirlo.
	 */
	setErrorMessage(errormessage : string) {

		let innerHTML = document.getElementById('errors') as HTMLElement;
		innerHTML.innerHTML = errormessage
		setTimeout(function(){
			innerHTML.innerHTML = "";
		}, 10000);
	}
}

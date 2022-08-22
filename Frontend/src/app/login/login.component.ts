import { Component, NgModule, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { Globals } from 'src/globals';
import { AppRoutingModule } from '../app-routing.module';
import { AppComponent } from '../app.component';
var crypto = require("crypto-js");

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
	debug = true;

	constructor(
		private router: Router,
		private cookieservice : CookieService
		) {
		//Router per il rerouting della pagina.
		this.router = router;
	}

	ngOnInit(): void { }

	onClick(): void {
		//console.log("Parsing\n");

		function hash(p: string) {
			return crypto.SHA256(p).toString(crypto.enc.hex);
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
			//Setto l'header per contenuto della risposta.

			
			//Body e header della richiesta
			let request_options: RequestInit = {
				method: "POST",
				body: JSON.stringify(body),
				headers: {
					'content-type': 'application/json'
				},
				redirect: "follow"
			};

			//Esecuzione e passaggio della callback per salvare il body
			//linuxmanager
			const token_response = fetch(Globals.getUrl()+ '/login', request_options);

			token_response
				.then(
					//Richiesta ritorna 200, ritorno il token e lo mantengo.
					
					(success : Response) => {
						success
						.json()
						.then(
							(responseJson)=> {
								this.cookieservice.set('token', responseJson['token']);
								this.router.navigate(["/dashboard/table"]);
							}
						)
					},
					(failure) => {
						//Ritornato errore. Invio messaggio di errore al frontend.
						//Setto errtxt per side effect. 
						console.warn("Bad request:",failure);
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

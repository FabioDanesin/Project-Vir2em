import { Component, NgModule, OnInit } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { Globals } from 'src/globals';
import { AppRoutingModule } from '../app-routing.module';
import { AppComponent } from '../app.component';
const crypto  = require('crypto-js');

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

			//return crypto.createHash('sha256').update(p).digest('hex');
			return crypto.SHA256(p);
		}
		const username = document.getElementById("username");
		const password = document.getElementById("password");

		console.log("Scraping");

		if (!username || !password) {
			console.error("No data found");
			this.errorMessage = "No data found";
			this.getErrorMessage();
		}
		else {
			console.log(`Obtained : ${username} - ${password}`);

			//Creo e setto headers
			let headers = new Headers();
			
			headers.set("Content-Type", "application/json");
			headers.set("Accept", "application/json");

			//Debug. Da ignorare per la release
			if(this.url.match("*localhost*")){
				headers.set("Access-Control-Allow-Origin", "http://localhost:5000/"); //TODO:eliminare
				headers.set("Access-Control-Allow-Credentials", "true");	
			}
			
			//Creo il payload
			const body = {
				username: hash(username?.innerHTML),
				password: hash(password?.innerHTML)
			}

			//Body e header della richiesta
			let request_options: RequestInit = {
				method: "POST",
				headers: headers,
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
									console.log(token);
									localStorage.setItem("access-token", token); //Storing del token
									this.router.navigate(["/dashboard/table"]);
									console.log("success");

								}
							);
					},
					(failure: Response) => {
						//Ritornato errore. Invio messaggio di errore al frontend. 
						console.log(`status=${failure.status}`);
						console.log(failure);
						/**
						 
						 failure
						 .json()
							.then(
								(error_data) => {
									const parsed = JSON.parse(error_data);
									console.log(parsed);
									console.error(parsed.keys())
									this.errorMessage = parsed["$error"]
									this.getErrorMessage();
								}
							)
						*/
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
	getErrorMessage() {

		let innerHTML = document.getElementById('errors') as HTMLElement;
		console.log(this.errorMessage);
		innerHTML.innerHTML = this.errorMessage;
		this.errorMessage = "";

	}
}

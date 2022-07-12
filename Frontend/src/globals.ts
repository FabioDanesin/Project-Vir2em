
//Variabili globali usate in tutta l'applicazione
const Globals = {
    VIR2EMAPI_IP: "157.138.24.164",
    VIR2EMAPI_PROTOCOL: "http",
    VIR2EMAPI_PORT: 9000,
    /*
    VIR2EMAPI_IP: "localhost",
    VIR2EMAPI_PROTOCOL: "http",
    VIR2EMAPI_PORT: 8000,
    */

    getUrl : ()=>{
        return `${Globals.VIR2EMAPI_PROTOCOL}://${Globals.VIR2EMAPI_IP}:${Globals.VIR2EMAPI_PORT.toString()}`;
    }

}

export { Globals };

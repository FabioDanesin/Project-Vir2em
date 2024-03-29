import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts/highstock';
import HC_stock from 'highcharts/modules/stock';
import HC_exporting from 'highcharts/modules/exporting';
import HIndicatorsAll from "highcharts/indicators/indicators-all";
import HDragPanes from "highcharts/modules/drag-panes";
import HAnnotationsAdvanced from "highcharts/modules/annotations-advanced";
import HPriceIndicator from "highcharts/modules/price-indicator";
import HFullScreen from "highcharts/modules/full-screen";
import HStockTools from "highcharts/modules/stock-tools";

HIndicatorsAll(Highcharts);
HDragPanes(Highcharts);
HAnnotationsAdvanced(Highcharts);
HPriceIndicator(Highcharts);
HFullScreen(Highcharts);
HStockTools(Highcharts);
HC_exporting(Highcharts); 
HC_stock(Highcharts);

@Component({
   selector: 'app-storico',
   templateUrl: './storico.component.html',
   styleUrls: ['./storico.component.css']
})

//@ts-ignore
export class StoricoComponent implements OnInit {

   constructor(){}
   ngOnInit(): void {
   }

   //grafico 1: prova statica linea
   highcharts1 = Highcharts;
   chartOptions1: Highcharts.Options = {
      chart: {
         type: 'spline',
         height: 400,
      },
      title: {
         text: "Average Temperature"
      },
      xAxis: {
         categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
      },
      yAxis: {
         title: {
            text: "Temperature"
         }
      },
      series: [
         {
            name: 'Tokyo',
            type: 'spline',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6]
         },
         {
            name: 'New York',
            type: 'spline',
            data: [-0.2, 0.8, 5.7, 11.3, 17.0, 22.0, 24.8, 24.1, 20.1, 14.1, 8.6, 2.5]
         },
         {
            name: 'Berlin',
            type: 'spline',
            data: [-0.9, 0.6, 3.5, 8.4, 13.5, 17.0, 18.6, 17.9, 14.3, 9.0, 3.9, 1.0]
         },
         {
            name: 'London',
            type: 'spline',
            data: [3.9, 4.2, 5.7, 8.5, 11.9, 15.2, 17.0, 16.6, 14.2, 10.3, 6.6, 4.8]
         }
      ]
   }

   //grafico 2: prova statica istogramma
   highcharts2 = Highcharts;
   chartOptions2: Highcharts.Options = {
      chart: {
         type: 'column',
         height: 400,
      },
      title: {
         text: 'Monthly Average Rainfall'
      },
      xAxis: {
         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
         crosshair: true
      },
      yAxis: {
         min: 0,
         title: {
            text: 'Rainfall (mm)'
         }
      },
      tooltip: {
         headerFormat: '<span style = "font-size:10px">{point.key}</span><table>',
         pointFormat: '<tr><td style = "color:{series.color};padding:0">{series.name}: </td>' +
            '<td style = "padding:0"><b>{point.y:.1f} mm</b></td></tr>', footerFormat: '</table>', shared: true, useHTML: true
      },
      plotOptions: {
         column: {
            pointPadding: 0.2,
            borderWidth: 0
         }
      },
      series: [{
         name: 'Tokyo',
         type: 'column',
         data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
      },
      {
         name: 'New York',
         type: 'column',
         data: [83.6, 78.8, 98.5, 93.4, 106.0, 84.5, 105.0, 104.3, 91.2, 83.5, 106.6, 92.3]
      },
      {
         name: 'London',
         type: 'column',
         data: [48.9, 38.8, 39.3, 41.4, 47.0, 48.3, 59.0, 59.6,
            52.4, 65.2, 59.3, 51.2]
      },
      {
         name: 'Berlin',
         type: 'column',
         data: [42.4, 33.2, 34.5, 39.7, 52.6, 75.5, 57.4, 60.4,
            47.6, 39.1, 46.8, 51.1]
      }]
   }

   //prova statica 3 con stockchart e json
   highcharts5 = Highcharts;
   chartOptions5: Highcharts.Options = {
      rangeSelector: {
         selected: 1
       },
      chart: {
         type: 'spline',
         height: 400,
      },
      title: {
         text: 'Valori AAPL'
      },
      data: {
         rowsURL: 'https://demo-live-data.highcharts.com/aapl-c.json',
      }
   }
}


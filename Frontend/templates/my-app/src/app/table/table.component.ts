import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts';
import HC_data from 'highcharts/modules/data';
HC_data(Highcharts);

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css']
})

export class TableComponent implements OnInit {
   ngOnInit(): void { }

   public buttonClicked3: boolean = false;
   public onButtonClick3() { this.buttonClicked3 = !this.buttonClicked3; }

   public buttonClicked4: boolean = false;
   public onButtonClick4() { this.buttonClicked4 = !this.buttonClicked4; }

   //grafico 3: prova dinamica che si aggiorna da solo ogni seondo
   highcharts3 = Highcharts;
   chartOptions3: Highcharts.Options = {
      chart : {
         type: 'spline',
         height: 400,
         width: 800,
         events: {
            load: function () {
               // set up the updating of the chart each second
               var series = this.series[0];
               setInterval(function () {
                  var x = (new Date()).getTime(), // current time
                  y = Math.random();
                  series.addPoint([x, y], true, true);
               }, 1000);
            }
         }
      },
      title : {
         text: 'Live random data'   
      },   
      xAxis : {
         type: 'datetime',
         tickPixelInterval: 150
      },
      yAxis : {
         title: {
            text: 'Value'
         },
         plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
         }]
      },
      tooltip: {
         formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
            Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
            Highcharts.numberFormat(this.y, 2);
         }
      },
      plotOptions: {
         area: {
            pointStart: 1940,
            marker: {
               enabled: false,
               symbol: 'circle',
               radius: 2,
               states: {
                  hover: {
                     enabled: true
                  }
               }
            }
         }
      },
      legend: {
         enabled: false
      },
      exporting : {
         enabled: false
      },
      series : [{
         name: 'Random data',
         type: 'spline',
         data: (function () {
            var data = [],time = (new Date()).getTime(),i;
            for (i = -19; i <= 0; i += 1) {
               data.push({
                  x: time + i * 1000,
                  y: Math.random()
               });
            }
            return data;
         }())    
      }]
   }

   //grafico 4: prova dinamica a istogramma
   highcharts4 = Highcharts;
   chartOptions4: Highcharts.Options = { 
      chart: {
         type: 'bar',
         height: 600
     },
     title: {
         text: 'Server Monitoring Demo'
     },
     legend: {
         enabled: false
     },
     subtitle: {
         text: 'Instance Load'
     },
        data: {
            csvURL: 'https://demo-live-data.highcharts.com/vs-load.csv',
            enablePolling: true,
            dataRefreshRate: 1
        },
        plotOptions: {
            bar: {
                colorByPoint: true
            },
            series: {
                zones: [{
                    color: '#4CAF50',
                    value: 0
                }, {
                    color: '#8BC34A',
                    value: 10
                }, {
                    color: '#CDDC39',
                    value: 20
                }, {
                    color: '#CDDC39',
                    value: 30
                }, {
                    color: '#FFEB3B',
                    value: 40
                }, {
                    color: '#FFEB3B',
                    value: 50
                }, {
                    color: '#FFC107',
                    value: 60
                }, {
                    color: '#FF9800',
                    value: 70
                }, {
                    color: '#FF5722',
                    value: 80
                }, {
                    color: '#F44336',
                    value: 90
                }, {
                    color: '#F44336',
                    value: Number.MAX_VALUE
                }],
                dataLabels: {
                    enabled: true,
                    format: '{point.y:.0f}%'
                }
            }
        },
        tooltip: {
            valueDecimals: 1,
            valueSuffix: '%'
        },
        xAxis: {
            type: 'category',
            labels: {
                style: {
                    fontSize: '10px'
                }
            }
        },
        yAxis: {
            max: 100,
            plotBands: [{
                from: 0,
                to: 30,
                color: '#E8F5E9'
            }, {
                from: 30,
                to: 70,
                color: '#FFFDE7'
            }, {
                from: 70,
                to: 100,
                color: "#FFEBEE"
            }]
        }
    }
    
}
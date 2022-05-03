import { Component, OnInit } from '@angular/core';
import * as Highcharts from 'highcharts/highstock';
import HC_data from 'highcharts/modules/data';
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

   //grafico 3: con funzione che genera numeri random ogni secondo con stockchart
   highcharts3 = Highcharts;
   chartOptions3: Highcharts.Options = {
        chart : {
            height: 400,
            events: {
                load: function() {
                    var series1 = this.addSeries({
                    type: 'spline',
                    data: [
                        [(new Date()).getTime(), 5000]
                    ]
                    });
                    (function loop() {
                    var rand = Math.round(Math.random() * 100) + 500;
                    setTimeout(function() {
                        var timeStamp = (new Date()).getTime();
                        var shift1 = (timeStamp - series1.data[0].x) > 50000;
                        var y1 = 5000 + Math.round(Math.random() * 100);
                        series1.addPoint([timeStamp, y1], true, shift1);
                        loop();
                    }, rand);
                    }());
                }
            }
        },
        title: {
            text: 'Live random data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 1500
        },
        yAxis: {
            plotLines: [{
            value: 0,
            width: 1, 
            color: '#808080'
            }]
        },
        tooltip: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        exporting: {
            enabled: false
        }
   }

   //grafico 4: prova dinamica a istogramma e csv
   highcharts4 = Highcharts;
   chartOptions4: Highcharts.Options = { 
        chart: {
            type: 'bar',
            height: 600,
        },
        title: {
            text: 'Server Monitoring Demo'
        },
        legend: {
            enabled: false
        },
        exporting: {
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
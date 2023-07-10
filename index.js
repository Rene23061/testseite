import ApexCharts from '/root/node_modules/apexcharts';

import WebSocket from './root/node_modules/ws';

const chartOptions = {
  series: [{
    data: []
  }],
  chart: {
    type: 'candlestick',
    height: 400
  },
  title: {
    text: 'Candlestick Chart'
  },
  xaxis: {
    type: 'datetime'
  },
  yaxis: {
    tooltip: {
      enabled: true
    }
  }
};

const chart = new ApexCharts(document.getElementById('chart-container'), chartOptions);
chart.render();

const ws = new WebSocket('wss://eule-trading.site:8000');

ws.onopen = () => {
  console.log('WebSocket-Verbindung hergestellt');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);

  // Überprüfen, ob die empfangene Nachricht Kerzendaten enthält
  if (message.type === 'candle') {
    const candleData = message.data;

    // Aktualisieren Sie die Chart-Daten mit den empfangenen Kerzendaten
    chart.updateSeries([{
      data: [...chartOptions.series[0].data, candleData]
    }]);
  }
};

ws.onclose = () => {
  console.log('WebSocket-Verbindung geschlossen');
};

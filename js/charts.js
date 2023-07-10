console.log('Das Skript wurde geladen.');

window.addEventListener('DOMContentLoaded', function() {
  // Funktion zum Neu laden des Charts
  function reloadChart() {
    // Code zum Neu laden des Charts hier einfügen
    fetch('./side/chart_cash.php')
      .then(response => response.json())
      .then(data => {
        // Funktion zum Filtern der Daten basierend auf dem Zeitintervall
        function filterDataByInterval(interval) {
          var currentDate = new Date(); // Aktuelles Datum und Uhrzeit
          var filteredData = data.filter(item => {
            var timestamp = new Date(item.timestamp);
            var diff = currentDate - timestamp;

            if (interval === 'hour') {
              // Daten der letzten Stunde
              return diff <= 60 * 60 * 1000; // 60 Minuten * 60 Sekunden * 1000 Millisekunden
            } else if (interval === 'day') {
              // Daten des letzten Tages
              return diff <= 24 * 60 * 60 * 1000; // 24 Stunden * 60 Minuten * 60 Sekunden * 1000 Millisekunden
            } else if (interval === 'week') {
              // Daten der letzten Woche
              return diff <= 7 * 24 * 60 * 60 * 1000; // 7 Tage * 24 Stunden * 60 Minuten * 60 Sekunden * 1000 Millisekunden
            } else if (interval === 'month') {
              // Daten des letzten Monats
              var currentMonth = currentDate.getMonth();
              var currentYear = currentDate.getFullYear();
              var itemMonth = timestamp.getMonth();
              var itemYear = timestamp.getFullYear();

              return currentYear === itemYear && currentMonth === itemMonth;
            }
          });

          fetch('./side/chart_cash.php')
          .then(response => response.json())
          .then(data => {
            // Ihr Chart-Code hier
          })
          .catch(error => console.log(error));
          return filteredData;
        }

        window.addEventListener('popstate', function() {
          console.log('popstate event triggered');
          console.log('chart-spot width:', document.getElementById('chart-spot').offsetWidth);
          console.log('chart-spot height:', document.getElementById('chart-future').offsetHeight);
          reloadChart();
        });

        // Standardmäßig Daten der letzten Stunde anzeigen
        var filteredData = filterDataByInterval('hour');
        var timestamps = filteredData.map(item => item.timestamp);
        var spotData = filteredData.map(item => item.betrag_spot);
        var futureData = filteredData.map(item => item.betrag_future);

        var ctxSpot = document.getElementById('chart-spot').getContext('2d');
        var ctxFuture = document.getElementById('chart-future').getContext('2d');

        var spotChart = new Chart(ctxSpot, {
          type: 'line',
          data: {
            labels: timestamps,
            datasets: [{
              label: 'Spot',
              data: spotData,
              borderColor: 'orange',
              backgroundColor: 'transparent',
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: 'Zeit'
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'Betrag'
                }
              }
            }
          }
        });

        var futureChart = new Chart(ctxFuture, {
          type: 'line',
          data: {
            labels: timestamps,
            datasets: [{
              label: 'Future',
              data: futureData,
              borderColor: 'orange',
              backgroundColor: 'transparent',
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                display: true,
                title: {
                  display: true,
                  text: 'Zeit'
                }
              },
              y: {
                display: true,
                title: {
                  display: true,
                  text: 'Betrag'
                }
              }
            }
          }
        });

        // Event Listener für die Buttons
        var dayButton = document.getElementById('day-button');
        var weekButton = document.getElementById('week-button');
        var monthButton = document.getElementById('month-button');

        dayButton.addEventListener('click', function() {
          var filteredData = filterDataByInterval('day');
          var timestamps = filteredData.map(item => item.timestamp);
          var spotData = filteredData.map(item => item.betrag_spot);
          var futureData = filteredData.map(item => item.betrag_future);

          spotChart.data.labels = timestamps;
          spotChart.data.datasets[0].data = spotData;
          spotChart.update();

          futureChart.data.labels = timestamps;
          futureChart.data.datasets[0].data = futureData;
          futureChart.update();
        });

        weekButton.addEventListener('click', function() {

          var filteredData = filterDataByInterval('month');
          var timestamps = filteredData.map(item => item.timestamp);
          var spotData = filteredData.map(item => item.betrag_spot);
          var futureData = filteredData.map(item => item.betrag_future);

          spotChart.data.labels = timestamps;
          spotChart.data.datasets[0].data = spotData;
          spotChart.update();

          futureChart.data.labels = timestamps;
          futureChart.data.datasets[0].data = futureData;
          futureChart.update();
        });
      });
  }

  // Chart beim Seitenladen initial laden
  reloadChart();

  // Chart beim Wechseln zwischen internen Links neu laden
  window.addEventListener('popstate', function() {
    reloadChart();
  });
});

window.addEventListener('popstate', function() {
  setTimeout(reloadChart, 100); // Warten Sie 100 Millisekunden, bevor Sie den Chart neu laden
});
<?php
session_start();
include('../check_session.php');
include('../mysql.php');
// Rest von home.php Code...
?>  
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script src="/js/coininfo.js"></script>
        <div class="timeline-left">

        <div class="intro box">
            <div class="intro-title">
              Signale
            </div>
            <div class="info">
            <table class="signal">
            <h3>API Logs</h3>
              <tr>
                  <th>Datum</th>
                  <th>Info</th>
              </tr>
              <?php
                  // Lese den Inhalt der Datei
                  $content = file_get_contents('../api_response.txt');
                  // Suche nach dem Pattern, das zu JSON-Objekten passt
                  $pattern = '/\{.*?"msg":"(.*?)","requestTime":(\d+).*?\}/';
                  preg_match_all($pattern, $content, $matches, PREG_SET_ORDER);
                  // Sortiere die Matches nach dem neuesten Datum zuerst
                  usort($matches, function($a, $b) {
                      return $b[2] - $a[2];
                  });
                  // Begrenze die Anzahl der anzuzeigenden Zeilen auf maximal fünf
                  $matches = array_slice($matches, 0, 3);
                  // Erzeuge die Tabellenzeilen
                  foreach ($matches as $match) {
                      echo '<tr>';
                      echo '<td>' . date('m-d H:i:s', $match[2]/1000) . '</td>';
                      echo '<td>' . $match[1] . '</td>';
                      echo '</tr>';
                  }
              ?>
          </table>
          </div>
          <div class="info">
          <h3>TradingView Signale</h3>
          <table class="signal">
    <tr>
        <th>Timestamp</th>
        <th>Symbol</th>
        <th>Direction</th>
    </tr>
    <?php
        // SQL-Abfrage ausführen
        $result = $conn->query('SELECT timestamp, symbol, direction FROM TradingViewAlerts ORDER BY timestamp DESC LIMIT 3');

        // Daten abrufen und in der Tabelle anzeigen
        while ($row = $result->fetch_assoc()) {
            echo '<tr>';
            echo '<td>' . date('m-d H:i:s', strtotime($row['timestamp'])) . '</td>'; // Jahr aus dem Zeitstempel entfernen
            echo '<td>' . str_replace('USDT.P', '', $row['symbol']) . '</td>'; // "USDT.P" aus dem Symbol entfernen
            echo '<td>' . str_replace('open_', '', $row['direction']) . '</td>'; // "open_" aus der Richtung entfernen
            echo '</tr>';
        }
    ?>
</table>
            </div>
          </div>


          <div class="event box">
gggggg
          </div>
          <div class="pages box">
ggggg
          </div>
        </div>
        <div class="timeline-right">
        <div class="album box">
    <div class="status-menu">
        <div class="intro-title">Kontostand</div>
    </div>
    <div class="status-main">
        <div class="cash-coin-box">
            <div class="cash-h">Spot</div>
            <div class="cash-cs"></div>
        </div>
        <div class="cash-coin-box">
            <div class="cash-h">Verfügbarer Bertag</div>
            
            <div class="cash-ce"></div>
        </div>
        <div class="cash-coin-box">
            <div class="cash-h">Future</div>
            <div class="cash-cf"></div>
        </div>
        <div class="cash-coin-box">
            <div class="cash-h">Gesamt Betrag</div>
            <div class="cash-c"></div>
        </div>
    </div>
</div>
            <div class="status box">
                <div class="status-menu">
                        <div class="intro-title">Balance</div>
                </div>
                        <div class="status-main">
                            <div class="chartbox">
                            <canvas id="chart-spot" style="height: 150px;"></canvas>
                                    </div>
                                        <div class="chartbox">
                                <button id="day-button">Tag</button>
                            <button id="week-button">Woche</button>
                            <button id="month-button">Monat</button>
                            </div>
                        <div class="chartbox">
                        <canvas id="chart-future" style="height: 150px;"></canvas>
                    </div>
                </div>
            </div>
            <?php include './side/bilance_charts.php'; ?>

        <div class="status box">
        <div class="status-menu">
        <div class="intro-title">Gehaltene Coins</div>
    </div>
    <div class="status-main-coin">
        <?php include '../loader.php'; ?>
    </div>
</div>
</div>
</div>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
$(document).ready(function() {
    // Funktion zum Aktualisieren des Gesamtguthabens
    function updateTotalBalance() {
        var spotBalance = parseFloat($('.cash-cs').text()); // Spot-Guthaben auslesen und in eine Gleitkommazahl konvertieren
        var futureBalance = parseFloat($('.cash-cf').text()); // Future-Guthaben auslesen und in eine Gleitkommazahl konvertieren

        // Überprüfen, ob die Werte gültige Zahlen sind (nicht NaN)
        if (isNaN(spotBalance)) {
            spotBalance = 0;
        }
        if (isNaN(futureBalance)) {
            futureBalance = 0;
        }

        var totalBalance = spotBalance + futureBalance; // Beide Guthaben addieren

        $('.cash-c').text(totalBalance.toFixed(2) + ' $'); // Gesamtguthaben aktualisieren
    }

    // Funktion zum Aktualisieren des Future-Guthabens
    function updateFutureBalance() {
        $.ajax({
            url: './side/bitget-futures-usd.php',
            success: function(data) {
                $('.cash-cf').html('' + data + ' $');
                updateTotalBalance(); // Gesamtguthaben aktualisieren, nachdem das Future-Guthaben aktualisiert wurde
            },
            error: function(xhr, status, error) {
                console.error('AJAX Fehler: ' + status + error);
            }
        });
    }

    // Funktion zum Aktualisieren des Equity-Guthabens
    function updateEquityBalance() {
        $.ajax({
            url: './side/bitgt-futures-equity.php',
            success: function(data) {
                $('.cash-ce').html('' + data + ' $');
            },
            error: function(xhr, status, error) {
                console.error('AJAX Fehler: ' + status + error);
            }
        });
    }

    // Funktion zum Aktualisieren des Future-Guthabens alle 10 Sekunden
    setInterval(updateFutureBalance, 1000);

    // Funktion zum Aktualisieren des Equity-Guthabens alle 5 Sekunden
    setInterval(updateEquityBalance, 5000);
});
  </script>
  <script>
document.getElementById('day-button').addEventListener('click', function() {
  // Aktualisieren Sie die Diagramme für den Tag
});

document.getElementById('week-button').addEventListener('click', function() {
  // Aktualisieren Sie die Diagramme für die Woche
});

document.getElementById('month-button').addEventListener('click', function() {
  // Aktualisieren Sie die Diagramme für den Monat
});
</script>

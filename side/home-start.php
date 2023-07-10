<?php
session_start();

include('../check_session.php');
include('get_user_info.php');
// Rest von home.php Code...
?>  
<script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
<link href="https://cdn.jsdelivr.net/npm/apexcharts/dist/apexcharts.css" rel="stylesheet">
  </style>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script>
    $(document).ready(function() {
      // Funktion zum Aktualisieren des Gesamtguthabens
      function updateTotalBalance() {
        var spotBalance = parseFloat($('.spot-info-item').text()); // Spot-Guthaben auslesen und in eine Gleitkommazahl konvertieren
        var futureBalance = parseFloat($('.future-info-item').text()); // Future-Guthaben auslesen und in eine Gleitkommazahl konvertieren

      }

    });
  </script>
  <script>
    $(document).ready(function() {
      // Funktion zum Aktualisieren des Future-Guthabens
      function updateFutureBalance() {
        $.ajax({
    url: './side/bitget-futures-usd.php',
    success: function(data) {
        $('.future-info-item').html('' + data + ' $');
    },
    error: function(xhr, status, error) {
        console.error('AJAX Fehler: ' + status + error);
    }
});
      }

      // Funktion zum Aktualisieren des Future-Guthabens alle 1 Sekunden
      setInterval(updateFutureBalance, 1000);

    });
  </script>
<script src="/js/coininfo.js" type="module"></script>
  <div class="timeline-left">
<div class="intro box">
<div class="intro-title">Guthaben Spot / Future</div>
  <div class="intro-title">
  </div>
  <div class="info">
  <table class="invisible-table">
                <tr>
                  <th>Spot</th>
                  <th>Future</th>
                </tr>
                <tr>
                  <td class="spot-info-item">
                    <!-- Ihr Kontostand für Spot -->
                  </td>
                  <td class="future-info-item">
                    <!-- Ihr Kontostand für Future -->
                  </td>
                </tr>
              </table>
  </div>
</div>

            <div class="event box">
            <div class="intro-title">Guthaben Spot / Future</div>
dfdfdddfdd
            </div>
            <div class="pages box">
              <div class="intro-title">
                Your pages
              </div>
              <div class="user">
                <img src="https://images.unsplash.com/photo-1549068106-b024baf5062d?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&ixid=eyJhcHBfaWQiOjE3Nzg0f" alt="" class="user-img">
                <div class="username">Chandelio</div>
              </div>
              <div class="user">
                <img src="https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?ixlib=rb-0.3.5&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&s=d5849d81af587a09dbcf3f11f6fa122f" alt="" class="user-img">
                <div class="username">Janet Jolie</div>
              </div>
              <div class="user">
                <img src="https://images.unsplash.com/photo-1546539782-6fc531453083?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=200&fit=max&ixid=eyJhcHBfaWQiOjE3Nzg0fQ" alt="" class="user-img">
                <div class="username">Patrick Watsons</div>
              </div>
            </div>
          </div>
          <div class="timeline-right">
          <div class="status box">
    <div class="status-menu">
        <div class="intro-title">Balance</div>
    </div>
   hier der chart
</div>
            <div class="album box">
              <div class="status-main">
                <div class="intro-title">Gehaltene Coins</div>
              </div>
                <div class="album-content">        
                  <?php include '../test3.php'; ?>
              </div>
            </div>
          </div>
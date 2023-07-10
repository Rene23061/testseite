<?php
session_start();
include('check_session.php');
include('side/get_user_info.php');
?>
<!DOCTYPE html>
<html lang="de" >
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CodePen - Responsive Social Platform UI</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
  <script src='https://cdn.jsdelivr.net/gh/alpinejs/alpine@v1.9.4/dist/alpine.js'></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>


<link rel="stylesheet" href="./css/home.css">

</head>
<body>
<!-- partial:index.partial.html -->
<div class="container" x-data="{ rightSide: false, leftSide: false }">
  <div class="left-side" :class="{'active' : leftSide}">
    <div class="left-side-button" @click="leftSide = !leftSide">
      <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
      <svg stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
  <path d="M19 12H5M12 19l-7-7 7-7"/>
</svg>
    </div>
    <div class="logo">ULTRANET</div>
    <div class="side-wrapper">
      <div class="side-title">MENU</div>
      <div class="side-menu">
      <a href="#" id="home-link" class="home-link active">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <path d="M19.31 18.9C19.75 18.21 20 17.38 20 16.5C20 14 18 12 15.5 12S11 14 11 16.5 13 21 15.5 21C16.37 21 17.19 20.75 17.88 20.32L21 23.39L22.39 22L19.31 18.9M15.5 19C14.12 19 13 17.88 13 16.5S14.12 14 15.5 14 18 15.12 18 16.5 16.88 19 15.5 19M5 20V12H2L12 3L22 12H20.18C19.33 11.11 18.23 10.47 17 10.18L12 5.69L7 10.19V18H9.18C9.35 18.72 9.64 19.39 10.03 20H5Z" fill="rgba(255,255,255,1)"></path> 
          </svg>
          Home
        </a>
        <a href="#" class="trade-button" id="trade-link">
          <svg stroke="currentColor" stroke-width="1" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <path d="M6,16.5L3,19.44V11H6M11,14.66L9.43,13.32L8,14.64V7H11M16,13L13,16V3H16M18.81,12.81L17,11H22V16L20.21,14.21L13,21.36L9.53,18.34L5.75,22H3L9.47,15.66L13,18.64" fill="rgba(255,255,255,1)"></path>
          </svg>
          Aktuelle Trades 
        </a>
        <a href="#" id="bot-link">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <path d="M22 14H21C21 10.13 17.87 7 14 7H13V5.73C13.6 5.39 14 4.74 14 4C14 2.9 13.11 2 12 2S10 2.9 10 4C10 4.74 10.4 5.39 11 5.73V7H10C6.13 7 3 10.13 3 14H2C1.45 14 1 14.45 1 15V18C1 18.55 1.45 19 2 19H3V20C3 21.11 3.9 22 5 22H19C20.11 22 21 21.11 21 20V19H22C22.55 19 23 18.55 23 18V15C23 14.45 22.55 14 22 14M21 17H19V20H5V17H3V16H5V14C5 11.24 7.24 9 10 9H14C16.76 9 19 11.24 19 14V16H21V17M17.5 15.5C17.5 16.61 16.61 17.5 15.5 17.5C14.53 17.5 13.73 16.81 13.54 15.9L16.5 13.78C17.1 14.13 17.5 14.76 17.5 15.5M7.5 13.78L10.46 15.9C10.28 16.81 9.47 17.5 8.5 17.5C7.4 17.5 6.5 16.61 6.5 15.5C6.5 14.76 6.9 14.13 7.5 13.78Z" fill="rgba(255,255,255,1)">
          </svg>
          Trade Bots
        </a>
        <a href="#" id="history-link">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
          <path d="M21 11.11V5C21 3.9 20.11 3 19 3H14.82C14.4 1.84 13.3 1 12 1S9.6 1.84 9.18 3H5C3.9 3 3 3.9 3 5V19C3 20.11 3.9 21 5 21H11.11C12.37 22.24 14.09 23 16 23C19.87 23 23 19.87 23 16C23 14.09 22.24 12.37 21 11.11M12 3C12.55 3 13 3.45 13 4S12.55 5 12 5 11 4.55 11 4 11.45 3 12 3M5 19V5H7V7H17V5H19V9.68C18.09 9.25 17.08 9 16 9H7V11H11.1C10.5 11.57 10.04 12.25 9.68 13H7V15H9.08C9.03 15.33 9 15.66 9 16C9 17.08 9.25 18.09 9.68 19H5M16 21C13.24 21 11 18.76 11 16S13.24 11 16 11 21 13.24 21 16 18.76 21 16 21M16.5 16.25L19.36 17.94L18.61 19.16L15 17V12H16.5V16.25Z" fill="rgba(255,255,255,1)">
          </svg>
          History
        </a>
        <a href="#" id="stat-link">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17.5 16.82L19.94 18.23L19.19 19.53L16 17.69V14H17.5V16.82M24 17C24 20.87 20.87 24 17 24S10 20.87 10 17C10 16.66 10.03 16.33 10.08 16H2V4H20V10.68C22.36 11.81 24 14.21 24 17M10.68 14C10.86 13.64 11.05 13.3 11.28 12.97C11.19 13 11.1 13 11 13C9.34 13 8 11.66 8 10S9.34 7 11 7 14 8.34 14 10C14 10.25 13.96 10.5 13.9 10.73C14.84 10.27 15.89 10 17 10C17.34 10 17.67 10.03 18 10.08V8C16.9 8 16 7.11 16 6H6C6 7.11 5.11 8 4 8V12C5.11 12 6 12.9 6 14H10.68M22 17C22 14.24 19.76 12 17 12S12 14.24 12 17 14.24 22 17 22 22 19.76 22 17Z" fill="rgba(255,255,255,1)">
          </svg>
          Statistik
        </a>
        <a href="#" id="spot-link">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14.24 10.56C13.93 11.8 12 11.17 11.4 11L11.95 8.82C12.57 9 14.56 9.26 14.24 10.56M11.13 12.12L10.53 14.53C11.27 14.72 13.56 15.45 13.9 14.09C14.26 12.67 11.87 12.3 11.13 12.12M21.7 14.42C20.36 19.78 14.94 23.04 9.58 21.7C4.22 20.36 .963 14.94 2.3 9.58C3.64 4.22 9.06 .964 14.42 2.3C19.77 3.64 23.03 9.06 21.7 14.42M14.21 8.05L14.66 6.25L13.56 6L13.12 7.73C12.83 7.66 12.54 7.59 12.24 7.53L12.68 5.76L11.59 5.5L11.14 7.29C10.9 7.23 10.66 7.18 10.44 7.12L10.44 7.12L8.93 6.74L8.63 7.91C8.63 7.91 9.45 8.1 9.43 8.11C9.88 8.22 9.96 8.5 9.94 8.75L8.71 13.68C8.66 13.82 8.5 14 8.21 13.95C8.22 13.96 7.41 13.75 7.41 13.75L6.87 15L8.29 15.36C8.56 15.43 8.82 15.5 9.08 15.56L8.62 17.38L9.72 17.66L10.17 15.85C10.47 15.93 10.76 16 11.04 16.08L10.59 17.87L11.69 18.15L12.15 16.33C14 16.68 15.42 16.54 16 14.85C16.5 13.5 16 12.7 15 12.19C15.72 12 16.26 11.55 16.41 10.57C16.61 9.24 15.59 8.53 14.21 8.05Z" fill="rgba(255,255,255,1)">
          </svg>
          Spot Coins
        </a>
      </div>
    </div>
    <div class="side-wrapper">
      <div class="side-title">Einstellungen</div>
      <div class="side-menu">
      <a href="#" id="prof-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22,3H2C0.91,3.04 0.04,3.91 0,5V19C0.04,20.09 0.91,20.96 2,21H22C23.09,20.96 23.96,20.09 24,19V5C23.96,3.91 23.09,3.04 22,3M22,19H2V5H22V19M14,17V15.75C14,14.09 10.66,13.25 9,13.25C7.34,13.25 4,14.09 4,15.75V17H14M9,7A2.5,2.5 0 0,0 6.5,9.5A2.5,2.5 0 0,0 9,12A2.5,2.5 0 0,0 11.5,9.5A2.5,2.5 0 0,0 9,7M14,7V8H20V7H14M14,9V10H20V9H14M14,11V12H18V11H14" fill="rgba(255,255,255,1)">  
        </svg>
          Profil Übersicht
        </a>
        <a href="#" id="edit-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 17V20H10V18.11H3.9V17C3.9 16.36 7.03 14.9 10 14.9C10.96 14.91 11.91 15.04 12.83 15.28L14.35 13.76C12.95 13.29 11.5 13.03 10 13C7.33 13 2 14.33 2 17M10 4C7.79 4 6 5.79 6 8S7.79 12 10 12 14 10.21 14 8 12.21 4 10 4M10 10C8.9 10 8 9.11 8 8S8.9 6 10 6 12 6.9 12 8 11.11 10 10 10M21.7 13.35L20.7 14.35L18.65 12.35L19.65 11.35C19.86 11.14 20.21 11.14 20.42 11.35L21.7 12.63C21.91 12.84 21.91 13.19 21.7 13.4M12 18.94L18.06 12.88L20.11 14.88L14.11 20.95H12V18.94" fill="rgba(255,255,255,1)">
          </svg>
          Edit Profil
        </a>
        <a href="#" id="wallet-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5,3C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V16.72C21.59,16.37 22,15.74 22,15V9C22,8.26 21.59,7.63 21,7.28V5A2,2 0 0,0 19,3H5M5,5H19V7H13A2,2 0 0,0 11,9V15A2,2 0 0,0 13,17H19V19H5V5M13,9H20V15H13V9M16,10.5A1.5,1.5 0 0,0 14.5,12A1.5,1.5 0 0,0 16,13.5A1.5,1.5 0 0,0 17.5,12A1.5,1.5 0 0,0 16,10.5Z" fill="rgba(255,255,255,1)"> 
          </svg>
          Wallets
        </a>
        <a href="#" id="key-link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 8C7.3 8 6 9.3 6 11S7.3 14 9 14C10.3 14 11.4 13.2 11.8 12H14V14H16V12H18V10H11.8C11.4 8.8 10.3 8 9 8M9 12C8.4 12 8 11.6 8 11S8.4 10 9 10 10 10.4 10 11 9.6 12 9 12M15 20C15 19.5 14.6 19 14 19H13V17H19C20.1 17 21 16.1 21 15V7C21 5.9 20.1 5 19 5H13L11 3H5C3.9 3 3 3.9 3 5V15C3 16.1 3.9 17 5 17H11V19H10C9.4 19 9 19.5 9 20H2V22H9C9 22.5 9.4 23 10 23H14C14.6 23 15 22.5 15 22H22V20H15M5 15V7H19V15H5Z" fill="rgba(255,255,255,1)"> 
          </svg>
          Keys
        </a>

      </div>
    </div>
    <a href="?logout" class="follow-me">
      <svg fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5.636 5.636a9 9 0 1012.728 0M12 3v9" />
    </svg>
        <span class="follow-text">
          Logout
       </span>
        <span class="developer">
        <svg fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M5.636 5.636a9 9 0 1012.728 0M12 3v9" />
    </svg>
    Log Out</span>
      </a>
  </div>
  <div class="main">
    <div class="main-container">
    <div class="profile">
    <div class="profile-avatar">
            <img src="<?php echo $_SESSION['avatar']; ?>" alt="" class="profile-img">
            <div class="profile-name"><?php echo $_SESSION['username']; ?></div>
        </div>
      <img src="imc/head.png" alt="" class="profile-cover">
    </div>

    <div class="timeline">
      
    </div>
    
  </div>
  </div>
  <div class="right-side" :class="{ 'active': rightSide }">
    <div class="account">
INFOS
    </div>
    <div class="side-wrapper stories">
    <div class="info">
    <table class="signal">
    <h3>Aktive Positionen</h3>
    <tr>
        <th>Order</th>
        <th>P/L</th>
    </tr>
    <tbody id="position-data">
        <!-- Hier werden die Positionen eingefügt -->
    </tbody>
</table>
<!-- JavaScript zum Ändern des Links -->
<script>
function updateTable() {
  // Fetch data from the API
  fetch('side/bitget-positions.php')
    .then(response => response.json())
    .then(data => {
      // Get the table body
      let tableBody = document.getElementById('position-data');

      // Clear the table body
      tableBody.innerHTML = '';

      // Loop through the data
      data.forEach(item => {
        // Create a new row and cells
        let row = document.createElement('tr');
        let orderCell = document.createElement('td');
        let plCell = document.createElement('td');

        // Set the text content of the cells
        orderCell.textContent = item.symbol.replace('USDT_UMCBL', '');
        plCell.textContent = `$ ${parseFloat(item.unrealizedPL).toFixed(2)}`;

        // Color the P/L cell based on the value
        plCell.style.color = item.unrealizedPL < 0 ? 'red' : 'green';

        // Add the cells to the row
        row.appendChild(orderCell);
        row.appendChild(plCell);

        // Add the row to the table body
        tableBody.appendChild(row);
      });
    });
}

// Update the table immediately and then every 1 seconds
updateTable();
setInterval(updateTable, 1000);
</script>
</div>
<button class="button-m" id="trade-link">more Trades</button>
</div>
<div class="account">
History
    </div>
    <div class="side-wrapper contacts">
    <div class="info">

<?php
// Binden Sie die Datei ein und speichern Sie die zurückgegebenen Daten
$orderData = include('side/bitget-history.php');

// Verwenden Sie die Daten, um die Tabelle zu erzeugen
echo '<table class="signal">';
echo '<h3>Trade History</h3>';
echo '<tr>';
echo '<th>Coin</th>';
echo '<th>Side</th>';
echo '<th>P/L</th>';
echo '</tr>';
echo '<tbody id="position-data">';

$counter = 0;
foreach ($orderData as $order) {
    echo '<tr>';
    echo '<td>' . $order['symbol'] . '</td>';
    echo '<td>' . $order['posSide'] . '</td>';
    echo '<td style="color:' . $order['profitsColor'] . ';">' . number_format($order['totalProfits'], 2) . '</td>';
    echo '</tr>';

    $counter++;
    if ($counter >= 5) {
        break;
    }
}

echo '</tbody>';
echo '</table>';

?>
      </div>
      <button class="history-button" id="trade-link">more History</button>
    </div>
  </div>
</div>
<!-- partial -->
<script>

</script>

<script>
$(document).ready(function(){
  // Laden Sie home-start.php beim Start der Seite
  $(".timeline").load("side/home-start1.php");

  $("#home-link").click(function(e){
  e.preventDefault();
  $(".timeline").load("side/home-start1.php", function() {
    // Code zum Erstellen des Charts und Anhängen der Event-Listener hier einfügen
  });
  $('a.active').removeClass('active');
  $(this).addClass('active');
});

  $("#trade-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/trade.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $(".button-m").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/trade.php");
    $('a.active').removeClass('active');
    $('#trade-link').addClass('active');
  });

  $("#history-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/history.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $(".history-button").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/history.php");
    $('a.active').removeClass('active');
    $('#history-link').addClass('active');
  });

  $("#bot-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/bot.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#stat-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/statistik.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#spot-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/spotcoin.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#prof-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/prof.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#edit-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/edit.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#wallet-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/wallet.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

  $("#key-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/keys.php");
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

});
</script>
</body>
</html>

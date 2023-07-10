<?php
include('check_session.php');
?>
<!DOCTYPE html>
<html lang="en" >
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>CodePen - Responsive Social Platform UI</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/5.0.0/normalize.min.css">
<link rel="stylesheet" href="css/home.css">
<script src="https://cdn.jsdelivr.net/npm/apexcharts@latest"></script>
</head>
<body>
<body>
<?php
if (isset($_GET['show_popup']) && !isset($_COOKIE['popup_shown'])) {
  echo "<script>
  setTimeout(function() {
      alert('Willkommen " . $_SESSION['username'] . "! Deine Daten werden geladen!');
      location.reload();
  }, 1000);
</script>";

    // Setzen Sie den Cookie, um das Popup als angezeigt zu markieren
    setcookie('popup_shown', '1', time() + (86400 * 30), '/'); // Gültig für 30 Tage
}
?>
<!-- partial:index.partial.html -->
<div class="container" x-data="{ rightSide: false, leftSide: false }">
    <div class="left-side" :class="{'active' : leftSide}">
      <div class="left-side-button" @click="leftSide = !leftSide">
        <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>
        <svg stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
    <path d="M19 12H5M12 19l-7-7 7-7"/>
  </svg>
      </div>
      <div class="logo">EULE-Trading-BOT</div>
      <div class="side-wrapper">
        <div class="side-title">MENU</div>
        <div class="side-menu">
        <a href="#" id="home-link" class="active">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M8.25 21v-4.875c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21m0 0h4.5V3.545M12.75 21h7.5V10.75M2.25 21h1.5m18 0h-18M2.25 9l4.5-1.636M18.75 3l-1.5.545m0 6.205l3 1m1.5.5l-1.5-.5M6.75 7.364V3h-3v18m3-13.636l10.5-3.819" />
              <path d="M9 22V12h6v10" />
            </svg>
            Home
          </a>
          <a href="#">
            <svg stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.631 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.699 2.7c-.103.021-.207.041-.311.06a15.09 15.09 0 01-2.448-2.448 14.9 14.9 0 01.06-.312m-2.24 2.39a4.493 4.493 0 00-1.757 4.306 4.493 4.493 0 004.306-1.758M16.5 9a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"></path>
            </svg>
            Latest News
          </a>
          <a href="#">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor"  width="24" height="24" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
            <path d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"></path>
              <circle cx="12" cy="10" r="3" /></svg>
            Explore
          </a>
          <a href="#">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
              <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
              <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" />
            </svg>
            Files
          </a>
          <a href="#">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              <circle cx="8.5" cy="8.5" r="1.5" />
              <path d="M21 15l-5-5L5 21" />
            </svg>
            Galery
          </a>
          <a href="#">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <path d="M16 2v4M8 2v4M3 10h18" />
            </svg>
            Events
          </a>
        </div>
      </div>
      <div class="side-wrapper">
        <div class="side-title">YOUR FAVOURITE</div>
        <div class="side-menu">
          <a href="#" id="settings">
            <svg fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"></path>
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            </svg>
            Persönliche Einstellungen
          </a>
          <a href="#">
scg hier
            Birds
          </a>
          <a href="#">
hier svg
            Nature
          </a>
          <a href="#">
hier svg
            Animals
          </a>
          <a href="#">
hier svg
            Motobike
          </a>
          <a href="#">
hier svg
            Dance
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
    <div class="main-container">
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
      </div>
    </div>  
<!-- partial -->
  <script src='https://cdn.jsdelivr.net/gh/alpinejs/alpine@v1.9.4/dist/alpine.js'></script>
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
$(document).ready(function(){
  // Laden Sie home-start.php beim Start der Seite
  $(".timeline").load("side/home-start.php");

  $("#home-link").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/home-start.php");
    // Setzen Sie alle Links auf nicht aktiv und machen Sie diesen Link aktiv
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });
  
  $("#settings").click(function(e){
    e.preventDefault();
    $(".timeline").load("side/settings.php");
    // Setzen Sie alle Links auf nicht aktiv und machen Sie diesen Link aktiv
    $('a.active').removeClass('active');
    $(this).addClass('active');
  });

});
</script>
</body>
</html>

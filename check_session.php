<?php
// Überprüfen, ob der Benutzer eingeloggt ist, wenn nicht, dann zurück zur Anmeldeseite
if (!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true) {
    header("location: index.php");
    exit;
} else if (isset($_GET['logout'])) {
    // Löschen Sie alle Sitzungsvariablen
    $_SESSION = array();

    // Vernichten Sie die Sitzung
    session_destroy();

    // Leiten Sie den Benutzer zur Login-Seite weiter
    header("Location: index.php");
    exit;
}
?>

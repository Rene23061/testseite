<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

include('../mysql.php');
// Erstellen Sie die Verbindung
// Erstellen Sie die Verbindung
$conn = new mysqli($servername, $username, $password, $dbname);

// Überprüfen Sie die Verbindung
if ($conn->connect_error) {
  die("Verbindung fehlgeschlagen: " . $conn->connect_error);
}

$sql = "SELECT timestamp, betrag_spot, betrag_future FROM Guthaben"; // Nun wird die Tabelle "Guthaben" abgefragt
$result = $conn->query($sql);

$data = array();

if ($result->num_rows > 0) {
  // Daten von jeder Zeile ausgeben
  while($row = $result->fetch_assoc()) {
    $data[] = $row;
  }
} else {
  echo "0 Ergebnisse";
}
$conn->close();

echo json_encode($data);
?>

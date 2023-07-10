<?php
// Datenbank-Zugangsdaten
$host = "localhost";
$user = "admin_bot";
$password = "Web0m95@6";
$database = "Bitget_Bot";

// Verbindung zur Datenbank herstellen
$connection = new mysqli($host, $user, $password, $database);
if ($connection->connect_error) {
    die("Connection failed: " . $connection->connect_error);
}

// Symbol überprüfen
$symbol = isset($_GET['symbol']) ? $_GET['symbol'] : "";

// SQL-Abfrage für neue Daten
$newDataQuery = "SELECT UNIX_TIMESTAMP(timestamp) * 1000 AS timestamp, open, high, low, close FROM CandlestickData WHERE symbol='$symbol' ORDER BY timestamp DESC LIMIT 1";
$newDataResult = $connection->query($newDataQuery);

if ($newDataResult->num_rows > 0) {
    $row = $newDataResult->fetch_assoc();
    $timestamp = $row['timestamp'];
    
    $newData = array(
        'timestamp' => $timestamp,
        'open' => $row['open'],
        'high' => $row['high'],
        'low' => $row['low'],
        'close' => $row['close']
    );

    // JSON-Antwort mit den neuen Daten senden
    $response = array("data" => $newData);
    echo json_encode($response);
} else {
    // JSON-Antwort senden, wenn keine neuen Daten vorhanden sind
    $response = array("data" => null);
    echo json_encode($response);
}

$connection->close();
?>

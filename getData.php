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

// Aktion überprüfen (symbols oder chart)
$action = isset($_GET['action']) ? $_GET['action'] : "";

if ($action === "symbols") {
    // SQL-Abfrage für verfügbare Symbole
    $symbolQuery = "SELECT DISTINCT symbol FROM CandlestickData";
    $symbolResult = $connection->query($symbolQuery);
    $symbols = [];
    if ($symbolResult->num_rows > 0) {
        while ($row = $symbolResult->fetch_assoc()) {
            $symbols[] = $row["symbol"];
        }
    }

    // JSON-Antwort mit den verfügbaren Symbolen senden
    $response = array("symbols" => $symbols);
    echo json_encode($response);
} elseif ($action === "chart") {
    // Symbol überprüfen
    $symbol = isset($_GET['symbol']) ? $_GET['symbol'] : "";

    // SQL-Abfrage für Chart-Daten
    $chartQuery = "SELECT timestamp, open, high, low, close FROM CandlestickData WHERE symbol='$symbol' ORDER BY timestamp ASC";
    $chartResult = $connection->query($chartQuery);
    $chartData = [];
    if ($chartResult->num_rows > 0) {
        while ($row = $chartResult->fetch_assoc()) {
            $timestamp = $row['timestamp'] / 1000; // Umwandlung von Millisekunden zu Sekunden
            $date = date("Y-m-d H:i:s", $timestamp); // Konvertierung des Zeitstempels in das gewünschte Format

            $chartData[] = array(
                'timestamp' => $date,
                'open' => $row['open'],
                'high' => $row['high'],
                'low' => $row['low'],
                'close' => $row['close']
            );
        }
    }

    // JSON-Antwort mit den Chart-Daten senden
    $response = array("data" => $chartData);
    echo json_encode($response);
}

$connection->close();
?>








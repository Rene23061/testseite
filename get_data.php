<?php
// Datenbankinformationen
$host = 'localhost';
$db   = 'Bitget_Bot';
$user = 'admin_bot';
$pass = 'Web0m95@6';

// Symbol aus der GET-Anfrage abrufen
$symbol = $_GET['symbol'];

// Verbindung zur Datenbank herstellen
$conn = new PDO("mysql:host=$host;dbname=$db", $user, $pass);

// SQL-Abfrage zum Abrufen der Kerzendaten für das ausgewählte Symbol
$query = "SELECT timestamp, open, high, low, close FROM CandlestickData WHERE symbol = :symbol ORDER BY timestamp";
$stmt = $conn->prepare($query);
$stmt->bindParam(':symbol', $symbol, PDO::PARAM_STR);
$stmt->execute();
$result = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Kerzendaten vorbereiten
$data = [];
foreach ($result as $row) {
    $data[] = [
        (int)$row['timestamp'],
        (float)$row['open'],
        (float)$row['high'],
        (float)$row['low'],
        (float)$row['close']
    ];
}

// Daten als JSON zurückgeben
header('Content-Type: application/json');
echo json_encode($data);
?>

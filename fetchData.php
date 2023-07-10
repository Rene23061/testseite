<?php
// Verbindung zur Datenbank herstellen
$host = 'localhost';
$db   = 'Bitget_Bot';
$user = 'admin_bot';
$pass = 'Web0m95@6';

$conn = new PDO("mysql:host=$host;dbname=$db", $user, $pass);

// Daten aus der Datenbank abrufen
$query = "SELECT timestamp, open, high, low, close FROM CandlestickData";
$stmt = $conn->prepare($query);
$stmt->execute();
$data = $stmt->fetchAll(PDO::FETCH_ASSOC);

// Daten in das Apex-Format konvertieren
$chartData = [];
foreach ($data as $row) {
    $chartData[] = [
        'x' => (int) $row['timestamp'],
        'y' => [
            (float) $row['open'],
            (float) $row['high'],
            (float) $row['low'],
            (float) $row['close'],
        ],
    ];
}

// JSON-Daten für den Apex Kerzenchart erstellen
$jsonData = json_encode([
    'series' => [
        [
            'data' => $chartData,
        ],
    ],
]);

// JSON-Daten ausgeben
header('Content-Type: application/json');
echo $jsonData;
?>

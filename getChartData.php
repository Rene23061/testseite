<?php
$host = 'localhost';
$user = 'admin_bot';
$password = 'Web0m95@6';
$database = 'Bitget_Bot';

$connection = new mysqli($host, $user, $password, $database);
if ($connection->connect_error) {
    die('Failed to connect to database: ' . $connection->connect_error);
}

$query = 'SELECT timestamp, open, high, low, close, volume FROM CandlestickData ORDER BY timestamp ASC';
$result = $connection->query($query);
if (!$result) {
    die('Failed to retrieve data from database: ' . $connection->error);
}

$data = [];
while ($row = $result->fetch_assoc()) {
    $timestamp = intval($row['timestamp']) / 1000;  // Zeitstempel in Sekunden
    $formattedTimestamp = $timestamp * 1000; // Zeitstempel in Millisekunden
    $data[] = [
        'x' => $formattedTimestamp,
        'y' => [floatval($row['open']), floatval($row['high']), floatval($row['low']), floatval($row['close'])]
    ];
}

$connection->close();

header('Content-Type: application/json');
echo json_encode($data);
?>

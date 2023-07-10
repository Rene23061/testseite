<?php

header("Access-Control-Allow-Origin: *");
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require '../api_keys.php';

function getSignature($timestamp, $method, $requestPath, $body, $secretKey) {
    $what = $timestamp . $method . $requestPath . $body;
    return base64_encode(hash_hmac("sha256", $what, $secretKey, true));
}

function getAccountAssets() {
    global $apiKey, $secretKey, $passphrase;

    $timestamp = time() * 1000;  // Bitget API benötigt den Zeitstempel in Millisekunden
    $method = "GET";
    $requestPath = "/api/spot/v1/account/assets";
    $body = "";

    // Hier generieren wir die Signatur
    $signature = getSignature($timestamp, $method, $requestPath, $body, $secretKey);

    // Erstellen Sie den cURL-Handle
    $ch = curl_init();

    // Setzen Sie die URL und andere notwendige Felder
    curl_setopt($ch, CURLOPT_URL, "https://api.bitget.com" . $requestPath);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "Content-Type: application/json",
        "ACCESS-KEY: $apiKey",
        "ACCESS-SIGN: $signature",
        "ACCESS-TIMESTAMP: $timestamp",
        "ACCESS-PASSPHRASE: $passphrase",
    ));
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);

    // Führen Sie die cURL-Sitzung aus und speichern Sie die Rückgabe in $output
    $output = curl_exec($ch);

    // Überprüfen Sie, ob ein Fehler aufgetreten ist
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        return null;
    }

    // Schließen Sie die cURL-Sitzung
    curl_close($ch);

    // Wandeln Sie die JSON-Antwort in ein PHP-Array um
    $outputData = json_decode($output, true);

    // Filtern Sie nur die Einträge, bei denen das verfügbare Guthaben größer als 0.001 ist
    $filteredData = array_filter($outputData['data'], function($item) {
        return $item['available'] > 0.001;
    });

    // Geben Sie die gefilterten Daten zurück
    return $filteredData;
}

$outputData = getAccountAssets();

// Reset array keys
$outputData = array_values($outputData);

// Output the data as JSON
header('Content-Type: application/json');
echo json_encode($outputData);

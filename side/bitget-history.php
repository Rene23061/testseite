<?php
// Bitget API-Zugangsdaten
$apiKey = 'bg_081b87110c6026fb71e717624d70294f';
$secretKey = 'a4894c0222c68f7b4f21cddf29b37f25ddcf88e3a48a04ade7c461a181f3fc0a';
$passphrase = 'Shorty2306';

$startTimestamp = strtotime('2023-01-01 midnight') * 1000;

$startTime = strval($startTimestamp);

$endTimestamp = time() * 1000;
$endTime = strval($endTimestamp);

$requestPath = '/api/mix/v1/order/historyProductType?productType=umcbl&startTime=' . $startTime . '&endTime=' . $endTime . '&pageSize=100';

$timestamp = round(microtime(true) * 1000); // Aktueller Zeitstempel in Millisekunden
$method = 'GET';

$message = $timestamp . $method . $requestPath;
$hmacDigest = base64_encode(hash_hmac('sha256', $message, $secretKey, true));

$headers = array(
    'Content-Type: application/json',
    'ACCESS-KEY: ' . $apiKey,
    'ACCESS-SIGN: ' . $hmacDigest,
    'ACCESS-TIMESTAMP: ' . $timestamp,
    'ACCESS-PASSPHRASE: ' . $passphrase,
    'locale: en-US'
);

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://api.bitget.com' . $requestPath);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);

$totalProfitsSum = 0;  // Total profits sum variable
$todayProfitsSum = 0;  // Today's profits sum variable
$weekProfitsSum = 0;  // This week's profits sum variable
$monthProfitsSum = 0;  // This month's profits sum variable


$todayTimestamp = strtotime('today midnight') * 1000;
$thisWeekTimestamp = strtotime('monday this week midnight') * 1000;
$thisMonthTimestamp = strtotime('first day of this month midnight') * 1000;

function get_order_data($orderList) {
    $orderData = array();

    foreach ($orderList as $order) {
        $symbolParts = explode('_', $order['symbol']);
        $symbol = str_replace('USDT', '', $symbolParts[0]);

        $totalProfits = $order['totalProfits'];

        // Wenn totalProfits gleich 0 ist, überspringen wir diese Iteration und gehen zur nächsten
        if ($totalProfits == 0) {
            continue;
        }

        $profitsColor = $totalProfits < 0 ? 'red' : 'green';

        $orderData[] = array(
            'symbol' => $symbol,
            'posSide' => $order['posSide'],
            'totalProfits' => $totalProfits,
            'profitsColor' => $profitsColor
        );
    }

    return $orderData;
}


if (curl_errno($ch)) {
    echo 'Curl-Fehler: ' . curl_error($ch);
} else {
    $httpStatusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    if ($httpStatusCode !== 200) {
        echo 'Fehler beim Abrufen der Daten. HTTP-Statuscode: ' . $httpStatusCode . '<br>';
        echo 'Serverantwort: ' . $response . '<br>';
    } else {
        $result = json_decode($response, true);

        if ($result['code'] === '00000') {
            $data = $result['data'];
            $orderList = $data['orderList'];
            
            // Rufen Sie die Funktion auf und speichern Sie die zurückgegebenen Daten
            $orderData = get_order_data($orderList);

            return $orderData;

            // Speichern Sie die Daten in einer Datei
            file_put_contents('order_data.json', json_encode($orderData));
            
            echo '<table>';
            echo '<tr>';
            echo '<th>Coin</th>';
            echo '<th>Marge</th>';
            echo '<th>Gebühren</th>';
            echo '<th>Total Profits</th>';
            echo '<th>Pos. Side</th>';
            echo '<th>Leverage</th>';
            echo '<th>Order Type</th>';
            echo '<th>Enter Point</th>';
            echo '<th>Eröffnungszeit</th>';
            echo '</tr>';
            
            $rowCounter = 0;  // Zeilenzähler, direkt vor der foreach-Schleife hinzugefügt

            foreach ($orderList as $order) {
                $symbolParts = explode('_', $order['symbol']);
                $symbol = str_replace('USDT', '', $symbolParts[0]);
            
                $totalProfits = $order['totalProfits'];
                
                // Wenn totalProfits gleich 0 ist, überspringen wir diese Iteration und gehen zur nächsten
                if ($totalProfits == 0) {
                    continue;
                }
            
                $profitsColor = $totalProfits < 0 ? 'red' : 'green';
            
                $totalProfitsSum += $totalProfits;
            
                $orderTimestamp = $order['cTime'];
                if ($orderTimestamp >= $todayTimestamp) {
                    $todayProfitsSum += $totalProfits;
                }
                if ($orderTimestamp >= $thisWeekTimestamp) {
                    $weekProfitsSum += $totalProfits;
                }
                if ($orderTimestamp >= $thisMonthTimestamp) {
                    $monthProfitsSum += $totalProfits;
                }
            
                // Nur die ersten 200 Zeilen anzeigen
                if ($rowCounter < 200) {
                    echo '<tr>';
                    echo '<td>' . $symbol . '</td>';
                    echo '<td>' . $order['size'] . '</td>';
                    echo '<td>' . $order['fee'] . '</td>';
                    echo '<td style="color:' . $profitsColor . ';">' . number_format($totalProfits, 2) . '</td>';
                    echo '<td>' . $order['posSide'] . '</td>';
                    echo '<td>' . $order['leverage'] . '</td>';
                    echo '<td>' . $order['orderType'] . '</td>';
                    echo '<td>' . $order['enterPointSource'] . '</td>';
                    echo '<td>' . date('m-d H:i:s', $order['cTime'] / 1000) . '</td>';
                    echo '</tr>';
                }
                $rowCounter++;  // Zähler nach jeder Iteration erhöhen
                error_log("Matching Position for Order: " . json_encode($order) . " not found");
            }

            echo '</table>';

            echo '<div style="margin-top: 20px;">';
            echo '<span style="margin-right: 10px;"><b>Total Profits Today:</b> <span style="color:' . ($todayProfitsSum < 0 ? 'red' : 'green') . ';">' . number_format($todayProfitsSum, 2) . '</span></span>';
            echo '<span style="margin-right: 10px;"><b>Total Profits This Week:</b> <span style="color:' . ($weekProfitsSum < 0 ? 'red' : 'green') . ';">' . number_format($weekProfitsSum, 2) . '</span></span>';
            echo '<span style="margin-right: 10px;"><b>Total Profits This Month:</b> <span style="color:' . ($monthProfitsSum < 0 ? 'red' : 'green') . ';">' . number_format($monthProfitsSum, 2) . '</span></span>';
            echo '<span style="margin-right: 10px;"><b>Total Profits:</b> <span style="color:' . ($totalProfitsSum < 0 ? 'red' : 'green') . ';">' . number_format($totalProfitsSum, 2) . '</span></span>';            
            echo '</div>';
        } else {
            echo json_encode(array(
                'error' => 'Fehler beim Abrufen der Daten.',
                'errorCode' => $result['code'],
                'errorMessage' => $result['msg']
            ));
        }
    }
}

curl_close($ch);
?>

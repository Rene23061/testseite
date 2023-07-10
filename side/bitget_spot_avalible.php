<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET, POST");
header("Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept");

$apiUrl1 = '../side/bitget_spot_asset.php';
$response1 = file_get_contents($apiUrl1);
if ($response1 === false) {
    die('Fehler beim Abrufen der Daten von ' . $apiUrl1);
}
$data1 = json_decode($response1, true);

$apiUrl2 = 'https://api.bitget.com/api/spot/v1/market/tickers';
$response2 = file_get_contents($apiUrl2);
if ($response2 === false) {
    die('Fehler beim Abrufen der Daten von ' . $apiUrl2);
}
$data2 = json_decode($response2, true);

$results = array();

foreach ($data1 as $coinData1) {
    if (floatval($coinData1['available']) > 0.001) {
        if ($coinData1['coinName'] == 'USDT') {
            $results[] = array(
                'coinName' => 'USDT',
                'totalInUSDT' => floatval($coinData1['available'])
            );
        } else {
            foreach ($data2['data'] as $tickerData2) {
                $symbol2 = substr($tickerData2['symbol'], 0, strlen($tickerData2['symbol']) - 4);
                if ($coinData1['coinName'] == $symbol2) {
                    $available = floatval($coinData1['available']);
                    $close = floatval($tickerData2['close']);
                    $result = $available * $close;
                    $results[] = array(
                        'coinName' => $coinData1['coinName'],
                        'totalInUSDT' => $result
                    );
                    break;
                }
            }
        }
    }
}

$totalSum = 0;
foreach ($results as $result) {
    $totalSum += floatval($result['totalInUSDT']);
}

$results[] = array(
    'coinName' => 'Total',
    'totalInUSDT' => $totalSum
);

header('Content-Type: application/json');
echo json_encode($results);
?>

<?php
$apiKey = 'bg_081b87110c6026fb71e717624d70294f';
$secretKey = 'a4894c0222c68f7b4f21cddf29b37f25ddcf88e3a48a04ade7c461a181f3fc0a';
$passphrase = 'Shorty2306';

$timestamp = round(microtime(true) * 1000); // Aktueller Zeitstempel in Millisekunden
$method = 'GET';
$requestPath = '/api/mix/v1/position/allPosition-v2?productType=umcbl&marginCoin=USDT';

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
            $positions = array();
            foreach ($data as $position) {
                $positions[] = array(
                    'symbol' => $position['symbol'],
                    'marginCoin' => $position['marginCoin'],
                    'holdSide' => $position['holdSide'],
                    'openDelegateCount' => $position['openDelegateCount'],
                    'margin' => $position['margin'],
                    'available' => $position['available'],
                    'locked' => $position['locked'],
                    'total' => $position['total'],
                    'leverage' => $position['leverage'],
                    'achievedProfits' => $position['achievedProfits'],
                    'averageOpenPrice' => $position['averageOpenPrice'],
                    'marginMode' => $position['marginMode'],
                    'holdMode' => $position['holdMode'],
                    'unrealizedPL' => $position['unrealizedPL'],
                    'liquidationPrice' => $position['liquidationPrice'],
                    'keepMarginRate' => $position['keepMarginRate'],
                    'marketPrice' => $position['marketPrice'],
                    'creationTime' => $position['cTime']
                );
            }
            echo json_encode($positions);
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

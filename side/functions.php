<?php

if (!function_exists('getAccountList')) {
  function getAccountList() {
    global $apiKey, $secretKey, $passphrase;

    $timestamp = time() * 1000; // Millisekunden
    $method = 'GET';
    $requestPath = '/api/mix/v1/account/accounts';
    $queryString = 'productType=umcbl';
    $body = '';

    $signature = generateSignature($timestamp, $method, $requestPath, $queryString, $body, $secretKey);

    $url = "https://api.bitget.com{$requestPath}?{$queryString}";
    $headers = [
      "ACCESS-KEY: {$apiKey}",
      "ACCESS-SIGN: {$signature}",
      "ACCESS-TIMESTAMP: {$timestamp}",
      "ACCESS-PASSPHRASE: {$passphrase}",
      "Content-Type: application/json",
    ];

    $curl = curl_init();
    curl_setopt_array($curl, [
      CURLOPT_URL => $url,
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_HTTPHEADER => $headers,
    ]);
    $response = curl_exec($curl);
    curl_close($curl);

    $result = json_decode($response);
    return $result;
  }
}

<?php

if (!function_exists('generateSignature')) {
  function generateSignature($timestamp, $method, $requestPath, $queryString, $body, $secretKey) {
    $method = strtoupper($method);
    $body = $body ?? '';
    $queryString = $queryString ? "?$queryString" : '';
    $preHash = $timestamp . $method . $requestPath . $queryString . $body;

    $signature = base64_encode(hash_hmac('sha256', $preHash, $secretKey, true));

    return $signature;
  }
}

<?php
header('Content-Type: application/json');
$url = 'https://api.bitget.com/api/spot/v1/market/tickers';
$data = file_get_contents($url);
echo $data;
?>

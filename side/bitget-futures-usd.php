<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require '../api_keys.php';

include('signature.php');
include('functions.php');

$accountList = getAccountList();
if ($accountList && $accountList->code === '00000') {
  $usdtEquity = number_format($accountList->data[0]->usdtEquity, 2);

  echo $usdtEquity ;
} else {
  echo "Fehler beim Abrufen der Kontoliste";
}
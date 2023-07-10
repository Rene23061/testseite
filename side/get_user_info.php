<?php
include('./mysql.php');

// Annahme, dass die Benutzerinformationen in der Datenbank gespeichert sind

// Funktion zum Abrufen der Benutzerinformationen aus der Datenbank
function getUserInfo($userId)
{
    global $conn;

    $sql = "SELECT username, last_login, avatar, vname, nname, apiKey, secretKey, passphrase, BTC_wallet, USDT_wallet, 	email   FROM USER WHERE id = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $userId);
    $stmt->execute();
    $result = $stmt->get_result();
    $userInfo = $result->fetch_assoc();

    return $userInfo;
}

// Überprüfen, ob der Benutzer eingeloggt ist
if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true && isset($_SESSION['id'])) {
    $userId = $_SESSION['id'];
    // Benutzerinformationen abrufen
    $userInfo = getUserInfo($userId);

    // Überprüfen, ob Benutzerinformationen gefunden wurden
    if ($userInfo) {
        // Benutzername und letzten Login speichern
        $username = $userInfo['username'];
        $lastLogin = $userInfo['last_login'];
        $avatar = $userInfo['avatar'];
        $vname = $userInfo['vname'];
        $nname = $userInfo['nname'];
        $apiKey = $userInfo['apiKey'];
        $secretKey = $userInfo['secretKey'];
        $passphrase = $userInfo['passphrase'];
        $BTC_wallet = $userInfo['BTC_wallet'];
        $USDT_wallet = $userInfo['USDT_wallet'];
        $email = $userInfo['email'];




        // Aktualisiere die Session-Variablen, um die Informationen bereitzustellen
        $_SESSION['username'] = $username;
        $_SESSION['last_login'] = $lastLogin;
        $_SESSION['avatar'] = $avatar;
        $_SESSION['vname'] = $vname;
        $_SESSION['nname'] = $nname;
        $_SESSION['apiKey'] = $apiKey;
        $_SESSION['secretKey'] = $secretKey;
        $_SESSION['passphrase'] = $passphrase;
        $_SESSION['BTC_wallet'] = $BTC_wallet;
        $_SESSION['USDT_wallet'] = $USDT_wallet;
        $_SESSION['email'] = $email;
    }
}
?>

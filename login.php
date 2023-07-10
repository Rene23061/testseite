<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

include('./mysql.php');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Abfrage aus der Datenbank
    $sql = "SELECT id, password FROM USER WHERE username = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_object();

    // Prüfen, ob der Benutzer existiert und das Passwort korrekt ist
    if ($user && password_verify($password, $user->password)) {
        // Login erfolgreich, Benutzer existiert und Passwort ist korrekt
        session_start();
        $_SESSION['loggedin'] = true;
        $_SESSION['id'] = $user->id; // Benutzer-ID in der Sitzung speichern

        // Aktualisieren des Zeitstempels für den letzten Login
        $sql = "UPDATE USER SET last_login = CURRENT_TIMESTAMP WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("i", $user->id);
        $stmt->execute();

        header("Location: loader_home.php");
        exit;
    } else {
        // Login fehlgeschlagen, Benutzer existiert nicht oder Passwort ist falsch
        echo "Invalid username or password.";
    }
}

?>
<script>
  if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
  }
</script>

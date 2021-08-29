
<?php 

$servername = "localhost";  
$dbname = "enlodin1_cankurt"; 
$username = "enlodin1_cankurt"; 
$password = "X%[2c2~X&P%j"; 
$conn = new mysqli($servername, $username, $password, $dbname); 
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 
$conn->set_charset("utf8");
header('Content-Type: text/html; charset=utf-8');

$sql = "SELECT day,gubre,miktar,birim FROM days "; 
 
if ($result = $conn->query($sql)) {
    while($row = $result->fetch_array(MYSQLI_ASSOC)) {
      $myArray[] = $row;
    }
     
    echo json_encode($myArray,JSON_FORCE_OBJECT|\JSON_UNESCAPED_UNICODE);
}

$result->close();
$conn->close();
?>  
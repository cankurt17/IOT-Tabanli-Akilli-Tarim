

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

$sql = "SELECT  date,SUM(count)  FROM sulama_kayit  WHERE date >= NOW() - INTERVAL 11 month GROUP BY month(date) ORDER BY date ASC"; 
 
if ($result = $conn->query($sql)) {
    while($row = $result->fetch_array(MYSQLI_ASSOC)) {
      $myArray[] = $row;
    }
     
    echo json_encode($myArray,JSON_FORCE_OBJECT|\JSON_UNESCAPED_UNICODE);
}

$result->close();
$conn->close();
?>  
<?php 


$servername = "localhost";  
$dbname = "enlodin1_cankurt"; 
$username = "enlodin1_cankurt"; 
$password = "X%[2c2~X&P%j";
$api_key_value = "tPmAT5Ab3j7F9";

$tablo= $api_key= $day = $start = $stop = $durum = $id = $toplam = $startnem = $stopnem = $stopnem = $topraknem = $ortamnem = $ortamsicaklik ="";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $api_key = test_input($_POST["api_key"]);
    if($api_key == $api_key_value) {
        $day = test_input($_POST["day"]);
        $start = test_input($_POST["start"]);
        $stop = test_input($_POST["stop"]);
        $durum = test_input($_POST["durum"]);  
        $id = test_input($_POST["id"]); 
        $tablo = test_input($_POST["tablo"]); 
        $toplam = test_input($_POST["toplam"]); 
        $startnem = test_input($_POST["startnem"]); 
        $stopnem = test_input($_POST["stopnem"]); 
        $topraknem = test_input($_POST["topraknem"]); 
        $ortamnem = test_input($_POST["ortamnem"]); 
        $ortamsicaklik = test_input($_POST["ortamsicaklik"]); 

         
        $conn = new mysqli($servername, $username, $password, $dbname);
         
        $conn->set_charset("utf8");
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } else if ($tablo=='tablo_days') {
            $sql = "UPDATE days SET   start='" . $start . "' , stop='" . $stop . "', durum='  $durum  ', gubre='  $toplam  ' WHERE day='" . $day . "' ";
        } 
          
        if ($tablo=='tablo_gubre') {
            $sql = "UPDATE days SET   gubre='" . $start . "',miktar='" . $stop . "' , birim='" . $durum . "' WHERE day='" . $day . "' ";
        } 
        else if ($tablo=='tablo_mod') {
            $sql = "UPDATE `mod` SET  durum='  $durum  ' "; 
        } 
        else if ($tablo=='tablo_kayit') {
            $sql = "UPDATE `kayit` SET  durum='  $durum  ' "; 
        } 
        else if ($tablo=='tablo_mail') {
            $sql = "UPDATE `mod` SET  mail='" . $durum . "' "; 
        } 
        else if ($tablo=='tablo_nem') {
            $sql = "UPDATE `nem` SET start='$start' , stop=' $stop '"; 
        }  
        else if ($tablo=='sulama_kayit') {
            $sql = "INSERT INTO `sulama_kayit`(`day`,`start`, `stop`, `count`, `start_nem`, `stop_nem`, `mod_durum`, `gubre`, `hata` ) VALUES ('" . $day . "','" . $start . "','" . $stop . "','  $toplam  ','  $startnem  ','  $stopnem  ','" . $durum . "','  $ortamnem  ','  $ortamsicaklik  ') "; 
        }
         else if ($tablo=='tablo_arduino') {
            $sql = "UPDATE `arduino` SET toprak_nem='$topraknem' , durum=' $durum ' , ortam_nem=' $ortamnem ', ortam_sicaklik=' $ortamsicaklik ', su_debi=' $day ', pil=' $start ', gubre_durum=' $stop ', gubre_miktar=' $toplam ', modd=' $startnem '"; 
        }  
        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } 
        else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    
        $conn->close();
    }
    else {
        echo "Wrong API Key provided.";
    }

}
else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
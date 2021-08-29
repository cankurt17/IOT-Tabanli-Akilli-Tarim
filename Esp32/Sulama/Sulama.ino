#include "EasyNextionLibrary.h"
#include <EEPROM.h>
#include <virtuabotixRTC.h>
#include <DHT.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include "HX711.h"


EasyNex myNex(Serial2);
#define DHTTYPE DHT11

String id_sulama_durum[7] = {"manuel_ekran.cPt", "manuel_ekran.cSl", "manuel_ekran.cCrs", "manuel_ekran.cPrs", "manuel_ekran.cCm", "manuel_ekran.cCt", "manuel_ekran.cPz",};
String id_sulama_baslaSaat[7] = {"manuel_ekran.ptBasla", "manuel_ekran.slBasla", "manuel_ekran.crsBasla", "manuel_ekran.prsBasla", "manuel_ekran.cmBasla", "manuel_ekran.ctBasla", "manuel_ekran.pzBasla",};
String id_sulama_bitisSaat[7] = {"manuel_ekran.ptBitir", "manuel_ekran.slBitir", "manuel_ekran.crsBitir", "manuel_ekran.prsBitir", "manuel_ekran.cmBitir", "manuel_ekran.ctBitir", "manuel_ekran.pzBitir",};

String id_gubre_durum[7] = {"gubre_ayar.g_cPt", "gubre_ayar.g_cSl", "gubre_ayar.g_cCrs", "gubre_ayar.g_cPrs", "gubre_ayar.g_cCm", "gubre_ayar.g_cCt", "gubre_ayar.g_cPz",};
String id_gubre_miktar[7] = {"gubre_ayar.ptMiktar", "gubre_ayar.slMiktar", "gubre_ayar.crsMiktar", "gubre_ayar.prsMiktar", "gubre_ayar.cmMiktar", "gubre_ayar.ctMiktar", "gubre_ayar.pzMiktar",};
String id_gubre_birim[7] = {"gubre_ayar.ptBirim", "gubre_ayar.slBirim", "gubre_ayar.crsBirim", "gubre_ayar.prsBirim", "gubre_ayar.cmBirim", "gubre_ayar.ctBirim", "gubre_ayar.pzBirim",};

String id_sulama_nem[2] = {"manuel_nem.nemBasla", "manuel_nem.nemBitir"};
String id_sulama_mod = {"mod_ekran.mod" };
String id_dekar = {"dekar_ekran.dekar" };
String id_suSayaci = {"su_sayaci.suSayaci" };

String gunler[7] = {"Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"};

const char* mailServer = "http://maker.ifttt.com/trigger/esp_mail/with/key/dOcBsvl9Rl1Jaqve76vQB2";

const char* writeServer = "https://enlodi.com/Sulama-Proje/post-esp-data.php";
const char* readServer = "https://enlodi.com/Sulama-Proje/";
String apiKeyValue = "tPmAT5Ab3j7F9";
String httpRequestData;
//const char* ssid     = "KURT";
//const char* password = "enlodi.46";
const char* ssid     = "G4_7465";
const char* password = "11111111";

String mailAdresi;

unsigned long eskizaman = 0;
int sulama_durum[7];
String sulama_baslaSaat[7];
String sulama_bitisSaat[7];
int gubre_durum[7];
int gubre_miktar[7];
String gubre_birim[7];
int sulama_nem[2];
int sulama_mod;
int dekar;
int suSayaci;
int toplamSulama;
bool suKesintisi = false;
int kesintiSayisi = 0;
unsigned long kesintiZaman = 0;
String gubreBirimler[2] = {"mL", "L"};

uint32_t ekranKayit = 0 ;
String text = "";
uint32_t asd = 0 ;

byte lsb;
byte msb;
unsigned long ekran_zaman = 0;
String suDurum = "KAPALI";
String gubreDurum = "KAPALI";

///////////////////////////////// Pinler
int suVana = 33;
int gubreVana = 26;
int Saat_CLK_PIN = 13 ;
int Saat_DT_PIN = 12;
int Saat_RST_PIN = 14 ;
const int DHTPin = 25;
int nem_sensor = 35;
const int debi_sensor = 27;
#define DOUT 22
#define CLK 23


HX711 scale(DOUT, CLK);
float kalibrasyon_faktoru = 103000;

bool debiKontrol;
int hata = 1;

int debi = 0;
int nemdeger = 0;
String sulamaRapor;
int ortDebi = 0;
int _gun;

int debiSaniye = 120000;
int gubreSaniye = 300000;
int veriMod;
int veriGubre;
String veriBaslamaSaati;
String veriBitisSaati;
int veriBaslamaNem;
int veriBitisNem;
int veriAnlikNem;
unsigned long veriSuBaslama = 0;
unsigned long mysql_zaman = 0;
float veriAtilacakGubre = 0;
float veriAnlikGubre = 0;
float gubreMiktar = 0;

volatile int  Pulse_Count;
unsigned int  Liter_per_hour;
unsigned long Current_Time, Loop_Time;

DHT dht(DHTPin, DHTTYPE);
virtuabotixRTC myRTC(Saat_CLK_PIN, Saat_DT_PIN, Saat_RST_PIN);

void setup() {
  myNex.begin(115200); // Begin the object with a baud rate of 9600
  Serial.begin(115200);                  // If no parameter was given in the begin(), the default baud rate of 9600 will be used v
  EEPROM.begin(512);
  dht.begin();
  pinMode(nem_sensor, INPUT);
  pinMode(suVana, OUTPUT);
  pinMode(gubreVana, OUTPUT);
  pinMode(debi_sensor, INPUT);
  digitalWrite(suVana, LOW);
  scale.set_scale(kalibrasyon_faktoru); // Ölçek ayarlandı
  scale.tare(); // Ölçek sıfırlandı
  attachInterrupt(digitalPinToInterrupt(debi_sensor), Detect_Rising_Edge, RISING);
  Current_Time = millis();
  Loop_Time = Current_Time;
  loadEEPROM();
  loadNextion();
  initWiFi();
}


void loop() {
  myNex.NextionListen();
  myRTC.updateTime();
  homePage();
  ekranKayit = myNex.readNumber ( "settings.kayitEkran.val" );
  Current_Time = millis();
  getDebiSensor();
  sulamaKontrol();
  mysqlKontrol();
  debiHesapla();
  suKontrol();
  wifiKontrol();
  if (ekranKayit == 1) {

    getNextionMod();
    writeModEEPROM();
    mysqlModKayit();
  }
  if (ekranKayit == 2) {
    getNextionSulama();
    writeSulamaEEPROM();
    mysqlGunKayit();
  }
  if (ekranKayit == 3) {
    getNextionNem();
    writeNemEEPROM();
    mysqlNemKayit();
  }
  if (ekranKayit == 4) {
    getNextionGubre();
    writeGubreEEPROM();
    mysqlGubreKayit();
  }
  if (ekranKayit == 5) {
    getNextionDekar();
    writeDekarEEPROM();
    kayitEkran();
  }
  if (ekranKayit == 6) {
    writeSayacEEPROM(0);
    kayitEkran();
  }
  if (ekranKayit == 7) {
    saatKayit();
    kayitEkran();
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////  getNextion
void getNextionSulama() {
  for (int i = 0; i <= 6; i++) {
    sulama_durum[i] = myNex.readNumber( id_sulama_durum[i] + ".val" );
    sulama_baslaSaat[i] = myNex.readStr( id_sulama_baslaSaat[i] + ".txt" );
    sulama_bitisSaat[i] = myNex.readStr( id_sulama_bitisSaat[i] + ".txt" );
  }
  for (int i = 0; i <= 6; i++) {
    Serial.println(sulama_durum[i]);
    Serial.println(sulama_baslaSaat[i]);
    Serial.println(sulama_bitisSaat[i]);
  }
}
void getNextionNem() {
  sulama_nem[0] = myNex.readNumber( id_sulama_nem[0] + ".val"  );
  sulama_nem[1] = myNex.readNumber( id_sulama_nem[1] + ".val"  );
}
void getNextionMod() {
  sulama_mod = myNex.readNumber( id_sulama_mod + ".val"  );
  String abc = myNex.readStr( "mod_ekran.b2.txt" );
  Serial.println(sulama_mod);
  Serial.println(abc);
}
void getNextionGubre() {
  for (int i = 0; i <= 6; i++) {
    gubre_durum[i] = myNex.readNumber( id_gubre_durum[i] + ".val" );
    gubre_miktar[i] = myNex.readStr( id_gubre_miktar[i] + ".txt" ).toInt();
    gubre_birim[i] = myNex.readStr( id_gubre_birim[i] + ".txt" );
  }
  for (int i = 0; i <= 6; i++) {
    Serial.println(gubre_durum[i]);
    Serial.println(gubre_miktar[i]);
    Serial.println(gubre_birim[i]);
  }
}

void getNextionDekar() {
  dekar = myNex.readNumber( id_dekar + ".val"  );
}
//////////////////////////////////////////////////////////////////////////////////////////////////////  setNextion
void setNextionSulama() {
  for (int i = 0; i <= 6; i++) {
    myNex.writeNum( id_sulama_durum[i] + ".val", sulama_durum[i] );
    myNex.writeStr( id_sulama_baslaSaat[i] + ".txt", sulama_baslaSaat[i] );
    myNex.writeStr( id_sulama_bitisSaat[i] + ".txt", sulama_bitisSaat[i]);
  }
}
void setNextionNem() {
  myNex.writeNum( id_sulama_nem[0] + ".val", sulama_nem[0]);
  myNex.writeNum( id_sulama_nem[1] + ".val", sulama_nem[1]);
}
void setNextionMod() {
  myNex.writeNum( id_sulama_mod + ".val", sulama_mod);
}
void setNextionGubre() {
  for (int i = 0; i <= 6; i++) {
    myNex.writeNum( id_gubre_durum[i] + ".val" , gubre_durum[i]);
    myNex.writeStr( id_gubre_miktar[i] + ".txt", String(gubre_miktar[i]) );
    myNex.writeStr( id_gubre_birim[i] + ".txt" , gubre_birim[i]);
  }
}
void setNextionDekar() {
  myNex.writeNum( id_dekar + ".val", dekar);
}
void setNextionSayac() {
  myNex.writeNum( id_suSayaci + ".val", suSayaci);
}
//////////////////////////////////////////////////////////////////////////////////////////////////////  writeEEPROM
void writeSulamaEEPROM() {
  int addr = 1;
  for (int i = 0; i <= 6; i++) {
    writeEEPROM(addr, sulama_durum[i]);
    writeEEPROM(addr + 1, sulama_baslaSaat[i].substring(0, 2).toInt());
    writeEEPROM(addr + 2, sulama_baslaSaat[i].substring(3, 5).toInt());
    writeEEPROM(addr + 3, sulama_bitisSaat[i].substring(0, 2).toInt());
    writeEEPROM(addr + 4, sulama_bitisSaat[i].substring(3, 5).toInt());
    addr = addr + 5;
  }

}
void writeNemEEPROM() {
  writeEEPROM(40, sulama_nem[0]);
  writeEEPROM(41, sulama_nem[1]);
}
void writeModEEPROM() {
  writeEEPROM(42, sulama_mod);
}
void writeGubreEEPROM() {
  int addr = 45;
  for (int i = 0; i <= 6; i++) {
    intToByte(gubre_miktar[i]);
    writeEEPROM(addr, gubre_durum[i]);
    writeEEPROM(addr + 1, lsb);
    writeEEPROM(addr + 2, msb);
    writeEEPROM(addr + 3, getGubreBirim(gubre_birim[i]));
    addr = addr + 4;
  }
}
void writeDekarEEPROM() {
  intToByte(dekar);
  writeEEPROM(90, lsb);
  writeEEPROM(91, msb);
}
void writeSayacEEPROM(int sayac) {
  intToByte(sayac);
  writeEEPROM(92, lsb);
  writeEEPROM(93, msb);
}
//////////////////////////////////////////////////////////////////////////////////////////////////////  readEEPROM
void readSulamaEEPROM() {
  EEPROM.begin(512);
  int addr = 1;
  for (int i = 0; i <= 6; i++) {
    sulama_durum[i] = EEPROM.read(addr);
    sulama_baslaSaat[i] = setClockText(EEPROM.read(addr + 1), EEPROM.read(addr + 2));
    sulama_bitisSaat[i] = setClockText(EEPROM.read(addr + 3), EEPROM.read(addr + 4));
    addr = addr + 5;
  }
}

void readNemEEPROM() {
  sulama_nem[0] = EEPROM.read(40);
  sulama_nem[1] = EEPROM.read(41);
}
void readModEEPROM() {
  EEPROM.begin(512);
  sulama_mod = EEPROM.read(42);
}

void readGubreEEPROM() {
  int addr = 45;
  for (int i = 0; i <= 6; i++) {
    gubre_durum[i] =  EEPROM.read(addr);
    gubre_miktar[i] =  byteToInt(EEPROM.read(addr + 1), EEPROM.read(addr + 2));
    gubre_birim[i] =  gubreBirimler[EEPROM.read(addr + 3)] ;
    addr = addr + 4;
  }
}

void readDekarEEPROM() {
  EEPROM.begin(512);
  dekar = byteToInt(EEPROM.read(90), EEPROM.read(91));
}

void readSayacEEPROM() {
  EEPROM.begin(512);
  suSayaci = byteToInt(EEPROM.read(92), EEPROM.read(93));
}
//////////////////////////////////////////////////////////////////////////////////////////////////////  startApp

void loadEEPROM() {
  readSulamaEEPROM();
  readNemEEPROM();
  readModEEPROM();
  readGubreEEPROM();
  readDekarEEPROM();
  readSayacEEPROM();
}
void loadNextion() {
  setNextionSulama();
  setNextionNem();
  setNextionMod();
  setNextionGubre();
  setNextionDekar();
  setNextionSayac();
}
/////////////////////////////////////////////////////////////////////////////////////////////////////


void writeEEPROM(int addr, int value) {
  if (EEPROM.read(addr) != value) {
    EEPROM.begin(512);
    EEPROM.write(addr, value);
    EEPROM.commit();
  }
}

void intToByte(int value) {
  lsb = lowByte(value);
  msb = highByte(value);
}

int byteToInt(byte a, byte b) {
  return a + (b << 8);
}

int getGubreBirim(String birim) {
  int _birim;
  if (birim == "mL") {
    _birim = 0;
  } else if (birim == "L") {
    _birim = 1;
  }
  return _birim;
}

String setClockText(int saat, int dk) {
  String deger;
  if (saat < 10) {
    if (dk < 10) {
      deger = "0" + String(saat) + ":" + "0" + String(dk);
    } else {
      deger = "0" + String(saat) + ":" + String(dk);
    }
  } else if (dk < 10) {
    deger = String(saat) + ":" + "0" + String(dk);
  } else {
    deger = String(saat) + ":" + String(dk);
  }
  return deger;
}

void kayitEkran() {
  myNex.writeNum( "p1.pic", 23 );
  myNex.writeStr ("t2.txt", "Bağlantı başarılı.");
  myNex.writeStr( "vis p1,1");
  myNex.writeStr( "vis t2,1");
  delay(100);
  myNex.writeNum( "t0.pco", 1024 );
  myNex.writeStr ("t0.txt", "Kaydedildi.");
  delay(500);
  myNex.writeNum( "settings.kayitEkran.val", 0 );
  myNex.writeStr ("page settings");
  delay(100);
}


void homePage() {
  if (millis() - ekran_zaman > 2000) {
    nemdeger = analogRead(nem_sensor);
    nemdeger = map(nemdeger, 0, 4095, 100, 0);
    gubreMiktar = getTarti();
    if (digitalRead(suVana) == HIGH) {
      suDurum = "AÇIK";
    } else {
      suDurum = "KAPALI";
    }
    if (digitalRead(gubreVana) == HIGH) {
      gubreDurum = "AÇIK";
    } else {
      gubreDurum = "KAPALI";
    }
    myNex.writeNum( "home.saat.val", myRTC.hours);
    myNex.writeNum( "home.dk.val", myRTC.minutes);
    myNex.writeStr( "home.day.txt", gunler[myRTC.dayofweek - 1]);
    myNex.writeStr( "home.sic.txt", String((int)dht.readTemperature()) + "°C");
    myNex.writeStr( "home.nem.txt", "%" + String((int)dht.readHumidity()));
    myNex.writeStr( "home.tnem.txt", "%" + String(nemdeger));
    myNex.writeStr( "home.debi.txt", String(debi) + " L/sa");
    myNex.writeStr( "home.rapor.txt", suRapor());
    myNex.writeStr( "home.suDurum.txt", suDurum);
    myNex.writeStr( "home.gMiktar.txt", String(gubreMiktar, 1) + " Litre");
    myNex.writeStr( "home.gubreDurum.txt", gubreDurum);
    loadNextion();
    ekran_zaman = millis();
  }
}

void saatKayit() {
  int gun = getDay(myNex.readStr("saat_ayar.t0.txt" ));
  int saat = myNex.readNumber("saat_ayar.n0.val" );
  int dk = myNex.readNumber("saat_ayar.n1.val" );
  myRTC.setDS1302Time(00, dk, saat, gun, 10, 1, 2020);
}

int getDay(String gun) {
  int _gun;
  if (gun == "Pazartesi") {
    _gun = 1;
  } else if (gun == "Salı") {
    _gun = 2;
  } else if (gun == "Çarşamba") {
    _gun = 3;
  } else if (gun == "Perşembe") {
    _gun = 4;
  } else if (gun == "Cuma") {
    _gun = 5;
  } else if (gun == "Cumartesi") {
    _gun = 6;
  } else if (gun == "Pazar") {
    _gun = 7;
  }
  return _gun;
}


void getDebiSensor() {
  Current_Time = millis();
  if (Current_Time >= (Loop_Time + 1000))
  {
    Loop_Time = Current_Time;
    Liter_per_hour = (Pulse_Count * 60 / 7.5);
    Pulse_Count = 0;
    debi = Liter_per_hour;
  }
}


void Detect_Rising_Edge ()
{
  Pulse_Count++;
}

String suRapor() {
  int _gun = myRTC.dayofweek - 1;
  if (digitalRead(suVana) == LOW) {

    int saat = myRTC.hours * 100 + myRTC.minutes;
    int basla  = vanaSaatKontrol(sulama_baslaSaat[_gun]);
    if (sulama_durum[_gun] == 1 && saat <= basla) {
      if (gubre_durum[_gun] == 1) {
        return sulamaRapor = "Sıradaki sulama " + gunler[_gun] + " " + sulama_baslaSaat[_gun] + " / " + sulama_bitisSaat[_gun] + "  Gübreleme VAR";
      } else {
        return sulamaRapor = "Sıradaki sulama " + gunler[_gun] + " " + sulama_baslaSaat[_gun] + " / " + sulama_bitisSaat[_gun] + "  Gübreleme YOK";
      }
    }
    for (int i = _gun + 1; i <= 6; i++) {
      int saat = myRTC.hours * 100 + myRTC.minutes;
      int basla  = vanaSaatKontrol(sulama_baslaSaat[i]);

      if (sulama_durum[i] == 1) {
        if (gubre_durum[i] == 1) {
          return sulamaRapor = "Sıradaki sulama " + gunler[i] + " " + sulama_baslaSaat[i] + " / " + sulama_bitisSaat[i] + "  Gübreleme VAR";
        } else {
          return sulamaRapor = "Sıradaki sulama " + gunler[i] + " " + sulama_baslaSaat[i] + " / " + sulama_bitisSaat[i] + "  Gübreleme YOK";
        }
      }

    }
    for (int i = 0; i <= 6; i++) {
      int saat = myRTC.hours * 100 + myRTC.minutes;
      int basla  = vanaSaatKontrol(sulama_baslaSaat[i]);

      if (sulama_durum[i] == 1) {
        if (gubre_durum[i] == 1) {
          return sulamaRapor = "Sıradaki sulama " + gunler[i] + " " + sulama_baslaSaat[i] + " / " + sulama_bitisSaat[i] + "  Gübreleme VAR";
        } else {
          return sulamaRapor = "Sıradaki sulama " + gunler[i] + " " + sulama_baslaSaat[i] + " / " + sulama_bitisSaat[i] + "  Gübreleme YOK";
        }
      }
    }
    return sulamaRapor = "Kayıtlı sulama yok";
  } else {
    if (gubre_durum[_gun] == 1) {
      return sulamaRapor = "Bahçe şuanda sulanıyor Gübreleme VAR";
    } else {
      return sulamaRapor = "Bahçe şuanda sulanıyor Gübreleme YOK";
    }
  }
}
void sulamaKontrol() {
  if (sulama_mod == 1) {
    manSulama();
  }
  else if (sulama_mod == 0) {
    otoSulama();
  }
}
void manSulama() {
  int _gun = myRTC.dayofweek - 1;
  if (sulama_durum[_gun] == 1 ) {
    int basla  = vanaSaatKontrol(sulama_baslaSaat[_gun]);
    int bitir  = vanaSaatKontrol(sulama_bitisSaat[_gun]);
    int saat = myRTC.hours * 100 + myRTC.minutes;
    if (basla <= saat && saat <= bitir) {
      if (digitalRead(suVana) == LOW) {
        digitalWrite(suVana, HIGH);
        Serial.println("1");
        suDurum = "AÇIK";
        debiKontrol = true;
        ortDebi = 0;
        suKesintisi = false;
        veriSuBaslama = millis();
        manSulamaMail();
        sulamaKayitVerileri();
      } else {
        gubreKontrol();
      }
    } else if (digitalRead(suVana) == HIGH) {
      digitalWrite(suVana, LOW);
      Serial.println("2");
      suDurum = "KAPALI";
      sulamaBittiMail();
      sulamaBitis();
    }
  } else {
    if (digitalRead(suVana) == HIGH) {
      digitalWrite(suVana, LOW);
      Serial.println("3");
      suDurum = "KAPALI";
    }
  }
}

void otoSulama() {
  if (nemdeger <= sulama_nem[0] ) {
    if (digitalRead(suVana) == LOW) {
      digitalWrite(suVana, HIGH);
      Serial.println("4");
      suDurum = "AÇIK";
      ortDebi = 0;
      suKesintisi = false;
      veriSuBaslama = millis();
      debiKontrol = true;
      otoSulamaMail();
      sulamaKayitVerileri();
    }
  } else if (sulama_nem[1] < nemdeger) {
    if (digitalRead(suVana) == HIGH) {
      digitalWrite(suVana, LOW);
      Serial.println("5");
      suDurum = "KAPALI";
      sulamaBitis();
      sulamaBittiMail();
    }
  }
}


void sulamaVerileri() {
  _gun = myRTC.dayofweek - 1;
  nemdeger = analogRead(nem_sensor);
  nemdeger = map(nemdeger, 0, 4095, 100, 0);
  gubreMiktar = getTarti();
  veriMod = sulama_mod;
  veriGubre = gubre_durum[myRTC.dayofweek - 1];
  veriBaslamaSaati = sulama_baslaSaat[_gun];
  veriBitisSaati = sulama_bitisSaat[_gun];
  veriAnlikNem = nemdeger;
  veriSuBaslama = millis();
  veriAnlikGubre = gubreMiktar;
}

int _nemdegerKayit;
int _modKayit;
int _baslangisSaati;
int _baslangisDk;
void sulamaKayitVerileri() {
  _gun = myRTC.dayofweek - 1;
  _nemdegerKayit = analogRead(nem_sensor);
  _nemdegerKayit = map(_nemdegerKayit, 0, 4095, 100, 0);
  _modKayit = sulama_mod;
  veriGubre = gubre_durum[myRTC.dayofweek - 1];
  _baslangisSaati = myRTC.hours;
  _baslangisDk = myRTC.minutes;
}

void sulamaBitis() {
  ortDebi = 0;
  String _mod;
  String baslangic = String(_baslangisSaati) + ":" + String(_baslangisDk);
  String bitis = String(myRTC.hours) + ":" + String(myRTC.minutes);
  int _toplamSulama = toplamDk(baslangic, bitis);
  nemdeger = analogRead(nem_sensor);
  nemdeger = map(nemdeger, 0, 4095, 100, 0);
  if (_modKayit == 1) {
    _mod = "Manuel";
  } else {
    _mod = "Otomatik";
    veriGubre = 0;
  }
  readSayacEEPROM();
  suSayaci = suSayaci + _toplamSulama;
  Serial.print(suSayaci);
  writeSayacEEPROM(suSayaci);
  loadEEPROM();
  loadNextion();
  httpRequestData = "api_key=" + apiKeyValue + "&day=" +  gunler[myRTC.dayofweek - 1] +
                    "&start=" + baslangic + "&stop=" + bitis +
                    "&toplam=" + _toplamSulama  + "&startnem=" + _nemdegerKayit +
                    "&stopnem=" + nemdeger + "&durum=" + _mod + "&ortamnem=" + veriGubre + "&ortamsicaklik=" + hata + "&tablo=" + "sulama_kayit";
  loadMysql(httpRequestData);
  hata = 1;
}

void gubreKontrol() {
  _gun = myRTC.dayofweek - 1;

  int gbr_basla  = vanaSaatKontrol(sulama_baslaSaat[_gun]) + 5;
  int saat = myRTC.hours * 100 + myRTC.minutes;
  if (gubre_durum[_gun] == 1) {
    if (saat >= gbr_basla && digitalRead(gubreVana) == LOW) {
      int birim = getGubreBirim(gubre_birim[_gun]);
      if (birim == 0) {
        gubre_ml_L();
      } else if (birim == 1) {
        gubre_kg_L();
      }
      digitalWrite(gubreVana, HIGH);
      gubreDurum = "AÇIK";
      veriAnlikGubre = gubreMiktar;
      gubreMail();
    } else if (digitalRead(gubreVana) == HIGH) {

      if (suKesintisi == true) {
        digitalWrite(gubreVana, LOW);
        gubre_durum[_gun] = 0;
        gubreDurum = "KAPALI";
        writeGubreEEPROM();
        setNextionGubre();
        hata = 2;
        hataMail(1);
      } else if (gubreMiktar < 0.5) {
        digitalWrite(gubreVana, LOW);
        gubre_durum[_gun] = 0;
        gubreDurum = "KAPALI";
        writeGubreEEPROM();
        setNextionGubre();
        hata = 4;
        hataMail(2);
      }
      else if (veriAnlikGubre - gubreMiktar > veriAtilacakGubre) {
      
        digitalWrite(gubreVana, LOW);
        gubre_durum[_gun] = 0;
        gubreTamamMail();
        gubreDurum = "KAPALI";
        writeGubreEEPROM();
        setNextionGubre();
      }
    }
  }
}

int  vanaSaatKontrol(String saat) {
  return saat.substring(0, 2).toInt() * 100 + saat.substring(3, 5).toInt();
}
int toplamDk(String baslaSaat, String bitirSaat) {
  return (bitirSaat.substring(0, 2).toInt() - baslaSaat.substring(0, 2).toInt()) * 60 + (bitirSaat.substring(3, 5).toInt() - baslaSaat.substring(3, 5).toInt());
}

void debiHesapla() {
  if (debiKontrol == true && digitalRead(suVana) == HIGH) {

    int _gun = myRTC.dayofweek - 1;
    int debi_basla  = vanaSaatKontrol(sulama_baslaSaat[_gun]) + 2;
    int debi_bitir  = vanaSaatKontrol(sulama_baslaSaat[_gun]) + 4;
    int saat = myRTC.hours * 100 + myRTC.minutes;
    if (digitalRead(suVana) == HIGH && ( saat > debi_basla ) &&  ( debi_bitir >= saat ) ) {
      Serial.println("debi basladı");
      ortDebi = (ortDebi + debi) / 2;
    } else if ((saat > debi_bitir )) {
      debiKontrol = false;
      Serial.println(ortDebi);
      debiMail();
    }
  }
}
void gubre_ml_L() {
  //  toplamSulama = toplamDk(veriBaslamaSaati, veriBitisSaati);
  //  veriAtilacakGubre = ((toplamSulama / 60 * ortDebi) *  gubre_miktar[_gun]) / 1000 ;
  veriAtilacakGubre = gubre_miktar[_gun] / 1000 ;
}
void gubre_kg_L() {
  //  toplamSulama = toplamDk(veriBaslamaSaati, veriBitisSaati);
  //  veriAtilacakGubre = ((toplamSulama / 60 * ortDebi) *  gubre_miktar[_gun]) / 1000 ;
  veriAtilacakGubre = gubre_miktar[_gun]  ;
}
void suKontrol() {
  if (digitalRead(suVana) == HIGH) {
    if (suKesintisi == false) {
      if (digitalRead(suVana) == HIGH) {
        if (kesintiSayisi < 3) {
          if (debi == 0 && (millis() - kesintiZaman > 10000)) {
            kesintiSayisi = kesintiSayisi + 1;
            kesintiZaman = millis();
            Serial.print(kesintiSayisi);
          } else if (debi != 0 && (millis() - kesintiZaman > 10000)) {
            kesintiSayisi = 0;
            kesintiZaman = millis();
            Serial.print(kesintiSayisi);
          }

        } else {
          Serial.println("Su kesildi");
          suKesintisi = true;
          kesintiSayisi = 0;
          hataMail(3);
          kesintiZaman = millis();
        }
      }
    } else {
      if (digitalRead(suVana) == HIGH ) {
        if (kesintiSayisi < 3) {
          if (debi != 0  && (millis() - kesintiZaman > 10000)) {
            Serial.println(debi);
            kesintiSayisi = kesintiSayisi + 1;
            kesintiZaman = millis();
            Serial.print(kesintiSayisi);
          } else if (debi == 0 && (millis() - kesintiZaman > 10000)) {
            kesintiSayisi = 0;
            kesintiZaman = millis();
            Serial.print(kesintiSayisi);
          }

        } else {
          suKesintisi = false;
          hataMail(4);
          kesintiSayisi = 0;
          Serial.println("Su geldi");
          kesintiZaman = millis();
        }
      }
    }
  } else {
    suKesintisi == false;
  }
}
void initWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  wifiKontrol();
  Serial.print("heehehehe ..");

  Serial.println(WiFi.localIP());
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////// Mysql
void mysqlGunKayit() {

  for (int i = 0; i <= 6; i++) {
    httpRequestData = "api_key=" + apiKeyValue + "&day=" + gunler[i]
                      + "&start=" + sulama_baslaSaat[i] + "&stop=" + sulama_bitisSaat[i]
                      + "&durum=" + sulama_durum[i] + "&tablo=" + "tablo_days";
    writeMysql(httpRequestData);
  }
  kayitEkran();
}
void mysqlNemKayit() {
  String httpRequestData;
  httpRequestData = "api_key=" + apiKeyValue + "&start=" + sulama_nem[0] + "&stop=" + sulama_nem[1] + "&tablo=" + "tablo_nem";
  writeMysql(httpRequestData);
  kayitEkran();
}

void mysqlModKayit() {
  String httpRequestData;
  httpRequestData = "api_key=" + apiKeyValue + "&durum=" + sulama_mod + "&tablo=" + "tablo_mod";
  writeMysql(httpRequestData);
  kayitEkran();
}

void mysqlGubreKayit() {
  for (int i = 0; i <= 6; i++) {
    httpRequestData = "api_key=" + apiKeyValue + "&day=" + gunler[i]
                      + "&start=" + gubre_durum[i] + "&stop=" + gubre_miktar[i]
                      + "&durum=" + getGubreBirim(gubre_birim[i]) + "&tablo=" + "tablo_gubre";
    writeMysql(httpRequestData);
  }
  kayitEkran();
}

void writeMysql(String httpRequestData) {

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(writeServer);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");

    int httpResponseCode = http.POST(httpRequestData);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      kayitIntKontrol(true);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
      kayitIntKontrol(false);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
    kayitIntKontrol(false);
  }
}



void kayitIntKontrol(bool kayit) {
  if (kayit) {
    myNex.writeStr( "p0.pic=21" );
    myNex.writeStr( "t1.txt", "Bağlantı başarılı.");
    myNex.writeStr( "vis p0,1" );
    myNex.writeStr( "vis t1,1" );
    delay(100);
    myNex.writeStr( "vis p1,1" );
    myNex.writeStr( "vis t2,1" );

  } else {
    myNex.writeStr( "p0.pic=22" );
    myNex.writeStr( "t1.txt", "Bağlantı Yok.");
    myNex.writeStr( "vis p0,1" );
    myNex.writeStr( "vis t1,1" );
    delay(100);
    myNex.writeStr( "vis p1,1" );

  }
}


void loadMysql(String httpRequestData) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(writeServer);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST(httpRequestData);
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

void mysqlKontrol() {
  if (millis() - mysql_zaman > 15000) {
    String _data;
    _data = getMysql("tablo-kayit");
    int kayit = json (_data, "0", "durum").toInt();
    if (kayit == 1) {
      loadNem();
      loadDays();
      loadMod();
      loadGubre();
      writeModEEPROM();
      writeGubreEEPROM();
      writeNemEEPROM();
      writeSulamaEEPROM();
      loadEEPROM();
      loadNextion();
      kayit = 0;
      String httpRequestData;
      httpRequestData = "api_key=" + apiKeyValue  + "&durum=" + kayit + "&tablo=tablo_kayit";
      loadMysql(httpRequestData);
      digitalWrite(suVana, LOW);
      digitalWrite(gubreVana, LOW);
      myNex.writeStr("page home");
    }
    String httpRequestData;
    httpRequestData = "api_key=" + apiKeyValue + "&topraknem=" + nemdeger + "&durum=" +   digitalRead(suVana) + "&ortamnem=" + (int)dht.readHumidity() +   "&ortamsicaklik=" + (int)dht.readTemperature() + "&day=" + debi + "&start=" + 25 +  "&stop=" + digitalRead(gubreVana) + "&toplam=" + gubreMiktar + "&startnem=" + sulama_mod + "&tablo=" + "tablo_arduino";
    loadMysql(httpRequestData);
    mysql_zaman = millis();

  }
}





String getMysql(String php) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(readServer + php + ".php");
    int httpResponseCode = http.GET();
    String _data = http.getString();
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      return _data;
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

String json(String _data, String key, String value) {
  JSONVar myObject = JSON.parse(_data);
  if (JSON.typeof(myObject) == "undefined") {
    Serial.println("Parsing input failed!");
  } else {
    String _data = (const char*)myObject[key][value];
    return _data;
  }
}


void loadNem() {
  String _data;
  _data = getMysql("tablo-nem");
  sulama_nem[0] = json(_data, "0", "start").toInt();
  sulama_nem[1] = json(_data, "0", "stop").toInt();
}


void loadDays() {
  String _data;
  _data = getMysql("tablo-days");
  for (int i = 0; i <= 6; i++) {
    sulama_durum[i] = json(_data, String(i), "durum").toInt();
    sulama_baslaSaat[i] = json(_data, String(i), "start") ;
    sulama_bitisSaat[i] = json(_data, String(i), "stop") ;
  }
}

void loadGubre() {
  String _data;
  _data = getMysql("tablo-days-gubre");
  for (int i = 0; i <= 6; i++) {
    gubre_durum[i] = json(_data, String(i), "gubre").toInt();
    gubre_miktar[i] = json(_data, String(i), "miktar").toInt() ;
    gubre_birim[i] = json(_data, String(i), "birim") ;
  }
}


void loadMod() {
  String _data;
  _data = getMysql("tablo-mod");
  sulama_mod = json(_data, "0", "durum").toInt();
}

void loadMail() {
  String _data;
  _data = getMysql("tablo-mod");
  mailAdresi = json(_data, "0", "mail");
}


void sendMail(String httpRequestData) {

  if (WiFi.status() == WL_CONNECTED) {
    loadMail();
    Serial.println(mailAdresi);
    HTTPClient http;
    http.begin(mailServer);
    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    int httpResponseCode = http.POST("value1=" + String(mailAdresi) + httpRequestData);
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

void manSulamaMail() {
  nemdeger = analogRead(nem_sensor);
  nemdeger = map(nemdeger, 0, 4095, 100, 0);
  _gun = myRTC.dayofweek - 1;
  String _gubreDurum;
  if (gubre_durum[_gun] == 1) {
    _gubreDurum = "Var";
  } else {
    _gubreDurum = "Yok";
  }
  String mail = "<strong>Sulama başladı.</strong><br><br><b>Mod: </b>" + String("Manuel") +
                "<br><b>Başlangıç saati: </b>" +  sulama_baslaSaat[_gun] +
                "<br><b>Bitiş saati: </b>" +   sulama_bitisSaat[_gun]  +
                "<br><b>Toprak nemi: </b> " + String(nemdeger) +
                "<br><b>Ortam sıcaklığı: </b> " + String((int)dht.readTemperature()) + "°C" +
                "<br><b>Ortam nemi: </b> "  + String((int)dht.readHumidity()) +
                "<br><b>Gubreleme: </b> " + _gubreDurum ;
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void otoSulamaMail() {
  String mail = "<strong>Sulama başladı.</strong><br><br><b>Mod: </b>" + String("Otomatik") +
                "<br><b>Başlangıç Nemi: </b>" +  sulama_nem[0] +
                "<br><b>Bitiş Nemi: </b>" +   sulama_nem[1]  +
                "<br><b>Toprak nemi: </b> " + String(nemdeger) +
                "<br><b>Ortam sıcaklığı: </b> " + String((int)dht.readTemperature()) + "°C" +
                "<br><b>Ortam nemi: </b> " + String((int)dht.readHumidity());
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void gubreMail() {
  gubreMiktar = getTarti();
  String mail = "<strong>Gubreleme başladı.</strong><br><br><b>Gübre ayarı: </b>" +
                String(gubre_miktar[_gun]) + " " + gubre_birim[_gun]  +
                "<br><b>Mevcut gübre: </b> " + String(gubreMiktar) + " Litre";
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void gubreTamamMail() {
  gubreMiktar = getTarti();
  String mail = "<strong>Gubreleme bitti.</strong><br><br><b>Gübre ayarı: </b>" +
                String(gubre_miktar[_gun]) + gubre_birim[_gun]  +
                "<br><b>Mevcut gübre: </b> " + String(gubreMiktar) + " Litre";
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}
void debiMail() {
  String mail = "<strong>Sulama Debisi.</strong><br><br><b>Debi: </b>" + String(ortDebi) + " L/sa";
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void gubreSuKesintisiMail() {
  String mail = "<strong>Gübreleme İptal Edildi!</strong><br><br><b>Hata: </b>" + String("Su kesintisinden dolayı gübreleme iptal edildi.") ;
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}
void suKesintisiMail() {
  String mail = "<strong>Su kesintisi!</strong><br><br><b>Durum: </b>" + String("Su kesildi.") ;
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void suGeldiMail() {
  String mail = "<strong>Su geldi!</strong><br><br><b>Durum: </b>" + String("Su geldi.") ;
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void gubreBittiMail() {
  String mail = "<strong>Gübreleme İptal Edildi!</strong><br><br><b>Hata: </b>" + String("Gübre bittiği için gübreleme iptal edildi.") ;
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void sulamaBittiMail() {

  String _mod;
  String baslangic = String(_baslangisSaati) + ":" + String(_baslangisDk);
  String bitis = String(myRTC.hours) + ":" + String(myRTC.minutes);
  int _toplamSulama = toplamDk(baslangic, bitis);
  nemdeger = analogRead(nem_sensor);
  nemdeger = map(nemdeger, 0, 4095, 100, 0);
  if (_modKayit == 1) {
    _mod = "Manuel";
  } else {
    _mod = "Otomatik";
    veriGubre = 0;
  }
  String mail = "<strong>Sulama bitti.</strong><br><br><b>Mod: </b>" + _mod +
                "<br><b>Başlangıç saati: </b>" +  baslangic +
                "<br><b>Bitiş saati: </b>" +   bitis  +
                "<br><b>Toplam sulama: </b> " + String(_toplamSulama) + " dk" +
                "<br><b>Başlangıç nemi: </b> " + String(_nemdegerKayit)  +
                "<br><b>Bitiş nemi: </b> "  + String(nemdeger);
  httpRequestData = "&value2=" + mail ;
  sendMail(httpRequestData);
}

void hataMail(int hata) {
  if (WiFi.status() == WL_CONNECTED) {
    if (hata == 1) {
      gubreSuKesintisiMail();
    } else if (hata == 2) {
      gubreBittiMail();
    } else if (hata == 3) {
      suKesintisiMail();
    } else if (hata == 4) {
      suGeldiMail();
    }
  }
}


void wifiKontrol() {
  if (WiFi.status() == WL_CONNECTED) {
    myNex.writeStr("home.wifi.pic=21");
    myNex.writeStr("settings.wifi.pic=21");
  } else if (millis() - eskizaman > 10000) {
    myNex.writeStr("home.wifi.pic=22");
    myNex.writeStr("settings.wifi.pic=22");
    Serial.println("wifi kontrol");
    WiFi.begin(ssid, password);
    eskizaman = millis();
  }
}
float getTarti() {
  return scale.get_units();
}

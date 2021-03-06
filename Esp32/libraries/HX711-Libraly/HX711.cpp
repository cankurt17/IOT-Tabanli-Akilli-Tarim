#include <Arduino.h>
#include <HX711.h>

HX711::HX711(byte dout, byte pd_sck, byte gain) {
	PD_SCK 	= pd_sck;
	DOUT 	= dout;
	
	pinMode(PD_SCK, OUTPUT);
	pinMode(DOUT, INPUT);

	set_gain(gain);
}

HX711::~HX711() {

}

bool HX711::is_ready() {
	return digitalRead(DOUT) == LOW;
}

void HX711::set_gain(byte gain) {
	switch (gain) {
		case 128:		// channel A, gain factor 128
			GAIN = 1;
			break;
		case 64:		// channel A, gain factor 64
			GAIN = 3;
			break;
		case 32:		// channel B, gain factor 32
			GAIN = 2;
			break;
	}

	digitalWrite(PD_SCK, LOW);
	read();
}
long HX711::read() {
  int buffer;
  buffer = 0;

  while (digitalRead(DOUT) == HIGH) {
    yield();
  }
  delayMicroseconds(1);

  for (uint8_t i = 0; i < 24; i++)
  {
      digitalWrite(PD_SCK, HIGH);
      delayMicroseconds(1);
      digitalWrite(PD_SCK, LOW);
      delayMicroseconds(1);
      buffer = buffer << 1 ;

      if (digitalRead(DOUT) == HIGH)
      {
          buffer ++;
      } 


  }

// CHANNEL A, gain 128
  digitalWrite(PD_SCK, HIGH);
  digitalWrite(PD_SCK, LOW);


  buffer = buffer ^ 0x800000;

  return static_cast<long>(buffer);
}

long HX711::read_average(byte times) {
	long sum = 0;
	for (byte i = 0; i < times; i++) {
		sum += read();
	}
	return sum / times;
}

double HX711::get_value(byte times) {
	return read_average(times) - OFFSET;
}

float HX711::get_units(byte times) {
	return get_value(times) / SCALE;
}

void HX711::tare(byte times) {
	double sum = read_average(times);
	set_offset(sum);
}

void HX711::set_scale(float scale) {
	SCALE = scale;
}

void HX711::set_offset(long offset) {
	OFFSET = offset;
}

void HX711::power_down() {
	digitalWrite(PD_SCK, LOW);
	digitalWrite(PD_SCK, HIGH);	
}

void HX711::power_up() {
	digitalWrite(PD_SCK, LOW);	
}
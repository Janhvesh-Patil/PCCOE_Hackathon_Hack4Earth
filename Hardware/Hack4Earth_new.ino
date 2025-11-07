#include "DHT.h"

// === Configuration ===
#define DHTPIN 4       // GPIO pin connected to DHT data
#define DHTTYPE DHT11  // Change to DHT11 if using DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("ESP32 Temperature Sensor Started");
}

void loop() {
  float temperature = dht.readTemperature();  // Celsius

  if (isnan(temperature)) {
    Serial.println("Error reading temperature");
  } else {
    // Send temperature to PC via serial
    Serial.println(temperature);
  }

  delay(5000);  // Send reading every 5 seconds

  while (true);
}


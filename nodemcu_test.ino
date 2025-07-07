#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>

// Wi-Fi credentials
const char* ssid = "YourWiFiName";
const char* password = "YourWiFiPassword";

// Flask server URL (Update with your server IP)
const char* serverUrl = "http://192.168.X.X:5000/predict";

// DS18B20 sensor pin setup
#define ONE_WIRE_BUS 4
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Relay control pin
#define RELAY_PIN 5

// Variables for dynamic calculations
float lastTemp = 30.0;
unsigned long lastTime = 0;

void setup() {
  Serial.begin(115200);
  sensors.begin();
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Ensure cooling is off

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n✅ WiFi Connected.");
}

void loop() {
  sensors.requestTemperatures();
  float temperature = sensors.getTempCByIndex(0);

  // Simulated values for now; replace with INA219/ACS712 readings
  float voltage = 3.6;         // Replace with analogRead() or sensor function
  float current = 1.4;         // Replace with analogRead() or sensor function
  float ambient_temp = 31.5;   // Replace if you have ambient sensor
  float battery_charge = 65.0; // Placeholder, or calculate SoC
  float power = voltage * current;
  float temp_vs_ambient = temperature - ambient_temp;

  // Temperature rise rate calculation
  unsigned long now = millis();
  float time_diff_sec = (now - lastTime) / 1000.0;
  float temp_rise_rate = (time_diff_sec > 0) ? (temperature - lastTemp) / time_diff_sec : 0.0;
  lastTemp = temperature;
  lastTime = now;

  // Create JSON payload
  StaticJsonDocument<512> jsonDoc;
  jsonDoc["temperature"] = temperature;
  jsonDoc["voltage"] = voltage;
  jsonDoc["current"] = current;
  jsonDoc["ambient_temp"] = ambient_temp;
  jsonDoc["battery_charge"] = battery_charge;
  jsonDoc["temp_rise_rate"] = temp_rise_rate;
  jsonDoc["temp_vs_ambient"] = temp_vs_ambient;
  jsonDoc["power"] = power;

  String jsonString;
  serializeJson(jsonDoc, jsonString);

  // Send JSON to ML server
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonString);
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server response: " + response);

      // Check prediction and control relay
      if (response.indexOf("\"prediction\":1") > 0) {
        Serial.println("⚠️ Overheating predicted → Cooling ON");
        digitalWrite(RELAY_PIN, HIGH);
      } else {
        Serial.println("✅ Safe → Cooling OFF");
        digitalWrite(RELAY_PIN, LOW);
      }
    } else {
      Serial.print("HTTP Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("❌ WiFi not connected.");
  }

  delay(15000); // Send every 15 seconds
}

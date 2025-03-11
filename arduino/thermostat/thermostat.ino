#include "ArduinoGraphics.h"
#include "Arduino_LED_Matrix.h"
#include <WiFi.h>
#include <DHT.h>

#define DHTPIN 2
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const char* ssid = "Trogdor";
const char* password = "chrisevan21";

const char* server = "192.168.50.159";
const int port = 5000;

ArduinoLEDMatrix matrix;

float humidity;
float temperature;

bool fan;
bool window;

void setup() {
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED){
    delay(1000);
  }

  dht.begin();
  matrix.begin();
}

void loop() {
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  sendData();
  getState();
  
  matrix.beginDraw();
  matrix.stroke(0xFFFFFFFF);
  char h[3];
  itoa((int)humidity, h, 10);
  matrix.textFont(Font_5x7);
  matrix.beginText(0, 1, 0xFFFFFF);
  matrix.println(h);
  matrix.endText();
  matrix.endDraw();

  delay(5000);

  matrix.beginDraw();
  matrix.stroke(0xFFFFFFFF);
  char t[3];
  itoa((int)temperature, t, 10);
  matrix.textFont(Font_5x7);
  matrix.beginText(0, 1, 0xFFFFFF);
  matrix.println(t);
  matrix.endText();
  matrix.endDraw();

  delay(5000);
}

void getState(){
  WiFiClient client;

  if(WiFi.status() == WL_CONNECTED){
    if(client.connect(server, port)){
      client.print(String("GET ") + "/get_device/thermostat HTTP/1.1\r\n Host: " + server + "\r\nConnection: close\r\n\r\n");
      while(!client.available()){
        delay(1);
      }

      String response = "";
      while(client.available()){
        response += client.readStringUntil('\n');
      }
      client.stop();

      int fanStatusIndex = response.indexOf("\"fan_status\": \"");
      int windowStatusIndex = response.indexOf("\"window_status\": \"");
      if(fanStatusIndex != -1){
        int start = fanStatusIndex + 15;
        int end = response.indexOf("\"", start);
        String fanStatusValue = response.substring(start, end);
        if(fanStatusValue == "on"){
          fan = true;
        }else{
          fan = false;
        }
      }
      if(windowStatusIndex != -1){
        int start = windowStatusIndex + 18;
        int end = response.indexOf("\"", start);
        String windowStatusValue = response.substring(start, end);
        if(windowStatusValue == "open"){
          window = true;
        }else{
          window = false;
        }
      }
    }
  }
}
void sendData(){
  WiFiClient client;
  String payload = "{\"temperature\":" + String(temperature) + ", \"humidity\":" + String(humidity) + "}";

  if(client.connect(server, port)){
    String httpRequest = "POST /update_temperature HTTP/1.1\r\n";
    httpRequest += "Host: " + String(server) + "\r\n";
    httpRequest += "Content-Type: application/json\r\n";
    httpRequest += "Content-Length: " + String(payload.length()) + "\r\n";
    httpRequest += "Connection: close\r\n\r\n";
    httpRequest += payload;

    client.print(httpRequest);

    client.stop();
  }
}
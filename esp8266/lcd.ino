#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

/**
* VCC - VIN
* GND - GND
* SDA - D2
* SCL - D1
*/
LiquidCrystal_I2C lcd(0x27, 16, 2);
const char* WLAN_SSID = "<SSID>";
const char* WLAN_PASSWD = "<Password>";
IPAddress ip( 192, 168, 86, 23 );
IPAddress gateway( 192, 168, 86, 1 );
IPAddress subnet( 255, 255, 255, 0 );
const char* API_BACKLIGHT = "http://192.168.86.100/iot/api/display?place=backlight";
const char* API_LINE_1 = "http://192.168.86.100/iot/api/display?place=line1";
const char* API_LINE_2 = "http://192.168.86.100/iot/api/display?place=line2";
int line1LastUpdated = 0, line2LastUpdated = 0, backlightLastUpdated = 0;

void setup() {
  Serial.begin(115200); 
  Serial.println();
  WiFi.config( ip, gateway, subnet );
  WiFi.begin( WLAN_SSID, WLAN_PASSWD );
  if( WiFi.waitForConnectResult() == WL_CONNECTED ) {
    Serial.println("Connected to Wifi");
  } else {
    Serial.println("Failed to connect to wifi");
  }
  //init lcd.
  lcd.init();
  lcd.begin(16,2);
}

void loop() {
  StaticJsonBuffer<200> jsonBuffer;
  String backlightStr = httpGet(API_BACKLIGHT);
  JsonObject& backlightObj = jsonBuffer.parseObject(backlightStr);
  int backlightUpdate = backlightObj["updated"];
  if (backlightUpdate > backlightLastUpdated) {
    String state = backlightObj["state"];
    if (state.equals("on")) {
      lcd.backlight();
    } else {
      lcd.noBacklight();
    }
    Serial.println("Update backlight to " + String(backlightUpdate));
    backlightLastUpdated = backlightUpdate;
  }

  // line 1 and line 2
  line1LastUpdated = updateLine(API_LINE_1, line1LastUpdated, 0);
  line2LastUpdated = updateLine(API_LINE_2, line2LastUpdated, 1);

  delay(5000);
}

int updateLine(String url, int lastUpdated, int lineNo) {
  StaticJsonBuffer<200> jsonBuffer;
  String lineStr = httpGet(url);
  JsonObject& line = jsonBuffer.parseObject(lineStr);
  int lineUpdated = line["updated"];
  String state = line["state"];
  if (lineUpdated != lastUpdated) {
    Serial.println("Update line " + String(lineNo) + " to " + String(lineUpdated));
    while (state.length() < 16) {
      state.concat(' ');
    }
    lcd.setCursor(0, lineNo);
    lcd.print(state);
    Serial.println(state);
    return lineUpdated;
  } else {
    return lastUpdated;
  }
}

String httpGet(String url) {
  HTTPClient http;
  http.begin(url);
  String response;
  int httpCode = http.GET();
  if (httpCode == HTTP_CODE_OK) {
    response = http.getString();
  } else {
    Serial.println("Failed to get "+url+" with error "+httpCode);
  }
  http.end();
  return response;
}


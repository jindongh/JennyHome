#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#define MAGIC_NUM 654321

/**
* 3V3 - VCC
* GND - GND
* D2  - IN
*/
void connectWifi();
void turnOffWifi();
void gotoSleep();
bool getState();
void updateState(bool isOn);
void turnOn();
void turnOff();
const char* WLAN_SSID = "<SSID>";
const char* WLAN_PASSWD = "<Password>";
const char* API_GET = "http://192.168.86.100/iot/api/relay?place=thermostat";
const char* API_ON = "http://192.168.86.100/iot/api/relay?place=thermostat&value=on";
const char* API_OFF = "http://192.168.86.100/iot/api/relay?place=thermostat&value=off";
int RELAY_PIN = 4;//D2
int DEEP_SLEEP_TIME = 5 * 60 * 1000000; // macro ms
int DELAY_TIME = 5 * 60 * 1000; // ms
IPAddress ip( 192, 168, 86, 21 );
IPAddress gateway( 192, 168, 86, 1 );
IPAddress subnet( 255, 255, 255, 0 );

void setup() {
  Serial.begin(115200);
  Serial.println();

  connectWifi();
  bool isOn = getState();
  if (isOn) {
    Serial.println("Relay is on");
    turnOn();
    updateState(true);
    turnOffWifi();
  } else {
    Serial.println("Relay is off, go to sleep");
    gotoSleep();
  }
}

void loop() {
  delay(DELAY_TIME);
  connectWifi();

  bool isOn = getState();
  if (isOn) {
    Serial.println("Relay is still on, will turn off wifi");
    turnOffWifi();
  } else {
    Serial.println("Turn off relay and go to sleep");
    turnOff();
    updateState(false);
    gotoSleep();
  }
}

struct {
  uint32_t magic;   // 4 bytes
  uint8_t channel;  // 1 byte,   5 in total
  uint8_t bssid[6]; // 6 bytes, 11 in total
  uint8_t padding;  // 1 byte,  12 in total
} rtcData;
void connectWifi() {
  WiFi.forceSleepWake();
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  delay(1);
  WiFi.config( ip, gateway, subnet );
  if( ESP.rtcUserMemoryRead( 0, (uint32_t*)&rtcData, sizeof( rtcData )) && rtcData.magic == MAGIC_NUM ) {
    Serial.println("Connect with rtc data");
    WiFi.begin( WLAN_SSID, WLAN_PASSWD, rtcData.channel, rtcData.bssid, true);
  } else {
    Serial.println("Connect with password");
    WiFi.begin( WLAN_SSID, WLAN_PASSWD );
  }
  if( WiFi.waitForConnectResult() == WL_CONNECTED ) {
    Serial.println("Connect succeed");
  } else {
    Serial.println("Connect failed, will retry with password");
    WiFi.begin(WLAN_SSID, WLAN_PASSWD);
    if (WiFi.waitForConnectResult() == WL_CONNECTED) {
      Serial.println("Connect succeed after retry");
        rtcData.channel = WiFi.channel();
        memcpy( rtcData.bssid, WiFi.BSSID(), sizeof(rtcData.bssid) ); // Copy 6 bytes of BSSID (AP's MAC address)
        rtcData.magic = MAGIC_NUM;
        ESP.rtcUserMemoryWrite( 0, (uint32_t*)&rtcData, sizeof( rtcData ) );
    } else {
      Serial.println("Connect failed after retry, will goto sleep");
      Serial.println(WiFi.status());
      gotoSleep();
    }
  }
}
void turnOffWifi() {
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  delay(1);
  Serial.println("Wifi is off");
}
void gotoSleep() {
  WiFi.disconnect();
  WiFi.mode( WIFI_OFF );
  WiFi.forceSleepBegin();
  delay(1);
  ESP.deepSleep( DEEP_SLEEP_TIME );
}

bool getState() {
  HTTPClient http;
  bool isOn;
  http.begin(API_GET);
  int httpCode = http.GET();
  if (httpCode != 200) {
    Serial.println("Failed to get state with httpCode " + String(httpCode));
    isOn = false;
  } else {
    StaticJsonBuffer<200> jsonBuffer;
    String response = http.getString();
    JsonObject& responseObj = jsonBuffer.parseObject(response);
    String state = responseObj["state"];
    isOn = state.equals("on");
  }
  http.end();
  return isOn;
}

void updateState(bool isOn) {
  HTTPClient http;
  if (isOn) {
    http.begin(API_ON);
  } else {
    http.begin(API_OFF);
  }
  int httpCode = http.GET();
  Serial.println("Update state to server");
}

void turnOn() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
}

void turnOff() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
}


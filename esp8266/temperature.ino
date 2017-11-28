#include <OneWire.h> 
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#define MAGIC_NUM 654321
#define RELAY_PIN 4 
#define DEEP_SLEEP_TIME 5 * 60 * 1000000 /* 5 minutes */


/**
* 3V3 - VCC
* GND - GND
* D2 - IN
*/
const char* WLAN_SSID = "<SSID>";
const char* WLAN_PASSWD = "<Password>";
const char* API = "http://192.168.86.100/iot/api/temperature?place=bedroom&value=";
IPAddress ip( 192, 168, 86, 22 );
IPAddress gateway( 192, 168, 86, 1 );
IPAddress subnet( 255, 255, 255, 0 );
OneWire oneWire(RELAY_PIN); 
DallasTemperature sensors(&oneWire);
float getTemperature();
void reportTemperature(float temperature);
void connectWifi();
void gotoSleep();

void setup(void) 
{ 
  Serial.begin(115200); 
  Serial.println();
  Serial.println("Temperature Reporter"); 
  WiFi.forceSleepBegin();
  float temperature = getTemperature();
  Serial.print("Temperature(C) is ");
  Serial.println(temperature);
  connectWifi();
  Serial.println("Wifi is ready");
  reportTemperature(temperature);
  Serial.println("Report is done, will go to sleep");
  delay(2000);
  gotoSleep();  
} 

void loop(void) {}

float getTemperature() {
  sensors.begin(); 
  sensors.requestTemperatures();
  return sensors.getTempCByIndex(0);
}

void reportTemperature(float temperature) {
  HTTPClient http;
  String url = String(API) + String(temperature);
  http.begin(url);
  int httpCode = http.GET();
  Serial.print("Report temperature result:");
  Serial.println(httpCode);
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
    Serial.println("Connect failed");
    WiFi.begin(WLAN_SSID, WLAN_PASSWD);
    if (WiFi.waitForConnectResult() == WL_CONNECTED) {
      Serial.println("Connect succeed after retry");
    } else {
      Serial.println(WiFi.status());
    }
  }
  rtcData.channel = WiFi.channel();
  memcpy( rtcData.bssid, WiFi.BSSID(), sizeof(rtcData.bssid) ); // Copy 6 bytes of BSSID (AP's MAC address)
  rtcData.magic = MAGIC_NUM;
  ESP.rtcUserMemoryWrite( 0, (uint32_t*)&rtcData, sizeof( rtcData ) );
}

void gotoSleep() {
  WiFi.disconnect( true );
  delay(10);
  WiFi.mode( WIFI_OFF );
  delay(10);
  ESP.deepSleep( DEEP_SLEEP_TIME, WAKE_RF_DISABLED );
}


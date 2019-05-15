#include <SoftwareSerial.h>
SoftwareSerial gprsSerial(11, 10);

#include <DHT.h>
#define DHTPIN 2     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);
float f;
float h;

#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 12
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
float bt;

void setup()
{
  gprsSerial.begin(19200);
  Serial.begin(19200);

  Serial.println("Config SIM900...");
  delay(2000);
  Serial.println("Done!...");
  gprsSerial.flush();
  Serial.flush();

  // ensure GPRS disconnected
  gprsSerial.println("AT+SAPBR=0,1");
  //delay(2000);
  //toSerial();

  // attach or detach from GPRS service 
  gprsSerial.println("AT+CGATT?");
  delay(100);
  toSerial();

  // bearer settings
  //gprsSerial.println("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"");
  delay(2000);
  toSerial();

  // bearer settings
  //gprsSerial.println("AT+SAPBR=3,1,\"APN\",\"www\"");
  delay(2000);
  toSerial();

  // bearer settings
  gprsSerial.println("AT+SAPBR=1,1");
  delay(2000);
  toSerial();

}


void loop()
{
  send_data_to_api();
}

void send_data_to_api()
{
  String post_data;
  get_temperature(post_data);
  gprsSerial.println(post_data);
  delay(5000);
  
  // initialize http service
  gprsSerial.println("AT+HTTPINIT");
  delay(2000); 
  toSerial();

  // set http param value
  gprsSerial.println("AT+HTTPPARA=\"URL\",\"http://api.beepeeker.com/dev_metrics\"");
  delay(1000);
  toSerial();

   // set http content type to JSON
   gprsSerial.println("AT+HTTPPARA=\"CONTENT\",\"application/json\"");
   delay(1000);
   toSerial();

   // set http DATA length and supply data
   gprsSerial.println("AT+HTTPDATA=256,10000");
   toSerial();
   delay(1000);
   gprsSerial.println(post_data);
   toSerial();
   delay(10000);

   // set http action type 0 = GET, 1 = POST, 2 = HEAD
   gprsSerial.println("AT+HTTPACTION=1");
   delay(6000);
   toSerial();

   // read server response
   gprsSerial.println("AT+HTTPREAD"); 
   delay(1000);
   toSerial();

   gprsSerial.println("");
   gprsSerial.println("AT+HTTPTERM");
   toSerial();
   delay(300);

   gprsSerial.println("");
   delay(300000);
 }

void toSerial()
{
  while(gprsSerial.available()!=0)
  {
    Serial.write(gprsSerial.read());
  }
}

void get_temperature(String &generate_data) {
  delay(5000);
  f = dht.readTemperature(true);
  h = dht.readHumidity();
  sensors.requestTemperatures();
  bt = (sensors.getTempCByIndex(0)) * 9.0 / 5.0 + 32;

  generate_data = "{\"temp1\":\""+String((float)f)+"\",\"humidity1\":\""+String((float)h)+"\",\"broodtemp1\":\""+String((float)bt)+"\",\"datetime\":\"2016-10-13 10:34:56\",\"account_id\":\"001\",\"device_id\":\"101010\",\"weight\":\"0\"}";
}


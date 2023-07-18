#include <Arduino.h>
// #include <esp8266WiFi.h>
#include <SPI.h>
#include <Wire.h>
#include <fdrs_globals.h>
#include <fdrs_node.h>
#include <SD.h>
#include <DHT.h>
#include <SFE_BMP180.h>

DHT dht(DHT_PIN, DHT_TYPE);// pour capteur dht11 humi/temp
SFE_BMP180 pressure;// pour capteur BMP180 pression/temp


void setup() {
    beginFDRS();
    dht.begin();
    pressure.begin();
    if (!SD.begin(SD_CS)) {
        Serial.println("Fail, verifier que la carte SD est presente.");
        return;
    }
}

void loop() {

    // mesure DHT11
    float data1 = dht.readHumidity();
    float data2 = dht.readTemperature();

    if (isnan(data1) || isnan(data2)) {
        DBG("Failed to read from DHT sensor!");
        return;
    }

    // mesure BMP180
    double data3;
    double data4;

    char status = pressure.startTemperature();

    if (status != 0){
        delay(status);
        status = pressure.getPressure(data3,data4);
    }
    if(status == 0){
        DBG("failed to read BMP sensor!")
        return;
    }

    loadFDRS(data1, HUMIDITY_T);
    loadFDRS(data2, TEMP_T);
    loadFDRS(data3, PRESSURE_T);
    sendFDRS();

    File dataFile = SD.open(LOG_FILENAME, FILE_WRITE);
    if (dataFile) {
        DBG("SD OK");
        dataFile.print("[{\"id\":");
        dataFile.print(READING_ID);
        dataFile.print(",\"type\":");
        dataFile.print(HUMIDITY_T);
        dataFile.print(",\"data\":");
        dataFile.print(data1);
        dataFile.print("},{\"id\":");
        dataFile.print(READING_ID);
        dataFile.print(",\"type\":");
        dataFile.print(TEMP_T);
        dataFile.print(",\"data\":");
        dataFile.print(data2);
        dataFile.print("},{\"id\":");
        dataFile.print(READING_ID);
        dataFile.print(",\"type\":");
        dataFile.print(PRESSURE_T);
        dataFile.print(",\"data\":");
        dataFile.print(data3);
        dataFile.println("}],");
        dataFile.close();
    }else{
        DBG("SD fail");
    }
    sleepFDRS(10);  //Sleep time in seconds
}

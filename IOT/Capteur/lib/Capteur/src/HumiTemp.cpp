#include "../include/HumiTemp.h"

HumiTemp::HumiTemp(int pin, uint8_t type):
    Capteur("H/T"){
    this->capteur = new DHT(pin, type);
    this->capteur->begin();
}

int HumiTemp::getTemp(){
    int temp = this->capteur->readTemperature();
    if(isnan(temp)){
        Serial.println(" DHT reading failed ");
        return -1;
    }
    return temp;
}

int HumiTemp::getHumi(){
    int hum = this->capteur->readHumidity();
    if(isnan(hum)){
        Serial.println(" DHT reading failed ");
        return -1;
    }
    return hum;
}

String HumiTemp::read(){
    String sortie = "";

    sortie += String(this->getHumi());
    sortie += "/";
    sortie += String(this->getTemp());
    return sortie;
}

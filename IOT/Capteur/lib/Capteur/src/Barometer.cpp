#include "../include/Barometer.h"

Barometer::Barometer():
    Capteur("P/T"){
    this->capteur = new SFE_BMP180();
    this->capteur->begin();
}

int Barometer::getTemp(){
    char status = capteur->startTemperature();
    if (status != 0){
        delay(status);
    }
    double temp;
    status = this->capteur->getTemperature(temp);
    if(status == 0){
        Serial.println("Temperature reading failed ");
        return -1;
    }
    return temp;
}

int Barometer::getPressure(){
    char status = this->capteur->startPressure(3);
    if(status){
        delay(status);
    }
    double press = 0;
    double T = 0;
    status = this->capteur->getPressure(press, T);
    if(status == 0){
        Serial.println("Pressure reading failed ");
        return -1;
    }
    return press;
}

String Barometer::read(){
    String sortie = "";

    sortie += String(this->getPressure());
    sortie += "/";
    sortie += String(this->getTemp());
    return sortie;
}

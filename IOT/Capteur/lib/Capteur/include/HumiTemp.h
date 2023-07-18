#ifndef HUMI_TEMP_H
#define HUMI_TEMP_H

#include <Arduino.h>
#include <DHT.h>
#include "Capteur.h"

class HumiTemp : public Capteur{

public:

    /**
     * @brief Construct a new Humi Temp object
     * 
     * @param pin pin du capteur dht
     * @param type type de capteur dht (11,22,...)
     */
    HumiTemp(int pin, uint8_t type);

    /**
     * @brief lit le capteur d'humi/temp
     * 
     * @return String valeur format "XX/YY" X% et Y°C
     */
    String read();

    //TODO: faire commentaire
    int getTemp();
    int getHumi();

private:
    
    DHT* capteur;

};


#endif //HUMI_TEMP_H

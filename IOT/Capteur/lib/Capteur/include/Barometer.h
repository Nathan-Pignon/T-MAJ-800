#ifndef BAROMETER_H
#define BAROMETER_H

#include <Arduino.h>
#include <SFE_BMP180.h>
#include <Wire.h>
#include "Capteur.h"

class Barometer :  public Capteur{
public:

    /**
     * @brief Construct a new Capteur object
     * 
     */
    Barometer();

    /**
     * @brief lit la valeur du capteur
     * 
     * @return String valeur forma "XX/YY" X mBar et Y °C
     */
    virtual String read();

    /**
     * @brief retourne le type de valeur lue
     * 
     * @return String 
     */
    String getValType();

    //TODO: faire commentaire
    int getTemp();
    int getPressure();

private:

    //TODO: faire commentaire
    SFE_BMP180* capteur;

};


#endif // BAROMETER_H

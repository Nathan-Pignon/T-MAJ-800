#ifndef PROGRAM_H
#define PROGRAM_H

#include <Arduino.h>
#include "Capteur.h"
#include "HumiTemp.h"
#include "Barometer.h"

class Program {
public:
    /**
     * Program startup
     */
    Program();

    /**
     * Program main loop
     */
    void loop();
private:

    //TODO: faire commentaire
    Capteur* DHT;
    Capteur* barometer;

};

#endif

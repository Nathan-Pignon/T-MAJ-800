#ifndef CAPTEUR_H
#define CAPTEUR_H

#include <Arduino.h>

class Capteur{
public:

    /**
     * @brief Construct a new Capteur object
     * 
     * @param[in] type type de mesure lue (T/H, W, D,...)
     */
    Capteur(String type);

    /**
     * @brief tar le capteur si il a besoins d'être tarré
     * 
     * @param[in] val *opt* si le capteur a besoins d'une valeur de ref pour être tarré
     * @return true si la tarre a bien réussi (ou si il n'a pas besoins de tarre)
     * @return false erreur durrant la tar
     */
    virtual bool tar(int val = 0);

    /**
     * @brief lit la valeur du capteur
     * 
     * @return String retour la valeur
     */
    virtual String read() = 0;

    /**
     * @brief retourne le type de valeur lue
     * 
     * @return String 
     */
    String getValType();

protected:
    /**
     * @brief type de mesure lue (T/H, W, D,...)
     * 
     */
    String type;

};


#endif // CAPTEUR_H

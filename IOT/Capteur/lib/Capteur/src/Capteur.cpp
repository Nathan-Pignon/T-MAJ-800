#include "../include/Capteur.h"

Capteur::Capteur(String type){
    this->type = type;
}

bool Capteur::tar(int val){
    return true;
}

String Capteur::getValType(){
    return this->type;
}
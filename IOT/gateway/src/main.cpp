//  FARM DATA RELAY SYSTEM
//
//  GATEWAY 2.000
//
//  Developed by Timm Bogner (timmbogner@gmail.com) in Urbana, Illinois, USA.
//

#include <Arduino.h>
#include <SPI.h>
#include <fdrs_gateway.h>
void setup() {
beginFDRS();
}

void loop() {
loopFDRS();
}
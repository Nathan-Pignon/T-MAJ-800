#include "Program.h"

Program::Program() {
    // Startup
    Serial.begin(MONITOR_SPEED);
    this->DHT = new HumiTemp(DHT_PIN, DHT_TYPE);
    this->barometer = new Barometer();
}

void Program::loop() {
    // Loop
    delay(2000);
    Serial.print(this->DHT->read());
    Serial.print('\t');
    Serial.print(this->barometer->read());


    Serial.println();
}

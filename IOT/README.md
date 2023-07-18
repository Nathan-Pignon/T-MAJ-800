# Section IOT :

## POC :

original depot : [gitea](https://git.lab-ouest.org/Epitech/T-MAJ-800_msc2024)

code compilé via [platformio](https://platformio.org/)

### Capteur :

- BMP180 (baromètre)

- DHT11 (humidité, température)

Communication LoRa (via lib [FDRS](https://github.com/timmbogner/Farm-Data-Relay-System))

Stockage des donnée sur carte SD

Prise de mesure toute les 10 seconds avec deepSleep entre chaque mesure

Schémas de câblage sous [kicad 7.0](https://www.kicad.org/)



### Gateway :

Carte original : [TTGO LoRa32 SX1276 OLED](https://fr.aliexpress.com/item/4001275174741.html)

Communication LoRa (via lib [FDRS](https://github.com/timmbogner/Farm-Data-Relay-System))

Envoi des données sur api (WIP) et sur le terminal serie


https://github.com/Nathan-Pignon/T-MAJ-800/blob/main-IOT/IOT/img/photo_1_2023-07-18_15-35-55.jpg


![archi global](img/archiGraph.png)

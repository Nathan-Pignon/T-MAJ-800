---
tags: Epitech, Voltron, MAJ
---

original file : https://hedgedoc.cb85.software/TZCWQHD4SjO17wnNnQuOsA#

# Chiffrage solution IOT :

[TOC]

## Chiffrage processeur :

pour le processeur des capteurs, nous avons choisi les ESP8266 car suffisant pour le besoin et peu consommateur d'énergie

ESP8266 :

- Consommation : 72 mA
- Consommation en sommeil : 20 µA
- Wifi : oui *non utiliser*
- GPIO : 16
- PRIX : 10€×2

*pris de l'esp sur Amazon*

ESP32-C3 :
- Consommation faible activité : 22 mA
- Wifi : oui *non utiliser*
- GPIO : 22
- PRIX : 15,90 €

[gotronic](https://www.gotronic.fr/art-carte-esp32-c3-devkitm-1-34172.htm)

## Choix Capteur :

|     | DHT11 | DHT22 | Jeu de capteurs météo | Capteur d'humidité GT110 | Baromètre | ML8511 SEN0175 |
| --- | --- | --- | --- | --- | --- | --- |
| type de capteur | humidité / température (air) | humidité / température (air) | pluviomètre<br/>anémomètre<br/>girouette | humidité (sol) | pression atmosphérique | Capteur UV |
| précision | ± 2 °C<br/>± 5 % | ± 0,5 °C<br/>± 2 % | 0,2794 mm<br/>2,4 km/h<br/>16 secteur | Sortie analogique | 0,01 hPa | 280 à 390 nm |
| prix | 2,90 € | 10,90 € | 99,90 € | 2,40 € | 19,80 € | 11,30 € |
| type de connectique | digital IO | digital IO | IO / IO / 8 analogue | analogique | I2C | analogique |

*tous les prix viennent de Gotronic*

humi/temp
https://www.gotronic.fr/art-capteur-de-t-et-d-humidite-dht11-20692.htm
https://www.gotronic.fr/art-capteur-de-t-et-d-humidite-dht22-20719.htm

capteur météo
https://www.gotronic.fr/art-jeu-de-capteurs-meteo-33052.htm

humidité sol
https://www.gotronic.fr/art-capteur-d-humidite-gt110-26091.htm

baromettre
https://www.gotronic.fr/art-barometre-de-precision-grove-101020068-21822.htm

capteur d'ensoleillement (UV)
https://www.gotronic.fr/art-capteur-uv-ml8511-sen0175-22701.htm

lecteur SD :
https://www.gotronic.fr/art-module-carte-sd-gt126-28506.htm


## choix émetteur récepteur LoRa :

pour le choix de l'émetteur récepteur LoRa, nous avons choisi le SX1278, car il est de petite taille, est très abordable et répond à nos besoins.

https://www.amazon.com/Comimark-SX1278-Wireless-Mental-Arduino/dp/B07W6ZPH7D/

## choix batterie

pour l'alimentation des capteurs, nous pensons partir sur une batterie seule pour diminuer la taille et le prix des capteurs. Cette solution à la contrainte qu'il faut venir changer les batteries à intervalle régulé, mais qui permet d'avoir un contrôle périodique des capteurs. 

pour le choix de la batterie, nous pensons partir sur le format 18650, parce que le plus standard et le moins cher aujourd'hui.

le choix n'est pas définitif, car il faut d'abord calculer la capacité nécessaire au fonctionnement des capteurs pendant une longue durée.

### technologie batterie

*(risque sur les batteries : [stress test](https://www.youtube.com/watch?v=Qzt9RZ0FQyM))*

#### Li-Po/Li-Ion

les technologies Li-Po et Li-Ion sont les plus communes pour ce genre d'application. Elles sont les moins chers et ont la meilleure capacité. Elles ont cependant quelques inconvénients :

- Elle résiste moyennement aux basses températures
    *(surtout si on leur demande une grosse puissance ce qui n'est pas notre cas)*
- Elles perdent de leur capacité au fils du temps
    *(Ce qui force à les changer tous les 5/10 ans)*
- Si elles sont endommagées, elles peuvent prendre feu
    *(ce qui peu posé un problème si l'agriculteur labour sans retirer les capteurs)*
    
- (500/1000 cycles de charge max)

il est aussi facile de connaitre la capacité restante de la batterie en fonction de sa tension restante


#### Plomb

technologie traditionnelle de batterie, elles n'ont pas de risque d'explosion et tiennent très bien au froid, mais elles ont grosse lourde et ne stocke qu'une faible quantité d'énergie, elle ne corresponde donc pas à nos besoins.

#### LiFePo4

technologie similaire au Li-Ion, elle stocke moins d'énergie et sont plus légèrement plus sensible au froid. Elles ont néanmoins l'avantage de ne pas générer d'explosion en cas d'endommagement. Elles sont aussi moins sujettes à l'usure dans le temps. Il est aussi complexe de voir la capacité de la batterie, car elle reste assez constance (3,6 V) sauf a charge ou décharge complète.

- (2000 cycles de charge max)

[comparaison avec lipo](https://www.youtube.com/watch?v=eiyBavjQ1Rk)

#### NiMH

technologie traditionnelle des "piles rechargeables" disponible en forma standard (AA, AAA…). Elle n'explose pas non plus en cas de dommage physique, mais sont extrêmement sensibles au froid et est donc exclu d'office du projet


### technologie de pile

#### Alkaline

pile traditionnelle en forma AA, AAA... avantage d'être pas dangereux en cas de dommage physique. Elle est également très abordable, mais n'est pas rechargeable après utilisation et doit donc être changé périodiquement. Elles sont généralement utilisées pour les applications à faible demande énergétique.


#### Li-SoCl2
pile pour conçue pour une utilisation en condition extrême et pour des applications à très faible demande énergétique. Les piles Lithium-Thionyl-Chlorid non rechargeable son idéal pour l'utilisation en condition de -60 à plus 80°C. Elles sont aussi écartées, car surdimensionné pour les besoins du projet.

### choix des batteries :

pour bien choisir une batterie, il faut commencer par calculer la consommation de notre système sur une unité de temps donnée.

dans notre cas ont par du principe que l'on fait une mesure par heure sur un pat de temps d'une journée.

#### consommation capteur :

pour chaque capteur il y a des composants communs que sont l'ESP et le module LoRa. Ils ont aussi tous les 2 un "sleep mode" qui permet de fortement réduire leur consommation entre les périodes d'activité.

*pour simplifier, nous partons du principe que la période d'activité est de 15 seconde par heure*

nous cherchons à savoir la consommation par heures des éléments pour qualifier la taille de batterie nécessaire au fonctionnement.

module LoRa : 120 mA émission et 0.2 µA sleep mode

$$
mAh = \frac{120\times 6 + 0.0002\times 24\times59.75}{24\times60}\\
mAh = 0.5
$$

l'esp : 72 mA Fonctionnement et 20 µA sommeil

$$
mAh = \frac{72\times 24 + 0.02\times24\times59}{24\times60}\\
mAh = 1.2
$$

la consommation pour les composants communs du système est de $1.2 + 0.5 = 1.7 mAh$ en moyenne par heure.




## boitier

pour le boitier, nous pensons en concevoir un sur mesure pour les différents capteurs pour les imprimés en 3D. Le coup n'est donc pas définitif, mais nous pouvons néanmoins l'estimer à 5€ par capteur, car le coup pour ce genre d'application ne dépasse que très rarement cette somme. Il devra être d'une couleur très visible comme blanc, jaune ou orange pour être plus facilement visible par les viticulteurs.

# pris unitaire du capteur :

## station météo :

la station météo contient un ensemble de capteur pour mesurer les conditions météo du vignoble. Une seule station est requise pas vignoble *(voir une 2nd suivant la typologie du terrain)*

liste des mesures lue :

- humidité air
- température air
- pression atmosphérique
- direction vent
- vitesse vent
- pluviomètre
- ensoleillement

### Consomation :

ESP32-C3[^espC3]: 22 mAh

LoRa : 0.5 mAh

[^espC3]:l'utilisation du C3 par apport au 8266 est requis, car les capteurs de vent et de pluviométrie fonctionne via impulsion, donc requière que le processeur soit constamment en fonctionnement.


DHT22 : 1,5 mA mesure et 50 µA sleep mode (0.056 mAh)

$$
mAh = \frac{1,5\times 6 + 0.05\times 24\times59.75}{24\times60}\\
mAh = 0.056
$$

Baromètre Grove : 1.1 mAh$

SEN0175 : 0.5mA mesure et 1 µA sleep mode (0.004 mAh)

$$
mAh = \frac{0,5\times 6 + 0.001\times 24\times59.75}{24\times60}\\
mAh = 0.004
$$


le jeu de capteur météo étant à impulsion, nous partons du principe que sa consommation est négligeable.

**TOTAL :**

$$
22+0.5+0.056+1.1+0.004 = 23.66 mA
$$

le système utilise une puissance totale de 23.66 mA de moyenne

sur une journée, il aura donc utilisé : $24\times23.66 = 567.84 mAh$

### L'alimentation :

du fait de la consommation relativement élever du système *(pour une batterie de 3000 mAh l'autonomie n'est que de 5 jours !)* il est intéressant voir indispensable d'ajouter un panneau solaire à notre installation pour ne pas avoir a changé très régulièrement sa batterie.

[panneau solaire batterie](https://fr.aliexpress.com/item/1005003119869019.html?spm=a2g0o.detail.1000013.2.5060sQhMsQhMmt&gps-id=pcDetailBottomMoreThisSeller&scm=1007.13339.291025.0&scm_id=1007.13339.291025.0&scm-url=1007.13339.291025.0&pvid=6bdd1385-9e48-4d0a-81bb-348fc20a9620&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.13339.291025.0,pvid:6bdd1385-9e48-4d0a-81bb-348fc20a9620,tpp_buckets:668%232846%238112%231997&isseo=y&pdp_npi=3%40dis%21EUR%2143.55%2127.44%21%21%21%21%21%4021059dbe16876173426443185e3b1d%2112000024246369624%21rec%21FR%212432164328)
ce genre de dispositif est idéal pour notre application, car il en braque 6000 mAh (soit 10 jours de batterie dans notre cas) et a un panneau solaire de 5w qui est suffisant pour la recharge des batteries en journée.


### Prix total :


| composant        | pris unitaire | quantité | prix total |
| ---------------- | ------------- | -------- | ---------- |
| esp32 C3         | 15,90€        | 1        | 15,90€     |
| émetteur LoRa    | 7€            | 1        | 7€         |
| DHT22            | 10,90€        | 1        | 10,90€     |
| capteur météo    | 99.90€        | 1        | 99.90€     |
| Baromètre        | 19,80 €       | 1        | 19,80 €    |
| SEN0175          | 11,30 €       | 1        | 11,30 €    |
| Batterie solaire | 48,43€        | 1        | 48,43€     |
| boitier          | 15€           | 1        | 15€        |
| Lecteur SD       | 2,10 €        | 1        | 2.10 €     |
| **TOTAL**        |               |          | **230,33** |


le système a un coût total de 230,33€ pour le matériel.

## capteur au sol

le capteur au sol est un système d'une petite taille sous la forme d'une carotte qui s'enfonce quelques centimètres dans le sol leur but est de monitorer l'humidité du sol dans le but de mieux répartir l'arrosage du sol

### Consommation : 

LoRa : 0.5 mAh *voir calcule au-dessus*
esp8266 : 1.2 mAh *voir calcule au-dessus*
le capteur GT110 est un capteur analogique passif, sa consommation est négligeable

$$
1.2 + 0.5 = 1.7 mAh
$$

$$
1.7 \times 24 = 40.8 mAh
$$

les capteurs au sol ont une consommation moyenne de 40.8 mAh par jour

les batteries LiFePo4 sont les mieux adaptées à cette utilisation, car les capteurs peuvent être sujets à des dommages physiques en cas de labour du vignoble.

[ref batterrie](https://fr.aliexpress.com/item/1005004937180552.html?spm=a2g0o.productlist.main.1.2e8ddcae7O2ZaX&algo_pvid=36a9e9a7-5276-418d-8069-23992b22e1d2&aem_p4p_detail=202306240144214693746228715440014133077&algo_exp_id=36a9e9a7-5276-418d-8069-23992b22e1d2-0&pdp_npi=3%40dis%21EUR%2123.06%2114.76%21%21%21%21%21%4021021f7b16875962619047930d076d%2112000031081332818%21sea%21FR%212432164328&curPageLogUid=ewjCCm1mJO45&search_p4p_id=202306240144214693746228715440014133077_1) = 14,82€ les 4 soit 3.70 € unité

avec 2 batteries de ce type mise en parallèle l'autonomie des capteurs est de :
$$
\frac{3000\times2}{40.8} = 147
$$

l'autonomie du capteur est estimée à 147 jours soit environ 5 mois.


### prix total


| composant        | pris unitaire | quantité | prix total |
| ---------------- | ------------- | -------- | ---------- |
| esp8266          | 5€            | 1        | 5€         |
| émetteur LoRa    | 7€            | 1        | 7€         |
| GT110            | 2.40€         | 1        | 2.40€      |
| Batterie         | 3.70€         | 2        | 7.42€      |
| boitier          | 10€           | 1        | 10€        |
| Lecteur SD       | 2,10 €        | 1        | 2.10 €     |
| **TOTAL**        |               |          | **33.92**  |



# placement des capteurs

Le chiffrage des capteurs dépend beaucoup du nombre et du placement des capteurs.
Ce nombre varie beaucoup en fonction de la taille du vignoble et de sa topologie.

## Station météo :

comme déjà précisé au-dessus 1 seul par vignoble nous parait suffisant (une 2nd pour les grands vignobles)

## capteur au sol :

les capteurs au sol mesurent l'humidité au sol. Il permet un arrosage plus efficace et responsable des vignes.

plus il y a de capteur dans le vignoble, plus le résultat sera précis. Nous pensons que 4 capteurs par hectare (soit 1 tous les 50 m) est une bonne approche. On peut monter à 9 (un tous les 33 m) pour les vignobles ou le terrain est le plus demandeur.


## cable cam :

pour la cable cam, on peut repartir sur des solutions du commerce que l'on adaptera par la suite à nos besoins

[cable cam motorisé](https://fr.aliexpress.com/item/32975149119.html)
[gimbal](https://fr.aliexpress.com/item/32861971456.html)
[Caméra](https://fr.aliexpress.com/item/1005003804757059.html)
[batterie](https://fr.aliexpress.com/item/1005003119869019.html)

— La caméra sera capable de communiqué avec les différents composants du système (moteur, ...)
— Le système de batterie solaire peut servir pour la caméra également.
- La caméra est équipée de wifi et d'un lecteur de carte SD pour stocker les images en local en cas de problème de WiFi.

| composant        | pris unitaire | quantité | prix total |
| ---------------- | ------------- | -------- | ---------- |
| cable cam        | 674,88€       | 1        | 674,88€    |
| gimbal           | 158,38€       | 1        | 158,38€    |
| Caméra           | 5,56€         | 1        | 5,56€      |
| Batterie Solaire | 27,55€        | 1        | 27,55€     |
| boitier          | 15€           | 1        | 10€        |
| **TOTAL**        |               |          | **876,37** |

# maintenance :

## station météo :

Aucune maintenance spécifique est à prévoir. Une usure des capteurs mécanique peu avoir lieux dans le temps en cas de valeur incorrect le vigneron devra nous le signaler pour que l'on identifie le problème

## capteur au sol :

Le vigneron aura une courte formation sur la maintenance des capteurs qui consiste au changement des batteries pour les mettre a chargé environ deux fois par ans.

Si au bout de plusieurs années, l'autonomie des capteurs basse trop, le vigneron peut changer le jeu de batterie pas des batteries neuve de caractéristique équivalente.

Comme la technologie de batterie utilisée permet difficilement de connaitre la capacité restante, l'estimation de la capacité est basée sur le temps (environ six mois d'autonomie). Le vigneron sera alerter après le temps écoulé ou a l'arrêt prolongé de la transmission de valeur par un capteur

## data logging :

Chaque capteur ainsi que les stations météos sont tous équipés de carte SD pour le stockage en local des données lue. Elle sera de petite taille et choisie en fonction de son nombre de cycles d'écriture pour une longévité maximal

### calcul capacité :

le calcul de la capacité est fait avec le POC mais pour donnée un ordre de grandeur qui sera applicable au capteur réel.

pour 430 valeur on arrive a un fichier de 41 944 octects soit environ 97,5 onctect par valeurs.

une carte SD de 4 Go fait 4 000 000 000 octect environ

on peut donc stocké 41 237 113 valeur a une mesur par heure on a un stockage de 4707 ans

# TODO:
- faire un truc example pour 21 hectar
- faire shéma a la con d'un type de vignioble

---
tags: Epitech, Voltron, MAJ
---

original file: https://hedgedoc.cb85.software/4rP7InXrSYm-2ImgqBJMbA#

# Documentation Voltron IOT


[TOC]


## prise de mesure

Cette partie tente de répondre au besoin de prise de mesure environnemental dans un vignoble. Elle sera faite via un nuage de petite capteur autonome répartie dans les différentes parcelles en fonction de la topographie du site.

### type de valeur :

- l'humidité de l'air
- la température
- pression atmosphérique

Ces mesures nous renseignent sur la qualité de l'environnement à différent endroit dans le vignoble. Elles peuvent aider à l'anticipation de l'apparition de maladie en cas de trop grosse variation

- humidité sol
- météo
- ensoleillement

Ces mesures quant à elles nous renseignent essentiellement sur les besoins des vignes, notamment en eau.


Les capteurs seront alimentés via une pile ou une batterie qui faudra changer dans le temps (autonomie à définir).

Les capteurs communiqueront via le protocole LoRa qui nous offre une grande portée qui nous permet de couvrir tout le vignoble sans être dépendant d'un réseau extérieur, ni d'avoir de grosses infrastructures réseaux comme ça pourrait être le cas avec du wifi ou l'utilisation de répéteur à distance régulière.

un bridge LoRa sera aussi a installé dans les bâtiments du vigneron pour récupérer les informations.

en cas de problème de connexion les capteur sont en mesure de stocker leur donnée et de les renvoyer une fois la connexion rétablie


## prise d'image

Pour la prise d'images qui est requise pour alimenter l'IA. Elle sera en mesure d'interpréter des signes caractéristique de maladie.

Nous avons identifié 3 solutions possibles :

### Drone aérien

L'utilisation de drone aérien est à première vue une excellente solution. Cependant, elle pose de gros problèmes dans la mise en place, car une solution autonome est assez chère et une solution manuelle nécessite un pilot formé pour une prise d'image exploitable.
De plus, cette solution est fortement sujette aux conditions climatiques et n'est donc pas utilisable pas temps de plus, vent, brouillard,...
Pour finir, cette solution nous renseigne sur un état global de chaque parcelle, mais elle est limitée dans la prise d'image détaillée des feuilles de vigne.

### Drone terrestre

L'utilisation de drone terrestre permet d'être moins sujet à, c'est problématique environnemental. Elle offre la possibilité d'être au plus proche des plantes ce qui permet d'avoir plus de détails sur l'état des feuilles et donc de réagir plus rapidement à l'apparition de maladie.
Cette solution a néanmoins un inconvénient, cet qu'elle est plus sujette à la topologie du terrain (souvent assez accidenté) et doit par conséquemment être fortement dimensionnée (roue tout terrain, 4 roue motrice,...)

### Cable cam

La solution idéale pour la prise d'image régulière dans un vignoble est selon nous l'utilisation d'une caméra sur câble (cable cam) car elle permet d'avoir un bon entre deux des solutions par drone. En effet, une caméra sur nacelle n'est pas sujette au problème du sol et est quand même moins sujet aléa climatique. Elle est de plus très facile à automatiser. Elle peut être relativement proche des vignes pour avoir plus de détail dans l'image.
Cette solution a cependant besoins d'une installation conséquente, car elle nécessite l'installation de plusieurs mats sur lesquels les câbles seront reliés.

# Voltron GreenTech - NAN-2 - Section IA
Cette section du repository est consacré au travail de la section IA NAN-2 sur le sujet GreenTech du projet Voltron.

## Groupe
Le groupe de travail de la section IA est composé de :
- CLAVIER Eliott
- PIGNON Nathan
- RIPAULT Paul
- BOUCHET Valentin

## Présentation du POC
Le groupe de travail de la section IA a établi un POC répondant à deux problématiques:
- anticiper la détection de maladies dans les vignobles du client
- optimiser l'irrigation des vignes

![image](https://github.com/Nathan-Pignon/T-MAJ-800/assets/58919064/c66df97b-811b-4515-89e4-4123d475a3fa)

![image](https://github.com/Nathan-Pignon/T-MAJ-800/assets/58919064/9d5b03b9-d0dd-467a-b5d1-231568b379bc)

D'abord, l'équipe IA est de créer une intelligence artificielle permettant de détecter de manière prématurée les maladies de la vigne. Pour cela, des images des vignes sont fournies en temps réel à l’intelligence artificielle qui analuse ces dernières et détecte les maladies. Cette intelligence artificielle est ensuite servie par le biais d'une interface où le vigneron peut somuettre des images sur lesquelles l'intelligence artificielle livre des prédictions. Ces prédictions sont accompagnés de "heatmaps" permettant de comprendre les caractéristiques sur lesquels l'intelligence artificielle a porté son attention.

Sur cette interface de POC, l'équipe de la section IA a également implémenté une démonstration de l'intégration de l'équation Penman-Monteith, qui permet de calculer l'irrigation optimale à fournir aux vignes selon plusieurs critères géographiques et météorologiques. Des statistiques mensuelles et annuelles sont également transmises par des graphiques.

![image](https://github.com/Nathan-Pignon/T-MAJ-800/assets/58919064/ecabca61-8644-4748-937e-d0b383183204)

![image](https://github.com/Nathan-Pignon/T-MAJ-800/assets/58919064/f7492e16-4948-4fdb-8949-2b64515c5d96)

![image](https://github.com/Nathan-Pignon/T-MAJ-800/assets/58919064/6853611f-644a-4809-9265-8ee9535673fb)

## Documentation
Plusieurs documents sont disponibles pour la section IA :
- [Un document de spécification techniques et de proposition de valeur](documents/VOLTRON%20-%20Spécifications%20IA%20v.2.pdf)
- [Un tableau des coûts de mise en place de la solution proposée](documents/VOLTRON%20-%20Tableau%20des%20coûts.xlsx)
- [Un document de justification des coûts de mise en place de la solution proposée](documents/VOLTRON%20-%20Justification%20des%20coûts%20et%20explication%20de%20la%20procédure.pdf)
- [Un document explicatif de l'intégration de l'équation Penman-Monteith](documents/VOLTRON%20-%20Intégration%20Penman-Monteith%20et%20calcul%20d'irrigation.pdf)
- [Un document complémentaire aux notebooks sur recherches sur le CNN](documents/VOLTRON%20-%20CNN%20-%20Détection%20maladies.pdf)

 _Vous trouverez également l'ensemble de ces documents à jour et versionnés [sur ce lien Google Drive.](https://drive.google.com/drive/folders/1LN4IbbcflLLJx0nflg_llQ_aKdlhDj_y?usp=sharing)_

## Installation
Dans le répertoire racine du projet IA, exécutez les commandes suivantes :
```powershell
python -m venv env
```

```powershell
env\Scripts\activate
```

```powershell
pip install -r requirements.txt
```

## Lancement
Une fois l'environnement virtual configuré, exécutez les commandes suivantes pour lancer l'application :
```powershell
cd app
```

```powershell
flask run
```

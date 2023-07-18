# Voltron GreenTech - NAN-2 - Section IA
Cette section du repository est consacré au travail de la section IA NAN-2 sur le sujet GreenTech du projet Voltron.

## Groupe
Le groupe de travail de la section IA est composé de :
- CLAVIER Eliott
- PIGNON Nathan
- RIPAULT Paul
- BOUCHET Valentin

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
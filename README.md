# STAGE L3 Informatique

4 grands objectifs :

- Détecter les os d'un corps depuis une caméra. **Done**
- Enregistrer ces mouvements. **Done**
- Animer un rig dans blender avec ces mouvements. **To do**
- Créer une IA pour corriger les mouvements d'arts martiaux. **To do**

Nous sommes actuellement en train de travailler sur une solution à deux webcam pour une précision accrue des points enregistrés

## Prerequis

Avoir python d'installé.
Testé sous **Python 3.12.3**

Pour pouvoir éxécuter le programme, veuillez être certains de l'installation des modules pythons suivants :

```bash
pip install opencv-python
pip install mediapipe
pip install vedo
```

L'installation devrait être complète.

### Copie du repository

Depuis un terminal, après avoir sélectionné l'endroit désiré, entrez la commande :

```bash
git clone https://github.com/mrktttt/STAGE-L3.git
```

### Exécution du programme

Avant de pouvoir utiliser efficacement le programme, munissez vous du damier fourni au format pdf imprimé sur une feuille A4. **Checkerboard-A2-70mm-7x4.pdf**

Il faudra ensuite capturer entre 10 et 20 photos en gardant le damier plutôt plat.

```bash
python3 captureCalibrationImages.py
```

Appuyez sur espace pour prendre une photo.

Ensuite il faudra calibrer et tester la calibration dans le programme cameraCalibration.py en exécutant la commande :

```bash
python3 cameraCalibration.py
```

Option n°1 : Appliquer une calibration

Option n°2 : Tester la calibration

Finalement, vous pouvez commencer la détection avec le programme principal :

```bash
python3 detection.py
```

En appuyant sur **"r"** il est possible d'enregistrer un mouvement. Ensuite vous pourrez relire ce mouvement en utilisant le programme :

```bash
python3 animationTest.py
```

## Auteurs

- Mya Soudain
- Killian Treuil
